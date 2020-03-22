# -*- coding: utf-8 -*-
# @Author: Xi He
# @Date:   2020-03-21 18:11:20
# @Last Modified by:   Xi He
# @Last Modified time: 2020-03-21 23:01:19

import music21 as m2
from .note import Note
from .chord import Chord

class Stream(object):
    def __init__(self, elements=[]):
        assert len(elements) > 0, 'Empty elements!'
        self.elements = elements
        self.m2elements = self.convertToM2Elements(self.elements)
        self.stream = self.buildStream(self.m2elements)

    def convertToM2Elements(self, elements):
        m2elements = []
        for el in elements:
            if hasattr(el, "instanceCheck"):
                if el.instanceCheck() == 'Note':
                    m2elements.append(el.m2note)
                if el.instanceCheck() == 'Chord':
                    chord = m2.chord.Chord([note.nameWithOctave for note in el.notes])
                    m2elements.append(chord)
            else:
                if isinstance(el, m2.chord.Chord):
                    m2elements.append(el)
                if isinstance(el, m2.note.Note):
                    m2elements.append(el)
        return m2elements

    def buildStream(self, m2elements):
        stream = m2.stream.Stream()
        [stream.append(el) for el in m2elements]
        return stream

    def show(self, show_type=''):
        if show_type == 'midi': 
            stream = m2.stream.Stream([m2.note.Rest()])
            [stream.append(el) for el in self.m2elements]
            stream.show('midi')
        elif show_type == 'text':
            for el in self.elements:
                if hasattr(el, "instanceCheck"):
                    if el.instanceCheck() == 'Note':
                        print(el.__repr__())
                    if el.instanceCheck() == 'Chord':
                        print(f"{el.root.name}{el.chord_type} on bass {el.bass.name}")
        elif show_type == 'notation':
            print(self.elements)
            for idx, el in enumerate(self.elements):
                self.stream[idx].lyric = el.__str__()
            self.stream.show()
            for idx, el in enumerate(self.elements):
                self.stream[idx].lyric = ''
        elif show_type == '':
            self.stream.show()
        else:
            raise NotImplementedError()