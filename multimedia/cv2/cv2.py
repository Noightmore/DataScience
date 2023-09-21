import wave
import matplotlib.pyplot as plt
import numpy as np


class WavFile:
    """
        Class that loads WAV file and provides methods to read and plot it.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.sample_width = None
        self.frame_rate = None
        self.num_channels = None
        self.num_frames = None
        self.audio_data = None

        try:
            self.load_wav_file()
        except Exception as e:
            raise Exception(f"Failed to load WAV file '{file_path}': {str(e)}")

    def load_wav_file(self):
        with wave.open(self.file_path, 'rb') as wav_file:
            self.sample_width = wav_file.getsampwidth()
            self.frame_rate = wav_file.getframerate()
            self.num_channels = wav_file.getnchannels()
            self.num_frames = wav_file.getnframes()
            self.audio_data = wav_file.readframes(self.num_frames)

    def __str__(self):
        return (
            f"File path: {self.file_path}\n"
            f"Sample width: {self.sample_width} bytes\n"
            f"Frame rate: {self.frame_rate} Hz\n"
            f"Number of channels: {self.num_channels}\n"
            f"Number of frames: {self.num_frames}\n"
        )

    def plot_channels(self):
        if self.num_channels == 1:
            self.plot_single_channel()
            plt.grid(True)
            plt.show()
            return None

        if self.num_channels > 1:
            for channel_num in range(self.num_channels):
                plt.figure(figsize=(10, 3))
                plt.title(f'Channel {channel_num + 1}')
                self.plot_single_channel(channel_num)
                plt.tight_layout()
                plt.grid(True)
                plt.show()
            return None

        print("No audio channels found.")

    def plot_single_channel(self, channel_num=0):
        if self.audio_data is None or (self.num_channels <= channel_num or channel_num < 0):
            print(f"Invalid channel number: {channel_num}")
            return None

        audio_data_np = np.frombuffer(self.audio_data, dtype=np.int16)
        channel_data = audio_data_np[channel_num::self.num_channels]
        time = np.arange(0, self.num_frames) / self.frame_rate

        plt.plot(time, channel_data)
        plt.xlabel('t[s]')
        plt.ylabel('A[-]')


def main():

    audio_files = ["cv02_wav_01.wav", "cv02_wav_02.wav",
                   "cv02_wav_03.wav", "cv02_wav_04.wav",
                   "cv02_wav_05.wav", "cv02_wav_06.wav", "cv02_wav_07.wav"]

    for path in audio_files:
        print(f"Loading WAV file '{path}'")

        try:
            wav_loader = WavFile(path)
            print(wav_loader)
            wav_loader.plot_channels()
        except Exception as e:
            print(f"Error: {str(e)}")
        print("--------------------------------------------------")
        print()


if __name__ == "__main__":
    main()
