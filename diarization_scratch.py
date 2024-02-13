import torchaudio
from speechbrain.pretrained import EncoderClassifier
classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")
signal, fs =torchaudio.load(r"C:\Users\jawad\Downloads\projects\audio\new_files\20231215_1020_03338407124_61589.mp3")
embeddings = classifier.encode_batch(signal)

# Reshape the embeddings tensor into a 2D array
nsamples, nx, ny = embeddings.shape
d2_embeddings = embeddings.reshape((nsamples,nx*ny))

from sklearn.cluster import KMeans

# Assume `d2_embeddings` is a 2D array where each row is the embedding of a segment
kmeans = KMeans(n_clusters=3)  # Replace 2 with the expected number of speakers
labels = kmeans.fit_predict(d2_embeddings)

print(labels)
