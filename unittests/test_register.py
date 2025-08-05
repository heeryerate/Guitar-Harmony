# -*- coding: utf-8 -*-
# @Author: Xi He
# @Date:   2020-03-22 15:00:52
# @Last Modified by:   Xi He
# @Last Modified time: 2020-04-01 15:01:40
import unittest
from guitarHarmony.register import Register
from guitarHarmony.note import Note
from guitarHarmony.chord import Chord
from guitarHarmony.scale import Scale
from guitarHarmony.interval import Interval


class TestRegister(unittest.TestCase):
    def setUp(self):
        self.register = Register()
        self.test_note = Note('C')
        self.test_chord = Chord('C', 'maj7')
        self.test_scale = Scale('C', 'major')
        self.test_interval = Interval('P5')

    def test_register_init(self):
        """Test Register initialization."""
        self.assertEqual(self.register.notes, {})
        self.assertEqual(self.register.chords, {})
        self.assertEqual(self.register.scales, {})
        self.assertEqual(self.register.intervals, {})

    def test_register_note(self):
        """Test registering a note."""
        self.register.register_note('C', self.test_note)
        self.assertIn('C', self.register.notes)
        self.assertEqual(self.register.notes['C'], self.test_note)

    def test_register_chord(self):
        """Test registering a chord."""
        self.register.register_chord('Cmaj7', self.test_chord)
        self.assertIn('Cmaj7', self.register.chords)
        self.assertEqual(self.register.chords['Cmaj7'], self.test_chord)

    def test_register_scale(self):
        """Test registering a scale."""
        self.register.register_scale('C_major', self.test_scale)
        self.assertIn('C_major', self.register.scales)
        self.assertEqual(self.register.scales['C_major'], self.test_scale)

    def test_register_interval(self):
        """Test registering an interval."""
        self.register.register_interval('P5', self.test_interval)
        self.assertIn('P5', self.register.intervals)
        self.assertEqual(self.register.intervals['P5'], self.test_interval)

    def test_get_note(self):
        """Test getting a registered note."""
        self.register.register_note('C', self.test_note)
        retrieved_note = self.register.get_note('C')
        self.assertEqual(retrieved_note, self.test_note)
        
        # Test getting non-existent note
        self.assertIsNone(self.register.get_note('D'))

    def test_get_chord(self):
        """Test getting a registered chord."""
        self.register.register_chord('Cmaj7', self.test_chord)
        retrieved_chord = self.register.get_chord('Cmaj7')
        self.assertEqual(retrieved_chord, self.test_chord)
        
        # Test getting non-existent chord
        self.assertIsNone(self.register.get_chord('Dm'))

    def test_get_scale(self):
        """Test getting a registered scale."""
        self.register.register_scale('C_major', self.test_scale)
        retrieved_scale = self.register.get_scale('C_major')
        self.assertEqual(retrieved_scale, self.test_scale)
        
        # Test getting non-existent scale
        self.assertIsNone(self.register.get_scale('D_minor'))

    def test_get_interval(self):
        """Test getting a registered interval."""
        self.register.register_interval('P5', self.test_interval)
        retrieved_interval = self.register.get_interval('P5')
        self.assertEqual(retrieved_interval, self.test_interval)
        
        # Test getting non-existent interval
        self.assertIsNone(self.register.get_interval('M3'))

    def test_list_notes(self):
        """Test listing registered notes."""
        self.assertEqual(self.register.list_notes(), [])
        
        self.register.register_note('C', self.test_note)
        self.register.register_note('D', Note('D'))
        
        notes = self.register.list_notes()
        self.assertIn('C', notes)
        self.assertIn('D', notes)
        self.assertEqual(len(notes), 2)

    def test_list_chords(self):
        """Test listing registered chords."""
        self.assertEqual(self.register.list_chords(), [])
        
        self.register.register_chord('Cmaj7', self.test_chord)
        self.register.register_chord('Dm', Chord('D', 'm'))
        
        chords = self.register.list_chords()
        self.assertIn('Cmaj7', chords)
        self.assertIn('Dm', chords)
        self.assertEqual(len(chords), 2)

    def test_list_scales(self):
        """Test listing registered scales."""
        self.assertEqual(self.register.list_scales(), [])
        
        self.register.register_scale('C_major', self.test_scale)
        self.register.register_scale('D_minor', Scale('D', 'natural_minor'))
        
        scales = self.register.list_scales()
        self.assertIn('C_major', scales)
        self.assertIn('D_minor', scales)
        self.assertEqual(len(scales), 2)

    def test_list_intervals(self):
        """Test listing registered intervals."""
        self.assertEqual(self.register.list_intervals(), [])
        
        self.register.register_interval('P5', self.test_interval)
        self.register.register_interval('M3', Interval('M3'))
        
        intervals = self.register.list_intervals()
        self.assertIn('P5', intervals)
        self.assertIn('M3', intervals)
        self.assertEqual(len(intervals), 2)

    def test_clear(self):
        """Test clearing all registrations."""
        # Register some items
        self.register.register_note('C', self.test_note)
        self.register.register_chord('Cmaj7', self.test_chord)
        self.register.register_scale('C_major', self.test_scale)
        self.register.register_interval('P5', self.test_interval)
        
        # Verify they exist
        self.assertGreater(len(self.register.notes), 0)
        self.assertGreater(len(self.register.chords), 0)
        self.assertGreater(len(self.register.scales), 0)
        self.assertGreater(len(self.register.intervals), 0)
        
        # Clear all
        self.register.clear()
        
        # Verify they're gone
        self.assertEqual(len(self.register.notes), 0)
        self.assertEqual(len(self.register.chords), 0)
        self.assertEqual(len(self.register.scales), 0)
        self.assertEqual(len(self.register.intervals), 0)


if __name__ == '__main__':
    unittest.main() 