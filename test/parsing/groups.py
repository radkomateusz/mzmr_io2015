import unittest
from common.models import *
from parsing.groups import parse_groups


class TestGroupsParsing(unittest.TestCase):
    def test_parsing(self):
        groups = parse_groups('645279:258557  ,258645\n  645279:258600,258567  \n645271 :258627  ,258694,249953')
        expected = frozenset([
            Group(subject=Subject(id=645279), participants=frozenset([Person(id=258557), Person(id=258645)])),
            Group(subject=Subject(id=645279), participants=frozenset([Person(id=258600), Person(id=258567)])),
            Group(subject=Subject(id=645271),
                  participants=frozenset([Person(id=258627), Person(id=258694), Person(id=249953)]))
        ])
        self.assertEquals(groups, expected)

        if __name__ == '__main__':
            unittest.main()
