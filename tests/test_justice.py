import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import justice
from justice import Case, Criterion, Party, Remedy, Status, Verdict, judge, judge_each

FULL_PROCEDURE = dict.fromkeys(justice.PROCEDURE_ITEMS, True)
EXAMPLE = Path(__file__).resolve().parent.parent / "examples" / "aid.json"


def party(name, outcome, group="x", **measures):
    return Party(name, outcome, measures, {"group": group})


def result_of(judgement, name):
    return next(t for t in judgement.tests if t.name == name)


class CriterionTest(unittest.TestCase):
    def test_criterion_is_required_and_validated(self):
        with self.assertRaises(ValueError):
            judge("luck", Case("x"))

    def test_accepts_string_or_enum(self):
        self.assertEqual(judge("need", Case("x")).criterion, Criterion.NEED)
        self.assertEqual(judge(Criterion.HARM, Case("x")).criterion, Criterion.HARM)


class ConsistencyTest(unittest.TestCase):
    def test_equal_measure_equal_outcome_passes(self):
        case = Case("x", (party("a", 5, "n", need=2), party("b", 5, "s", need=2)))
        self.assertEqual(result_of(judge("need", case), "consistency").status, Status.PASS)

    def test_equal_measure_different_outcome_fails_and_names_attribute(self):
        case = Case("x", (party("a", 5, "n", need=2), party("b", 3, "s", need=2)))
        result = result_of(judge("need", case), "consistency")
        self.assertEqual(result.status, Status.FAIL)
        self.assertEqual(result.score, 0.0)
        self.assertIn("group", result.reasons[0])

    def test_no_equal_pairs_is_not_assessed(self):
        case = Case("x", (party("a", 5, need=2), party("b", 3, need=1)))
        self.assertEqual(result_of(judge("need", case), "consistency").status, Status.NOT_ASSESSED)

    def test_equality_criterion_compares_everyone(self):
        case = Case("x", (party("a", 1), party("b", 1), party("c", 2)))
        result = result_of(judge("equality", case), "consistency")
        self.assertEqual(result.status, Status.FAIL)
        self.assertAlmostEqual(result.score, 1 / 3)

    def test_parties_without_the_measure_are_skipped(self):
        case = Case("x", (party("a", 5, need=2), party("b", 9, desert=2)))
        self.assertEqual(result_of(judge("need", case), "consistency").status, Status.NOT_ASSESSED)


class ProportionalityTest(unittest.TestCase):
    def test_outcomes_tracking_measure_pass(self):
        case = Case("x", (party("a", 1, harm=1), party("b", 2, harm=2), party("c", 3, harm=3)))
        result = result_of(judge("harm", case), "proportionality")
        self.assertEqual(result.status, Status.PASS)
        self.assertEqual(result.score, 1.0)

    def test_inversion_fails_with_count(self):
        case = Case("x", (party("a", 1, desert=1), party("b", 3, desert=2), party("c", 2, desert=3)))
        result = result_of(judge("desert", case), "proportionality")
        self.assertEqual(result.status, Status.FAIL)
        self.assertEqual(result.reasons[0], "1 inversion in 3 pairs")
        self.assertIn("c has more desert", result.reasons[1])

    def test_ties_in_outcome_are_not_inversions(self):
        case = Case("x", (party("a", 2, need=1), party("b", 2, need=2)))
        self.assertEqual(result_of(judge("need", case), "proportionality").status, Status.PASS)

    def test_single_level_is_not_assessed(self):
        case = Case("x", (party("a", 1, need=1), party("b", 2, need=1)))
        self.assertEqual(result_of(judge("need", case), "proportionality").status, Status.NOT_ASSESSED)


class ProcedureTest(unittest.TestCase):
    def test_all_five_pass(self):
        result = result_of(judge("need", Case("x", procedure=FULL_PROCEDURE)), "procedure")
        self.assertEqual((result.status, result.score), (Status.PASS, 1.0))

    def test_missing_appeal_is_partial_four_of_five(self):
        result = result_of(judge("need", Case("x", procedure={**FULL_PROCEDURE, "appeal": False})), "procedure")
        self.assertEqual(result.status, Status.PARTIAL)
        self.assertEqual(result.reasons, ("4/5", "no appeal"))

    def test_none_present_fails(self):
        result = result_of(judge("need", Case("x", procedure={})), "procedure")
        self.assertEqual((result.status, result.score), (Status.FAIL, 0.0))

    def test_missing_info_is_not_assessed(self):
        self.assertEqual(result_of(judge("need", Case("x")), "procedure").status, Status.NOT_ASSESSED)


