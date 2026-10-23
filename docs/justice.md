# The diamond shield: an operational definition of justice

An operational definition says what you would observe or do to decide whether
something is just. It can't rest on words like "fairness" or "what people
deserve", because those only move the question somewhere else.

One part can't be operationalized away: the **criterion**, meaning what the
outcome should track. That is a value choice, so this definition takes it as an
explicit input and makes everything else checkable around it.

## The diamond shield

The diamond shield is a remix of Iron Dome. Iron Dome doesn't try to stop
everything in the air. It tracks each incoming rocket, works out whether it
will land on something that matters, and intercepts only the ones that will.
Everything else is let through.

The diamond shield does the same job for decisions. Every decision, rule or
outcome that reaches it is screened against a stated criterion C using the five
tests below:

| Iron Dome | Diamond shield |
|-----------|----------------|
| Detect: radar picks up a launch | **Detect:** a decision, rule or outcome is recorded, with the parties it affects |
| Track: compute the trajectory | **Assess:** state C, then run the five tests and get a profile |
| Decide: will it hit a populated area? | **Decide:** does any test fail for anyone it affects? |
| Intercept, or let it fall in open ground | **Intercept** a failing decision before it lands: block it, send it back for correction, or trigger a remedy. **Pass** everything that clears all five. |

Two things carry over from the original. The shield stays out of the way of
decisions that pass, so it doesn't second-guess just outcomes. And every
intercept comes with the profile that triggered it, so anyone can see which
test failed and for whom. The rest of this document defines those tests.

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

## Recording the inputs in the merit ledger

The shield can only screen what has been written down. ADAM's merit ledger
already keeps two append-only, hash-chained files: `ledger.jsonl` for changes to
standing and to the rules, and `audit_log.jsonl` for every grading decision.
Each line names its decider and is signed. This section says what those files
would need to hold so that every input the five tests use is on record before
anyone runs them.

This is a proposal. The ledger isn't in this repository yet, so the field names
below are suggestions to settle when it lands.

### Principles

- **C is a rule, so it goes where rules go.** The criterion for a task is
  published as a rule change in `ledger.jsonl`, with its measure and scale. Like
  any rule, it binds nobody until its fingerprint has been delivered to everyone
  it affects. That gives "C must be stated before any test is run" a timestamp
  and a hash instead of a promise.
- **C can't be changed after the fact.** Changing it is a new rule line that
  applies from then on. A decision is always judged under the criterion that was
  in force when it was made, which it cites by fingerprint.
- **Inputs are recorded with the decision, not reconstructed later.** The
  party's measure on C goes into the decision line at grading time, by the same
  decider and under the same signature.
- **A check is itself a record.** Running the five tests produces a profile, and
  the profile is appended to the audit log as a decision by a formula, so it can
  be appealed like any other.
- **The shield never moves standing.** An intercept doesn't take standing from
  one person and give it to another, because the ledger has no transfers. It
  sends the decision back for a new, appealable grading, or triggers a remedy
  paid in civcoin.

### What each record holds

**1. Criterion rule** (`ledger.jsonl`, kind `rule`). Declares C for a task.

```json
{"kind": "rule", "task": "flood-aid-2026", "criterion": "need",
 "measure": {"what": "shortfall below shelter threshold", "unit": "score", "scale": [1, 3]},
 "direction": null,
 "thresholds": {"acceptance_gap": 0.20, "remedy_tolerance": 0.10, "measurement_error": 0},
 "decider": "trenton", "fingerprint": "sha256:..."}
```

`direction` is only used when C is harm: `"caused"` for a penalty, `"suffered"`
for compensation. For equality, `measure` is `null`, since there is nothing to
measure. If a task needs two criteria, it publishes two rule lines and every
decision under it records both measures.

**2. Grading decision** (`audit_log.jsonl`, kind `decision`). The line the
ledger already writes, with four additions.

```json
{"kind": "decision", "task": "flood-aid-2026", "subject": "household-B",
 "rule": "sha256:...", "measures": {"need": 3},
 "outcome": 100,
 "attributes": {"district": "south"},
 "procedure": {"notice": "sha256:...", "hearing": "sub-0042", "reasons": "...",
               "impartial_decider": true, "appeal": "open"},
 "decider": "committee", "reasoning": "...", "signature": "..."}
```

