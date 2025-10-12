import sys
import time
import re
import threading
import wave
from datetime import datetime
import os

import numpy as np
import sounddevice as sd


SR = 16000          # 16 kHz sample rate
CHANNELS = 1        # mono
DTYPE = 'float32'   # internal recording dtype
EDGE_SILENCE_SEC = 0.5   # required near-silence at start/end
SILENCE_THRESH = 0.01    # abs(amplitude) below this counts as "near-silence"
NOISE_RMS = 0.0002       # very low-level noise for padding (~ inaudible hiss)


def _sanitize_filename(text: str) -> str:
    base = text.strip().lower()
    base = re.sub(r'\s+', '_', base)
    base = re.sub(r'[^a-z0-9_]+', '', base)
    base = base[:60] if base else "recording"
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base}_{stamp}.wav"


def _edge_silence_samples(x: np.ndarray, thresh: float, required: int) -> tuple[int, int]:
    """Return (leading_count, trailing_count) of consecutive 'near-silence' samples."""
    absx = np.abs(x)
    # leading
    lead = 0
    for v in absx:
        if v < thresh:
            lead += 1
            if lead >= required:
                break
        else:
            break
    # trailing
    trail = 0
    for v in absx[::-1]:
        if v < thresh:
            trail += 1
            if trail >= required:
                break
        else:
            break
    return lead, trail


def _pad_with_low_noise(x: np.ndarray, needed_left: int, needed_right: int, noise_rms: float) -> np.ndarray:
    """Pad with low-level Gaussian noise (near silence) so padding isn't true zero."""
    left = np.random.normal(0.0, noise_rms, size=needed_left).astype(x.dtype) if needed_left > 0 else np.empty(0, dtype=x.dtype)
    right = np.random.normal(0.0, noise_rms, size=needed_right).astype(x.dtype) if needed_right > 0 else np.empty(0, dtype=x.dtype)
    return np.concatenate([left, x, right])


def _float_to_int16(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, -1.0, 1.0)
    return (x * 32767.0).astype(np.int16)


def _save_wav_int16_mono(filepath: str, y_int16: np.ndarray, samplerate: int) -> None:
    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(samplerate)
        wf.writeframes(y_int16.tobytes())


def _record_until_enter(samplerate=SR, channels=CHANNELS, dtype=DTYPE) -> np.ndarray:
    """
    Open mic and collect audio frames until the user presses Enter.
    Returns a 1-D float numpy array in range [-1, 1].
    """
    print("\nPress Enter to STOP recording…", flush=True)

    stop_event = threading.Event()
    # Thread that waits for Enter, then signals stop
    def _waiter():
        try:
            input()
        except EOFError:
            pass
        stop_event.set()

    waiter = threading.Thread(target=_waiter, daemon=True)
    waiter.start()

    chunks = []
    lock = threading.Lock()

    def callback(indata, frames, time_info, status):
        if status:
            # Non-fatal warnings from driver/backend
            print(f"[Audio Status] {status}", file=sys.stderr)
        with lock:
            chunks.append(indata.copy())
        if stop_event.is_set():
            raise sd.CallbackStop()

    print("Recording… (speak now)")
    with sd.InputStream(samplerate=samplerate, channels=channels, dtype=dtype, callback=callback):
        while not stop_event.is_set():
            sd.sleep(50)

    # Concatenate all chunks
    with lock:
        if len(chunks) == 0:
            return np.zeros(0, dtype=np.float32)
        data = np.concatenate(chunks, axis=0)

    # Ensure 1-D mono float32
    data = data.reshape(-1, channels).astype(np.float32)
    if channels > 1:
        data = np.mean(data, axis=1)  # downmix to mono if needed
    else:
        data = data[:, 0]
    return data


def record_sentence(sentence: str, output_dir: str = ".") -> None:
    """
    Record a sentence after user prompt, enforce >=0.5 s near-silence at start/end
    (padding with low-level noise if shorter), allow redo, playback for verification,
    and save as 16 kHz, 16-bit mono WAV.

    Parameters
    ----------
    sentence : str
        The text that should be spoken and used to name the file.
    output_dir : str
        Directory where the .wav file will be saved (default: current directory).
    """
    os.makedirs(output_dir, exist_ok=True)

    print("\n==============================")
    print(" Sentence to record:")
    print(f"  \"{sentence}\"")
    print("==============================")
    print("Instructions:")
    print("  1) Prepare your microphone.")
    print("  2) Press Enter to START recording.")
    input("Ready? Press Enter to START… ")

    while True:
        audio = _record_until_enter(SR, CHANNELS, DTYPE)

        if audio.size == 0:
            print("No audio captured. Try again.\n")
            retry = input("Redo recording? [Y/n]: ").strip().lower() or 'y'
            if retry.startswith('y'):
                continue
            else:
                print("Aborted; nothing saved.")
                return

        dur = len(audio) / SR
        print(f"Captured {dur:.2f} seconds.")

        print("Playing back…")
        sd.play(audio, SR)
        sd.wait()

        keep = input("Keep this take? [Y/n]: ").strip().lower() or 'y'
        if keep.startswith('y'):
            break
        print("Okay, let’s try again. Press Enter to START…")
        input()

    required = int(EDGE_SILENCE_SEC * SR)
    lead, trail = _edge_silence_samples(audio, SILENCE_THRESH, required)
    need_left = max(0, required - lead)
    need_right = max(0, required - trail)

    if need_left > 0 or need_right > 0:
        audio = _pad_with_low_noise(audio, need_left, need_right, NOISE_RMS)
        print(f"Added low-level noise padding: left {need_left/SR:.2f}s, right {need_right/SR:.2f}s.")
    else:
        print("Recording already has ≥0.5 s near-silence at both ends.")

    print("Final check (with padded edges)…")
    sd.play(audio, SR)
    sd.wait()

    y16 = _float_to_int16(audio)
    filename = _sanitize_filename(sentence)
    filepath = os.path.join(output_dir, filename)
    _save_wav_int16_mono(filepath, y16, SR)

    print(f"\nSaved: {filepath}")
    print("Done.")

