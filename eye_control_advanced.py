import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
from collections import deque

# ---------------- CONFIG ----------------
pyautogui.FAILSAFE = False

BLINK_EAR_THRESHOLD = 0.28
CLICK_MAX_DURATION = 0.6
DRAG_MIN_DURATION = 1.2
CLICK_COOLDOWN = 1.0
PAUSE_EYES_CLOSED_TIME = 3.0

SENSITIVITY = 2.2
SMOOTHING_FRAMES = 7
SCROLL_THRESHOLD = 0.15
SCROLL_SPEED = 25
# ---------------------------------------

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(refine_landmarks=True)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
LEFT_IRIS = [468, 469, 470, 471]

def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

screen_w, screen_h = pyautogui.size()
cap = cv2.VideoCapture(0)

cursor_x_history = deque(maxlen=SMOOTHING_FRAMES)
cursor_y_history = deque(maxlen=SMOOTHING_FRAMES)

blink_start = 0
last_click_time = 0
dragging = False
paused = False
eyes_closed_start = None

print("👁️ Eye Control Advanced Started | Press Q to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        lm = results.multi_face_landmarks[0].landmark

        # -------- CURSOR MOVEMENT (IRIS) --------
        eye_x = sum(lm[i].x for i in LEFT_IRIS) / 4
        eye_y = sum(lm[i].y for i in LEFT_IRIS) / 4

        eye_x = (eye_x - 0.5) * SENSITIVITY + 0.5
        eye_y = (eye_y - 0.5) * SENSITIVITY + 0.5

        eye_x = min(max(eye_x, 0), 1)
        eye_y = min(max(eye_y, 0), 1)

        cx = int(eye_x * screen_w)
        cy = int(eye_y * screen_h)

        cursor_x_history.append(cx)
        cursor_y_history.append(cy)

        smooth_x = int(np.mean(cursor_x_history))
        smooth_y = int(np.mean(cursor_y_history))

        if not paused:
            pyautogui.moveTo(smooth_x, smooth_y)

        # -------- SCROLLING --------
        if not paused:
            if eye_y < 0.5 - SCROLL_THRESHOLD:
                pyautogui.scroll(SCROLL_SPEED)
            elif eye_y > 0.5 + SCROLL_THRESHOLD:
                pyautogui.scroll(-SCROLL_SPEED)

        # -------- BLINK DETECTION --------
        left_eye = np.array([[lm[i].x, lm[i].y] for i in LEFT_EYE])
        right_eye = np.array([[lm[i].x, lm[i].y] for i in RIGHT_EYE])
        ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2

        # -------- PAUSE / RESUME --------
        if ear < BLINK_EAR_THRESHOLD:
            if eyes_closed_start is None:
                eyes_closed_start = time.time()
            elif time.time() - eyes_closed_start > PAUSE_EYES_CLOSED_TIME:
                paused = not paused
                print("⏸️ PAUSED" if paused else "▶️ RESUMED")
                eyes_closed_start = None
        else:
            eyes_closed_start = None

        # -------- CLICK & DRAG --------
        if ear < BLINK_EAR_THRESHOLD:
            if blink_start == 0:
                blink_start = time.time()
        else:
            if blink_start != 0:
                duration = time.time() - blink_start

                if duration < CLICK_MAX_DURATION:
                    if time.time() - last_click_time > CLICK_COOLDOWN and not paused:
                        pyautogui.click()
                        last_click_time = time.time()
                        print("🖱️ CLICK")

                elif duration > DRAG_MIN_DURATION:
                    if not dragging and not paused:
                        pyautogui.mouseDown()
                        dragging = True
                        print("📦 DRAG START")
                    elif dragging:
                        pyautogui.mouseUp()
                        dragging = False
                        print("📦 DROP")

                blink_start = 0

        # -------- VISUALS --------
        h, w, _ = frame.shape
        cv2.circle(frame, (int(eye_x * w), int(eye_y * h)), 6, (0, 0, 255), -1)
        cv2.putText(frame, f"EAR: {ear:.2f}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        if paused:
            cv2.putText(frame, "PAUSED", (20, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    cv2.imshow("Eye Control Advanced (Q to exit)", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
