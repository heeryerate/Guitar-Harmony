# -*- coding: utf-8 -*-
# @Author: Xi He
# @Date:   2020-03-22 15:00:52
# @Last Modified by:   Xi He
# @Last Modified time: 2020-04-01 15:01:40
import unittest
from guitarHarmony.exercise import Exercise
from guitarHarmony.chord import Chord
from guitarHarmony.scale import Scale


class TestExercise(unittest.TestCase):
    def setUp(self):
        self.exercise = Exercise()

    def test_exercise_init(self):
        """Test Exercise initialization."""
        self.assertEqual(self.exercise.exercise_type, 'chord_recognition')
        self.assertEqual(self.exercise.difficulty, 'beginner')
        self.assertEqual(self.exercise.exercises, [])

    def test_generate_chord_exercise(self):
        """Test chord exercise generation."""
        self.exercise.generate_chord_exercise(5)
        self.assertEqual(len(self.exercise.exercises), 5)
        
        for exercise in self.exercise.exercises:
            self.assertEqual(exercise['type'], 'chord_recognition')
            self.assertIn('question', exercise)
            self.assertIn('answer', exercise)
            self.assertIn('notes', exercise)
            self.assertIsInstance(exercise['answer'], Chord)
            self.assertIsInstance(exercise['notes'], list)

    def test_generate_scale_exercise(self):
        """Test scale exercise generation."""
        self.exercise.generate_scale_exercise(3)
        self.assertEqual(len(self.exercise.exercises), 3)
        
        for exercise in self.exercise.exercises:
            self.assertEqual(exercise['type'], 'scale_construction')
            self.assertIn('question', exercise)
            self.assertIn('answer', exercise)
            self.assertIn('notes', exercise)
            self.assertIsInstance(exercise['answer'], Scale)
            self.assertIsInstance(exercise['notes'], list)

    def test_get_exercises(self):
        """Test getting exercises."""
        self.exercise.generate_chord_exercise(2)
        exercises = self.exercise.get_exercises()
        self.assertEqual(len(exercises), 2)
        self.assertIsInstance(exercises, list)

    def test_clear_exercises(self):
        """Test clearing exercises."""
        self.exercise.generate_chord_exercise(3)
        self.assertEqual(len(self.exercise.exercises), 3)
        
        self.exercise.clear_exercises()
        self.assertEqual(len(self.exercise.exercises), 0)

    def test_exercise_content(self):
        """Test exercise content quality."""
        self.exercise.generate_chord_exercise(1)
        exercise = self.exercise.exercises[0]
        
        # Check question format
        self.assertIn('Identify the chord:', exercise['question'])
        
        # Check answer is valid chord
        chord = exercise['answer']
        self.assertIsInstance(chord, Chord)
        self.assertGreater(len(chord.chord_notes), 0)
        
        # Check notes list
        notes = exercise['notes']
        self.assertEqual(len(notes), len(chord.chord_notes))
        for note in notes:
            self.assertIsInstance(note, str)

    def test_scale_exercise_content(self):
        """Test scale exercise content quality."""
        self.exercise.generate_scale_exercise(1)
        exercise = self.exercise.exercises[0]
        
        # Check question format
        self.assertIn('Construct the', exercise['question'])
        self.assertIn('scale starting on', exercise['question'])
        
        # Check answer is valid scale
        scale = exercise['answer']
        self.assertIsInstance(scale, Scale)
        self.assertGreater(len(scale.scale_notes), 0)
        
        # Check notes list
        notes = exercise['notes']
        self.assertEqual(len(notes), len(scale.scale_notes))
        for note in notes:
            self.assertIsInstance(note, str)


if __name__ == '__main__':
    unittest.main() 