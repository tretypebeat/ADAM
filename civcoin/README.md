# civcoin

civcoin is ADAM's money. ADAM works in two steps, money and then
rectification, and civcoin is the unit that carries value through both: it is
earned in the first step and paid out as remedies in the second.

This is a starting design. Anything marked **Assumption** is a guess to be
confirmed or corrected.

## How it fits with the ledger

The ledger records **standing**, and standing can never be handed over. Money
has to move, or it isn't money. So civcoin is kept apart from standing:

| | Standing (ledger) | civcoin |
|---|---|---|
| How you get it | earned through graded work | minted only against a graded decision in the ledger |
| Can it move? | never | yes, holder to holder |
| Can one buy the other? | no | no: civcoin never buys standing |
| Record | `ledger.jsonl`, hash-chained | `civcoin.jsonl`, hash-chained |

## The three rules

1. **Minted only for recorded work.** Every mint cites the ledger decision
   that judged the work (`--decision`) and the decider who signed it (`--by`).
   Nothing else creates civcoin.
2. **Spent like money.** Holders can pay each other. Nobody can spend more
   than they hold.
3. **Remedies are checked.** A remedy payment states the harm it answers.
   It is flagged as disproportionate when it is not within 10% of that harm,
   the same threshold as test 5 (remedy) in
   [docs/justice.md](../docs/justice.md).

## The book

`civcoin.py` keeps one append-only file, `civcoin.jsonl`. Each line holds a
sequence number, the hash of the line before it and a hash of itself, so an
edited, deleted or reordered line breaks the chain and `verify` reports it.

```
python civcoin/civcoin.py mint alice 10 --decision D-1 --by examiner
python civcoin/civcoin.py pay alice bob 3
python civcoin/civcoin.py remedy fund carol 50 --harm 50 --by panel
python civcoin/civcoin.py balance alice
python civcoin/civcoin.py verify
```

Tests: `python -m unittest discover -s civcoin -v`

## Assumptions and open questions

- **Assumption:** "civcoin is with TSP" means civcoin belongs to TSP. What
  TSP stands for isn't defined anywhere in ADAM yet, so this design doesn't
  depend on it.
- **Assumption:** civcoin is a book kept by ADAM, not a blockchain token. The
  hash chain gives tamper evidence without a network. It could be put on a
  public chain later.
- **Assumption:** how much civcoin a graded decision is worth is set by
  whoever mints it. A fixed rate per criterion, published like the ledger's
  rules, would be the natural next step.
- **Not yet done:** entries are not signed with the decider's SSH key the way
  ledger lines are, and a mint doesn't check that the cited decision actually
  exists in `ledger.jsonl`. Both wait for the ledger to land in this repo.
- **Not yet done:** cutting lines off the *end* of the book can't be detected
  from the file alone. Publishing the latest head hash somewhere else fixes
  that, the same way the ledger delivers rule fingerprints.
