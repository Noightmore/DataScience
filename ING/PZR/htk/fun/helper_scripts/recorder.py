import os
import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt

data_folder = "data"

# SETTINGS
WORDS = ["ZOBRAZ", "TESLA", "APPLE", "ZA", "POSLEDNI", "TYDEN", "MESIC", "ROK", "V",
         "INTERVALU", "DNU", "HODIN"]
RECORDINGS_PER_WORD = 1
SAMPLE_RATE = 16000  # 16kHz
SILENCE_PADDING = 0.3  # 0.5 seconds of silence at start and end
PRE_RECORD_DISCARD = 0 # Discard first 100ms

def trim_silence(audio, threshold=0.01):
    frame_size = int(0.01 * SAMPLE_RATE)  # 10ms frames
    hop_size = frame_size // 2  # Overlap
    energy = np.array([
        np.sqrt(np.mean(audio[i:i+frame_size]**2))
        for i in range(0, len(audio) - frame_size, hop_size)
    ])

    # Smooth the energy (moving average)
    window = 5  # frames
    smooth_energy = np.convolve(energy, np.ones(window)/window, mode='same')

    speech_frames = np.where(smooth_energy > threshold)[0]

    if len(speech_frames) == 0:
        return audio, 0, len(audio)  # No speech detected

    start = max(0, speech_frames[0] * hop_size - int(SILENCE_PADDING * SAMPLE_RATE))
    end = min(len(audio), speech_frames[-1] * hop_size + frame_size + int(SILENCE_PADDING * SAMPLE_RATE))

    return audio[start:end], start, end


def plot_waveform(audio, trimmed_start, trimmed_end):
    time_axis = np.linspace(0, len(audio) / SAMPLE_RATE, len(audio))
    plt.figure(figsize=(10, 4))
    plt.plot(time_axis, audio, label="Original", color="gray")

    # Highlight trimmed section
    plt.axvspan(trimmed_start / SAMPLE_RATE, trimmed_end / SAMPLE_RATE, color="cyan", alpha=0.3, label="Trimmed section")

    plt.title("Waveform with Trimmed Section")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def record_audio(filename):
    print(f"\nReady to record: {filename}")
    input("Press ENTER to start recording...")
    print("Recording... Press ENTER again to stop.")

    recording = []

    def callback(indata, frames, time, status):
        recording.append(indata.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback):
        input()  # ENTER to stop

    audio = np.concatenate(recording, axis=0).flatten()

    # Discard first 100ms to avoid spikes
    discard_samples = int(PRE_RECORD_DISCARD * SAMPLE_RATE)
    audio = audio[discard_samples:]

    # Trim silence
    trimmed_audio, start, end = trim_silence(audio)

    # Playback trimmed
    print(f"▶️ Playing trimmed ({len(trimmed_audio)/SAMPLE_RATE:.2f} sec)...")
    sd.play(trimmed_audio, SAMPLE_RATE)
    sd.wait()

    # Save
    sf.write(filename, trimmed_audio, SAMPLE_RATE)
    full_path = os.path.abspath(filename)
    print(f"💾 Saved: {full_path}")


# Plot
    plot_waveform(audio, start, end)


def main():
    person = input("Enter speaker name (person): ").strip()
    os.makedirs(person, exist_ok=True)

    for word in WORDS:
        for series_num in range(1, RECORDINGS_PER_WORD + 1):
            filename = f"{person}/w{word}_p{person}_s{series_num}.wav"
            record_audio(filename)

    print("\n✅ All recordings done!")

if __name__ == "__main__":
    main()
