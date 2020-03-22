from .helper import reverseDict, warning, suf
import numpy as np
import music21 as m2
from .note import Note

class Interval(object):
    """
    The interval class.

    The notes are to be parsed in th following way:
    * the quality, (m, M, p, A, d)
    * the number. (1 to 8) [Compound intervals will be supported]

    For example, 'd8', 'P1', 'A5' are valid intervals. 'P3', '5' are not.
    """
    __all__ = ['getIntervals', 'applyInterval', 'show']
    interval_to_semisteps = {   'P1':0,     'A1':1, 
                                'd2':0,     'm2':1,     'M2':2,     'A2':3,
                                'd3':2,     'm3':3,     'M3':4,     'A3':5, 
                                'd4':4,     'P4':5,     'A4':6, 
                                'd5':6,     'P5':7,     'A5':8,  
                                'd6':7,     'm6':8,     'M6':9,     'A6':10,
                                'd7':9,     'm7':10,    'M7':11,    'A7':12,
                                'd8':11,    'P8':12,    'A8':13, 
                                'd9':12,    'm9':13,    'M9':14,    'A9':15, 
                                'd10':14,   'm10':15,   'M10':16,   'A10':17,
                                'd11':16,   'P11':17,   'A11':18, 
                                'd12':18,   'P12':19,   'A12':20,
                                'd13':19,   'm13':20,   'M13':21,   'A13':22,
                                'd14':21,   'm14':22,   'M14':23,   }
    semisteps_to_interval = reverseDict(interval_to_semisteps)
    tone_to_order = {'C':1, 'D':2, 'E':3, 'F':4, 'G':5, 'A':6, 'B':7}
    order_to_tone = reverseDict(tone_to_order)
    type_mapping = {'P': 'Perfect', 'd': 'Diminished', 
                    'm': 'Minor', 'M': 'Major', 'A': 'Augmented'}

    def __init__(self, interval = 'P1'):
        self.interval = interval
        self.interval_type = str(self.interval[0])
        self.pitch_steps = int(self.interval[1:])
        try:
            self.semitone_steps = self.interval_to_semisteps[self.interval]
        except:
            raise Exception(f'Could not parse the interval {interval}! Check valid list at Interval.displayAllIntervals()')

    @staticmethod
    def getIntervals(base='C', target='D'):
        if isinstance(base, str): base = Note(base)
        if isinstance(target, str): target = Note(target)

        semiA = base.semiSteps()
        semiB = target.semiSteps()
        semi_diff= semiB-semiA

        if semi_diff < 0:
            warning(f"Reverse base and target, getIntervals({target}, {base}): {Interval.getIntervals(target, base)}")
            return 
        octave_diff = target.octave - base.octave
        if octave_diff >= 2:
            warning(f"{target} is two octave from {base}")
            return 
        pitch_steps = Interval.tone_to_order[target.tone]-Interval.tone_to_order[base.tone]+octave_diff*7+1

        if len(Interval.semisteps_to_interval[semi_diff]) == 1:
            return Interval(Interval.semisteps_to_interval[semi_diff][0])
        for interval in Interval.semisteps_to_interval[semi_diff]:
            if interval.endswith(str(pitch_steps)):
                return Interval(interval)
        else:
            warning(f"double augmented or double diminished ignored.")
            return

    @staticmethod
    def applyInterval(base='C', interval='P1'):
        if isinstance(base, str): base=Note(base)
        if isinstance(interval, str): interval=Interval(interval)

        target_pitch_order = Interval.tone_to_order[base.tone] + interval.pitch_steps - 1
        if target_pitch_order % 7:
            target_pitch = Interval.order_to_tone[target_pitch_order % 7][0]
            target_octave = target_pitch_order // 7
        else:
            target_pitch = Interval.order_to_tone[7][0]
            target_octave = target_pitch_order // 7 - 1

        accent=interval.semitone_steps-(Note(target_pitch+str(base.octave+target_octave)).semiSteps() - base.semiSteps())
        if not accent:
            return Note(target_pitch+str(base.octave+target_octave))
        else:
            mark = 'b'*(-accent) if accent<0 else '#'*accent
            return Note(target_pitch+mark+str(base.octave+target_octave))

    @staticmethod
    def displayAllIntervals():
        return list(Interval.interval_to_semisteps.keys())

    def show(self, show_type = '', base='C'):
        from .chord import Chord
        from .stream import Stream 

        chord = Chord(root=base, chord_type=None, notes_recipe=[base, Interval.applyInterval(base, self.interval)])
        s = Stream([chord])
        if show_type == 'text':
            print(f"{self} on base {Note(base)}")
        else:
            s.show(show_type)

    def __repr__(self):
        pitch_suffix = suf(int(self.interval[1:]))
        return f"Interval({Interval.type_mapping[self.interval_type]},{pitch_suffix})"

    def __str__(self):
        return self.interval

    def __eq__(self, other):
        return self.interval_to_semisteps[self.interval] == self.interval_to_semisteps[other.interval]

    def __neg__(self):
        return 

