import wave
import numpy as np
import matplotlib.pyplot as plt
import struct


def read_wav_header(wav_file):
    with wave.open(wav_file, 'rb') as wf:
        print("WAV File Header Information:")
        print("---------------------------")
        for key, value in wf.getparams()._asdict().items():
            print(f"{key.capitalize()}: {value}")

    print("---------------------------------")


def plot_wav_file(wav_file):
    # with open('cv01_dobryden.wav', 'rb') as f:
    # # head
    # data = f.read(4)
    # print(data)
    # A1 = struct.unpack('i', f.read(4))[0]
    # print(A1)

    # Open the WAV file for binary reading
    with open('cv01_dobryden.wav', 'rb') as f:
        riff_identifier = f.read(4)
        print(f"riff: {riff_identifier.decode()}")

        file_size = struct.unpack('<I', f.read(4))[0]
        print(f"A1: {file_size} bytes")

        wave_format = f.read(4)
        print(f"WAVE retezec: {wave_format.decode()}")

        fmt_subchunk_header = f.read(4)
        print(f"'fmt ' retezec: {fmt_subchunk_header.decode()}")

        fmt_subchunk_size = struct.unpack('<I', f.read(4))[0]
        print(f"AF: {fmt_subchunk_size} bytes")

        audio_format = struct.unpack('<H', f.read(2))[0]
        print(f"K: {audio_format}")

        num_channels = struct.unpack('<H', f.read(2))[0]
        print(f"C: {num_channels}")

        sample_rate = struct.unpack('<I', f.read(4))[0]
        print(f"VF: {sample_rate} Hz")

        byte_rate = struct.unpack('<I', f.read(4))[0]
        print(f"PB: {byte_rate} bytes/second")

        block_align = struct.unpack('<H', f.read(2))[0]
        print(f"VB: {block_align} bytes")

        bits_per_sample = struct.unpack('<H', f.read(2))[0]
        print(f"VV: {bits_per_sample} bits")

        data_subchunk_header = f.read(4)
        print(f"'retezec data': {data_subchunk_header.decode()}")

        data_subchunk_size = struct.unpack('<I', f.read(4))[0]
        print(f"A2: {data_subchunk_size} bytes")

        audio_data = np.frombuffer(f.read(data_subchunk_size), dtype=np.uint8)

    # delka audia
    audio_duration = len(audio_data) / (sample_rate * num_channels * (bits_per_sample // 8))

    t = np.linspace(0, audio_duration, len(audio_data))

    # Plot the audio signal
    plt.figure(figsize=(10, 4))
    plt.plot(t, audio_data)
    plt.title('Audio Signal')
    plt.xlabel('t[s]')
    plt.ylabel('A[-]')
    plt.grid(True)
    plt.show()


# def plot_spectogram(wav_file):
#     y, sr = librosa.load(wav_file)
#
#     # Create a spectrogram
#     d = librosa.amplitude_to_db(librosa.stft(y), ref=np.max)  # Short-Time Fourier Transform (STFT)
#
#     # Display the spectrogram
#     plt.figure(figsize=(10, 6))
#     librosa.display.specshow(d, sr=sr, x_axis='time', y_axis='log')
#     plt.colorbar(format='%+2.0f dB')
#     plt.title('Spectrogram')
#     plt.show()


if __name__ == "__main__":
    my_wav_file = "cv01_dobryden.wav"  # Replace with the path to your .wav file
    read_wav_header(my_wav_file)
    plot_wav_file(my_wav_file)
    #plot_spectogram(my_wav_file)
