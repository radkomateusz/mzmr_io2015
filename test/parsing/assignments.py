import unittest
from common.models import *
from parsing.assignments import parse_assignments


class TestPeopleAndPreferencesParsing(unittest.TestCase):
    def test_parsing(self):
        assignments = parse_assignments('''
[258597]
645273:645342
645275:645366
[258590]
645274:645355
645275:645368''')
        self.assertEquals(assignments, frozenset([
            Assignment(person=Person(id=258597)),
            Assignment(person=Person(id=258590))
        ]))

        mapping = {assignment.person.id: assignment.subject_ids_to_term_ids for assignment in assignments}
        self.assertEquals(mapping, {
            258590: {645274: 645355, 645275: 645368},
            258597: {645273: 645342, 645275: 645366}
        })

    if __name__ == '__main__':
        unittest.main()
