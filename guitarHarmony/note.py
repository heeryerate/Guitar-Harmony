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

    def __init__(self, note=None):
        self.__note = m2.note.Note(pitchName = note if note is None else note.replace('b', '-'), keywords={})
        self._updateAttrs()

    def _updateAttrs(self):
        self.name = self.__note.name
        self.pitch = self.__note.pitch
        self.octave = self.__note.octave if self.__note.octave is not None else 4
        self.duration = self.__note.duration
        self.nameWithOctave = self.__note.nameWithOctave
        self.lyric = self.__note.lyric
        self.tone = self.__note.step

    def show(self, show_type = ''):
        if show_type == 'midi':
            s = m2.stream.Stream()
            s.append(m2.note.Rest())
            s.append(self.__note)
            s.show('midi')
        elif show_type == 'text':
            self.__note.show('text')
        elif show_type == 'notation':
            self._addNotation()
            self.__note.show()
            self._removeNotation()
        elif show_type == '':
            self.__note.show()
        else:
            raise NotImplementedError()

    def transpose(self, step=0):
        return Note(self.__note.transpose(step).nameWithOctave)

    def semiSteps(self):
        octave_steps = 12 * (self.octave - 4)
        tone_steps = self.tone_to_step[self.__note.step]
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

    def _removeNotation(self):
        self.__note.lyric = ''
        self._updateAttrs()

    def _addNotation(self):
        self._removeNotation()
        self.__note.insertLyric(self.name)
        self._updateAttrs()

    def __repr__(self):
        return f"Note({self.nameWithOctave})"

    def __str__(self):
        return self.nameWithOctave

    def __eq__(self, other):
        return self.nameWithOctave == other.nameWithOctave