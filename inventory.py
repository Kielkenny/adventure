
class Item:
    """
    One item
    """
    def __init__(self, id=0, desc="", take=True, name="", desc_room=""):
        """ :arg id = item number
            :arg desc = description of the item if you look at
            :arg take = true if the player can pick it up
            ;arg name = short name of the item
            ;arg desc_room = the description of the item when it is found in a room
        """
        self.id = id
        self.name = name
        self.description = desc
        self.takeable = take
        self.description_room = desc_room
