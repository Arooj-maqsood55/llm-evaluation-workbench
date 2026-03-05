import unittest

from src.scoring import compare_pair, score_answer


class ScoringTests(unittest.TestCase):
    def test_score_answer_prefers_keyword_coverage(self):
        criteria = [{"id": "reliability", "weight": 1.0, "keywords": ["validate", "schema"]}]
        strong = score_answer("Validate schema before import", criteria)
        weak = score_answer("Skip checks", criteria)
        self.assertGreater(strong["total"], weak["total"])

    def test_compare_pair_selects_preferred(self):
        pair = {
            "id": "p1",
            "answer_a": "Validate required fields and remove duplicates",
            "answer_b": "Ignore quality",
        }
        rubric = {
            "version": "1.0",
            "criteria": [
                {"id": "completeness", "weight": 1.0, "keywords": ["validate", "required", "duplicates"]}
            ],
        }
        result = compare_pair(pair, rubric)
        self.assertEqual(result["preferred"], "A")


if __name__ == "__main__":
    unittest.main()
