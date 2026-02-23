# VigiLance

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Security](https://img.shields.io/badge/Domain-Cybersecurity-red)
![Encryption](https://img.shields.io/badge/Logging-Encrypted-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![Status](https://img.shields.io/badge/Status-Active-success)

A Windows-based intrusion detection system designed to monitor unauthorized access to WhatsApp Desktop, capture forensic evidence, encrypt logs, and send real-time Telegram alerts.

---

## 🚀 Features

- Real-time WhatsApp Desktop activity detection
- Automated webcam-based intruder photo capture
- Encrypted forensic log storage (Fernet encryption)
- Instant Telegram alert notifications (with evidence)
- Password-protected control panel
- Standalone executable deployment via PyInstaller
- Lightweight background monitoring engine

---

## 🛠️ Tech Stack

- Python 3.12
- OpenCV
- Cryptography (Fernet)
- Psutil
- PyGetWindow
- Requests (Telegram Bot API)
- Tkinter (GUI Framework)
- PyInstaller (Executable Packaging)

---

## 📦 Installation & Usage (Development Mode)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/aroh3006/VigiLance.git
cd VigiLance
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run Background Monitoring Engine

```bash
python guard_v6.py
```

### 4️⃣ Run Control Panel

```bash
python control_panel.py
```

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


## 🏗️ Project Structure

```
VigiLance/
│
├── control_panel.py      # GUI controller
├── guard_v6.py           # Background monitoring engine
├── requirements.txt
├── VigiLance.ico
└── README.md
```

---

## 🧠 How It Works

1. The background engine continuously monitors:
   - Active window titles
   - Running processes

2. When WhatsApp Desktop activity is detected:
   - Webcam captures an image
   - WhatsApp process is terminated
   - Incident is encrypted and logged
   - Telegram alert is sent instantly

3. The control panel allows:
   - Secure start/stop functionality
   - Password-protected access

---

## 🔐 Security Concepts Implemented

- Endpoint Monitoring
- Process Inspection
- Real-Time Threat Detection
- Incident Response Automation
- Encrypted Logging
- Cloud-Based Alerting
- Defensive Security Engineering

---

## 📲 Telegram Alert Integration

- Custom Telegram Bot integration
- Instant alert messages upon detection
- Photo evidence delivery
- Remote monitoring capability

---

## 🧪 Executable Build (Production Mode)

```bash
python -m PyInstaller --onefile --noconsole guard_v6.py
```

```bash
python -m PyInstaller --onefile --noconsole --icon=VigiLance.ico --name VigiLance control_panel.py
```

---

## ⚠️ Disclaimer

This project is developed strictly for educational and authorized defensive security purposes only.
Do NOT deploy or use on systems without proper permission.

---

## 📌 Future Improvements

- Multi-application monitoring support
- Cloud log backup integration
- Admin dashboard with analytics
- Auto-start on system boot
- AI-based anomaly detection
- Cross-platform support (Linux/macOS)

---

## 👨‍💻 Author

**Aroh Maurya**

GitHub: https://github.com/aroh3006

---

⭐ If you found this project interesting, consider giving it a star.
