

from .note import Note
from .interval import Interval
from .chord import Chord
from .helper import CONSTANT

class Scale(object):
    def __init__(self, root='C', scale_type = '', scale_recipe=[], scale_notes=[], durations=[]):
        if isinstance(root, str): root = Note(root)
        self.root, self.scale_type, self.scale_recipe, self.scale_notes = self._check(root, scale_type, scale_recipe, scale_notes)
        self.durations=durations

    def _check(self, root, scale_type, scale_recipe, scale_notes):
        # TODO: not start
        return root, scale_type, scale_recipe, scale_notes

    def matchScale(self):
        # TODO: not start
        pass

    def associateChord(self):
        # TODO: not start
        pass

    @staticmethod
    def pharseScale(text='C.major'):
        if '.' in text:
            root, scale_type = text.split('.')
            return Scale(root=root, scale_type=scale_type)
        else:
            return Scale(root=root, scale_type='natural major')

    @staticmethod
    def displayAllScalesRecipe():
        return list(CONSTANT.scale_recipes().keys())

    @staticmethod
    def buildScale(root, scale_recipe):
        return [Interval.applyInterval(root, interval) for interval in scale_recipe]

    @staticmethod
    def buildRecipe(scale_notes):
        return [Interval.getInterval(base=scale_notes[0], target=note) for note in scale_notes]

    def m2(self):
        m2scale = [m2.note.Note(note.nameWithOctave.replace('b', '-')) for note in self.scale_notes]
        if isinstance(self.durations, float):
            for note in m2scale:
                note.quarterLength = self.durations
        elif isinstance(self.durations, list) and len(self.durations) == len(self.scale_notes):
            for idx, note in enumerate(m2scale):
                note.quarterLength = self.durations[idx]
        else:
            raise ValueError(f"music21 scale failed to convert")

        return m2scale

    def __repr__(self):
        return f"Scale(Root({self.root.name}), {self.scale_type})"

    def __str__(self):
        return f"{self.root.name}{self.scale_type}"

    def __eq__(self, other):
        if len(self.scale_notes) != len(other.scale_notes):
            return False
        else:
            return all(self.scale_notes[i] == other.scale_notes[i] for i in range(len(self.scale_notes)))