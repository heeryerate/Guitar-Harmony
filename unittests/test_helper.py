# -*- coding: utf-8 -*-
# @Author: Xi He
# @Date:   2020-03-22 15:00:52
# @Last Modified by:   Xi He
# @Last Modified time: 2020-04-01 15:01:40
import unittest
from guitarHarmony.helper import CONSTANT, reverseDict, warning, suf, flatten, cyclelist


class TestHelper(unittest.TestCase):
    def setUp(self):
        pass

    def test_reverseDict(self):
        """Test reverseDict function."""
        test_dict = {'a': 1, 'b': 2, 'c': 1}
        result = reverseDict(test_dict)
        expected = {1: ['a', 'c'], 2: ['b']}
        self.assertEqual(result, expected)

    def test_tone_to_semisteps(self):
        """Test tone_to_semisteps mapping."""
        mapping = CONSTANT.tone_to_semisteps()
        self.assertEqual(mapping['C'], 0)
        self.assertEqual(mapping['C#'], 1)
        self.assertEqual(mapping['Db'], 1)
        self.assertEqual(mapping['B'], 11)

    def test_semisteps_to_tone(self):
        """Test semisteps_to_tone mapping."""
        mapping = CONSTANT.semisteps_to_tone()
        self.assertIn('C', mapping[0])
        self.assertIn('C#', mapping[1])
        self.assertIn('Db', mapping[1])

    def test_tone_to_steps(self):
        """Test tone_to_steps mapping."""
        mapping = CONSTANT.tone_to_steps()
        self.assertEqual(mapping['C'], 1)
        self.assertEqual(mapping['D'], 2)
        self.assertEqual(mapping['E'], 3)
        self.assertEqual(mapping['F'], 4)
        self.assertEqual(mapping['G'], 5)
        self.assertEqual(mapping['A'], 6)
        self.assertEqual(mapping['B'], 7)

    def test_steps_to_tone(self):
        """Test steps_to_tone mapping."""
        mapping = CONSTANT.steps_to_tone()
        self.assertIn('C', mapping[1])
        self.assertIn('D', mapping[2])
        self.assertIn('E', mapping[3])

    def test_accidental_to_step(self):
        """Test accidental_to_step mapping."""
        mapping = CONSTANT.accidental_to_step()
        self.assertEqual(mapping['b'], -1)
        self.assertEqual(mapping['#'], 1)

    def test_interval_to_semisteps(self):
        """Test interval_to_semisteps mapping."""
        mapping = CONSTANT.interval_to_semisteps()
        self.assertEqual(mapping['P1'], 0)
        self.assertEqual(mapping['M2'], 2)
        self.assertEqual(mapping['P5'], 7)
        self.assertEqual(mapping['P8'], 12)

    def test_semisteps_to_interval(self):
        """Test semisteps_to_interval mapping."""
        mapping = CONSTANT.semisteps_to_interval()
        self.assertIn('P1', mapping[0])
        self.assertIn('M2', mapping[2])
        self.assertIn('P5', mapping[7])

    def test_interval_name_mapping(self):
        """Test interval_name_mapping."""
        mapping = CONSTANT.interval_name_mapping()
        self.assertEqual(mapping['P'], 'Perfect')
        self.assertEqual(mapping['d'], 'Diminished')
        self.assertEqual(mapping['m'], 'Minor')
        self.assertEqual(mapping['M'], 'Major')
        self.assertEqual(mapping['A'], 'Augmented')

    def test_chord_recipes(self):
        """Test chord_recipes."""
        recipes = CONSTANT.chord_recipes()
        self.assertIn('', recipes)  # Major triad
        self.assertIn('m', recipes)  # Minor triad
        self.assertIn('7', recipes)  # Dominant 7th
        self.assertIn('maj7', recipes)  # Major 7th
        self.assertIn('user', recipes)  # User-defined

    def test_scale_recipes(self):
        """Test scale_recipes."""
        recipes = CONSTANT.scale_recipes()
        self.assertIn('major', recipes)
        self.assertIn('natural_minor', recipes)
        self.assertIn('harmonic_minor', recipes)
        self.assertIn('melodic_minor', recipes)
        self.assertIn('dorian', recipes)
        self.assertIn('user', recipes)

    def test_alter_recipes(self):
        """Test alter_recipes."""
        recipes = CONSTANT.alter_recipes()
        self.assertIn('power5', recipes)
        self.assertIn('add2', recipes)

    def test_arpeggio_note_units(self):
        """Test arpeggio_note_units."""
        units = CONSTANT.arpeggio_note_units()
        self.assertIn(1/8, units)
        self.assertIn(1/4, units)
        self.assertIn(1/3, units)
        self.assertIn(1/6, units)

    def test_arpeggio_kinds(self):
        """Test argeggio_kinds."""
        kinds = CONSTANT.argeggio_kinds()
        self.assertIn('up', kinds)
        self.assertIn('down', kinds)
        self.assertIn('Up', kinds)
        self.assertIn('Down', kinds)
        self.assertIn('valley', kinds)
        self.assertIn('hill', kinds)

    def test_suf(self):
        """Test suf function."""
        self.assertEqual(suf(1), '1st')
        self.assertEqual(suf(2), '2nd')
        self.assertEqual(suf(3), '3rd')
        self.assertEqual(suf(4), '4th')
        self.assertEqual(suf(21), '21st')
        self.assertEqual(suf(22), '22nd')
        self.assertEqual(suf(23), '23rd')
        self.assertEqual(suf(24), '24th')

    def test_flatten(self):
        """Test flatten function."""
        # Test with nested lists
        nested = [[1, 2], [3, 4], [5, 6]]
        self.assertEqual(flatten(nested), [1, 2, 3, 4, 5, 6])
        
        # Test with mixed types
        mixed = [[1, 'a'], [2, 'b']]
        self.assertEqual(flatten(mixed), [1, 'a', 2, 'b'])
        
        # Test with single item
        single = [1]
        self.assertEqual(flatten(single), [1])

    def test_cyclelist(self):
        """Test cyclelist function."""
        test_list = [1, 2, 3]
        result = cyclelist(test_list)
        expected = [[1, 2, 3], [2, 3, 1], [3, 1, 2]]
        self.assertEqual(result, expected)
        
        # Test with single item
        single = [1]
        result = cyclelist(single)
        self.assertEqual(result, [[1]])
        
        # Test with empty list
        empty = []
        result = cyclelist(empty)
        self.assertEqual(result, [])

    def test_cyclelist_invalid_input(self):
        """Test cyclelist with invalid input."""
        with self.assertRaises(ValueError):
            cyclelist("not a list")


if __name__ == '__main__':
    unittest.main() 