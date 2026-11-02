import whisper

print("Loading AI speech model...")

model = whisper.load_model("base")

print("Ask the candidate to answer now...")

result = model.transcribe("answer.wav")

print("\nCandidate Answer:")
print(result["text"])