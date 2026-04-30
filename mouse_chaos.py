import ctypes
import ctypes.wintypes
import random
import time
import threading
import tkinter as tk
import math
import os

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
SW = user32.GetSystemMetrics(0)
SH = user32.GetSystemMetrics(1)

running = True
mode    = [0]
mode_timer = [time.time()]

# ── Annoying messages ──
MESSAGES = [
    "LOL",
    "hehehe",
    "u mad bro?",
    "gotcha!!",
    "try clicking that",
    "nope",
    "HAHAHA",
    "too slow",
    "good luck",
    "skill issue",
    "your mouse belongs to me now",
    "press ctrl+z to undo",      # it does nothing
    "have you tried turning it off and on again?",
    "this is fine  🔥",
    "404: mouse not found",
    "calculating mouse trajectory...",
    "why are you running",
    "bye bye cursor",
    "ur doing great sweetie",
    "can't stop won't stop",
    "oopsie",
    "wheeeee",
]

# ── Laughing sound via Beep tones ──
def laugh():
    def _laugh():
        # Ha ha ha rhythm — rising tones
        notes = [
            (600, 80), (0, 40),
            (650, 80), (0, 40),
            (700, 80), (0, 40),
            (750, 90), (0, 30),
            (800, 90), (0, 30),
            (850, 100),(0, 30),
            (900, 110),(0, 30),
            (950, 120),(0, 50),
            # fast giggle
            (800, 50),(0,20),(820,50),(0,20),(840,50),(0,20),(860,50),(0,20),
            (880,60),(0,15),(900,60),(0,15),(920,60),(0,15),
        ]
        for freq, dur in notes:
            if freq == 0:
                time.sleep(dur / 1000)
            else:
                kernel32.Beep(freq, dur)
    threading.Thread(target=_laugh, daemon=True).start()

# ── Floating annoy popup ──
annoy_lock = threading.Lock()
annoy_windows = []

def show_annoy(msg):
    def _make():
        with annoy_lock:
            if len(annoy_windows) > 6:
                try:
                    old = annoy_windows.pop(0)
                    old.destroy()
                except: pass

        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        w.configure(bg="#111111")

        # random screen position
        px = random.randint(20, max(21, SW - 320))
        py = random.randint(20, max(21, SH - 80))
        w.geometry(f"+{px}+{py}")

        lbl = tk.Label(w, text=msg,
                       font=("Arial Black", random.randint(14, 26), "bold"),
                       fg=random.choice(["#ff2222","#ff9900","#ffff00","#00ff88","#ff00ff","#00cfff"]),
                       bg="#111111", padx=14, pady=8)
        lbl.pack()

        with annoy_lock:
            annoy_windows.append(w)

        # auto-destroy after 1.8–3s
        delay = random.randint(1800, 3000)
        w.after(delay, lambda: _kill(w))

    def _kill(w):
        try:
            with annoy_lock:
                if w in annoy_windows:
                    annoy_windows.remove(w)
            w.destroy()
        except: pass

    root.after(0, _make)

# ── Mouse chaos thread ──
def chaos_loop():
    angle = [0]
    cx, cy = SW // 2, SH // 2
    radius = [300]
    last_laugh = [time.time()]
    last_annoy = [time.time()]

    while running:
        m = mode[0]

        if m == 0:
            user32.SetCursorPos(random.randint(0, SW), random.randint(0, SH))
            time.sleep(random.uniform(0.02, 0.08))

        elif m == 1:
            angle[0] += 18
            x = int(cx + math.cos(math.radians(angle[0])) * radius[0])
            y = int(cy + math.sin(math.radians(angle[0])) * radius[0])
            user32.SetCursorPos(max(0, min(SW, x)), max(0, min(SH, y)))
            time.sleep(0.02)

        elif m == 2:
            pt = ctypes.wintypes.POINT()
            user32.GetCursorPos(ctypes.byref(pt))
            user32.SetCursorPos(
                max(0, min(SW, pt.x + random.randint(-80, 80))),
                max(0, min(SH, pt.y + random.randint(-80, 80)))
            )
            time.sleep(0.01)

        elif m == 3:
            for x in range(0, SW, 60):
                if not running: break
                y = 0 if (x // 60) % 2 == 0 else SH
                user32.SetCursorPos(x, y)
                time.sleep(0.03)

        # switch mode every 4 seconds
        if time.time() - mode_timer[0] > 4:
            mode[0] = (mode[0] + 1) % 4
            mode_timer[0] = time.time()

        # laugh every 7–14 seconds
        if time.time() - last_laugh[0] > random.uniform(7, 14):
            laugh()
            last_laugh[0] = time.time()

        # annoy message every 2.5–5 seconds
        if time.time() - last_annoy[0] > random.uniform(2.5, 5):
            msg = random.choice(MESSAGES)
            show_annoy(msg)
            last_annoy[0] = time.time()

threading.Thread(target=chaos_loop, daemon=True).start()

# ── Hidden root window (invisible, just keeps tkinter alive) ──
root = tk.Tk()
root.withdraw()   # completely hidden — no window, no taskbar icon
root.attributes("-topmost", True)

# Keep alive forever — no exit button, no key sequence
root.mainloop()
