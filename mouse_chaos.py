import ctypes
import random
import time
import threading
import tkinter as tk
import math

user32 = ctypes.windll.user32
SW = user32.GetSystemMetrics(0)
SH = user32.GetSystemMetrics(1)

running = True
mode = [0]  # cycle through chaos modes
mode_timer = [time.time()]

def chaos_loop():
    angle = [0]
    cx, cy = SW // 2, SH // 2
    radius = [300]

    while running:
        m = mode[0]

        if m == 0:
            # pure random teleport
            user32.SetCursorPos(random.randint(0, SW), random.randint(0, SH))
            time.sleep(random.uniform(0.02, 0.08))

        elif m == 1:
            # spin in a circle
            angle[0] += 18
            x = int(cx + math.cos(math.radians(angle[0])) * radius[0])
            y = int(cy + math.sin(math.radians(angle[0])) * radius[0])
            x = max(0, min(SW, x))
            y = max(0, min(SH, y))
            user32.SetCursorPos(x, y)
            time.sleep(0.02)

        elif m == 2:
            # shake violently near current pos
            pt = ctypes.wintypes.POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
            user32.SetCursorPos(
                max(0, min(SW, pt.x + random.randint(-80, 80))),
                max(0, min(SH, pt.y + random.randint(-80, 80)))
            )
            time.sleep(0.01)

        elif m == 3:
            # zigzag across screen
            for x in range(0, SW, 60):
                if not running: break
                y = 0 if (x // 60) % 2 == 0 else SH
                user32.SetCursorPos(x, y)
                time.sleep(0.03)

        # switch mode every 4 seconds
        if time.time() - mode_timer[0] > 4:
            mode[0] = (mode[0] + 1) % 4
            mode_timer[0] = time.time()

threading.Thread(target=chaos_loop, daemon=True).start()

root = tk.Tk()
root.title("Mouse Chaos")
root.attributes("-topmost", True)
root.geometry("240x95+10+10")
root.resizable(False, False)
root.configure(bg="#1a1a1a")

tk.Label(root, text="Mouse Chaos ACTIVE!", font=("Arial", 11, "bold"), fg="red", bg="#1a1a1a").pack(pady=8)

def stop():
    global running
    running = False
    root.destroy()

tk.Button(root, text="STOP  (type 4308)", command=stop,
          bg="#ff4444", fg="white", font=("Arial", 10), relief="flat", padx=10).pack()

secret = [0]
sequence = [str(d) for d in [4, 3, 0, 8]]
def on_key(event):
    ch = event.char
    if ch == sequence[secret[0]]:
        secret[0] += 1
        if secret[0] == len(sequence):
            stop()
    else:
        secret[0] = 0
root.bind("<Key>", on_key)
root.mainloop()
