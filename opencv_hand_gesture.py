import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Landmark indices for fingertip and lower joint (used to check if a finger is extended)
FINGER_TIPS = [8, 12, 16, 20]      # index, middle, ring, pinky tips
FINGER_PIPS = [6, 10, 14, 18]      # corresponding lower joints
THUMB_TIP = 4
THUMB_IP = 3


def euclidean(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def fingers_up(landmarks, handedness_label):
    """Returns a list [thumb, index, middle, ring, pinky] where 1 = extended, 0 = folded."""
    fingers = []

    # Thumb: compare x-position relative to hand orientation (mirrored for left/right hand)
    if handedness_label == "Right":
        fingers.append(1 if landmarks[THUMB_TIP].x < landmarks[THUMB_IP].x else 0)
    else:
        fingers.append(1 if landmarks[THUMB_TIP].x > landmarks[THUMB_IP].x else 0)

    # Other four fingers: tip above pip joint (smaller y = higher up in image) means extended
    for tip, pip in zip(FINGER_TIPS, FINGER_PIPS):
        fingers.append(1 if landmarks[tip].y < landmarks[pip].y else 0)

    return fingers


def classify_gesture(fingers):
    total = sum(fingers)
    thumb, index, middle, ring, pinky = fingers

    if total == 0:
        return "FIST"
    if total == 5:
        return "OPEN PALM"
    if index == 1 and middle == 1 and ring == 0 and pinky == 0 and thumb == 0:
        return "PEACE"
    if thumb == 1 and index == 0 and middle == 0 and ring == 0 and pinky == 0:
        return "THUMBS UP"
    if index == 1 and total == 1:
        return "POINTING"
    return f"{total} FINGERS"


def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        gesture = "NO HAND"

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks, results.multi_handedness
            ):
                label = handedness.classification[0].label  # "Left" or "Right"
                fingers = fingers_up(hand_landmarks.landmark, label)
                gesture = classify_gesture(fingers)

                mp_draw.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

        cv2.putText(
            frame, f"Gesture: {gesture}", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
        )

        cv2.imshow("Hand Gesture Recognition", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
