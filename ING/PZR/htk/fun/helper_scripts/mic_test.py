import sounddevice as sd
import soundfile as sf
import plotext as plt
import numpy as np

SAMPLE_RATE = 16000
DURATION = 5

print("🎤 Mic test (Terminal Plot): Recording for 5 seconds...")
input("Press ENTER to start...")

recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
sd.wait()

print("✅ Recording complete! Playing back...")
sd.play(recording, samplerate=SAMPLE_RATE)
sd.wait()

sf.write("mic_test.wav", recording, SAMPLE_RATE)

# Terminal plot
samples = recording.flatten()
downsampled = samples[::100]  # Downsample for terminal display
plt.plot(downsampled)
plt.title("Mic Test Waveform (Terminal)")
plt.show()

