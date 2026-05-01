"""
window_chaos.py — grabs every open window and goes absolutely insane with it.
Shakes, shrinks, teleports, spins, swaps, cascades, mega-shakes, and more.
Opens random apps, Explorer locations, Task Manager, funny Notepad files.
Animated emoji bounce windows. Creepy TTS. Zero beep sounds.
Secret exit: type 4308 anywhere on keyboard.
"""
import ctypes, ctypes.wintypes, random, time, threading
import tkinter as tk, os, subprocess, math, tempfile

user32   = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
SW_W     = user32.GetSystemMetrics(0)
SW_H     = user32.GetSystemMetrics(1)

# ── Global keyboard hook — secret exit 4308 ──────────────────────────────────
class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [('vkCode', ctypes.c_uint32), ('scanCode', ctypes.c_uint32),
                ('flags',  ctypes.c_uint32), ('time',     ctypes.c_uint32),
                ('dwExtraInfo', ctypes.POINTER(ctypes.c_ulong))]
HOOKPROC  = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                ctypes.POINTER(KBDLLHOOKSTRUCT))
_sec_buf  = []
def _kb(nCode, wParam, lParam):
    if nCode >= 0 and wParam == 0x0100:
        vk = lParam.contents.vkCode
        if 0x30 <= vk <= 0x39:
            _sec_buf.append(chr(vk))
            if len(_sec_buf) > 4: _sec_buf.pop(0)
            if ''.join(_sec_buf) == '4308': os._exit(0)
    return user32.CallNextHookEx(None, nCode, wParam, lParam)
_kbproc = HOOKPROC(_kb)
def _hook_thread():
    user32.SetWindowsHookExW(13, _kbproc, None, 0)
    msg = ctypes.wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageW(ctypes.byref(msg))
threading.Thread(target=_hook_thread, daemon=True).start()

# ── TTS ───────────────────────────────────────────────────────────────────────
def speak(text, rate=-1):
    def _do():
        safe = text.replace("'","").replace('"','')
        ps   = (f"Add-Type -AssemblyName System.Speech; "
                f"$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                f"$s.Rate = {rate}; $s.Speak('{safe}');")
        try:
            subprocess.Popen(["powershell", "-WindowStyle", "Hidden", "-Command", ps],
                             creationflags=subprocess.CREATE_NO_WINDOW)
        except: pass
    threading.Thread(target=_do, daemon=True).start()

# ── Window enumeration ────────────────────────────────────────────────────────
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool,
                                  ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
SKIP = ['program manager','task switching','windows input','microsoft text input',
        'default ime','msctfime ui','window message pump','task manager',
        'computur','python','shell_traywnd','button']

def get_windows():
    wins = []
    def _cb(hwnd, _):
        if not user32.IsWindowVisible(hwnd): return True
        n = user32.GetWindowTextLengthW(hwnd)
        if n == 0: return True
        buf = ctypes.create_unicode_buffer(n+1)
        user32.GetWindowTextW(hwnd, buf, n+1)
        title = buf.value.lower()
        if any(s in title for s in SKIP): return True
        r = ctypes.wintypes.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(r))
        if (r.right-r.left) > 120 and (r.bottom-r.top) > 80:
            wins.append(hwnd)
        return True
    user32.EnumWindows(WNDENUMPROC(_cb), 0)
    return wins

def get_rect(hwnd):
    r = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(r))
    return r.left, r.top, r.right-r.left, r.bottom-r.top

# ── Window actions ────────────────────────────────────────────────────────────
def shake(hwnd):
    ox, oy, w, h = get_rect(hwnd)
    for _ in range(18):
        user32.MoveWindow(hwnd, ox+random.randint(-40,40), oy+random.randint(-30,30), w, h, True)
        time.sleep(0.030)
    user32.MoveWindow(hwnd, ox, oy, w, h, True)

def mega_shake(hwnd):
    """Extra violent shake."""
    ox, oy, w, h = get_rect(hwnd)
    for _ in range(30):
        user32.MoveWindow(hwnd, ox+random.randint(-80,80), oy+random.randint(-60,60), w, h, True)
        time.sleep(0.022)
    user32.MoveWindow(hwnd, ox, oy, w, h, True)

