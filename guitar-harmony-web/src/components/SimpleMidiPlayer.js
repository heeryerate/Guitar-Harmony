import React, { useState } from 'react';
import { Button, Row, Col } from 'react-bootstrap';

const SimpleMidiPlayer = ({ notes, title, isNote = false }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [audioContext, setAudioContext] = useState(null);

  // Initialize audio context on first user interaction
  const initAudio = () => {
    if (!audioContext) {
      const context = new (window.AudioContext || window.webkitAudioContext)();
      setAudioContext(context);
      console.log('Audio context initialized');
    }
  };

  // Convert note to frequency
  const noteToFrequency = (note) => {
    const noteMap = {
      'C': 261.63, 'C#': 277.18, 'Db': 277.18,
      'D': 293.66, 'D#': 311.13, 'Eb': 311.13,
      'E': 329.63, 'F': 349.23, 'F#': 369.99, 'Gb': 369.99,
      'G': 392.00, 'G#': 415.30, 'Ab': 415.30,
      'A': 440.00, 'A#': 466.16, 'Bb': 466.16,
      'B': 493.88
    };

    let noteName = note.toUpperCase();
    
    // Handle flats - check for Bb, Eb, Ab, etc.
    if (noteName.includes('B') && noteName.length > 1 && noteName[1] === 'B') {
      noteName = noteName.replace('BB', 'Bb');
    }
    
    // Handle other flats (Db, Eb, Gb, Ab)
    const flatPatterns = ['DB', 'EB', 'GB', 'AB'];
    if (flatPatterns.includes(noteName)) {
      noteName = noteName.replace('B', 'b');
    }
    
    console.log('Converting note:', note, 'to:', noteName);
    return noteMap[noteName] || 440; // Default to A4 if not found
  };

  const playTone = (frequency, duration = 1000) => {
    if (!audioContext) {
      console.log('Initializing audio context...');
      initAudio();
      return;
    }

    try {
      const oscillator = audioContext.createOscillator();
      const gainNode = audioContext.createGain();
      
      oscillator.connect(gainNode);
      gainNode.connect(audioContext.destination);
      
      oscillator.frequency.value = frequency;
      oscillator.type = 'sine';
      
      gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration / 1000);
      
      oscillator.start(audioContext.currentTime);
      oscillator.stop(audioContext.currentTime + duration / 1000);
      
      console.log('Playing tone at frequency:', frequency);
    } catch (error) {
      console.error('Error playing tone:', error);
    }
  };

  const playSingleNote = () => {
    if (!notes || notes.length === 0) return;
    
    initAudio();
    const frequency = noteToFrequency(notes[0]);
    playTone(frequency, 1000);
  };

  const playChord = () => {
    if (!notes || notes.length === 0) return;
    
    initAudio();
    notes.forEach((note, index) => {
      const frequency = noteToFrequency(note);
      setTimeout(() => {
        playTone(frequency, 2000);
      }, index * 100);
    });
  };

  const playSequence = () => {
    if (!notes || notes.length === 0) return;
    
    initAudio();
    notes.forEach((note, index) => {
      const frequency = noteToFrequency(note);
      setTimeout(() => {
        playTone(frequency, 500);
      }, index * 600);
    });
  };

  return (
    <div className="midi-player">
      <h6 className="mb-0">
        <i className="fas fa-music me-1"></i>
        Audio
      </h6>
      
      {isNote ? (
        // Simple play/stop for notes
        <Row className="mb-0">
          <Col sm={6}>
            <Button
              variant="primary"
              onClick={playSingleNote}
              disabled={!notes || notes.length === 0}
              className="w-100 mb-0"
              size="sm"
            >
              <i className="fas fa-play me-1"></i>
              Play
            </Button>
          </Col>
          <Col sm={6}>
            <Button
              variant="warning"
              onClick={() => console.log('Stop clicked')}
              className="w-100 mb-0"
              size="sm"
            >
              <i className="fas fa-stop me-1"></i>
              Stop
            </Button>
          </Col>
        </Row>
      ) : (
        // Play sequence/chord for other tabs
        <>
          <Row className="mb-0">
            <Col sm={6}>
              <Button
                variant="primary"
                onClick={playSequence}
                disabled={!notes || notes.length === 0}
                className="w-100 mb-0"
                size="sm"
              >
                <i className="fas fa-play me-1"></i>
                Sequence
              </Button>
            </Col>
            <Col sm={6}>
              <Button
                variant="success"
                onClick={playChord}
                disabled={!notes || notes.length === 0}
                className="w-100 mb-0"
                size="sm"
              >
                <i className="fas fa-layer-group me-1"></i>
                Chord
              </Button>
            </Col>
          </Row>
          
          <Row>
            <Col sm={6}>
              <Button
                variant="warning"
                onClick={() => console.log('Stop clicked')}
                className="w-100"
                size="sm"
              >
                <i className="fas fa-stop me-1"></i>
                Stop
              </Button>
            </Col>
            <Col sm={6}>
              <div className="text-muted small">
                <strong>Notes:</strong> {notes ? notes.join(', ') : 'None'}
              </div>
            </Col>
          </Row>
        </>
      )}
      
      {/* Debug info */}
      <div className="text-center mt-1">
        <small className="text-muted">
          <strong>Status:</strong> {audioContext ? 'Ready' : 'Click to initialize'} | 
          <strong>Notes:</strong> {notes ? notes.join(', ') : 'None'}
        </small>
      </div>
    </div>
  );
};

export default SimpleMidiPlayer; 