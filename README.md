# VigiLance
Windows-based intrusion detection system with encrypted forensic logging and real-time Telegram alerts for WhatsApp Desktop.

Author : Aroh Maurya

---

## 🚀 Features

- Real-time WhatsApp activity detection
- Webcam-based intruder photo capture (OpenCV)
- Secure process termination
- Encrypted forensic logging (Fernet encryption)
- Password-protected control panel
- Telegram bot integration for remote alerts
- Standalone Windows executable deployment

---

## 🏗️ Architecture

1. guard_v6.py  
   - Background monitoring engine  
   - Detects WhatsApp foreground activity  
   - Captures image evidence  
   - Encrypts logs  
   - Sends Telegram alerts  

2. control_panel.py  
   - GUI-based protection control  
   - Password authentication  
   - Start / Stop protection  
   - View encrypted logs  

---

## 🛠️ Technologies Used

- Python
- OpenCV
- Tkinter
- Cryptography (Fernet encryption)
- Psutil
- PyGetWindow
- Telegram Bot API
- PyInstaller

---

## ⚠️ Disclaimer

This project was built for educational and cybersecurity learning purposes only.
