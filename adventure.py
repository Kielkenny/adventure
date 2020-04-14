import xml.etree.ElementTree as ET
import world
from player import Player
from advparser import Adv_Parser, Word, Understood
from inventory import Item
from res.localized import Responses, DirText
import debug


class Actions:
    """
    Possible actions with a number, make sure those align with the words.csv list
    """
    LOOK = 11
    TAKE = 12
    INV = 13
    DROP = 14
    DIG = 15
    READ = 16
    TOUCH = 17
    ENTER = 18
    FLEE = 19
    LEAVE = 20
    SWIM = 21
    DIVE = 22
    JUMP = 24
    MOVE = 25
    ROW = 26
    REST = 27
    SLEEP = 28
    RIDE = 29
    SIT = 30
    STAND = 31
    BUY = 32
    CHECK = 33
    OPEN = 34
    CLOSE = 35
    LOCK = 36
    COVER = 37
    DECODE = 38
    EMPTY = 39
    FILL = 40
    FIND = 41
    BIND = 42
    GIVE = 43
    PICKUP = 44
    BURN = 45
    PAY = 46
    STICK = 47
    CLEAN = 48
    SHAKE = 49
    WATER = 50
    PRESS = 51
    TEAR = 52
    SELL = 54
    SEND = 55
    DESTROY = 56
    KILL = 57
    STEAL = 58
    TASTE = 59
    TURN = 61
    USE = 63
    WINK = 64
    WEAR = 65
    ASK = 66
    BLOW = 67
    BRIBE = 68
    INFO = 69
    SHOUT = 70
    KISS = 71
    PLAY = 72
    SAY = 73
    THANK = 74
    BLOCK = 75
    WALE = 76
    DRINK = 78
    SMOKE = 78
    END = 98
    HELP = 99


