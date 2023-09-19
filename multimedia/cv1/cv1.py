import wave
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display


def read_wav_header(wav_file):
    with wave.open(wav_file, 'rb') as wf:
        print("WAV File Header Information:")
        print("---------------------------")
        for key, value in wf.getparams()._asdict().items():
            print(f"{key.capitalize()}: {value}")


def plot_wav_file(wav_file):
    # Read audio data
    with wave.open(wav_file, 'rb') as wf:
        audio_data = wf.readframes(-1)
        audio_data = np.frombuffer(audio_data, dtype=np.int16)

        # Plot the audio signal
        plt.figure(figsize=(10, 4))
        plt.plot(audio_data)
        plt.title('Audio Signal')
        plt.xlabel('Sample')
        plt.ylabel('Amplitude')
        plt.grid(True)
        plt.show()


def plot_spectogram(wav_file):
    y, sr = librosa.load(wav_file)

    # Create a spectrogram
    d = librosa.amplitude_to_db(librosa.stft(y), ref=np.max)  # Short-Time Fourier Transform (STFT)

    # Display the spectrogram
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(d, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.show()


if __name__ == "__main__":
    my_wav_file = "audi.wav"  # Replace with the path to your .wav file
    read_wav_header(my_wav_file)
    plot_wav_file(my_wav_file)
    plot_spectogram(my_wav_file)
