from .interval import Interval
from .note import Note
from .chord import Chord
from .scale import Scale

class Style():
    """
    The style class.
    """
    style_recipes = {
                    'major_triads':['M', 'm', 'm', 'M', 'M', 'm', 'dim','M'],
                    'minor_triads':['m', 'dim', 'M', 'm', 'm', 'M', 'M','m'],
                    'major_sevenths': ['maj7', 'min7', 'min7', 'maj7', 'dom7', 'min7', 'min7b5','maj7'],
                    'minor_sevenths': ['min7', 'min7b5', 'maj7', 'min7', 'min7', 'maj7', 'dom7','min7']
                    }

    def __init__(self, root='C', style_type='major_triads'):
        self.chords = []

        try:
            self.root = root
        except:
            raise Exception('Invalid root note supplied.')

        if 'major' in style_type:
            self.notes = list(map(str, Scale(self.root, 'major').notes))
            print(self.notes)
        elif 'minor' in style_type:
            self.notes = list(map(str, Scale(self.root, 'natural_minor').notes))
        else:
            raise Exception('Unknow mode! current valid types: major, minor')


        if style_type in self.style_recipes.keys():
            self.style_type = style_type
        else:
            raise Exception('Invalid style type supplied! current valid types: {} '.format(self.style_recipes.keys()))

        self.build_style()

    def build_style(self):
        self.add_chords(self.style_recipes[self.style_type][0:])

    def all_styles(self):
        return self.style_recipes.keys()

    def add_chords(self, chords):
        for i in range(len(chords)):
            self.chords.append(Chord(self.notes[i], chords[i]))

    def __repr__(self):
        return "style(Note({!r}), {!r})".format(str(self.root), self.style_type)

    def __str__(self):
        return "{}{}".format(str(self.root),self.style_type)

    # def __eq__(self, other):
    #     if len(self.notes) != len(other.notes):
    #         #if styles dont have the same number of notes, def not equal
    #         return False
    #     else:
    #         return all(self.notes[i] == other.notes[i] for i in range(len(self.notes)))