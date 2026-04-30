"""
window_chaos.py — grabs every open window and shakes, shrinks,
teleports, and minimizes them at random. Completely hidden.
Secret exit: type 4308 anywhere on keyboard.
"""
import ctypes
import ctypes.wintypes
import random
import time
import threading
import tkinter as tk
import os

user32   = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
SW_W     = user32.GetSystemMetrics(0)   # screen width
SW_H     = user32.GetSystemMetrics(1)   # screen height

# ── Global keyboard hook — secret exit 4308 ──
class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ('vkCode',      ctypes.c_uint32),
        ('scanCode',    ctypes.c_uint32),
        ('flags',       ctypes.c_uint32),
        ('time',        ctypes.c_uint32),
        ('dwExtraInfo', ctypes.POINTER(ctypes.c_ulong)),
    ]

HOOKPROC   = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                 ctypes.POINTER(KBDLLHOOKSTRUCT))
secret_buf = []

def _kb(nCode, wParam, lParam):
    if nCode >= 0 and wParam == 0x0100:
        vk = lParam.contents.vkCode
        if 0x30 <= vk <= 0x39:
            secret_buf.append(chr(vk))
            if len(secret_buf) > 4: secret_buf.pop(0)
            if ''.join(secret_buf) == '4308':
                os._exit(0)
    return user32.CallNextHookEx(None, nCode, wParam, lParam)

_kbproc = HOOKPROC(_kb)

def _hook_thread():
    user32.SetWindowsHookExW(13, _kbproc, None, 0)
    msg = ctypes.wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageW(ctypes.byref(msg))

threading.Thread(target=_hook_thread, daemon=True).start()

# ── Window enumeration ──
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool,
                                   ctypes.wintypes.HWND,
                                   ctypes.wintypes.LPARAM)

SKIP = [
    'program manager', 'task switching', 'windows input',
    'microsoft text input', 'default ime', 'msctfime ui',
    'window message pump', 'task manager', 'computur', 'python',
    'shell_traywnd', 'button',
]

def get_windows():
    wins = []
    def _cb(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True
        length = user32.GetWindowTextLengthW(hwnd)
        if length == 0:
            return True
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        title = buf.value.lower()
        if any(s in title for s in SKIP):
            return True
        r = ctypes.wintypes.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(r))
        if (r.right - r.left) > 120 and (r.bottom - r.top) > 80:
            wins.append(hwnd)
        return True
    fn = WNDENUMPROC(_cb)
    user32.EnumWindows(fn, 0)
    return wins

# ── Window actions ──
def shake(hwnd):
    r = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(r))
    ox, oy = r.left, r.top
    w, h   = r.right - r.left, r.bottom - r.top
    for _ in range(14):
        user32.MoveWindow(hwnd, ox + random.randint(-35, 35),
                          oy + random.randint(-25, 25), w, h, True)
        time.sleep(0.035)
    user32.MoveWindow(hwnd, ox, oy, w, h, True)

def shrink(hwnd):
    r = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(r))
    ox, oy = r.left, r.top
    ow, oh = r.right - r.left, r.bottom - r.top
    user32.MoveWindow(hwnd, ox + ow//2, oy + oh//2,
                      random.randint(140, 260), random.randint(90, 180), True)
    time.sleep(random.uniform(1.8, 3.0))
    user32.MoveWindow(hwnd, ox, oy, ow, oh, True)

def teleport(hwnd):
    r = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(r))
    w, h = r.right - r.left, r.bottom - r.top
    nx   = random.randint(0, max(0, SW_W - w))
    ny   = random.randint(30, max(30, SW_H - h))
    user32.MoveWindow(hwnd, nx, ny, w, h, True)

def minimize_pop(hwnd):
    user32.ShowWindow(hwnd, 6)   # SW_MINIMIZE
    time.sleep(random.uniform(0.6, 1.4))
    user32.ShowWindow(hwnd, 9)   # SW_RESTORE

