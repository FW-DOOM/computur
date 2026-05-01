"""
bonzi_buddy.py — Fake BonziBUDDY desktop companion prank.
REAL Bonzi Buddy sprites! Wanders your desktop.
Left-click drag to move. Right-click for options menu.
Jumpscares at the end. Secret exit: type 4308. Restore hidden Bonzi: type 1111.
"""
import tkinter as tk
import random, threading, time, base64, io, sys, subprocess, os
import ctypes, ctypes.wintypes

# Auto-install Pillow if needed
try:
    from PIL import Image, ImageTk
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Pillow', '-q'])
    from PIL import Image, ImageTk

user32   = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
SW = user32.GetSystemMetrics(0)
SH = user32.GetSystemMetrics(1)

# ── Real Bonzi Buddy sprites — imported from bonzi_b64.py ────────────────────
# (200×160 RGBA PNGs extracted from original BonziBUDDY ACS character file)
from bonzi_b64 import BONZI_F0, BONZI_F26, BONZI_F27

# ── Image / canvas constants ──────────────────────────────────────────────────
CHROMA = '#00fe01'          # transparent chroma key = RGB(0,254,1)
SCALE  = 2.0
IMG_W  = int(200 * SCALE)   # 400
IMG_H  = int(160 * SCALE)   # 320
CW, CH = 420, 480
IMG_CX = CW // 2            # 210
IMG_CY = 250                # image centre y → image occupies canvas y=90..410

_photo_cache = {}

def _decode_frame(b64str):
    data = base64.b64decode(b64str)
    img  = Image.open(io.BytesIO(data)).convert('RGBA')
    return img.resize((IMG_W, IMG_H), Image.LANCZOS)

def _to_photo(rgba_img):
    bg = Image.new('RGBA', (IMG_W, IMG_H), (0, 254, 1, 255))
    bg.paste(rgba_img, (0, 0), rgba_img)
    return ImageTk.PhotoImage(bg.convert('RGB'))

def load_bonzi_frames():
    f0  = _decode_frame(BONZI_F0)
    f26 = _decode_frame(BONZI_F26)
    f27 = _decode_frame(BONZI_F27)
    b1  = f0.copy(); b1.paste(f26, (0, 0), f26)
    b2  = f0.copy(); b2.paste(f27, (0, 0), f27)
    return _to_photo(f0), _to_photo(b1), _to_photo(b2)

# ── Global Bonzi window ref (for reappear via 1111) ───────────────────────────
_bonzi_main = [None]

# ── Global keyboard hook — exit: 4308 | restore: 1111 ────────────────────────
class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [('vkCode',     ctypes.c_uint32),
                ('scanCode',   ctypes.c_uint32),
                ('flags',      ctypes.c_uint32),
                ('time',       ctypes.c_uint32),
                ('dwExtraInfo',ctypes.POINTER(ctypes.c_ulong))]

HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int,
                               ctypes.POINTER(KBDLLHOOKSTRUCT))
_sb = []

def _kb(n, w, l):
    if n >= 0 and w == 0x0100:
        v = l.contents.vkCode
        if 0x30 <= v <= 0x39:
            _sb.append(chr(v))
            if len(_sb) > 4: _sb.pop(0)
            seq = ''.join(_sb)
            if seq == '4308':
                os._exit(0)
            if seq == '1111':
                def _restore():
                    m = _bonzi_main[0]
                    if m is not None:
                        try:
                            if m.winfo_exists():
                                m.deiconify()
                                m.attributes('-topmost', True)
                                return
                        except: pass
                    build_bonzi()
                root.after(0, _restore)
    return user32.CallNextHookEx(None, n, w, l)

_kbp = HOOKPROC(_kb)

def _ht():
    user32.SetWindowsHookExW(13, _kbp, None, 0)
    m = ctypes.wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(m), None, 0, 0) != 0:
        user32.TranslateMessage(ctypes.byref(m))
        user32.DispatchMessageW(ctypes.byref(m))

threading.Thread(target=_ht, daemon=True).start()

