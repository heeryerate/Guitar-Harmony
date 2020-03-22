from __future__ import absolute_import

import copy
import music21 as m2

from .note import Note
from .interval import Interval
from .helper import suf, reverseDict

class Chord():
    """
    The chord class.
    """
    chord_recipes = {''         : ['P1', 'M3', 'P5'],
                     'm'        : ['P1', 'm3', 'P5'],
                     'dim'      : ['P1', 'm3', 'd5'],
                     'aug'      : ['P1', 'M3', 'A5'],

                     '7'        : ['P1', 'M3', 'P5', 'm7'],
                     'm7'       : ['P1', 'm3', 'P5', 'm7'],
                     'maj7'     : ['P1', 'M3', 'P5', 'M7'],
                     'dim7'     : ['P1', 'm3', 'd5', 'd7'],
                     'm7b5'     : ['P1', 'm3', 'd5', 'd7'],
                     'mmaj7'    : ['P1', 'm3', 'P5', 'M7'],
                     'aug7'     : ['P1', 'M3', 'A5', 'm7'],
                     'aug-maj7' : ['P1', 'M3', 'A5', 'M7'],
                     '7b5'      : ['P1', 'M3', 'd5', 'm7'],
                     '7#5'      : ['P1', 'M3', 'A5', 'm7'],

                     'sus2'     : ['P1', 'M2', 'P5'],
                     'sus4'     : ['P1', 'P4', 'P5'],
                     }

    alter_recipes = {
                     'power5'   : ['P1', 'P5'],
                     'add2'     : ['M9'],
                     }

    tone_to_order = {'C':1, 'D':2, 'E':3, 'F':4, 'G':5, 'A':6, 'B':7}
    order_to_tone = reverseDict(tone_to_order)

    def __init__(self, root='C', chord_type=None, inversion=0, notes_recipe=[]):
        if isinstance(root, str): root=Note(root)
        self.bass = root
        self.root = root
        self.inversion = inversion
        self.notes = []

        if chord_type in self.chord_recipes.keys():
            self.chord_type = chord_type
            self.chord_recipe = self.chord_recipes[chord_type]
        elif chord_type is None and len(notes_recipe) >= 2:
            self.chord_type = 'user'
            self.chord_recipe = ['P1'] + [Interval.getIntervals(base=notes_recipe[0], target=note) for note in notes_recipe[1:]]
        else:
            raise Exception(f'Invalid chord type {chord_type}! Current valid types at Chord.displayAllChords()')

        self.buildChord(self.chord_recipe)

        if self.inversion:
            assert 0<=inversion<= len(self.chord_recipe)-1, f"Chord inversion failed."
            self.bass = self.notes[inversion]
            self.notes = self.notes[inversion:] + [note.changeOctave(1) if note.semiSteps() < self.notes[-1].semiSteps() else note for note in self.notes[:inversion]]
            self.chord_recipe = self.chord_recipe[inversion:] + self.chord_recipe[:inversion]

        self.buildArpeggio(self.notes)

    def buildChord(self, chord_recipe):
        self.notes = [Interval.applyInterval(self.root, interval) for interval in chord_recipe]

    @staticmethod
    def displayAllChords():
        return list(Chord.chord_recipes.keys())

    def getInversion(self, order=1):
        assert 0<=order <= len(self.chord_recipe)-1, f"Chord inversion failed."
        return Chord(self.root, self.chord_type, inversion=order)

    def show(self, show_type = ''):
        from .stream import Stream
        stream = Stream([self])
        stream.show(show_type)

    def instanceCheck(self):
        return 'Chord'

    def buildArpeggio(self, notes):
        self.arpeggio = self.notes

    def __repr__(self):
        return f"Chord(Root({self.root.name}), {self.chord_type}, Bass({self.bass.name}))"

    def __str__(self):
        if len(self.notes) == 2:
            return f"Inv.{self.chord_recipe[-1]}"

        if self.inversion:
            return f"{self.root.name}{self.chord_type}/{self.bass.name}"
        else:
            return f"{self.root.name}{self.chord_type}"

    def __eq__(self, other):
        if len(self.notes) != len(other.notes):
            return False
        else:
            return all(self.notes[i] == other.notes[i] for i in range(len(self.notes)))