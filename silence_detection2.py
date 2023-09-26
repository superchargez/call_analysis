import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment
from configparser import ConfigParser, ExtendedInterpolation

configuration_file = 'config.ini'
configuration = ConfigParser(interpolation=ExtendedInterpolation())
configuration.read(configuration_file)

audio_file_path = r"3119753712.wav"
import os
os.chdir(r"static/audio")

# Load audio file with PyDub then export it as wav
audio_data = AudioSegment.from_file(audio_file_path)
audio_data = audio_data.set_channels(1)
audio_data.export("temp.wav", format="wav")

# Read the wav file with scipy.io.wavfile
sample_rate, samples = wavfile.read("temp.wav")

def silence_detection(samples, sample_rate):
    config = configuration['abrupt_hangup']
    silence_zone = config.getint('silence_zone')
    region_list = []
    
    # Convert silence length and threshold to sample values
    min_silence_len = 1000 * sample_rate // 1000
    silence_thresh = -45

    # Find places where audio is below the silence threshold
    silent_samples = np.where(np.abs(samples) < silence_thresh)[0]

    # Initialize variables for silence detection
    start, stop = None, None
    regions = 0

    # Iterate over silent samples and detect silence regions
    for sample in silent_samples:
        if start is None:
            start = sample
        elif sample - stop > min_silence_len:
            if (stop - start) / sample_rate > silence_zone:
                region_list.append([start / sample_rate, stop / sample_rate])
                regions += 1
            start = sample
        stop = sample

    result = regions > 0

    message = "There were {} silent region(s) that were greater than {} seconds".format(regions, silence_zone)
    
    return {'result': result, 'message': message, 'regions': region_list, 'good': config.getboolean('good')}

import time

start_time = time.time()

# Call your function here
silence_detection(samples, sample_rate)

end_time = time.time()

execution_time = end_time - start_time

print(f"The function took {execution_time} seconds to run.")
