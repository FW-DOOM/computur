"""
bonzi_buddy.py — Fake BonziBUDDY prank.
Purple gorilla talks, DELETE button dodges your mouse for a while,
then opens a fake file cleaner. Ends in Pikachu + Freddy jumpscares.
I GOT YOU!!   Secret exit: type 4308.
"""
import tkinter as tk
from tkinter import ttk
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
HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int,
                               ctypes.POINTER(KBDLLHOOKSTRUCT))
_sec_buf = []
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
def speak(text, rate=0):
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

# ── Sounds ────────────────────────────────────────────────────────────────────
def screech():
    def _do():
        for _ in range(45): kernel32.Beep(random.randint(300, 2200), 18)
        for f in [1800, 1400, 1000, 600]: kernel32.Beep(f, 60)
    threading.Thread(target=_do, daemon=True).start()

def laugh():
    def _do():
        for f, d in [(600,75),(0,40),(660,75),(0,40),(720,80),(0,35),(780,90),(0,30),
                     (840,95),(0,25),(900,105),(0,25),(960,115),(0,25),(1020,125),(0,50),
                     (800,40),(0,18),(840,40),(0,18),(880,40),(0,18),(920,45)]:
            if f == 0: time.sleep(d/1000)
            else:      kernel32.Beep(f, d)
    threading.Thread(target=_do, daemon=True).start()

def bonzi_boop():
    def _do():
        for f, d in [(440,60),(0,30),(550,60),(0,30),(660,90)]:
            if f == 0: time.sleep(d/1000)
            else:      kernel32.Beep(f, d)
    threading.Thread(target=_do, daemon=True).start()

# ── Canvas drawing helpers ────────────────────────────────────────────────────
def draw_pikachu(canvas, cx, cy, r):
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill='#FFD700', outline='#cc9900', width=4)
    canvas.create_polygon(cx-r*0.65, cy-r*0.8, cx-r*0.4, cy-r*1.45, cx-r*0.05, cy-r*0.82,
                          fill='#FFD700', outline='#cc9900', width=3)
    canvas.create_polygon(cx-r*0.50, cy-r*1.02, cx-r*0.4, cy-r*1.45, cx-r*0.13, cy-r*1.0,
                          fill='#111', outline='')
    canvas.create_polygon(cx+r*0.05, cy-r*0.82, cx+r*0.4, cy-r*1.45, cx+r*0.65, cy-r*0.8,
                          fill='#FFD700', outline='#cc9900', width=3)
    canvas.create_polygon(cx+r*0.13, cy-r*1.0, cx+r*0.4, cy-r*1.45, cx+r*0.50, cy-r*1.02,
                          fill='#111', outline='')
    er = r*0.18
    canvas.create_oval(cx-r*0.38-er, cy-r*0.22-er, cx-r*0.38+er, cy-r*0.22+er, fill='#111', outline='')
    canvas.create_oval(cx+r*0.38-er, cy-r*0.22-er, cx+r*0.38+er, cy-r*0.22+er, fill='#111', outline='')
    sr = er*0.38
    canvas.create_oval(cx-r*0.43-sr, cy-r*0.27-sr, cx-r*0.43+sr, cy-r*0.27+sr, fill='white', outline='')
    canvas.create_oval(cx+r*0.33-sr, cy-r*0.27-sr, cx+r*0.33+sr, cy-r*0.27+sr, fill='white', outline='')
    cr2 = r*0.20
    canvas.create_oval(cx-r*0.72-cr2, cy-cr2, cx-r*0.72+cr2, cy+cr2, fill='#ff4444', outline='')
    canvas.create_oval(cx+r*0.72-cr2, cy-cr2, cx+r*0.72+cr2, cy+cr2, fill='#ff4444', outline='')
    mr = r*0.23
    canvas.create_oval(cx-mr, cy+r*0.18-mr, cx+mr, cy+r*0.18+mr, fill='#111', outline='#333', width=2)
    canvas.create_text(cx, cy+r*0.18, text='O', font=('Arial', int(r*0.28), 'bold'), fill='#fff')

