"""
virus_prank.py — Animated red skull, fake virus chaos, Pikachu + Freddy
jumpscares, bouncing memes, error storm, random app launcher, TTS.
Everything is closeable. Secret exit: type 4308 on keyboard.
"""
import tkinter as tk
import random, threading, time, math
import ctypes, ctypes.wintypes, subprocess, os

user32   = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
SW = user32.GetSystemMetrics(0)
SH = user32.GetSystemMetrics(1)

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

# ── TTS via PowerShell ────────────────────────────────────────────────────────
def speak(text, rate=0):
    def _do():
        safe = text.replace("'", "").replace('"', '')
        ps   = (f"Add-Type -AssemblyName System.Speech; "
                f"$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                f"$s.Rate = {rate}; $s.Speak('{safe}');")
        try:
            subprocess.Popen(["powershell", "-WindowStyle", "Hidden", "-Command", ps],
                             creationflags=subprocess.CREATE_NO_WINDOW)
        except: pass
    threading.Thread(target=_do, daemon=True).start()

# ── Sounds ────────────────────────────────────────────────────────────────────
def screech():
    def _do():
        for _ in range(45):
            kernel32.Beep(random.randint(300, 2200), 18)
        for f in [1800, 1400, 1000, 600]:
            kernel32.Beep(f, 60)
    threading.Thread(target=_do, daemon=True).start()

def laugh():
    def _do():
        for f, d in [(600,75),(0,40),(660,75),(0,40),(720,80),(0,35),(780,90),(0,30),
                     (840,95),(0,25),(900,105),(0,25),(960,115),(0,25),(1020,125),(0,50),
                     (800,40),(0,18),(840,40),(0,18),(880,40),(0,18),(920,45)]:
            if f == 0: time.sleep(d / 1000)
            else:      kernel32.Beep(f, d)
    threading.Thread(target=_do, daemon=True).start()

# ── Canvas drawing helpers ────────────────────────────────────────────────────
def draw_skull(canvas, cx, cy, r, color='#cc0000'):
    bg = color
    # Cranium
    canvas.create_oval(cx-r, cy-r*1.05, cx+r, cy+r*0.55,
                       fill=bg, outline='#ff5555', width=3)
    # Eye sockets
    er = r * 0.28
    canvas.create_oval(cx-r*0.43-er, cy-r*0.28-er, cx-r*0.43+er, cy-r*0.28+er,
                       fill='#000', outline='')
    canvas.create_oval(cx+r*0.43-er, cy-r*0.28-er, cx+r*0.43+er, cy-r*0.28+er,
                       fill='#000', outline='')
    # Red glow in eyes
    gr = er * 0.38
    canvas.create_oval(cx-r*0.43-gr, cy-r*0.28-gr, cx-r*0.43+gr, cy-r*0.28+gr,
                       fill='#ff0000', outline='')
    canvas.create_oval(cx+r*0.43-gr, cy-r*0.28-gr, cx+r*0.43+gr, cy-r*0.28+gr,
                       fill='#ff0000', outline='')
    # Nose hole
    canvas.create_polygon(cx, cy-r*0.02, cx-r*0.13, cy+r*0.22, cx+r*0.13, cy+r*0.22,
                          fill='#000', outline='')
    # Jaw
    jt = cy + r * 0.24
    jh = r * 0.38
    canvas.create_rectangle(cx-r*0.68, jt, cx+r*0.68, jt+jh,
                            fill=bg, outline='#ff5555', width=2)
    # Teeth (4)
    tw = r * 0.19
    for i in range(4):
        tx = cx - r*0.60 + i * (tw * 1.18)
        canvas.create_rectangle(tx+2, jt+5, tx+tw-2, jt+jh-5,
                                fill='white', outline='#999', width=1)
    # Skull crack
    pts = [cx+r*0.08, cy-r*0.88, cx+r*0.26, cy-r*0.48,
           cx+r*0.10, cy-r*0.18, cx+r*0.30, cy+r*0.12]
    canvas.create_line(*pts, fill='#ff9999', width=2, smooth=True)

def draw_pikachu(canvas, cx, cy, r):
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r,
                       fill='#FFD700', outline='#cc9900', width=4)
    # Left ear (triangle)
    canvas.create_polygon(cx-r*0.65, cy-r*0.8, cx-r*0.4, cy-r*1.45, cx-r*0.05, cy-r*0.82,
                          fill='#FFD700', outline='#cc9900', width=3)
    canvas.create_polygon(cx-r*0.50, cy-r*1.02, cx-r*0.4, cy-r*1.45, cx-r*0.13, cy-r*1.0,
                          fill='#111', outline='')
    # Right ear (triangle)
    canvas.create_polygon(cx+r*0.05, cy-r*0.82, cx+r*0.4, cy-r*1.45, cx+r*0.65, cy-r*0.8,
                          fill='#FFD700', outline='#cc9900', width=3)
    canvas.create_polygon(cx+r*0.13, cy-r*1.0, cx+r*0.4, cy-r*1.45, cx+r*0.50, cy-r*1.02,
                          fill='#111', outline='')
    # Eyes (wide, surprised)
    er = r * 0.18
    canvas.create_oval(cx-r*0.38-er, cy-r*0.22-er, cx-r*0.38+er, cy-r*0.22+er, fill='#111', outline='')
    canvas.create_oval(cx+r*0.38-er, cy-r*0.22-er, cx+r*0.38+er, cy-r*0.22+er, fill='#111', outline='')
    sr = er * 0.38
    canvas.create_oval(cx-r*0.43-sr, cy-r*0.27-sr, cx-r*0.43+sr, cy-r*0.27+sr, fill='white', outline='')
    canvas.create_oval(cx+r*0.33-sr, cy-r*0.27-sr, cx+r*0.33+sr, cy-r*0.27+sr, fill='white', outline='')
    # Cheeks
    cr2 = r * 0.20
    canvas.create_oval(cx-r*0.72-cr2, cy-cr2, cx-r*0.72+cr2, cy+cr2, fill='#ff4444', outline='')
    canvas.create_oval(cx+r*0.72-cr2, cy-cr2, cx+r*0.72+cr2, cy+cr2, fill='#ff4444', outline='')
    # Mouth O (surprised)
    mr = r * 0.23
    canvas.create_oval(cx-mr, cy+r*0.18-mr, cx+mr, cy+r*0.18+mr, fill='#111', outline='#333', width=2)
    # "OH!" text
    canvas.create_text(cx, cy+r*0.18, text='O', font=('Arial', int(r*0.3), 'bold'), fill='#fff')

