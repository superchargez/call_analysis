from pydub import AudioSegment
import math

audio_file_path = r"C:\Users\jawad\Downloads\projects\audio\files\EC8033251128747242023102616513141.wav" # 3312223710.wav
audio_data = AudioSegment.from_file(audio_file_path)

def late_hangup(audio_data):
    last_recording = audio_data.get_array_of_samples()
    sampling_rate = audio_data.frame_rate
    five_seconds = 5 * sampling_rate
    start = int(len(last_recording) - five_seconds)
    end = len(last_recording)
    last_recording_synthesized = last_recording[start:end]

    print("Max Value",audio_data.max)
    thresh = math.ceil(audio_data.max * 0.1)

    print("Treshold", thresh)

    silence_duration = 0
    speech_started = False

    for idx, j in enumerate(last_recording_synthesized):
        if abs(j) <= thresh:
            # Increment silence_duration if we're still waiting for speech to start
            if not speech_started:
                silence_duration += 1
        else:
            # Mark that speech has started
            speech_started = True

        # Check if there has been silence for four seconds and then speech for at least two seconds
        if silence_duration / sampling_rate <= 4 and (idx - silence_duration) / sampling_rate >= 2:
            message = f"The agent stopped speaking within four seconds and the silence lasted for at least {(idx - silence_duration) / sampling_rate} seconds."
            result = False
            print(f"'result: ' {result}, 'message: ' {message}")
            return {'result': result, 'message': message}

    # If no such silence is found, it is considered a late hangup
    message = "The agent did not stop speaking within the last four seconds or the silence did not last for at least two seconds."
    result = True
    print(f"'result: ' {result}, 'message: ' {message}")
    return {'result': result, 'message': message}

late_hangup(audio_data)
