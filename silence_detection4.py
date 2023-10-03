import subprocess
import re

def detect_silence(filename, threshold=-30.0, duration=20.0):
    cmd = f'ffmpeg -i "{filename}" -af silencedetect=n={threshold}dB:d={duration} -f null -'
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode()

    pattern = r'\[silencedetect .* silence_(start|end): (\d+\.\d*)'
    matches = re.findall(pattern, output)

    # Pair up the start and end times of each silent section
    iter_matches = iter(matches)
    silent_zones = list(zip(iter_matches, iter_matches))

    # Convert to float and return
    silent_zones = [(float(start[1]), float(end[1])) for start, end in silent_zones]

    print(f'Silent zones: {silent_zones}')

    return silent_zones

file = r'static\audio\3119753712.wav'
silent_zones = detect_silence(file)

from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np

def plot_audio(filename, silent_zones):
    # Load the audio file
    audio_data = AudioSegment.from_file(filename)
    
    # Get the frame rate
    fs = audio_data.frame_rate
    
    # Convert the audio data to a numpy array
    audio_data = np.array(audio_data.get_array_of_samples())

    # If the audio file is stereo, convert it to mono
    if len(audio_data.shape) > 1:
        audio_data = np.mean(audio_data, axis=1)


    # Create a time vector
    time = np.linspace(0, len(audio_data) / fs, num=len(audio_data))

    # Create a figure and plot the audio data
    plt.figure(figsize=(10, 4))
    plt.plot(time, audio_data, label='Audio data')

    # Plot the silent zones
    for start_time, end_time in silent_zones:
        plt.axvspan(start_time, end_time, color='r', alpha=0.5, label='Silent zones')

    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()

plot_audio(file, silent_zones)
