# VigiLance
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![Security](https://img.shields.io/badge/Focus-Cybersecurity-red)
![License](https://img.shields.io/badge/License-MIT-green)

Windows-based Intrusion Detection System for WhatsApp Desktop.

VigiLance monitors unauthorized access attempts, captures forensic evidence, encrypts logs, and sends real-time Telegram alerts.

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

## 📂 Project Structure

VigiLance/
│
├── control_panel.py      # GUI controller
├── guard_v6.py           # Background monitoring engine
├── requirements.txt
├── VigiLance.ico
└── README.md

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
