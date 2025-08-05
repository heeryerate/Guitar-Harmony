import React, { useState } from 'react';
import { Card, Form, Button, Row, Col, Alert, Spinner, Badge } from 'react-bootstrap';
import axios from 'axios';
import AbcMusicStaff from './AbcMusicStaff';
import SimpleMidiPlayer from './SimpleMidiPlayer';

const ScaleTab = () => {
  const [root, setRoot] = useState('C');
  const [scaleType, setScaleType] = useState('major');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const scaleTypes = [
    { value: 'major', label: 'Major' },
    { value: 'natural_minor', label: 'Natural Minor' },
    { value: 'harmonic_minor', label: 'Harmonic Minor' },
    { value: 'melodic_minor', label: 'Melodic Minor' },
    { value: 'dorian', label: 'Dorian' },
    { value: 'mixolydian', label: 'Mixolydian' },
    { value: 'lydian', label: 'Lydian' },
    { value: 'phrygian', label: 'Phrygian' },
    { value: 'locrian', label: 'Locrian' }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/api/scale', {
        root: root,
        scale_type: scaleType
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
        <i className="fas fa-arrow-up me-2"></i>
        Create Scale
      </h2>

      <Row className="mb-1">
        <Col md={6}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Scale Parameters</h5>
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
                    The root note of the scale
                  </Form.Text>
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Scale Type</Form.Label>
                  <Form.Select
                    value={scaleType}
                    onChange={(e) => setScaleType(e.target.value)}
                  >
                    {scaleTypes.map((type) => (
                      <option key={type.value} value={type.value}>
                        {type.label}
                      </option>
                    ))}
                  </Form.Select>
                  <Form.Text className="text-muted">
                    The type of scale to create
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
                      Creating Scale...
                    </>
                  ) : (
                    <>
                      <i className="fas fa-plus me-2"></i>
                      Create Scale
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
                  Scale Created Successfully
                </h6>
              </Card.Header>
              <Card.Body>
                <div className="text-center mb-3">
                  <div className="display-4 text-primary fw-bold">
                    {result.scale}
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
                    <strong>Type:</strong> {result.scale_type}<br />
                    <strong>Notes Count:</strong> {result.notes.length}
                  </Col>
                  <Col sm={6}>
                    <strong>Full Name:</strong> {result.scale}<br />
                    <strong>Pattern:</strong> {result.notes.join(' - ')}
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
                  title={`Scale: ${result.scale}`}
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
                  title={`Scale: ${result.scale}`}
                />
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}
    </div>
  );
};

export default ScaleTab; 