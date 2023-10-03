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
