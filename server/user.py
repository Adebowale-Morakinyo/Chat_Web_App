class User:
    """Represents a user-client, holds name, sock object as client, and addr."""
    def __init__(self, addr, client):
        self.addr = addr
        self.client = client
        self.name = None

    def set_name(self, name):
        self.name = name

    def __repr__(self):
        return f"User({self.addr}, {self.name})"
