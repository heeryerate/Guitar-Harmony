from .interval import Interval
from .note import Note

class Chord():
    """
    The chord class.
    """
    chord_recipes = {'': ['R', 'M3', 'P5'],
                     'm': ['R', 'm3', 'P5'],
                     'dim': ['R', 'm3', 'd5'],
                     'aug': ['R', 'M3', 'A5'],
                     'open5': ['R', 'P5', 'P8'],
                     'dim7': ['R', 'm3', 'd5', 'd7'],
                     'm7b5': ['R', 'm3', 'd5', 'd7'],
                     'maj7': ['R', 'M3', 'P5', 'M7'],
                     'm7': ['R', 'm3', 'P5', 'm7'],
                     '7': ['R', 'M3', 'P5', 'm7'],
                     'aug7': ['R', 'M3', 'A5', 'm7'],
                     'sus2': ['R', 'P5', 'P8', 'M2'],
                     'sus4': ['R', 'P4', 'P5'],
                     'add2': ['R', 'M2', 'M3', 'P5'],
                     'madd2': ['R', 'M2', 'm3', 'P5'],
                     }

    def __init__(self, root='C', chord_type=''):
        self.notes = []

        try:
            self.notes.append(Note(root))
        except:
            raise Exception('Invalid root note supplied.')

        if chord_type in self.chord_recipes.keys():
            self.chord_type = chord_type
        else:
            raise Exception('Invalid chord type {} supplied! current valid types: {} '.format(chord_type, self.chord_recipes.keys()))

        self.build_chord()

    def build_chord(self):
        self.add_intervals(self.chord_recipes[self.chord_type][1:])

    def all_chords(self):
        return self.chord_recipes.keys()

    def add_intervals(self, intervals):
        for i in intervals:
            self.notes.append(self.notes[0]+Interval(i))

    def __repr__(self):
        return "Chord(Note({!r}), {!r})".format(str(self.notes[0]), self.chord_type)

    def __str__(self):
        return "{}{}".format(str(self.notes[0]),self.chord_type)

    def __eq__(self, other):
        if len(self.notes) != len(other.notes):
            #if chords dont have the same number of notes, def not equal
            return False
        else:
            return all(self.notes[i] == other.notes[i] for i in range(len(self.notes)))