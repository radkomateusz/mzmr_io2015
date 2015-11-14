from common.models import Subject, Term
from parsing.terms import parse_subjects_and_terms
import unittest


class TestSubjectsAndTermsParsing(unittest.TestCase):
    def test_parsing(self):
        subjects, terms = parse_subjects_and_terms('''
[645274]
1
645350:11:0:0:70:88:0:1
645354:12:0:1:51:69:0:1
[645275]
1
645362:10:0:0:31:49:1:1
[kolizje]
645274,645350;645274,645354
645274,645354;645274,645350
645274,645354;645275,645362
''')
        self.assertEquals(subjects, frozenset([Subject(id=645274), Subject(id=645275)]))
        self.assertEquals(terms, frozenset([Term(id=645350), Term(id=645354), Term(id=645362)]))

        capacities = {term.id: term.capacity for term in terms}
        subjects = {term.id: term.subject for term in terms}
        collisions = {term.id: term.collisions for term in terms}

        self.assertEquals(capacities, {
            645350: 11,
            645354: 12,
            645362: 10
        })
        self.assertEquals(subjects, {
            645350: Subject(id=645274),
            645354: Subject(id=645274),
            645362: Subject(id=645275)
        })
        self.assertEquals(collisions, {
            645350: frozenset({Term(id=645354)}),
            645354: frozenset({Term(id=645362), Term(id=645350)}),
            645362: frozenset()
        })

    if __name__ == '__main__':
        unittest.main()
