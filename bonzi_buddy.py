"""
bonzi_buddy.py — Fake BonziBUDDY prank. Transparent floating purple gorilla
wanders your desktop, tells facts & trivia, dodges the DELETE button, then
unleashes Pikachu + Freddy jumpscares. No voice.
Secret exit: type 4308. Right-click gorilla to close.
"""
import tkinter as tk
from tkinter import ttk
import random, threading, time, math
import ctypes, ctypes.wintypes, subprocess, os, tempfile

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

# ── Sounds (no beeps — only subtle) ──────────────────────────────────────────
def screech():
    def _do():
        for _ in range(45): kernel32.Beep(random.randint(300, 2200), 18)
        for f in [1800,1400,1000,600]: kernel32.Beep(f, 60)
    threading.Thread(target=_do, daemon=True).start()

# ── Drawing helpers ───────────────────────────────────────────────────────────
CHROMA = '#00fe01'   # transparent chroma-key color (near-lime, won't appear in drawing)

def draw_bubble(c, x1, y1, x2, y2, r=14, fill='white', out='#7733bb', lw=2, tag='bubble'):
    """Draw a rounded-corner speech bubble rectangle."""
    # Fill body
    c.create_rectangle(x1+r, y1,   x2-r, y2,   fill=fill, outline='', tags=tag)
    c.create_rectangle(x1,   y1+r, x2,   y2-r, fill=fill, outline='', tags=tag)
    # Fill corners
    c.create_oval(x1, y1, x1+2*r, y1+2*r, fill=fill, outline=out, width=lw, tags=tag)
    c.create_oval(x2-2*r, y1, x2, y1+2*r, fill=fill, outline=out, width=lw, tags=tag)
    c.create_oval(x1, y2-2*r, x1+2*r, y2, fill=fill, outline=out, width=lw, tags=tag)
    c.create_oval(x2-2*r, y2-2*r, x2, y2, fill=fill, outline=out, width=lw, tags=tag)
    # Outline edges
    c.create_line(x1+r, y1, x2-r, y1, fill=out, width=lw, tags=tag)
    c.create_line(x1+r, y2, x2-r, y2, fill=out, width=lw, tags=tag)
    c.create_line(x1, y1+r, x1, y2-r, fill=out, width=lw, tags=tag)
    c.create_line(x2, y1+r, x2, y2-r, fill=out, width=lw, tags=tag)

def update_bubble(canvas, text, CW=280):
    """Redraw the speech bubble with new text on the canvas."""
    canvas.delete('bubble')
    # Bubble rect
    draw_bubble(canvas, 8, 8, CW-8, 100, r=12, fill='white', out='#7733bb', lw=2, tag='bubble')
    # Pointer triangle (pointing down toward Bonzi head)
    mid = CW // 2
    canvas.create_polygon(mid-12, 100, mid+12, 100, mid, 126,
                          fill='white', outline='#7733bb', width=2, tags='bubble')
    canvas.create_polygon(mid-9, 101, mid+9, 101, mid, 124,
                          fill='white', outline='', tags='bubble')
    # Text
    canvas.create_text(CW//2, 54, text=text,
                       font=('Segoe UI', 10), fill='#220044',
                       width=CW-32, anchor='center', justify='center', tags='bubble')

