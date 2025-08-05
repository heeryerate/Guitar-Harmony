import React, { useState } from 'react';
import { Card, Form, Button, Row, Col, Alert, Spinner, Badge } from 'react-bootstrap';
import axios from 'axios';
import AbcMusicStaff from './AbcMusicStaff';
import SimpleMidiPlayer from './SimpleMidiPlayer';

const ChordTab = () => {
  const [root, setRoot] = useState('C');
  const [chordType, setChordType] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const chordTypes = [
    { value: '', label: 'Major' },
    { value: 'm', label: 'Minor' },
    { value: '7', label: 'Dominant 7th' },
    { value: 'maj7', label: 'Major 7th' },
    { value: 'm7', label: 'Minor 7th' },
    { value: 'dim', label: 'Diminished' },
    { value: 'aug', label: 'Augmented' },
    { value: 'sus2', label: 'Suspended 2nd' },
    { value: 'sus4', label: 'Suspended 4th' },
    { value: 'add9', label: 'Add 9th' }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/api/chord', {
        root: root,
        chord_type: chordType,
        duration: 1.0
      });

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2 className="mb-1">
        <i className="fas fa-layer-group me-2"></i>
        Create Chord
      </h2>

      <Row className="mb-1">
        <Col md={6}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Chord Parameters</h5>
            </Card.Header>
            <Card.Body>
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>Root Note</Form.Label>
                  <Form.Control
                    type="text"
                    value={root}
                    onChange={(e) => setRoot(e.target.value)}
                    placeholder="e.g., C, D, E"
                  />
                  <Form.Text className="text-muted">
                    The root note of the chord
                  </Form.Text>
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Chord Type</Form.Label>
                  <Form.Select
                    value={chordType}
                    onChange={(e) => setChordType(e.target.value)}
                  >
                    {chordTypes.map((type) => (
                      <option key={type.value} value={type.value}>
                        {type.label}
                      </option>
                    ))}
                  </Form.Select>
                  <Form.Text className="text-muted">
                    The type of chord to create
                  </Form.Text>
                </Form.Group>

                

                <Button 
                  type="submit" 
                  variant="primary" 
                  disabled={loading}
                  className="w-100"
                >
                  {loading ? (
                    <>
                      <Spinner
                        as="span"
                        animation="border"
                        size="sm"
                        role="status"
                        aria-hidden="true"
                        className="me-2"
                      />
                      Creating Chord...
                    </>
                  ) : (
                    <>
                      <i className="fas fa-plus me-2"></i>
                      Create Chord
                    </>
                  )}
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          {error && (
            <Alert variant="danger">
              <i className="fas fa-exclamation-triangle me-2"></i>
              <strong>Error:</strong> {error}
            </Alert>
          )}

          {result && (
            <Card className="border-success">
              <Card.Header className="bg-success text-white">
                <h6 className="mb-0">
                  <i className="fas fa-check me-2"></i>
                  Chord Created Successfully
                </h6>
              </Card.Header>
              <Card.Body>
                <div className="text-center mb-3">
                  <div className="display-4 text-primary fw-bold">
                    {result.chord}
                  </div>
                </div>

                <div className="text-center mb-3">
                  {result.notes.map((note, index) => (
                    <Badge 
                      key={index} 
                      bg="primary" 
                      className="me-2 fs-6"
                    >
                      {note}
                    </Badge>
                  ))}
                </div>

                <Row>
                  <Col sm={6}>
                    <strong>Root:</strong> {result.root}<br />
                    <strong>Type:</strong> {result.chord_type || 'Major'}<br />
                    <strong>Duration:</strong> {result.duration}
                  </Col>
                  <Col sm={6}>
                    <strong>Notes Count:</strong> {result.notes.length}<br />
                    <strong>Full Name:</strong> {result.chord}
                  </Col>
                </Row>
              </Card.Body>
            </Card>
          )}
        </Col>
      </Row>

      {/* Music Staff and MIDI Player */}
      {result && (
        <Row className="mt-1">
          <Col md={6}>
            <Card>
              <Card.Header>
                <h6 className="mb-0">
                  <i className="fas fa-music me-2"></i>
                  Music Notation
                </h6>
              </Card.Header>
              <Card.Body>
                <AbcMusicStaff 
                  notes={result.notes} 
                  title={`Chord: ${result.chord}`}
                />
              </Card.Body>
            </Card>
          </Col>
          <Col md={6}>
            <Card>
              <Card.Header>
                <h6 className="mb-0">
                  <i className="fas fa-volume-up me-2"></i>
                  Audio Playback
                </h6>
              </Card.Header>
              <Card.Body>
                <SimpleMidiPlayer 
                  notes={result.notes} 
                  title={`Chord: ${result.chord}`}
                />
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}
    </div>
  );
};

export default ChordTab; 