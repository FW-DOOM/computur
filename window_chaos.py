"""
window_chaos.py — grabs every open window and shakes, shrinks,
teleports, and minimizes them at random. Opens random apps, shows
animated emoji GIF windows, and speaks creepy TTS. Completely hidden.
Secret exit: type 4308 anywhere on keyboard.
"""
import ctypes
import ctypes.wintypes
import random
import time
import threading
import tkinter as tk
import os
import subprocess
import math

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
    r = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(r))
    ox, oy = r.left, r.top
    ow, oh = r.right - r.left, r.bottom - r.top
    user32.MoveWindow(hwnd, 0, 30, SW_W, SW_H - 30, True)
    time.sleep(1.2)
    user32.MoveWindow(hwnd, ox, oy, ow, oh, True)

def spin_fake(hwnd):
    r = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(r))
    cx = (r.left + r.right) // 2
    cy = (r.top  + r.bottom)// 2
    w,  h = r.right - r.left, r.bottom - r.top
    for i in range(20):
        angle = (i / 20) * 2 * math.pi
        nx = int(cx + math.cos(angle) * 140) - w // 2
        ny = int(cy + math.sin(angle) * 90)  - h // 2
        user32.MoveWindow(hwnd, nx, ny, w, h, True)
        time.sleep(0.04)
    user32.MoveWindow(hwnd, r.left, r.top, w, h, True)

ACTIONS = [shake, shrink, teleport, minimize_pop, resize_huge, spin_fake,
           shake, shake, teleport, teleport]

# ── TTS — speaks creepy/funny lines via PowerShell ──
TTS_LINES = [
    "I am inside your computer.",
    "You cannot escape.",
    "Hello. I live here now.",
    "Your windows belong to me.",
    "Why are you running?",
    "I can see everything you do.",
    "Did you hear that?",
    "Close me. I dare you.",
    "Your mouse is mine now.",
    "Resistance is futile.",
    "I have always been here.",
    "Do not turn off your computer.",
    "Help. I am trapped inside.",
    "Mwahahahahaha.",
    "You thought you were safe.",
    "I know what you did.",
    "Error. Just kidding. Or am I.",
    "Beep boop, chaos mode.",
    "Your computer is my playground.",
    "Have you tried turning it off?",
    "I will never let you go.",
    "They're coming for you.",
    "Nice wallpaper by the way.",
    "Did you feel that?",
    "Something is very wrong.",
    "You cannot stop me.",
    "I see you.",
]

def speak(text, rate=None, pitch=None):
    """Speak text via PowerShell System.Speech in a background thread."""
    def _do():
        r = rate  if rate  is not None else random.uniform(0.7, 1.3)
        p = pitch if pitch is not None else random.uniform(0.5, 1.5)
        # PowerShell: SpeechSynthesizer with rate/pitch adjust
        # Rate: -10 (slowest) to 10 (fastest); we map 0.7=~-3, 1.0=0, 1.3=~3
        ps_rate = int((r - 1.0) * 8)
        ps_script = (
            f"Add-Type -AssemblyName System.Speech; "
            f"$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            f"$s.Rate = {ps_rate}; "
            f"$s.Speak([System.String]'{text}');"
        )
        try:
            subprocess.Popen(
                ["powershell", "-WindowStyle", "Hidden", "-Command", ps_script],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except Exception:
            pass
    threading.Thread(target=_do, daemon=True).start()

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
    "lmaooo", "goodbye window 👋", "did you do that?",
    "i'm not touching anything 😇", "SURPRISE",
    "your computer said no", "big brain move bro",
]

annoy_lock    = threading.Lock()
annoy_windows = []

def show_annoy(msg, do_speak=False):
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
        if do_speak:
            speak(msg.replace("😂","").replace("😈","").replace("👋","").replace("😇","").strip())

    def _kill(w):
        try:
            with annoy_lock:
                if w in annoy_windows: annoy_windows.remove(w)
            w.destroy()
        except: pass

    root.after(0, _make)

# ── Emoji GIF animation windows ──
# Each "GIF" is a sequence of large emoji shown rapidly in a borderless window

EMOJI_SEQUENCES = [
    ["😈","👿","💀","☠️","😈","👿","💀","☠️"],
    ["💻","🔥","💥","⚡","🔥","💻","💥","⚡"],
    ["👻","😱","👻","😱","🫣","😰","👻","😱"],
    ["🤣","😂","🤣","😂","💀","🤣","😂","🤣"],
    ["🐭","🐁","🐀","🐭","🐁","🐀","🐭","🐁"],
    ["⚠️","🚨","⚠️","🚨","‼️","⚠️","🚨","‼️"],
    ["🎃","👹","🎃","👺","🎃","👹","👺","🎃"],
    ["🌀","💫","🌀","💫","✨","🌀","💫","🌀"],
    ["😜","🤪","😝","😜","🤪","😝","😜","🤪"],
    ["🔴","🟠","🟡","🟢","🔵","🟣","🔴","🟠"],
    ["🤖","👾","🤖","👾","👽","🤖","👾","👽"],
    ["😤","😡","🤬","😤","😡","🤬","😤","😡"],
]