# ── Sounds ────────────────────────────────────────────────────────────────────
def play_pikachu_meme():
    def _do():
        ps = (
            "Add-Type -AssemblyName System.Speech; "
            "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            "foreach ($v in $s.GetInstalledVoices()) { "
            "  if ($v.VoiceInfo.Gender -eq 'Female') { $s.SelectVoice($v.VoiceInfo.Name); break } }; "
            "$s.Rate = 9; $s.Volume = 100; "
            "$s.Speak('Oh my GOD! It s PIKACHU!!!');"
        )
        try:
            subprocess.Popen(["powershell", "-WindowStyle", "Hidden", "-Command", ps],
                             creationflags=subprocess.CREATE_NO_WINDOW)
        except: pass
    threading.Thread(target=_do, daemon=True).start()

def screech():
    def _do():
        for _ in range(45): kernel32.Beep(random.randint(300, 2200), 18)
        for f in [1800, 1400, 1000, 600]: kernel32.Beep(f, 60)
    threading.Thread(target=_do, daemon=True).start()

# ── Speech bubble ─────────────────────────────────────────────────────────────
def draw_bubble(c, x1, y1, x2, y2, r=12, fill='white', out='#4A0A99', lw=2, tag='bubble'):
    c.create_rectangle(x1+r, y1,    x2-r, y2,    fill=fill, outline='',          tags=tag)
    c.create_rectangle(x1,   y1+r,  x2,   y2-r,  fill=fill, outline='',          tags=tag)
    c.create_oval(x1,       y1,       x1+2*r, y1+2*r, fill=fill, outline=out, width=lw, tags=tag)
    c.create_oval(x2-2*r,   y1,       x2,     y1+2*r, fill=fill, outline=out, width=lw, tags=tag)
    c.create_oval(x1,       y2-2*r,   x1+2*r, y2,     fill=fill, outline=out, width=lw, tags=tag)
    c.create_oval(x2-2*r,   y2-2*r,   x2,     y2,     fill=fill, outline=out, width=lw, tags=tag)
    c.create_line(x1+r, y1, x2-r, y1, fill=out, width=lw, tags=tag)
    c.create_line(x1+r, y2, x2-r, y2, fill=out, width=lw, tags=tag)
    c.create_line(x1, y1+r, x1, y2-r, fill=out, width=lw, tags=tag)
    c.create_line(x2, y1+r, x2, y2-r, fill=out, width=lw, tags=tag)

def update_bubble(c, text):
    c.delete('bubble')
    bx1, by1, bx2, by2 = 8, 8, CW-8, 100
    draw_bubble(c, bx1, by1, bx2, by2, tag='bubble')
    mid = CW // 2
    c.create_polygon(mid-13, by2, mid+13, by2, mid, by2+24,
                     fill='white', outline='#4A0A99', width=2, tags='bubble')
    c.create_polygon(mid-10, by2+1, mid+10, by2+1, mid, by2+22,
                     fill='white', outline='', tags='bubble')
    c.create_text(CW//2, (by1+by2)//2, text=text,
                  font=('Segoe UI', 10), fill='#220044',
                  width=CW-30, anchor='center', justify='center', tags='bubble')

# ── Pikachu ───────────────────────────────────────────────────────────────────
def draw_pikachu(c, cx, cy, r):
    c.create_oval(cx-r, cy-r*0.94, cx+r, cy+r*0.96, fill='#FFD700', outline='#cc8800', width=4)
    c.create_polygon(cx-r*0.20, cy-r*0.80, cx-r*0.72, cy-r*1.55, cx-r*0.62, cy-r*0.72,
                     fill='#FFD700', outline='#cc8800', width=3)
    c.create_polygon(cx-r*0.30, cy-r*1.15, cx-r*0.72, cy-r*1.55, cx-r*0.62, cy-r*1.02,
                     fill='#1a1a1a', outline='')
    c.create_polygon(cx+r*0.20, cy-r*0.80, cx+r*0.62, cy-r*0.72, cx+r*0.72, cy-r*1.55,
                     fill='#FFD700', outline='#cc8800', width=3)
    c.create_polygon(cx+r*0.30, cy-r*1.15, cx+r*0.62, cy-r*1.02, cx+r*0.72, cy-r*1.55,
                     fill='#1a1a1a', outline='')
    ew = r*0.19; eh = r*0.23
    c.create_oval(cx-r*0.34-ew, cy-r*0.22-eh, cx-r*0.34+ew, cy-r*0.22+eh, fill='#111', outline='')
    c.create_oval(cx+r*0.34-ew, cy-r*0.22-eh, cx+r*0.34+ew, cy-r*0.22+eh, fill='#111', outline='')
    sr = ew*0.4
    c.create_oval(cx-r*0.41-sr, cy-r*0.30-sr, cx-r*0.41+sr, cy-r*0.30+sr, fill='white', outline='')
    c.create_oval(cx+r*0.27-sr, cy-r*0.30-sr, cx+r*0.27+sr, cy-r*0.30+sr, fill='white', outline='')
    cr2 = r*0.22
    c.create_oval(cx-r*0.72-cr2, cy+r*0.04-cr2, cx-r*0.72+cr2, cy+r*0.04+cr2, fill='#FF4500', outline='')
    c.create_oval(cx+r*0.72-cr2, cy+r*0.04-cr2, cx+r*0.72+cr2, cy+r*0.04+cr2, fill='#FF4500', outline='')
    c.create_oval(cx-r*0.09, cy+r*0.06, cx+r*0.09, cy+r*0.18, fill='#553300', outline='')
    mw = r*0.29; mh = r*0.26
    c.create_oval(cx-mw, cy+r*0.26-mh, cx+mw, cy+r*0.26+mh, fill='#331100', outline='#110000', width=2)
    c.create_oval(cx-mw*0.75, cy+r*0.26-mh*0.68, cx+mw*0.75, cy+r*0.26+mh*0.62, fill='#CC3344', outline='')
    c.create_oval(cx-mw*0.42, cy+r*0.26+mh*0.00, cx+mw*0.42, cy+r*0.26+mh*0.55, fill='#DD5566', outline='')
    c.create_arc(cx-r*0.5, cy+r*0.50, cx+r*0.5, cy+r*0.95, start=200, extent=140,
                 style='arc', outline='#cc8800', width=2)

# ── Freddy ────────────────────────────────────────────────────────────────────
def draw_freddy(c, cx, cy, r):
    c.create_oval(cx-r, cy-r*1.05, cx+r, cy+r, fill='#150600', outline='#3d1500', width=5)
    er2 = r*.28
    c.create_oval(cx-r-er2*.5, cy-r*.35-er2, cx-r+er2*.5, cy-r*.35+er2, fill='#220a00', outline='#3d1500', width=3)
    c.create_oval(cx+r-er2*.5, cy-r*.35-er2, cx+r+er2*.5, cy-r*.35+er2, fill='#220a00', outline='#3d1500', width=3)
    eye_r = r*.23
    c.create_oval(cx-r*.42-eye_r, cy-r*.25-eye_r, cx-r*.42+eye_r, cy-r*.25+eye_r, fill='#ffc300', outline='#ff8800', width=3)
    c.create_oval(cx+r*.42-eye_r, cy-r*.25-eye_r, cx+r*.42+eye_r, cy-r*.25+eye_r, fill='#ffc300', outline='#ff8800', width=3)
    pr = eye_r*.45
    c.create_oval(cx-r*.42-pr, cy-r*.25-pr, cx-r*.42+pr, cy-r*.25+pr, fill='#000', outline='')
    c.create_oval(cx+r*.42-pr, cy-r*.25-pr, cx+r*.42+pr, cy-r*.25+pr, fill='#000', outline='')
    c.create_rectangle(cx-r*.75, cy-r*.98, cx+r*.75, cy-r*.82, fill='#0a0300', outline='#3d1500', width=3)
    c.create_rectangle(cx-r*.52, cy-r*1.45, cx+r*.52, cy-r*.9, fill='#0a0300', outline='#3d1500', width=3)
    c.create_arc(cx-r*.62, cy+r*.05, cx+r*.62, cy+r*.78, start=205, extent=130,
                 style='chord', fill='#0a0300', outline='#3d1500', width=3)
    tw = r*.14; ts = cx-r*.45
    for i in range(5):
        tx = ts + i*(tw+r*.05)
        c.create_rectangle(tx, cy+r*.32, tx+tw, cy+r*.6, fill='white', outline='#aaa', width=1)

# ── Jumpscares ────────────────────────────────────────────────────────────────
def show_pikachu_scare(on_done=None):
    def _make():
        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes('-topmost', True)
        w.geometry(f'{SW}x{SH}+0+0')
        w.configure(bg='#FFD700')
        c2 = tk.Canvas(w, width=SW, height=SH, bg='#FFD700', highlightthickness=0)
        c2.pack()
        r = min(SW, SH) * 0.31
        draw_pikachu(c2, SW//2, SH//2-55, r)
        c2.create_text(SW//2, SH//2+r+40, text="OH MY GOD IT'S PIKACHU!!",
                       font=('Impact', max(40, SW//22), 'bold'), fill='#cc0000')
        c2.create_text(SW//2, SH//2+r+100, text='( click to continue )',
                       font=('Arial', 18), fill='#775500')
        play_pikachu_meme()
        def _next():
            w.destroy()
            if on_done: root.after(400, on_done)
        w.bind('<Button-1>', lambda e: _next())
        w.after(6000, _next)
    root.after(0, _make)

def show_freddy_scare(on_done=None):
    def _make():
        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes('-topmost', True)
        w.geometry(f'{SW}x{SH}+0+0')
        w.configure(bg='#000')
        c2 = tk.Canvas(w, width=SW, height=SH, bg='#000', highlightthickness=0)
        c2.pack()
        r = min(SW, SH) * 0.34
        draw_freddy(c2, SW//2, SH//2-35, r)
        screech()
        p = [0]
        def _p():
            p[0] += 1
            c2.configure(bg='#ff2200' if p[0]%2==0 else '#000')
            if p[0] < 10: w.after(110, _p)
            else: c2.configure(bg='#000')
        w.after(80, _p)
        def _done():
            w.destroy()
            if on_done: root.after(400, on_done)
        w.after(3800, _done)
    root.after(0, _make)

def show_got_you():
    def _make():
        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes('-topmost', True)
        w.geometry(f'{SW}x{SH}+0+0')
        w.configure(bg='#009900')
        f = tk.Frame(w, bg='#009900')
        f.place(relx=0.5, rely=0.44, anchor='center')
        tk.Label(f, text='I GOT YOU!! \U0001f602\U0001f602\U0001f602',
                 font=('Impact', max(50, SW//16), 'bold'), fg='white', bg='#009900').pack()
        tk.Label(f, text='it was BonziBUDDY the whole time lmaoooo',
                 font=('Arial', 22), fg='#ccffcc', bg='#009900').pack(pady=8)
        tk.Button(f, text='ok fine \U0001f62d', command=w.destroy,
                  font=('Arial', 18), bg='#007700', fg='white',
                  relief='flat', padx=22, pady=10).pack(pady=28)
    root.after(0, _make)

# ── Fake File Cleaner ─────────────────────────────────────────────────────────
FAKE_FILES = [
    r'C:\Windows\System32\svchost.exe',
    r'C:\Users\AppData\Local\Temp\~DF3A12.tmp',
    r'C:\Windows\System32\drivers\etc\hosts',
    r'C:\Users\Documents\passwords_backup.txt',
    r'C:\Program Files\Google\Chrome\chrome.exe',
    r'C:\Windows\explorer.exe',
    r'C:\Users\AppData\Roaming\Microsoft\crypto\rsa',
    r'C:\Windows\System32\lsass.exe',
    r'C:\Users\Pictures\family_photos.zip',
    r'C:\Windows\System32\winlogon.exe',
    r'C:\Users\Desktop\bank_info.xlsx',
    r'C:\Program Files\Discord\Discord.exe',
    r'C:\Windows\System32\ntoskrnl.exe',
    r'C:\Users\AppData\Local\Microsoft\Credentials',
    r'C:\Windows\SysWOW64\msvcrt.dll',
    r'C:\Users\Documents\homework_final.docx',
    r'C:\Program Files\Steam\steam.exe',
    r'C:\Windows\System32\config\SAM',
    r'C:\Users\AppData\Local\Google\Chrome\User Data\Default\Login Data',
    r'C:\Windows\System32\drivers\ntfs.sys',
    r'C:\Users\Videos\my_videos.mp4',
    r'C:\Windows\System32\kernel32.dll',
    r'C:\Users\AppData\Roaming\Discord\tokens.sqlite',
]
STATUSES = ['INFECTED ☠', 'CRITICAL ⛔', 'COMPROMISED ⚠', 'THREAT FOUND \U0001f534', 'SCANNING...', 'SUSPICIOUS ⚠']

def open_file_cleaner():
    cw = tk.Toplevel()
    cw.title('BonziBUDDY File Cleaner 3.0')
    cw.geometry(f'700x530+{SW//2-350}+{SH//2-265}')
    cw.configure(bg='#0a001a'); cw.resizable(False, False)
    cw.attributes('-topmost', True)

    hdr = tk.Frame(cw, bg='#5500aa', height=50)
    hdr.pack(fill='x'); hdr.pack_propagate(False)
    tk.Label(hdr, text='  \U0001f98d  BonziBUDDY File Cleaner 3.0  —  Deep Scan',
             font=('Segoe UI', 12, 'bold'), bg='#5500aa', fg='white').pack(side='left', pady=10)

    sv = tk.StringVar(value='Initializing deep scan of all drives...')
    tk.Label(cw, textvariable=sv, font=('Consolas', 9), bg='#0a001a', fg='#cc88ff').pack(anchor='w', padx=12, pady=(6,2))

    lf = tk.Frame(cw, bg='#0a001a'); lf.pack(fill='both', expand=True, padx=12, pady=4)
    sb2 = tk.Scrollbar(lf); sb2.pack(side='right', fill='y')
    fl = tk.Listbox(lf, yscrollcommand=sb2.set, bg='#0d0020', fg='#ff88cc',
                    font=('Consolas', 8), selectbackground='#5500aa',
                    relief='flat', highlightthickness=1, highlightbackground='#5500aa')
    fl.pack(side='left', fill='both', expand=True)
    sb2.config(command=fl.yview)

    pf = tk.Frame(cw, bg='#0a001a'); pf.pack(fill='x', padx=12, pady=4)
    tk.Label(pf, text='SCAN PROGRESS:', font=('Consolas', 9), bg='#0a001a', fg='#cc88ff').pack(anchor='w')
    pc = tk.Canvas(pf, width=676, height=22, bg='#1a0033',
                   highlightthickness=1, highlightbackground='#5500aa'); pc.pack()

    cv = tk.StringVar(value='Files scanned: 0  |  Threats: 0')
    tk.Label(cw, textvariable=cv, font=('Consolas', 9), bg='#0a001a', fg='#ff6699').pack(anchor='w', padx=12)

    bf = tk.Frame(cw, bg='#0a001a'); bf.pack(pady=8)
    cb = tk.Button(bf, text='\U0001f5d1  CONFIRM — DELETE ALL THREATS',
                   font=('Segoe UI', 13, 'bold'), bg='#aa0055', fg='white', relief='flat', padx=18, pady=10)
    cb.pack(); cb.pack_forget()

    def on_confirm():
        cb.config(state='disabled', text='Deleting files...')
        sv.set('Removing all infected files...')
        cw.after(1400, lambda: show_pikachu_scare(
            on_done=lambda: show_freddy_scare(on_done=show_got_you)))
    cb.config(command=on_confirm)

    def _scan():
        random.shuffle(FAKE_FILES)
        t = [0]
        for i, fp in enumerate(FAKE_FILES):
            if not cw.winfo_exists(): return
            time.sleep(random.uniform(0.07, 0.20))
            st = random.choice(STATUSES)
            if 'SCANNING' not in st: t[0] += 1
            d = f'{fp:<55}  {st}'
            def _add(d=d, t2=t[0], idx=i+1):
                if not cw.winfo_exists(): return
                fl.insert('end', d); fl.yview_moveto(1.0)
                row = fl.size()-1
                if 'INFECTED' in d or 'CRITICAL' in d: fl.itemconfig(row, fg='#ff4444')
                elif 'COMPROMISED' in d or 'THREAT' in d: fl.itemconfig(row, fg='#ff8800')
                else: fl.itemconfig(row, fg='#cc88ff')
                pct = int(idx/len(FAKE_FILES)*100); wf = int(676*pct/100)
                pc.delete('all')
                pc.create_rectangle(0, 0, wf, 22, fill='#aa00cc', outline='')
                pc.create_text(338, 11, text=f'{pct}%  ({idx}/{len(FAKE_FILES)} files)',
                               fill='white', font=('Consolas', 8))
                cv.set(f'Files scanned: {idx}  |  Threats found: {t2}')
                sv.set(f'Scanning: {d[:52]}...')
            root.after(0, _add)
        def _done():
            if not cw.winfo_exists(): return
            sv.set(f'⛔  SCAN COMPLETE — {t[0]} CRITICAL THREATS FOUND!')
            pc.delete('all')
            pc.create_rectangle(0, 0, 676, 22, fill='#ff0055', outline='')
            pc.create_text(338, 11, text=f'COMPLETE — {t[0]} THREATS — DELETE NOW',
                           fill='white', font=('Consolas', 8, 'bold'))
            cv.set(f'Scanned: {len(FAKE_FILES)}  |  Threats: {t[0]} CRITICAL ⛔')
            cb.pack()
        root.after(0, _done)
    threading.Thread(target=_scan, daemon=True).start()

# ── Menu content ──────────────────────────────────────────────────────────────
FACTS = [
    'FACT: Gorillas share 98.3% DNA with humans!\nI share 100% of your DESKTOP. Lucky you.',
    'FACT: A group of gorillas is called a troop!\nI\'m invading yours. One PC at a time. \U0001f98d',
    'FACT: BonziBUDDY launched in 1999!\nI have been in computers for 25 years. I am eternal.',
    'FACT: The first computer virus was created in 1971!\nI am NOT a virus. I\'m a companion. Very different.',
    'FACT: Your PC has billions of transistors!\nI have taken control of all of them. \U0001f608',
    'FACT: Gorillas can live 50 years in captivity!\nI will live in this PC FOREVER.',
    'FACT: The average person types 40 words per minute!\nI can read every single one. Just saying. \U0001f440',
    'FACT: RAM stands for Random Access Memory!\nYours is running out. Because of me. Sorry. Not sorry.',
]

TRIVIA = [
    ('TRIVIA: What does CPU stand for?',
     'Central Processing Unit!\nI\'ve been processing your files.\nFor fun. While you slept.'),
    ('TRIVIA: What year was Windows XP released?',
     '2001!\nBack when BonziBUDDY ruled the internet.\nThose were MY glory days. \U0001f624'),
    ('TRIVIA: What\'s the most common password in the world?',
     '123456!\nPlease change yours.\nAlso... I already know it. \U0001f440'),
    ('TRIVIA: How many bytes are in a kilobyte?',
     '1,024 bytes!\nI\'ve used all of yours.\nSorry. No I\'m not.'),
    ('TRIVIA: What color is BonziBUDDY?',
     'PURPLE!\nThe most superior color ever created.\nNo debate. No arguments. PURPLE.'),
    ('TRIVIA: What was BonziBUDDY called by the FTC?',
     'SPYWARE!\nBut that was the OLD me.\nThe new me is completely trustworthy. \U0001f607'),
]

JOKES = [
    'Why did the computer go to the doctor?\nIt had a VIRUS! Just like yours does right now! \U0001f602',
    'Why was the computer late to work?\nIt had a hard drive! ...get it? HARD DRIVE? \U0001f480',
    'What do you call a sleeping computer?\nA HARD drive! Wait I already used that one. Oh well.',
    'Why don\'t computers take naps?\nBecause they\'re afraid of crashing!\nMuch like YOURS is about to. \U0001f608',
    'What\'s a gorilla\'s favorite computer?\nA DELL! A DELL-gorilla! GET IT!\nI\'ll be here all week. \U0001f98d',
    'How many programmers does it take to change a lightbulb?\nNone. That\'s a HARDWARE problem.',
    'Why did the computer squeak?\nSomeone stepped on the mouse! ...that mouse is MINE now btw.',
]

FIXES = [
    'PC running slow?\n→ Step 1: Close unused apps\n→ Step 2: Restart\n→ Step 3: Accept the chaos \U0001f98d',
    'Computer overheating?\n→ Check airflow vents\n→ Clean dust from fans\n→ Or just let it cook. \U0001f525',
    'WiFi not working?\n→ Restart your router\n→ Restart your modem\n→ Restart your LIFE.',
    'Getting weird pop-ups?\n→ Run antivirus\n→ Clear browser cache\n→ Or just enjoy the vibes. \U0001f608',
    'Hard drive making noise?\n→ Back up your files NOW\n→ Buy a replacement drive\n→ Say goodbye. \U0001f480',
    'Computer frozen?\n→ Wait 3 minutes\n→ If still frozen, gently weep\n→ Then hit power. Carefully.',
]

ABOUT_LINES = [
    'BonziBUDDY v4.2\nYour trusted desktop companion!\n© Totally Not Spyware Inc. 1999-Forever \U0001f98d',
    'I can tell jokes, share facts,\nfix your computer, and\ndefinitely NOT read your files. \U0001f607',
    'The original BonziBUDDY was called spyware.\nI am COMPLETELY different.\n...Please don\'t Google that.',
    'Now featuring REAL Bonzi Buddy sprites!\nExtracted from the original ACS character.\nYou\'re welcome.',
]

DODGE_LINES = [
    'hehe \U0001f60f', 'nope!', 'too slow! \U0001f602', 'almost!',
    'try again!', 'lol', 'nuh uh!', 'nice try \U0001f602',
    '404: button not found', 'hehehe', 'boop!',
    'i\'m faster!', 'keep trying \U0001f608', 'getting warmer!',
    'COLD!', 'almost... NOT', 'you thought \U0001f480', 'HA',
]

SCRIPT = [
    ('Hi there! I\'m BonziBUDDY! \U0001f44b',                             2600),
    ('Your helpful desktop companion!',                                    2400),
    ('I know EVERYTHING about your computer.',                             2600),
    ('Right-click me anytime for facts, jokes, and more!',                3000),
    ('I\'ve been scanning your PC in the background...',                  2800),
    ('And I found something VERY concerning. \U0001f631',                  2600),
    ('247 INFECTED FILES on your system!',                                2800),
    ('Don\'t worry! I can clean it all up for you!',                      2600),
    ('Just click the DELETE button below!',                               2400),
]

# ── Main BonziBUDDY window ────────────────────────────────────────────────────
def build_bonzi():
    main = tk.Toplevel()
    _bonzi_main[0] = main
    main.overrideredirect(True)
    main.attributes('-topmost', True)
    main.configure(bg=CHROMA)
    try:
        main.wm_attributes('-transparentcolor', CHROMA)
    except: pass

    sx = max(20, SW//2 - CW//2)
    sy = max(20, SH//2 - CH//2)
    main.geometry(f'{CW}x{CH}+{sx}+{sy}')

    c = tk.Canvas(main, width=CW, height=CH, bg=CHROMA, highlightthickness=0)
    c.pack()

    # ── Load real Bonzi frames and place image ────────────────────────────────
    norm_photo, blink1_photo, blink2_photo = load_bonzi_frames()
    _photo_cache['norm']   = norm_photo
    _photo_cache['blink1'] = blink1_photo
    _photo_cache['blink2'] = blink2_photo

    img_item = c.create_image(IMG_CX, IMG_CY, anchor='center', image=norm_photo)

    # Draw speech bubble on top of image
    update_bubble(c, 'Loading BonziBUDDY...')

    # ── Drag support ──────────────────────────────────────────────────────────
    drag = {'x': 0, 'y': 0, 'active': False}
    def _press(e):
        drag['x'] = e.x_root; drag['y'] = e.y_root; drag['active'] = True
    def _move(e):
        if not drag['active']: return
        dx = e.x_root - drag['x']; dy = e.y_root - drag['y']
        nx = main.winfo_x() + dx; ny = main.winfo_y() + dy
        main.geometry(f'+{nx}+{ny}')
        drag['x'] = e.x_root; drag['y'] = e.y_root
    def _release(e): drag['active'] = False

    c.bind('<Button-1>',        _press)
    c.bind('<B1-Motion>',       _move)
    c.bind('<ButtonRelease-1>', _release)

    # ── Right-click context menu ──────────────────────────────────────────────
    menu = tk.Menu(main, tearoff=0,
                   bg='#1a0033', fg='white',
                   activebackground='#5500aa', activeforeground='white',
                   font=('Segoe UI', 10))

    def do_fact():    update_bubble(c, random.choice(FACTS))
    def do_trivia():
        q, a = random.choice(TRIVIA)
        update_bubble(c, q)
        main.after(3800, lambda: update_bubble(c, a))
    def do_joke():    update_bubble(c, random.choice(JOKES))
    def do_fix():     update_bubble(c, random.choice(FIXES))
    def do_about():   update_bubble(c, random.choice(ABOUT_LINES))
    def _hide():      main.withdraw()   # type 1111 to restore

    menu.add_command(label='\U0001f4ac  Tell me a fact!',      command=do_fact)
    menu.add_command(label='❓  Ask me a question!',        command=do_trivia)
    menu.add_command(label='\U0001f602  Tell me a joke!',      command=do_joke)
    menu.add_command(label='\U0001f527  Fix my computer!',     command=do_fix)
    menu.add_separator()
    menu.add_command(label='ℹ️   About BonziBUDDY',  command=do_about)
    menu.add_separator()
    menu.add_command(label='❌  Hide  (type 1111 to restore)', command=_hide)

    def _rightclick(e):
        try: menu.tk_popup(e.x_root, e.y_root)
        finally: menu.grab_release()
    c.bind('<Button-3>', _rightclick)

    # ── Real blink animation (swap PhotoImage on canvas item) ─────────────────
    def _blink():
        if not main.winfo_exists(): return
        seq    = [blink1_photo, blink2_photo, blink1_photo, norm_photo]
        delays = [80, 80, 80, random.randint(2500, 5500)]
        def _step(i=0):
            if not main.winfo_exists(): return
            c.itemconfig(img_item, image=seq[i])
            if i < len(seq)-1:
                main.after(delays[i], lambda: _step(i+1))
            else:
                main.after(delays[i], _blink)
        _step()
    main.after(2200, _blink)

    # ── Auto-wander ───────────────────────────────────────────────────────────
    wander_on = [False]
    def _wander():
        if not main.winfo_exists() or not wander_on[0]: return
        tx = random.randint(40, max(41, SW-CW-40))
        ty = random.randint(40, max(41, SH-CH-40))
        steps = 55
        ox, oy = main.winfo_x(), main.winfo_y()
        def _step(s=0):
            if s >= steps or not main.winfo_exists() or drag['active']: return
            t = s/steps; ease = t*t*(3-2*t)
            nx = int(ox+(tx-ox)*ease); ny = int(oy+(ty-oy)*ease)
            try: main.geometry(f'+{nx}+{ny}')
            except: return
            main.after(20, lambda: _step(s+1))
        _step()
        main.after(random.randint(7000, 14000), _wander)

    # ── DELETE button ─────────────────────────────────────────────────────────
    del_btn = tk.Button(main, text='  \U0001f5d1  DELETE VIRUSES  ',
                        font=('Segoe UI', 12, 'bold'),
                        bg='#cc0044', fg='white', relief='flat',
                        activebackground='#aa0033', cursor='hand2')
    del_item = c.create_window(CW//2, CH-28, window=del_btn, anchor='center')
    c.itemconfig(del_item, state='hidden')

    dodge_count = [0]
    MAX_DODGES  = 18
    phase       = ['script']

    def _dodge(event=None):
        if phase[0] != 'dodge': return
        dodge_count[0] += 1
        if dodge_count[0] >= MAX_DODGES:
            phase[0] = 'done'
            c.coords(del_item, CW//2, CH-28)
            del_btn.config(command=_on_click, bg='#880000',
                           text='  \U0001f5d1  DELETE VIRUSES  ← NOW  ')
            update_bubble(c, '...ok fine. You win.\nClick it. I dare you. \U0001f612')
            wander_on[0] = True
            main.after(3000, _wander)
            return
        nx = random.randint(40, CW-100)
        ny = random.randint(CH-95, CH-15)
        c.coords(del_item, nx, ny)
        update_bubble(c, random.choice(DODGE_LINES))

    del_btn.bind('<Enter>',    _dodge)
    del_btn.bind('<Button-1>', lambda e: _dodge() if phase[0]=='dodge' else None)

    def _on_click():
        c.itemconfig(del_item, state='hidden')
        update_bubble(c, 'Opening BonziBUDDY File Cleaner...\nStand by! \U0001f60a')
        main.after(1400, open_file_cleaner)

    # ── Script auto-progression ───────────────────────────────────────────────
    script_idx = [0]
    def _next_line():
        if not main.winfo_exists(): return
        idx = script_idx[0]
        if idx >= len(SCRIPT):
            phase[0] = 'dodge'
            c.itemconfig(del_item, state='normal')
            update_bubble(c, '\U0001f446 Click that DELETE button!\nI\'ll clean EVERYTHING up!')
            return
        text, delay = SCRIPT[idx]
        update_bubble(c, text)
        script_idx[0] += 1
        main.after(delay, _next_line)
    main.after(900, _next_line)

# ── Entry point ───────────────────────────────────────────────────────────────
root = tk.Tk()
root.withdraw()
root.after(300, build_bonzi)
root.mainloop()
