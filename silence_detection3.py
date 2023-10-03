import numpy as np
import soundfile as sf

def detect_silence(audio_data, sample_rate, threshold=0.01, frame_size=0.01,
                   hop_size=0.005, min_silence_len=20):
  """Detects silence in audio data using the energy thresholding technique.

  Args:
    audio_data: A NumPy array containing the audio data.
    sample_rate: The sample rate of the audio data, in Hz.
    threshold: The energy threshold, below which a frame is considered to be silent.
    frame_size: The size of each frame for energy calculation, in seconds.
    hop_size: The hop size for frame overlapping, in seconds.
    min_silence_len: The minimum length of a silent zone to be considered as silence, in seconds.

  Returns:
    A list of silent zones (start time, end time), in seconds.
  """

  # If the audio file has more than one channel (i.e., it's stereo), convert it to mono
  if len(audio_data.shape) > 1:
      audio_data = np.mean(audio_data, axis=1)

  # Compute the energy of each frame in the audio data.
  frame_length = int(frame_size * sample_rate)
  hop_length = int(hop_size * sample_rate)
  frames = np.array([audio_data[i:i + frame_length] for i in range(0, len(audio_data) - frame_length + 1, hop_length)])

  # Check if frames is 1-D or 2-D before calculating frame_energies
  if frames.ndim == 1:
      frame_energies = np.sum(frames ** 2)
  else:
      frame_energies = np.sum(frames ** 2, axis=1)

  # Identify the silent zones in the audio data.
  silent_zones = []
  start_time = None
  for i in range(len(frame_energies)):
    if frame_energies[i] < threshold:
      if start_time is None:
        start_time = i * hop_size
    else:
      if start_time is not None and (i * hop_size - start_time) >= min_silence_len:
        end_time = i * hop_size
        silent_zones.append((start_time, end_time))
      start_time = None

  # Check if the last zone is silent and longer than min_silence_len
  if start_time is not None and (len(audio_data) / sample_rate - start_time) >= min_silence_len:
    end_time = len(audio_data) / sample_rate
    silent_zones.append((start_time, end_time))

  # Return the list of silent zones.
  return silent_zones


audio_data, sample_rate = sf.read(r'static\audio\3119753712.wav')

silent_zones = detect_silence(audio_data, sample_rate)

# Print the list of silent zones.
for start_time, end_time in silent_zones:
    print(f"Silent zone from {start_time:.3f}s to {end_time:.3f}s")