def draw_freddy(canvas, cx, cy, r):
    canvas.create_oval(cx-r, cy-r*1.05, cx+r, cy+r, fill='#150600', outline='#3d1500', width=5)
    er2 = r*0.28
    canvas.create_oval(cx-r-er2*0.5, cy-r*0.35-er2, cx-r+er2*0.5, cy-r*0.35+er2,
                       fill='#220a00', outline='#3d1500', width=3)
    canvas.create_oval(cx+r-er2*0.5, cy-r*0.35-er2, cx+r+er2*0.5, cy-r*0.35+er2,
                       fill='#220a00', outline='#3d1500', width=3)
    eye_r = r*0.23
    canvas.create_oval(cx-r*0.42-eye_r, cy-r*0.25-eye_r, cx-r*0.42+eye_r, cy-r*0.25+eye_r,
                       fill='#ffc300', outline='#ff8800', width=3)
    canvas.create_oval(cx+r*0.42-eye_r, cy-r*0.25-eye_r, cx+r*0.42+eye_r, cy-r*0.25+eye_r,
                       fill='#ffc300', outline='#ff8800', width=3)
    pr = eye_r*0.45
    canvas.create_oval(cx-r*0.42-pr, cy-r*0.25-pr, cx-r*0.42+pr, cy-r*0.25+pr, fill='#000', outline='')
    canvas.create_oval(cx+r*0.42-pr, cy-r*0.25-pr, cx+r*0.42+pr, cy-r*0.25+pr, fill='#000', outline='')
    canvas.create_rectangle(cx-r*0.75, cy-r*0.98, cx+r*0.75, cy-r*0.82, fill='#0a0300', outline='#3d1500', width=3)
    canvas.create_rectangle(cx-r*0.52, cy-r*1.45, cx+r*0.52, cy-r*0.9,  fill='#0a0300', outline='#3d1500', width=3)
    canvas.create_arc(cx-r*0.62, cy+r*0.05, cx+r*0.62, cy+r*0.78,
                      start=205, extent=130, style='chord', fill='#0a0300', outline='#3d1500', width=3)
    tw = r*0.14; ts = cx-r*0.45
    for i in range(5):
        tx = ts+i*(tw+r*0.05)
        canvas.create_rectangle(tx, cy+r*0.32, tx+tw, cy+r*0.60, fill='white', outline='#aaa', width=1)

