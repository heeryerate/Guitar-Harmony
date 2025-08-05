# -*- coding: utf-8 -*-
# @Author: Xi He
# @Date:   2020-03-21 12:34:40
# @Last Modified by:   Xi He
# @Last Modified time: 2020-03-21 12:36:06

from .helper import CONSTANT
from .note import Note
from .chord import Chord
from .scale import Scale
from .interval import Interval

class Register:
    """
    Register class for managing musical elements and their relationships.
    """
    
    def __init__(self):
        self.notes = {}
        self.chords = {}
        self.scales = {}
        self.intervals = {}
        
    def register_note(self, note_name, note_obj):
        """Register a note object."""
        self.notes[note_name] = note_obj
        
    def register_chord(self, chord_name, chord_obj):
        """Register a chord object."""
        self.chords[chord_name] = chord_obj
        
    def register_scale(self, scale_name, scale_obj):
        """Register a scale object."""
        self.scales[scale_name] = scale_obj
        
    def register_interval(self, interval_name, interval_obj):
        """Register an interval object."""
        self.intervals[interval_name] = interval_obj
        
    def get_note(self, note_name):
        """Get a registered note."""
        return self.notes.get(note_name)
        
    def get_chord(self, chord_name):
        """Get a registered chord."""
        return self.chords.get(chord_name)
        
    def get_scale(self, scale_name):
        """Get a registered scale."""
        return self.scales.get(scale_name)
        
    def get_interval(self, interval_name):
        """Get a registered interval."""
        return self.intervals.get(interval_name)
        
    def list_notes(self):
        """List all registered notes."""
        return list(self.notes.keys())
        
    def list_chords(self):
        """List all registered chords."""
        return list(self.chords.keys())
        
    def list_scales(self):
        """List all registered scales."""
        return list(self.scales.keys())
        
    def list_intervals(self):
        """List all registered intervals."""
        return list(self.intervals.keys())
        
    def clear(self):
        """Clear all registrations."""
        self.notes.clear()
        self.chords.clear()
        self.scales.clear()
        self.intervals.clear()