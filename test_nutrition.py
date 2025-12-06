import unittest

from nutrition import FoodInfo, lookup_food, summarize


class NutritionTests(unittest.TestCase):
    def test_lookup_known_food(self):
        info, suggestions = lookup_food("닭가슴살")
        self.assertIsInstance(info, FoodInfo)
        self.assertEqual(info.calories, 165)
        self.assertEqual(suggestions, [])

    def test_lookup_unknown_food(self):
        info, suggestions = lookup_food("미지의음식")
        self.assertIsNone(info)
        self.assertTrue(isinstance(suggestions, list))

    def test_summarize_accumulates_totals(self):
        rows, total = summarize(["닭가슴살", "고구마"])
        self.assertEqual(len(rows), 2)
        self.assertEqual(total.calories, 165 + 86)
        self.assertAlmostEqual(total.protein, 31.0 + 1.6)


if __name__ == "__main__":
    unittest.main()