def draw_bonzi(c, cx=140, hcy=230, hr=68):
    """
    Draw BonziBUDDY — round chubby purple gorilla.
    cx  = horizontal center
    hcy = head center y
    hr  = head radius
    """
    # ── Body (round, partially behind head)
    c.create_oval(cx-60, hcy+hr-20, cx+60, hcy+hr+140,
                  fill='#6622bb', outline='#4411aa', width=2)
    # Belly (lighter)
    c.create_oval(cx-36, hcy+hr, cx+36, hcy+hr+118,
                  fill='#9955dd', outline='')

    # ── Left arm (slightly raised — presenting gesture)
    c.create_oval(cx-hr-28, hcy-5, cx-hr+18, hcy+65,
                  fill='#6622bb', outline='#4411aa', width=2)
    # Left hand
    c.create_oval(cx-hr-32, hcy+50, cx-hr+10, hcy+88,
                  fill='#8844cc', outline='#4411aa', width=2)

    # ── Right arm
    c.create_oval(cx+hr-18, hcy-5, cx+hr+28, hcy+65,
                  fill='#6622bb', outline='#4411aa', width=2)
    # Right hand
    c.create_oval(cx+hr-10, hcy+50, cx+hr+32, hcy+88,
                  fill='#8844cc', outline='#4411aa', width=2)

    # ── Feet / legs (squat sitting)
    c.create_oval(cx-55, hcy+hr+110, cx-8,  hcy+hr+168,
                  fill='#6622bb', outline='#4411aa', width=2)
    c.create_oval(cx+8,  hcy+hr+110, cx+55, hcy+hr+168,
                  fill='#6622bb', outline='#4411aa', width=2)

    # ── HEAD (large, dominant, round)
    c.create_oval(cx-hr, hcy-hr, cx+hr, hcy+hr,
                  fill='#7733cc', outline='#4411aa', width=3)

    # ── Ears (small ovals on sides)
    c.create_oval(cx-hr-20, hcy-28, cx-hr+12, hcy+28,
                  fill='#6622bb', outline='#4411aa', width=2)
    c.create_oval(cx-hr-16, hcy-22, cx-hr+8, hcy+22,   # inner ear
                  fill='#cc77ff', outline='')
    c.create_oval(cx+hr-12, hcy-28, cx+hr+20, hcy+28,
                  fill='#6622bb', outline='#4411aa', width=2)
    c.create_oval(cx+hr-8,  hcy-22, cx+hr+16, hcy+22,
                  fill='#cc77ff', outline='')

    # ── Snout / muzzle (lighter oval in lower face)
    c.create_oval(cx-44, hcy+10, cx+44, hcy+hr-2,
                  fill='#bb88ee', outline='#9955cc', width=1)

    # ── EYES — very large, cartoon-style (the key Bonzi feature)
    ew = 26          # eye radius
    elx = cx - 34   # left eye center x
    erx = cx + 34   # right eye center x
    ecy = hcy - 16  # eye center y
    # White
    c.create_oval(elx-ew, ecy-ew, elx+ew, ecy+ew,
                  fill='white', outline='#222', width=2, tags='eye_l_w')
    c.create_oval(erx-ew, ecy-ew, erx+ew, ecy+ew,
                  fill='white', outline='#222', width=2, tags='eye_r_w')
    # Pupils (large dark circles)
    pw = 16
    c.create_oval(elx-pw, ecy-pw, elx+pw, ecy+pw, fill='#111', outline='', tags='eye_l_p')
    c.create_oval(erx-pw, ecy-pw, erx+pw, ecy+pw, fill='#111', outline='', tags='eye_r_p')
    # Iris ring around pupil
    c.create_oval(elx-pw, ecy-pw, elx+pw, ecy+pw, fill='', outline='#1a1a6e', width=2, tags='eye_l_i')
    c.create_oval(erx-pw, ecy-pw, erx+pw, ecy+pw, fill='', outline='#1a1a6e', width=2, tags='eye_r_i')
    # White shine dot
    c.create_oval(elx-10, ecy-15, elx+2, ecy-3, fill='white', outline='', tags='eye_l_s')
    c.create_oval(erx-10, ecy-15, erx+2, ecy-3, fill='white', outline='', tags='eye_r_s')

    # ── Nose (between eyes and mouth)
    c.create_oval(cx-12, hcy+14, cx+12, hcy+28, fill='#330055', outline='')
    c.create_oval(cx-10, hcy+16, cx-3,  hcy+26, fill='#110022', outline='')
    c.create_oval(cx+3,  hcy+16, cx+10, hcy+26, fill='#110022', outline='')

    # ── Mouth — signature wide Bonzi grin with visible teeth
    c.create_arc(cx-40, hcy+30, cx+40, hcy+64,
                 start=207, extent=126, style='chord',
                 fill='#110022', outline='#330055', width=2)
    # Teeth (5)
    for i in range(5):
        tx = cx - 30 + i*13
        c.create_rectangle(tx, hcy+36, tx+10, hcy+52,
                            fill='white', outline='#ccc', width=1)

    # ── Eyebrows (slightly raised = friendly expression)
    c.create_arc(cx-62, hcy-56, cx-14, hcy-20,
                 start=25, extent=130, style='arc', outline='#330055', width=3)
    c.create_arc(cx+14, hcy-56, cx+62, hcy-20,
                 start=25, extent=130, style='arc', outline='#330055', width=3)


