from __future__ import absolute_import

import copy
import music21 as m2
import collections
import random
import math

from .note import Note
from .interval import Interval
from .helper import suf, reverseDict, CONSTANT, flatten, warning, cyclelist

class Chord():
    """
    The chord class.
    """
    def __init__(self, root='C', chord_type='', chord_recipe=[], chord_notes=[], inversion=0, duration=1., bass=''):
        if isinstance(root, str): root=Note(root)
        self.root, self.chord_type, self.chord_recipe, self.chord_notes =  self._check(root, chord_type, chord_recipe, chord_notes)

        if inversion:
            if not (isinstance(inversion, int) and 0 <= inversion <= len(self.chord_recipe)-1):
                raise ValueError(f"Chord inversion failed.")
            self.bass = self.chord_notes[inversion]
            self.chord_notes = self.chord_notes[inversion:] + [note.changeOctave(1) if note.getSemiSteps() < self.chord_notes[-1].getSemiSteps() else note for note in self.chord_notes[:inversion]]
            self.chord_recipe = Chord.buildRecipe(self.chord_notes)
        else:
            self.bass = copy.deepcopy(self.root)

        if bass != '' and self.bass != bass:
            self.setBass(bass)

        self.inversion = inversion
        self.arpeggio = self.buildArpeggio()
        self.duration = duration

    def setBass(self, note):
        bass = Note(note)
        if self.bass > self.root:
            raise ValueError(f"bass note {self.bass} is above chord root")

        if bass.name in [note.name for note in self.chord_notes]:
            chord_notes = [bass] + [note for note in self.chord_notes if note.name != bass.name]
        else:
            chord_notes = [bass] + self.chord_notes

        self.bass = bass
        self.chord_notes = chord_notes

    @staticmethod
    def pharseChord(text='C.m', inversion=0, duration=1.):
        if '.' in text:
            bass, chord_type = text.split('.')
            return Chord(root=bass, chord_type=chord_type, inversion=inversion, duration=duration)
        else:
            return Chord(root=text, inversion=inversion, duration=duration)

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

    @staticmethod
    def buildRecipe(chord_notes):
        return [Interval('P1')] + [Interval.getInterval(base=chord_notes[0], target=note) for note in chord_notes[1:]]

    @staticmethod
    def displayAllChordsRecipe():
        return list(CONSTANT.chord_recipes().keys())

    def m2(self):
        chord = m2.chord.Chord([note.nameWithOctave.replace('b', '-') for note in self.chord_notes])
        chord.quarterLength = self.duration
        return chord

    def getInversion(self, order=1):
        assert 0<=order <= len(self.chord_recipe)-1, f"Chord inversion failed."
        return Chord(self.root, self.chord_type, inversion=order, duration=self.duration)

    def show(self, show_type = ''):
        from .stream import Stream
        stream = Stream([self])
        stream.show(show_type)

    def type(self):
        return 'Chord'

    def buildArpeggio(self, length=4., unit=1/4, kind='up'):
        # TODO: need more refine. Hard to define a proper Arpeggio
        if unit not in CONSTANT.arpeggio_note_units():
            raise ValueError(f"unit {unit} invalid, should be in {CONSTANT.arpeggio_note_units()} ")

        if kind not in CONSTANT.argeggio_kinds():
            raise ValueError(f"kind {kind} invalid, should be in {CONSTANT.argeggio_kinds()}")

        if int(length % unit):
            raise ValueError(f"length not valid. Set to be even times of 1/16 or 1/6")

        notes_count = int(length / unit)
        arpeggio_group = [note.setDuration(unit) for note in self.chord_notes]

        groups_count = math.ceil(notes_count / len(self.chord_notes))

        if kind == 'up':
            return (arpeggio_group * groups_count)[:notes_count]
        if kind == 'Up':
            return flatten([Note.changeNotesOctave(arpeggio_group, 1) if i%2 else arpeggio_group for i in range(groups_count)])[:notes_count]

        if kind == 'down':
            return (arpeggio_group[::-1] * groups_count)[:notes_count]
        if kind == 'Down':
            return flatten([Note.changeNotesOctave(arpeggio_group[::-1], -1) if i%2 else arpeggio_group[::-1] for i in range(groups_count)])[:notes_count]

        if kind == 'hill':
            return flatten([arpeggio_group[::-1] if i%2 else arpeggio_group for i in range(groups_count)])[:notes_count]
        # if kind == 'Hill': ## TODO: need refine
            # return flatten([Note.changeNotesOctave(arpeggio_group[::-1], -1) if i%2 else Note.changeNotesOctave(arpeggio_group, -1) for i in range(groups_count)])[:notes_count]

        if kind == 'valley':
            return flatten([arpeggio_group if i%2 else arpeggio_group[::-1]] for i in range(groups_count))[:notes_count]
        # if kind == 'Valley': ## TODO: need refine
            # return flatten([Note.changeNotesOctave(arpeggio_group[::-1], -1) if i%2 else arpeggio_group[::-1] for i in range(groups_count)])[:notes_count]

    @staticmethod
    def matchChord(obj, verbose=False):
        if not isinstance(obj, list) and obj.type() == 'Chord':
            notes = obj.chord_notes
        else:
            notes = obj
        sorted_notes = Note.sortNotes(notes)
        notes_recipe = Chord.buildRecipe(sorted_notes)
        for k, v in CONSTANT.chord_recipes().items():
            if notes_recipe in cyclelist(v): # TODO: clear wrong, need refine
                if verbose:
                    return Chord(sorted_notes[0], k)
                else:
                    return k
        else:
            warning('No match found!')
            return 

    def expandChord(self):
        bass = self.root.changeOctave(-1)
        notes = [bass] + [bass.applyInterval('P5')] + self.chord_notes + [self.root.changeOctave(1)]
        return Chord(bass, chord_type='user', chord_notes = notes, duration=self.duration)

    def closeChord(self):
        pass

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