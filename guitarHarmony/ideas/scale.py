from .interval import Interval
from .note import Note

class Scale():
    """
    The scales class.
    """
    scale_recipes = {
        'major' :           ['M2', 'M3', 'P4', 'P5', 'M6', 'M7', 'P8'],
        'natural_minor':    ['M2', 'm3', 'P4', 'P5', 'm6', 'm7', 'P8'],
        'harmonic_minor':   ['M2', 'm3', 'P4', 'P5', 'm6', 'M7', 'P8'],
        'melodic_minor':    ['M2', 'm3', 'P4', 'P5', 'M6', 'M7', 'P8'],
        'dorian':           ['M2', 'm3', 'P4', 'P5', 'M6', 'm7', 'P8'],
        'locrian':          ['m2', 'm3', 'P4', 'd5', 'm6', 'm7', 'P8'],
        'lydian':           ['M2', 'M3', 'A4', 'P5', 'M6', 'M7', 'P8'],
        'mixolydian':       ['M2', 'M3', 'P4', 'P5', 'M6', 'm7', 'P8'],
        'phrygian':         ['m2', 'm3', 'P4', 'P5', 'm6', 'm7', 'P8'],
        'major_pentatonic': ['M2', 'M3', 'P5', 'M6', 'P8'],
        'minor_pentatonic': ['m3', 'P4', 'P5', 'm7', 'P8'],
        'alter': ['m2', 'm3', 'P4', 'd5', 'm6', 'm7', 'P8'],
        'blues':['m3', 'P4', 'd5', 'P5', 'm7', 'P8'],
        'lydian_dominant':['M2', 'M3', 'A4', 'P5', 'M6', 'm7', 'P8']
    }


    def __init__(self, root='C', scale_type = 'major'):
        self.notes = []

        try:
            self.notes.append(Note(root))
        except:
            raise Exception('Invalid root note supplied.')

        if scale_type in self.scale_recipes.keys():
            self.scale_type = scale_type
        else:
            raise Exception('Invalid scale type supplied! current valid types: {} '.format(self.scale_recipes.keys()))

        self.build_scale()

    def all_scales(self):
        return self.scale_recipes.keys()

    def build_scale(self):
        self.add_intervals(self.scale_recipes[self.scale_type][0:])

    def add_intervals(self, intervals):
        for i in intervals:
            self.notes.append(self.notes[0]+Interval(i))

    def __repr__(self):
        return "Scale(Note({!r}), {!r})".format(str(self.notes[0]), self.scale_type)

    def __str__(self):
        return "{}{}".format(str(self.notes[0]),self.scale_type)

    def __eq__(self, other):
        if len(self.notes) != len(other.notes):
            #if chords dont have the same number of notes, def not equal
            return False
        else:
            return all(self.notes[i] == other.notes[i] for i in range(len(self.notes)))

