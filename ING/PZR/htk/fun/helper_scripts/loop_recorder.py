#!/usr/bin/env python3
import os
import queue
import numpy as np
import sounddevice as sd
import soundfile as sf
import time
from datetime import datetime

# Configuration
DATA_DIR = "recordings"
SAMPLE_RATE = 16000
CHANNELS = 1
MAX_SILENCE = 2.0     # Max allowed silence (seconds) between speech chunks
SILENCE_THRESH = 0.01 # Energy threshold for speech
SILENCE_PADDING = 0.3 # Padding before/after detected speech (seconds)
MIN_SENTENCE_LEN = 0.6  # Minimum length of a sentence to keep (seconds)

os.makedirs(DATA_DIR, exist_ok=True)

def energy(audio):
    """Calculate short-term energy of audio buffer."""
    return np.sqrt(np.mean(np.square(audio)))

def trim_silence(audio, thresh, padding_sec, sample_rate):
    frame = int(0.01 * sample_rate)
    hop = frame // 2
    energy = np.array([np.sqrt(np.mean(audio[i:i+frame]**2)) 
                       for i in range(0, len(audio)-frame, hop)])
    smooth = np.convolve(energy, np.ones(5)/5, mode="same")
    voiced = np.where(smooth > thresh)[0]
    if voiced.size == 0:
        return audio, 0, len(audio)
    start = max(0, voiced[0]*hop - int(padding_sec*sample_rate))
    end = min(len(audio), voiced[-1]*hop + frame + int(padding_sec*sample_rate))
    return audio[start:end], start, end

def record_sentence():
    """Continuously records from mic, waits for speech, then records until long silence, returns the audio."""
    q = queue.Queue()
    rec = []
    silence_timer = None
    is_recording = False
    print("Listening for speech... (ctrl+c to exit)")
    
    def callback(indata, frames, time_info, status):
        q.put(indata.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback, dtype="float32"):
        while True:
            indata = q.get()
            mono = indata[:,0]
            e = energy(mono)
            if is_recording:
                rec.append(mono)
                if e > SILENCE_THRESH:
                    silence_timer = time.time()
                else:
                    # If we've been silent for MAX_SILENCE seconds, stop
                    if silence_timer and (time.time() - silence_timer) > MAX_SILENCE:
                        print("Detected end of sentence.")
                        break
            else:
                # Not yet started: wait for speech
                if e > SILENCE_THRESH:
                    print("Speech detected! Recording...")
                    is_recording = True
                    rec.append(mono)
                    silence_timer = time.time()

    audio = np.concatenate(rec)
    return audio

def save_sentence(audio, sample_rate, out_dir):
    # Trim silence at start/end
    trimmed, _, _ = trim_silence(audio, SILENCE_THRESH, SILENCE_PADDING, sample_rate)
    # Skip very short sentences
    if len(trimmed)/sample_rate < MIN_SENTENCE_LEN:
        print("Skipped: too short.")
        return
    # Unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"sentence_{timestamp}.wav"
    out_path = os.path.join(out_dir, fname)
    sf.write(out_path, trimmed, sample_rate)
    print(f"Saved: {out_path} ({len(trimmed)/sample_rate:.2f}s)")

def main():
    print("Sentence recorder started.")
    while True:
        audio = record_sentence()
        save_sentence(audio, SAMPLE_RATE, DATA_DIR)
        print("Ready for next sentence.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting.")


