import unittest
from parsing.parser import parse
from ranker.goal import evaluate_goal


class TestGoalEvaluation(unittest.TestCase):
    def test_evaluation(self):
        configuration, assignments = parse()
        value, completness = evaluate_goal(configuration, assignments)
        self.assertAlmostEquals(value, .7719, delta=0.0001)
        self.assertAlmostEquals(completness, 100)

    if __name__ == '__main__':
        unittest.main()
