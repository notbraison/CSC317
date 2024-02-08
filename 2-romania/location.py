import uuid


class Location():
    def __init__(self, name: str):
        self.id = uuid.uuid4()
        self.name: str = name
        self.visited: bool = False

    def __str__(self):
        return f"location --name {self.name} --visited {self.visited}"

    def __eq__(self, other):
        if isinstance(other, Location):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)