def draw_pikachu(canvas, cx, cy, r):
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill='#FFD700', outline='#cc9900', width=4)
    # Left ear
    canvas.create_polygon(cx-r*.65,cy-r*.8, cx-r*.4,cy-r*1.45, cx-r*.05,cy-r*.82,
                          fill='#FFD700', outline='#cc9900', width=3)
    canvas.create_polygon(cx-r*.5,cy-r*1.02, cx-r*.4,cy-r*1.45, cx-r*.13,cy-r*1.0,
                          fill='#111', outline='')
    # Right ear
    canvas.create_polygon(cx+r*.05,cy-r*.82, cx+r*.4,cy-r*1.45, cx+r*.65,cy-r*.8,
                          fill='#FFD700', outline='#cc9900', width=3)
    canvas.create_polygon(cx+r*.13,cy-r*1.0, cx+r*.4,cy-r*1.45, cx+r*.5,cy-r*1.02,
                          fill='#111', outline='')
    er = r*.18
    canvas.create_oval(cx-r*.38-er,cy-r*.22-er, cx-r*.38+er,cy-r*.22+er, fill='#111', outline='')
    canvas.create_oval(cx+r*.38-er,cy-r*.22-er, cx+r*.38+er,cy-r*.22+er, fill='#111', outline='')
    sr = er*.38
    canvas.create_oval(cx-r*.43-sr,cy-r*.27-sr, cx-r*.43+sr,cy-r*.27+sr, fill='white', outline='')
    canvas.create_oval(cx+r*.33-sr,cy-r*.27-sr, cx+r*.33+sr,cy-r*.27+sr, fill='white', outline='')
    cr2 = r*.20
    canvas.create_oval(cx-r*.72-cr2,cy-cr2, cx-r*.72+cr2,cy+cr2, fill='#ff4444', outline='')
    canvas.create_oval(cx+r*.72-cr2,cy-cr2, cx+r*.72+cr2,cy+cr2, fill='#ff4444', outline='')
    mr = r*.23
    canvas.create_oval(cx-mr,cy+r*.18-mr, cx+mr,cy+r*.18+mr, fill='#111', outline='#333', width=2)
    canvas.create_text(cx, cy+r*.18, text='O', font=('Arial', int(r*.26), 'bold'), fill='#fff')

