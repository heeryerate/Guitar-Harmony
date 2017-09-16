from basics.Note import Note
from basics.Scale import Scale
from basics.Interval import Interval
from basics.Chord import Chord
from basics.Progression import Progression

from itertools import product
import random

def generate_scale(root='C', scale_type='major'):
    return list(map(str, Scale(root, scale_type).notes))

def generate_chord(root='C', chord_type=''):
    return list(map(str, Chord(root, chord_type).notes))

def generate_interval(root='C', interval='P1'):
    return [str(Note(root)+Interval(interval))]

def generate_progression(root='C', progression_type='major_triads'):
    return list(map(str, Progression(root, progression_type).chords))

sharp_circle_roots=['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#']
flat_circle_roots=['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb']
modes = ['minor', 'major']


if __name__ == '__main__':

    print(generate_interval('Db', 'A5'))
    print(generate_chord('E', '7'))
    print(generate_scale('F#', 'mixolydian'))
    print(generate_progression('Ab', 'major_sevenths'))

    # random.seed(123)

    # exs_1 = [generate_progression(i, y) for i, y in product(flat_circle_roots, Progression().all_progressions())]
    # random.shuffle(exs_1)
    # for item in exs_1:
    #     print(item)
        # raw_input("Press Enter to continue...")





