import uuid
from location import Location


class Distance():
    def __init__(self, distance: float, location: Location):
        self.id = uuid.uuid4()
        self.distance: float = distance
        self.destination: Location = location

    def __str__(self):
        return f"distance\n\t--distance {self.distance}\n\t--destination {self.destination}"

    def __eq__(self, other):
        if isinstance(other, Distance):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)


# l1 = Location("l1")
# l2 = Location("l2")
#
# d1 = Distance(1, l2)
#
# print(d1)
