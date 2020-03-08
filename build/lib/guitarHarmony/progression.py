from .interval import Interval
from .note import Note
from .chord import Chord
from .scale import Scale

class Progression():
    """
    The progression class.
    """
    progression_recipes = {
                    'major_triads':['', 'm', 'm', '', '', 'm', 'dim',''],
                    'minor_triads':['m', 'dim', '', 'm', 'm', '', '','m'],
                    'major_sevenths': ['maj7', 'm7', 'm7', 'maj7', '7', 'm7', 'm7b5','maj7'],
                    'minor_sevenths': ['m7', 'm7b5', 'maj7', 'm7', 'm7', 'maj7', '7','m7']
                    }

    def __init__(self, root='C', progression_type='major_triads'):
        self.chords = []

        try:
            self.root = root
        except:
            raise Exception('Invalid root note supplied.')

        if 'major' in progression_type:
            self.notes = list(map(str, Scale(self.root, 'major').notes))
        elif 'minor' in progression_type:
            self.notes = list(map(str, Scale(self.root, 'natural_minor').notes))
        else:
            raise Exception('Unknow mode! current valid types: major, minor')

        if progression_type in self.progression_recipes.keys():
            self.progression_type = progression_type
        else:
            raise Exception('Invalid progression type supplied! current valid types: {} '.format(self.progression_recipes.keys()))

        self.build_progression()

    def build_progression(self):
        self.add_chords(self.progression_recipes[self.progression_type][0:])

    def all_progressions(self):
        return self.progression_recipes.keys()

    def add_chords(self, chords):
        for i in range(len(chords)):
            self.chords.append(Chord(self.notes[i], chords[i]))

    def __repr__(self):
        return "progression(Note({!r}), {!r})".format(str(self.root), self.progression_type)

    def __str__(self):
        return "{}{}".format(str(self.root),self.progression_type)

    # def __eq__(self, other):
    #     if len(self.notes) != len(other.notes):
    #         #if progressions dont have the same number of notes, def not equal
    #         return False
    #     else:
    #         return all(self.notes[i] == other.notes[i] for i in range(len(self.notes)))