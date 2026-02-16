import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import hashlib
import os
import psutil
import sys
import base64
from cryptography.fernet import Fernet
import cv2
import numpy as np


# ---------------- Path Handling ---------------- #

def get_exe_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = get_exe_dir()

GUARD_EXE = os.path.join(BASE_DIR, "guard_v6.exe")
ICON_PATH = os.path.join(BASE_DIR, "VigiLance.ico")

LOG_FOLDER = os.path.join(BASE_DIR, "logs")
KEY_FILE = os.path.join(BASE_DIR, "key.key")


# ---------------- Security ---------------- #

PASSWORD_HASH = hashlib.sha256("Aroh@2026".encode()).hexdigest()


def check_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest() == PASSWORD_HASH


# ---------------- Load Encryption Key ---------------- #

if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        key = f.read()
    cipher = Fernet(key)
else:
    cipher = None


# ---------------- Guard Control ---------------- #

def is_guard_running():
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == "guard_v6.exe":
                return True
        except:
            pass
    return False


def start_guard():

    if is_guard_running():
        messagebox.showinfo("Info", "Protection already running")
        status_label.config(text="Status: ACTIVE", fg="green")
        return

    if not os.path.exists(GUARD_EXE):
        messagebox.showerror("Error", "guard_v6.exe not found")
        return

    try:
        subprocess.Popen([GUARD_EXE])
        status_label.config(text="Status: ACTIVE", fg="green")
        messagebox.showinfo("Success", "Protection Enabled")

    except:
        messagebox.showerror("Error", "Failed to start guard")


def stop_guard():

    pw = password_entry.get()

    if not check_password(pw):
        messagebox.showerror("Error", "Wrong Password!")
        return

    stopped = False

    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == "guard_v6.exe":
                proc.kill()
                stopped = True
        except:
            pass

    if stopped:
        status_label.config(text="Status: STOPPED", fg="red")
        messagebox.showinfo("Success", "Protection Disabled")
    else:
        messagebox.showinfo("Info", "Guard not running")


# ---------------- Log Viewer ---------------- #

def view_logs():

    pw = password_entry.get()

    if not check_password(pw):
        messagebox.showerror("Error", "Wrong Password!")
        return

    if not cipher:
        messagebox.showerror("Error", "Encryption key missing")
        return

    if not os.path.exists(LOG_FOLDER):
        messagebox.showinfo("Info", "No logs found")
        return


    logs = [f for f in os.listdir(LOG_FOLDER) if f.endswith(".vlog")]

    if not logs:
        messagebox.showinfo("Info", "No logs found")
        return


    win = tk.Toplevel(root)
    win.title("VigiLance - Log Dashboard")
    win.geometry("650x400")
    win.resizable(False, False)

    if os.path.exists(ICON_PATH):
        win.iconbitmap(ICON_PATH)


    tk.Label(
        win,
        text="Intrusion Logs",
        font=("Arial", 16, "bold")
    ).pack(pady=10)


    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True, padx=10, pady=5)


    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")


    listbox = tk.Listbox(
        frame,
        width=80,
        height=15,
        yscrollcommand=scrollbar.set
    )
    listbox.pack(side="left", fill="both", expand=True)

    scrollbar.config(command=listbox.yview)


    for log in sorted(logs, reverse=True):
        listbox.insert("end", log)


    # -------- Buttons -------- #

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=10)


    def get_selected():

        sel = listbox.curselection()

        if not sel:
            messagebox.showwarning("Warning", "Select a log first")
            return None

        return listbox.get(sel[0])


    def decrypt_log(filename):

        path = os.path.join(LOG_FOLDER, filename)

        with open(path, "rb") as f:
            encrypted = f.read()

        decrypted = cipher.decrypt(encrypted).decode()

        return decrypted


    def extract_image(data):

        if "Image:" not in data:
            return None

        img_b64 = data.split("Image:")[1].strip()

        img_bytes = base64.b64decode(img_b64)

        nparr = np.frombuffer(img_bytes, np.uint8)

        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        return img


    def preview():

        file = get_selected()
        if not file:
            return

        try:
            data = decrypt_log(file)
            img = extract_image(data)

            if img is None:
                raise Exception("No image found")


            cv2.imshow("VigiLance - Preview", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        except Exception as e:
            messagebox.showerror("Error", str(e))


    def export():

        file = get_selected()
        if not file:
            return

        try:
            data = decrypt_log(file)
            img = extract_image(data)

            if img is None:
                raise Exception("No image found")


            path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("Image", "*.jpg")]
            )

            if not path:
                return

            cv2.imwrite(path, img)

            messagebox.showinfo("Success", "Image exported")

        except Exception as e:
            messagebox.showerror("Error", str(e))


    def delete():

        file = get_selected()
        if not file:
            return

        confirm = messagebox.askyesno(
            "Confirm",
            "Delete this log permanently?"
        )

        if not confirm:
            return

        try:
            os.remove(os.path.join(LOG_FOLDER, file))

            listbox.delete(listbox.curselection())

            messagebox.showinfo("Success", "Log deleted")

        except Exception as e:
            messagebox.showerror("Error", str(e))


    tk.Button(
        btn_frame,
        text="Preview",
        width=15,
        command=preview
    ).grid(row=0, column=0, padx=5)


    tk.Button(
        btn_frame,
        text="Export",
        width=15,
        command=export
    ).grid(row=0, column=1, padx=5)


    tk.Button(
        btn_frame,
        text="Delete",
        width=15,
        command=delete
    ).grid(row=0, column=2, padx=5)


# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("VigiLance")

if os.path.exists(ICON_PATH):
    root.iconbitmap(ICON_PATH)

root.geometry("340x370")
root.resizable(False, False)


# Title

title = tk.Label(
    root,
    text="VigiLance",
    font=("Arial", 18, "bold")
)
title.pack(pady=(10, 2))


subtitle = tk.Label(
    root,
    text="WhatsApp Intrusion Detection System",
    font=("Arial", 10),
    fg="gray"
)
subtitle.pack(pady=(0, 10))


# Password

tk.Label(root, text="Enter Password:").pack()

password_entry = tk.Entry(root, show="*", width=26)
password_entry.pack(pady=5)


# Buttons

start_btn = tk.Button(
    root,
    text="Start Protection",
    width=25,
    height=2,
    command=start_guard
)
start_btn.pack(pady=5)


stop_btn = tk.Button(
    root,
    text="Stop Protection",
    width=25,
    height=2,
    command=stop_guard
)
stop_btn.pack(pady=5)


view_btn = tk.Button(
    root,
    text="View Logs",
    width=25,
    height=2,
    command=view_logs
)
view_btn.pack(pady=5)


# Status

status_label = tk.Label(
    root,
    text="Status: STOPPED",
    fg="red",
    font=("Arial", 11, "bold")
)
status_label.pack(pady=12)


root.mainloop()
