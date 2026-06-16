import os
import matplotlib
matplotlib.use('Agg')  # Forces matplotlib to run without a GUI monitor
os.environ["QT_QPA_PLATFORM"] = "offscreen"  # Forces OpenCV to run without a GUI monitorimport cv2
from ultralytics import YOLO
import smtplib
import cv2  # <--- MAKE SURE THIS LINE IS EXPLICITLY HERE!
from ultralytics import YOLO
from email.mime.text import MIMEText
import threading
import time
import os
import sys
import platform
import numpy as np

try:
    import simpleaudio as sa # pyright: ignore[reportMissingImports]
    SIMPLEAUDIO_AVAILABLE = True
except ImportError:
    sa = None
    SIMPLEAUDIO_AVAILABLE = False

WINSOUND_AVAILABLE = False
if platform.system() == "Windows":
    try:
        import winsound
        WINSOUND_AVAILABLE = True
    except ImportError:
        WINSOUND_AVAILABLE = False

# Parse command line arguments
video_file = None
if len(sys.argv) > 1:
    video_file = sys.argv[1]
    if not os.path.exists(video_file):
        print(f"Error: Video file '{video_file}' not found.")
        exit(1)

# Check if model file exists
model_path = "model/best.pt"
if not os.path.exists(model_path):
    print(f"Error: Model file '{model_path}' not found.")
    exit(1)

model = YOLO(model_path)

print("Model classes:", model.names)

def try_open_capture(source, backend=None):
    if backend is None:
        cap = cv2.VideoCapture(source)
    else:
        cap = cv2.VideoCapture(source, backend)
    if cap is None or not cap.isOpened():
        if cap is not None:
            cap.release()
        return None
    return cap


def backend_name(backend):
    if backend is None:
        return "default"
    if hasattr(cv2, "CAP_DSHOW") and backend == cv2.CAP_DSHOW:
        return "CAP_DSHOW"
    if hasattr(cv2, "CAP_MSMF") and backend == cv2.CAP_MSMF:
        return "CAP_MSMF"
    return str(backend)


class SyntheticCapture:
    def __init__(self, width=640, height=480, color=(0, 0, 0)):
        self.width = width
        self.height = height
        self.color = color

    def isOpened(self):
        return True

    def read(self):
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        frame[:] = self.color
        return True, frame

    def release(self):
        pass

    def get(self, prop):
        return 0

    def set(self, prop, value):
        return False


def find_available_camera():
    """Try to find an available camera on Windows and fallback to default backends."""
    backends = []
    if hasattr(cv2, "CAP_DSHOW"):
        backends.append(cv2.CAP_DSHOW)
    if hasattr(cv2, "CAP_MSMF"):
        backends.append(cv2.CAP_MSMF)
    backends.append(None)

    for i in range(5):  # Try camera indexes 0-4
        for backend in backends:
            cap = try_open_capture(i, backend)
            if cap is None:
                continue
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f"Using camera index {i} with backend {backend_name(backend)}")
                return cap
            cap.release()
    return None

# Open camera or video file
if video_file:
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print(f"Error: Could not open video file '{video_file}'.")
        exit(1)
    print(f"Using video file: {video_file}")
else:
    cap = find_available_camera()
    if cap is None:
        default_video = "fire_video.mp4"
        if os.path.exists(default_video):
            cap = cv2.VideoCapture(default_video)
            if cap.isOpened():
                print(f"No webcam found. Using default video file: {default_video}")
            else:
                cap.release()
                cap = None
        if cap is None:
            print("Warning: No webcam available and no fallback video found.")
            print("Using a blank test feed instead. Run with a real video file via: python detect.py your_video.mp4")
            cap = SyntheticCapture()



def send_email_alert():
    def send():
        sender_email = "sshivappa610@gmail.com"
        receiver_email = "srujanasinchana36@gmail.com"
        app_password = "xpbo xirm xerj acal"
        msg = MIMEText("🔥 Fire detected! Immediate attention required!")
        msg["Subject"] = "Fire Alert 🚨"
        msg["From"] = sender_email
        msg["To"] = receiver_email

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            print("Email sent!")
        except Exception as e:
            print("Email error:", e)

    threading.Thread(target=send).start()

def log_fire_event():
    with open("output/log.txt", "a") as f:
        f.write(f"Fire detected at {time.ctime()}\n")

wave_obj = None
if SIMPLEAUDIO_AVAILABLE:
    try:
        wave_obj = sa.WaveObject.from_wave_file("Alarm.wav")
    except Exception as e:
        print("Warning: could not load Alarm.wav with simpleaudio:", e)
        wave_obj = None
        SIMPLEAUDIO_AVAILABLE = False

if not SIMPLEAUDIO_AVAILABLE:
    if WINSOUND_AVAILABLE:
        print("Warning: simpleaudio unavailable, using winsound fallback for audio alerts.")
    else:
        print("Warning: simpleaudio unavailable and winsound not available; audio alerts are disabled.")


def play_alarm_sound():
    global play_obj

    if SIMPLEAUDIO_AVAILABLE and wave_obj is not None:
        try:
            if play_obj is not None and getattr(play_obj, "is_playing", lambda: False)():
                play_obj.stop()
            play_obj = wave_obj.play()
            return
        except Exception as e:
            print("Audio warning: simpleaudio failed to play Alarm.wav:", e)

    if WINSOUND_AVAILABLE and os.path.exists("Alarm.wav"):
        try:
            winsound.PlaySound("Alarm.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            return
        except Exception as e:
            print("Audio warning: winsound failed to play Alarm.wav:", e)

    if WINSOUND_AVAILABLE:
        try:
            winsound.Beep(1000, 700)
            return
        except Exception as e:
            print("Audio warning: winsound beep failed:", e)

    print("Audio alert unavailable.")

play_obj = None

fire_frames = 0
last_alert_time = 0
COOLDOWN = 2  

try:
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            if isinstance(cap, cv2.VideoCapture) and cap.get(cv2.CAP_PROP_FRAME_COUNT) > 0:
                # If it's a video file, loop it
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()
                if not ret or frame is None:
                    print("Error: Could not read frame from video file.")
                    break
            else:
                print("Error: Could not read frame from camera/video.")
                time.sleep(1)  # Wait a bit before retrying
                continue

        results = model(frame)

        fire_detected = False

        for result in results:
            boxes = result.boxes

            if boxes is not None:
                for box in boxes:
                    cls = int(box.cls[0])
                    label = model.names[cls]
                    conf = float(box.conf[0])

                    if label.lower() == "fire" and conf > 0.25:
                        fire_detected = True

        if fire_detected:
            fire_frames += 1
        else:
            fire_frames = 0

        current_time = time.time()

        if fire_frames >= 2 and (current_time - last_alert_time > COOLDOWN):
            print("🔥 FIRE DETECTED !!!")
            play_alarm_sound()
            send_email_alert()
            log_fire_event()
            last_alert_time = current_time

        if fire_frames == 0 and SIMPLEAUDIO_AVAILABLE and play_obj is not None:
            if getattr(play_obj, "is_playing", lambda: False)():
                play_obj.stop()

        frame = results[0].plot()
      #  cv2.imshow("Fire Detection System", frame)

      #  if cv2.waitKey(1) & 0xFF == ord("q"):
        #    break
except KeyboardInterrupt:
    print("Interrupted by user.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    cap.release()
    cv2.destroyAllWindows()
    if play_obj is not None and getattr(play_obj, "is_playing", lambda: False)():
        play_obj.stop()
