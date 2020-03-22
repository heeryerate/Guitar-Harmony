from __future__ import absolute_import

import re
import music21 as m2

from .helper import reverseDict

class Note(object):
    """
    The note class. 

    The notes are to be parsed in the following way:
    * the letter name,
    * accidentals (up to 4),
    * octave (default is 4).

    For example, 'Ab', 'A-', 'A--3', 'G3', 'B##4' are all valid notes. '#', 'A9b',
    'Dbbbbb' are not.
    """
    __all__ = ['show', 'transpose', 'semiSteps', 'simplify']
    tone_to_step = {'C':0, 'D':2, 'E':4, 'F':5, 'G':7, 'A':9, 'B':11}
    step_to_tone = {0:'C', 1:'C#,Db', 2:'D', 3:'D#,Eb', 4:'E', 5:'F', 
                    6:'F#,Gb',7:'G',8:'G#,Ab',9:'A',10:'A#,Bb', 11:'B'}

    def __init__(self, note='C'):
        self.m2note = m2.note.Note(pitchName = self._check(note), keywords={})
        self._updateAttrs()

    def _check(self, note):
        assert isinstance(note, str), 'note has to be a string'
        if note == '': note = 'C4'
        if not note[-1].isdigit(): note += '4'
        assert bool(re.match("[A-G](#{0,4}|(b|-){0,4})[1-9]", note)), 'Note invalid! example: Ab, A-, A--3, G3, B##4'
        return note.replace('-', 'b')

    def _updateAttrs(self):
        self.name = self.m2note.name.replace('-','b')
        self.pitch = self.m2note.pitch
        self.octave = self.m2note.octave if self.m2note.octave is not None else 4
        self.duration = self.m2note.duration
        self.nameWithOctave = self.m2note.nameWithOctave
        self.lyric = self.m2note.lyric
        self.tone = self.m2note.step

    def show(self, show_type = ''):
        from .stream import Stream
        stream = Stream([self])
        stream.show(show_type)

    def instanceCheck(self):
        return 'Note'

    def transpose(self, step=0):
        return Note(self.m2note.transpose(step).nameWithOctave)

    def semiSteps(self):
        octave_steps = 12 * (self.octave - 4)
        tone_steps = self.tone_to_step[self.m2note.step]
        alter_steps = int(self.pitch.accidental.alter) if self.pitch.accidental is not None else 0
        return octave_steps + tone_steps + alter_steps

    def simplify(self, accidental_type='#'):
        semi_steps = self.semiSteps()
        octave, residual = semi_steps // 12, semi_steps % 12
        if residual in self.tone_to_step.values():
            pitchName = self.step_to_tone[residual]+str(octave+4)
        else:
            if accidental_type == '#':
                pitchName = self.step_to_tone[residual].split(',')[0] + str(octave+4)
            elif accidental_type == 'b':
                pitchName = self.step_to_tone[residual].split(',')[1] + str(octave+4)
            else:
                raise ValueError()

        return Note(pitchName)

    def changeOctave(self, diff=0):
        return Note(self.name + str(self.octave+diff))

    def __repr__(self):
        return f"Note({(self.nameWithOctave if self.octave!=4 else self.name).replace('-','b')})"

    def __str__(self):
        return (self.nameWithOctave if self.octave!=4 else self.name).replace('-','b')

    def __eq__(self, other):
        return self.nameWithOctave == other.nameWithOctave