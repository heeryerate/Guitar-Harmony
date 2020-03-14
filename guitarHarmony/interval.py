from .note import Note
from .helper import reverseDict
import numpy as np
import warnings
warnings.simplefilter("error")

class Interval(object):
    """
    The interval class.

    The notes are to be parsed in th following way:
    * the quality, (m, M, p, A, d)
    * the number. (1 to 8) [Compound intervals will be supported]

    For example, 'd8', 'P1', 'A5' are valid intervals. 'P3', '5' are not.
    """
    interval_to_semisteps = {'P1':0, 'A1':1, 'd2':0, 'm2':1, 'M2':2, 'A2':3,
                 'd3':2, 'm3':3, 'M3':4, 'A3':5, 'd4':4, 'P4':5,
                 'A4':6, 'd5':6, 'P5':7, 'A5':8, 'd6':7, 'm6':8,
                 'M6':9, 'A6':10,'d7':9, 'm7':10, 'M7':11, 'A7':12,
                 'd8':11, 'P8':12, 'A8':13, 'm9':13, 'M9':14, 'M10':16, 'P11':17,
                 'A11':18, 'm13':20, 'M13':21}
    semisteps_to_interval = reverseDict(interval_to_semisteps)
    step_to_order = {'C':1, 'D':2, 'E':3, 'F':4, 'G':5, 'A':6, 'B':7}
    type_mapping = {'P': 'Perfect', 'd': 'Diminished', 
                    'm': 'Minor', 'M': 'Major', 'A': 'Augmented'}

    def __init__(self, interval = 'P1', ):
        self.interval = interval
        self.interval_type = str(self.interval[0])
        self.pitch_steps = int(self.interval[1])
        try:
            self.semitone_steps = self.interval_to_semisteps[self.interval]
        except:
            raise Exception('Could not parse the interval.')

    @staticmethod
    def getIntervals(noteA, noteB):
        # TODO: add warning instead of print
        semiA = noteA.semiSteps()
        semiB = noteB.semiSteps()
        semi_diff= semiB-semiA

        if semi_diff < 0:
            print(f"Reverse notes, getIntervals({noteB}, {noteA}): {Interval.getIntervals(noteB, noteA)}")
            return 
        octave_diff = noteB.octave - noteA.octave
        if octave_diff >= 2:
            print(f"{noteB} is two octave from {noteA}")
            return 
        pitch_steps = (Interval.step_to_order[noteB.tone] - Interval.step_to_order[noteA.tone]+1)
        if octave_diff == 1 and pitch_steps == 1:
            pitch_steps = 8 
        if semi_diff not in Interval.semisteps_to_interval:
            semi_diff -= 12

        if len(Interval.semisteps_to_interval[semi_diff]) == 1:
            return Interval(Interval.semisteps_to_interval[semi_diff][0])
        for interval in Interval.semisteps_to_interval[semi_diff]:
            if interval.endswith(str(pitch_steps)):
                return Interval(interval)
        else:
            print(f"double augmented or double diminished ignored.")
            return

    def allIntervals(self):
        return list(self.interval_to_semisteps.keys())

    def __repr__(self):
        if str(self.interval[1:]).endswith('1'):
            pitch_suffix = 'st'
        elif str(self.interval[1:]).endswith('2'):
            pitch_suffix = 'nd'
        elif str(self.interval[1:]).endswith('3'):
            pitch_suffix = 'rd'
        else:
            pitch_suffix = 'th'
        return f"Interval({self.type_mapping[self.interval_type]}, {self.interval[1:]}{pitch_suffix})"

    def __str__(self):
        return self.interval

    def __eq__(self, other):
        return self.interval_to_semisteps[self.interval] == self.interval_to_semisteps[other.interval]

    def __neg__(self):
        return 

