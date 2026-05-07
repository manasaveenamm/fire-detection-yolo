import cv2
from ultralytics import YOLO
import simpleaudio as sa # pyright: ignore[reportMissingImports]
import smtplib
from email.mime.text import MIMEText
import threading
import time

model = YOLO("model/best.pt")

print("Model classes:", model.names)

def send_email_alert():
    def send():
        sender_email = "harsharover2002@gmail.com"
        receiver_email = "harshapower2002@gmail.com"
        app_password = "odaq gwza eaud qiyt"

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

cap = cv2.VideoCapture(0)

wave_obj = sa.WaveObject.from_wave_file("Alarm.wav")
play_obj = None

fire_frames = 0
last_alert_time = 0
COOLDOWN = 2  

while True:
    ret, frame = cap.read()
    if not ret:
        break

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

        if play_obj is not None and play_obj.is_playing():
            play_obj.stop()

        play_obj = wave_obj.play()

        send_email_alert()
        log_fire_event()

        last_alert_time = current_time

    if fire_frames == 0:
        if play_obj is not None and play_obj.is_playing():
            play_obj.stop()

    frame = results[0].plot()
    cv2.imshow("Fire Detection System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()