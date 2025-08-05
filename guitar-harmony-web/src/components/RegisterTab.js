import React, { useState } from 'react';
import { Card, Form, Button, Row, Col, Alert, Spinner, Badge } from 'react-bootstrap';
import axios from 'axios';

const RegisterTab = () => {
  const [registerType, setRegisterType] = useState('note');
  const [registerName, setRegisterName] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [registeredItems, setRegisteredItems] = useState(null);

  const registerTypes = [
    { value: 'note', label: 'Note' },
    { value: 'chord', label: 'Chord' },
    { value: 'scale', label: 'Scale' }
  ];

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/api/register', {
        type: registerType,
        name: registerName
      });

      setResult(response.data);
      setRegisterName('');
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleListItems = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.get('http://localhost:8000/api/register/list');
      setRegisteredItems(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2 className="mb-4">
        <i className="fas fa-bookmark me-2"></i>
        Register Items
      </h2>

      <Row>
        <Col md={6}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Register New Item</h5>
            </Card.Header>
            <Card.Body>
              <Form onSubmit={handleRegister}>
                <Form.Group className="mb-3">
                  <Form.Label>Item Type</Form.Label>
                  <Form.Select
                    value={registerType}
                    onChange={(e) => setRegisterType(e.target.value)}
                  >
                    {registerTypes.map((type) => (
                      <option key={type.value} value={type.value}>
                        {type.label}
                      </option>
                    ))}
                  </Form.Select>
                  <Form.Text className="text-muted">
                    The type of item to register
                  </Form.Text>
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Name</Form.Label>
                  <Form.Control
                    type="text"
                    value={registerName}
                    onChange={(e) => setRegisterName(e.target.value)}
                    placeholder="e.g., C, C maj7, C major"
                  />
                  <Form.Text className="text-muted">
                    The name of the item to register
                  </Form.Text>
                </Form.Group>

                <Button 
                  type="submit" 
                  variant="primary" 
                  disabled={loading || !registerName}
                  className="w-100 mb-3"
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
                      Registering Item...
                    </>
                  ) : (
                    <>
                      <i className="fas fa-save me-2"></i>
                      Register Item
                    </>
                  )}
                </Button>
              </Form>

              <Button 
                variant="secondary" 
                onClick={handleListItems}
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
                    Loading...
                  </>
                ) : (
                  <>
                    <i className="fas fa-list me-2"></i>
                    List Registered Items
                  </>
                )}
              </Button>
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
                  Item Registered Successfully
                </h6>
              </Card.Header>
              <Card.Body>
                <p><strong>Type:</strong> {result.type}</p>
                <p><strong>Message:</strong> {result.message}</p>
              </Card.Body>
            </Card>
          )}

          {registeredItems && (
            <Card className="border-info">
              <Card.Header className="bg-info text-white">
                <h6 className="mb-0">
                  <i className="fas fa-list me-2"></i>
                  Registered Items
                </h6>
              </Card.Header>
              <Card.Body>
                {registeredItems.notes.length > 0 && (
                  <div className="mb-3">
                    <strong>Notes:</strong>
                    <div className="mt-2">
                      {registeredItems.notes.map((note, index) => (
                        <Badge key={index} bg="primary" className="me-2">
                          {note}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                {registeredItems.chords.length > 0 && (
                  <div className="mb-3">
                    <strong>Chords:</strong>
                    <div className="mt-2">
                      {registeredItems.chords.map((chord, index) => (
                        <Badge key={index} bg="success" className="me-2">
                          {chord}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                {registeredItems.scales.length > 0 && (
                  <div className="mb-3">
                    <strong>Scales:</strong>
                    <div className="mt-2">
                      {registeredItems.scales.map((scale, index) => (
                        <Badge key={index} bg="warning" className="me-2">
                          {scale}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                {registeredItems.intervals.length > 0 && (
                  <div className="mb-3">
                    <strong>Intervals:</strong>
                    <div className="mt-2">
                      {registeredItems.intervals.map((interval, index) => (
                        <Badge key={index} bg="info" className="me-2">
                          {interval}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                {registeredItems.notes.length === 0 && 
                 registeredItems.chords.length === 0 && 
                 registeredItems.scales.length === 0 && 
                 registeredItems.intervals.length === 0 && (
                  <p className="text-muted">
                    <em>No items registered yet.</em>
                  </p>
                )}
              </Card.Body>
            </Card>
          )}
        </Col>
      </Row>
    </div>
  );
};

export default RegisterTab; 