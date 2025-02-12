import os
import numpy as np
import simpleaudio as sa
from datetime import datetime
import av
from pathlib import Path
from pydub.silence import detect_nonsilent
import plotly.graph_objects as go
from pydub import AudioSegment
import shutil
from huggingface_hub import snapshot_download

RECORDINGS_DIR = "./recordings"
RECORDINGS_DIR = Path(RECORDINGS_DIR)
dataset_name = "night12/czech_time_shards_recordings"


def download_recordings():
    os.makedirs(RECORDINGS_DIR, exist_ok=True)

    # Download all files from the dataset repository
    downloaded_path = snapshot_download(dataset_name, local_dir=RECORDINGS_DIR, repo_type="dataset")

    print(f"Dataset downloaded to: {downloaded_path}")


def plot_waveform(audio_segment, title="Waveform"):
    """ Visualize the waveform using Plotly """
    samples = np.array(audio_segment.get_array_of_samples(), dtype=np.int16)
    time_axis = np.linspace(0, len(samples) / audio_segment.frame_rate, num=len(samples))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_axis, y=samples, mode="lines", name="Waveform"))
    fig.update_layout(title=title, xaxis_title="Time (seconds)", yaxis_title="Amplitude")
    fig.show()


def load_opus_with_pyav(file_path):
    """ Load Opus file and return raw PCM data as AudioSegment """
    try:
        container = av.open(file_path)
        stream = next(s for s in container.streams if s.type == 'audio')

        audio_frames = []
        sample_rate = stream.sample_rate
        num_channels = stream.channels or 1  # Default to mono if not specified

        for frame in container.decode(stream):
            frame_data = frame.to_ndarray()

            # Debug: Print frame shape and dtype
            #print(f"Decoded frame shape: {frame_data.shape}, dtype: {frame_data.dtype}")

            # Convert stereo to mono if necessary
            if frame_data.ndim > 1:
                frame_data = np.mean(frame_data, axis=0)  # Convert to mono by averaging channels

            # Convert float32 data to int16 PCM (sound card expects this)
            if frame_data.dtype == np.float32:
                frame_data = (frame_data * 32767).astype(np.int16)

            audio_frames.append(frame_data)

        if not audio_frames:
            raise ValueError(f"❌ No valid audio frames in {file_path}")

        # Concatenate all frames into a single NumPy array
        audio_data = np.concatenate(audio_frames).astype(np.int16)

        # Debug: Print sample statistics
        #print(f"Audio data stats - min: {audio_data.min()}, max: {audio_data.max()}, mean: {audio_data.mean()}")

        # Convert NumPy array to raw PCM byte stream
        pcm_bytes = audio_data.tobytes()

        # Wrap PCM bytes in BytesIO and create a pydub AudioSegment
        audio_segment = AudioSegment(
            data=pcm_bytes,
            sample_width=2,  # 16-bit PCM
            frame_rate=sample_rate,
            channels=num_channels
        )

        return audio_segment

    except Exception as e:
        raise RuntimeError(f"❌ Error decoding {file_path}: {e}")


