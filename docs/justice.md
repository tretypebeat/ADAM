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

Default thresholds, used unless a case states its own:

- **Consistency**: two parties count as equal on C when their measures match
  exactly (or within the stated measurement error).
- **Position-neutrality**: a position fails when its acceptance rate is more
  than 20 percentage points below the highest position's rate.
- **Remedy**: a remedy is proportionate when it is within 10% of the harm.

## What each criterion makes observable

Tests 1 and 2 need a number for C for every affected party. Tests 3 to 5 read
the same whatever C is. The table says what to measure for each criterion and
what a just outcome looks like under tests 1 and 2.

| C | Measure for each party | Consistency passes when... | Proportionality passes when... |
|---|------------------------|----------------------------|--------------------------------|
| **Desert** | A score for the conduct being judged: offence severity and culpability for a penalty, merit for a reward. The scale is fixed before outcomes are seen. | parties with the same conduct score get the same outcome. | a worse score never gets a lighter penalty, and a better score never gets a smaller reward. |
| **Need** | The shortfall between what the party has and a stated threshold (food, shelter, care), on one scale for everyone. | parties with the same shortfall get the same outcome. | more shortfall never gets less. |
| **Contribution** | What the party put in, in a stated unit: hours, output, capital, risk taken. | parties who put in the same get the same outcome. | putting in more never gets less. |
| **Equality** | The same value for everyone. There is nothing to measure. | every party gets the same outcome. With C equal for all, tests 1 and 2 collapse into this one check. | the spread of outcomes is zero, or within the stated rounding. |
| **Harm** | The harm the party caused (for a penalty) or suffered (for compensation), in a stated unit such as money or days lost. State which direction applies. | parties with the same harm get the same outcome. | more harm caused never gets a lighter penalty, and more harm suffered never gets less compensation. |

An outcome is just under C when tests 1 and 2 pass on that measure and tests
3 to 5 pass or don't apply. If the measure for C can't be stated, the case
can't be judged under that C, and the profile should say "not assessed"
rather than guess.

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

## Worked examples

Each example states C first, then runs the five tests. The numbers are made up
to show the method.

### 1. Disaster aid, judged under need and under contribution

Four households receive aid after a flood. Need is scored 1 to 3 and
contribution (hours volunteered in the recovery, scored 1 to 3) is recorded
too. The allocation committee gave notice, held hearings and stated reasons,
and its members had no stake, but there is no appeal. Asked whether they
would accept the rule without knowing their district, 78% of the north and
71% of the south said yes.

| Household | District | Need | Contribution | Aid |
|-----------|----------|------|--------------|-----|
| A | north | 3 | 1 | 300 |
| B | south | 3 | 2 | 100 |
| C | north | 2 | 2 | 200 |
| D | south | 1 | 3 | 50 |

```
C: need
1 Consistency         fail     (A and B both have need 3 but got 300 and 100; they differ only in district)
2 Proportionality     fail     (1 inversion in 5 pairs: B has more need than C but got less)
3 Procedure           4/5      (no appeal)
4 Position-neutrality pass     (78% vs 71%, a 7-point gap)
5 Remedy              n/a      (no demonstrated wrong)

C: contribution
1 Consistency         fail     (B and C both contributed 2 but got 100 and 200)
2 Proportionality     fail     (5 inversions in 5 pairs: aid falls as contribution rises)
3 Procedure           4/5      (no appeal)
4 Position-neutrality pass     (78% vs 71%)
5 Remedy              n/a      (no demonstrated wrong)
```

**Reading it.** The allocation is unjust under need, and the cause is
visible: household B got a third of what A got at the same need, and the only
difference is district. Under contribution it is even further off, because
aid runs in the opposite order to contribution. That second result isn't a
flaw in the method. It shows the two criteria pull apart, and someone has to
decide which one aid should track.

### 2. Sentencing, judged under desert

Two people are convicted of the same theft, with the same value stolen and
no prior record, so their desert scores are equal. One hired a private
lawyer and received 6 months. The other had an overworked public defender and
received 18 months. Both had notice, a hearing, a reasoned judgment, an
impartial judge and a right of appeal.

```
C: desert
1 Consistency         fail     (equal desert, 6 vs 18 months; they differ only in wealth)
2 Proportionality     n/a      (both have the same desert, so there is nothing to rank)
3 Procedure           5/5
4 Position-neutrality not assessed (no acceptance survey)
5 Remedy              n/a      (no wrong against either party has been established)
```

**Reading it.** A perfect procedure score didn't prevent an unjust outcome.
Proportionality can't help with two equal cases. The swap test catches what the checklist misses: the formal steps were all
present, but the outcome changed with an attribute that desert says is
irrelevant.

### 3. A club vote, judged under equality

A club decides by vote. Its 10 founding members get 2 votes each and its 30
newer members get 1 vote each. When asked whether they would accept the rule
without knowing which kind of member they would be, 95% of founders said yes
and 40% of newer members did.

```
C: equality
1 Consistency         fail     (members get 1 or 2 votes; equality requires everyone to get the same)
2 Proportionality     fail     (spread of outcomes is 1 vote, should be 0)
3 Procedure           5/5      (the rule is published, debated, reasoned, chaired neutrally, appealable)
4 Position-neutrality fail     (95% vs 40%, a 55-point gap)
5 Remedy              n/a
```

**Reading it.** Under equality the first two tests reduce to one question:
does everyone get the same? They don't. The veil test agrees independently:
the rule is acceptable only to the people it favours. If the club argued the
extra vote tracks contribution (founders built the club), the right move is to
rerun the tests under contribution and see whether the numbers support that,
not to keep calling it equal.

### 4. A chemical spill, judged under harm

A factory spill damages three farms. Losses are assessed at 10,000, 10,000
and 40,000. The factory pays 10,000, 10,000 and 20,000 after a process with
notice, hearings, reasons, an independent assessor and an appeal. The wrong is
established, so the remedy test applies.

```
C: harm (suffered)
1 Consistency         pass     (the two farms with equal losses got equal payments)
2 Proportionality     pass     (no inversions: the largest loss got the largest payment)
3 Procedure           5/5
4 Position-neutrality not assessed
5 Remedy              partial  (farms 1 and 2 fully restored; farm 3 restored to 50%, a gap of 20,000)
```

**Reading it.** The payments are in the right order and treat equal cases
alike, so tests 1 and 2 pass. Test 5 catches the problem they can't: being in
the right order is not the same as being the right size. The largest loss was
only half repaid. This is why the profile is reported test by test. An average
would make this case look mostly just and hide the 20,000 shortfall.

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
