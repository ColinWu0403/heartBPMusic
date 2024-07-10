import random
from midiutil import MIDIFile

def create_drum_loop(bpm, length=4, drum_midi_path="midi/drum_loop.mid"):
    midi = MIDIFile(1)
    track = 0
    time = 0
    midi.addTrackName(track, time, "Drum Track")
    midi.addTempo(track, time, bpm)
    
    drum_channel = 9  # MIDI channel 10 for drums
    for i in range(length * 4):
        midi.addNote(track, drum_channel, 36, time + i * (60 / bpm / 4), 0.5, 100)  # Bass drum on each beat
        if i % 2 == 0:
            midi.addNote(track, drum_channel, 38, time + i * (60 / bpm / 4), 0.5, 100)  # Snare on every 2nd beat
    
    with open(drum_midi_path, "wb") as output_file:
        midi.writeFile(output_file)


def create_melody(bpm, length=4, scale="C major", melody_midi_path="midi/melody.mid"):
    midi = MIDIFile(1)
    track = 0
    time = 0
    midi.addTrackName(track, time, "Melody Track")
    midi.addTempo(track, time, bpm)
    
    melody_channel = 0
    notes = {
        "C major": [60, 62, 64, 65, 67, 69, 71, 72],
        "A minor": [57, 59, 60, 62, 64, 65, 67, 69]
    }
    
    scale_notes = notes[scale]
    
    for i in range(length * 4):
        note = random.choice(scale_notes)
        duration = random.choice([0.25, 0.5, 1])
        midi.addNote(track, melody_channel, note, time + i * (60 / bpm / 4), duration, 100)

    with open(melody_midi_path, "wb") as output_file:
        midi.writeFile(output_file)
