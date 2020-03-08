
import unittest
from basics.Note import Note
from basics.Scale import Scale
from basics.Interval import Interval
from basics.Chord import Chord
from basics.Progression import Progression


class TestsForJesus(unittest.TestCase):
    def test_note_parsing(self):
        self.assertEqual(str(Note('A4')), 'A')
        self.assertEqual(str(Note('Ab6')), 'Ab')
        self.assertEqual(str(Note('Dbb')), 'Dbb')
        self.assertEqual(str(Note('G###0')), 'G###')

        self.assertRaises(Exception, Note, 'A99')
        self.assertRaises(Exception, Note, 'Ab#')
        self.assertRaises(Exception, Note, 'E####')

    def test_interval_parsing(self):
        self.assertEqual(Interval('d5').semitone, 6)
        self.assertRaises(Exception, Interval, 'P3')

    def test_note_sum(self):
        self.assertEqual(str(Note('A4')+Interval('d5')), str(Note('Eb')))
        self.assertEqual(str(Note('A')+Interval('P1')), str(Note('A')))
        self.assertEqual(str(Note('G##')+Interval('m3')), str(Note('B#')))
        self.assertEqual(str(Note('F')+Interval('P5')), str(Note('C')))

    def test_note_scales(self):
        self.assertEqual(list(map(str, Scale('C', 'major').notes)),          ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C'])
        self.assertEqual(list(map(str, Scale('C', 'natural_minor').notes)),  ['C', 'D', 'Eb','F', 'G', 'Ab','Bb','C'])
        self.assertEqual(list(map(str, Scale('C', 'harmonic_minor').notes)), ['C', 'D', 'Eb','F', 'G', 'Ab','B', 'C'])
        self.assertEqual(list(map(str, Scale('C', 'melodic_minor').notes)),  ['C', 'D', 'Eb','F', 'G', 'A', 'B', 'C'])
        self.assertEqual(list(map(str, Scale('C', 'dorian').notes)),         ['C', 'D', 'Eb','F', 'G', 'A', 'Bb','C'])
        self.assertEqual(list(map(str, Scale('C', 'locrian').notes)),        ['C', 'Db','Eb','F', 'Gb','Ab','Bb','C'])
        self.assertEqual(list(map(str, Scale('C', 'lydian').notes)),         ['C', 'D', 'E', 'F#','G', 'A', 'B', 'C'])
        self.assertEqual(list(map(str, Scale('C', 'mixolydian').notes)),     ['C', 'D', 'E', 'F', 'G', 'A', 'Bb','C'])
        self.assertEqual(list(map(str, Scale('C', 'phrygian').notes)),       ['C', 'Db','Eb','F', 'G', 'Ab','Bb','C'])
        self.assertEqual(list(map(str, Scale('C','major_pentatonic').notes)),['C', 'D', 'E', 'G', 'A', 'C'])
        self.assertEqual(list(map(str, Scale('C','minor_pentatonic').notes)),['C', 'Eb','F', 'G', 'Bb','C'])
        self.assertRaises(Exception, Scale, 'C', 'non-existent scale')

class TestsForJesusChords(unittest.TestCase):
    def setUp(self):
        '''put here for later building of test chords, one for each
        chord_type in chord_recipes'''
        self.chord_types = [k for k in Chord('Bb').chord_recipes.keys()]
        self.chords = {k:Chord('A', k) for k in self.chord_types}
        self.rootNote = Note('A')

    def tearDown(self):
        self.chords = {}
        self.chord_types = []
        self.rootNote = None

    def test_chord_creation(self):
        #check __str__ returns
        self.assertEqual(list(map(str, Chord('A').notes)), ['A', 'C#', 'E'])
        self.assertEqual(list(map(str, Chord('B','dim').notes)), ['B', 'D', 'F'])
        self.assertEqual(list(map(str, Chord('C','aug').notes)), ['C', 'E', 'G#'])
        self.assertEqual(list(map(str, Chord('D','maj7').notes)), ['D', 'F#', 'A', 'C#'])
        self.assertEqual(list(map(str, Chord('A#','sus4').notes)), ['A#', 'D#', 'E#'])
        self.assertEqual(list(map(str, Chord('Ab','m').notes)), ['Ab', 'Cb', 'Eb'])
        self.assertEqual(list(map(str, Chord('G','add2').notes)), ['G', 'A', 'B', 'D'])

        #check __repr__ returns
        #//todo

        #check __eq__
        #//todo

        #check faulty inputs
        self.assertRaises(Exception, Chord, 'A$')
        self.assertRaises(Exception, Chord, 'H')

        #check recipe notes
        self.assertEqual(self.chords[''].notes,
                         [self.rootNote,
                          self.rootNote+Interval('M3'),
                          self.rootNote+Interval('P5')
                          ])
        self.assertEqual(self.chords['m'].notes,
                         [self.rootNote,
                          self.rootNote+Interval('m3'),
                          self.rootNote+Interval('P5')
                          ])
        self.assertEqual(self.chords['dim'].notes,
                         [self.rootNote,
                          self.rootNote+Interval('m3'),
                          self.rootNote+Interval('d5')
                          ])
        self.assertEqual(self.chords['aug'].notes,
                         [self.rootNote,
                          self.rootNote+Interval('M3'),
                          self.rootNote+Interval('A5')
                          ])

unittest.main()