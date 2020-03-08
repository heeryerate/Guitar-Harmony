import re
import music21 as m2
from .interval import Interval

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
    __all__ = ['show', 'transpose']

    def __init__(self, note=None):
        self.__note = m2.note.Note(pitchName = note if note is None else note.replace('b', '-'), keywords={})
        self._updateAttrs()

    def _updateAttrs(self):
        self.name = self.__note.name
        self.pitch = self.__note.pitch
        self.octave = self.__note.octave
        self.duration = self.__note.duration
        self.nameWithOctave = self.__note.nameWithOctave
        self.lyric = self.__note.lyric

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
        return self.name

    def __eq__(self, other):
        return self.nameWithOctave == other.nameWithOctave