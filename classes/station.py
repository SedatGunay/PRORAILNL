class Station:
    def __init__(self, name, x=None, y=None):
        self.name = name
        self.x = x
        self.y = y
        self.connections = []

    def add_connection(self, connection):
        self.connections.append(connection)
