import React, { useState } from 'react';
import { Card, Form, Button, Row, Col, Alert, Spinner, Badge } from 'react-bootstrap';
import axios from 'axios';

const ExerciseTab = () => {
  const [exerciseType, setExerciseType] = useState('chord_recognition');
  const [count, setCount] = useState(5);
  const [difficulty, setDifficulty] = useState('beginner');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const exerciseTypes = [
    { value: 'chord_recognition', label: 'Chord Recognition' },
    { value: 'scale_construction', label: 'Scale Construction' }
  ];

  const difficulties = [
    { value: 'beginner', label: 'Beginner' },
    { value: 'intermediate', label: 'Intermediate' },
    { value: 'advanced', label: 'Advanced' }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/api/exercise', {
        exercise_type: exerciseType,
        count: count,
        difficulty: difficulty
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
      <h2 className="mb-4">
        <i className="fas fa-graduation-cap me-2"></i>
        Generate Exercises
      </h2>

      <Row>
        <Col md={6}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Exercise Parameters</h5>
            </Card.Header>
            <Card.Body>
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>Exercise Type</Form.Label>
                  <Form.Select
                    value={exerciseType}
                    onChange={(e) => setExerciseType(e.target.value)}
                  >
                    {exerciseTypes.map((type) => (
                      <option key={type.value} value={type.value}>
                        {type.label}
                      </option>
                    ))}
                  </Form.Select>
                  <Form.Text className="text-muted">
                    The type of exercise to generate
                  </Form.Text>
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Number of Exercises</Form.Label>
                  <Form.Control
                    type="number"
                    value={count}
                    onChange={(e) => setCount(parseInt(e.target.value))}
                    min="1"
                    max="20"
                  />
                  <Form.Text className="text-muted">
                    How many exercises to generate (1-20)
                  </Form.Text>
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Difficulty</Form.Label>
                  <Form.Select
                    value={difficulty}
                    onChange={(e) => setDifficulty(e.target.value)}
                  >
                    {difficulties.map((diff) => (
                      <option key={diff.value} value={diff.value}>
                        {diff.label}
                      </option>
                    ))}
                  </Form.Select>
                  <Form.Text className="text-muted">
                    The difficulty level
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
                      Generating Exercises...
                    </>
                  ) : (
                    <>
                      <i className="fas fa-play me-2"></i>
                      Generate Exercises
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
                  Exercises Generated Successfully
                </h6>
              </Card.Header>
              <Card.Body>
                <div className="mb-3">
                  <strong>Type:</strong> {exerciseType.replace('_', ' ').toUpperCase()}<br />
                  <strong>Count:</strong> {result.count}<br />
                  <strong>Difficulty:</strong> {difficulty}
                </div>

                <div className="mt-3">
                  {result.exercises.map((exercise, index) => (
                    <Card key={index} className="mb-3">
                      <Card.Body>
                        <h6 className="card-title">Exercise {index + 1}</h6>
                        <p className="card-text">
                          <strong>Question:</strong> {exercise.question}
                        </p>
                        <div className="text-center">
                          {exercise.notes.map((note, noteIndex) => (
                            <Badge 
                              key={noteIndex} 
                              bg="primary" 
                              className="me-2 fs-6"
                            >
                              {note}
                            </Badge>
                          ))}
                        </div>
                      </Card.Body>
                    </Card>
                  ))}
                </div>
              </Card.Body>
            </Card>
          )}
        </Col>
      </Row>
    </div>
  );
};

export default ExerciseTab; 