def draw_freddy(canvas, cx, cy, r):
    canvas.create_oval(cx-r, cy-r*1.05, cx+r, cy+r, fill='#150600', outline='#3d1500', width=5)
    er2 = r*.28
    canvas.create_oval(cx-r-er2*.5, cy-r*.35-er2, cx-r+er2*.5, cy-r*.35+er2,
                       fill='#220a00', outline='#3d1500', width=3)
    canvas.create_oval(cx+r-er2*.5, cy-r*.35-er2, cx+r+er2*.5, cy-r*.35+er2,
                       fill='#220a00', outline='#3d1500', width=3)
    eye_r = r*.23
    canvas.create_oval(cx-r*.42-eye_r,cy-r*.25-eye_r, cx-r*.42+eye_r,cy-r*.25+eye_r,
                       fill='#ffc300', outline='#ff8800', width=3)
    canvas.create_oval(cx+r*.42-eye_r,cy-r*.25-eye_r, cx+r*.42+eye_r,cy-r*.25+eye_r,
                       fill='#ffc300', outline='#ff8800', width=3)
    pr = eye_r*.45
    canvas.create_oval(cx-r*.42-pr,cy-r*.25-pr, cx-r*.42+pr,cy-r*.25+pr, fill='#000', outline='')
    canvas.create_oval(cx+r*.42-pr,cy-r*.25-pr, cx+r*.42+pr,cy-r*.25+pr, fill='#000', outline='')
    canvas.create_rectangle(cx-r*.75,cy-r*.98, cx+r*.75,cy-r*.82, fill='#0a0300', outline='#3d1500', width=3)
    canvas.create_rectangle(cx-r*.52,cy-r*1.45, cx+r*.52,cy-r*.9,  fill='#0a0300', outline='#3d1500', width=3)
    canvas.create_arc(cx-r*.62,cy+r*.05, cx+r*.62,cy+r*.78,
                      start=205, extent=130, style='chord', fill='#0a0300', outline='#3d1500', width=3)
    tw = r*.14; ts = cx-r*.45
    for i in range(5):
        tx = ts+i*(tw+r*.05)
        canvas.create_rectangle(tx,cy+r*.32, tx+tw,cy+r*.6, fill='white', outline='#aaa', width=1)

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
        draw_pikachu(c, SW//2, SH//2-50, r)
        c.create_text(SW//2, SH//2+r+45,
                      text="OH MY GOD IT'S PIKACHU!!",
                      font=("Impact", max(38, SW//22), "bold"), fill='#cc0000')
        c.create_text(SW//2, SH//2+r+105,
                      text="( click to continue )",
                      font=("Arial", 18), fill='#775500')
        def _next():
            w.destroy()
            if on_done: root.after(300, on_done)
        w.bind("<Button-1>", lambda e: _next())
        w.after(5500, _next)
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
        w.after(3800, _done)
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
                 font=("Impact", max(50, SW//17), "bold"),
                 fg='white', bg='#009900').pack()
        tk.Label(f, text="it was BonziBUDDY the whole time lmaooo",
                 font=("Arial", 22), fg='#ccffcc', bg='#009900').pack(pady=8)
        tk.Button(f, text="ok fine 😭  (close)", command=w.destroy,
                  font=("Arial", 18), bg='#007700', fg='white',
                  relief='flat', padx=22, pady=10).pack(pady=28)
    root.after(0, _make)

# ── Fake File Cleaner ─────────────────────────────────────────────────────────
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
    r"C:\Users\AppData\Local\Temp\setup_virus_420.exe",
]
STATUSES = ["INFECTED ☠", "CRITICAL ⛔", "COMPROMISED ⚠", "THREAT FOUND 🔴", "SCANNING..."]

def open_file_cleaner():
    cw = tk.Toplevel()
    cw.title("BonziBUDDY File Cleaner 3.0  —  Scanning for Threats")
    cw.geometry(f"700x530+{SW//2-350}+{SH//2-265}")
    cw.configure(bg='#0a001a')
    cw.resizable(False, False)
    cw.attributes("-topmost", True)

    hdr = tk.Frame(cw, bg='#5500aa', height=50)
    hdr.pack(fill='x'); hdr.pack_propagate(False)
    tk.Label(hdr, text="  🦍  BonziBUDDY File Cleaner 3.0  —  Deep Virus Scan",
             font=("Segoe UI", 12, "bold"), bg='#5500aa', fg='white').pack(side='left', pady=10)

    status_var = tk.StringVar(value="Starting deep scan of all drives...")
    tk.Label(cw, textvariable=status_var, font=("Consolas", 9),
             bg='#0a001a', fg='#cc88ff').pack(anchor='w', padx=12, pady=(6,2))

    lf = tk.Frame(cw, bg='#0a001a')
    lf.pack(fill='both', expand=True, padx=12, pady=4)
    sb = tk.Scrollbar(lf); sb.pack(side='right', fill='y')
    fl = tk.Listbox(lf, yscrollcommand=sb.set, bg='#0d0020', fg='#ff88cc',
                    font=("Consolas", 8), selectbackground='#5500aa',
                    relief='flat', highlightthickness=1, highlightbackground='#5500aa')
    fl.pack(side='left', fill='both', expand=True)
    sb.config(command=fl.yview)

    pf = tk.Frame(cw, bg='#0a001a')
    pf.pack(fill='x', padx=12, pady=4)
    tk.Label(pf, text="SCAN PROGRESS:", font=("Consolas", 9),
             bg='#0a001a', fg='#cc88ff').pack(anchor='w')
    pc = tk.Canvas(pf, width=676, height=22, bg='#1a0033',
                   highlightthickness=1, highlightbackground='#5500aa')
    pc.pack()

    count_var = tk.StringVar(value="Files scanned: 0  |  Threats: 0")
    tk.Label(cw, textvariable=count_var, font=("Consolas", 9),
             bg='#0a001a', fg='#ff6699').pack(anchor='w', padx=12)

    bf = tk.Frame(cw, bg='#0a001a')
    bf.pack(pady=8)
    confirm_btn = tk.Button(bf, text="🗑  CONFIRM — DELETE ALL THREATS",
                            font=("Segoe UI", 13, "bold"), bg='#aa0055', fg='white',
                            relief='flat', padx=18, pady=10)
    confirm_btn.pack(); confirm_btn.pack_forget()

    def on_confirm():
        confirm_btn.config(state='disabled', text="Deleting files... please wait...")
        status_var.set("Removing all infected files...")
        cw.after(1400, lambda: show_pikachu_scare(
            on_done=lambda: show_freddy_scare(on_done=show_got_you)))

    confirm_btn.config(command=on_confirm)

    def _scan():
        random.shuffle(FAKE_FILES)
        threats = [0]
        for i, fp in enumerate(FAKE_FILES):
            if not cw.winfo_exists(): return
            time.sleep(random.uniform(0.07, 0.20))
            st = random.choice(STATUSES)
            if "SCANNING" not in st: threats[0] += 1
            disp = f"{fp:<55}  {st}"
            def _add(d=disp, t=threats[0], idx=i+1):
                if not cw.winfo_exists(): return
                fl.insert('end', d)
                fl.yview_moveto(1.0)
                row = fl.size()-1
                if 'INFECTED' in d or 'CRITICAL' in d: fl.itemconfig(row, fg='#ff4444')
                elif 'COMPROMISED' in d or 'THREAT' in d: fl.itemconfig(row, fg='#ff8800')
                else: fl.itemconfig(row, fg='#cc88ff')
                pct = int(idx/len(FAKE_FILES)*100)
                wf  = int(676*pct/100)
                pc.delete("all")
                pc.create_rectangle(0,0,wf,22, fill='#aa00cc', outline='')
                pc.create_text(338,11, text=f"{pct}%  ({idx}/{len(FAKE_FILES)} files)",
                               fill='white', font=("Consolas",8))
                count_var.set(f"Files scanned: {idx}  |  Threats found: {t}")
                status_var.set(f"Scanning: {d[:52]}...")
            root.after(0, _add)

        def _done():
            if not cw.winfo_exists(): return
            status_var.set(f"⛔  SCAN COMPLETE — {threats[0]} CRITICAL THREATS FOUND!")
            pc.delete("all")
            pc.create_rectangle(0,0,676,22, fill='#ff0055', outline='')
            pc.create_text(338,11, text=f"COMPLETE — {threats[0]} THREATS — DELETE NOW",
                           fill='white', font=("Consolas",8,"bold"))
            count_var.set(f"Files scanned: {len(FAKE_FILES)}  |  Threats: {threats[0]} CRITICAL ⛔")
            confirm_btn.pack()
        root.after(0, _done)

    threading.Thread(target=_scan, daemon=True).start()

# ── BonziBUDDY message script ─────────────────────────────────────────────────
# Each entry: (display_text, delay_ms_before_next)
# "question" entries show text, wait, then show answer
SCRIPT = [
    # Intro
    ("Hi there! I'm BonziBUDDY! 👋",                              2800),
    ("Your helpful desktop companion!",                             2500),
    ("I know EVERYTHING about your computer.",                      2800),
    # Facts / trivia
    ("FUN FACT: Gorillas share 98.3% DNA with humans.\nI share 100% of your DESKTOP.",  3500),
    ("TRIVIA: What's the most popular password?\n...\n...it's yours, by the way.",       4000),
    ("DID YOU KNOW: BonziBUDDY was called spyware by the FTC.\nI am COMPLETELY different. Probably.",  4200),
    ("QUICK QUIZ: Is your antivirus up to date?\n...\n...The answer is no. I checked.",  4000),
    ("TRUE or FALSE: Your computer is totally safe.\n...\nFALSE. I'm literally right here. 😈",        4000),
    ("FUN FACT: The average human blinks 15 times per minute.\nYou haven't blinked since I appeared.", 3800),
    ("RIDDLE: What has keys but no locks, and I can see all of it?\n...\nYour keyboard. I'm watching.", 4200),
    # Pre-delete
    ("Hmm... I've been scanning your PC in the background...",     3000),
    ("And I found something VERY concerning. 😱",                  2800),
    ("247 INFECTED FILES detected on your computer!",              3000),
    ("Good news! I can fix this for you!",                         2500),
    ("Just click the DELETE button below! Easy!",                  2500),
]

DODGE_LINES = [
    "hehe 😏", "nope!", "too slow! 😂", "almost got me!",
    "try again!", "lol", "nuh uh!", "nice try 😂",
    "you'll never catch it!", "hehehe", "boop!",
    "i'm faster than u!", "404: button not found",
    "keep trying! 😈", "nice reflexes tho",
    "getting warmer!", "cold!", "HA",
]

# ── Main BonziBUDDY window ────────────────────────────────────────────────────
CW = 280   # canvas / window width
CH = 480   # canvas / window height

def build_bonzi():
    main = tk.Toplevel()
    main.overrideredirect(True)
    main.attributes("-topmost", True)
    main.configure(bg=CHROMA)
    # Transparent chroma-key: anything painted in CHROMA color becomes see-through
    try:
        main.wm_attributes('-transparentcolor', CHROMA)
    except Exception:
        pass  # fallback: non-transparent, still works fine

    # Start near center of screen
    start_x = SW//2 - CW//2
    start_y = SH//2 - CH//2
    main.geometry(f"{CW}x{CH}+{start_x}+{start_y}")

    # ── Canvas (same chroma bg so gorilla floats)
    c = tk.Canvas(main, width=CW, height=CH, bg=CHROMA, highlightthickness=0)
    c.pack()

    # ── Draw Bonzi (head center at y=255 roughly)
    draw_bonzi(c, cx=CW//2, hcy=258, hr=68)

    # ── Initial speech bubble
    update_bubble(c, "Loading BonziBUDDY...", CW)

    # ── Drag support (so user can move the floating gorilla)
    drag = {'x': 0, 'y': 0}
    def _press(e):
        drag['x'] = e.x_root; drag['y'] = e.y_root
    def _drag(e):
        dx = e.x_root - drag['x']; dy = e.y_root - drag['y']
        main.geometry(f"+{main.winfo_x()+dx}+{main.winfo_y()+dy}")
        drag['x'] = e.x_root; drag['y'] = e.y_root
    def _right_click(e):
        main.destroy()
    c.bind("<Button-1>",  _press)
    c.bind("<B1-Motion>", _drag)
    c.bind("<Button-3>",  _right_click)

    # ── Auto-wander: slowly drift to new random positions
    wander_active = [True]
    def _wander():
        if not wander_active[0] or not main.winfo_exists(): return
        tx = random.randint(40, SW-CW-40)
        ty = random.randint(40, SH-CH-40)
        steps = 60
        cur   = [main.winfo_x(), main.winfo_y()]
        def _step(s=0):
            if s >= steps or not main.winfo_exists(): return
            t = s / steps
            ease = t * t * (3 - 2*t)   # smoothstep
            nx = int(cur[0] + (tx-cur[0]) * ease)
            ny = int(cur[1] + (ty-cur[1]) * ease)
            try: main.geometry(f"+{nx}+{ny}")
            except: return
            main.after(22, lambda: _step(s+1))
        _step()
        main.after(random.randint(7000, 14000), _wander)
    main.after(4000, _wander)

    # ── Blink animation
    def _blink():
        if not main.winfo_exists(): return
        # Close eyes
        c.itemconfig('eye_l_w', fill='#7733cc')
        c.itemconfig('eye_r_w', fill='#7733cc')
        c.itemconfig('eye_l_p', fill='#7733cc')
        c.itemconfig('eye_r_p', fill='#7733cc')
        c.itemconfig('eye_l_s', fill='#7733cc')
        c.itemconfig('eye_r_s', fill='#7733cc')
        c.itemconfig('eye_l_i', outline='#7733cc')
        c.itemconfig('eye_r_i', outline='#7733cc')
        def _reopen():
            if not main.winfo_exists(): return
            c.itemconfig('eye_l_w', fill='white')
            c.itemconfig('eye_r_w', fill='white')
            c.itemconfig('eye_l_p', fill='#111')
            c.itemconfig('eye_r_p', fill='#111')
            c.itemconfig('eye_l_s', fill='white')
            c.itemconfig('eye_r_s', fill='white')
            c.itemconfig('eye_l_i', outline='#1a1a6e')
            c.itemconfig('eye_r_i', outline='#1a1a6e')
            main.after(random.randint(2800, 5500), _blink)
        main.after(100, _reopen)
    main.after(2000, _blink)

    # ── Script / message cycling ──────────────────────────────────────────────
    script_idx = [0]
    phase      = ['script']  # 'script' → 'dodge' → 'done'

    # DELETE button (hidden initially, positioned via canvas.create_window)
    del_btn = tk.Button(main, text="  🗑  DELETE VIRUSES  ",
                        font=("Segoe UI", 12, "bold"),
                        bg='#cc0044', fg='white', relief='flat',
                        activebackground='#aa0033', activeforeground='white',
                        cursor='hand2')
    del_item = c.create_window(CW//2, CH-38, window=del_btn, anchor='center')
    c.itemconfig(del_item, state='hidden')

    dodge_count = [0]
    MAX_DODGES  = 18

    def _dodge(event=None):
        if phase[0] != 'dodge': return
        dodge_count[0] += 1
        if dodge_count[0] >= MAX_DODGES:
            phase[0] = 'done'
            # Stop dodging — lock the button in place
            c.coords(del_item, CW//2, CH-38)
            del_btn.config(command=_on_click, bg='#880000',
                           text="  🗑  DELETE VIRUSES  ← CLICK ME  ")
            update_bubble(c, "ok ok... you got me.\nfine. click it. i dare you. 😒", CW)
            return
        # Teleport button to random position in lower half of window
        nx = random.randint(50, CW-50)
        ny = random.randint(CH-90, CH-20)
        c.coords(del_item, nx, ny)
        update_bubble(c, random.choice(DODGE_LINES), CW)

    del_btn.bind("<Enter>",    _dodge)
    del_btn.bind("<Button-1>", lambda e: _dodge() if phase[0]=='dodge' else None)

    def _on_click():
        c.itemconfig(del_item, state='hidden')
        update_bubble(c, "Opening BonziBUDDY File Cleaner...\nStand by! 😊", CW)
        main.after(1400, open_file_cleaner)

    def _show_script_line():
        if not main.winfo_exists(): return
        idx = script_idx[0]
        if idx >= len(SCRIPT):
            # All script done — enter dodge phase
            phase[0] = 'dodge'
            c.itemconfig(del_item, state='normal')
            update_bubble(c, "👆 Click that DELETE button below!\nI'll clean everything for you!", CW)
            return
        text, delay = SCRIPT[idx]
        update_bubble(c, text, CW)
        script_idx[0] += 1
        main.after(delay, _show_script_line)

    main.after(800, _show_script_line)

# ── Entry point ───────────────────────────────────────────────────────────────
root = tk.Tk()
root.withdraw()
root.after(300, build_bonzi)
root.mainloop()
