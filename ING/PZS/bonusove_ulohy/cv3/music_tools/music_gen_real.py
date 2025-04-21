import fluidsynth

import time
from ING.PZS.bonusove_ulohy.cv3.music_tools.notes import (demons_souls_theme_bass, dark_souls_theme_notes,
                                                          demons_souls_theme_notes, majula_theme_melody,
                                                          majula_theme_bass, majula_theme_harmony,
                                                          dark_souls_theme_bass)

from ING.PZS.bonusove_ulohy.cv3.music_tools.MusicSynthetiser import apply_rir


# Map note names to their semitone offsets
NOTE_MAP = {
    'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
    'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
    'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
}

def note_name_to_midi(note):
    """
    Convert note name like "C4", "F#3" to MIDI number.
    MIDI 60 = C4.
    """
    base = note[:-1]
    octave = int(note[-1])
    return (octave + 1) * 12 + NOTE_MAP[base]

def render_melody_to_wav(melody,
                         soundfont_path,
                         output_wav,
                         fs=44100,
                         velocity=100,
                         tempo=1.0):
    """
    Render a list of (note_name, duration_seconds) with FluidSynth,
    writing the result to a WAV file, at the given tempo.
      - tempo=1.0 → original speed
      - tempo<1.0 → slower (e.g. 0.5 is half‑speed)
      - tempo>1.0 → faster
    """

    # 1) start up
    synth = fluidsynth.Synth(samplerate=fs)
    # write straight to a file instead of real‑time ALSA:
    synth.start(driver="pulseaudio")

    sfid = synth.sfload(soundfont_path)
    synth.program_select(0, sfid, 0, 0)  # channel, sfid, bank, preset

    # 2) play through your melody
    for note_name, dur in melody:
        midi_num = note_name_to_midi(note_name)

        # “stretched” duration:
        stretched = dur / tempo

        synth.noteon(0, midi_num, velocity)
        time.sleep(stretched)
        synth.noteoff(0, midi_num)

    # 3) clean up
    synth.delete()
    print(f"Wrote {output_wav} at {tempo}× speed")


def play_demons_souls_theme():
    theme = demons_souls_theme_notes()
    bass = demons_souls_theme_bass()


    render_melody_to_wav(
        melody=theme,
        soundfont_path="../FluidR3_GM.sf2",   # ← your .sf2 file here
        output_wav="dark_souls_theme.wav",
        fs=44100,
        tempo=0.2
    )

    # rename file fluidsynth.wav to demons_souls_theme.wav
    import os
    os.rename("fluidsynth.wav", "dark_souls_theme.wav")

    # get bass melody
    render_melody_to_wav(
        melody=bass,
        soundfont_path="../FluidR3_GM.sf2",   # ← your .sf2 file here
        output_wav="dark_souls_theme_bass.wav",
        fs=44100,
        tempo=0.2
    )

    # rename file fluidsynth.wav to demons_souls_theme_bass.wav
    os.rename("fluidsynth.wav", "dark_souls_theme_bass.wav")
    # Mix the two melodies

    # Load the two melodies
    import soundfile as sf
    melody, fs = sf.read("dark_souls_theme.wav")
    bass, fs = sf.read("dark_souls_theme_bass.wav")
    # Ensure both melodies are the same length
    min_len = min(len(melody), len(bass))
    melody = melody[:min_len]
    bass = bass[:min_len]
    # Mix the two melodies
    mix = melody + 0.5 * bass  # Volume balance
    # Save the mixed melody
    sf.write("demons_souls_theme.wav", mix, fs)

    # Apply reverb
    rir_path = "../rirs/RIRS_NOISES/real_rirs_isotropic_noises/air_type1_air_binaural_stairway_1_1_90.wav"
    melody = apply_rir("demons_souls_theme.wav", rir_path, fs=44100)

    # Play the sound
    #import IPython.display as ipd
    #ipd.Audio("fluidsynth.wav")

    # play the sound using sounddevice
    import sounddevice as sd
    import soundfile as sf
    data, fs = sf.read("demons_souls_theme.wav", dtype='float32')
    sd.play(data, fs)

