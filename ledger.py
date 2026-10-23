#!/usr/bin/env python3
"""ADAM merit ledger: an append-only, hash-chained, ed25519-signed record.

Each line of the ledger file is one JSON entry:

    {"seq": 0, "prev": "<sha256 of previous entry, or 64 zeros>",
     "time": "<UTC ISO 8601>", "signer": "<ed25519 public key, hex>",
     "body": {...}, "sig": "<ed25519 signature, hex>", "hash": "<sha256, hex>"}

The signature covers every field except "sig" and "hash". The hash covers every
field except "hash", so it also commits to the signature. Fields are serialised
as canonical JSON (sorted keys, no whitespace) before signing and hashing.
"""

import argparse
import fcntl
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

GENESIS = "0" * 64


class LedgerError(Exception):
    pass


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def public_hex(private_key):
    raw = private_key.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )
    return raw.hex()


# --- keys -------------------------------------------------------------------

def generate_key(path):
    """Write a new ed25519 private key to `path` (mode 0600) and return its public key hex."""
    key = Ed25519PrivateKey.generate()
    pem = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(pem)
    return public_hex(key)


def load_key(path):
    with open(path, "rb") as f:
        key = serialization.load_pem_private_key(f.read(), password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise LedgerError(f"{path} is not an ed25519 private key")
    return key


# --- entries ----------------------------------------------------------------

def _signed_part(entry):
    return {k: v for k, v in entry.items() if k not in ("sig", "hash")}


def _hashed_part(entry):
    return {k: v for k, v in entry.items() if k != "hash"}


def make_entry(key, body, seq, prev, time=None):
    entry = {
        "seq": seq,
        "prev": prev,
        "time": time or datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "signer": public_hex(key),
        "body": body,
    }
    entry["sig"] = key.sign(canonical(_signed_part(entry))).hex()
    entry["hash"] = hashlib.sha256(canonical(_hashed_part(entry))).hexdigest()
    return entry


def read_entries(path):
    if not os.path.exists(path):
        return []
    entries = []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise LedgerError(f"line {lineno}: not valid JSON ({e.msg})")
    return entries


def append(path, key, body):
    """Sign `body` and append it to the ledger, chained to the last entry."""
    with open(path, "a+", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            errors = verify(path)
            if errors:
                raise LedgerError("refusing to append to a broken ledger: " + errors[0])
            entries = read_entries(path)
            prev = entries[-1]["hash"] if entries else GENESIS
            entry = make_entry(key, body, len(entries), prev)
            f.write(canonical(entry).decode() + "\n")
            f.flush()
            os.fsync(f.fileno())
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
    return entry


# --- verification -----------------------------------------------------------

def verify_entry(entry):
    """Return a list of problems with a single entry's hash and signature."""
    required = ("seq", "prev", "time", "signer", "body", "sig", "hash")
    missing = [k for k in required if k not in entry]
    if missing:
        return ["missing field(s): " + ", ".join(missing)]
    problems = []
    if hashlib.sha256(canonical(_hashed_part(entry))).hexdigest() != entry["hash"]:
        problems.append("hash does not match contents")
    try:
        pub = Ed25519PublicKey.from_public_bytes(bytes.fromhex(entry["signer"]))
        pub.verify(bytes.fromhex(entry["sig"]), canonical(_signed_part(entry)))
    except (ValueError, TypeError):
        problems.append("malformed signer or signature")
    except InvalidSignature:
        problems.append("bad signature")
    return problems


def verify(path, trusted=None):
    """Check every entry's hash, signature and link to its predecessor.

    `trusted` is an optional set of public key hexes; entries signed by any
    other key are reported. Returns a list of error strings (empty means valid).
    """
    try:
        entries = read_entries(path)
    except LedgerError as e:
        return [str(e)]
    errors = []
    prev = GENESIS
    for i, entry in enumerate(entries):
        for p in verify_entry(entry):
            errors.append(f"entry {i}: {p}")
        if entry.get("seq") != i:
            errors.append(f"entry {i}: seq is {entry.get('seq')!r}, expected {i}")
        if entry.get("prev") != prev:
            errors.append(f"entry {i}: prev does not match hash of entry {i - 1}" if i else
                          f"entry {i}: prev is not the genesis value")
        if trusted is not None and entry.get("signer") not in trusted:
            errors.append(f"entry {i}: signed by untrusted key {entry.get('signer')}")
        prev = entry.get("hash")
    return errors


def standings(entries):
    """Total merit points per person."""
    totals = {}
    for e in entries:
        body = e.get("body", {})
        if "person" in body and "points" in body:
            totals[body["person"]] = totals.get(body["person"], 0) + body["points"]
    return totals


# --- CLI --------------------------------------------------------------------

def main(argv=None):
    p = argparse.ArgumentParser(prog="ledger", description="ADAM merit ledger")
    p.add_argument("--ledger", default="ledger.jsonl", help="ledger file (default: ledger.jsonl)")
    sub = p.add_subparsers(dest="cmd", required=True)

    kg = sub.add_parser("keygen", help="create an ed25519 signing key")
    kg.add_argument("out", help="where to write the private key")

    ap = sub.add_parser("append", help="sign and append a merit entry")
    ap.add_argument("--key", required=True, help="private key file")
    ap.add_argument("--person", required=True)
    ap.add_argument("--points", required=True, type=int)
    ap.add_argument("--reason", required=True)

    vf = sub.add_parser("verify", help="check hashes, signatures and the chain")
    vf.add_argument("--trust", action="append", metavar="PUBKEY",
                    help="only accept entries signed by this public key (repeatable)")

    sub.add_parser("show", help="print every entry")
    sub.add_parser("standings", help="print total points per person")

    args = p.parse_args(argv)
    try:
        if args.cmd == "keygen":
            print(generate_key(args.out))
        elif args.cmd == "append":
            body = {"person": args.person, "points": args.points, "reason": args.reason}
            entry = append(args.ledger, load_key(args.key), body)
            print(f"appended entry {entry['seq']} {entry['hash']}")
        elif args.cmd == "verify":
            errors = verify(args.ledger, set(args.trust) if args.trust else None)
            for e in errors:
                print(e, file=sys.stderr)
            if errors:
                return 1
            print(f"ok: {len(read_entries(args.ledger))} entries")
        elif args.cmd == "show":
            for e in read_entries(args.ledger):
                b = e["body"]
                print(f"{e['seq']:>4}  {e['time']}  {e['signer'][:12]}  {json.dumps(b, ensure_ascii=False)}")
        elif args.cmd == "standings":
            for person, pts in sorted(standings(read_entries(args.ledger)).items()):
                print(f"{person}\t{pts}")
    except (LedgerError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
