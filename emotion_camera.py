import cv2
from deepface import DeepFace

# start camera
cap = cv2.VideoCapture(0)

print("Camera started. Press Q to exit.")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        emotion = result[0]['dominant_emotion']

        cv2.putText(frame, f'Emotion: {emotion}', (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0,255,0), 2)

    except:
        pass

    cv2.imshow("Interview Emotion Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

with open("emotion.txt", "w") as f:
    f.write(dominant_emotion)
    
cap.release()
cv2.destroyAllWindows()