import unittest
from common.models import *


class TestEquality(unittest.TestCase):
    def test_same_model_id_equality(self):
        self.assertEqual(Subject(id=99), Subject(id=99))
        self.assertTrue(Subject(id=99) == Subject(id=99))
        self.assertTrue({Subject(id=99)} == {Subject(id=99)})
        self.assertTrue(Subject(id=99).__eq__(Subject(id=99)))
        self.assertNotEqual(Subject(id=19), Subject(id=99))

    def test_different_model_id_equality(self):
        self.assertNotEqual(Term(id=99), Subject(id=99))
        self.assertFalse(Term(id=99) == Subject(id=99))
        self.assertFalse({Term(id=99)} == {Subject(id=99)})
        self.assertFalse(Term(id=99).__eq__(Subject(id=99)))
        self.assertNotEqual(Term(id=19), Subject(id=99))

    def test_same_model_fields_equality(self):
        self.assertEqual(
            Group(subject=Subject(id=99), participants={Person(id=88)}),
            Group(subject=Subject(id=99), participants={Person(id=88)})
        )
        self.assertTrue(
            Group(subject=Subject(id=99), participants={Person(id=88)}) ==
            Group(subject=Subject(id=99), participants={Person(id=88)})
        )
        self.assertTrue(
            {Group(subject=Subject(id=99), participants={Person(id=88)})} ==
            {Group(subject=Subject(id=99), participants={Person(id=88)})}
        )
        self.assertTrue(
            Group(subject=Subject(id=99), participants={Person(id=88)}).__eq__(
                Group(subject=Subject(id=99), participants={Person(id=88)})
            )
        )
        self.assertNotEqual(
            Group(subject=Subject(id=99), participants={Person(id=88)}),
            Group(subject=Subject(id=9), participants={Person(id=88)})
        )
        self.assertNotEqual(
            Group(subject=Subject(id=99), participants={Person(id=88)}),
            Group(subject=Subject(id=99), participants={Person(id=88), Person(id=17)})
        )


if __name__ == '__main__':
    unittest.main()
