import numpy as np
from scipy.io.wavfile import write

# Pengaturan musik
SAMPLE_RATE = 44100
DURATION = 30
BPM = 120

print("Memulai Memphis Phonk Generator...")
print("Durasi:", DURATION, "detik")
print("Tempo:", BPM, "BPM")

# Membuat audio kosong
total_samples = SAMPLE_RATE * DURATION
audio = np.zeros(total_samples, dtype=np.float32)

print("Audio dasar berhasil dibuat!")
