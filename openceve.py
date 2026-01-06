import cv2
import mediapipe as mp
import math

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(refine_landmarks=True)

def euclidean(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def EAR(landmarks, idx):
    top = euclidean(landmarks[idx[1]], landmarks[idx[5]])
    bottom = euclidean(landmarks[idx[2]], landmarks[idx[4]])
    width = euclidean(landmarks[idx[0]], landmarks[idx[3]])
    return (top + bottom) / (2.0 * width)

LEFT_EYE = [33, 159, 158, 133, 153, 144]
RIGHT_EYE = [362, 386, 385, 263, 380, 373]

cap = cv2.VideoCapture(0)

EAR_THRESHOLD = 0.25
FRAME_THRESHOLD = 15
closed_frames = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face in results.multi_face_landmarks:
            landmarks = face.landmark

            left_ear = EAR(landmarks, LEFT_EYE)
            right_ear = EAR(landmarks, RIGHT_EYE)
            ear = (left_ear + right_ear) / 2

            if ear < EAR_THRESHOLD:
                closed_frames += 1
            else:
                closed_frames = 0

            status = "SLEEPING" if closed_frames >= FRAME_THRESHOLD else "AWAKE"
            color = (0, 0, 255) if status == "SLEEPING" else (0, 255, 0)

            cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            cv2.putText(frame, f"Status: {status}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("Sleep Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
