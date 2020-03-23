from __future__ import absolute_import

import re
import music21 as m2

from .helper import reverseDict, CONSTANT
from collections import Counter

class Note(object):
    __all__ = ['show', 'transpose', 'semiSteps', 'simplify']

    def __init__(self, note='C', duration=1.):
        self.nameWithOctave = self._check(note)
        self.name = self.nameWithOctave[:-1]
        self.octave = int(self.nameWithOctave[-1])
        self.tone = self.nameWithOctave[0]
        self.accidental = self.nameWithOctave[1:-1]
        self.duration = duration

    def _check(self, note):
        if not isinstance(note, str):   raise ValueError('Note has to be a string')
        if note == '':  note = 'C'
        if not note[-1].isdigit(): note += '4'
        accidentals = Counter(note[1:-1])
        bool_acc = (len(accidentals) == 0) or (len(accidentals) == 1 and list(accidentals.keys())[0] in 'b#' and list(accidentals.values())[0] <= 4)
        # if not bool(re.match("[A-G](#{0,4}|(b|-){0,4})[1-9]", note)): regRex Error?
        if not ((note[0] in 'CDEFGAB') and bool_acc and (note[-1] in '123456789')):
            raise ValueError('Note invalid! example: Ab, Abb3, G5, B###')
        return note

    def show(self, kind = ''):
        from .stream import Stream
        stream = Stream([self])
        stream.show(kind)

    def type(self):
        return 'Note'

    def transpose(self, steps=0, accidental_type='#'):
        semi_steps = self.getSemiSteps()
        return self.applySemiSteps(semi_steps+steps, accidental_type)

    def m2note(self):
        note = m2.note.Note(self.nameWithOctave.replace('b','-'))
        note.quarterLength = self.duration
        return note

    def getSemiSteps(self):
        octave_steps = 12 * (self.octave - 4)
        tone_steps = CONSTANT.tone_to_semisteps[self.tone]
        alter_steps = CONSTANT.accidental_to_step[list(set(self.accidental))[0]] * len(self.accidental) if self.accidental else 0
        return octave_steps + tone_steps + alter_steps

    def simplify(self, accidental_type='#'):
        if not accidental_type in 'b#':
            raise ValueError(f'{accidental_type} invalid!')
        semi_steps = self.getSemiSteps()
        return Note.applySemiSteps(semi_steps, accidental_type)

    def applyInterval(self, interval='P1'):
        from .interval import Interval
        if isinstance(interval, str): interval=Interval(interval)
        return Interval.applyInterval(self, interval)

    @staticmethod
    def applySemiSteps(semi_steps=0, accidental_type='#'):
        octave, residual = semi_steps // 12, semi_steps % 12
        names = CONSTANT.semisteps_to_tone[residual]
        if len(names) == 1:
            return Note(names[0] + str(octave+4))
        else:
            for name in names:
                if accidental_type in name:
                    return Note(name + str(octave+4))

    def changeOctave(self, diff=0):
        return Note(self.name + str(self.octave+diff))

    def __repr__(self):
        return f"Note({(self.nameWithOctave if self.octave!=4 else self.name)})"

    def __str__(self):
        return self.nameWithOctave if self.octave!=4 else self.name

    def __eq__(self, other):
        if isinstance(other, str): other=Note(other)
        return self.nameWithOctave == other.nameWithOctave