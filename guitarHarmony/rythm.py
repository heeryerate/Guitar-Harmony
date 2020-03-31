from __future__ import absolute_import
from collections import Counter
import numpy as np

class Rythm(object):
    def __init__(self, *args, **kwargs):
        self._init(*args, **kwargs)
        
    def _init(self,*args, **kwargs):
        #TODO
        sample = kwargs.get('test') or 'BxSxBxSx'
        beats = {}
        for k in Counter(sample):
            beats[k] = [i for i,x in enumerate(sample) if x==k]
        self.beats1 = beats
        self.beats2 = {i:k for k,v in beats.items() for i in v}
        self.dur = self._decide_duration()
        
    def _decide_duration(self):
        ''' decide duration according to self.beats'''
        #TODO
        return 1.0/8
    
    def applyNotes(self, sorted_note_list):
        '''
        Test: sorted_note_list = ['A2', 'E3', 'A3', 'C4', 'D4', 'G4']
        '''
        #TODO
        beat2chord = {}
        nnotes = len(sorted_note_list)
        B1 = sorted_note_list[:int(nnotes/3)]
        S1 = sorted_note_list[-int(nnotes/2):]
        beat2chord['B'] = gt.Chord(B1[0], 'user', chord_notes=B1)
        beat2chord['S'] = gt.Chord(S1[0], 'user', chord_notes=S1)
        
        xset = sorted_note_list[1:-1] + ['R']

        out = []
        for i in sorted(self.beats2):
            a = beat2chord.get(self.beats2.get(i)) or gt.Note(np.random.choice(xset),self.dur)
            out.append(a)
        
        self.out = out
        self.outStream = gt.Stream(out)
        
    def __call__(self, note_list):
        sorted_note_list = sorted(note_list)
        # sorted_note_list = note_list
        self.applyNotes(sorted_note_list)
        return self.outStream.show('midi')
    
    
    
# Test: 
# ss = Rythm(test='BxSBBxSx')
# ss(['A2', 'E3', 'A3', 'C4', 'D4', 'G4'])