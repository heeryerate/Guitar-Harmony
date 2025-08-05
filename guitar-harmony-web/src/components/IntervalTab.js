import React, { useState } from 'react';
import { Card, Form, Button, Row, Col, Alert, Spinner, Badge } from 'react-bootstrap';
import axios from 'axios';
import AbcMusicStaff from './AbcMusicStaff';
import SimpleMidiPlayer from './SimpleMidiPlayer';

const IntervalTab = () => {
  const [interval, setInterval] = useState('P5');
  const [baseNote, setBaseNote] = useState('C');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const intervals = [
    { value: 'P1', label: 'Perfect Unison (P1)' },
    { value: 'm2', label: 'Minor Second (m2)' },
    { value: 'M2', label: 'Major Second (M2)' },
    { value: 'm3', label: 'Minor Third (m3)' },
    { value: 'M3', label: 'Major Third (M3)' },
    { value: 'P4', label: 'Perfect Fourth (P4)' },
    { value: 'P5', label: 'Perfect Fifth (P5)' },
    { value: 'm6', label: 'Minor Sixth (m6)' },
    { value: 'M6', label: 'Major Sixth (M6)' },
    { value: 'm7', label: 'Minor Seventh (m7)' },
    { value: 'M7', label: 'Major Seventh (M7)' },
    { value: 'P8', label: 'Perfect Octave (P8)' }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/api/interval', {
        interval: interval,
        base: baseNote
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
        <i className="fas fa-arrows-alt-h me-2"></i>
        Create Interval
      </h2>

      <Row className="mb-1">
        <Col md={6}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Interval Parameters</h5>
            </Card.Header>
            <Card.Body>
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>Interval</Form.Label>
                  <Form.Select
                    value={interval}
                    onChange={(e) => setInterval(e.target.value)}
                  >
                    {intervals.map((int) => (
                      <option key={int.value} value={int.value}>
                        {int.label}
                      </option>
                    ))}
                  </Form.Select>
                  <Form.Text className="text-muted">
                    The interval to apply
                  </Form.Text>
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Base Note</Form.Label>
                  <Form.Control
                    type="text"
                    value={baseNote}
                    onChange={(e) => setBaseNote(e.target.value)}
                    placeholder="e.g., C, D, E"
                  />
                  <Form.Text className="text-muted">
                    The starting note
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
                      Creating Interval...
                    </>
                  ) : (
                    <>
                      <i className="fas fa-plus me-2"></i>
                      Create Interval
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
                  Interval Created Successfully
                </h6>
              </Card.Header>
              <Card.Body>
                <div className="text-center mb-3">
                  <div className="display-4 text-primary fw-bold">
                    {result.interval}
                  </div>
                </div>

                <div className="text-center mb-3">
                  <Badge bg="primary" className="me-2 fs-6">
                    {result.base_note}
                  </Badge>
                  <i className="fas fa-arrow-right mx-2 text-muted"></i>
                  <Badge bg="success" className="fs-6">
                    {result.result_note}
                  </Badge>
                </div>

                <Row>
                  <Col sm={6}>
                    <strong>Base Note:</strong> {result.base_note}<br />
                    <strong>Interval:</strong> {result.interval}<br />
                    <strong>Semi-steps:</strong> {result.semi_steps}
                  </Col>
                  <Col sm={6}>
                    <strong>Result Note:</strong> {result.result_note}<br />
                    <strong>Full Name:</strong> {result.interval}
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
                  notes={[result.base_note, result.result_note]} 
                  title={`Interval: ${result.interval}`}
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
                  notes={[result.base_note, result.result_note]} 
                  title={`Interval: ${result.interval}`}
                />
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}
    </div>
  );
};

export default IntervalTab; 