- `rule` cites the criterion rule by fingerprint.
- `measures` holds the subject's value on each C in force, in the rule's unit.
- `outcome` is the size of what the decision gave or took, in a stated unit, so
  test 2 can compare it with C.
- `attributes` holds the things that should *not* matter (district, group,
  status, wealth). Test 1 needs them to show which irrelevant difference
  changed an outcome. They are personal data, so see the open questions below.

**3. Acceptance survey** (`audit_log.jsonl`, kind `survey`). Input for test 4.
It records who was asked, the rule they were shown (stated without naming who
benefits), and counts per position, not individual answers.

```json
{"kind": "survey", "rule": "sha256:...",
 "positions": {"north": {"asked": 50, "accepted": 39}, "south": {"asked": 48, "accepted": 34}},
 "decider": "examiner", "signature": "..."}
```

**4. Wrong and remedy** (`audit_log.jsonl`, kind `wrong`). Input for test 5. A
wrong is a decision like any other, so it is graded, signed and appealable. Its
remedy is paid through civcoin's `remedy` command, and the wrong line cites the
civcoin entry.

```json
{"kind": "wrong", "harmed": "farm-3", "harm": 40000, "unit": "money",
 "remedy": {"civcoin_entry": 118, "restored": 20000},
 "decider": "panel", "signature": "..."}
```

**5. Justice check** (`audit_log.jsonl`, kind `check`). The shield's output:
one profile per criterion, the decisions it covers, the code version that
produced it, and what the shield did.

```json
{"kind": "check", "criterion": "need", "rule": "sha256:...",
 "covers": [101, 102, 103, 104], "code": "justice.py@812152e",
 "profile": {"consistency": "fail", "proportionality": "fail", "procedure": "4/5",
             "position_neutrality": "pass", "remedy": "n/a"},
 "verdict": "unjust", "action": "intercept: returned for regrading",
 "decider": "formula", "signature": "..."}
```

### Where each test gets its evidence

| Test | Read from | Comes free from the ledger? |
|------|-----------|------------------------------|
| 1 Consistency | `measures`, `outcome` and `attributes` on decisions under the same rule | No. Needs `measures` and `attributes` recorded at grading time. |
| 2 Proportionality | `measures` and `outcome` across those decisions | No. Needs `outcome` in a stated unit. |
| 3 Procedure | (a) notice: the rule's fingerprint was delivered; (b) hearing: a submission is on record; (c) reasons: the decision's `reasoning`; (d) impartial decider: the decider isn't the subject and has no stake; (e) appeal: the appeal route is open and the appeal grader differs from the original decider | Mostly yes. The ledger already enforces delivered fingerprints, written reasoning and appeals graded by someone else. |
| 4 Position-neutrality | `survey` lines for the rule | No. Surveys have to be run and recorded. |
| 5 Remedy | `wrong` lines and the civcoin remedy they cite | Partly. civcoin already flags remedies more than 10% from the harm. |

Procedure is the test the ledger answers almost by construction, which fits:
the ledger was designed around notice, reasons and appeal. Tests 1 and 2 are
where it needs the most new data, because the ledger records what each person
got but not yet their measure on C.

### Open questions

- **Privacy of attributes.** Test 1 needs irrelevant attributes to detect
  disparity, but writing someone's wealth or group into a permanent, readable
  log is its own harm. One option is to store a salted hash or a coarse code in
  the ledger and keep the raw value off-chain with the subject's consent.
- **Who sets the measure's scale.** The scale for C has to be fixed before
  outcomes are seen, or it can be tuned to fit them. Publishing it in the rule
  line handles timing, but not whether the scale itself is fair. That question
  is a candidate for the veil test.
- **When checks run.** A check could run on every decision, on a schedule, or
  only when someone appeals. Tests 1 and 2 need several decisions under the same
  rule before they mean anything.
- **Truncation.** Like civcoin, the ledger can't detect lines cut from its
  end using the file alone. A check that covers decisions 101 to 104 should
  also publish the head hash it saw.

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
