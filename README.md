# ADAM

*A device, a man.*

ADAM is a device intended for people. At its core is a **ledger**: a record of
what each person has done, who judged it, and why, kept so that nobody can
quietly rewrite it.

## Purpose

ADAM works in two steps, in this order:

1. **Money.** Build up the resources to do anything at all.
2. **Rectification.** Use them to put wrongs right, judged against a stated
   definition of justice instead of whoever happens to be in charge.

The ledger connects the two. Every decision about who earned what is written
down, signed and open to appeal, so both the money and the rectification can be
checked by the people they affect.

## The ledger

The ledger is a single Python script that keeps two append-only files:

- `ledger.jsonl` holds every change to a person's standing and every change to
  the rules.
- `audit_log.jsonl` holds every grading decision: the submission, the grade and
  the reasoning.

How it works:

- **Tamper-evident.** Each line carries a hash of itself and of the line before
  it, so an altered or deleted line breaks the chain.
- **Signed.** Every decision names who made it (a named human, an examiner or a
  formula) and is signed with that decider's ed25519 key.
- **Published rules.** Each task lists its criteria. A pass means every
  criterion was met, and a fail says which ones weren't. A rule change binds
  nobody until its fingerprint has been delivered to everyone it affects.
- **Appeals.** Anyone can contest a decision about their own work, and the
  person who made the decision can't grade the appeal.
- **No transfers.** No command moves standing from one person to another.
  Standing is earned, never handed over.

### Using the merit ledger

`ledger.py` implements the merit part of the ledger today: signed,
hash-chained entries recording points for a person and the reason. The audit
log, published rules and appeals described above are not built yet.

It needs Python 3.9+ and the `cryptography` package
(`pip install -r requirements.txt`).

```sh
# Make a signing key. Prints the public key; keep the .pem file private.
python3 ledger.py keygen alice.pem

# Record merit, signed by that key and chained to the previous entry.
python3 ledger.py append --key alice.pem --person bob --points 3 --reason "fixed the pump"

# Check every hash, signature and chain link. Exits 1 on any problem.
python3 ledger.py verify
python3 ledger.py verify --trust <public key hex>   # also reject unknown signers

python3 ledger.py show        # list entries
python3 ledger.py standings   # total points per person
```

Pass `--ledger PATH` before the command to use a file other than
`ledger.jsonl`.

Each line holds `seq`, `prev` (the previous entry's hash, or 64 zeros for the
first), `time`, `signer` (public key), `body`, `sig` and `hash`. The signature
covers everything except `sig` and `hash`; the hash covers everything except
itself. Editing, deleting or reordering a line breaks verification. Anyone can
make a valid chain with their own key, so use `--trust` to say whose
signatures count.

Run the tests with `python3 -m unittest -v`.

## Justice

Rectification needs a definition of justice that can actually be checked.
[docs/justice.md](docs/justice.md) defines it with five tests (consistency,
proportionality, procedure, position-neutrality and remedy), each run against a
criterion that has to be stated up front.

## Docs

- [Justice: an operational definition](docs/justice.md)

## Status

ADAM is at an early stage. The ledger runs and has tests, but it hasn't been
added to this repository yet. The justice definition and its code are in open
pull requests, along with a first hardware build (a gauntlet).
