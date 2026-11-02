import os
import imageio_ffmpeg
import sounddevice as sd
from scipy.io.wavfile import write
import whisper

# Fix FFmpeg path automatically
os.environ["PATH"] += os.pathsep + os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())

# Recording settings
duration = 10
sample_rate = 44100

print("Recording... Speak now!")

audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
sd.wait()

file_name = "answer.wav"
write(file_name, sample_rate, audio)

print("Audio saved as answer.wav")

print("Loading Whisper AI model...")
model = whisper.load_model("base")

result = model.transcribe(file_name)

print("\n--- Transcription ---")
print(result["text"])

with open("transcription.txt", "w") as f:
    f.write(result["text"])