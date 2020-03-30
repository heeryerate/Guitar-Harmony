# -*- coding: utf-8 -*-
# @Author: Xi He
# @Date:   2020-03-22 15:00:52
# @Last Modified by:   Xi He
# @Last Modified time: 2020-03-28 17:37:17
import unittest
from guitarHarmony.note import Note
from guitarHarmony.interval import Interval
from guitarHarmony.chord import Chord
import music21 as m2

class TestChord(unittest.TestCase):
    def setUp(self):
        self.C = Chord()
        self.Am = Chord('A','m')
        self.Bb7b5 = Chord('Bb','7b5')
        self.Gminv1 = Chord('Bb','7b5', inversion=1)
        self.user1 = Chord('F#', 'user', chord_recipe=['P1', 'P5', 'M9'])
        self.user2 = Chord('Gb3', 'user', chord_notes=['Gb3', 'Bb3', 'Db4'])

    def testChordInit(self):
        self.assertRaises(ValueError, Chord, 'C', 'm4')
        self.assertRaises(ValueError, Chord, 'F', 'm', ['P1', 'm3', 'A5'])
        self.assertRaises(ValueError, Chord, 'B2', 'user', [], [])
        self.assertRaises(ValueError, Chord, 'G', 'user', ['P1', 'm3'], ['G', 'B'])
        self.assertRaises(ValueError, Chord, 'D', 'user', ['P1', 'm3'], ['D', 'F', 'A'])
        self.assertRaises(ValueError, Chord, 'A', 'user', chord_notes=['A', 'F'], inversion=3)
        self.assertRaises(ValueError, Chord, 'Gb', 'user', chord_notes=['Gb', 'F'])
        self.assertRaises(ValueError, Chord, 'A', 'user', chord_notes=['D', 'F'])


    # def test_getInverval(self):
    #     self.assertEqual(Interval.getInterval('C', 'D'), 'M2')
    #     self.assertEqual(Interval.getInterval('D', 'G#'), 'A4')
    #     self.assertEqual(Interval.getInterval('E', 'B#5'), 'A12')

    #     self.assertEqual(Interval.getInterval('D', 'G#'), self.A4)
    #     self.assertEqual(Interval.getInterval('C', 'D5'), self.M9)
    #     self.assertEqual(Interval.getInterval('E', 'B#5'), self.A12)

    # def test_applyToNote(self):
    #     self.assertEqual(self.A4.applyToNote(self.C), 'F#')
    #     self.assertEqual(self.A4.applyToNote('A'), 'D#5')
    #     self.assertEqual(self.M9.applyToNote('B'), 'C#6')
    #     self.assertEqual(self.M9.applyToNote('G##2'), Note('A##3'))

    # def test_intervalType(self):
    #     self.assertEqual(self.A4.type(), 'Interval')

if __name__ == '__main__':
    unittest.main()
