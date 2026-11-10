
import numpy as np
from scipy.io.wavfile import write

# ==================================
# MEMPHIS PHONK MUSIC GENERATOR
# ==================================

SR = 44100
DURATION = 30
BPM = 120

rng = np.random.default_rng(21)
total = SR * DURATION
music = np.zeros(total, dtype=np.float64)

beat = 60 / BPM
bar = beat * 4


def add_sound(sound, start, volume=1.0):
    start_sample = int(start * SR)
    end_sample = min(start_sample + len(sound), total)

    if start_sample < total and end_sample > start_sample:
        music[start_sample:end_sample] += (
            sound[:end_sample - start_sample] * volume
        )


def kick():
    length = int(0.35 * SR)
    t = np.arange(length) / SR
    freq = 110 * np.exp(-t * 16)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    env = np.exp(-t * 11)
    return np.sin(phase) * env


def snare():
    length = int(0.22 * SR)
    t = np.arange(length) / SR
    noise = rng.normal(0, 1, length)
    tone = np.sin(2 * np.pi * 190 * t)
    env = np.exp(-t * 19)
    return (noise * 0.65 + tone * 0.35) * env


def hat():
    length = int(0.07 * SR)
    t = np.arange(length) / SR
    noise = rng.normal(0, 1, length)
    return noise * np.exp(-t * 65)


def cowbell(freq=650):
    length = int(0.28 * SR)
    t = np.arange(length) / SR

    tone = (
        np.sin(2 * np.pi * freq * t)
        + 0.55 * np.sin(2 * np.pi * freq * 1.48 * t)
    )

    env = np.exp(-t * 12)
    return tone * env * 0.45


def bass(freq=55):
    length = int(0.38 * SR)
    t = np.arange(length) / SR
    tone = np.sin(2 * np.pi * freq * t)
    env = np.exp(-t * 5)
    return tone * env


# ==================================
# MUSICAL ARRANGEMENT
# ==================================

for step in range(int(DURATION / (beat / 2))):
    time = step * beat / 2
    bar_number = time // bar

    # Intro: 0-5 seconds
    if time < 5:
        if step % 4 == 0:
            add_sound(hat(), time, 0.22)
        if step % 8 == 0:
            add_sound(cowbell(550), time, 0.35)
        continue

    # Main beat
    if step % 4 == 0:
        add_sound(kick(), time, 0.85)

    if step % 4 == 2:
        add_sound(snare(), time, 0.55)

    if step % 2 == 1:
        add_sound(hat(), time, 0.18)

    # Cowbell melody
    if step % 2 == 0:
        notes = [660, 740, 880, 740, 550, 660, 880, 990]
        note = notes[(step // 2) % len(notes)]
        add_sound(cowbell(note), time, 0.55)

    # Bass pattern
    if step % 4 == 0:
        bass_notes = [55, 55, 65.4, 49]
        freq = bass_notes[int(bar_number) % 4]
        add_sound(bass(freq), time, 0.7)


# ==================================
# ENDING AND EXPORT
# ==================================

fade = int(1.5 * SR)
music[-fade:] *= np.linspace(1, 0, fade)

peak = np.max(np.abs(music))
if peak > 0:
    music = music / peak * 0.85

audio = (music * 32767).astype(np.int16)

write("output.wav", SR, audio)

print("Memphis Phonk berhasil dibuat!")
print("Durasi:", DURATION, "detik")
print("Tempo:", BPM, "BPM")
print("File: output.wav")