class Game:
    def __init__(self):
        self.my_world = world.World()
        # self.my_world.load_world(r".\res\map.txt")
        self.my_world.load_world_xml(r".\res\adventure_data.xml")

        self.ego = Player()
        self.ego.move_to(1)

        self.pars = Adv_Parser()
        self.pars.load_words()

        self.help_text = []

        with open(r".\res\help.txt", "r", encoding="utf-8") as help_file:
            self.help_text = help_file.readlines()

        # Put items in room
        self.read_items()


    def read_items(self):
        tree = ET.parse(r".\res\adventure_data.xml")
        root = tree.getroot()

        # def __init__(self, id=0, desc="", take=True, name="", desc_room=""):

        for child in root.iter("item"):
            ch_id = int(child.find("id").text)
            ch_look = child.find("look_text").text
            ch_word = child.find("word").text
            ch_take = child.find("takeable").text
            ch_name = child.find("word_use").text
            ch_room = child.find("room_text").text
            ch_in_room = int(child.find("in_room").text)

            w = Word(ch_word, 3, int(ch_id))  # Add to Wordlist
            self.pars.wordlist.append(w)

            item_to_add = Item(ch_id, ch_look, ch_take == "True", ch_name, ch_room)
            if ch_in_room > 0:
                self.my_world.find_room_by_id(ch_in_room).add_item(item_to_add)
            else:
                self.my_world.find_room_by_id(world.SECRET_STORAGE).add_item(item_to_add)  #create items not in room yet

    def intro(self):
        """ prints the introduction text"""
        with open(r".\res\intro.txt", "r", encoding="utf-8") as intro:
            for line in intro:
                print(line, end="")

    def print_directions(self, room: world.Room):
        """ prints all possible directions"""
        all_possible = DirText()
        possible = []
        for x in range(len(all_possible.directionList)):
            if room.possible_exits[x] != 0:
                possible.append(all_possible.directionList[x])

        print(Responses.EXITS + str(possible) + "\n")

    def move(self, com: Understood):
        """
        Used the directions in understood and checks if from the player current room
        the desired direction is possible. the directions either contain 0 or a string if it
        is not possible. otherwise the room number.
        """

        try_move = self.where_am_i().possible_exits[com.dir_id - 1]  # There can be a number, a text or a zero

        try:
            direction = int(try_move)
        except ValueError:
            print(try_move)
            return

        if direction == 0:  # cannot move TODO add more default answers if a direction is not possible
            print(Responses.NOT_POSSIBLE_TO_GO)
        else:
            self.ego.move_to(direction)
            print(Responses.YOU_MOVED)

    def just_do_it(self, com: Understood):
        """:arg com what was understood
        does all the actions
        """

        if com.obj1_id == 0 and com.obj2_id != 0:
            com.obj1_id = com.obj2_id
            com.obj2_id = 0

        # Take action
        if com.verb_id == Actions.TAKE:
            # look for first object
            if com.obj1_id != 0:
                # check if object is in room
                for it in self.where_am_i().bag:
                    if it.id == com.obj1_id:
                        if it.takeable:
                            print(Responses.TAKE_IT.format(it.name))
                            self.ego.bag.add(it)
                            self.where_am_i().bag.remove(it)
                            return
                        else:
                            print(Responses.NO_TO_TAKE.format(it.name))
                            return

                # check if I have the object already
                for it in self.ego.bag:
                    if it.id == com.obj1_id:
                        print(Responses.ALREADY_HAVE.format(it.name))
                        return

                print(Responses.IS_NOT_HERE)

        # Print inventory
        if com.verb_id == Actions.INV:
            self.print_inventory()

        # exit the game
        if com.verb_id == Actions.END:
            quit()

        # print help
        if com.verb_id == Actions.HELP:
            if com.obj1_id == 0:
                self.print_help()

        # drop action
        if com.verb_id == Actions.DROP:
            for obj_no in [com.obj1_id, com.obj2_id]:
                if obj_no != 0:
                    for inv in self.ego.bag:
                        found = False
                        if obj_no == inv.id: # I have the object
                            self.where_am_i().bag.add(inv)  # add to room
                            self.ego.bag.remove(inv) # remove from inventory
                            print(Responses.YOU_DROP.format(inv.name))
                            found = True
                            break
                        if not found:
                            print(Responses.NO_HAVE.format(inv.name))

            if com.obj1_id + com.obj2_id == 0:
                print(Responses.WHAT_TO_DROP)




    def print_inventory(self):
        """
        Prints inventory content
        """
        if len(self.ego.bag) == 0:
            print(Responses.CARRY_NOTHING)

        print(Responses.YOU_CARRY)
        for piece in self.ego.bag:
            print(piece.name)

    def print_help(self):
        print("-" * 60)
        for line in self.help_text:
            print(line, end='')
        print("-" * 60)

    def where_am_i(self) -> world.Room:
        """
        :return: Room object the player is in 
        """
        return self.my_world.find_room_by_id(self.ego.room)

    def loop(self):
        """
        This is the main game loop
        """
        last_room = -1
        while True:
            if last_room != self.ego.room:
                print(self.where_am_i().description)  # Room description only if rooms are changing.
                item_list = []
                for x in self.where_am_i().bag:
                    # print(str(Responses.YOU_SEE) + x.name + ".")
                    print(x.description_room)

            self.print_directions(self.where_am_i())

            command = input(Responses.AND_NOW)      # Ask for command

            what_to_do = self.pars.parse_spacy(command) # Parse the command using spacy

            if debug.DEBUG:
                print("-" * 40)
                if command == "db.items":
                    for x in self.my_world.find_room_by_id(self.ego.room).bag:
                        print(x.name)

                # print(self.pars.parse(command))

                for x in what_to_do:
                    print("------------")
                    print(x.dir_id, x.verb_id, x.obj1_id, x.obj2_id, x.is_question)
                print("-" * 40)

            # what to do can be more than one command set
            # Work thou one command at a time
            for cmd in what_to_do:
                if cmd.dir_id != 0:  # move, if direction is filled ignore verb and object
                    last_room = self.where_am_i().id    # Save the current room in the last room variable
                    self.move(cmd)                      # Try to move the player
                elif cmd.verb_id != 0:                  # do something, found a verb
                    self.just_do_it(cmd)
                else:
                    print(Responses.NO_IDEA)            # if no verb was found and no direction given


if __name__ == "__main__":
    great_game = Game()     # create the game object
    great_game.intro()      # Print out intro text

    name = input(Responses.YOUR_NAME)   # Ask for Player name
    
    print(Responses.WELCOME.format(name))   # Say thank you and welcome
    great_game.ego.name = name  # save the name in the player

    great_game.loop()   # start the game loop
