from __future__ import absolute_import

import copy
import music21 as m2
import collections

from .note import Note
from .interval import Interval
from .helper import suf, reverseDict, CONSTANT

class Chord():
    """
    The chord class.
    """
    def __init__(self, root='C', chord_type='', chord_recipe=[], chord_notes=[], inversion=0):
        if isinstance(root, str): root=Note(root)
        self.root, self.chord_type, self.chord_recipe, self.chord_notes =  self._check(root, chord_type, chord_recipe, chord_notes)

        if inversion:
            if not (isinstance(inversion, int) and 0 <= inversion <= len(self.chord_recipe)-1):
                raise ValueError(f"Chord inversion failed.")
            self.bass = self.chord_notes[inversion]
            self.chord_notes = self.chord_notes[inversion:] + [note.changeOctave(1) if note.getSemiSteps() < self.chord_notes[-1].getSemiSteps() else note for note in self.chord_notes[:inversion]]
            self.chord_recipe = self.chord_recipe[inversion:] + self.chord_recipe[:inversion]
        else:
            self.bass = copy.deepcopy(self.root)

        self.inversion = inversion
        self.arpeggio = self.buildArpeggio()

    def _check(self, root, chord_type, chord_recipe, chord_notes):
        if chord_type not in CONSTANT.chord_recipes().keys():
            raise ValueError(f'Invalid chord type {chord_type}! Current valid types at Chord.displayAllChords()')

        if chord_type != 'user':
            chord_recipe_ref = CONSTANT.chord_recipes()[chord_type]
            chord_notes_ref= self.buildChord(root, chord_recipe_ref)
            if chord_notes != [] and chord_notes != chord_notes_ref:
                raise ValueError(f'{chord_type} do not match chord_notes {chord_notes}')
            if chord_recipe != [] and chord_recipe_ref != chord_recipe:
                raise ValueError(f'{chord_type} do not match chord_recipe {chord_recipe}')
            chord_recipe, chord_notes = chord_recipe_ref, chord_notes_ref
        else:
            if chord_recipe == [] and chord_notes == []:
                raise ValueError(f'user chord type not specified!')
            elif chord_recipe == [] and len(chord_notes) >= 2:
                chord_recipe = self.buildRecipe(chord_notes)
            elif chord_notes == [] and len(chord_recipe) >= 2:
                chord_notes = self.buildChord(root, chord_recipe)
            elif len(chord_notes) >= 2 and len(chord_recipe) >= 2:
                chord_notes_ref = self.buildChord(root, chord_recipe)
                if chord_notes_ref != chord_notes:
                    raise ValueError(f'{chord_recipe} and {chord_notes} do not match')
            else:
                raise ValueError(f'{chord_recipe} and {chord_notes} do not match or can not construct chord')
        
        if root != chord_notes[0]:
            raise ValueError(f'root {root} and chord_notes {chord_notes} not match.')

        chord_recipe = [Interval(interval) if isinstance(interval, str) else interval for interval in chord_recipe]
        chord_notes = [Note(note) if isinstance(note, str) else note for note in chord_notes]

        if Note.sortNotes(chord_notes) != chord_notes:
            raise ValueError(f'chord notes {chord_notes} is not sorted.')

        return root, chord_type, chord_recipe, chord_notes

    @staticmethod
    def buildChord(root, chord_recipe):
        return [Interval.applyInterval(root, interval) for interval in chord_recipe]

    def buildRecipe(self, chord_notes):
        return [Interval('P1')] + [Interval.getInterval(base=chord_notes[0], target=note) for note in chord_notes[1:]]

    @staticmethod
    def displayAllChordsRecipe():
        return list(CONSTANT.chord_recipes().keys())

    def m2chord(self):
        # TODO: need test
        chord = m2.chord.Chord(self.chord_notes)
        return chord

    def getInversion(self, order=1):
        assert 0<=order <= len(self.chord_recipe)-1, f"Chord inversion failed."
        return Chord(self.root, self.chord_type, inversion=order)

    def show(self, show_type = ''):
        from .stream import Stream
        stream = Stream([self])
        stream.show(show_type)

    def type(self):
        return 'Chord'

    def buildArpeggio(self):
        #TODO: need refine
        notes = copy.deepcopy(self.chord_notes)
        for note in notes:
            note.duration = 0.25
        return notes+notes[::-1]+notes+notes[::-1]

    def __repr__(self):
        return f"Chord(Root({self.root.name}), {self.chord_type}, Bass({self.bass.name}))"

    def __str__(self):
        if len(self.chord_notes) == 2:
            return f"Inv.{self.chord_recipe[-1]}"

        if self.inversion:
            return f"{self.root.name}{self.chord_type}/{self.bass.name}"
        else:
            return f"{self.root.name}{self.chord_type}"

    def __eq__(self, other):
        if len(self.chord_notes) != len(other.chord_notes):
            return False
        else:
            return all(self.chord_notes[i] == other.chord_notes[i] for i in range(len(self.chord_notes)))