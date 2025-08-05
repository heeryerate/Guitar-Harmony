import React, { useState } from 'react';
import { Card, Form, Button, Row, Col, Alert, Spinner } from 'react-bootstrap';
import axios from 'axios';
import AbcMusicStaff from './AbcMusicStaff';
import SimpleMidiPlayer from './SimpleMidiPlayer';

const NoteTab = () => {
  const [noteName, setNoteName] = useState('C');
  const [duration, setDuration] = useState(1.0);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/api/note', {
        note: noteName,
        duration: duration
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
        <i className="fas fa-music me-2"></i>
        Create Note
      </h2>

      <Row className="mb-1">
        <Col md={6}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Note Parameters</h5>
            </Card.Header>
            <Card.Body>
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>Note Name</Form.Label>
                  <Form.Control
                    type="text"
                    value={noteName}
                    onChange={(e) => setNoteName(e.target.value)}
                    placeholder="e.g., C, F#, Ab"
                  />
                  <Form.Text className="text-muted">
                    Enter a note name with optional accidentals (# or b)
                  </Form.Text>
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Duration</Form.Label>
                  <Form.Control
                    type="number"
                    value={duration}
                    onChange={(e) => setDuration(parseFloat(e.target.value))}
                    step="0.1"
                    min="0.1"
                  />
                  <Form.Text className="text-muted">
                    Duration in beats
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
                      Creating Note...
                    </>
                  ) : (
                    <>
                      <i className="fas fa-plus me-2"></i>
                      Create Note
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
                  Note Created Successfully
                </h6>
              </Card.Header>
              <Card.Body>
                <div className="text-center mb-3">
                  <div className="display-4 text-primary fw-bold">
                    {result.note}
                  </div>
                </div>

                <Row>
                  <Col sm={6}>
                    <strong>Name:</strong> {result.name}<br />
                    <strong>Octave:</strong> {result.octave}<br />
                    <strong>Semi-steps:</strong> {result.semi_steps}
                  </Col>
                  <Col sm={6}>
                    <strong>Duration:</strong> {result.duration}<br />
                    <strong>Full Name:</strong> {result.note}
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
                  notes={[result.name]} 
                  title={`Note: ${result.note}`}
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
                  notes={[result.name]} 
                  title={`Note: ${result.note}`}
                  isNote={true}
                />
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}
    </div>
  );
};

export default NoteTab; 