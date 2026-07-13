# Code-Work-Palace

A sandbox of small computer-vision and Python experiments — mostly OpenCV/MediaPipe scripts built while learning, ahead of using them for real robotics/vision work.

## Projects

### `opencv_colour_detector.py`
Tracks a specific color (HSV range) from a webcam feed and draws a bounding box around detected blobs. Good starting point for color-based object tracking — the kind of thing a robot's camera might use to find a target object (The code currently only detect yellow colour, can add other colour later).

### `opencv_sleep_detector.py`
Drowsiness/eye-closure detector using MediaPipe Face Mesh. Computes the Eye Aspect Ratio (EAR) from eye landmarks — if EAR stays below a threshold for several consecutive frames, it flags "SLEEPING" on screen.

### `opencv_hand_gesture.py` *(new)*
Real-time hand gesture recognition using MediaPipe Hands. Detects which fingers are extended and classifies simple gestures: `FIST`, `OPEN PALM`, `PEACE`, `THUMBS UP`, `POINTING`, or a finger count. A natural extension of the face-mesh work above — this kind of gesture detection is a common first step toward gesture-based robot control.

### `print.py`
My very first commit is a "hello world" loop used to test that Git was set up correctly. Its probably everyone's first coding project ngl, but it sure is memorable.

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
OR press Ctrl + C on your VS Code terminal

## Troubleshooting

### `AttributeError: module 'mediapipe' has no attribute 'solutions'`

This one has two possible causes — check both.

**1. Wrong Python interpreter (Windows, `py` vs `python`)**

If you're using a venv on Windows, always activate it and run scripts with `python`, not `py`. The `py` launcher ignores whatever venv is active and falls back to its own default Python install (e.g. a newer 3.13/3.14), which may not have MediaPipe installed correctly for that interpreter.

```powershell
# activate your venv first
venv\Scripts\Activate.ps1

# use python, not py
python opencv_hand_gesture.py
```

Sanity check which interpreter and mediapipe build you're actually running:

```powershell
python -c "import mediapipe as mp; print(mp.__file__); print(mp.__version__)"
```

**2. Python version too new**

MediaPipe's legacy `solutions` API (`mp.solutions.hands`, `.face_mesh`, etc.) doesn't ship working wheels for very new Python releases (3.13+ at time of writing). If you're on Python 3.13/3.14, create a venv with Python 3.10 or 3.11 instead:

```powershell
py -3.11 -m venv venv311
venv311\Scripts\Activate.ps1
pip install -r requirements.txt
```

**3. Broken/regressed MediaPipe release**

Even on a supported Python version, some recent MediaPipe releases (0.10.3x) shipped with the legacy `solutions` module broken or missing — this is a known upstream issue, not a local setup problem ([tracked in multiple GitHub issues](https://github.com/google-ai-edge/mediapipe/issues/6204)). If `hasattr(mediapipe, 'solutions')` is `False` even in a fresh, correctly activated venv, pin to a known-good older version:

```powershell
pip uninstall mediapipe -y
pip install mediapipe==0.10.14
```

If that still doesn't work, try `0.10.9` or `0.10.11` as fallbacks. Google is migrating away from the legacy `solutions` API toward the newer Tasks API (`mediapipe.tasks.python.vision`), so long-term these scripts may need a rewrite to that API instead of pinning old versions forever.

## Ideas for what's next

- ArUco marker detection + pose estimation (useful for robot localization/navigation)
- Single-camera object distance estimation from known object width
- Basic line-follower path detection (classic robotics CV building block)
