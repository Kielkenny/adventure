import spacy
import copy
import debug

class Word:
    """
    Stores a single word with ID and Type
    """
    def __init__(self, word, wtype, wid):
        self.word = word
        self.word_type = wtype
        self.id = wid

class Understood:
    """
    Stores what was understood by the parser as in words found in the wordlist
    stores the ids based in the wordfile
    """
    def __init__(self):
        self.verb_id = 0
        self.dir_id = 0
        self.obj1_id = 0
        self.obj2_id = 0
        self.is_question = False

    def clear(self):
        self.verb_id = 0
        self.dir_id = 0
        self.obj1_id = 0
        self.obj2_id = 0
        self.is_question = False

class Adv_Parser:
    """
    Class to handle the parsing.
    """

    def __init__(self):
        """
        Initializes the blank word list and the spacy parser
        """
        self.wordlist = []
        self.nlp = spacy.load("de_core_news_sm")

    def load_words(self):
        """
        Loads word list which will be understood by the adventure
        """
        with open(r".\res\words.csv", "r", encoding="utf-8") as wordfile:
            # csv_file = csv.reader(wordfile, delimiter=";")
            for row in wordfile:
                a,b,c = row.split(";")
                w = Word(a, int(b), int(c))
                self.wordlist.append(w)

    def parse(self, command):
        verb = direction = obj1 = obj2 = adj = out = 0

        for w in command.split(" "):
            for lookup in self.wordlist:
                if w.lower() == lookup.word:
                    if lookup.word_type == 1:
                        verb = lookup.id
                    elif lookup.word_type == 2:
                        direction = lookup.id
                    elif lookup.word_type == 3:
                        if obj1 == 0:
                            obj1 = lookup.id
                        else:
                            obj2 = lookup.id
                    elif lookup.word_type == 4:
                        adj = lookup.id
                    else:
                        out = lookup.id

        return [verb, direction, obj1, obj2, adj, out]


    def lookup_word(self, w):
        """
        Looks up w in the wordlist and returns the type and the id if found otherwise 0,0
        :param w: word to lookup
        :return: type and id if found
        """
        for lookup in self.wordlist:
            if w.lower() == lookup.word:
                return [int(lookup.word_type), int(lookup.id)]

        return [0, 0]

    def parse_spacy(self, command):
        """
        Parses command using spacy returns list of commands
        ;param command: user entry for command
        ;return list of Understood
        """
        doc = self.nlp(command)

        return_commands = []

        ud = Understood()

        for token in doc:
            if token.pos_ in ["NOUN",  "VERB", "PUNCT", "CCONJ", "ADJ", "X", "ADV", "PART", "PROPN"]:      #ignore everything which is not a noun or a verb or a conjucntion
                if token.pos_ == "PUNCT" or token.lemma_ == "und":   # command end and add in case of interpunction or the word "und"
                                                                     # TODO put "und" in variable
                    ud.is_question = (token.lemma_ == "?")
                    if ud.verb_id != 0 or ud.dir_id != 0: # return if at least a verb or a direction was found
                        return_commands.append(copy.deepcopy(ud))
                    ud.clear() # reset
                else:
                    wordtype, id = self.lookup_word(token.lemma_)

                    if debug.DEBUG:
                        print(f"typ {wordtype}, ID {id} {token.lemma_}")
                    if wordtype == 0:
                        wordtype, id = self.lookup_word(token.text)

                    if wordtype == 1:
                        ud.verb_id = id
                    if wordtype == 2:
                        ud.dir_id = id
                    if wordtype == 3: # store a maximum of two objects per command
                        if ud.obj1_id == 0:
                            ud.obj1_id = id
                        elif ud.obj2_id == 0:
                            ud.obj2_id = id
            if debug.DEBUG:
                print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
        if ud.verb_id != 0 or ud.dir_id != 0:  # return if at least a verb or a direction was found
            return_commands.append(copy.deepcopy(ud))
        return return_commands