def play_dark_souls_theme():
    theme = dark_souls_theme_notes()
    bass = dark_souls_theme_bass()


    render_melody_to_wav(
        melody=theme,
        soundfont_path="../FluidR3_GM.sf2",   # ← your .sf2 file here
        output_wav="dark_souls_theme.wav",
        fs=44100,
        tempo=0.3
    )

    # rename file fluidsynth.wav to demons_souls_theme.wav
    import os
    os.rename("fluidsynth.wav", "dark_souls_theme.wav")

    # get bass melody
    render_melody_to_wav(
        melody=bass,
        soundfont_path="../FluidR3_GM.sf2",   # ← your .sf2 file here
        output_wav="dark_souls_theme_bass.wav",
        fs=44100,
        tempo=0.3
    )

    # rename file fluidsynth.wav to demons_souls_theme_bass.wav
    os.rename("fluidsynth.wav", "dark_souls_theme_bass.wav")
    # Mix the two melodies

    # Load the two melodies
    import soundfile as sf
    melody, fs = sf.read("dark_souls_theme.wav")
    bass, fs = sf.read("dark_souls_theme_bass.wav")
    # Ensure both melodies are the same length
    min_len = min(len(melody), len(bass))
    melody = melody[:min_len]
    bass = bass[:min_len]
    # Mix the two melodies
    mix = melody + 0.5 * bass  # Volume balance
    # Save the mixed melody
    sf.write("demons_souls_theme.wav", mix, fs)

    # Apply reverb
    rir_path = "../rirs/RIRS_NOISES/real_rirs_isotropic_noises/air_type1_air_binaural_stairway_1_1_90.wav"
    melody = apply_rir("demons_souls_theme.wav", rir_path, fs=44100)

    # Play the sound
    #import IPython.display as ipd
    #ipd.Audio("fluidsynth.wav")

    # play the sound using sounddevice
    import sounddevice as sd
    import soundfile as sf
    data, fs = sf.read("demons_souls_theme.wav", dtype='float32')
    sd.play(data, fs)


def play_majula_theme():
    theme = majula_theme_melody()
    bass = majula_theme_bass()
    harmony = majula_theme_harmony()


    render_melody_to_wav(
        melody=theme,
        soundfont_path="../FluidR3_GM.sf2",   # ← your .sf2 file here
        output_wav="dark_souls_theme.wav",
        fs=44100,
        tempo=0.3
    )

    # rename file fluidsynth.wav to demons_souls_theme.wav
    import os
    os.rename("fluidsynth.wav", "dark_souls_theme.wav")

    # get bass melody
    render_melody_to_wav(
        melody=bass,
        soundfont_path="../FluidR3_GM.sf2",   # ← your .sf2 file here
        output_wav="dark_souls_theme_bass.wav",
        fs=44100,
        tempo=0.1
    )

    # rename file fluidsynth.wav to demons_souls_theme_bass.wav
    os.rename("fluidsynth.wav", "dark_souls_theme_bass.wav")

    # get harmony melody
    render_melody_to_wav(
        melody=harmony,
        soundfont_path="../FluidR3_GM.sf2",   # ← your .sf2 file here
        output_wav="dark_souls_theme_harmony.wav",
        fs=44100,
        tempo=0.1
    )

    # rename file fluidsynth.wav to demons_souls_theme_bass.wav
    os.rename("fluidsynth.wav", "dark_souls_theme_harmony.wav")


    # Load the two melodies
    import soundfile as sf
    melody, fs = sf.read("dark_souls_theme.wav")
    bass, fs = sf.read("dark_souls_theme_bass.wav")
    harmony, fs = sf.read("dark_souls_theme_harmony.wav")
    # Ensure both melodies are the same length
    min_len = min(len(melody), len(bass))
    melody = melody[:min_len]
    bass = bass[:min_len]
    harmony = harmony[:min_len]
    # Mix the two melodies
    mix = melody + 0.5 * bass + 0.5 * harmony  # Volume balance
    # Save the mixed melody
    sf.write("demons_souls_theme.wav", mix, fs)

    # Apply reverb
    rir_path = "../rirs/RIRS_NOISES/real_rirs_isotropic_noises/air_type1_air_binaural_stairway_1_1_90.wav"
    melody = apply_rir("demons_souls_theme.wav", rir_path, fs=44100)

    # Play the sound
    #import IPython.display as ipd
    #ipd.Audio("fluidsynth.wav")

    # play the sound using sounddevice
    import sounddevice as sd
    import soundfile as sf
    data, fs = sf.read("demons_souls_theme.wav", dtype='float32')
    sd.play(data, fs)


if __name__ == '__main__':
    play_demons_souls_theme()
    #play_dark_souls_theme()
    #play_majula_theme()