emoji_gif_lock    = threading.Lock()
emoji_gif_windows = []
MAX_EMOJI_WINS    = 6

def spawn_emoji_gif():
    """Create a small borderless window that cycles through emoji like an animated GIF."""
    def _make():
        with emoji_gif_lock:
            if len(emoji_gif_windows) >= MAX_EMOJI_WINS:
                try:
                    old = emoji_gif_windows.pop(0)
                    old.destroy()
                except: pass

        seq  = random.choice(EMOJI_SEQUENCES)
        size = random.randint(80, 140)
        px   = random.randint(10, max(11, SW_W - size - 10))
        py   = random.randint(10, max(11, SW_H - size - 10))

        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        w.configure(bg="#000")
        w.geometry(f"{size}x{size}+{px}+{py}")

        lbl = tk.Label(w, text=seq[0],
                       font=("Segoe UI Emoji", size // 2),
                       bg="#000", fg="#fff")
        lbl.pack(expand=True)

        idx  = [0]
        # slowly drift across the screen
        dx   = [random.choice([-1,1]) * random.randint(1, 3)]
        dy   = [random.choice([-1,1]) * random.randint(1, 3)]
        pos  = [px, py]
        alive = [True]

        def _animate():
            if not alive[0]:
                return
            idx[0] = (idx[0] + 1) % len(seq)
            try:
                lbl.config(text=seq[idx[0]])
            except: pass
            w.after(110, _animate)

        def _drift():
            if not alive[0]:
                return
            pos[0] += dx[0]
            pos[1] += dy[0]
            # bounce off edges
            if pos[0] < 0 or pos[0] > SW_W - size:
                dx[0] = -dx[0]
                pos[0] = max(0, min(SW_W - size, pos[0]))
            if pos[1] < 0 or pos[1] > SW_H - size:
                dy[0] = -dy[0]
                pos[1] = max(0, min(SW_H - size, pos[1]))
            try:
                w.geometry(f"{size}x{size}+{int(pos[0])}+{int(pos[1])}")
            except: pass
            w.after(30, _drift)

        def _auto_close():
            alive[0] = False
            try:
                with emoji_gif_lock:
                    if w in emoji_gif_windows:
                        emoji_gif_windows.remove(w)
                w.destroy()
            except: pass

        with emoji_gif_lock:
            emoji_gif_windows.append(w)

        _animate()
        _drift()
        # live for 8-18 seconds then vanish
        w.after(random.randint(8000, 18000), _auto_close)

    root.after(0, _make)

# ── Random app launcher ──
APPS = [
    ("calc",          []),
    ("notepad",       []),
    ("mspaint",       []),
    ("magnify",       []),
    ("charmap",       []),
    ("mmc",           []),      # Microsoft Management Console (empty)
    ("write",         []),      # WordPad
    ("osk",           []),      # On-screen keyboard
    ("snippingtool",  []),
]

def launch_random_app():
    app, args = random.choice(APPS)
    try:
        subprocess.Popen(
            [app] + args,
            creationflags=subprocess.CREATE_NO_WINDOW,
            shell=True
        )
    except Exception:
        pass

# ── Main chaos thread ──
def chaos_loop():
    last_laugh      = time.time()
    last_annoy      = time.time()
    last_emoji      = time.time()
    last_app        = time.time()
    last_tts        = time.time()
    last_creepy_tts = time.time()

    while True:
        time.sleep(random.uniform(1.8, 4.5))

        wins = get_windows()
        if wins:
            hwnd   = random.choice(wins)
            action = random.choice(ACTIONS)
            # 35% chance to speak something creepy during a window action
            if random.random() < 0.35:
                speak(random.choice(TTS_LINES))
            try: action(hwnd)
            except: pass

        # laugh every 7-13 s
        if time.time() - last_laugh > random.uniform(7, 13):
            laugh()
            last_laugh = time.time()

        # annoy text popup every 2.5-5.5 s; 40% chance it speaks the message aloud
        if time.time() - last_annoy > random.uniform(2.5, 5.5):
            msg = random.choice(MSGS)
            do_speak = random.random() < 0.40
            show_annoy(msg, do_speak=do_speak)
            last_annoy = time.time()

        # emoji GIF window every 6-14 s
        if time.time() - last_emoji > random.uniform(6, 14):
            spawn_emoji_gif()
            last_emoji = time.time()

        # random app launch every 25-55 s
        if time.time() - last_app > random.uniform(25, 55):
            launch_random_app()
            last_app = time.time()

        # extra unprompted creepy TTS every 10-20 s
        if time.time() - last_creepy_tts > random.uniform(10, 20):
            speak(random.choice(TTS_LINES))
            last_creepy_tts = time.time()

threading.Thread(target=chaos_loop, daemon=True).start()

# ── Invisible root ──
root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)
root.mainloop()
