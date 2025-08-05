#!/usr/bin/env python3
"""
Simple API server for GuitarHarmony React app.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from guitarHarmony.note import Note
from guitarHarmony.chord import Chord
from guitarHarmony.scale import Scale
from guitarHarmony.interval import Interval
from guitarHarmony.exercise import Exercise
from guitarHarmony.register import Register
from guitarHarmony.config import get_config
from guitarHarmony.logger import get_logger

logger = get_logger()

app = FastAPI(
    title="GuitarHarmony API",
    description="API for GuitarHarmony music theory library",
    version="0.5.9"
)

# Enable CORS for React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global register for storing user data
register = Register()
config = get_config()

# Pydantic models for request/response
class NoteRequest(BaseModel):
    note: str = "C"
    duration: float = 1.0

class NoteResponse(BaseModel):
    success: bool
    note: str
    name: str
    octave: int
    semi_steps: int
    duration: float

class ChordRequest(BaseModel):
    root: str = "C"
    chord_type: str = ""
    duration: float = 1.0

class ChordResponse(BaseModel):
    success: bool
    chord: str
    root: str
    chord_type: str
    notes: List[str]
    duration: float

class ScaleRequest(BaseModel):
    root: str = "C"
    scale_type: str = "major"

class ScaleResponse(BaseModel):
    success: bool
    scale: str
    root: str
    scale_type: str
    notes: List[str]

class IntervalRequest(BaseModel):
    interval: str = "P5"
    base: str = "C"

class IntervalResponse(BaseModel):
    success: bool
    interval: str
    base_note: str
    result_note: str
    semi_steps: int

class ExerciseRequest(BaseModel):
    exercise_type: str = "chord_recognition"
    count: int = 5
    difficulty: str = "beginner"

class ExerciseResponse(BaseModel):
    success: bool
    exercises: List[dict]
    count: int

class RegisterRequest(BaseModel):
    type: str
    name: str

class RegisterResponse(BaseModel):
    success: bool
    message: str

class OptionsResponse(BaseModel):
    success: bool
    chord_types: List[str]
    scale_types: List[str]
    intervals: List[str]

class ConfigResponse(BaseModel):
    success: bool
    config: dict

@app.get("/")
def read_root():
    """Root endpoint."""
    return {"message": "GuitarHarmony API", "version": "0.5.9"}

@app.post("/api/note", response_model=NoteResponse)
def create_note(request: NoteRequest):
    """Create a note."""
    try:
        note = Note(request.note, request.duration)
        
        return NoteResponse(
            success=True,
            note=str(note),
            name=note.name,
            octave=note.octave,
            semi_steps=note.getSemiSteps(),
            duration=note.duration
        )
    except Exception as e:
        logger.error(f"Error creating note: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/chord", response_model=ChordResponse)
def create_chord(request: ChordRequest):
    """Create a chord."""
    try:
        chord = Chord(request.root, request.chord_type, duration=request.duration)
        
        return ChordResponse(
            success=True,
            chord=str(chord),
            root=chord.root.name,
            chord_type=chord.chord_type,
            notes=[note.name for note in chord.chord_notes],
            duration=chord.duration
        )
    except Exception as e:
        logger.error(f"Error creating chord: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/scale", response_model=ScaleResponse)
def create_scale(request: ScaleRequest):
    """Create a scale."""
    try:
        scale = Scale(request.root, request.scale_type)
        
        return ScaleResponse(
            success=True,
            scale=str(scale),
            root=scale.root.name,
            scale_type=scale.scale_type,
            notes=[note.name for note in scale.scale_notes]
        )
    except Exception as e:
        logger.error(f"Error creating scale: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/interval", response_model=IntervalResponse)
def create_interval(request: IntervalRequest):
    """Create an interval."""
    try:
        interval = Interval(request.interval)
        result_note = interval.applyToNote(request.base)
        
        return IntervalResponse(
            success=True,
            interval=str(interval),
            base_note=request.base,
            result_note=str(result_note),
            semi_steps=interval.semi_steps
        )
    except Exception as e:
        logger.error(f"Error creating interval: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/exercise", response_model=ExerciseResponse)
def generate_exercise(request: ExerciseRequest):
    """Generate exercises."""
    try:
        exercise = Exercise(request.exercise_type, request.difficulty)
        
        if request.exercise_type == 'chord_recognition':
            exercise.generate_chord_exercise(request.count)
        elif request.exercise_type == 'scale_construction':
            exercise.generate_scale_exercise(request.count)
        else:
            raise HTTPException(status_code=400, detail="Invalid exercise type")
        
        exercises = exercise.get_exercises()
        
        return ExerciseResponse(
            success=True,
            exercises=exercises,
            count=len(exercises)
        )
    except Exception as e:
        logger.error(f"Error generating exercise: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/options", response_model=OptionsResponse)
def get_options():
    """Get available options."""
    try:
        return OptionsResponse(
            success=True,
            chord_types=Chord.displayAllChordsRecipe(),
            scale_types=Scale.displayAllScalesRecipe(),
            intervals=Interval.displayAllIntervals()
        )
    except Exception as e:
        logger.error(f"Error getting options: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/register", response_model=RegisterResponse)
def register_item(request: RegisterRequest):
    """Register a musical item."""
    try:
        if request.type == 'note':
            note = Note(request.name)
            register.register_note(request.name, note)
        elif request.type == 'chord':
            root, chord_type = request.name.split(' ', 1) if ' ' in request.name else (request.name, '')
            chord = Chord(root, chord_type)
            register.register_chord(request.name, chord)
        elif request.type == 'scale':
            root, scale_type = request.name.split(' ', 1) if ' ' in request.name else (request.name, 'major')
            scale = Scale(root, scale_type)
            register.register_scale(request.name, scale)
        else:
            raise HTTPException(status_code=400, detail="Invalid item type")
        
        return RegisterResponse(
            success=True,
            message=f"{request.type} registered successfully"
        )
    except Exception as e:
        logger.error(f"Error registering item: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/register/list")
def list_registered():
    """List all registered items."""
    try:
        return {
            "success": True,
            "notes": register.list_notes(),
            "chords": register.list_chords(),
            "scales": register.list_scales(),
            "intervals": register.list_intervals()
        }
    except Exception as e:
        logger.error(f"Error listing registered items: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/config", response_model=ConfigResponse)
def get_config_info():
    """Get current configuration."""
    try:
        return ConfigResponse(
            success=True,
            config=config.to_dict()
        )
    except Exception as e:
        logger.error(f"Error getting config: {e}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    print("🎸 GuitarHarmony API Server")
    print("=" * 40)
    print("Starting server on http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    print("=" * 40)
    
    uvicorn.run(app, host="0.0.0.0", port=8000) 