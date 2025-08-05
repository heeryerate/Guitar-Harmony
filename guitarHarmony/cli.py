# -*- coding: utf-8 -*-
"""
Command-line interface for GuitarHarmony.
"""

import argparse
import sys
from typing import List, Optional

from .note import Note
from .chord import Chord
from .scale import Scale
from .interval import Interval
from .exercise import Exercise
from .config import get_config


def create_note(args: argparse.Namespace) -> None:
    """Create and display a note."""
    try:
        note = Note(args.note, args.duration)
        print(f"Note: {note}")
        if args.show:
            note.show(args.show_type)
    except ValueError as e:
        print(f"Error creating note: {e}")
        sys.exit(1)


def create_chord(args: argparse.Namespace) -> None:
    """Create and display a chord."""
    try:
        chord = Chord(args.root, args.chord_type, duration=args.duration)
        print(f"Chord: {chord}")
        print(f"Notes: {[note.name for note in chord.chord_notes]}")
        if args.show:
            chord.show(args.show_type)
    except ValueError as e:
        print(f"Error creating chord: {e}")
        sys.exit(1)


def create_scale(args: argparse.Namespace) -> None:
    """Create and display a scale."""
    try:
        scale = Scale(args.root, args.scale_type)
        print(f"Scale: {scale}")
        print(f"Notes: {[note.name for note in scale.scale_notes]}")
        if args.show:
            # Create a stream from scale notes
            from .stream import Stream
            stream = Stream(scale.scale_notes)
            stream.show(args.show_type)
    except ValueError as e:
        print(f"Error creating scale: {e}")
        sys.exit(1)


def create_interval(args: argparse.Namespace) -> None:
    """Create and display an interval."""
    try:
        interval = Interval(args.interval)
        print(f"Interval: {interval}")
        if args.show:
            interval.show(args.show_type, args.base)
    except ValueError as e:
        print(f"Error creating interval: {e}")
        sys.exit(1)


def generate_exercises(args: argparse.Namespace) -> None:
    """Generate exercises."""
    try:
        exercise = Exercise(args.exercise_type, args.difficulty)
        
        if args.exercise_type == 'chord_recognition':
            exercise.generate_chord_exercise(args.count)
        elif args.exercise_type == 'scale_construction':
            exercise.generate_scale_exercise(args.count)
        else:
            print(f"Unknown exercise type: {args.exercise_type}")
            sys.exit(1)
        
        exercises = exercise.get_exercises()
        print(f"Generated {len(exercises)} exercises:")
        for i, ex in enumerate(exercises, 1):
            print(f"{i}. {ex['question']}")
            print(f"   Notes: {ex['notes']}")
            print()
            
    except Exception as e:
        print(f"Error generating exercises: {e}")
        sys.exit(1)


def list_options(args: argparse.Namespace) -> None:
    """List available options."""
    if args.type == 'chords':
        print("Available chord types:")
        for chord_type in Chord.displayAllChordsRecipe():
            print(f"  - {chord_type}")
    elif args.type == 'scales':
        print("Available scale types:")
        for scale_type in Scale.displayAllScalesRecipe():
            print(f"  - {scale_type}")
    elif args.type == 'intervals':
        print("Available intervals:")
        for interval in Interval.displayAllIntervals():
            print(f"  - {interval}")
    else:
        print(f"Unknown type: {args.type}")


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="GuitarHarmony - Music theory and guitar learning library",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s note C --show
  %(prog)s chord C maj7 --show midi
  %(prog)s scale C major --show notation
  %(prog)s interval P5 --show --base C
  %(prog)s exercise chord_recognition --count 5
  %(prog)s list chords
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Note command
    note_parser = subparsers.add_parser('note', help='Create a note')
    note_parser.add_argument('note', help='Note name (e.g., C, F#, Ab)')
    note_parser.add_argument('--duration', type=float, default=1.0, help='Note duration')
    note_parser.add_argument('--show', action='store_true', help='Show the note')
    note_parser.add_argument('--show-type', choices=['', 'midi', 'notation', 'text'], 
                           default='', help='Show type')
    note_parser.set_defaults(func=create_note)
    
    # Chord command
    chord_parser = subparsers.add_parser('chord', help='Create a chord')
    chord_parser.add_argument('root', help='Root note')
    chord_parser.add_argument('chord_type', help='Chord type (e.g., maj7, m, 7)')
    chord_parser.add_argument('--duration', type=float, default=1.0, help='Chord duration')
    chord_parser.add_argument('--show', action='store_true', help='Show the chord')
    chord_parser.add_argument('--show-type', choices=['', 'midi', 'notation', 'text'], 
                            default='', help='Show type')
    chord_parser.set_defaults(func=create_chord)
    
    # Scale command
    scale_parser = subparsers.add_parser('scale', help='Create a scale')
    scale_parser.add_argument('root', help='Root note')
    scale_parser.add_argument('scale_type', help='Scale type (e.g., major, minor)')
    scale_parser.add_argument('--show', action='store_true', help='Show the scale')
    scale_parser.add_argument('--show-type', choices=['', 'midi', 'notation', 'text'], 
                            default='', help='Show type')
    scale_parser.set_defaults(func=create_scale)
    
    # Interval command
    interval_parser = subparsers.add_parser('interval', help='Create an interval')
    interval_parser.add_argument('interval', help='Interval (e.g., P5, M3)')
    interval_parser.add_argument('--base', default='C', help='Base note')
    interval_parser.add_argument('--show', action='store_true', help='Show the interval')
    interval_parser.add_argument('--show-type', choices=['', 'midi', 'notation', 'text'], 
                               default='', help='Show type')
    interval_parser.set_defaults(func=create_interval)
    
    # Exercise command
    exercise_parser = subparsers.add_parser('exercise', help='Generate exercises')
    exercise_parser.add_argument('exercise_type', choices=['chord_recognition', 'scale_construction'],
                               help='Exercise type')
    exercise_parser.add_argument('--count', type=int, default=5, help='Number of exercises')
    exercise_parser.add_argument('--difficulty', default='beginner', 
                               choices=['beginner', 'intermediate', 'advanced'],
                               help='Exercise difficulty')
    exercise_parser.set_defaults(func=generate_exercises)
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available options')
    list_parser.add_argument('type', choices=['chords', 'scales', 'intervals'],
                           help='Type to list')
    list_parser.set_defaults(func=list_options)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main() 