def draw_bonzi(canvas, cx, cy):
    """Draw a purple gorilla (BonziBUDDY) on the canvas centered at (cx, cy)."""
    # === BODY ===
    canvas.create_oval(cx-70, cy-35, cx+70, cy+120, fill='#8800dd', outline='#5500aa', width=3)
    # Belly (lighter)
    canvas.create_oval(cx-44, cy-10, cx+44, cy+98, fill='#aa44ee', outline='#8800dd', width=1)

    # === LEFT ARM ===
    canvas.create_oval(cx-112, cy-18, cx-58, cy+62,  fill='#8800dd', outline='#5500aa', width=2)
    canvas.create_oval(cx-120, cy+38, cx-55, cy+88,  fill='#9933ee', outline='#5500aa', width=2)

    # === RIGHT ARM ===
    canvas.create_oval(cx+58, cy-18, cx+112, cy+62,  fill='#8800dd', outline='#5500aa', width=2)
    canvas.create_oval(cx+55, cy+38, cx+120, cy+88,  fill='#9933ee', outline='#5500aa', width=2)

    # === LEGS ===
    canvas.create_oval(cx-62, cy+82, cx-8,  cy+158, fill='#8800dd', outline='#5500aa', width=2)
    canvas.create_oval(cx+8,  cy+82, cx+62, cy+158, fill='#8800dd', outline='#5500aa', width=2)
    # Feet
    canvas.create_oval(cx-70, cy+132, cx-4,  cy+170, fill='#9933ee', outline='#5500aa', width=2)
    canvas.create_oval(cx+4,  cy+132, cx+70, cy+170, fill='#9933ee', outline='#5500aa', width=2)

    # === HEAD ===
    canvas.create_oval(cx-64, cy-188, cx+64, cy-54, fill='#8800dd', outline='#5500aa', width=3)

    # === EARS ===
    canvas.create_oval(cx-84, cy-175, cx-42, cy-122, fill='#8800dd', outline='#5500aa', width=2)
    canvas.create_oval(cx-80, cy-171, cx-46, cy-126, fill='#cc66ff', outline='')
    canvas.create_oval(cx+42, cy-175, cx+84, cy-122, fill='#8800dd', outline='#5500aa', width=2)
    canvas.create_oval(cx+46, cy-171, cx+80, cy-126, fill='#cc66ff', outline='')

    # === FACE / SNOUT ===
    canvas.create_oval(cx-40, cy-144, cx+40, cy-68, fill='#cc88ff', outline='#9944cc', width=2)

    # === EYES ===
    canvas.create_oval(cx-56, cy-173, cx-20, cy-136, fill='white', outline='#333', width=2, tags='eye_l')
    canvas.create_oval(cx-49, cy-166, cx-27, cy-143, fill='#111',   outline='',     tags='pupil_l')
    canvas.create_oval(cx-48, cy-165, cx-41, cy-158, fill='white',  outline='',     tags='shine_l')
    canvas.create_oval(cx+20, cy-173, cx+56, cy-136, fill='white',  outline='#333', width=2, tags='eye_r')
    canvas.create_oval(cx+27, cy-166, cx+49, cy-143, fill='#111',   outline='',     tags='pupil_r')
    canvas.create_oval(cx+41, cy-165, cx+48, cy-158, fill='white',  outline='',     tags='shine_r')

    # === NOSE ===
    canvas.create_oval(cx-13, cy-120, cx+13, cy-102, fill='#330055', outline='#220044')
    canvas.create_oval(cx-11, cy-117, cx-3,  cy-106, fill='#110022', outline='')
    canvas.create_oval(cx+3,  cy-117, cx+11, cy-106, fill='#110022', outline='')

    # === MOUTH / GRIN ===
    canvas.create_arc(cx-32, cy-98, cx+32, cy-64, start=205, extent=130,
                      style='chord', fill='#110022', outline='#330055', width=2)
    for i in range(3):
        tx = cx-22+i*16
        canvas.create_rectangle(tx, cy-88, tx+12, cy-70, fill='white', outline='#aaa', width=1)

    # === EYEBROWS (friendly raised) ===
    canvas.create_arc(cx-58, cy-185, cx-14, cy-150, start=20, extent=140,
                      style='arc', outline='#330055', width=3)
    canvas.create_arc(cx+14, cy-185, cx+58, cy-150, start=20, extent=140,
                      style='arc', outline='#330055', width=3)

def update_speech_bubble(canvas, text, bx=20, by=10, bw=380, bh=72):
    """Redraw the speech bubble on the canvas with new text."""
    canvas.delete('bubble')
    # Rounded rect (fake via overlapping rectangles + ovals)
    canvas.create_rectangle(bx+12, by, bx+bw-12, by+bh,    fill='white', outline='#9944cc', width=3, tags='bubble')
    canvas.create_rectangle(bx, by+12, bx+bw, by+bh-12,    fill='white', outline='',        tags='bubble')
    canvas.create_oval(bx, by, bx+24, by+24,                fill='white', outline='#9944cc', width=3, tags='bubble')
    canvas.create_oval(bx+bw-24, by, bx+bw, by+24,          fill='white', outline='#9944cc', width=3, tags='bubble')
    canvas.create_oval(bx, by+bh-24, bx+24, by+bh,          fill='white', outline='#9944cc', width=3, tags='bubble')
    canvas.create_oval(bx+bw-24, by+bh-24, bx+bw, by+bh,    fill='white', outline='#9944cc', width=3, tags='bubble')
    # Pointer triangle (points down toward Bonzi head)
    mid = bx + bw//2
    canvas.create_polygon(mid-14, by+bh, mid+14, by+bh, mid, by+bh+22,
                          fill='white', outline='#9944cc', width=3, tags='bubble')
    canvas.create_polygon(mid-11, by+bh+1, mid+11, by+bh+1, mid, by+bh+20,
                          fill='white', outline='', tags='bubble')
    # Text
    canvas.create_text(bx+bw//2, by+bh//2, text=text,
                       font=('Segoe UI', 11), fill='#220033',
                       width=bw-28, anchor='center', tags='bubble')