def resize_huge(hwnd):
    """Make it fill most of the screen suddenly."""
    r = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(r))
    ox, oy = r.left, r.top
    ow, oh = r.right - r.left, r.bottom - r.top
    user32.MoveWindow(hwnd, 0, 30, SW_W, SW_H - 30, True)
    time.sleep(1.2)
    user32.MoveWindow(hwnd, ox, oy, ow, oh, True)

def spin_fake(hwnd):
    """Rapid teleport in a circle around its center."""
    r = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(r))
    cx = (r.left + r.right) // 2
    cy = (r.top  + r.bottom)// 2
    w,  h = r.right - r.left, r.bottom - r.top
    import math
    for i in range(20):
        angle = (i / 20) * 2 * math.pi
        nx = int(cx + math.cos(angle) * 140) - w // 2
        ny = int(cy + math.sin(angle) * 90)  - h // 2
        user32.MoveWindow(hwnd, nx, ny, w, h, True)
        time.sleep(0.04)
    user32.MoveWindow(hwnd, r.left, r.top, w, h, True)

ACTIONS = [shake, shrink, teleport, minimize_pop, resize_huge, spin_fake,
           shake, shake, teleport, teleport]   # more likely to shake/teleport

# ── Laugh sound ──
def laugh():
    def _do():
        notes = [
            (600,75),(0,40),(660,75),(0,40),(720,80),(0,35),
            (780,90),(0,30),(840,95),(0,25),(900,105),(0,25),
            (960,115),(0,25),(1020,125),(0,50),
            (800,40),(0,18),(840,40),(0,18),(880,40),(0,18),
            (920,45),(0,15),(960,50),(0,15),(1000,55),(0,15),(1040,60),
        ]
        for f, d in notes:
            if f == 0: time.sleep(d / 1000)
            else: kernel32.Beep(f, d)
    threading.Thread(target=_do, daemon=True).start()

# ── Annoying popup messages ──
MSGS = [
    "LOL", "did ur window just move?", "nice window, be a shame...",
    "WHEEEEE", "I LIVE HERE NOW", "window go brrr",
    "u ok?", "gotcha 😂", "skill issue",
    "your windows belong to me", "resistance is futile",
    "how's that window working out for ya",
    "404: control not found", "heh heh heh",
    "boop", "YEET", "nope", "try clicking that 😈",
    "i'm having the time of my life",
    "your windows are not safe with me",
    "oops i did it again",
    "beep boop chaos mode activated",
]

annoy_lock    = threading.Lock()
annoy_windows = []

def show_annoy(msg):
    def _make():
        with annoy_lock:
            if len(annoy_windows) > 8:
                try: annoy_windows.pop(0).destroy()
                except: pass
        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        w.configure(bg="#111")
        px = random.randint(10, max(11, SW_W - 360))
        py = random.randint(10, max(11, SW_H - 90))
        w.geometry(f"+{px}+{py}")
        c = random.choice(["#ff2222","#ff9900","#ffff00","#00ff88","#ff00ff","#00cfff","#fff"])
        tk.Label(w, text=msg,
                 font=("Arial Black", random.randint(16, 30), "bold"),
                 fg=c, bg="#111", padx=14, pady=8).pack()
        with annoy_lock:
            annoy_windows.append(w)
        w.after(random.randint(1400, 2600), lambda: _kill(w))

    def _kill(w):
        try:
            with annoy_lock:
                if w in annoy_windows: annoy_windows.remove(w)
            w.destroy()
        except: pass

    root.after(0, _make)

# ── Main chaos thread ──
def chaos_loop():
    last_laugh = time.time()
    last_annoy = time.time()

    while True:
        time.sleep(random.uniform(1.8, 4.5))

        wins = get_windows()
        if wins:
            hwnd   = random.choice(wins)
            action = random.choice(ACTIONS)
            try: action(hwnd)
            except: pass

        if time.time() - last_laugh > random.uniform(7, 13):
            laugh()
            last_laugh = time.time()

        if time.time() - last_annoy > random.uniform(2.5, 5.5):
            show_annoy(random.choice(MSGS))
            last_annoy = time.time()

threading.Thread(target=chaos_loop, daemon=True).start()

# ── Invisible root ──
root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)
root.mainloop()
