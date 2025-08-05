# GuitarHarmony

A Python library for music theory, harmony, and guitar learning.

## Features

- **Music Theory**: Notes, intervals, chords, scales, and progressions
- **Music Generation**: Create MIDI files and musical streams
- **Rhythm**: Generate and manipulate rhythmic patterns
- **Exercises**: Generate music theory exercises
- **Analysis**: Analyze musical structures and relationships

## Installation

### From Source
```bash
git clone https://github.com/heeryerate/Guitar-Harmony.git
cd Guitar-Harmony
pip install -e .
```

### Dependencies
```bash
pip install -r requirements.txt
```

## Quick Start

```python
import guitarHarmony as gt

# Create a note
note = gt.Note('C')
print(note)  # C

# Create a chord
chord = gt.Chord('C', 'maj7')
print([note.name for note in chord.chord_notes])  # ['C', 'E', 'G', 'B']

# Create a scale
scale = gt.Scale('C', 'major')
print([note.name for note in scale.scale_notes])  # ['C', 'D', 'E', 'F', 'G', 'A', 'B']

# Generate exercises
exercise = gt.Exercise()
exercise.generate_chord_exercise(5)

## Command Line Interface

GuitarHarmony also provides a command-line interface:

```bash
# Create a note
guitar-harmony note C --show

# Create a chord
guitar-harmony chord C maj7 --show midi

# Create a scale
guitar-harmony scale C major --show notation

# Create an interval
guitar-harmony interval P5 --show --base C

# Generate exercises
guitar-harmony exercise chord_recognition --count 5

# List available options
guitar-harmony list chords
guitar-harmony list scales
guitar-harmony list intervals
```

## Documentation

[**Read docs here**](http://guitar-harmony.readthedocs.io/en/latest/)

## License

MIT License - see LICENSE.txt for details.

