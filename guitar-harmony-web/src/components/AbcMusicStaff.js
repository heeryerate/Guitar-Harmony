import React, { useEffect, useRef } from 'react';

const AbcMusicStaff = ({ notes, title }) => {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!notes || notes.length === 0) return;

    // Clear previous content
    if (containerRef.current) {
      containerRef.current.innerHTML = '';
    }

    try {
      // Import ABC.js
      const ABCJS = require('abcjs');
      
      // Convert notes to ABC notation
      const abcNotation = convertToAbc(notes);
      console.log('ABC notation:', abcNotation);
      
      // Render the music notation
      ABCJS.renderAbc(containerRef.current, abcNotation, {
        responsive: 'resize',
        scale: 0.6,
        paddingleft: 0,
        paddingright: 0,
        paddingbottom: 0,
        paddingtop: 0
      });
      
    } catch (error) {
      console.error('Error rendering music staff:', error);
      console.error('Error details:', error.message);
      if (containerRef.current) {
        containerRef.current.innerHTML = `
          <div class="text-center p-3">
            <p class="text-muted mb-2">Music Notation</p>
            <div class="border rounded p-2 bg-light">
              <strong>Notes:</strong> ${notes.join(', ')}
            </div>
            <small class="text-muted">Error: ${error.message}</small>
          </div>
        `;
      }
    }
  }, [notes, title]);

  // Convert notes to ABC notation
  const convertToAbc = (notes) => {
    const noteMap = {
      'C': 'C', 'C#': '^C', 'Db': '_D',
      'D': 'D', 'D#': '^D', 'Eb': '_E',
      'E': 'E', 'F': 'F', 'F#': '^F', 'Gb': '_G',
      'G': 'G', 'G#': '^G', 'Ab': '_A',
      'A': 'A', 'A#': '^A', 'Bb': '_B',
      'B': 'B'
    };

    // Convert each note to ABC format
    const abcNotes = notes.map(note => {
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
      return noteMap[noteName] || note;
    });

    // Remove duplicates and sort notes to ensure root is at bottom (lowest pitch)
    const uniqueNotes = [...new Set(abcNotes)];
    const sortedNotes = uniqueNotes.sort((a, b) => {
      const noteOrder = ['C', 'D', 'E', 'F', 'G', 'A', 'B'];
      const aIndex = noteOrder.indexOf(a.replace(/[^A-Z]/g, ''));
      const bIndex = noteOrder.indexOf(b.replace(/[^A-Z]/g, ''));
      return aIndex - bIndex;
    });

    // Create ABC notation string
    const abcString = `
X:1
T:${title || 'Music'}
M:4/4
L:1/4
K:C
${sortedNotes.join(' ')}
    `.trim();

    return abcString;
  };

  return (
    <div className="music-staff-container">
      <div ref={containerRef} className="music-staff"></div>
    </div>
  );
};

export default AbcMusicStaff; 