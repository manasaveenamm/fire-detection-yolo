# Fire Detection System using YOLO26s

This project implements a real-time fire detection system using a custom-trained YOLO26s model. It captures video from a webcam, detects fire and triggers alerts such as alarm sound, email notifications and event logging.

---

## Project Structure

```text
FIRE-DETECTION-YOLO/                
│── model/
│   └── best.pt             # Trained YOLO26s model
│── output/                 # Logs and outputs
│── .gitignore              # Git ignore file
│── Alarm.wav               # Alarm sound file
│── detect.py               # Main detection script
│── train.py                # Training script
│── requirements.txt        # Dependencies
│── yolo26s.pt              # Base YOLO26s model
│── README.md
```

---

## Features

* Real-time fire detection using webcam
* Custom-trained YOLO26s model
* Alarm sound on fire detection
* Email alert system
* Fire event logging
* Cooldown mechanism to prevent repeated alerts

---

## Requirements

* Python 3.9 or above
* Webcam
* Trained model file: `model/best.pt`
* Alarm file: `Alarm.wav`

---

## Installation (macOS)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fire-detection-yolo.git
cd fire-detection-yolo
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate environment

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the project

```bash
python3 detect.py
```

---

## Installation (Windows)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fire-detection-yolo.git
cd fire-detection-yolo
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate environment

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the project

```bash
python detect.py
```

---

## How It Works

1. The YOLO26s model processes each frame from the webcam
2. If fire is detected with sufficient confidence:

   * Detection is confirmed across multiple frames
   * Alert system is triggered
3. The system performs:

   * Alarm sound playback
   * Email notification
   * Logging in `output/log.txt`

---

## Email Configuration

Update the following inside `detect.py`:

```python
sender_email = "your_email@gmail.com"
receiver_email = "receiver_email@gmail.com"
app_password = "your_app_password"
```

Use an application-specific password instead of your main email password.

---

## Model Information

* Architecture: YOLO26s
* Trained model: `model/best.pt`
* Base model: `yolo26s.pt`
* Class: Fire

---

## Output

On fire detection:

* Alarm sound is triggered
* Email alert is sent
* Event is logged in `output/log.txt`
* Detection is displayed on screen

---

## Training

Training script is available in:

```text
train.py
```

Dataset should be placed in:

```text
dataset/
```

Trained model should be saved as:

```text
model/best.pt
```

---

## Notes

* Dataset and model weights are not included in the repository
* Ensure `.venv/`, dataset and output files are ignored using `.gitignore`
* Detection accuracy depends on dataset quality
* Include small flame data (matchstick, lighter) for better performance

---

## License

This project is for educational and research purposes only.