class Responses:
    """
    Responses to commands which should be localized
    """
    YOU_CARRY = "Du trägst: "
    AND_NOW = "Was nun? "
    ALREADY_HAVE = "Du hast {0!s} doch schon.\n"
    IS_NOT_HERE = "Das sehe ich hier nicht.\n"
    NO_TO_TAKE = "Du kannst {0!s} nicht mitnehmen.\n"
    TAKE_IT = "Du steckst {0!s} ein.\n"
    YOU_SEE = "Du siehst: "
    EXITS = "Mögliche Ausgänge sind: "
    CARRY_NOTHING = "Du leerst alle Deine Taschen, aber Du findest nichts."
    YOUR_NAME = "Sag mir zu allererst, wie Du heißt: "
    WELCOME = "Herzlich willkommen {0!s}. Viel Spaß im Spiel.\n"
    NOT_POSSIBLE_TO_GO = "Du kannst nicht in diese Richtung gehen.\n"
    YOU_MOVED = "Du wechselst den Raum.\n"
    NO_IDEA = "Ich verstehe dich nicht. Versuche 'HILFE', um Vorschläge für mögliche Aktionen zu bekommen.\n"
    YOU_DROP = "Du lässt {0!s} fallen."
    NO_HAVE = "Du hast {0!s} nicht."
    WHAT_TO_DROP = "Du legst Dich hin und Du stehst wieder auf."
    GENERAL_LOOK = "Du schaust dich um, doch do siehst nichts spezielles."
    GENERAL_LOOK_AT = "{0!s} sieht nicht besonders aus."



class DirText:
    """
    Texts of the directions
    """

    # N, S, W, O, NW, NO, SW, SO, U, D
    N = "Norden"
    S = "Süden"
    W = "Westen"
    O = "Osten"
    NW = "Nordwesten"
    NO = "Nordosten"
    SW = "Südwesten"
    SO = "Südosten"
    U = "Rauf"
    D = "Runter"

    def __init__(self):
        self.directionList = [DirText.N, DirText.S, DirText.W, DirText.O, DirText.NW, DirText.NO, DirText.SW, DirText.SO, DirText.U, DirText.D]

class DirShorts:
    """
    Short Texts for directions - used to import from xml file
    """

    def __init__(self):
        self.directionDict = \
            {
                "N": 0,
                "S": 1,
                "W": 2,
                "E": 3,
                "NW": 4,
                "NO": 5,
                "SW": 6,
                "SO": 7,
                "U": 8,
                "D": 9
            }