class PositionNeutralityTest(unittest.TestCase):
    def test_close_rates_pass(self):
        case = Case("x", acceptance={"north": 0.78, "south": 0.71})
        self.assertEqual(result_of(judge("need", case), "position-neutrality").status, Status.PASS)

    def test_lagging_position_fails(self):
        case = Case("x", acceptance={"owners": 0.9, "tenants": 0.4, "others": 0.85})
        result = result_of(judge("need", case), "position-neutrality")
        self.assertEqual(result.status, Status.FAIL)
        self.assertEqual(len(result.reasons), 1)
        self.assertIn("tenants", result.reasons[0])

    def test_single_position_is_not_assessed(self):
        case = Case("x", acceptance={"only": 0.5})
        self.assertEqual(result_of(judge("need", case), "position-neutrality").status, Status.NOT_ASSESSED)


class RemedyTest(unittest.TestCase):
    def check(self, harm, restored):
        return result_of(judge("harm", Case("x", remedy=Remedy(harm, restored))), "remedy").status

    def test_full_restoration_passes(self):
        self.assertEqual(self.check(100, 100), Status.PASS)
        self.assertEqual(self.check(100, 95), Status.PASS)

    def test_partial_restoration_is_partial(self):
        self.assertEqual(self.check(100, 50), Status.PARTIAL)

    def test_nothing_restored_fails(self):
        self.assertEqual(self.check(100, 0), Status.FAIL)

    def test_excessive_remedy_fails(self):
        self.assertEqual(self.check(100, 300), Status.FAIL)

    def test_no_wrong_is_not_assessed(self):
        self.assertEqual(self.check(0, 0), Status.NOT_ASSESSED)
        self.assertEqual(result_of(judge("harm", Case("x")), "remedy").status, Status.NOT_ASSESSED)


class VerdictTest(unittest.TestCase):
    def test_all_pass_is_just(self):
        case = Case("x", (party("a", 1, need=1), party("b", 2, need=2)), procedure=FULL_PROCEDURE)
        self.assertEqual(judge("need", case).verdict, Verdict.JUST)

    def test_partial_without_fail_is_partly_just(self):
        case = Case("x", procedure={**FULL_PROCEDURE, "hearing": False})
        self.assertEqual(judge("need", case).verdict, Verdict.PARTLY_JUST)

    def test_any_fail_is_unjust(self):
        case = Case("x", (party("a", 1, need=1), party("b", 2, need=1)), procedure=FULL_PROCEDURE)
        self.assertEqual(judge("need", case).verdict, Verdict.UNJUST)

    def test_nothing_assessable_is_inconclusive(self):
        judgement = judge("need", Case("x"))
        self.assertEqual(judgement.verdict, Verdict.INCONCLUSIVE)
        self.assertEqual(len(judgement.tests), 5)

    def test_reasons_are_prefixed_by_test(self):
        reasons = judge("need", Case("x")).reasons
        self.assertEqual(len(reasons), 5)
        self.assertTrue(reasons[0].startswith("consistency: "))


class MultipleCriteriaTest(unittest.TestCase):
    def test_same_case_can_be_just_under_one_criterion_and_not_another(self):
        case = Case("x", (party("a", 1, need=1, desert=2), party("b", 2, need=2, desert=1)))
        by_need, by_desert = judge_each(["need", "desert"], case)
        self.assertEqual(by_need.verdict, Verdict.JUST)
        self.assertEqual(by_desert.verdict, Verdict.UNJUST)


class InputOutputTest(unittest.TestCase):
    def test_judge_accepts_a_dict(self):
        data = json.loads(EXAMPLE.read_text())
        judgement = judge("need", data)
        self.assertEqual(judgement.description, data["description"])
        self.assertEqual(judgement.verdict, Verdict.UNJUST)
        self.assertEqual(result_of(judgement, "procedure").status, Status.PARTIAL)

    def test_from_dict_reads_remedy(self):
        case = Case.from_dict({"description": "x", "remedy": {"harm": 10, "restored": 10}})
        self.assertEqual(case.remedy, Remedy(10.0, 10.0))

    def test_to_dict_is_json_serialisable(self):
        out = judge("need", Case("x", procedure=FULL_PROCEDURE)).to_dict()
        self.assertEqual(json.loads(json.dumps(out))["tests"][2]["status"], "pass")

    def test_profile_matches_doc_layout(self):
        text = justice.profile(judge("need", Case("x", procedure={**FULL_PROCEDURE, "appeal": False})))
        lines = text.splitlines()
        self.assertEqual(lines[0], "C: need")
        self.assertTrue(lines[3].startswith("3 Procedure"))
        self.assertIn("partial", lines[3])
        self.assertIn("n/a", lines[5])
        self.assertEqual(lines[-1], "Verdict: partly just")

    def test_cli_prints_one_profile_per_criterion(self):
        out = io.StringIO()
        with redirect_stdout(out):
            justice.main([str(EXAMPLE), "--criterion", "need", "--criterion", "contribution"])
        self.assertIn("C: need", out.getvalue())
        self.assertIn("C: contribution", out.getvalue())

    def test_cli_json(self):
        out = io.StringIO()
        with redirect_stdout(out):
            justice.main([str(EXAMPLE), "--criterion", "need", "--json"])
        self.assertEqual(json.loads(out.getvalue())[0]["criterion"], "need")


if __name__ == "__main__":
    unittest.main()
