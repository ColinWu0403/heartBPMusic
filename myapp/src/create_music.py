from myapp.src.arrange_music import create_drum_loop, create_melody
import pretty_midi
import subprocess, os

def merge_midi_files(drum_midi_path, melody_midi_path, output_midi_path):
    # Load the MIDI files
    drum_midi = pretty_midi.PrettyMIDI(drum_midi_path)
    melody_midi = pretty_midi.PrettyMIDI(melody_midi_path)

    # Create a new MIDI file for the merged output
    merged_midi = pretty_midi.PrettyMIDI()

    # Add the tracks from the drum MIDI file to the merged MIDI file
    for instrument in drum_midi.instruments:
        merged_midi.instruments.append(instrument)

    # Add the tracks from the melody MIDI file to the merged MIDI file
    for instrument in melody_midi.instruments:
        merged_midi.instruments.append(instrument)

    # Save the merged MIDI file
    merged_midi.write(output_midi_path)


def render_midi_to_audio(midi_file_path, soundfont_path, output_audio_path):
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_audio_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Command to convert MIDI to WAV using timidity
    command = [
        'timidity', midi_file_path,
        '-Ow', '-o', output_audio_path,
        '-s', '44100',
        '--output-stereo'
    ]
    subprocess.run(command, check=True)

def generate_music_and_render(bpm, soundfont_path, output_audio_path):
    # Paths to save the individual and merged MIDI files
    drum_midi_path = 'midi/drum_loop.mid'
    melody_midi_path = 'midi/melody.mid'
    merged_midi_path = 'midi/merged.mid'

    # Generate the drum loop and melody MIDI files
    create_drum_loop(bpm, 4, drum_midi_path)
    create_melody(bpm, 4, "C major", melody_midi_path)

    # Merge the MIDI files
    merge_midi_files(drum_midi_path, melody_midi_path, merged_midi_path)

    # Render the merged MIDI file to an audio file
    render_midi_to_audio(merged_midi_path, soundfont_path, output_audio_path)

# Example usage
bpm = 120
soundfont_path = '/soundfonts/FluidR3_GM/FluidR3_GM.sf2'
output_audio_path = '/output/'
generate_music_and_render(bpm, soundfont_path, output_audio_path)