# GuitarHarmony Web Interface

A modern React web interface for the GuitarHarmony music theory library.

## Features

- **Notes**: Create and display musical notes with properties
- **Chords**: Build chords with different types (major, minor, 7th, etc.)
- **Scales**: Generate various scale types (major, minor, modes)
- **Intervals**: Apply intervals to base notes
- **Exercises**: Generate music theory exercises
- **Register**: Save and manage musical items
- **Music Notation**: Visual staff display using VexFlow
- **MIDI Playback**: Audio playback using Tone.js

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Python 3.7+ with GuitarHarmony library

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. The app will open in your browser at `http://localhost:3000`

### API Server

The React app communicates with a FastAPI backend. To start the API server:

```bash
# From the parent directory
python api_server.py
```

The API server runs on `http://localhost:8000`

## Usage

1. **Notes Tab**: Create notes by entering a note name (e.g., C, F#, Ab) and duration
2. **Chords Tab**: Build chords by selecting a root note and chord type
3. **Scales Tab**: Generate scales by choosing a root note and scale type
4. **Intervals Tab**: Apply intervals to base notes
5. **Exercises Tab**: Generate music theory exercises with different types and difficulties
6. **Register Tab**: Save and manage your favorite musical items

## Development

### Available Scripts

- `npm start`: Start the development server
- `npm run build`: Build the app for production
- `npm test`: Run tests
- `npm run eject`: Eject from Create React App (irreversible)

### Project Structure

```
src/
├── components/          # React components
│   ├── NoteTab.js      # Notes functionality
│   ├── ChordTab.js     # Chords functionality
│   ├── ScaleTab.js     # Scales functionality
│   ├── IntervalTab.js  # Intervals functionality
│   ├── ExerciseTab.js  # Exercises functionality
│   └── RegisterTab.js  # Register functionality
├── App.js              # Main app component
├── App.css             # Custom styles
└── index.js            # App entry point
```

## API Endpoints

The web interface communicates with the following API endpoints:

- `POST /api/note`: Create a note
- `POST /api/chord`: Create a chord
- `POST /api/scale`: Create a scale
- `POST /api/interval`: Create an interval
- `POST /api/exercise`: Generate exercises
- `POST /api/register`: Register an item
- `GET /api/register/list`: List registered items
- `GET /api/options`: Get available options

## Technologies Used

- **React**: Frontend framework
- **React Bootstrap**: UI components
- **Axios**: HTTP client for API calls
- **Font Awesome**: Icons
- **FastAPI**: Backend API (separate server)
- **VexFlow**: Music notation rendering
- **Web Audio API**: Native browser audio for reliable playback

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the GuitarHarmony library and follows the same license.
