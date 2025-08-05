import React, { useState } from 'react';
import { Container, Navbar, Nav } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

import NoteTab from './components/NoteTab';
import ChordTab from './components/ChordTab';
import ScaleTab from './components/ScaleTab';
import IntervalTab from './components/IntervalTab';
import ExerciseTab from './components/ExerciseTab';
import RegisterTab from './components/RegisterTab';

function App() {
  const [activeTab, setActiveTab] = useState('notes');

  return (
    <div className="App">
      {/* Navigation */}
      <Navbar bg="dark" variant="dark" expand="lg" className="mb-4">
        <Container>
          <Navbar.Brand href="#home">
            <i className="fas fa-guitar me-2"></i>
            GuitarHarmony
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ms-auto">
              <Nav.Link 
                active={activeTab === 'notes'} 
                onClick={() => setActiveTab('notes')}
              >
                <i className="fas fa-music me-1"></i>Notes
              </Nav.Link>
              <Nav.Link 
                active={activeTab === 'chords'} 
                onClick={() => setActiveTab('chords')}
              >
                <i className="fas fa-layer-group me-1"></i>Chords
              </Nav.Link>
              <Nav.Link 
                active={activeTab === 'scales'} 
                onClick={() => setActiveTab('scales')}
              >
                <i className="fas fa-arrow-up me-1"></i>Scales
              </Nav.Link>
              <Nav.Link 
                active={activeTab === 'intervals'} 
                onClick={() => setActiveTab('intervals')}
              >
                <i className="fas fa-arrows-alt-h me-1"></i>Intervals
              </Nav.Link>
              <Nav.Link 
                active={activeTab === 'exercises'} 
                onClick={() => setActiveTab('exercises')}
              >
                <i className="fas fa-graduation-cap me-1"></i>Exercises
              </Nav.Link>
              <Nav.Link 
                active={activeTab === 'register'} 
                onClick={() => setActiveTab('register')}
              >
                <i className="fas fa-bookmark me-1"></i>Register
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      {/* Main Content */}
      <Container>
        <div className="content-area">
          {activeTab === 'notes' && <NoteTab />}
          {activeTab === 'chords' && <ChordTab />}
          {activeTab === 'scales' && <ScaleTab />}
          {activeTab === 'intervals' && <IntervalTab />}
          {activeTab === 'exercises' && <ExerciseTab />}
          {activeTab === 'register' && <RegisterTab />}
        </div>

        {/* Footer */}
        <footer className="text-center mt-5 mb-3">
          <p className="text-muted">
            <i className="fas fa-code me-1"></i>
            GuitarHarmony Web Interface v0.5.9
            <br />
            <small>Music Theory and Guitar Learning Library</small>
          </p>
        </footer>
      </Container>
    </div>
  );
}

export default App;
