"""Operational definition of justice, as code.

A decision, rule, or outcome is *just* to the degree that, given a stated
criterion C, it passes five tests for everyone it affects:

1. Consistency (swap test): parties equal on C get equal outcomes, whatever
   their other attributes.
2. Proportionality: outcomes rise and fall with C (no inversions).
3. Procedure: notice, a hearing, stated reasons, an impartial decider and an
   appeal route were all present.
4. Position-neutrality (veil test): no affected position accepts the rule at a
   rate far below the others.
5. Remedy: a demonstrated wrong is answered by restoration proportionate to
   the harm.

The criterion is always an explicit input with no default: choosing it is the
value judgement the definition leaves to you. A case that seems to need two
criteria is judged once per criterion (see `judge_each`). The result is a
profile, one result per test, plus a verdict derived from it, so it stays
visible which kind of injustice occurred. See docs/justice.md.

Usage:
    python justice.py case.json --criterion need [--criterion desert] [--json]
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum
from itertools import combinations
from typing import Any

# Two numbers closer than this are treated as equal.
TOLERANCE = 1e-9
# Test 4 fails when a position's acceptance rate is more than this far below
# the highest position's rate.
ACCEPTANCE_GAP = 0.2
# Test 5 counts a remedy as proportionate when it is within this fraction of
# the harm.
REMEDY_TOLERANCE = 0.1


class Criterion(str, Enum):
    DESERT = "desert"
    NEED = "need"
    CONTRIBUTION = "contribution"
    EQUALITY = "equality"
    HARM = "harm"


class Status(str, Enum):
    PASS = "pass"
    PARTIAL = "partial"
    FAIL = "fail"
    NOT_ASSESSED = "not assessed"


class Verdict(str, Enum):
    JUST = "just"
    PARTLY_JUST = "partly just"
    UNJUST = "unjust"
    INCONCLUSIVE = "inconclusive"


PROCEDURE_ITEMS = ("notice", "hearing", "reasons", "impartial_decider", "appeal")


@dataclass(frozen=True)
class Party:
    """Someone the decision affects.

    `measures` holds the party's value on each criterion that applies (for
    example {"need": 3}). `attributes` holds everything that should *not*
    matter, such as group or status; it is only used to explain failures.
    """

    name: str
    outcome: float
    measures: Mapping[str, float] = field(default_factory=dict)
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def measure(self, criterion: Criterion) -> float | None:
        if criterion is Criterion.EQUALITY:
            return 1.0
        value = self.measures.get(criterion.value)
        return None if value is None else float(value)


@dataclass(frozen=True)
class Remedy:
    harm: float
    restored: float


@dataclass(frozen=True)
class Case:
    description: str
    parties: tuple[Party, ...] = ()
    procedure: Mapping[str, bool] | None = None
    acceptance: Mapping[str, float] | None = None
    remedy: Remedy | None = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Case:
        remedy = data.get("remedy")
        return cls(
            description=data.get("description", ""),
            parties=tuple(
                Party(
                    name=p["name"],
                    outcome=float(p["outcome"]),
                    measures=p.get("measures", {}),
                    attributes=p.get("attributes", {}),
                )
                for p in data.get("parties", [])
            ),
            procedure=data.get("procedure"),
            acceptance=data.get("acceptance"),
            remedy=Remedy(float(remedy["harm"]), float(remedy["restored"])) if remedy else None,
        )


@dataclass(frozen=True)
class TestResult:
    name: str
    status: Status
    score: float | None
    reasons: tuple[str, ...]

    __test__ = False  # not a test case, despite the name


@dataclass(frozen=True)
class Judgement:
    criterion: Criterion
    description: str
    verdict: Verdict
    tests: tuple[TestResult, ...]

    @property
    def reasons(self) -> list[str]:
        return [f"{t.name}: {r}" for t in self.tests for r in t.reasons]

    def to_dict(self) -> dict[str, Any]:
        return {
            "criterion": self.criterion.value,
            "description": self.description,
            "verdict": self.verdict.value,
            "tests": [
                {"name": t.name, "status": t.status.value, "score": t.score, "reasons": list(t.reasons)}
                for t in self.tests
            ],
        }


def _close(a: float, b: float) -> bool:
    return abs(a - b) <= TOLERANCE


def _measured(criterion: Criterion, parties: tuple[Party, ...]) -> list[tuple[Party, float]]:
    return [(p, m) for p in parties if (m := p.measure(criterion)) is not None]


def check_consistency(criterion: Criterion, case: Case) -> TestResult:
    name = "consistency"
    pairs = [
        (a, b)
        for (a, ma), (b, mb) in combinations(_measured(criterion, case.parties), 2)
        if _close(ma, mb)
    ]
    if not pairs:
        return TestResult(name, Status.NOT_ASSESSED, None, (f"no two parties are equal on {criterion.value}",))
    failures = []
    for a, b in pairs:
        if not _close(a.outcome, b.outcome):
            differing = sorted(
                k for k in set(a.attributes) | set(b.attributes) if a.attributes.get(k) != b.attributes.get(k)
            )
            why = f"; they differ in {', '.join(differing)}" if differing else ""
            failures.append(
                f"{a.name} and {b.name} are equal on {criterion.value} "
                f"but got {a.outcome:g} and {b.outcome:g}{why}"
            )
    score = 1 - len(failures) / len(pairs)
    if failures:
        return TestResult(name, Status.FAIL, score, tuple(failures))
    return TestResult(name, Status.PASS, score, (f"all {len(pairs)} pairs equal on {criterion.value} got equal outcomes",))


def check_proportionality(criterion: Criterion, case: Case) -> TestResult:
    name = "proportionality"
    pairs = [
        ((a, ma), (b, mb))
        for (a, ma), (b, mb) in combinations(_measured(criterion, case.parties), 2)
        if not _close(ma, mb)
    ]
    if not pairs:
        return TestResult(name, Status.NOT_ASSESSED, None, (f"fewer than two distinct levels of {criterion.value}",))
    inversions = []
    for (a, ma), (b, mb) in pairs:
        (hi, mhi), (lo, mlo) = ((a, ma), (b, mb)) if ma > mb else ((b, mb), (a, ma))
        if hi.outcome < lo.outcome and not _close(hi.outcome, lo.outcome):
            inversions.append(
                f"{hi.name} has more {criterion.value} ({mhi:g} vs {mlo:g}) "
                f"but got less than {lo.name} ({hi.outcome:g} vs {lo.outcome:g})"
            )
    score = 1 - len(inversions) / len(pairs)
    if inversions:
        n = len(inversions)
        summary = f"{n} inversion{'' if n == 1 else 's'} in {len(pairs)} pairs"
        return TestResult(name, Status.FAIL, score, (summary, *inversions))
    return TestResult(name, Status.PASS, score, (f"outcomes follow {criterion.value} across all {len(pairs)} pairs",))


def check_procedure(case: Case) -> TestResult:
    name = "procedure"
    if case.procedure is None:
        return TestResult(name, Status.NOT_ASSESSED, None, ("no procedure information given",))
    missing = [item for item in PROCEDURE_ITEMS if not case.procedure.get(item, False)]
    score = (len(PROCEDURE_ITEMS) - len(missing)) / len(PROCEDURE_ITEMS)
    if missing:
        status = Status.FAIL if len(missing) == len(PROCEDURE_ITEMS) else Status.PARTIAL
        reasons = (f"{len(PROCEDURE_ITEMS) - len(missing)}/{len(PROCEDURE_ITEMS)}",)
        reasons += tuple(f"no {item.replace('_', ' ')}" for item in missing)
        return TestResult(name, status, score, reasons)
    return TestResult(name, Status.PASS, score, ("notice, hearing, reasons, impartial decider and appeal all present",))


def check_position_neutrality(case: Case) -> TestResult:
    name = "position-neutrality"
    if not case.acceptance or len(case.acceptance) < 2:
        return TestResult(name, Status.NOT_ASSESSED, None, ("acceptance rates for at least two positions are needed",))
    best_position, best = max(case.acceptance.items(), key=lambda kv: kv[1])
    lagging = [
        f"{position} accepts at {rate:.0%}, versus {best:.0%} for {best_position}"
        for position, rate in case.acceptance.items()
        if best - rate > ACCEPTANCE_GAP + TOLERANCE
    ]
    score = min(case.acceptance.values()) / best if best > 0 else 0.0
    if lagging:
        return TestResult(name, Status.FAIL, score, tuple(lagging))
    return TestResult(name, Status.PASS, score, (f"every position accepts within {ACCEPTANCE_GAP:.0%} of the others",))


def check_remedy(case: Case) -> TestResult:
    name = "remedy"
    if case.remedy is None or case.remedy.harm <= 0:
        return TestResult(name, Status.NOT_ASSESSED, None, ("no demonstrated wrong to remedy",))
    harm, restored = case.remedy.harm, case.remedy.restored
    gap = restored - harm
    score = max(0.0, 1 - abs(gap) / harm)
    if abs(gap) <= REMEDY_TOLERANCE * harm:
        return TestResult(name, Status.PASS, score, (f"restored {restored:g} of {harm:g} harm",))
    if restored <= 0:
        return TestResult(name, Status.FAIL, score, (f"nothing restored for {harm:g} harm",))
    if gap > 0:
        return TestResult(name, Status.FAIL, score, (f"remedy of {restored:g} exceeds the {harm:g} harm",))
    return TestResult(name, Status.PARTIAL, score, (f"only {restored:g} of {harm:g} harm restored",))


def verdict_for(tests: tuple[TestResult, ...]) -> Verdict:
    statuses = {t.status for t in tests}
    if Status.FAIL in statuses:
        return Verdict.UNJUST
    if Status.PARTIAL in statuses:
        return Verdict.PARTLY_JUST
    if Status.PASS in statuses:
        return Verdict.JUST
    return Verdict.INCONCLUSIVE


def judge(criterion: Criterion | str, case: Case | Mapping[str, Any]) -> Judgement:
    """Apply the five tests to `case` under `criterion` and return a judgement."""
    criterion = Criterion(criterion)
    if not isinstance(case, Case):
        case = Case.from_dict(case)
    tests = (
        check_consistency(criterion, case),
        check_proportionality(criterion, case),
        check_procedure(case),
        check_position_neutrality(case),
        check_remedy(case),
    )
    return Judgement(criterion, case.description, verdict_for(tests), tests)


def judge_each(criteria: list[Criterion | str], case: Case | Mapping[str, Any]) -> list[Judgement]:
    """Judge `case` once per criterion; conflicts between the profiles are part of the answer."""
    return [judge(c, case) for c in criteria]


def profile(judgement: Judgement) -> str:
    """Render a judgement as the plain-text profile shown in docs/justice.md."""
    lines = [f"C: {judgement.criterion.value}"]
    for i, t in enumerate(judgement.tests, 1):
        status = "n/a" if t.status is Status.NOT_ASSESSED else t.status.value
        lines.append(f"{i} {t.name.capitalize():<19} {status:<7} ({'; '.join(t.reasons)})")
    lines.append(f"Verdict: {judgement.verdict.value}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Judge a case under a chosen criterion of justice.")
    parser.add_argument("case", help="path to a case JSON file, or - for stdin")
    parser.add_argument(
        "--criterion",
        required=True,
        action="append",
        choices=[c.value for c in Criterion],
        help="the criterion C; repeat to judge the case once per criterion",
    )
    parser.add_argument("--json", action="store_true", help="print JSON instead of text profiles")
    args = parser.parse_args(argv)
    if args.case == "-":
        data = json.load(sys.stdin)
    else:
        with open(args.case, encoding="utf-8") as f:
            data = json.load(f)
    judgements = judge_each(args.criterion, data)
    if args.json:
        json.dump([j.to_dict() for j in judgements], sys.stdout, indent=2)
        print()
    else:
        print("\n\n".join(profile(j) for j in judgements))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