# ── Jumpscares ────────────────────────────────────────────────────────────────
def show_pikachu_scare(on_done=None):
    def _make():
        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        w.geometry(f"{SW}x{SH}+0+0")
        w.configure(bg='#FFD700')
        c = tk.Canvas(w, width=SW, height=SH, bg='#FFD700', highlightthickness=0)
        c.pack()
        r = min(SW, SH) * 0.30
        draw_pikachu(c, SW//2, SH//2-40, r)
        c.create_text(SW//2, SH//2+r+50, text="OH MY GOD IT'S PIKACHU!!",
                      font=("Impact", max(36, SW//24), "bold"), fill='#cc0000', anchor='center')
        c.create_text(SW//2, SH//2+r+105, text="( click to continue )",
                      font=("Arial", 18), fill='#775500', anchor='center')
        speak("Oh my god, its Pikachu!", rate=8)
        def _next():
            w.destroy()
            if on_done: root.after(300, on_done)
        w.bind("<Button-1>", lambda e: _next())
        w.after(5000, _next)
    root.after(0, _make)

def show_freddy_scare(on_done=None):
    def _make():
        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        w.geometry(f"{SW}x{SH}+0+0")
        w.configure(bg='#000')
        c = tk.Canvas(w, width=SW, height=SH, bg='#000', highlightthickness=0)
        c.pack()
        r = min(SW, SH) * 0.34
        draw_freddy(c, SW//2, SH//2-30, r)
        screech()
        pulse = [0]
        def _pulse():
            pulse[0] += 1
            c.configure(bg='#ff2200' if pulse[0]%2==0 else '#000')
            if pulse[0] < 10: w.after(110, _pulse)
            else: c.configure(bg='#000')
        w.after(80, _pulse)
        def _done():
            w.destroy()
            if on_done: root.after(400, on_done)
        w.after(3500, _done)
    root.after(0, _make)

def show_got_you():
    def _make():
        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        w.geometry(f"{SW}x{SH}+0+0")
        w.configure(bg='#009900')
        f = tk.Frame(w, bg='#009900')
        f.place(relx=0.5, rely=0.45, anchor='center')
        tk.Label(f, text="I GOT YOU!! 😂😂😂",
                 font=("Impact", max(48, SW//16), "bold"),
                 fg='white', bg='#009900').pack()
        tk.Label(f, text="it was BonziBUDDY the whole time lmao",
                 font=("Arial", 24), fg='#ccffcc', bg='#009900').pack(pady=8)
        tk.Button(f, text="ok fine 😭  (close)", command=w.destroy,
                  font=("Arial", 18), bg='#007700', fg='white',
                  relief='flat', padx=22, pady=10).pack(pady=28)
        speak("I got you! It was BonziBUDDY the whole time! Mwahahaha!")
        laugh()
    root.after(0, _make)

# ── Fake File Cleaner window ──────────────────────────────────────────────────
FAKE_FILES = [
    r"C:\Windows\System32\svchost.exe",
    r"C:\Users\AppData\Local\Temp\~DF3A12.tmp",
    r"C:\Windows\System32\drivers\etc\hosts",
    r"C:\Users\Documents\passwords_backup.txt",
    r"C:\Program Files\Google\Chrome\chrome.exe",
    r"C:\Windows\explorer.exe",
    r"C:\Users\AppData\Roaming\Microsoft\crypto\rsa",
    r"C:\Windows\System32\lsass.exe",
    r"C:\Users\Pictures\family_photos.zip",
    r"C:\Windows\System32\winlogon.exe",
    r"C:\Users\Desktop\bank_info.xlsx",
    r"C:\Program Files\Discord\Discord.exe",
    r"C:\Windows\System32\ntoskrnl.exe",
    r"C:\Users\AppData\Local\Microsoft\Credentials",
    r"C:\Windows\SysWOW64\msvcrt.dll",
    r"C:\Users\Documents\school_project.docx",
    r"C:\Program Files\Steam\steam.exe",
    r"C:\Windows\System32\config\SAM",
    r"C:\Users\AppData\Local\Google\Chrome\User Data\Default\Login Data",
    r"C:\Windows\System32\drivers\ntfs.sys",
    r"C:\Users\Videos\important_recordings.mp4",
    r"C:\Windows\System32\kernel32.dll",
    r"C:\Users\AppData\Roaming\Discord\tokens.sqlite",
    r"C:\Program Files\Microsoft Office\WINWORD.EXE",
    r"C:\Users\Downloads\minecraft_installer.exe",
]
STATUSES = ["INFECTED ☠", "CRITICAL ⛔", "COMPROMISED ⚠", "SCANNING...", "THREAT FOUND 🔴"]

def open_file_cleaner():
    cw = tk.Toplevel()
    cw.title("BonziBUDDY File Cleaner 3.0  —  Threat Removal")
    cw.geometry(f"680x520+{SW//2-340}+{SH//2-260}")
    cw.configure(bg='#0a001a')
    cw.resizable(False, False)
    cw.attributes("-topmost", True)

    # Header
    hdr = tk.Frame(cw, bg='#5500aa', height=50)
    hdr.pack(fill='x'); hdr.pack_propagate(False)
    tk.Label(hdr, text="  🦍  BonziBUDDY File Cleaner 3.0  —  Scanning your PC...",
             font=("Segoe UI", 12, "bold"), bg='#5500aa', fg='white').pack(side='left', pady=10)

    # Status label
    status_var = tk.StringVar(value="Initializing deep scan...")
    tk.Label(cw, textvariable=status_var, font=("Consolas", 9),
             bg='#0a001a', fg='#cc88ff').pack(anchor='w', padx=12, pady=(6,2))

    # File listbox with scrollbar
    list_frame = tk.Frame(cw, bg='#0a001a')
    list_frame.pack(fill='both', expand=True, padx=12, pady=4)

    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side='right', fill='y')

    file_list = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                           bg='#0d0020', fg='#ff88cc', font=("Consolas", 8),
                           selectbackground='#5500aa', relief='flat',
                           highlightthickness=1, highlightbackground='#5500aa')
    file_list.pack(side='left', fill='both', expand=True)
    scrollbar.config(command=file_list.yview)

    # Progress bar (manual canvas)
    prog_frame = tk.Frame(cw, bg='#0a001a')
    prog_frame.pack(fill='x', padx=12, pady=4)
    tk.Label(prog_frame, text="SCAN PROGRESS:", font=("Consolas", 9),
             bg='#0a001a', fg='#cc88ff').pack(anchor='w')
    prog_c = tk.Canvas(prog_frame, width=656, height=22, bg='#1a0033',
                       highlightthickness=1, highlightbackground='#5500aa')
    prog_c.pack()

    # Threat counter
    count_var = tk.StringVar(value="Files scanned: 0 / 4,892  |  Threats found: 0")
    tk.Label(cw, textvariable=count_var, font=("Consolas", 9),
             bg='#0a001a', fg='#ff6699').pack(anchor='w', padx=12)

    # Confirm button (hidden initially)
    btn_frame = tk.Frame(cw, bg='#0a001a')
    btn_frame.pack(pady=10)
    confirm_btn = tk.Button(btn_frame, text="🗑  CONFIRM — DELETE ALL THREATS",
                            font=("Segoe UI", 13, "bold"), bg='#aa0055', fg='white',
                            relief='flat', padx=18, pady=10)
    confirm_btn.pack()
    confirm_btn.pack_forget()  # hidden until scan done

    def on_confirm():
        confirm_btn.config(state='disabled', text="Deleting files...")
        status_var.set("Deleting threats... please wait...")
        speak("Deleting all infected files. This may take a moment.")
        # Brief fake deletion then jumpscares
        cw.after(1200, lambda: show_pikachu_scare(
            on_done=lambda: show_freddy_scare(on_done=show_got_you)
        ))

    confirm_btn.config(command=on_confirm)

    # Animated scan in a thread
    def _scan():
        random.shuffle(FAKE_FILES)
        threats = [0]
        for i, fp in enumerate(FAKE_FILES):
            if not cw.winfo_exists():
                return
            time.sleep(random.uniform(0.08, 0.22))
            st = random.choice(STATUSES)
            if "SCANNING" not in st:
                threats[0] += 1
            display = f"{fp:<55}  {st}"
            def _add(d=display, t=threats[0], idx=i+1):
                if not cw.winfo_exists(): return
                file_list.insert('end', d)
                file_list.yview_moveto(1.0)
                # Color rows
                row = file_list.size()-1
                if 'INFECTED' in d or 'CRITICAL' in d:
                    file_list.itemconfig(row, fg='#ff4444')
                elif 'COMPROMISED' in d or 'THREAT' in d:
                    file_list.itemconfig(row, fg='#ff8800')
                else:
                    file_list.itemconfig(row, fg='#cc88ff')
                # Update progress
                pct = int(idx / len(FAKE_FILES) * 100)
                w_fill = int(656 * pct / 100)
                prog_c.delete("all")
                prog_c.create_rectangle(0, 0, w_fill, 22, fill='#aa00cc', outline='')
                prog_c.create_text(328, 11, text=f"{pct}%  ({idx}/{len(FAKE_FILES)} files)",
                                   fill='white', font=("Consolas", 8))
                count_var.set(f"Files scanned: {idx} / {len(FAKE_FILES)}  |  Threats found: {t}")
                status_var.set(f"Scanning: {d[:50]}...")
            root.after(0, _add)

        # Scan done
        def _done():
            if not cw.winfo_exists(): return
            status_var.set(f"⛔  SCAN COMPLETE — {threats[0]} CRITICAL THREATS FOUND. Immediate action required!")
            prog_c.delete("all")
            prog_c.create_rectangle(0, 0, 656, 22, fill='#ff0055', outline='')
            prog_c.create_text(328, 11,
                               text=f"SCAN COMPLETE — {threats[0]} THREATS — DELETE NOW",
                               fill='white', font=("Consolas", 8, "bold"))
            count_var.set(f"Files scanned: {len(FAKE_FILES)} / {len(FAKE_FILES)}  |  Threats: {threats[0]} CRITICAL")
            confirm_btn.pack()
            speak(f"Scan complete. Found {threats[0]} critical threats. Click confirm to delete them all.")
        root.after(0, _done)

    threading.Thread(target=_scan, daemon=True).start()

# ── Main BonziBUDDY window ────────────────────────────────────────────────────
BONZI_LINES = [
    ("Hi there! I'm BonziBUDDY! 👋",              True),
    ("Your friendly PC assistant!",                True),
    ("I just finished scanning your computer...",  False),
    ("And I found something VERY bad! 😱",         True),
    ("247 infected files detected on your PC!",    True),
    ("Trojan.Win32 AND spyware both active!",       True),
    ("Don't worry! I can fix this for you!",        True),
    ("Just click the DELETE button below!",         True),
    ("I'll clean EVERYTHING up for you! 😊",        True),
]

DODGE_MSGS = [
    "hehe 😏", "nope!", "too slow! 😂", "almost got me!",
    "try again!", "lol", "nuh uh!", "nice try 😂",
    "you'll never catch it!", "hehehe", "boop",
    "i'm faster than you!", "404: button not found",
    "keep trying! 😈",
]

UNLOCK_MSG = "ok ok fine... you win 😒\nnow click it for real"

def build_bonzi_window():
    main = tk.Toplevel()
    main.title("BonziBUDDY")
    main.geometry(f"420x560+{SW//2-210}+{SH//2-280}")
    main.configure(bg='#220033')
    main.resizable(False, False)
    main.attributes("-topmost", True)

    # ── Speech bubble canvas (top portion)
    speech_c = tk.Canvas(main, width=420, height=100, bg='#220033', highlightthickness=0)
    speech_c.pack()
    update_speech_bubble(speech_c, "Loading BonziBUDDY...", bx=20, by=8, bw=380, bh=68)

    # ── Bonzi canvas
    bonzi_c = tk.Canvas(main, width=420, height=380, bg='#220033', highlightthickness=0)
    bonzi_c.pack()
    draw_bonzi(bonzi_c, 210, 240)

    # ── Bottom frame (status + button)
    bot = tk.Frame(main, bg='#220033', height=80)
    bot.pack(fill='x'); bot.pack_propagate(False)

    status_lbl = tk.Label(bot, text="BonziBUDDY v4.2  |  Your friendly helper!",
                          font=("Segoe UI", 9), bg='#220033', fg='#cc88ff')
    status_lbl.pack(pady=(8,2))

    # DELETE button — uses place for free movement
    del_btn = tk.Button(main, text="🗑  DELETE VIRUSES",
                        font=("Segoe UI", 13, "bold"),
                        bg='#cc0055', fg='white', relief='flat',
                        padx=16, pady=9, cursor='hand2')
    del_btn.place(x=130, y=490)
    del_btn.place_forget()  # hidden initially

    # State tracking
    dodge_count = [0]
    max_dodges  = [16]
    dodging     = [True]
    line_idx    = [0]

    # ── Blink animation
    blink_on = [False]
    def _blink():
        if blink_on[0]:
            bonzi_c.itemconfig('eye_l',   fill='#8800dd')
            bonzi_c.itemconfig('eye_r',   fill='#8800dd')
            bonzi_c.itemconfig('pupil_l', fill='#8800dd')
            bonzi_c.itemconfig('pupil_r', fill='#8800dd')
            bonzi_c.itemconfig('shine_l', fill='#8800dd')
            bonzi_c.itemconfig('shine_r', fill='#8800dd')
            blink_on[0] = False
            main.after(110, _blink)
        else:
            bonzi_c.itemconfig('eye_l',   fill='white')
            bonzi_c.itemconfig('eye_r',   fill='white')
            bonzi_c.itemconfig('pupil_l', fill='#111')
            bonzi_c.itemconfig('pupil_r', fill='#111')
            bonzi_c.itemconfig('shine_l', fill='white')
            bonzi_c.itemconfig('shine_r', fill='white')
            blink_on[0] = True
            main.after(random.randint(2500, 5000), _blink)
    main.after(2000, _blink)

    # ── Advance through speech lines
    def _next_line():
        idx = line_idx[0]
        if idx < len(BONZI_LINES):
            text, do_speak = BONZI_LINES[idx]
            update_speech_bubble(speech_c, text, bx=20, by=8, bw=380, bh=68)
            if do_speak:
                speak(text)
            else:
                bonzi_boop()
            line_idx[0] += 1
            # After last line, show DELETE button
            if line_idx[0] >= len(BONZI_LINES):
                main.after(2000, _show_delete_btn)
            else:
                delay = 2800 + len(text) * 40
                main.after(delay, _next_line)
        else:
            _show_delete_btn()

    def _show_delete_btn():
        del_btn.place(x=130, y=490)
        update_speech_bubble(speech_c, "👆 Click that DELETE button!\nI'll clean everything for you!",
                             bx=20, by=8, bw=380, bh=68)
        speak("Click the delete button! I will clean everything for you!")

    main.after(800, _next_line)

    # ── Dodge logic
    def _dodge(event=None):
        if not dodging[0]:
            return
        dodge_count[0] += 1
        bonzi_boop()

        if dodge_count[0] >= max_dodges[0]:
            dodging[0] = False
            del_btn.place(x=130, y=490)
            del_btn.config(command=_on_real_click, bg='#880000',
                           text="🗑  DELETE VIRUSES  ← CLICK ME!")
            update_speech_bubble(speech_c, UNLOCK_MSG, bx=20, by=8, bw=380, bh=68)
            speak("Okay fine, you can click it now.")
            return

        # Teleport button to random position in lower window area
        nx = random.randint(20, 260)
        ny = random.randint(455, 510)
        del_btn.place(x=nx, y=ny)
        msg = random.choice(DODGE_MSGS)
        update_speech_bubble(speech_c, msg, bx=20, by=8, bw=380, bh=68)
        status_lbl.config(text=f"Dodge #{dodge_count[0]} / {max_dodges[0]}  hehe 😈")

    def _on_real_click():
        del_btn.config(state='disabled', text="Opening cleaner...")
        update_speech_bubble(speech_c, "Opening BonziBUDDY File Cleaner...\nThis will only take a moment! 😊",
                             bx=20, by=8, bw=380, bh=68)
        speak("Opening the file cleaner. Stand by!")
        main.after(1200, open_file_cleaner)

    del_btn.bind("<Enter>", _dodge)
    del_btn.bind("<Button-1>", lambda e: _dodge() if dodging[0] else None)

# ── Entry point ───────────────────────────────────────────────────────────────
root = tk.Tk()
root.withdraw()
root.after(300, build_bonzi_window)
root.mainloop()
