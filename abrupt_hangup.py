from pydub import AudioSegment
import numpy as np
from icecream import ic
audio_file_path = r"files\20231026_2234_3335903007_61427.mp3" # 3312223710.wav
# audio_file_path = r"C:\Users\jawad\Downloads\3334231610 abrupt m atif .wav" # 3312223710.wav
audio_data = AudioSegment.from_file(audio_file_path)

def abrupt_hangup(audio_data):
    recording = audio_data.get_array_of_samples()
    sampling_rate = audio_data.frame_rate
    # ic(sampling_rate)
    two_seconds = 2 * sampling_rate
    half_second = 0.5 * sampling_rate
    # thresh = math.ceil(audio_data.max * 0.1)

    # Get the magnitudes above the threshold for the entire audio, last two seconds, and last 0.5 seconds
    all_magnitudes = [abs(i) for i in recording if abs(i) > 45]
    last_two_seconds_magnitudes = [abs(i) for i in recording[-int(two_seconds):]]# if abs(i) > thresh]
    last_half_second_magnitudes = [abs(i) for i in recording[-int(half_second):]]# if abs(i) > thresh]
    # ic(max(all_magnitudes), max(last_two_seconds_magnitudes), max(last_half_second_magnitudes))
    # Calculate the averages
    avg_all_magnitudes = np.mean(all_magnitudes)
    avg_last_two_seconds = np.mean(last_two_seconds_magnitudes)
    avg_last_half_second = np.mean(last_half_second_magnitudes)
    # ic(avg_all_magnitudes, avg_last_half_second, avg_last_two_seconds)
    # Check if the averages of the last two seconds and last 0.5 seconds are below the threshold
    if avg_last_two_seconds < avg_all_magnitudes and avg_last_half_second < avg_all_magnitudes:
        message = "The agent did not hang up abruptly."
        result = False
        print(f"'result: ' {result}, 'message: ' {message}")
        return {'result': result, 'message': message}

    # If not, it's considered an abrupt hangup
    message = "The agent hung up abruptly."
    result = True
    print(f"'result: ' {result}, 'message: ' {message}")
    return {'result': result, 'message': message}

abrupt_hangup(audio_data)