# Function to flatten the nested list
def flatten_list(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list


def pick_correct_recordings_by_time(time_input, recordings_folder):
    # split time into hours and minutes, forget seconds
    hours = int(time_input.hour)
    minutes = int(time_input.minute)

    announcer = recordings_folder / "je_prave.opus"
    hour_desc_file = None
    minute_desc_file = None
    hour_val = []
    minute_val = []

    if hours in (2,3,4):
        announcer = recordings_folder / "jsou_prave.opus"

    if hours == 1:
        hour_desc_file = recordings_folder / f"hodina.opus"
    elif 5 > hours > 1:
        hour_desc_file = recordings_folder / f"hodiny.opus"
    else:
        hour_desc_file = recordings_folder / f"hodin.opus"

    if hours == 2:
        hour_val.append(recordings_folder / f"dve.opus")
    elif hours < 20:
        hour_val.append(recordings_folder / f"{hours}.opus")
    else:
        hour_val.append(recordings_folder / f"{hours - hours % 10}.opus")
        if hours % 10 != 0:
            hour_val.append(recordings_folder / f"{hours % 10}.opus")

    if minutes == 1:
        minute_desc_file = recordings_folder / f"minuta.opus"
    elif minutes == 0:
        minute_desc_file = recordings_folder / f"silence.opus"
    elif 5 > minutes > 1:
        minute_desc_file = recordings_folder / f"minuty.opus"
    else:
        minute_desc_file = recordings_folder / f"minut.opus"

    if minutes == 0:
        minute_val = []
    elif minutes == 2:
        minute_val.append(recordings_folder / f"dve.opus")
    elif minutes < 20:
        minute_val.append(recordings_folder / f"{minutes}.opus")
    else:
        if minutes % 10 == 0:
            minute_val.append(recordings_folder / f"{minutes}.opus")
        else:
            minute_val.append(recordings_folder / f"{minutes - minutes % 10}.opus")
            if minutes % 10 != 0:
                minute_val.append(recordings_folder / f"{minutes % 10}.opus")


    #print(hours, minutes)
    #print(hour_val, hour_desc_file)
    #print(minute_val, minute_desc_file)

    return announcer, hour_val, hour_desc_file, minute_val, minute_desc_file
    # returns a list of paths to the recordings


def play_audio(audio_segment):
    """ Play an AudioSegment object directly from RAM """
    samples = np.array(audio_segment.get_array_of_samples(), dtype=np.int16)

    # Normalize PCM data if stereo
    if audio_segment.channels == 2:
        samples = samples.reshape((-1, 2))

    # Debug: Check if samples contain valid audio
    #print(f"Playback samples min: {samples.min()}, max: {samples.max()}")

    # Play using simpleaudio
    sa.play_buffer(samples, num_channels=audio_segment.channels, bytes_per_sample=2, sample_rate=audio_segment.frame_rate).wait_done()


def boost_audio(audio_segment, factor=3):
    """ Boost the audio volume by a given factor. """

    # Convert factor to decibels (logarithmic scale)
    gain_db = 20 * np.log10(factor)

    # Apply volume gain
    boosted_audio = audio_segment.apply_gain(gain_db)

    return boosted_audio


def trim_silence(audio_segment, silence_thresh=-1, min_silence_len=50, keep_padding=50):
    """ Trim leading and trailing silence where volume is lower than `silence_thresh`. """

    # Detect nonsilent regions (start and end of actual sound)
    nonsilent_ranges = detect_nonsilent(audio_segment, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    if not nonsilent_ranges:
        print("⚠️ No speech detected, returning empty audio.")
        return AudioSegment.silent(duration=500)  # Return short silence to avoid errors

    # Get start and end of non-silent part
    start_trim = max(0, nonsilent_ranges[0][0] - keep_padding)  # Add buffer before start
    end_trim = min(len(audio_segment), nonsilent_ranges[-1][1] + keep_padding)  # Add buffer after end

    # Trim the audio
    trimmed_audio = audio_segment[start_trim:end_trim]

    return trimmed_audio


def normalize_audio(audio_segment, target_dBFS=-20.0):

    # Calculate current loudness
    current_dBFS = audio_segment.dBFS
    gain = target_dBFS - current_dBFS

    # Apply gain to normalize
    normalized_audio = audio_segment.apply_gain(gain)

    return normalized_audio

# o neco lepsi metoda
def adaptive_plosive_reduction(audio_segment, spike_threshold=22000, attack_window=10, release_window=30, reduction_factor=0.6):

    samples = np.array(audio_segment.get_array_of_samples(), dtype=np.int16)
    sample_rate = audio_segment.frame_rate

    # Find rapid spikes (potential plosives)
    spike_indices = np.where(np.abs(samples) > spike_threshold)[0]

    if len(spike_indices) > 0:
        #print(f"⚠️ Detected {len(spike_indices)} plosive spikes, selectively reducing...")

        # Process each detected plosive
        for idx in spike_indices:
            start = max(0, idx - attack_window)
            end = min(len(samples), idx + release_window)

            # Apply a gradual reduction instead of a hard cut
            fade_curve = np.linspace(1, reduction_factor, num=end-start)
            samples[start:end] = (samples[start:end] * fade_curve).astype(np.int16)

    # Convert back to AudioSegment
    processed_audio = AudioSegment(
        samples.tobytes(),
        frame_rate=sample_rate,
        sample_width=2,
        channels=1
    )

    return processed_audio


def enhanced_assemble_speech_from_time(time_input, recordings_folder):
    time_recording_files = pick_correct_recordings_by_time(time_input, recordings_folder)
    time_recording_files = flatten_list(time_recording_files)
    print(time_recording_files)


    for file in time_recording_files:
        audio = load_opus_with_pyav(file)
        audio = trim_silence(audio, silence_thresh=-60, min_silence_len=10, keep_padding=50)
        audio = normalize_audio(audio)
        audio = adaptive_plosive_reduction(audio) # neni 100 % uspesne; pouzita nejnormalnejsi metoda
        audio = boost_audio(audio, factor=1)
        # audio = adjust_pitch(audio, semitones=5) # zvyseni pitchu o 5 polotonu; divny zvuk s plno explozema
        play_audio(audio)


if __name__ == '__main__':
    download_recordings()
    enhanced_assemble_speech_from_time(datetime.now(), RECORDINGS_DIR)
