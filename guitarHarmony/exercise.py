from .note import Note
from .chord import Chord
from .scale import Scale
from .progression import Progression
import random

class Exercise:
    """
    Exercise class for generating music theory exercises.
    """
    
    def __init__(self, exercise_type='chord_recognition', difficulty='beginner'):
        self.exercise_type = exercise_type
        self.difficulty = difficulty
        self.exercises = []
        
    def generate_chord_exercise(self, num_exercises=10):
        """Generate chord recognition exercises."""
        chord_types = ['', 'm', '7', 'm7', 'maj7', 'dim', 'aug']
        roots = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        
        for _ in range(num_exercises):
            root = random.choice(roots)
            chord_type = random.choice(chord_types)
            chord = Chord(root, chord_type)
            self.exercises.append({
                'type': 'chord_recognition',
                'question': f'Identify the chord: {root}{chord_type}',
                'answer': chord,
                'notes': [note.name for note in chord.chord_notes]
            })
            
    def generate_scale_exercise(self, num_exercises=10):
        """Generate scale construction exercises."""
        scale_types = ['major', 'natural_minor', 'harmonic_minor', 'melodic_minor']
        roots = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        
        for _ in range(num_exercises):
            root = random.choice(roots)
            scale_type = random.choice(scale_types)
            scale = Scale(root, scale_type)
            self.exercises.append({
                'type': 'scale_construction',
                'question': f'Construct the {scale_type} scale starting on {root}',
                'answer': scale,
                'notes': [note.name for note in scale.scale_notes]
            })
            
    def get_exercises(self):
        """Return all generated exercises."""
        return self.exercises
        
    def clear_exercises(self):
        """Clear all exercises."""
        self.exercises = []
