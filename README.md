# Code-Work-Pallace

A sandbox of small computer-vision and Python experiments — mostly OpenCV/MediaPipe scripts built while learning, ahead of using them for real robotics/vision work.

## Projects

### `opencv_colour_detector.py`
Tracks a specific color (HSV range) from a webcam feed and draws a bounding box around detected blobs. Good starting point for color-based object tracking — the kind of thing a robot's camera might use to find a target object.

### `opencv_sleep_detector.py`
Drowsiness/eye-closure detector using MediaPipe Face Mesh. Computes the Eye Aspect Ratio (EAR) from eye landmarks — if EAR stays below a threshold for several consecutive frames, it flags "SLEEPING" on screen.

### `opencv_hand_gesture.py` *(new)*
Real-time hand gesture recognition using MediaPipe Hands. Detects which fingers are extended and classifies simple gestures: `FIST`, `OPEN PALM`, `PEACE`, `THUMBS UP`, `POINTING`, or a finger count. A natural extension of the face-mesh work above — this kind of gesture detection is a common first step toward gesture-based robot control.

### `print.py`
My very first commit is a "hello world" loop used to test that Git was set up correctly. It sure is memorable.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Running

Each script is standalone and opens your webcam directly:

```bash
python opencv_colour_detector.py
python opencv_sleep_detector.py
python opencv_hand_gesture.py
```

Press **ESC** in the video window to quit any of them.

## Ideas for what's next

- ArUco marker detection + pose estimation (useful for robot localization/navigation)
- Single-camera object distance estimation from known object width
- Basic line-follower path detection (classic robotics CV building block)
