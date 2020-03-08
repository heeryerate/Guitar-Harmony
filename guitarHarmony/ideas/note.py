import re
from .interval import Interval

class Note():
    """
    The note class.

    The notes are to be parsed in the following way:
    * the letter name,
    * accidentals (up to 3),
    * octave (default is 4).

    For example, 'Ab', 'G9', 'B##7' are all valid notes. '#', 'A9b',
    'Dbbbb' are not.
    """
    def __init__(self, note, simple = False):
        note_pattern = re.compile(r'^[A-Ga-g]([b#])?\1{0,2}?\d?$') #raw because of '\'
        if note_pattern.search(note) == None:
            raise Exception('Could not parse the note: '+note)

        self.tone = note[0].upper()
        self.accidental = re.findall('[b#]{1,3}', note)
        self.octave = re.findall('[0-9]', note)

        if self.accidental == []:
            self.accidental = ''
        else:
            self.accidental = self.accidental[0]

        if self.octave == []:
            self.octave = 4
        else:
            self.octave = int(self.octave[0])

        self.note_id = {'C':0, 'D':2, 'E':4, 'F':5, 'G':7, 'A':9, 'B':11, 'c':12, 'd':14, 'e':16, 'f':17, 'g':19, 'a':21, 'b':23}[self.tone]
        for change in self.accidental:
            if change == '#': self.note_id += 1
            elif change == 'b': self.note_id -= 1

        if self.note_id > 0:
            self.note_id %= 12


    def __add__(self, interval):
        if not isinstance(interval, Interval):
            raise Exception('Cannot add '+type(interval)+' to a note.')

        # * _old_note is the index in the list of the old note tone.
        # * new_note_tone is calculated adding the interval_number-1 because
        # you have start counting in the current tone. e.g. the fifth of
        # E is: (E F G A) B.
        _old_tone = 'CDEFGABcdefgab'.index(self.tone)
        new_note_tone = 'CDEFGABcdefgab'[_old_tone+interval.number-1]


        # %12 because it wraps in B->C and starts over.
        new_note_id = (self.note_id+interval.semitone)

        # First calculates the note, and then the difference from the note
        # without accidentals, then adds proper accidentals.
        difference = new_note_id - {'C':0, 'D':2, 'E':4, 'F':5, 'G':7, 'A':9, 'B':11, 'c':12, 'd':14, 'e':16, 'f':17, 'g':19, 'a':21, 'b':23}[new_note_tone]
        # In some cases, like G##+m3, difference is -11, and it should be
        # 1, so this corrects the error.
        if abs(difference)>3:
            difference = difference + 12

        if difference<0: accidental = 'b'*abs(difference)
        elif difference>0: accidental = '#'*abs(difference)
        else: accidental = ''

        new_note_tone = new_note_tone.upper()

        # it calculates how many times it wrapped around B->C and adds.
        new_note_octave = (self.note_id+interval.semitone)//12+self.octave
        # corrects cases like B#, B##, B### and A###.
        # http://en.wikipedia.org/wiki/Scientific_pitch_notation#C-flat_and_B-sharp_problems
        if new_note_tone+accidental in ['B#', 'B##', 'B###', 'A###']:
            new_note_octave -= 1

        return Note(new_note_tone+accidental+str(new_note_octave))

    def frequency(self):
        """
        Returns frequency in Hz. It uses the method given in
        http://en.wikipedia.org/wiki/Note#Note_frequency_.28hertz.29
        """
        pass

    def lilypond_notation(self):
        return str(self).replace('b', 'es').replace('#', 'is').lower()

    def scientific_notation(self):
        return str(self)+str(self.octave)

    def __repr__(self):
        return "Note(\"%s\")" % self.scientific_notation()

    def __str__(self):
        return self.tone+self.accidental

    def __eq__(self, other):
        return self.scientific_notation() == other.scientific_notation()