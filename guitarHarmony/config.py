# -*- coding: utf-8 -*-
"""
Configuration management for GuitarHarmony.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class GuitarHarmonyConfig:
    """Configuration class for GuitarHarmony."""
    
    # Default octave
    default_octave: int = 4
    
    # Default duration
    default_duration: float = 1.0
    
    # Default accidental type
    default_accidental_type: str = '#'
    
    # MIDI settings
    midi_tempo: int = 120
    midi_volume: int = 100
    midi_channel: int = 0
    
    # Display settings
    show_octave: bool = True
    show_duration: bool = True
    
    # Logging settings
    log_level: str = "INFO"
    log_file: Optional[str] = None
    console_output: bool = True
    
    # Exercise settings
    default_exercise_count: int = 10
    exercise_difficulty: str = "beginner"
    
    # Scale settings
    default_scale_type: str = "major"
    
    # Chord settings
    default_chord_type: str = ""
    
    # Rhythm settings
    default_rhythm_pattern: str = "BxSxSxSBSx"
    default_rhythm_duration: float = 4.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            'default_octave': self.default_octave,
            'default_duration': self.default_duration,
            'default_accidental_type': self.default_accidental_type,
            'midi_tempo': self.midi_tempo,
            'midi_volume': self.midi_volume,
            'midi_channel': self.midi_channel,
            'show_octave': self.show_octave,
            'show_duration': self.show_duration,
            'log_level': self.log_level,
            'log_file': self.log_file,
            'console_output': self.console_output,
            'default_exercise_count': self.default_exercise_count,
            'exercise_difficulty': self.exercise_difficulty,
            'default_scale_type': self.default_scale_type,
            'default_chord_type': self.default_chord_type,
            'default_rhythm_pattern': self.default_rhythm_pattern,
            'default_rhythm_duration': self.default_rhythm_duration,
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'GuitarHarmonyConfig':
        """Create config from dictionary."""
        return cls(**config_dict)
    
    def update(self, **kwargs) -> None:
        """Update configuration with new values."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


# Global configuration instance
config = GuitarHarmonyConfig()


def get_config() -> GuitarHarmonyConfig:
    """Get the global configuration."""
    return config


def update_config(**kwargs) -> None:
    """Update the global configuration."""
    config.update(**kwargs)


def load_config_from_env() -> None:
    """Load configuration from environment variables."""
    env_mapping = {
        'GUITAR_HARMONY_DEFAULT_OCTAVE': 'default_octave',
        'GUITAR_HARMONY_DEFAULT_DURATION': 'default_duration',
        'GUITAR_HARMONY_DEFAULT_ACCIDENTAL_TYPE': 'default_accidental_type',
        'GUITAR_HARMONY_MIDI_TEMPO': 'midi_tempo',
        'GUITAR_HARMONY_MIDI_VOLUME': 'midi_volume',
        'GUITAR_HARMONY_MIDI_CHANNEL': 'midi_channel',
        'GUITAR_HARMONY_SHOW_OCTAVE': 'show_octave',
        'GUITAR_HARMONY_SHOW_DURATION': 'show_duration',
        'GUITAR_HARMONY_LOG_LEVEL': 'log_level',
        'GUITAR_HARMONY_LOG_FILE': 'log_file',
        'GUITAR_HARMONY_CONSOLE_OUTPUT': 'console_output',
        'GUITAR_HARMONY_DEFAULT_EXERCISE_COUNT': 'default_exercise_count',
        'GUITAR_HARMONY_EXERCISE_DIFFICULTY': 'exercise_difficulty',
        'GUITAR_HARMONY_DEFAULT_SCALE_TYPE': 'default_scale_type',
        'GUITAR_HARMONY_DEFAULT_CHORD_TYPE': 'default_chord_type',
        'GUITAR_HARMONY_DEFAULT_RHYTHM_PATTERN': 'default_rhythm_pattern',
        'GUITAR_HARMONY_DEFAULT_RHYTHM_DURATION': 'default_rhythm_duration',
    }
    
    updates = {}
    for env_var, config_key in env_mapping.items():
        value = os.getenv(env_var)
        if value is not None:
            # Convert string values to appropriate types
            if config_key in ['default_octave', 'midi_tempo', 'midi_volume', 'midi_channel', 'default_exercise_count']:
                updates[config_key] = int(value)
            elif config_key in ['default_duration', 'default_rhythm_duration']:
                updates[config_key] = float(value)
            elif config_key in ['show_octave', 'show_duration', 'console_output']:
                updates[config_key] = value.lower() in ['true', '1', 'yes']
            else:
                updates[config_key] = value
    
    if updates:
        config.update(**updates)


# Load configuration from environment on import
load_config_from_env() 