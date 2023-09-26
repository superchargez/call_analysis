from configparser import ConfigParser, ExtendedInterpolation
from pydub import AudioSegment
import math

configuration_file = 'config.ini'
configuration = ConfigParser(interpolation=ExtendedInterpolation())
configuration.read(configuration_file)

audio_file_path = r"3119753712.wav" # 3312223710.wav
import os
os.chdir(r"static/audio")
audio_data = AudioSegment.from_file(audio_file_path)

def late_initialization(audio_data):
    config = configuration['late_initialization']
    first_recording = audio_data.get_array_of_samples()
    sampling_rate = audio_data.frame_rate
    five_seconds = 5 * sampling_rate
    start = 0
    end = int(five_seconds)
    first_recording_synthesized = first_recording[start:end]

    print("Max Value",audio_data.max)
    thresh = math.ceil(audio_data.max * 0.2)

    print("Treshold", thresh)

    silence_duration = 0
    speech_started = False

    for idx, j in enumerate(first_recording_synthesized):
        if abs(j) <= thresh:
            # Increment silence_duration if we're still waiting for speech to start
            if not speech_started:
                silence_duration += 1
        else:
            # Mark that speech has started
            speech_started = True

        # Check if there has been silence for four seconds and then speech for at least two seconds
        if silence_duration / sampling_rate <= 4 and (idx - silence_duration) / sampling_rate >= 2:
            message = f"The agent started speaking within four seconds and the speech lasted for at least {(idx - silence_duration) / sampling_rate} seconds."
            result = False
            print(f"'result: ' {result}, 'message: ' {message}")
            return {'result': result, 'message': message, 'good': config.getboolean('good')}

    # If no such speech is found, it is considered a late initialization
    message = "The agent did not start speaking within the first four seconds or the speech did not last for at least two seconds."
    result = True
    print(f"'result: ' {result}, 'message: ' {message}")
    return {'result': result, 'message': message, 'good': config.getboolean('good')}

late_initialization(audio_data)