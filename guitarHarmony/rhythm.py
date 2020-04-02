from __future__ import absolute_import
from collections import Counter
import numpy as np
import music21 as m2

class Rhythm(object):
    def __init__(self, pattern='', durations=None, bass='B', snare='S', hithat='x', *args, **kwargs):
        pattern = pattern or 'BxSxSxSBSx'
        durations = durations or [2, 2, 2, 1, 1, 1, 1, 2, 2, 2]
        self.bass, self.snare, self.hithat = bass, snare, hithat
        self.beatMap = {self.bass:[], self.snare:[], self.hithat:[]}

        self._init(pattern, durations, *args, **kwargs)
        
    def _init(self, pattern, durations=None, positions=None, total=4.0, normalize=4.0, *args, **kwargs):
        if durations is None:
            try:
                assert max(positions) < total, 'Invalid total positions'
                durations = self.position2duration(positions, total)
            except:
                raise ValueError('Invalid position provided.')

        assert len(pattern)==len(durations), 'Lenghth of pattern and durations not match.'

        normalize = float(normalize)

        self.pattern = pattern
        self.durations = [normalize*i/sum(durations) for i in durations]
        self.positions = positions or self.duration2position(self.durations)

    @staticmethod
    def duration2position(ds):
        p,ps = 0, [0]
        for i in ds:
            p+=i
            ps.append(p)
            
        return ps[:-1]
        
    @staticmethod
    def position2duration(ps, total=4):
        e, ds = total, []
        for s in ps[::-1]:
            ds.append(e-s)
            e = s
        return ds[::-1]

    @staticmethod
    def apply_elements(pattern, durations, **kwargs):
        stream = m2.stream.Stream([m2.note.Rest()])
        for i, d in zip(pattern, durations):
            el = kwargs[i]
            if isinstance(el,gt.chord.Chord):
                el = el.m2()
            el.quarterLength = d
            stream.append(el)
        return stream   

    @staticmethod
    def _replace_instrument(pattern, pos, instr):
        if pos==-1:
            pos = len(pattern)-1
        return pattern[:pos] + instr + pattern[pos+1:]

    def replace_instrument(self, pos, instr):
        new_pattern = self._replace_instrument(self.pattern, pos, instr)
        return Rhythm(new_pattern, self.durations, *self.args, **self.kwargs)

    @staticmethod
    def _split_note(pattern, durations, pos, instr=None):
        new_dur = durations[pos]/2.0
        instr = instr or pattern[pos]
        if len(instr)==1:
            instr = instr+instr

        if pos==-1:
            pos = len(pattern)-1
        new_pattern = pattern[:pos] + instr + pattern[pos+1:]
        new_durations = durations[:pos] + [new_dur, new_dur] + durations[pos+1:]
        return new_pattern, new_durations

    def split_note(self, pos, instr = None):
        new_pattern, new_durations = self._split_note(self.pattern, self.durations, pos, instr)
        return Rhythm(new_pattern, new_durations)

    @staticmethod
    def _substitute_pattern(pattern, durations, pos_1, pos_2, subpat, subdur):
        assert len(subpat)==len(subdur), 'len of subpat and subdur not match.'
        lpat, xpat, rpat = pattern[:pos_1], pattern[pos_1:pos_2], pattern[pos_2:]
        ldur, xdur, rdur = durations[:pos_1], durations[pos_1:pos_2], durations[pos_2:]
        scaler = 1.0*sum(xdur)/sum(subdur)
        subdur = [scaler*i for i in subdur]
        new_pattern = lpat + subpat + rpat
        new_durations = ldur + subdur + rdur
        return new_pattern, new_durations

    def substitute_pattern(self, pos_1, pos_2, sub=None, subpat=None, subdur=None):
        if isinstance(sub, self.__class__):
            subpat, subdur = sub.pattern, sub.durations

        new_pattern, new_durations = self._substitute_pattern(self.pattern, self.durations, pos_1, pos_2, subpat, subdur)
        return Rhythm(new_pattern, new_durations)

    @staticmethod
    def _chord2beat(note_list):
        '''
        note_list: Input chord, or a list of notes; each of type music21.note.Note:
        can be [music21.note.Note, music21.note.Note, music21.note.Note]
        or calling m2chord.notes, where m2chord is of type music21.chord.Chord
        or calling chord.m2().notes, where chord is of type guitarHarmony.chord.Chord
        '''
        nn = len(note_list)
        nB, nS = int(nn/3.0), int(nn/2.0)

        sorted_note_list = sorted(note_list)
        nl_B = sorted_note_list[:nB]
        nl_S = sorted_note_list[nS:]
        nl_x = sorted_note_list[1:-1]

        outB, outS = [], []
        for i in range(nB):
            outB.append(m2.chord.Chord(nl_B[i:]))

        for i in range(nS):
            outS.append(m2.chord.Chord(nl_S[::-1][i:]))
        
        return outB, outS, nl_x
        
    def reset_beatMap(self, note_list):
        bass, snare, hithat = self._chord2beat(note_list)
        self.beatMap[self.bass] = bass
        self.beatMap[self.snare] = snare
        self.beatMap[self.hithat] = hithat

    







