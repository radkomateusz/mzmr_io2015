class ModelToStringMixin(object):
    def __str__(self):
        return str(self.__class__.__name__) + str(self.__dict__)


class IdEqualityMixin(object):
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.id


class FieldsEqualityMixin(object):
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(frozenset(self.__dict__.items()))


class Group(FieldsEqualityMixin, ModelToStringMixin):
    def __init__(self, subject=None, participants=frozenset()):
        self.subject = subject
        self.participants = frozenset(participants)


class Person(IdEqualityMixin, ModelToStringMixin):
    def __init__(self, id=None):
        self.id = id


class Assignment(FieldsEqualityMixin, ModelToStringMixin):
    def __init__(self, person=None, subject_ids_to_term_ids=dict()):
        self.subject_ids_to_term_ids = subject_ids_to_term_ids
        self.person = person

    def get_term(self, subject_id):
        return self.subject_ids_to_term_ids[subject_id]

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.person == other.person

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.person)


class Preference(IdEqualityMixin, ModelToStringMixin):
    def __init__(self, person=None, term_ids_to_points=dict()):
        self.term_ids_to_points = term_ids_to_points
        self.person = person

    def get_points(self, term_id):
        return self.term_ids_to_points.get(term_id)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.person == other.person

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.person)


class Subject(IdEqualityMixin, ModelToStringMixin):
    def __init__(self, id=None):
        self.id = id


class Term(IdEqualityMixin, ModelToStringMixin):
    def __init__(self, id=None, subject=None, capacity=0, collisions=frozenset()):
        self.collisions = frozenset(collisions)
        self.capacity = capacity
        self.subject = subject
        self.id = id

    def add_collision(self, term):
        mutable = {self.collisions}
        self.collisions = frozenset(mutable.add(term))
