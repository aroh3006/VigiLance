import time
import cv2
from datetime import datetime
import os
import pygetwindow as gw
import psutil
import base64
from cryptography.fernet import Fernet
import requests


# ================= CONFIG =================

WINDOW_KEYWORD = "WhatsApp"
PROCESS_NAME = "WhatsApp.Root.exe"

LOG_FOLDER = "logs"
KEY_FILE = "key.key"

# ---- TELEGRAM CONFIG ----
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
# --------------------------


# ================= SETUP =================

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)


# Generate encryption key (first time only)
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

# Load key
with open(KEY_FILE, "rb") as f:
    key = f.read()

cipher = Fernet(key)


# ================= FUNCTIONS =================

def is_whatsapp_active():
    try:
        win = gw.getActiveWindow()

        if win and WINDOW_KEYWORD.lower() in win.title.lower():
            return True
    except:
        pass

    return False


def is_whatsapp_running():
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == PROCESS_NAME:
                return True
        except:
            pass

    return False


def kill_whatsapp():
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == PROCESS_NAME:
                proc.kill()
        except:
            pass


# -------- TELEGRAM ALERT -------- #

def send_telegram_alert(image_path, timestamp):

    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

        caption = (
            "🚨 VigiLance Alert\n\n"
            "Unauthorized WhatsApp Access Detected\n"
            f"Time: {timestamp}"
        )

        data = {
            "chat_id": CHAT_ID,
            "caption": caption
        }

        with open(image_path, "rb") as photo:
            files = {
                "photo": photo
            }

            requests.post(url, data=data, files=files, timeout=15)

    except Exception as e:
        print("Telegram Error:", e)


# -------- CAPTURE + ENCRYPT -------- #

def capture_encrypt_and_alert():

    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        return

    ret, frame = cam.read()

    if not ret:
        cam.release()
        return


    # Save temp image (for telegram)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    temp_img = f"temp_{timestamp}.jpg"

    cv2.imwrite(temp_img, frame)


    # Send Telegram alert
    send_telegram_alert(temp_img, timestamp)


    # Encode image
    ret, buffer = cv2.imencode(".jpg", frame)
    img_bytes = buffer.tobytes()

    img_base64 = base64.b64encode(img_bytes).decode()


    # Log data
    log_data = f"""
Time: {timestamp}
App: WhatsApp
Event: Unauthorized Access

Image:
{img_base64}
    """.strip()


    # Encrypt
    encrypted_data = cipher.encrypt(log_data.encode())


    # Save encrypted log
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".vlog"
    filepath = os.path.join(LOG_FOLDER, filename)

    with open(filepath, "wb") as f:
        f.write(encrypted_data)


    # Cleanup temp
    if os.path.exists(temp_img):
        os.remove(temp_img)


    cam.release()


# ================= MAIN =================

print("VigiLance Engine Started")
print("Encrypted Logging + Telegram Alerts Enabled")


was_active = False


while True:

    window_active = is_whatsapp_active()
    process_running = is_whatsapp_running()

    active = window_active and process_running


    if active and not was_active:

        capture_encrypt_and_alert()
        kill_whatsapp()


    was_active = active

    time.sleep(1.5)
