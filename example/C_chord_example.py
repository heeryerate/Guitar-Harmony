############################################################################
# A sample program to create a single-track MIDI file, add a note,
# and write to disk.
############################################################################

from midiutil.MidiFile import MIDIFile

# create your MIDI object
mf = MIDIFile(1)     # only 1 track
track = 0   # the only track

time = 0    # start at the beginning
mf.addTrackName(track, time, "Sample Track")
mf.addTempo(track, time, 120)

# add some notes
channel = 0
volume = 100

pitch = 58           # C4 (middle C)
time = 0             # start on beat 0
duration = 1         # 1 beat long
mf.addNote(track, channel, pitch, time, duration, volume)

pitch = 72          # C4 (middle C)
time = 1             # start on beat 0
duration = 1         # 1 beat long
mf.addNote(track, channel, pitch, time, duration, volume)

pitch = 64           # E4
time = 0             # start on beat 2
duration = 1         # 1 beat long
mf.addNote(track, channel, pitch, time, duration, volume)

pitch = 67           # G4
time = 0             # start on beat 4
duration = 1         # 1 beat long
mf.addNote(track, channel, pitch, time, duration, volume)

base_pitch = 60
for time in range(0, 20, 2):
    pitch_1 = time + 0 + base_pitch
    pitch_2 = time + 4 + base_pitch
    pitch_3 = time + 7 + base_pitch
    pitch_4 = time + 11 + base_pitch
    duration = 0.5
    mf.addNote(track, channel, pitch_1, time, duration, volume)
    mf.addNote(track, channel, pitch_3, time+duration*1, duration, volume)
    mf.addNote(track, channel, pitch_2, time+duration*2, duration, volume)
    mf.addNote(track, channel, pitch_4, time+duration*3, duration, volume)

base_pitch = 40
for time in range(0, 20, 2):
    pitch_1 = time + 0 + base_pitch
    pitch_2 = time + 4 + base_pitch
    pitch_3 = time + 7 + base_pitch
    pitch_4 = time + 11 + base_pitch
    duration = 1.0/5
    mf.addNote(track, channel, pitch_1, time, duration*1, volume)
    mf.addNote(track, channel, pitch_3, time+duration*2, duration, volume)
    mf.addNote(track, channel, pitch_2, time+duration*3, duration, volume)
    mf.addNote(track, channel, pitch_4, time+duration*4, duration, volume)

# write it to disk
with open("output.mid", 'wb') as outf:
    mf.writeFile(outf)