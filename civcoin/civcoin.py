"""civcoin: ADAM's money, kept in a tamper-evident book.

civcoin is the "money" step of ADAM. It is a unit that can be spent and paid,
unlike ledger standing, which can never be handed over. Three rules keep it
tied to the rest of ADAM:

1. Minted only for recorded work. A mint must cite the ledger decision that
   judged the work, and the decider who signed it.
2. Spent like money. Holders can pay each other, but nobody can spend more
   than they hold, and civcoin never buys standing.
3. Remedies are checked. A remedy payment states the harm it answers and is
   flagged when it is not within REMEDY_TOLERANCE of that harm, the same
   threshold test 5 of docs/justice.md uses.

The book is one append-only JSONL file. Each line carries the hash of the
line before it and of itself, so an altered or deleted line breaks the chain.
See civcoin/README.md for the design and its open assumptions.

Usage:
    python civcoin.py --book civcoin.jsonl mint alice 10 --decision D-1 --by examiner
    python civcoin.py --book civcoin.jsonl pay alice bob 3
    python civcoin.py --book civcoin.jsonl remedy fund carol 50 --harm 50 --by panel
    python civcoin.py --book civcoin.jsonl balance alice
    python civcoin.py --book civcoin.jsonl verify
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

# Hash that the first entry links back to.
GENESIS = "0" * 64
# Same as test 5 of docs/justice.md: a remedy within this fraction of the harm
# counts as proportionate.
REMEDY_TOLERANCE = 0.1


class CivcoinError(Exception):
    pass


def _hash(body: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()


def _amount(value: float) -> float:
    value = float(value)
    if value <= 0:
        raise CivcoinError("amount must be positive")
    return value


def is_proportionate(harm: float, restored: float) -> bool:
    return abs(restored - harm) <= REMEDY_TOLERANCE * harm


class Book:
    """An append-only, hash-chained record of every civcoin movement."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.entries: list[dict[str, Any]] = []
        if self.path.exists():
            with self.path.open() as f:
                self.entries = [json.loads(line) for line in f if line.strip()]

    def _append(self, body: dict[str, Any]) -> dict[str, Any]:
        body = {"seq": len(self.entries), "prev": self.head(), **body}
        entry = {**body, "hash": _hash(body)}
        with self.path.open("a") as f:
            f.write(json.dumps(entry, sort_keys=True) + "\n")
        self.entries.append(entry)
        return entry

    def head(self) -> str:
        return self.entries[-1]["hash"] if self.entries else GENESIS

    def balances(self) -> dict[str, float]:
        totals: dict[str, float] = defaultdict(float)
        for e in self.entries:
            if e["kind"] == "mint":
                totals[e["to"]] += e["amount"]
            else:
                totals[e["from"]] -= e["amount"]
                totals[e["to"]] += e["amount"]
        return dict(totals)

    def balance(self, holder: str) -> float:
        return self.balances().get(holder, 0.0)

    def mint(self, to: str, amount: float, decision: str, by: str) -> dict[str, Any]:
        if not decision or not by:
            raise CivcoinError("a mint must cite a ledger decision and its decider")
        return self._append({"kind": "mint", "to": to, "amount": _amount(amount),
                             "decision": decision, "by": by})

    def pay(self, sender: str, to: str, amount: float) -> dict[str, Any]:
        amount = _amount(amount)
        if sender == to:
            raise CivcoinError("cannot pay yourself")
        if self.balance(sender) < amount:
            raise CivcoinError(f"{sender} holds {self.balance(sender)}, cannot pay {amount}")
        return self._append({"kind": "pay", "from": sender, "to": to, "amount": amount})

    def remedy(self, source: str, to: str, amount: float, harm: float, by: str) -> dict[str, Any]:
        amount = _amount(amount)
        harm = _amount(harm)
        if not by:
            raise CivcoinError("a remedy must name its decider")
        if self.balance(source) < amount:
            raise CivcoinError(f"{source} holds {self.balance(source)}, cannot pay {amount}")
        return self._append({"kind": "remedy", "from": source, "to": to, "amount": amount,
                             "harm": harm, "by": by,
                             "proportionate": is_proportionate(harm, amount)})

    def verify(self) -> list[str]:
        """Return one problem per broken link; an empty list means the chain holds."""
        problems = []
        prev = GENESIS
        for i, e in enumerate(self.entries):
            body = {k: v for k, v in e.items() if k != "hash"}
            if e.get("seq") != i:
                problems.append(f"line {i}: sequence is {e.get('seq')}, expected {i}")
            if e.get("prev") != prev:
                problems.append(f"line {i}: does not link to the line before it")
            if _hash(body) != e.get("hash"):
                problems.append(f"line {i}: contents do not match its hash")
            prev = e.get("hash")
        return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Keep ADAM's civcoin book.")
    parser.add_argument("--book", default="civcoin.jsonl")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("mint")
    p.add_argument("to")
    p.add_argument("amount", type=float)
    p.add_argument("--decision", required=True)
    p.add_argument("--by", required=True)

    p = sub.add_parser("pay")
    p.add_argument("sender")
    p.add_argument("to")
    p.add_argument("amount", type=float)

    p = sub.add_parser("remedy")
    p.add_argument("source")
    p.add_argument("to")
    p.add_argument("amount", type=float)
    p.add_argument("--harm", type=float, required=True)
    p.add_argument("--by", required=True)

    p = sub.add_parser("balance")
    p.add_argument("holder")

    sub.add_parser("verify")

    args = parser.parse_args(argv)
    book = Book(args.book)
    try:
        if args.command == "mint":
            print(json.dumps(book.mint(args.to, args.amount, args.decision, args.by)))
        elif args.command == "pay":
            print(json.dumps(book.pay(args.sender, args.to, args.amount)))
        elif args.command == "remedy":
            entry = book.remedy(args.source, args.to, args.amount, args.harm, args.by)
            print(json.dumps(entry))
            if not entry["proportionate"]:
                print("warning: remedy is not within 10% of the harm", file=sys.stderr)
        elif args.command == "balance":
            print(book.balance(args.holder))
        elif args.command == "verify":
            problems = book.verify()
            for problem in problems:
                print(problem)
            print("chain holds" if not problems else "chain broken")
            return 1 if problems else 0
    except CivcoinError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
