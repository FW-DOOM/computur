import ctypes
import ctypes.wintypes
import random
import time
import threading
import tkinter as tk
import math
import os

user32  = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
SW = user32.GetSystemMetrics(0)
SH = user32.GetSystemMetrics(1)

running    = True
mode       = [0]
mode_timer = [time.time()]

# ── Global keyboard hook — works even with hidden window ──
class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ('vkCode',      ctypes.c_uint32),
        ('scanCode',    ctypes.c_uint32),
        ('flags',       ctypes.c_uint32),
        ('time',        ctypes.c_uint32),
        ('dwExtraInfo', ctypes.POINTER(ctypes.c_ulong)),
    ]

WH_KEYBOARD_LL = 13
WM_KEYDOWN     = 0x0100
secret_buf     = []

HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int,
                               ctypes.POINTER(KBDLLHOOKSTRUCT))

def _kb_proc(nCode, wParam, lParam):
    if nCode >= 0 and wParam == WM_KEYDOWN:
        vk = lParam.contents.vkCode
        if 0x30 <= vk <= 0x39:          # digit keys 0–9
            secret_buf.append(chr(vk))
            if len(secret_buf) > 4:
                secret_buf.pop(0)
            if ''.join(secret_buf) == '4308':
                os._exit(0)
    return user32.CallNextHookEx(None, nCode, wParam, lParam)

_kb_hook_proc = HOOKPROC(_kb_proc)

def _hook_thread():
    user32.SetWindowsHookExW(WH_KEYBOARD_LL, _kb_hook_proc, None, 0)
    msg = ctypes.wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageW(ctypes.byref(msg))

threading.Thread(target=_hook_thread, daemon=True).start()

# ── Annoying messages ──
MESSAGES = [
    "LOL", "hehehe", "u mad bro?", "gotcha!!",
    "try clicking that", "nope", "HAHAHA",
    "too slow 😂", "good luck", "SKILL ISSUE",
    "your mouse belongs to me now",
    "press ctrl+z to undo",          # does nothing lol
    "this is fine  🔥",
    "404: mouse not found",
    "why are you running",
    "bye bye cursor ✌",
    "ur doing great sweetie",
    "can't stop won't stop",
    "resistance is futile",
    "you thought 💀",
    "nice try lmao",
    "click me... oh wait",
    "i live here now",
    "no.",
    "heh heh heh",
    "imagine using your mouse 😂",
    "WHEEEEE",
    "get pranked",
    "have u tried turning it off?",
    "just give up bro",
    "i'm having so much fun",
    "oops wrong way",
    "are you ok?",
    "🤣🤣🤣",
]

# ── Laughing sound ──
def laugh():
    def _do():
        notes = [
            (600,80),(0,40),(650,80),(0,40),(700,80),(0,40),
            (750,90),(0,30),(800,90),(0,30),(850,100),(0,25),
            (900,110),(0,25),(960,130),(0,50),
            # fast giggle burst
            (800,45),(0,18),(830,45),(0,18),(860,45),(0,18),
            (890,50),(0,15),(920,50),(0,15),(950,55),(0,15),
            (980,60),(0,15),(1010,65),
        ]
        for freq, dur in notes:
            if freq == 0: time.sleep(dur / 1000)
            else: kernel32.Beep(freq, dur)
    threading.Thread(target=_do, daemon=True).start()

# ── Floating annoy popups ──
annoy_lock    = threading.Lock()
annoy_windows = []

def show_annoy(msg):
    def _make():
        with annoy_lock:
            if len(annoy_windows) > 10:
                try:
                    old = annoy_windows.pop(0)
                    old.destroy()
                except Exception:
                    pass

        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        w.configure(bg="#111111")

        px = random.randint(10, max(11, SW - 350))
        py = random.randint(10, max(11, SH - 90))
        w.geometry(f"+{px}+{py}")

        color = random.choice([
            "#ff2222", "#ff9900", "#ffff00",
            "#00ff88", "#ff00ff", "#00cfff", "#ffffff"
        ])
        size = random.randint(18, 34)
        tk.Label(w, text=msg,
                 font=("Arial Black", size, "bold"),
                 fg=color, bg="#111111", padx=16, pady=10).pack()

        with annoy_lock:
            annoy_windows.append(w)

        w.after(random.randint(1400, 2600), lambda: _kill(w))

    def _kill(w):
        try:
            with annoy_lock:
                if w in annoy_windows:
                    annoy_windows.remove(w)
            w.destroy()
        except Exception:
            pass

    root.after(0, _make)

# ── Mouse chaos thread ──
def chaos_loop():
    angle      = [0]
    cx, cy     = SW // 2, SH // 2
    last_laugh = [time.time()]
    last_annoy = [time.time()]

    while running:
        m = mode[0]

        if m == 0:
            # random teleport
            user32.SetCursorPos(random.randint(0, SW), random.randint(0, SH))
            time.sleep(random.uniform(0.02, 0.07))

        elif m == 1:
            # circle spin
            angle[0] += 20
            x = int(cx + math.cos(math.radians(angle[0])) * 300)
            y = int(cy + math.sin(math.radians(angle[0])) * 300)
            user32.SetCursorPos(max(0, min(SW, x)), max(0, min(SH, y)))
            time.sleep(0.018)

        elif m == 2:
            # violent shake
            pt = ctypes.wintypes.POINT()
            user32.GetCursorPos(ctypes.byref(pt))
            user32.SetCursorPos(
                max(0, min(SW, pt.x + random.randint(-100, 100))),
                max(0, min(SH, pt.y + random.randint(-100, 100)))
            )
            time.sleep(0.009)

        elif m == 3:
            # zigzag
            for x in range(0, SW, 55):
                if not running:
                    break
                y = 0 if (x // 55) % 2 == 0 else SH
                user32.SetCursorPos(x, y)
                time.sleep(0.025)

        # switch mode every 4 s
        if time.time() - mode_timer[0] > 4:
            mode[0] = (mode[0] + 1) % 4
            mode_timer[0] = time.time()

        # laugh every 5–10 s
        if time.time() - last_laugh[0] > random.uniform(5, 10):
            laugh()
            last_laugh[0] = time.time()

        # annoy message every 1.5–3.5 s
        if time.time() - last_annoy[0] > random.uniform(1.5, 3.5):
            show_annoy(random.choice(MESSAGES))
            last_annoy[0] = time.time()

threading.Thread(target=chaos_loop, daemon=True).start()

# ── Invisible root — no window, no taskbar, no exit ──
root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)
root.mainloop()
