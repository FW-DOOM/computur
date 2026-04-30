import tkinter as tk
import random
import time
import threading

messages = [
    "Downloading more RAM...",
    "Installing common sense... failed.",
    "Updating your personality (0%)...",
    "Backing up your memes...",
    "Scanning for existential threats...",
    "Optimizing coffee consumption habits...",
    "Reticulating splines...",
    "Reversing the polarity...",
    "Calibrating flux capacitor...",
    "Counting to infinity... please wait.",
    "Downloading the internet...",
    "Convincing CPU to try harder...",
    "Encrypting your thoughts...",
    "Searching for the any key...",
    "Negotiating with hard drive...",
    "Loading loading screen...",
    "Updating update manager...",
    "Rebooting the matrix...",
    "Compiling excuses...",
    "Installing updates that will never finish...",
]

root = tk.Tk()
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.configure(bg="#0078d7")
root.title("")

frame = tk.Frame(root, bg="#0078d7")
frame.place(relx=0.5, rely=0.4, anchor="center")

# Windows logo (simple text version)
logo = tk.Label(frame, text="⊞", font=("Segoe UI", 80), fg="white", bg="#0078d7")
logo.pack(pady=10)

title_lbl = tk.Label(frame, text="Working on updates\n32% complete", font=("Segoe UI Light", 36), fg="white", bg="#0078d7")
title_lbl.pack(pady=10)

sub_lbl = tk.Label(frame, text="Don't turn off your PC. This will take a while.", font=("Segoe UI", 14), fg="white", bg="#0078d7")
sub_lbl.pack()

progress_frame = tk.Frame(frame, bg="#0078d7")
progress_frame.pack(pady=20)

dots = [tk.Label(progress_frame, text="●", font=("Segoe UI", 18), fg="white", bg="#0078d7") for _ in range(5)]
for d in dots:
    d.pack(side="left", padx=6)

status_lbl = tk.Label(root, text="", font=("Segoe UI", 11), fg="white", bg="#0078d7")
status_lbl.place(relx=0.5, rely=0.75, anchor="center")

pct = [3]
msg_idx = [0]
running = True

def animate():
    active = [0]
    while running:
        for i, d in enumerate(dots):
            d.config(fg="white" if i == active[0] else "#005a9e")
        active[0] = (active[0] + 1) % len(dots)
        time.sleep(0.3)

def update_progress():
    while running and pct[0] < 99:
        increment = random.uniform(0.05, 0.4)
        pct[0] = min(pct[0] + increment, 98)
        p = int(pct[0])
        title_lbl.config(text=f"Working on updates\n{p}% complete")
        msg_idx[0] = (msg_idx[0] + 1) % len(messages)
        status_lbl.config(text=messages[msg_idx[0]])
        time.sleep(random.uniform(0.5, 1.5))

threading.Thread(target=animate, daemon=True).start()
threading.Thread(target=update_progress, daemon=True).start()

# secret exit: type 4308
secret = [0]
sequence = [str(d) for d in [4, 3, 0, 8]]

def on_key(event):
    global running
    ch = event.char
    if ch == sequence[secret[0]]:
        secret[0] += 1
        if secret[0] == len(sequence):
            running = False
            root.destroy()
    else:
        secret[0] = 0

root.bind("<Key>", on_key)
root.overrideredirect(True)
root.mainloop()
