# Souls Menu Theme Synthesizer
import numpy as np
import soundfile as sf
import scipy.signal as signal
from scipy.signal import butter, lfilter


def note_name_to_freq(note_name):
    """Convert note name like 'A4' or 'C#3' to frequency in Hz."""
    note_names = ["C", "C#", "D", "D#", "E", "F",
                  "F#", "G", "G#", "A", "A#", "B"]
    enharmonics = {"Db": "C#", "Eb": "D#", "Gb": "F#",
                   "Ab": "G#", "Bb": "A#"}

    name = note_name[:-1]
    octave = int(note_name[-1])

    # Convert flats to sharps
    if name in enharmonics:
        name = enharmonics[name]

    semitone = note_names.index(name)
    midi = (octave + 1) * 12 + semitone
    freq = 440.0 * 2 ** ((midi - 69) / 12)

    return freq


def generate_multi_octave_scale(instrument="guitar", fs=16000, duration=1.0, octave_range=3, base_note="C", base_octave=3):
    """
    Generate 12-tone chromatic scale across multiple octaves using Karplus-Strong synthesis.
    Supports both sharps (#) and flats (b) as enharmonic equivalents.
    """

    # Enharmonic mapping
    enharmonics = {
        "C#": "Db", "Db": "C#",
        "D#": "Eb", "Eb": "D#",
        "F#": "Gb", "Gb": "F#",
        "G#": "Ab", "Ab": "G#",
        "A#": "Bb", "Bb": "A#"
    }

    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note_index = {name: i for i, name in enumerate(note_names)}
    base_midi = (base_octave + 1) * 12 + note_index[base_note]

    def midi_to_freq(midi_num):
        return 440.0 * (2 ** ((midi_num - 69) / 12))

    def lowpass(signal, cutoff, fs, order=4):
        b, a = butter(order, cutoff / (0.5 * fs), btype='low')
        return lfilter(b, a, signal)

    def karplus_strong(freq, duration, fs=16000, decay=0.996, style="guitar"):
        N = int(fs / freq)
        if N < 2:
            return np.zeros(int(fs * duration))

        # Excitation
        if style == "guitar":
            excitation = np.random.uniform(-1, 1, N)
            if freq < 100:
                excitation = np.convolve(excitation, np.ones(10)/10, mode='same')
        elif style == "piano":
            excitation = np.exp(-np.linspace(0, 4, N)) * np.random.uniform(-1, 1, N)
        else:
            raise ValueError("Unsupported instrument type.")

        output = np.zeros(int(fs * duration))
        output[:N] = excitation

        if freq < 150:
            decay *= 0.98

        for i in range(N, len(output)):
            output[i] = decay * 0.5 * (output[i - N] + output[i - N - 1])

        if style == "piano":
            output *= np.hanning(len(output))

        # 🎯 Filter only the attack region for low notes
        if freq < 150:
            dynamic_cutoff = min(3.5 * freq, 600)
            attack_len = int(fs * 0.1)
            if attack_len < len(output):
                filtered_attack = lowpass(output[:attack_len], cutoff=dynamic_cutoff, fs=fs)
                output[:attack_len] = filtered_attack
            output *= 0.8  # optional: reduce volume of bass slightly

        return output

    tones = {}
    for i in range(octave_range * 12):
        midi_num = base_midi + i
        freq = midi_to_freq(midi_num)
        name = note_names[midi_num % 12]
        octave = (midi_num // 12) - 1
        note = name + str(octave)

        tone = karplus_strong(freq, duration, fs, style=instrument)
        tones[note] = tone

        # Add enharmonic alias
        if name in enharmonics:
            enh_name = enharmonics[name] + str(octave)
            tones[enh_name] = tone

    return tones, fs



    tones = {}
    for i in range(octave_range * 12):
        midi_num = base_midi + i
        freq = midi_to_freq(midi_num)

        # Canonical note name (using sharps)
        name = note_names[midi_num % 12]
        octave = (midi_num // 12) - 1
        note = name + str(octave)

        # Generate waveform once
        tone = karplus_strong(freq, duration, fs, style=instrument)

        # Add canonical name
        tones[note] = tone

        # Add enharmonic equivalent if exists (e.g., also "Db4" for "C#4")
        if name in enharmonics:
            enh_name = enharmonics[name] + str(octave)
            tones[enh_name] = tone  # alias to same waveform

    return tones, fs




# -----------------------------
# Concatenate melody
# -----------------------------
def synthesize_melody(tones, fs, melody_notes, base_duration=1.0, fade_ratio=0.1):
    """
    Concatenate tones into a melody with smooth fade-ins and fade-outs.
    Applies Hann window to each note and ensures zero-crossing transitions.
    """
    melody = []
    prev_tone_end = None

    for note_name, length_factor in melody_notes:
        tone = tones[note_name]
        total_samples = int(fs * base_duration * length_factor)

        # Trim or pad tone to target length
        if len(tone) > total_samples:
            tone = tone[:total_samples]
        else:
            tone = np.pad(tone, (0, total_samples - len(tone)))

        # Apply fade-in/out using Hann window
        fade_len = int(total_samples * fade_ratio)
        if fade_len > 0 and fade_len * 2 < total_samples:
            fade_window = np.hanning(fade_len * 2)
            fade_in = fade_window[:fade_len]
            fade_out = fade_window[fade_len:]
            tone[:fade_len] *= fade_in
            tone[-fade_len:] *= fade_out

        # Optional: crossfade overlap with previous note (anti-click)
        if prev_tone_end is not None and fade_len > 0:
            overlap = min(fade_len, len(prev_tone_end), len(tone))
            tone[:overlap] += prev_tone_end[-overlap:]
            melody.append(prev_tone_end[:-overlap])
        elif prev_tone_end is not None:
            melody.append(prev_tone_end)

        prev_tone_end = tone

    if prev_tone_end is not None:
        melody.append(prev_tone_end)

    return np.concatenate(melody)



# -----------------------------
# rir applier
# -----------------------------
# rir noise origin: https://www.openslr.org/28/
def apply_rir(signal_in, rir_path, fs):
    rir, rir_fs = sf.read(rir_path)
    if rir_fs != fs:
        raise ValueError(f"RIR sampling rate {rir_fs} must match melody rate {fs}")

    if rir.ndim == 1:
        # Mono RIR
        return signal.fftconvolve(signal_in, rir, mode='full')
    elif rir.ndim == 2:
        # Stereo RIR (left and right)
        left = signal.fftconvolve(signal_in, rir[:, 0], mode='full')
        right = signal.fftconvolve(signal_in, rir[:, 1], mode='full')
        return np.stack([left, right], axis=1)
    else:
        raise ValueError("Unsupported RIR format")