def draw_freddy(canvas, cx, cy, r):
    # Face
    canvas.create_oval(cx-r, cy-r*1.05, cx+r, cy+r,
                       fill='#150600', outline='#3d1500', width=5)
    # Ears
    er2 = r * 0.28
    canvas.create_oval(cx-r-er2*0.5, cy-r*0.35-er2, cx-r+er2*0.5, cy-r*0.35+er2,
                       fill='#220a00', outline='#3d1500', width=3)
    canvas.create_oval(cx+r-er2*0.5, cy-r*0.35-er2, cx+r+er2*0.5, cy-r*0.35+er2,
                       fill='#220a00', outline='#3d1500', width=3)
    # Eyes (golden)
    eye_r = r * 0.23
    canvas.create_oval(cx-r*0.42-eye_r, cy-r*0.25-eye_r, cx-r*0.42+eye_r, cy-r*0.25+eye_r,
                       fill='#ffc300', outline='#ff8800', width=3)
    canvas.create_oval(cx+r*0.42-eye_r, cy-r*0.25-eye_r, cx+r*0.42+eye_r, cy-r*0.25+eye_r,
                       fill='#ffc300', outline='#ff8800', width=3)
    pr = eye_r * 0.45
    canvas.create_oval(cx-r*0.42-pr, cy-r*0.25-pr, cx-r*0.42+pr, cy-r*0.25+pr, fill='#000', outline='')
    canvas.create_oval(cx+r*0.42-pr, cy-r*0.25-pr, cx+r*0.42+pr, cy-r*0.25+pr, fill='#000', outline='')
    # Hat
    canvas.create_rectangle(cx-r*0.75, cy-r*0.98, cx+r*0.75, cy-r*0.82, fill='#0a0300', outline='#3d1500', width=3)
    canvas.create_rectangle(cx-r*0.52, cy-r*1.45, cx+r*0.52, cy-r*0.9,  fill='#0a0300', outline='#3d1500', width=3)
    # Mouth grin
    canvas.create_arc(cx-r*0.62, cy+r*0.05, cx+r*0.62, cy+r*0.78,
                      start=205, extent=130, style='chord',
                      fill='#0a0300', outline='#3d1500', width=3)
    # Teeth (5)
    tw = r * 0.14; ts = cx - r*0.45
    for i in range(5):
        tx = ts + i*(tw + r*0.05)
        canvas.create_rectangle(tx, cy+r*0.32, tx+tw, cy+r*0.60, fill='white', outline='#aaa', width=1)
    # Freckles
    fkr = r * 0.05
    for fx, fy in [(-0.35,0.54),(-0.18,0.60),(0.0,0.62),(0.35,0.54),(0.18,0.60)]:
        canvas.create_oval(cx+fx*r-fkr, cy+fy*r-fkr, cx+fx*r+fkr, cy+fy*r+fkr,
                           fill='#2d1000', outline='')