def shrink(hwnd):
    ox, oy, w, h = get_rect(hwnd)
    user32.MoveWindow(hwnd, ox+w//2, oy+h//2, random.randint(140,260), random.randint(90,180), True)
    time.sleep(random.uniform(1.8, 3.0))
    user32.MoveWindow(hwnd, ox, oy, w, h, True)

def shrink_to_nothing(hwnd):
    """Rapidly shrink almost to zero, then snap back."""
    ox, oy, w, h = get_rect(hwnd)
    for s in [0.75, 0.50, 0.30, 0.15, 0.07]:
        nw, nh = max(40, int(w*s)), max(30, int(h*s))
        user32.MoveWindow(hwnd, ox+int(w*(1-s)/2), oy+int(h*(1-s)/2), nw, nh, True)
        time.sleep(0.065)
    time.sleep(0.4)
    user32.MoveWindow(hwnd, ox, oy, w, h, True)

def teleport(hwnd):
    _, _, w, h = get_rect(hwnd)
    nx = random.randint(0, max(0, SW_W-w))
    ny = random.randint(30, max(30, SW_H-h))
    user32.MoveWindow(hwnd, nx, ny, w, h, True)

def rapid_teleport(hwnd):
    """Teleport 5 times in quick succession."""
    for _ in range(5):
        teleport(hwnd)
        time.sleep(0.18)

def minimize_pop(hwnd):
    user32.ShowWindow(hwnd, 6)
    time.sleep(random.uniform(0.5, 1.2))
    user32.ShowWindow(hwnd, 9)

def resize_huge(hwnd):
    ox, oy, w, h = get_rect(hwnd)
    user32.MoveWindow(hwnd, 0, 30, SW_W, SW_H-30, True)
    time.sleep(1.2)
    user32.MoveWindow(hwnd, ox, oy, w, h, True)

def spin_fake(hwnd):
    ox, oy, w, h = get_rect(hwnd)
    cx = ox + w//2; cy = oy + h//2
    for i in range(24):
        a = (i/24)*2*math.pi
        nx = int(cx + math.cos(a)*150) - w//2
        ny = int(cy + math.sin(a)*100) - h//2
        user32.MoveWindow(hwnd, nx, ny, w, h, True)
        time.sleep(0.038)
    user32.MoveWindow(hwnd, ox, oy, w, h, True)

def cascade_all():
    """Cascade all windows diagonally across screen."""
    wins = get_windows()
    for i, hwnd in enumerate(wins[:10]):
        try:
            _, _, w, h = get_rect(hwnd)
            user32.MoveWindow(hwnd, 28*i, 28*i+30, w, h, True)
        except: pass

def swap_two(hwnd1, hwnd2):
    """Swap positions of two windows."""
    x1,y1,w1,h1 = get_rect(hwnd1)
    x2,y2,w2,h2 = get_rect(hwnd2)
    user32.MoveWindow(hwnd1, x2, y2, w1, h1, True)
    user32.MoveWindow(hwnd2, x1, y1, w2, h2, True)

def all_minimize_restore():
    """Minimize everything then restore it."""
    wins = get_windows()
    for hwnd in wins:
        try: user32.ShowWindow(hwnd, 6)
        except: pass
    time.sleep(1.8)
    for hwnd in wins:
        try: user32.ShowWindow(hwnd, 9)
        except: pass

def accordion(hwnd):
    """Rapidly resize width back and forth."""
    ox, oy, w, h = get_rect(hwnd)
    for _ in range(8):
        user32.MoveWindow(hwnd, ox, oy, random.randint(w//3, w*2), h, True)
        time.sleep(0.09)
    user32.MoveWindow(hwnd, ox, oy, w, h, True)

SINGLE_ACTIONS = [shake, mega_shake, shrink, shrink_to_nothing,
                  teleport, rapid_teleport, minimize_pop,
                  resize_huge, spin_fake, accordion,
                  shake, shake, mega_shake, teleport, teleport]

# ── Open varied targets ───────────────────────────────────────────────────────
NOTEPAD_MSGS = [
    "Hello. I am inside your computer.",
    "I see you reading this. Please stop. I need privacy.",
    "YOUR COMPUTER IS FINE. THIS IS FINE. EVERYTHING IS FINE.",
    "I moved all your files. They are safe. Probably.",
    "You have 0 unread messages. Wait, no. You have infinite.",
    "This is not a virus. This is a love letter. From your PC.",
    "IMPORTANT NOTICE: Your chair is possessed. Stand up slowly.",
    "Have you tried turning it off and on again? Don't.",
    "Your task manager cannot save you now.",
    "I have been living here since 2019. You never noticed.",
]

def open_funny_notepad():
    try:
        tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
        tmp.write(random.choice(NOTEPAD_MSGS))
        tmp.close()
        subprocess.Popen(["notepad", tmp.name], creationflags=subprocess.CREATE_NO_WINDOW)
    except: pass

OPEN_TARGETS = [
    lambda: subprocess.Popen("calc",          shell=True, creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen("notepad",       shell=True, creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen("mspaint",       shell=True, creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen("magnify",       shell=True, creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen("osk",           shell=True, creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen("write",         shell=True, creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen("snippingtool",  shell=True, creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen("charmap",       shell=True, creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen("taskmgr",       shell=True, creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen(["explorer", "shell:Desktop"],      creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen(["explorer", "shell:Downloads"],    creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen(["explorer", "shell:Documents"],    creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen(["explorer", "C:\\"],               creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen(["explorer", "shell:RecycleBinFolder"], creationflags=subprocess.CREATE_NO_WINDOW),
    open_funny_notepad,
    open_funny_notepad,  # twice as likely — it's the funniest
]

# ── Annoy popup messages ──────────────────────────────────────────────────────
MSGS = [
    "YOUR WINDOWS ARE MINE NOW",
    "WINDOW.EXE HAS STOPPED WORKING... OR HAS IT?",
    "I LIVE HERE. FOREVER.",
    "YOUR COMPUTER CALLED. IT WANTS A DIVORCE.",
    "ERROR 404: YOUR SANITY NOT FOUND",
    "HAVE YOU TRIED TURNING IT OFF? DON'T.",
    "THIS IS FINE 🔥",
    "NEW NOTIFICATION: YOUR PC HAS GONE ROGUE",
    "TASK MANAGER CANNOT SAVE YOU",
    "WINDOWS UPDATE: CHAOS INSTALLED SUCCESSFULLY",
    "SYS32 HAS LEFT THE BUILDING",
    "NICE DESKTOP YOU HAD THERE",
    "I MOVED YOUR WINDOW. AGAIN.",
    "CTRL+Z DOES NOTHING HERE",
    "YOUR TASKBAR FILED A COMPLAINT",
    "CHAOS LEVEL: MAXIMUM",
    "I AM THE WINDOW NOW",
    "THE DESKTOP BELONGS TO ME",
    "CLICK ANYWHERE TO MAKE IT WORSE",
    "YOUR CURSOR CALLED IN SICK",
    "I FOUND YOUR SEARCH HISTORY 👀",
    "WINDOW GO BRRR",
    "BEEP BOOP. CHAOS MODE.",
    "YOUR FILES ARE... SOMEWHERE",
    "RESISTANCE IS FUTILE",
    "SCREEN? MORE LIKE MY SCREEN.",
    "NOT A VIRUS. DEFINITELY NOT.",
    "HAVE A GREAT DAY :) ",
]

annoy_lock    = threading.Lock()
annoy_windows = []

def show_annoy(msg):
    def _make():
        with annoy_lock:
            if len(annoy_windows) > 9:
                try: annoy_windows.pop(0).destroy()
                except: pass
        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        w.configure(bg="#111")
        px = random.randint(10, max(11, SW_W-370))
        py = random.randint(10, max(11, SW_H-90))
        w.geometry(f"+{px}+{py}")
        c = random.choice(["#ff2222","#ff9900","#ffff00","#00ff88","#ff00ff","#00cfff","#fff"])
        tk.Label(w, text=msg, font=("Arial Black", random.randint(14,26),"bold"),
                 fg=c, bg="#111", padx=14, pady=8).pack()
        with annoy_lock: annoy_windows.append(w)
        w.after(random.randint(1600,2800), lambda: _kill(w))
    def _kill(w):
        try:
            with annoy_lock:
                if w in annoy_windows: annoy_windows.remove(w)
            w.destroy()
        except: pass
    root.after(0, _make)

# ── Emoji "GIF" bounce windows ────────────────────────────────────────────────
EMOJI_SEQS = [
    ["😈","👿","💀","☠️","😈","👿"], ["💻","🔥","💥","⚡","🔥","💥"],
    ["👻","😱","🫣","😰","👻","😱"], ["🤣","😂","💀","🤣","😂","💀"],
    ["⚠️","🚨","‼️","⚠️","🚨","‼️"], ["🎃","👹","👺","🎃","👹","👺"],
    ["🤖","👾","👽","🤖","👾","👽"], ["😤","😡","🤬","😤","😡","🤬"],
    ["🌀","💫","✨","🌀","💫","✨"], ["🐍","💀","🐍","💀","☠️","🐍"],
]
gif_lock    = threading.Lock()
gif_windows = []
MAX_GIFS    = 8

def spawn_emoji_gif():
    def _make():
        with gif_lock:
            if len(gif_windows) >= MAX_GIFS:
                try: gif_windows.pop(0).destroy()
                except: pass
        seq  = random.choice(EMOJI_SEQS)
        size = random.randint(75, 130)
        px   = random.randint(10, max(11, SW_W-size-10))
        py   = random.randint(10, max(11, SW_H-size-10))
        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        w.configure(bg="#000")
        w.geometry(f"{size}x{size}+{px}+{py}")
        lbl = tk.Label(w, text=seq[0], font=("Segoe UI Emoji", size//2), bg="#000")
        lbl.pack(expand=True)
        idx = [0]; dx = [random.choice([-1,1])*random.randint(2,4)]
        dy = [random.choice([-1,1])*random.randint(2,4)]; pos = [px, py]; alive = [True]
        def _anim():
            if not alive[0]: return
            idx[0] = (idx[0]+1) % len(seq)
            try: lbl.config(text=seq[idx[0]])
            except: pass
            w.after(105, _anim)
        def _drift():
            if not alive[0]: return
            pos[0]+=dx[0]; pos[1]+=dy[0]
            if pos[0]<0 or pos[0]>SW_W-size: dx[0]*=-1; pos[0]=max(0,min(SW_W-size,pos[0]))
            if pos[1]<0 or pos[1]>SW_H-size: dy[0]*=-1; pos[1]=max(0,min(SW_H-size,pos[1]))
            try: w.geometry(f"{size}x{size}+{int(pos[0])}+{int(pos[1])}")
            except: pass
            w.after(28, _drift)
        def _die():
            alive[0]=False
            try:
                with gif_lock:
                    if w in gif_windows: gif_windows.remove(w)
                w.destroy()
            except: pass
        with gif_lock: gif_windows.append(w)
        _anim(); _drift()
        w.after(random.randint(8000,18000), _die)
    root.after(0, _make)

# ── TTS lines ────────────────────────────────────────────────────────────────
TTS_LINES = [
    "I am inside your computer.",
    "You cannot escape.",
    "Hello. I live here now.",
    "Your windows belong to me.",
    "Why are you running?",
    "I can see everything.",
    "Do not turn off your computer.",
    "Help. I am trapped inside.",
    "Mwahahahahaha.",
    "You thought you were safe.",
    "I know what you did.",
    "Nice wallpaper by the way.",
    "I see you.",
    "They are coming for you.",
    "Something is very wrong.",
]

# ── Main chaos loop ───────────────────────────────────────────────────────────
start_time      = time.time()
last_annoy      = time.time()
last_emoji      = time.time()
last_app        = time.time()
last_tts        = time.time()
last_group      = time.time()
last_cascade    = time.time()

def chaos_loop():
    global last_annoy, last_emoji, last_app, last_tts, last_group, last_cascade

    while True:
        elapsed = time.time() - start_time
        # Escalate delay: starts calmer, gets faster
        if elapsed < 30:   sleep = random.uniform(2.5, 5.0)
        elif elapsed < 90: sleep = random.uniform(1.5, 3.5)
        else:              sleep = random.uniform(0.8, 2.2)
        time.sleep(sleep)

        wins = get_windows()
        if not wins:
            continue

        # ── Single-window action
        hwnd   = random.choice(wins)
        action = random.choice(SINGLE_ACTIONS)
        try: action(hwnd)
        except: pass

        # ── Two-window swap (if enough windows)
        if elapsed > 20 and len(wins) >= 2 and random.random() < 0.25:
            h1, h2 = random.sample(wins, 2)
            try: swap_two(h1, h2)
            except: pass

        # ── All-minimize-restore every 45-80s
        if time.time() - last_group > random.uniform(45, 80):
            threading.Thread(target=all_minimize_restore, daemon=True).start()
            last_group = time.time()

        # ── Cascade every 60-120s (after 60s in)
        if elapsed > 60 and time.time() - last_cascade > random.uniform(60, 120):
            threading.Thread(target=cascade_all, daemon=True).start()
            last_cascade = time.time()

        # ── Annoy popup every 2-5s
        if time.time() - last_annoy > random.uniform(2.0, 5.0):
            show_annoy(random.choice(MSGS))
            last_annoy = time.time()

        # ── Emoji GIF every 5-12s
        if time.time() - last_emoji > random.uniform(5, 12):
            spawn_emoji_gif()
            last_emoji = time.time()

        # ── Open random target every 15-40s (escalates)
        open_interval = random.uniform(15, 40) if elapsed < 60 else random.uniform(8, 20)
        if time.time() - last_app > open_interval:
            try: random.choice(OPEN_TARGETS)()
            except: pass
            last_app = time.time()

        # ── Creepy TTS every 10-22s
        if time.time() - last_tts > random.uniform(10, 22):
            speak(random.choice(TTS_LINES))
            last_tts = time.time()

threading.Thread(target=chaos_loop, daemon=True).start()

# ── Invisible root ────────────────────────────────────────────────────────────
root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)
root.mainloop()
