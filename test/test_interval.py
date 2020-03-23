# -*- coding: utf-8 -*-
# @Author: Xi He
# @Date:   2020-03-22 15:00:52
# @Last Modified by:   Xi He
# @Last Modified time: 2020-03-22 22:14:47
import unittest
from guitarHarmony.note import Note
from guitarHarmony.interval import Interval
import music21 as m2

class TestInterval(unittest.TestCase):
    def setUp(self):
        self.C = Note()
        self.Gsharp = Note('G#')
        self.P1 = Interval('P1')
        self.A4 = Interval('A4')
        self.m7 = Interval('m7')
        self.A12 = Interval('A12')
        self.M9 = Interval('M9')

    def test_IntervalInit(self):
        self.assertRaises(ValueError, Interval, 'P2')
        self.assertRaises(ValueError, Interval, 'c4')
        self.assertRaises(ValueError, Interval, 'M12')

    def test_getInverval(self):
        self.assertEqual(Interval.getInterval('C', 'D'), 'M2')
        self.assertEqual(Interval.getInterval('D', 'G#'), 'A4')
        self.assertEqual(Interval.getInterval('E', 'B#5'), 'A12')

        self.assertEqual(Interval.getInterval('D', 'G#'), self.A4)
        self.assertEqual(Interval.getInterval('C', 'D5'), self.M9)
        self.assertEqual(Interval.getInterval('E', 'B#5'), self.A12)

    def test_applyToNote(self):
        self.assertEqual(self.A4.applyToNote(self.C), 'F#')
        self.assertEqual(self.A4.applyToNote('A'), 'D#5')
        self.assertEqual(self.M9.applyToNote('B'), 'C#6')
        self.assertEqual(self.M9.applyToNote('G##2'), Note('A##3'))

    def test_intervalType(self):
        self.assertEqual(self.A4.type(), 'Interval')

if __name__ == '__main__':
    unittest.main()
