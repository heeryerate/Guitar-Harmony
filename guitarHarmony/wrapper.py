from basics.Note import Note
from basics.Scale import Scale
from basics.Interval import Interval
from basics.Chord import Chord
from basics.Progression import Progression

from itertools import product
import random

def getScale(root='C', scale_type='major'):
    return list(map(str, Scale(root, scale_type).notes))

def getChord(root='C', chord_type=''):
    return list(map(str, Chord(root, chord_type).notes))

def getInterval(root='C', interval='P1'):
    return [str(Note(root)+Interval(interval))]
    # return list(map(str, Interval(root, interval_type).notes))

def getProgression(root='C', progression_type='major_triads'):
    return list(map(str, Progression(root, progression_type).chords))

sharp_circle_roots=['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#']
flat_circle_roots=['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb']
modes = ['minor', 'major']


if __name__ == '__main__':

    print(Chord().all_chords())

    # TODO: generate scale, chord, interval, progression


    # print(getInterval('Db', 'A5'))
    # print(getChord('E', '7'))
    # print(getScale('F#', 'mixolydian'))
    # print(getProgression('Ab', 'major_sevenths'))

    # random.seed(123)

    # exs_1 = [getProgression(i, y) for i, y in product(flat_circle_roots, Progression().all_progressions())]
    # exs_1 = [(i, y) for i, y in product(flat_circle_roots, Progression().all_progressions())]
    # random.shuffle(exs_1)
    # for item in exs_1:
    #     print(item)
    #     input("Press Enter to continue...")





