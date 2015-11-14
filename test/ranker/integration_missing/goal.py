import unittest
from parsing.parser import parse
from ranker.goal import evaluate_goal


class TestGoalEvaluation(unittest.TestCase):
    def test_evaluation(self):
        configuration, assignments = parse()
        value, completness = evaluate_goal(configuration, assignments)
        self.assertAlmostEquals(value, .5, delta=0.1)
        self.assertAlmostEquals(completness, 99.65, delta=0.01)

    if __name__ == '__main__':
        unittest.main()
