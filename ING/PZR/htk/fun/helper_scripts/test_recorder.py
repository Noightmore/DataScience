#!/usr/bin/env python3
import os
import itertools
import numpy as np
import sounddevice as sd
import soundfile as sf

# ----------------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------------
DATA_DIR           = "data"
SAMPLE_RATE        = 16000
PRE_RECORD_DISCARD = 0.1    # secs to drop at start
SILENCE_PADDING    = 0.3    # pad around the speech region
RECORDINGS_PER_SENTENCE = 1 # how many takes per sentence
# ----------------------------------------------------------------------------

# your grammar slots
DISPLAY    = ["ZOBRAZ"]
STOCK      = ["TESLA","APPLE"]
PAST       = ["ZA-POSLEDNI"]
TIMEUNIT   = ["TYDEN","MESIC","ROK"]
IN_INTERVAL= ["V-INTERVALU"]
GRANULARITY= ["DNU","HODIN"]

def generate_sentences():
    for stock, tu, gran in itertools.product(STOCK, TIMEUNIT, GRANULARITY):
        yield f"{DISPLAY[0]} {stock} {PAST[0]} {tu} {IN_INTERVAL[0]} {gran}"

def trim_silence(audio, thresh=0.01):
    frame = int(0.01 * SAMPLE_RATE)
    hop   = frame // 2
    energy = np.array([np.sqrt(np.mean(audio[i:i+frame]**2))
                       for i in range(0, len(audio)-frame, hop)])
    smooth = np.convolve(energy, np.ones(5)/5, mode="same")
    voiced = np.where(smooth>thresh)[0]
    if voiced.size==0:
        return audio, 0, len(audio)
    start = max(0, voiced[0]*hop - int(SILENCE_PADDING*SAMPLE_RATE))
    end   = min(len(audio), voiced[-1]*hop + frame + int(SILENCE_PADDING*SAMPLE_RATE))
    return audio[start:end], start, end

def record_audio(prompt, out_path):
    print(f"\n--- Record: \"{prompt}\"  →  {out_path}")
    input("Press ENTER to start ▶")
    rec_buf = []
    def callback(indata, frames, time, status):
        rec_buf.append(indata.copy())
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback):
        input("Recording... press ENTER to stop ■\n")
    raw = np.concatenate(rec_buf, axis=0).flatten()
    raw = raw[int(PRE_RECORD_DISCARD*SAMPLE_RATE):]
    trimmed, s, e = trim_silence(raw)
    sf.write(out_path, trimmed, SAMPLE_RATE)
    print(f"💾 Saved {out_path}  ({len(trimmed)/SAMPLE_RATE:.2f}s)\n")

def main():
    speaker = input("Enter speaker name: ").strip()
    os.makedirs(speaker, exist_ok=True)

    sentences = list(generate_sentences())
    print(f"\nWill record {len(sentences)} sentences, one take each.\n")

    for sent in sentences:
        for take in range(1, RECORDINGS_PER_SENTENCE+1):
            # safe filename: replace spaces with underscores
            safe = sent.replace(" ", "_")
            fname = f"{speaker}/u{safe}_p{speaker}_s{take}.wav"
            record_audio(sent, fname)

    print("\n✅ All done! You have recordings for every grammar combination.")

if __name__=="__main__":
    main()

