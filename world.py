import xml.etree.ElementTree as ET
import debug

from res.localized import DirShorts

# Class for rooms
class Room:
    """
    One room in th world
    """

    def __init__(self, room_id, description, whereto):
        self.id = room_id
        self.description = description
        self.possible_exits = []
        self.not_possible_text = []
        self.set_directions(whereto)

        if debug.DEBUG:
            print("-" * 40)
            print(room_id)
            print(self.not_possible_text)
            print(self.possible_exits)
            print("-"*40)

        self.bag = set()

    def set_directions(self, whereto):

        for dirlist in whereto:
            try:
                room = int(dirlist)
                self.possible_exits.append(room)
                self.not_possible_text.append("")
            except ValueError:
                self.possible_exits.append(0)
                self.not_possible_text.append(dirlist)

    def add_item(self, item):
        self.bag.add(item)

    def remove_item(self, item):
        self.bag.remove(item)


class World:
    """
    Map of the world with list of rooms
    """

    def __init__(self):
        self.rooms = []

    def add_room(self, rm: Room):

        self.rooms.append(rm)

    def create_room(self, id, text, dir):
        """:arg id is the unique identifier of the room
           :arg text the description of the room
           :arg dir is a list of the directions with the room numbers those directions lead to
        """
        rm = Room(id, text, dir)
        return (rm)

    def find_room_by_id(self, id) -> Room:
        """:arg id = finds room with the id"""
        for r in self.rooms:
            if r.id == id:
                return r
        return None

    def load_world(self, filename):
        """:arg filename
        Loads the file which contains all the rooms with description
        """
        with open(filename, 'r', encoding="utf-8") as mapfile:
            room_id = 0
            room_text = ""
            room_directions = []

            for line in mapfile:

                if line[0:3] == "ID=":
                    if room_id != 0:
                        self.add_room(self.create_Room(room_id, room_text, room_directions))
                    else:
                        room_id = 0
                        room_text = ""
                        room_directions = []

                        room_id = int(line[3:])
                elif line[0:5] == "Text=":
                    room_text = line[5:]
                elif line[0:4] == "Dir=":
                    room_directions = line[4:].split(",")
                elif line[0] == "#":
                    pass
                elif room_id != 0:
                    room_text += line

                if (room_id != 0) and (room_text != "") and (len(room_directions) != 0):
                    if debug.DEBUG:
                        print(room_id)
                        print(room_text)
                        print(room_directions)

                    self.add_room(self.create_room(room_id, room_text, room_directions))
                    room_id = 0
                    room_text = ""
                    room_directions = []

        mapfile.close()

    def load_world_xml(self, filename):
        """:arg filename
        Loads the file which contains all the rooms with description
        """
        dirs = DirShorts()

        tree = ET.parse(filename)
        root = tree.getroot()

        for child in root.iter("room"):
            room_id = int(child.find("id").text)
            room_text = ""
            room_directions = [0,0,0,0,0,0,0,0,0,0]
            # TODO not completely correct fix.
            try:
                room_text = child.find("description").text
            except AttributeError:
                room_text = "The developer forgot the room description."

            for exits in child.iter('exit'):
               # print(exits.attrib)
                try:
                    room_directions[dirs.directionDict[exits.attrib["name"]]] = int(exits.attrib["room"])
                except ValueError:
                    room_directions[dirs.directionDict[exits.attrib["name"]]] = exits.attrib["room"]


            self.add_room(self.create_room(room_id, room_text, room_directions))
