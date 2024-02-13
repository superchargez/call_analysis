import torch
from speechbrain.pretrained import SpeakerRecognition
from torchaudio.transforms import Resample
from pydub import AudioSegment
import os

# Load SpeechBrain speaker recognition model
spkrec = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models")

# Load audio using PyDub
audio = AudioSegment.from_file(r"C:\Users\jawad\Downloads\projects\audio\new_files\20231215_1020_03008670633_61422.mp3")
fs = audio.frame_rate

# Resample to 16 kHz if necessary
if fs != 16000:
    resampler = Resample(fs, 16000)
    audio = resampler(torch.tensor(audio.get_array_of_samples()).float())
    fs = 16000

# Define chunk size (in seconds) for SpeechBrain
sb_chunk_size = 120  # Modify this based on your needs

# Process first chunk with SpeechBrain to get speaker embeddings
# first_chunk = audio[:sb_chunk_size * fs]
# embeddings = spkrec.encode_batch(first_chunk.unsqueeze(0))

# Process first chunk with SpeechBrain to get speaker embeddings
first_chunk = torch.tensor(audio[:sb_chunk_size * fs].get_array_of_samples()).float()
embeddings = spkrec.encode_batch(first_chunk.unsqueeze(0))

# Perform clustering to identify speaker segments
oracle_vad = spkrec.diarization(embeddings, num_speakers=2)

# Extract timestamps for each speaker segment
speaker_segments = []
for speaker_id in range(len(oracle_vad)):
    speaker_segments.append([oracle_vad[speaker_id][0], oracle_vad[speaker_id][-1]])

# Process remaining chunks with SpeechBrain using the same speaker embeddings
for i in range(sb_chunk_size * fs, len(audio), sb_chunk_size * fs):
    sb_chunk = audio[i:i + sb_chunk_size * fs]

    # Apply the same speaker embeddings to the chunk
    embeddings = spkrec.encode_batch(sb_chunk.unsqueeze(0))

    # Perform clustering to identify speaker segments
    oracle_vad = spkrec.diarization(embeddings, num_speakers=2)

    # Extract timestamps for each speaker segment
    for speaker_id in range(len(oracle_vad)):
        speaker_segments.append([oracle_vad[speaker_id][0] + i/fs, oracle_vad[speaker_id][-1] + i/fs])

# Print the speaker segments
for segment in speaker_segments:
    print(f"Speaker {segment[0]}: {segment[1]}")
