import io
import json
import os
import stat
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

import ledger


class LedgerTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "ledger.jsonl")
        self.key_path = os.path.join(self.dir.name, "key.pem")
        self.pub = ledger.generate_key(self.key_path)
        self.key = ledger.load_key(self.key_path)

    def tearDown(self):
        self.dir.cleanup()

    def add(self, person="alice", points=1, reason="did a thing", key=None):
        return ledger.append(self.path, key or self.key,
                             {"person": person, "points": points, "reason": reason})

    def rewrite(self, entries):
        with open(self.path, "w", encoding="utf-8") as f:
            for e in entries:
                f.write(json.dumps(e) + "\n")

    # keys

    def test_keygen_writes_private_file_and_returns_public_key(self):
        mode = stat.S_IMODE(os.stat(self.key_path).st_mode)
        self.assertEqual(mode, 0o600)
        self.assertEqual(len(self.pub), 64)
        self.assertEqual(ledger.public_hex(self.key), self.pub)

    def test_keygen_refuses_to_overwrite(self):
        with self.assertRaises(FileExistsError):
            ledger.generate_key(self.key_path)

    # appending

    def test_append_chains_entries(self):
        a = self.add()
        b = self.add(person="bob", points=3)
        self.assertEqual(a["seq"], 0)
        self.assertEqual(a["prev"], ledger.GENESIS)
        self.assertEqual(b["seq"], 1)
        self.assertEqual(b["prev"], a["hash"])
        self.assertEqual(b["signer"], self.pub)
        self.assertEqual(ledger.verify(self.path), [])

    def test_empty_ledger_verifies(self):
        self.assertEqual(ledger.verify(self.path), [])

    def test_append_refuses_broken_ledger(self):
        self.add()
        entries = ledger.read_entries(self.path)
        entries[0]["body"]["points"] = 100
        self.rewrite(entries)
        with self.assertRaises(ledger.LedgerError):
            self.add()

    # tampering

    def test_detects_edited_body(self):
        self.add()
        self.add()
        entries = ledger.read_entries(self.path)
        entries[0]["body"]["points"] = 100
        self.rewrite(entries)
        errors = ledger.verify(self.path)
        self.assertTrue(any("entry 0: hash" in e for e in errors))
        self.assertTrue(any("entry 0: bad signature" in e for e in errors))

    def test_detects_recomputed_hash_without_valid_signature(self):
        self.add()
        entries = ledger.read_entries(self.path)
        e = entries[0]
        e["body"]["points"] = 100
        e["hash"] = ledger.hashlib.sha256(ledger.canonical(ledger._hashed_part(e))).hexdigest()
        self.rewrite(entries)
        self.assertEqual(ledger.verify(self.path), ["entry 0: bad signature"])

    def test_detects_deleted_entry(self):
        for i in range(3):
            self.add(points=i)
        entries = ledger.read_entries(self.path)
        del entries[1]
        self.rewrite(entries)
        errors = ledger.verify(self.path)
        self.assertIn("entry 1: seq is 2, expected 1", errors)
        self.assertIn("entry 1: prev does not match hash of entry 0", errors)

    def test_detects_reordered_entries(self):
        self.add(points=1)
        self.add(points=2)
        entries = ledger.read_entries(self.path)
        self.rewrite(entries[::-1])
        self.assertTrue(ledger.verify(self.path))

    def test_detects_resigned_entry_by_other_key(self):
        # A forger with their own key can produce a self-consistent chain;
        # only a trusted-key check catches it.
        other = ledger.Ed25519PrivateKey.generate()
        self.add()
        self.add(key=other)
        self.assertEqual(ledger.verify(self.path), [])
        errors = ledger.verify(self.path, trusted={self.pub})
        self.assertEqual(len(errors), 1)
        self.assertIn("entry 1: signed by untrusted key", errors[0])

    def test_reports_invalid_json(self):
        self.add()
        with open(self.path, "a") as f:
            f.write("{not json\n")
        self.assertEqual(len(ledger.verify(self.path)), 1)

    def test_reports_missing_fields(self):
        self.rewrite([{"seq": 0}])
        self.assertTrue(any("missing field" in e for e in ledger.verify(self.path)))

    # standings

    def test_standings(self):
        self.add("alice", 2)
        self.add("bob", 5)
        self.add("alice", -1)
        self.assertEqual(ledger.standings(ledger.read_entries(self.path)),
                         {"alice": 1, "bob": 5})

    # CLI

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = ledger.main(["--ledger", self.path, *args])
        return code, out.getvalue(), err.getvalue()

    def test_cli_round_trip(self):
        key2 = os.path.join(self.dir.name, "k2.pem")
        code, out, _ = self.run_cli("keygen", key2)
        self.assertEqual(code, 0)
        pub2 = out.strip()

        code, out, _ = self.run_cli("append", "--key", key2, "--person", "carol",
                                    "--points", "4", "--reason", "fixed the pump")
        self.assertEqual(code, 0)
        self.assertIn("appended entry 0", out)

        self.assertEqual(self.run_cli("verify")[0], 0)
        self.assertEqual(self.run_cli("verify", "--trust", pub2)[0], 0)
        self.assertEqual(self.run_cli("verify", "--trust", self.pub)[0], 1)

        code, out, _ = self.run_cli("standings")
        self.assertEqual(out, "carol\t4\n")

        code, out, _ = self.run_cli("show")
        self.assertIn("fixed the pump", out)

    def test_cli_verify_fails_on_tamper(self):
        self.add()
        entries = ledger.read_entries(self.path)
        entries[0]["body"]["reason"] = "something else"
        self.rewrite(entries)
        code, _, err = self.run_cli("verify")
        self.assertEqual(code, 1)
        self.assertIn("entry 0", err)


if __name__ == "__main__":
    unittest.main()
