

from .note import Note
from .interval import Interval
from .chord import Chord
from .helper import CONSTANT

class Scale(object):
    def __init__(self, root='C', scale_type = '', scale_recipe=[], scale_notes=[], durations=[]):
        if isinstance(root, str): root = Note(root)
        self.root, self.scale_type, self.scale_recipe, self.scale_notes = self._check(root, scale_type, scale_recipe, scale_notes)
        self.durations=durations

    def _check(self, root, scale_type, scale_recipe, scale_notes):
        """Validate and build scale components."""
        if scale_type not in CONSTANT.scale_recipes().keys():
            raise ValueError(f'Invalid scale type {scale_type}! Current valid types: {list(CONSTANT.scale_recipes().keys())}')
            
        if scale_type != 'user':
            scale_recipe_ref = CONSTANT.scale_recipes()[scale_type]
            scale_notes_ref = self.buildScale(root, scale_recipe_ref)
            if scale_notes != [] and scale_notes != scale_notes_ref:
                raise ValueError(f'{scale_type} does not match scale_notes {scale_notes}')
            if scale_recipe != [] and scale_recipe_ref != scale_recipe:
                raise ValueError(f'{scale_type} does not match scale_recipe {scale_recipe}')
            scale_recipe, scale_notes = scale_recipe_ref, scale_notes_ref
        else:
            if scale_recipe == [] and scale_notes == []:
                raise ValueError(f'User scale type not specified!')
            elif scale_recipe == [] and len(scale_notes) >= 2:
                scale_recipe = self.buildRecipe(scale_notes)
            elif scale_notes == [] and len(scale_recipe) >= 2:
                scale_notes = self.buildScale(root, scale_recipe)
            elif len(scale_notes) >= 2 and len(scale_recipe) >= 2:
                scale_notes_ref = self.buildScale(root, scale_recipe)
                if scale_notes_ref != scale_notes:
                    raise ValueError(f'{scale_recipe} and {scale_notes} do not match')
            else:
                raise ValueError(f'{scale_recipe} and {scale_notes} do not match or cannot construct scale')
        
        if root != scale_notes[0]:
            raise ValueError(f'root {root} and scale_notes {scale_notes} do not match.')
            
        scale_recipe = [Interval(interval) if isinstance(interval, str) else interval for interval in scale_recipe]
        scale_notes = [Note(note) if isinstance(note, str) else note for note in scale_notes]
        
        return root, scale_type, scale_recipe, scale_notes

    def matchScale(self, target_notes):
        """Match a sequence of notes to a scale."""
        if isinstance(target_notes[0], str):
            target_notes = [Note(note) for note in target_notes]
        
        for scale_type in CONSTANT.scale_recipes().keys():
            if scale_type == 'user':
                continue
            test_scale = Scale(self.root, scale_type)
            if all(note in test_scale.scale_notes for note in target_notes):
                return scale_type
        return None

    def associateChord(self):
        """Return chords that can be built from this scale."""
        chords = []
        for i, note in enumerate(self.scale_notes):
            # Build triads on each scale degree
            if i + 2 < len(self.scale_notes):
                chord_notes = [note, self.scale_notes[i+2], self.scale_notes[(i+4) % len(self.scale_notes)]]
                chord = Chord(note, 'user', chord_notes=chord_notes)
                chords.append(chord)
        return chords

    @staticmethod
    def pharseScale(text='C.major'):
        if '.' in text:
            root, scale_type = text.split('.')
            return Scale(root=root, scale_type=scale_type)
        else:
            return Scale(root=root, scale_type='natural major')

    @staticmethod
    def displayAllScalesRecipe():
        return list(CONSTANT.scale_recipes().keys())

    @staticmethod
    def buildScale(root, scale_recipe):
        return [Interval.applyInterval(root, interval) for interval in scale_recipe]

    @staticmethod
    def buildRecipe(scale_notes):
        return [Interval.getInterval(base=scale_notes[0], target=note) for note in scale_notes]

    def m2(self):
        m2scale = [m2.note.Note(note.nameWithOctave.replace('b', '-')) for note in self.scale_notes]
        if isinstance(self.durations, float):
            for note in m2scale:
                note.quarterLength = self.durations
        elif isinstance(self.durations, list) and len(self.durations) == len(self.scale_notes):
            for idx, note in enumerate(m2scale):
                note.quarterLength = self.durations[idx]
        else:
            raise ValueError(f"music21 scale failed to convert")

        return m2scale

    def __repr__(self):
        return f"Scale(Root({self.root.name}), {self.scale_type})"

    def __str__(self):
        return f"{self.root.name}{self.scale_type}"

    def __eq__(self, other):
        if len(self.scale_notes) != len(other.scale_notes):
            return False
        else:
            return all(self.scale_notes[i] == other.scale_notes[i] for i in range(len(self.scale_notes)))