# ── Jumpscare state ───────────────────────────────────────────────────────────
pika_done   = [False]
freddy_done = [False]

def show_pikachu_scare():
    if pika_done[0]: return
    pika_done[0] = True
    def _make():
        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        w.geometry(f"{SW}x{SH}+0+0")
        w.configure(bg='#FFD700')
        c = tk.Canvas(w, width=SW, height=SH, bg='#FFD700', highlightthickness=0)
        c.pack()
        r = min(SW, SH) * 0.30
        draw_pikachu(c, SW//2, SH//2 - 40, r)
        c.create_text(SW//2, SH//2 + r + 55,
                      text="OH MY GOD IT'S PIKACHU!!",
                      font=("Impact", max(36, SW//25), "bold"), fill='#cc0000',
                      anchor='center')
        c.create_text(SW//2, SH//2 + r + 110,
                      text="( click anywhere to continue )",
                      font=("Arial", 18), fill='#775500', anchor='center')
        speak("Oh my god, its Pikachu!", rate=8)
        w.bind("<Button-1>", lambda e: w.destroy())
        w.after(5000, w.destroy)
    root.after(0, _make)

def show_freddy_scare(on_done=None):
    if freddy_done[0]: return
    freddy_done[0] = True
    def _make():
        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        w.geometry(f"{SW}x{SH}+0+0")
        w.configure(bg='#000')
        c = tk.Canvas(w, width=SW, height=SH, bg='#000', highlightthickness=0)
        c.pack()
        r = min(SW, SH) * 0.34
        draw_freddy(c, SW//2, SH//2 - 30, r)
        screech()
        pulse = [0]
        def _pulse():
            pulse[0] += 1
            col = '#ff2200' if pulse[0] % 2 == 0 else '#000'
            c.configure(bg=col)
            if pulse[0] < 10:
                w.after(110, _pulse)
            else:
                c.configure(bg='#000')
        w.after(80, _pulse)
        def _done():
            w.destroy()
            if on_done: root.after(300, on_done)
        w.after(3500, _done)
    root.after(0, _make)

def show_got_you():
    def _make():
        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        w.geometry(f"{SW}x{SH}+0+0")
        w.configure(bg='#009900')
        frame = tk.Frame(w, bg='#009900')
        frame.place(relx=0.5, rely=0.5, anchor='center')
        tk.Label(frame, text="I GOT YOU!! 😂😂😂",
                 font=("Impact", max(50, SW//18), "bold"),
                 fg='white', bg='#009900').pack()
        tk.Label(frame, text="it was all a prank lmao",
                 font=("Arial", 26), fg='#ccffcc', bg='#009900').pack(pady=10)
        tk.Button(frame, text="ok fine 😭  (close)", command=w.destroy,
                  font=("Arial", 18), bg='#006600', fg='white',
                  relief='flat', padx=24, pady=10).pack(pady=30)
        speak("I got you! It was all a prank! Hahahaha!")
        laugh()
    root.after(0, _make)

# ── Bouncing meme windows ─────────────────────────────────────────────────────
MEMES = [
    "YIKES","L + RATIO","GET REKT","SKILL ISSUE","COPE HARDER",
    "NO CAP FR FR","BRUH MOMENT","IT'S JOEVER","CAUGHT IN 4K",
    "W RIZZ","SUSSY BAKA","BASED","TOUCH GRASS","GG EZ",
    "YOU JUST LOST","BRO IS COOKED","NOT REAL","THE GOAT",
    "SHEESH","LOWKEY COOKED","FR THO","NGL THOUGH",
    "ABSOLUTE W","RENT FREE","MAIN CHARACTER","DOWN BAD",
    "UNDERSTOOD THE ASSIGNMENT","NO SHOT","UNIRONICALLY","SLAY",
    "BRO REALLY DID THAT","CERTIFIED HOOD CLASSIC","RATIO + L + COPE",
]
chaos_running = [False]

class BouncingWindow:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        w = random.randint(105, 210)
        h = random.randint(48, 80)
        self.x = random.uniform(0, SW - w)
        self.y = random.uniform(0, SH - h)
        self.dx = random.uniform(-15, 15)
        self.dy = random.uniform(-13, 13)
        if abs(self.dx) < 4: self.dx = 4 * (1 if self.dx >= 0 else -1)
        if abs(self.dy) < 4: self.dy = 4 * (1 if self.dy >= 0 else -1)
        self.w = w; self.h = h
        colors = ["#ff0000","#ff6600","#ffcc00","#00cc00","#0099ff","#cc00ff","#ff0099","#ffffff"]
        bg = random.choice(colors)
        fg = "#000000" if bg in ["#ffcc00","#ffffff","#00cc00"] else "#ffffff"
        self.win.configure(bg=bg)
        self.win.geometry(f"{w}x{h}+{int(self.x)}+{int(self.y)}")
        tk.Label(self.win, text=random.choice(MEMES),
                 font=("Impact", random.randint(12, 19), "bold"),
                 bg=bg, fg=fg, wraplength=w-8).pack(expand=True)
        self.move()

    def move(self):
        if not chaos_running[0]:
            try: self.win.destroy()
            except: pass
            return
        self.x += self.dx; self.y += self.dy
        if self.x <= 0 or self.x + self.w >= SW: self.dx *= -1; self.x = max(0, min(SW-self.w, self.x))
        if self.y <= 0 or self.y + self.h >= SH: self.dy *= -1; self.y = max(0, min(SH-self.h, self.y))
        try:
            self.win.geometry(f"{self.w}x{self.h}+{int(self.x)}+{int(self.y)}")
            self.win.after(16, self.move)
        except: pass

# ── Error popups ──────────────────────────────────────────────────────────────
ERRORS = [
    ("Windows Security",   "Threat found: Trojan:Win32/Wacatac.H!ml\nSeverity: SEVERE  |  Status: Active\nRegistry changes detected."),
    ("Disk Failure",       "SMART Failure on Disk 0: WDC WD10EZEX\nFailure imminent. Error: 0x800701E3"),
    ("System Critical",    "Stop: 0x0000007E  SYSTEM_THREAD_EXCEPTION\nntoskrnl.exe failed. Dump written."),
    ("Memory Error",       "Memory corruption at 0xFFFFFA8003B2C000\nContact hardware manufacturer."),
    ("Windows Defender",   "Ransom:Win32/Petya.A active on your system.\nFile: C:\\Windows\\System32\\lsass.exe"),
    ("Drive Error",        "Disk read error: \\Windows\\system32\\winload.exe\nStatus: 0xc000000e — File corrupt."),
    ("Network Alert",      "Unauthorized access from 185.220.101.47\nFirewall violation: svchost.exe PID 4812"),
    ("Boot Critical",      "File: \\Windows\\system32\\drivers\\ntfs.sys\nStatus: 0xc000014c — Unrecoverable"),
    ("GPU Error",          "DXGI_ERROR_DEVICE_HUNG — Display driver crashed.\nRecovery attempt failed."),
    ("CPU Temp",           "WARNING: Core temp 98°C — throttling active.\nThermal protection engaged."),
    ("Registry Corrupt",   "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\nCritical key missing. System unstable."),
    ("Firewall Breach",    f"Inbound on port 445 — SMB exploit detected.\nSource: 192.168.1.{random.randint(100,254)}"),
    ("Password Exposure",  "Saved credentials detected in memory.\nChrome: 24 passwords at risk."),
]

def spawn_error():
    if not chaos_running[0]: return
    title, msg = random.choice(ERRORS)
    win = tk.Toplevel()
    win.title(title)
    win.attributes("-topmost", True)
    win.resizable(False, False)
    win.configure(bg="#151515")
    win.geometry(f"410x185+{random.randint(0,max(0,SW-410))}+{random.randint(0,max(0,SH-185))}")
    tk.Label(win, text="⛔  " + title, font=("Segoe UI", 10, "bold"),
             bg="#151515", fg="#ff4444").pack(anchor="w", padx=10, pady=6)
    tk.Frame(win, height=1, bg="#444").pack(fill="x")
    tk.Label(win, text=msg, font=("Consolas", 8), bg="#151515", fg="#ffaaaa",
             justify="left", wraplength=390).pack(padx=10, pady=6)
    def close_more():
        win.destroy()
        if chaos_running[0]:
            for _ in range(random.randint(3, 5)):
                root.after(random.randint(50, 220), spawn_error)
    win.protocol("WM_DELETE_WINDOW", close_more)
    tk.Button(win, text="OK", command=close_more,
              bg="#333", fg="white", font=("Segoe UI", 9), relief="flat").pack(pady=4)

# ── Random app launcher ───────────────────────────────────────────────────────
APPS = ["calc", "notepad", "mspaint", "magnify", "charmap", "write", "osk", "snippingtool"]

def launch_apps():
    def _run():
        while chaos_running[0]:
            time.sleep(random.uniform(8, 22))
            if chaos_running[0]:
                try:
                    subprocess.Popen(random.choice(APPS), shell=True,
                                     creationflags=subprocess.CREATE_NO_WINDOW)
                except: pass
    threading.Thread(target=_run, daemon=True).start()

# ── TTS chaos lines ───────────────────────────────────────────────────────────
TTS_LINES = [
    "Your files are being deleted.",
    "I found your passwords.",
    "Uploading your data now.",
    "You cannot stop me.",
    "Error. Just kidding.",
    "Your computer belongs to me.",
    "Mwahahahahaha.",
    "Have a nice day.",
    "I see everything.",
]

# ── Main chaos sequence ───────────────────────────────────────────────────────
def start_chaos():
    chaos_running[0] = True

    def _run():
        # Initial flood of bouncing windows
        for _ in range(28):
            root.after(random.randint(0, 2500), BouncingWindow)

        def _keep_bouncing():
            while chaos_running[0]:
                time.sleep(0.45)
                root.after(0, BouncingWindow)
        threading.Thread(target=_keep_bouncing, daemon=True).start()

        def _keep_errors():
            while chaos_running[0]:
                time.sleep(0.14)
                root.after(0, spawn_error)
        threading.Thread(target=_keep_errors, daemon=True).start()

        launch_apps()

        def _tts_loop():
            while chaos_running[0]:
                time.sleep(random.uniform(6, 15))
                if chaos_running[0]: speak(random.choice(TTS_LINES))
        threading.Thread(target=_tts_loop, daemon=True).start()

        # Pikachu at 25–55 s
        pika_delay = random.randint(25000, 55000)
        root.after(pika_delay, show_pikachu_scare)

        # Freddy 18–28 s after Pikachu → then "I GOT YOU"
        freddy_delay = pika_delay + random.randint(18000, 28000)
        root.after(freddy_delay, lambda: show_freddy_scare(on_done=show_got_you))

    threading.Thread(target=_run, daemon=True).start()

# ── Main virus alert window with animated skull ───────────────────────────────
def show_virus_alert():
    alert = tk.Toplevel()
    alert.title("Windows Security — Critical Alert")
    alert.attributes("-topmost", True)
    alert.resizable(False, False)
    alert.configure(bg="#0d0000")
    alert.geometry(f"540x520+{SW//2-270}+{SH//2-260}")

    # ── Red header bar
    hdr = tk.Frame(alert, bg="#880000", height=50)
    hdr.pack(fill="x"); hdr.pack_propagate(False)
    tk.Label(hdr, text="  ☠  CRITICAL VIRUS DETECTED  ☠",
             font=("Segoe UI", 13, "bold"), bg="#880000", fg="#ffcccc").pack(side="left", pady=10)

    # ── Animated skull canvas
    skull_c = tk.Canvas(alert, width=540, height=190, bg="#0d0000", highlightthickness=0)
    skull_c.pack()

    skull_state = [0]
    skull_colors = ['#cc0000', '#aa0000', '#dd0000', '#bb0000', '#ff0000', '#aa0000']
    def _pulse_skull():
        skull_state[0] = (skull_state[0] + 1) % len(skull_colors)
        skull_c.delete("all")
        col = skull_colors[skull_state[0]]
        # Glow ring
        glow = skull_state[0] * 4
        skull_c.create_oval(270-105-glow, 95-105-glow, 270+105+glow, 95+105+glow,
                            fill='', outline=col, width=2)
        draw_skull(skull_c, 270, 95, 82, col)
        try: skull_c.after(500, _pulse_skull)
        except: pass
    _pulse_skull()

    # ── Info panel
    inf = tk.Frame(alert, bg="#0d0000")
    inf.pack(fill="x", padx=18)
    tk.Label(inf, text="THREAT:  Trojan:Win32/Wacatac.H!ml  +  Ransom:Win32/Petya.A",
             font=("Consolas", 9, "bold"), bg="#0d0000", fg="#ff4444").pack(anchor="w")
    details = ("Severity:     ████████████ CRITICAL\n"
               "Status:       ACTIVE — Spreading to network shares\n"
               "Files:        3,247 infected  |  891 encrypted\n"
               "Registry:     14 keys modified\n"
               "Passwords:    Scanning Chrome / Edge...\n"
               "Network:      Exfiltration in progress (port 443)")
    tk.Label(inf, text=details, font=("Consolas", 9), bg="#0d0000", fg="#ff8888",
             justify="left").pack(anchor="w", pady=4)

    # ── Fake scan progress bar
    pf = tk.Frame(alert, bg="#0d0000")
    pf.pack(fill="x", padx=18, pady=4)
    tk.Label(pf, text="SCANNING DRIVES:", font=("Consolas", 9),
             bg="#0d0000", fg="#ff5555").pack(anchor="w")
    prog_c = tk.Canvas(pf, width=504, height=20, bg="#1a0000",
                       highlightthickness=1, highlightbackground="#550000")
    prog_c.pack()
    prog = [0]
    def _prog():
        prog[0] = min(100, prog[0] + random.randint(1, 5))
        prog_c.delete("all")
        w_fill = int(504 * prog[0] / 100)
        col2 = '#ff2200' if prog[0] > 85 else '#cc0000'
        prog_c.create_rectangle(0, 0, w_fill, 20, fill=col2, outline="")
        prog_c.create_text(252, 10,
                           text=f"{prog[0]}%  —  C:\\Users\\AppData... infected",
                           fill="white", font=("Consolas", 8))
        if prog[0] < 100:
            prog_c.after(70, _prog)
        else:
            prog_c.create_rectangle(0, 0, 504, 20, fill="#ff0000", outline="")
            prog_c.create_text(252, 10, text="SCAN COMPLETE — 3,247 THREATS FOUND",
                               fill="white", font=("Consolas", 8, "bold"))
    prog_c.after(200, _prog)

    tk.Frame(alert, height=1, bg="#440000").pack(fill="x", pady=6)

    # ── Action button
    bf = tk.Frame(alert, bg="#0d0000")
    bf.pack(pady=6)
    def _go():
        alert.destroy()
        speak("Critical virus detected. Your computer is compromised. All files at risk.")
        start_chaos()
    tk.Button(bf, text="⚠   FIX NOW — REMOVE ALL THREATS",
              command=_go, bg="#cc0000", fg="white",
              font=("Segoe UI", 13, "bold"), relief="flat",
              padx=22, pady=11, cursor="hand2").pack()

    tk.Label(alert, text="Windows Security  |  Protected by Microsoft Defender Antivirus v4.18",
             font=("Segoe UI", 7), bg="#0d0000", fg="#3a0000").pack(pady=(4, 6))

# ── Entry point ───────────────────────────────────────────────────────────────
root = tk.Tk()
root.withdraw()
root.after(400, show_virus_alert)
root.mainloop()
