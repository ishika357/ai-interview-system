import cv2
from deepface import DeepFace

cap = cv2.VideoCapture(0)

ret, frame = cap.read()

emotion = "Unknown"

if ret:
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
    except:
        pass

cap.release()

print("Final Emotion:", emotion)

with open("emotion.txt","w") as f:
    f.write(emotion)