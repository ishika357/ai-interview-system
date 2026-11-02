import os
import imageio_ffmpeg
import whisper


# =========================
# SET FFMPEG
# =========================

ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

ffmpeg_folder = os.path.dirname(ffmpeg_path)

os.environ["PATH"] = ffmpeg_folder + os.pathsep + os.environ.get("PATH", "")

print("Setting up FFmpeg...")
print("FFmpeg:", ffmpeg_path)
print("FFmpeg ready.")


# =========================
# CHECK AUDIO FILE
# =========================

if not os.path.exists("answer.wav"):

    print("ERROR: answer.wav was not found.")

    exit()


# =========================
# LOAD WHISPER
# =========================

print("Loading AI speech model...")

model = whisper.load_model("base")

print("Transcribing answer...")


# =========================
# TRANSCRIBE
# =========================

result = model.transcribe(
    "answer.wav",
    language="en",
    fp16=False
)


answer = result["text"].strip()


# =========================
# DISPLAY ANSWER
# =========================

print()
print("Candidate Answer:")
print(answer)
print()


# =========================
# SAVE ANSWER
# =========================

with open(
    "candidate_answer.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(answer)


print("Transcription saved successfully.")