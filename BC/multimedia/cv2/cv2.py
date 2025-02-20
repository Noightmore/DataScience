import matplotlib.pyplot as plt
import numpy as np
import struct


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

    def read_wav_file(self):
        try:
            with open(self.file_path, 'rb') as file:
                # Read the WAV file header
                header = file.read(44)

                # Check the RIFF header
                if header[:4] != b'RIFF':
                    raise ValueError("Not a valid RIFF file")

                # Get the file size from the header
                file_size = struct.unpack('<I', header[4:8])[0]

                # Check the WAV format
                if header[8:12] != b'WAVE':
                    raise ValueError("Not a valid WAV file")

                # Check the format chunk
                if header[12:16] != b'fmt ':
                    raise ValueError("Missing 'fmt ' chunk")

                # Check the audio format (PCM should be 1)
                audio_format = struct.unpack('<H', header[20:22])[0]
                if audio_format != 1:
                    raise ValueError(f"Unsupported audio format: {audio_format}")

                # Check the number of channels (1 for mono, 2 for stereo)
                self.num_channels = struct.unpack('<H', header[22:24])[0]

                # Check the sample rate (e.g., 44100 Hz)
                self.frame_rate = struct.unpack('<I', header[24:28])[0]

                # Check the byte rate (bytes per second)
                # byte_rate = struct.unpack('<I', header[28:32])[0]
                #
                # # Check the block align (bytes per sample)
                # block_align = struct.unpack('<H', header[32:34])[0]

                # Check the bits per sample (e.g., 16 bits)
                self.sample_width = struct.unpack('<H', header[34:36])[0]

                # Check the data chunk
                if header[36:40] != b'data':
                    raise ValueError("Missing 'data' chunk")

                # Get the data size
                data_size = struct.unpack('<I', header[40:44])[0]

                # Check if data size matches file size
                if data_size != (file_size - 36):
                    raise ValueError("Data size does not match file size")

                # Read the audio data
                self.num_frames = data_size // (self.sample_width * self.num_channels)
                self.audio_data = file.read(data_size)

        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
        except Exception as e:
            print(f"Error: {e}")

    def load_wav_file(self):
        self.read_wav_file()

    def __str__(self):
        return (
            f"File path: {self.file_path}\n"
            f"Sample width: {self.sample_width} bytes\n"
            f"Frame rate: {self.frame_rate} Hz\n"
            f"Number of channels: {self.num_channels}\n"
            f"Number of frames: {self.num_frames}\n"
        )

    def plot_channels(self):
        if self.audio_data is None:
            print("WAV data corrupted or not loaded")
            return

        # Split the audio data into separate channels
        audio_data = np.frombuffer(self.audio_data, dtype=np.int16)
        channels = [audio_data[i::self.num_channels] for i in range(self.num_channels)]

        # Find the length of the longest channel
        max_length = max(len(channel) for channel in channels)

        # Create a time axis (in seconds) for the x-axis
        time_axis = np.linspace(0, max_length / (self.frame_rate * self.num_channels), num=max_length)

        # Plot each channel in a separate graph, padding shorter channels with zeros
        for i, channel_data in enumerate(channels):
            padded_channel_data = np.pad(channel_data, (0, max_length - len(channel_data)), 'constant')
            plt.figure(figsize=(10, 4))
            plt.plot(time_axis, padded_channel_data)
            plt.title(f'Channel {i + 1} - {self.file_path}')
            plt.xlabel('t[s]')
            plt.ylabel('A[-]')
            plt.grid(True)
            plt.show()


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
