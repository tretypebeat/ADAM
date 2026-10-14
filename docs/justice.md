# Justice: an operational definition

An operational definition says what you would observe or do to decide whether
something is just. It can't rest on words like "fairness" or "what people
deserve", because those only move the question somewhere else.

One part can't be operationalized away: the **criterion**, meaning what the
outcome should track. That is a value choice, so this definition takes it as an
explicit input and makes everything else checkable around it.

## Definition

> A decision, rule, or outcome is **just** to the degree that, given a stated
> criterion **C**, it passes the five tests below for everyone it affects.

## Input: the criterion C

C must be stated before any test is run. Choose one:

| C | The outcome should track... | Example |
|---|------------------------------|---------|
| **Desert** | what each party has earned through their conduct | a sentence matched to the offence |
| **Need** | what each party requires | aid allocated by severity of need |
| **Contribution** | what each party put in | profit split by work or capital invested |
| **Equality** | nothing; everyone gets the same | one person, one vote |
| **Harm** | the harm each party caused or suffered | compensation sized to the damage |

C is chosen per case. There is no default. If a case seems to need two
criteria, run the tests once per criterion and report both profiles; the
conflict between them is part of the answer.

## The five tests

| # | Test | Procedure | Observable |
|---|------|-----------|------------|
| 1 | **Consistency** (swap test) | Hold the C-relevant facts fixed and vary irrelevant attributes (identity, status, wealth, group). | Does the outcome change? Any change is a failure. Measure it as outcome disparity conditional on C. |
| 2 | **Proportionality** | Compare the size of each outcome to the size of C across cases. | Outcomes should rise and fall with C. Measure it as rank correlation between C and outcome, or the count of inversions (cases where more C got less outcome). |
| 3 | **Procedure** | Check whether affected parties had (a) notice of the rule, (b) a chance to be heard, (c) stated reasons, (d) an impartial decider, and (e) an appeal route. | A checklist score out of 5. |
| 4 | **Position-neutrality** (veil test) | State the rule without reference to who benefits. Ask people from each affected position whether they would accept it without knowing which position they would hold. | Acceptance rate per position. The rule fails if any position's rate is far below the others. |
| 5 | **Remedy** | For a demonstrated wrong, check whether the response restores the harmed party and is proportionate to the harm. | Restoration achieved (yes / partial / no), and the gap between harm and remedy. |

## Output: a profile, not a single number

Report the result of each test separately, alongside the C that was used:

```
C: need
1 Consistency         pass   (no disparity across groups at equal need)
2 Proportionality     fail   (3 inversions in 40 cases)
3 Procedure           4/5    (no appeal route)
4 Position-neutrality pass   (acceptance 71–78% across positions)
5 Remedy              n/a    (no demonstrated wrong)
```

Collapsing the five into one score hides which kind of injustice is occurring,
and the tests can pull against each other, for example when proportionality to
desert violates need. A profile keeps that visible.

## Scope and limits

- **It measures fairness as evidenced**, not the whole concept of justice.
  Tests 1 to 3 are about as operational as this gets. Tests 4 and 5 depend more
  on judgment.
- **The choice of C does the moral work.** Two people can agree on every test
  result and still disagree about whether an outcome is just, because they
  picked different criteria. That disagreement should surface openly rather
  than hide inside the tests.
- **It evaluates decisions, not people or societies.** Judging an institution
  means running the tests over many of its decisions and aggregating.
