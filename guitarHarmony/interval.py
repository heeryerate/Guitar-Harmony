from .helper import reverseDict, warning, suf, CONSTANT
import numpy as np
import music21 as m2
from .note import Note

class Interval(object):
    __all__ = ['getInterval', 'applyInterval', 'show']

    def __init__(self, interval = 'P1'):
        if not interval in CONSTANT.interval_to_semisteps():
            raise ValueError(f'Could not parse the interval {interval}! Check valid list at Interval.displayAllIntervals()')
        self.interval = interval
        self.interval_type = self.interval[0]
        self.pitch_steps = int(self.interval[1:])
        self.semi_steps = CONSTANT.interval_to_semisteps()[self.interval]

    @staticmethod
    def getInterval(base='C', target='D'):
        if isinstance(base, str): base = Note(base)
        if isinstance(target, str): target = Note(target)

        semiA = base.getSemiSteps()
        semiB = target.getSemiSteps()
        semi_diff= semiB-semiA

        if semi_diff < 0:
            warning(f"Reverse base and target, getInterval({target}, {base}): {Interval.getInterval(target, base)}")
            return 
        octave_diff = target.octave - base.octave
        if octave_diff >= 2:
            warning(f"{target} is two octave from {base}")
            return 
        pitch_steps = CONSTANT.tone_to_steps()[target.tone]-CONSTANT.tone_to_steps()[base.tone]+octave_diff*7+1

        if len(CONSTANT.semisteps_to_interval()[semi_diff]) == 1:
            return Interval(CONSTANT.semisteps_to_interval()[semi_diff][0])
        for interval in CONSTANT.semisteps_to_interval()[semi_diff]:
            if interval.endswith(str(pitch_steps)):
                return Interval(interval)
        else:
            warning(f"double augmented or double diminished ignored.")
            return

    def applyToNote(self, base='C'):
        if isinstance(base, str): base=Note(base)
        return Interval.applyInterval(base, self)

    @staticmethod
    def applyInterval(base='C', interval='P1'):
        if isinstance(base, str): base=Note(base)
        if isinstance(interval, str): interval=Interval(interval)

        target_pitch_order = CONSTANT.tone_to_steps()[base.tone] + interval.pitch_steps - 1
        if target_pitch_order % 7:
            target_pitch = CONSTANT.steps_to_tone()[target_pitch_order % 7][0]
            target_octave = target_pitch_order // 7
        else:
            target_pitch = CONSTANT.steps_to_tone()[7][0]
            target_octave = target_pitch_order // 7 - 1

        accent=interval.semi_steps-(Note(target_pitch+str(base.octave+target_octave)).getSemiSteps() - base.getSemiSteps())
        if not accent:
            return Note(target_pitch+str(base.octave+target_octave))
        else:
            mark = 'b'*(-accent) if accent<0 else '#'*accent
            return Note(target_pitch+mark+str(base.octave+target_octave))

    @staticmethod
    def displayAllIntervals():
        return list(CONSTANT.interval_to_semisteps().keys())

    def show(self, show_type = '', base='C'):
        from .chord import Chord
        from .stream import Stream 

        chord = Chord(root=base, chord_type='user', chord_notes=[base, Interval.applyInterval(base, self.interval)])
        print(chord)
        s = Stream([chord])
        if show_type == 'text':
            print(f"{self} on base {Note(base)}")
        else:
            s.show(show_type)

    def type(self):
        return 'Interval'

    def __repr__(self):
        pitch_suffix = suf(int(self.interval[1:]))
        return f"Interval({CONSTANT.interval_name_mapping()[self.interval_type]},{pitch_suffix})"

    def __str__(self):
        return self.interval

    def __eq__(self, other):
        if isinstance(other, str): other=Interval(other)
        return CONSTANT.interval_to_semisteps()[self.interval] == CONSTANT.interval_to_semisteps()[other.interval]

    def __neg__(self):
        return 

