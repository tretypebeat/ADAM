import json
import tempfile
import unittest
from pathlib import Path

from civcoin import Book, CivcoinError, main


class BookTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = Path(self.dir.name) / "civcoin.jsonl"
        self.book = Book(self.path)

    def tearDown(self):
        self.dir.cleanup()

    def test_mint_requires_a_decision_and_decider(self):
        with self.assertRaises(CivcoinError):
            self.book.mint("alice", 10, decision="", by="examiner")
        with self.assertRaises(CivcoinError):
            self.book.mint("alice", 10, decision="D-1", by="")

    def test_pay_moves_money_and_blocks_overspending(self):
        self.book.mint("alice", 10, decision="D-1", by="examiner")
        self.book.pay("alice", "bob", 4)
        self.assertEqual(self.book.balance("alice"), 6)
        self.assertEqual(self.book.balance("bob"), 4)
        with self.assertRaises(CivcoinError):
            self.book.pay("bob", "alice", 5)

    def test_amounts_must_be_positive(self):
        self.book.mint("alice", 10, decision="D-1", by="examiner")
        with self.assertRaises(CivcoinError):
            self.book.pay("alice", "bob", -1)

    def test_remedy_flags_disproportionate_payments(self):
        self.book.mint("fund", 100, decision="D-1", by="examiner")
        fair = self.book.remedy("fund", "carol", 48, harm=50, by="panel")
        short = self.book.remedy("fund", "dan", 10, harm=50, by="panel")
        self.assertTrue(fair["proportionate"])
        self.assertFalse(short["proportionate"])

    def test_book_survives_reload(self):
        self.book.mint("alice", 10, decision="D-1", by="examiner")
        self.assertEqual(Book(self.path).balance("alice"), 10)

    def test_verify_catches_an_edited_line(self):
        self.book.mint("alice", 10, decision="D-1", by="examiner")
        self.book.pay("alice", "bob", 4)
        self.assertEqual(Book(self.path).verify(), [])
        lines = self.path.read_text().splitlines()
        entry = json.loads(lines[0])
        entry["amount"] = 1000
        lines[0] = json.dumps(entry, sort_keys=True)
        self.path.write_text("\n".join(lines) + "\n")
        self.assertNotEqual(Book(self.path).verify(), [])

    def test_verify_catches_a_deleted_line(self):
        self.book.mint("alice", 10, decision="D-1", by="examiner")
        self.book.mint("bob", 5, decision="D-2", by="examiner")
        self.book.pay("alice", "bob", 1)
        lines = self.path.read_text().splitlines()
        self.path.write_text("\n".join([lines[0], lines[2]]) + "\n")
        self.assertNotEqual(Book(self.path).verify(), [])

    def test_cli_round_trip(self):
        book = str(self.path)
        self.assertEqual(main(["--book", book, "mint", "alice", "10", "--decision", "D-1", "--by", "x"]), 0)
        self.assertEqual(main(["--book", book, "pay", "alice", "bob", "20"]), 2)
        self.assertEqual(main(["--book", book, "verify"]), 0)


if __name__ == "__main__":
    unittest.main()
