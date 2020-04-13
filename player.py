
class Player:
    def __init__(self):
        self.bag = set()
        self.room = 0
        self.name = ""

    def move_to(self, to_room):
        self.room = to_room

    def set_name(self, name):
        self.name = name
