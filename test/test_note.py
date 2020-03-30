# -*- coding: utf-8 -*-
# @Author: Xi He
# @Date:   2020-03-22 15:00:52
# @Last Modified by:   Xi He
# @Last Modified time: 2020-03-30 00:00:45
import unittest
from guitarHarmony.note import Note
import music21 as m2

class TestNote(unittest.TestCase):
    def setUp(self):
        self.C = Note()
        self.A = Note('A')
        self.Fflat = Note('Fb')
        self.Gsharp2 = Note('G#2')
        self.Ebb5 = Note('Ebb5', 2.)
        self.Cbb = Note('Cbb')
        self.R = Note('R')

    def test_noteInit(self):
        self.assertRaises(ValueError, Note, 'Af')
        self.assertRaises(ValueError, Note, 'cb')
        self.assertRaises(ValueError, Note, 'Ab#')
        self.assertRaises(ValueError, Note, '-')
        self.assertRaises(ValueError, Note, 'CCb')
        self.assertRaises(ValueError, Note, 'C#####')
        self.assertRaises(ValueError, Note, 'A3#')

        self.assertRaises(ValueError, Note, 'A', 0.)
        self.assertRaises(ValueError, Note, 'C', '2.0')


    def test_noteAttrs(self):
        self.assertEqual(self.C.name, 'C')
        self.assertEqual(self.C.nameWithOctave, 'C4')
        self.assertEqual(self.C.tone, 'C')
        self.assertEqual(self.C.accidental, '')
        self.assertEqual(self.C.octave, 4)   

        self.assertEqual(self.A.name, 'A')
        self.assertEqual(self.A.nameWithOctave, 'A4')
        self.assertEqual(self.A.tone, 'A')
        self.assertEqual(self.A.accidental, '')
        self.assertEqual(self.A.octave, 4)   

        self.assertEqual(self.Fflat.name, 'Fb')
        self.assertEqual(self.Fflat.nameWithOctave, 'Fb4')
        self.assertEqual(self.Fflat.tone, 'F')
        self.assertEqual(self.Fflat.accidental, 'b')
        self.assertEqual(self.Fflat.octave, 4)  

        self.assertEqual(self.Gsharp2.name, 'G#')
        self.assertEqual(self.Gsharp2.nameWithOctave, 'G#2')
        self.assertEqual(self.Gsharp2.tone, 'G')
        self.assertEqual(self.Gsharp2.accidental, '#')
        self.assertEqual(self.Gsharp2.octave, 2)    

        self.assertEqual(self.Ebb5.name, 'Ebb')
        self.assertEqual(self.Ebb5.nameWithOctave, 'Ebb5')
        self.assertEqual(self.Ebb5.tone, 'E')
        self.assertEqual(self.Ebb5.accidental, 'bb')
        self.assertEqual(self.Ebb5.octave, 5)
        self.assertEqual(self.Ebb5.duration, 2.)

        self.assertEqual(self.Cbb.name, 'Cbb')
        self.assertEqual(self.Cbb.nameWithOctave, 'Cbb4')
        self.assertEqual(self.Cbb.tone, 'C')
        self.assertEqual(self.Cbb.accidental, 'bb')
        self.assertEqual(self.Cbb.octave, 4)

        self.assertEqual(self.R.name, 'R')
        self.assertEqual(self.R.nameWithOctave, 'Rest')
        self.assertEqual(self.R.tone, None)
        self.assertEqual(self.R.accidental, None)
        self.assertEqual(self.R.octave, None)

    def test_getSemiSteps(self):
        self.assertEqual(self.C.getSemiSteps(), 0)
        self.assertEqual(self.A.getSemiSteps(), 9)
        self.assertEqual(self.Fflat.getSemiSteps(), 4)
        self.assertEqual(self.Gsharp2.getSemiSteps(), -16)
        self.assertEqual(self.Ebb5.getSemiSteps(), 14)

        self.assertRaises(ValueError, self.R.getSemiSteps)

    def test_simplifyNote(self):
        self.assertEqual(self.C.simplify(), Note())
        self.assertEqual(self.A.simplify(), Note('A'))
        self.assertEqual(self.Fflat.simplify(), Note('E'))
        self.assertEqual(self.Gsharp2.simplify(), Note('G#2'))
        self.assertEqual(self.Ebb5.simplify(), Note('D5')) 
        self.assertEqual(self.Cbb.simplify(), Note('A#3')) 

        self.assertEqual(self.Gsharp2.simplify('b'), Note('Ab2'))
        self.assertEqual(self.Ebb5.simplify('b'), Note('D5')) 
        self.assertEqual(self.Cbb.simplify('b'), Note('Bb3'))

        self.assertRaises(ValueError, self.R.simplify)

    def test_applySemiSteps(self):
        self.assertEqual(Note.applySemiSteps(0), Note())
        self.assertEqual(Note.applySemiSteps(9), Note('A'))
        self.assertEqual(Note.applySemiSteps(4), Note('E'))
        self.assertEqual(Note.applySemiSteps(-16), Note('G#2'))
        self.assertEqual(Note.applySemiSteps(14), Note('D5'))

        self.assertEqual(Note.applySemiSteps(13,'b'), Note('Db5'))
        self.assertEqual(Note.applySemiSteps(-2,'b'), Note('Bb3'))

    def test_applyInterval(self):
        self.assertEqual(self.C.applyInterval('P1'), Note())
        self.assertEqual(self.A.applyInterval('P4'), Note('D5'))
        self.assertEqual(self.Fflat.applyInterval('M9'), 'Gb5')
        self.assertEqual(self.Gsharp2.applyInterval('A2'), 'A##2')
        self.assertEqual(self.Ebb5.applyInterval('P8'), Note('Ebb6'))

        self.assertRaises(ValueError, self.R.applyInterval, 'P1')

    def test_noteType(self):
        self.assertEqual(self.C.type(), 'Note')

    def test_transpose(self):
        self.assertEqual(self.C.transpose(4), Note('E'))
        self.assertEqual(self.C.transpose(-4), Note('G#3'))
        self.assertEqual(self.C.transpose(4, 'b'), Note('E'))
        self.assertEqual(self.C.transpose(-4, 'b'), Note('Ab3'))

        self.assertRaises(ValueError, self.R.transpose)

    def test_m2note(self):
        self.assertEqual(self.C.m2().nameWithOctave, m2.note.Note('C4').nameWithOctave)
        self.assertEqual(self.C.m2().quarterLength, m2.note.Note('C4').quarterLength)        

        self.assertEqual(self.Ebb5.m2().nameWithOctave, m2.note.Note('E--5').nameWithOctave)
        note = m2.note.Note('E--5')
        note.quarterLength=2.
        self.assertEqual(self.Ebb5.m2().quarterLength, note.quarterLength)        

        self.assertEqual(self.R.m2().quarterLength, 1.)

    def test_sortNotes(self):
        notes = [self.C, self.A, self.Fflat, self.Gsharp2, self.Ebb5, self.Cbb]
        self.assertEqual(Note.sortNotes(notes), ['G#2', 'Cbb', 'C', 'Fb', 'A', 'Ebb5'])

if __name__ == '__main__':
    unittest.main()
