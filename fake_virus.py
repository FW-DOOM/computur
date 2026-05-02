"""
fake_virus.py — Level 10 fake virus prank.
Looks exactly like a real ransomware/trojan attack. Entirely harmless.
Secret exit: type 4308 on keyboard at any time.
"""
import tkinter as tk
import threading, time, random, subprocess, os, sys, ctypes, ctypes.wintypes

user32   = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
SW = user32.GetSystemMetrics(0)
SH = user32.GetSystemMetrics(1)

# ── Secret exit hook ──────────────────────────────────────────────────────────
class _KHS(ctypes.Structure):
    _fields_ = [('vkCode',ctypes.c_uint32),('scanCode',ctypes.c_uint32),
                ('flags',ctypes.c_uint32),('time',ctypes.c_uint32),
                ('dwExtraInfo',ctypes.POINTER(ctypes.c_ulong))]
_HOOKP = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(_KHS))
_buf = []
def _kb(n, w, l):
    if n >= 0 and w == 0x0100:
        v = l.contents.vkCode
        if 0x30 <= v <= 0x39:
            _buf.append(chr(v))
            if len(_buf) > 4: _buf.pop(0)
            if ''.join(_buf) == '4308': os._exit(0)
    return user32.CallNextHookEx(None, n, w, l)
_kbp = _HOOKP(_kb)
def _hthread():
    user32.SetWindowsHookExW(13, _kbp, None, 0)
    m = ctypes.wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(m), None, 0, 0) != 0:
        user32.TranslateMessage(ctypes.byref(m)); user32.DispatchMessageW(ctypes.byref(m))
threading.Thread(target=_hthread, daemon=True).start()

def beep(f, d): kernel32.Beep(f, d)

# ── Fake file data ────────────────────────────────────────────────────────────
SYSTEM_FILES = [
    r'C:\Windows\System32\ntoskrnl.exe',       r'C:\Users\Documents\passwords.txt',
    r'C:\Windows\System32\drivers\tcpip.sys',   r'C:\Users\Pictures\family_photos.zip',
    r'C:\Windows\System32\lsass.exe',           r'C:\Users\Desktop\bank_details.xlsx',
    r'C:\Program Files\Google\Chrome\chrome.exe', r'C:\Users\AppData\Roaming\Discord\token.db',
    r'C:\Windows\System32\config\SAM',           r'C:\Users\Documents\resume_final.docx',
    r'C:\Windows\SysWOW64\msvcrt.dll',           r'C:\Users\Videos\private_recordings.mp4',
    r'C:\Windows\System32\winlogon.exe',         r'C:\Users\AppData\Local\Google\Passwords',
    r'C:\Program Files\Steam\userdata\config',   r'C:\Users\Documents\crypto_wallet.dat',
    r'C:\Windows\System32\kernel32.dll',         r'C:\Users\AppData\Roaming\FileZilla\sitemanager.xml',
    r'C:\Windows\System32\svchost.exe',          r'C:\Users\Documents\tax_return_2024.pdf',
    r'C:\Program Files\Discord\Discord.exe',     r'C:\Users\AppData\Local\Microsoft\Edge\Passwords',
    r'C:\Windows\System32\explorer.exe',         r'C:\Users\OneDrive\important_backup.zip',
    r'C:\Windows\System32\spoolsv.exe',          r'C:\Users\Desktop\investment_portfolio.xlsx',
]
EXTENSIONS = ['.encrypted', '.LOCKED', '.KRAKEN', '.crypt', '.darkness', '.zero']
COUNTRIES   = ['Russia','North Korea','Romania','Ukraine','Brazil','China','Iran']
C2_IPS      = ['185.220.101.47','91.108.4.0','104.244.72.0','45.142.212.100',
                '185.56.83.83','195.123.241.0','62.173.145.0','77.83.247.12']
PROCESSES   = ['system32.vbs','svhost32.exe','winsecure.dll','keylog_svc.exe',
               'netcap.bat','cryptomine.exe','rdp_backdoor.dll','stealer.py']

root = tk.Tk()
root.withdraw()

# ── Helpers ───────────────────────────────────────────────────────────────────
def toplevel(title='', x=0, y=0, w=SW, h=SH, bg='#1a0000', topmost=True):
    win = tk.Toplevel()
    win.title(title); win.configure(bg=bg); win.overrideredirect(True)
    win.geometry(f'{w}x{h}+{x}+{y}')
    if topmost: win.attributes('-topmost', True)
    return win

def label(parent, text, font=('Consolas',11), fg='#ff4444', bg=None, **kw):
    bg = bg or parent.cget('bg')
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kw)

def progressbar(parent, width=600, height=22, bg='#111', fill='#cc0000'):
    c = tk.Canvas(parent, width=width, height=height, bg=bg,
                  highlightthickness=1, highlightbackground='#440000')
    c.pack(pady=3)
    bar = c.create_rectangle(0, 0, 0, height, fill=fill, outline='')
    pct = c.create_text(width//2, height//2, text='0%', fill='white',
                        font=('Consolas', 9, 'bold'))
    return c, bar, pct, width

def animate_bar(canvas, bar, pct_item, bar_w, duration_ms=4000, color='#cc0000',
                done_cb=None, label_fmt='{p}%'):
    steps = 80
    def _step(i):
        if not canvas.winfo_exists(): return
        p = int(i / steps * 100)
        w = int(bar_w * i / steps)
        canvas.itemconfig(bar, fill=color)
        canvas.coords(bar, 0, 0, w, 99)
        canvas.itemconfig(pct_item, text=label_fmt.format(p=p))
        if i < steps:
            canvas.after(duration_ms // steps, lambda: _step(i + 1))
        elif done_cb:
            canvas.after(200, done_cb)
    _step(0)

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 1 — Windows Defender fake alert
# ══════════════════════════════════════════════════════════════════════════════
def phase1_defender_alert():
    threading.Thread(target=lambda: [beep(880,80), time.sleep(.1), beep(660,80),
                                     time.sleep(.1), beep(440,200)], daemon=True).start()
    w = toplevel(w=560, h=300, bg='#1e1e1e',
                 x=SW//2-280, y=SH//2-150)
    # Header bar (Windows Defender style)
    hdr = tk.Frame(w, bg='#d83b01', height=52); hdr.pack(fill='x'); hdr.pack_propagate(False)
    tk.Label(hdr, text='  ⚠  Windows Security  —  CRITICAL THREAT DETECTED',
             font=('Segoe UI',12,'bold'), fg='white', bg='#d83b01').pack(side='left', pady=14)
    tk.Frame(w, bg='#333333', height=1).pack(fill='x')
    body = tk.Frame(w, bg='#1e1e1e'); body.pack(fill='both', expand=True, padx=20, pady=14)
    tk.Label(body, text='Trojan:Win32/Zbot.AEK  ●  Ransomware:Win32/CryptoWall.5',
             font=('Consolas',11,'bold'), fg='#ff6633', bg='#1e1e1e').pack(anchor='w')
    tk.Label(body, text='Severity:  ████████████  SEVERE', fg='#ff2200',
             font=('Consolas',10), bg='#1e1e1e').pack(anchor='w', pady=2)
    tk.Label(body, text='Status:   Spreading through system files...', fg='#ffaa00',
             font=('Consolas',10), bg='#1e1e1e').pack(anchor='w')
    tk.Label(body, text='Action:   IMMEDIATE REMOVAL REQUIRED', fg='#ff2200',
             font=('Consolas',10,'bold'), bg='#1e1e1e').pack(anchor='w', pady=2)
    tk.Frame(body, bg='#333', height=1).pack(fill='x', pady=8)
    bf = tk.Frame(body, bg='#1e1e1e'); bf.pack(fill='x')
    tk.Button(bf, text='Remove Now', font=('Segoe UI',11,'bold'),
              bg='#d83b01', fg='white', relief='flat', padx=18, pady=8,
              command=lambda: (w.destroy(), root.after(500, phase2_scan))).pack(side='left', padx=6)
    tk.Button(bf, text='Ignore (Not Recommended)', font=('Segoe UI',10),
              bg='#333', fg='#888', relief='flat', padx=10, pady=8,
              command=lambda: (w.destroy(), root.after(500, phase2_scan))).pack(side='left', padx=6)
    # Auto-proceed after 8s
    root.after(8000, lambda: w.destroy() if w.winfo_exists() else None)
    root.after(8500, phase2_scan)

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 2 — Fake virus scan & "file encryption" starting
# ══════════════════════════════════════════════════════════════════════════════
def phase2_scan():
    w = toplevel(w=760, h=520, bg='#0d0d0d', x=SW//2-380, y=SH//2-260)
    tk.Label(w, text='⚠  MALWARE ACTIVITY DETECTED — SYSTEM COMPROMISE IN PROGRESS',
             font=('Consolas',11,'bold'), fg='#ff2200', bg='#0d0d0d').pack(pady=(14,4))
    tk.Frame(w, bg='#440000', height=2).pack(fill='x', padx=20)

    # Scrolling file list
    lf = tk.Frame(w, bg='#0d0d0d'); lf.pack(fill='both', expand=True, padx=20, pady=8)
    sb = tk.Scrollbar(lf); sb.pack(side='right', fill='y')
    lb = tk.Listbox(lf, yscrollcommand=sb.set, bg='#0d0d0d', fg='#ff4444',
                    font=('Consolas',8), selectbackground='#440000',
                    relief='flat', highlightthickness=0)
    lb.pack(side='left', fill='both', expand=True); sb.config(command=lb.yview)

    status = tk.StringVar(value='Initializing...')
    tk.Label(w, textvariable=status, font=('Consolas',9), fg='#ff8800',
             bg='#0d0d0d').pack(anchor='w', padx=20)
    c2, bar2, pct2, bw2 = progressbar(w, width=720, fill='#dd0000')

    stats_v = tk.StringVar(value='Files affected: 0  |  Data exfiltrated: 0 KB')
    tk.Label(w, textvariable=stats_v, font=('Consolas',9), fg='#ff4444',
             bg='#0d0d0d').pack(anchor='w', padx=20, pady=(0,8))

    files_done = [0]; data_kb = [0]
    flist = SYSTEM_FILES * 3; random.shuffle(flist)

    def _scan_loop():
        for fp in flist:
            if not w.winfo_exists(): return
            time.sleep(random.uniform(0.06, 0.18))
            ext = random.choice(EXTENSIONS)
            new_name = fp + ext
            color = random.choice(['#ff2200','#ff4400','#ff6600','#ffaa00'])
            kb = random.randint(12, 4096)
            data_kb[0] += kb
            files_done[0] += 1
            def _add(n=new_name, c=color, k=kb):
                if not w.winfo_exists(): return
                lb.insert('end', f'  ENCRYPTING  {n}  [{k} KB]')
                lb.itemconfig(lb.size()-1, fg=c)
                lb.yview_moveto(1.0)
                stats_v.set(f'Files affected: {files_done[0]}  |  Data exfiltrated: {data_kb[0]:,} KB')
                status.set(f'Encrypting: {n[:55]}...')
            root.after(0, _add)
        root.after(0, lambda: w.destroy() if w.winfo_exists() else None)
        root.after(500, phase3_network)

    animate_bar(c2, bar2, pct2, bw2, duration_ms=len(flist)*120,
                color='#cc0000', label_fmt='ENCRYPTING {p}%')
    threading.Thread(target=_scan_loop, daemon=True).start()
    # Spawn extra scary popups during scan
    root.after(2000, _extra_popup)
    root.after(5000, _process_popup)
    root.after(9000, _extra_popup)

def _extra_popup():
    msgs = [
        ('KEYLOGGER ACTIVE', 'Keystroke capture started.\nAll passwords being recorded.'),
        ('WEBCAM ACCESSED', 'Remote access to camera established.\nStreaming to external server.'),
        ('REGISTRY MODIFIED', r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
                              '\nPersistence mechanism installed.'),
        ('DATA EXFILTRATION', 'Uploading files to:\n185.220.101.47:8443 (TOR exit node)'),
        ('FIREWALL DISABLED', 'Windows Firewall rules cleared.\nAll ports now exposed.'),
    ]
    title, msg = random.choice(msgs)
    pw = toplevel(w=400, h=160, bg='#1a0000',
                  x=random.randint(0, SW-420), y=random.randint(0, SH-180))
    tk.Label(pw, text=f'  ⛔  {title}', font=('Consolas',11,'bold'),
             fg='#ff0000', bg='#1a0000').pack(anchor='w', pady=(10,4), padx=12)
    tk.Label(pw, text=msg, font=('Consolas',9), fg='#ff6600',
             bg='#1a0000', justify='left').pack(anchor='w', padx=16)
    pw.after(4000, lambda: pw.destroy() if pw.winfo_exists() else None)
    threading.Thread(target=lambda: (beep(1200,60), time.sleep(.08), beep(900,60)),
                     daemon=True).start()

def _process_popup():
    pw = toplevel(w=500, h=280, bg='#0a0a1a',
                  x=SW//2-250, y=random.randint(80, SH-320))
    tk.Label(pw, text='  SUSPICIOUS PROCESSES DETECTED',
             font=('Consolas',11,'bold'), fg='#aa44ff', bg='#0a0a1a').pack(anchor='w', pady=8)
    for p in random.sample(PROCESSES, 5):
        pid = random.randint(1000, 9999)
        cpu = random.randint(12, 98)
        tk.Label(pw, text=f'  PID {pid}  {p:<30}  CPU: {cpu}%  [MALICIOUS]',
                 font=('Consolas',8), fg='#ff44aa', bg='#0a0a1a').pack(anchor='w')
    tk.Label(pw, text='\n  Cannot terminate — rootkit protection active.',
             font=('Consolas',9,'bold'), fg='#ff2200', bg='#0a0a1a').pack(anchor='w')
    pw.after(5000, lambda: pw.destroy() if pw.winfo_exists() else None)

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 3 — Network exfiltration monitor
# ══════════════════════════════════════════════════════════════════════════════
def phase3_network():
    threading.Thread(target=lambda: [beep(200,150), time.sleep(.1), beep(150,200),
                                     time.sleep(.05), beep(100,400)], daemon=True).start()
    w = toplevel(w=800, h=440, bg='#000d00', x=SW//2-400, y=SH//2-220)
    tk.Label(w, text='▓ LIVE NETWORK EXFILTRATION MONITOR ▓',
             font=('Consolas',13,'bold'), fg='#00ff44', bg='#000d00').pack(pady=(12,4))
    tk.Frame(w, bg='#004400', height=1).pack(fill='x', padx=20)

    lf = tk.Frame(w, bg='#000d00'); lf.pack(fill='both', expand=True, padx=20, pady=6)
    lb = tk.Listbox(lf, bg='#000d00', fg='#00ff44', font=('Consolas',8),
                    relief='flat', highlightthickness=0)
    lb.pack(fill='both', expand=True)

    speed_v = tk.StringVar(value='Upload: 0 MB/s  |  Total sent: 0 MB')
    tk.Label(w, textvariable=speed_v, font=('Consolas',10,'bold'),
             fg='#ff4400', bg='#000d00').pack(pady=4)
    tk.Button(w, text='[CONTINUE →]', font=('Consolas',12,'bold'),
              bg='#002200', fg='#00ff44', relief='flat', padx=20, pady=8,
              command=lambda: (w.destroy(), root.after(300, phase4_ransom))).pack(pady=6)

    total_mb = [0]
    def _net_loop():
        countries = COUNTRIES * 4; random.shuffle(countries)
        for country in countries:
            if not w.winfo_exists(): return
            ip  = random.choice(C2_IPS)
            mb  = random.uniform(0.8, 8.4)
            total_mb[0] += mb
            port = random.choice([443,8443,4444,6881,1337,31337,9001])
            prot = random.choice(['TLS1.3','AES-256','RC4','RSA-2048'])
            msg  = f'  → {ip}:{port}  [{country}]  {mb:.1f} MB  [{prot}]  ✓ SENT'
            def _add(m=msg, t=total_mb[0]):
                if not w.winfo_exists(): return
                lb.insert('end', m); lb.yview_moveto(1.0)
                spd = random.uniform(1.2, 8.9)
                speed_v.set(f'Upload: {spd:.1f} MB/s  |  Total sent: {t:.1f} MB')
            root.after(0, _add)
            time.sleep(random.uniform(0.3, 0.8))
        root.after(0, lambda: w.destroy() if w.winfo_exists() else None)
        root.after(500, phase4_ransom)

    threading.Thread(target=_net_loop, daemon=True).start()

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 4 — Fullscreen ransom note with countdown
# ══════════════════════════════════════════════════════════════════════════════
def phase4_ransom():
    # Scream beep
    def _beeps():
        for f in [880,660,440,330,220,880,660,220]:
            beep(f, 80); time.sleep(0.05)
    threading.Thread(target=_beeps, daemon=True).start()

    w = toplevel(w=SW, h=SH, bg='#0a0000', x=0, y=0)
    w.attributes('-alpha', 0.97)

    # Skull header
    tk.Label(w, text='☠  YOUR FILES HAVE BEEN ENCRYPTED  ☠',
             font=('Impact', max(36, SW//28)), fg='#ff0000', bg='#0a0000').pack(pady=(60,8))
    tk.Label(w, text='All your documents, photos, databases and other important files\n'
                     'have been encrypted with military-grade AES-256 + RSA-4096 encryption.',
             font=('Consolas', 14), fg='#ff6600', bg='#0a0000', justify='center').pack(pady=8)

    tk.Frame(w, bg='#440000', height=2, width=SW//2).pack(pady=10)

    # Stats
    sf = tk.Frame(w, bg='#0a0000'); sf.pack(pady=6)
    for txt, val in [('Files encrypted:', f'{random.randint(8400, 24800):,}'),
                     ('Data affected:', f'{random.randint(40, 380)} GB'),
                     ('Origin:', random.choice(COUNTRIES)),
                     ('Malware family:', random.choice(['KRAKEN 4.0','DarkSide v3','LockBit 3.0']))]:
        rf = tk.Frame(sf, bg='#0a0000'); rf.pack(anchor='center')
        tk.Label(rf, text=f'{txt:<22}', font=('Consolas',13), fg='#888', bg='#0a0000').pack(side='left')
        tk.Label(rf, text=val, font=('Consolas',13,'bold'), fg='#ff4400', bg='#0a0000').pack(side='left')

    tk.Frame(w, bg='#440000', height=2, width=SW//2).pack(pady=10)

    # Countdown
    tk.Label(w, text='⏱  Time remaining before permanent deletion:',
             font=('Consolas',13), fg='#ff8800', bg='#0a0000').pack()
    timer_v = tk.StringVar()
    tk.Label(w, textvariable=timer_v, font=('Impact', max(52, SW//18)),
             fg='#ff0000', bg='#0a0000').pack(pady=4)

    tk.Label(w, text='Send 0.3 BTC to:  1A1zP1eP5QGefi2DMPTfTL5SLmv7Divf— wait actually...',
             font=('Consolas',11), fg='#888', bg='#0a0000').pack(pady=6)

    tk.Label(w, text='...just kidding. This is a prank. You\'re fine. 😂\n'
                     'Type 4308 to exit.',
             font=('Consolas', 12, 'bold'), fg='#44ff44', bg='#0a0000').pack(pady=20)

    # Countdown from 23:59:59
    secs = [23*3600 + 59*60 + 59]
    def _tick():
        if not w.winfo_exists(): return
        h, rem = divmod(secs[0], 3600); m, s = divmod(rem, 60)
        timer_v.set(f'{h:02d}:{m:02d}:{s:02d}')
        if secs[0] > 0:
            secs[0] -= 1
            w.after(1000, _tick)
    _tick()

    # Spam extra popups every few seconds
    def _spam():
        while True:
            time.sleep(random.uniform(3, 7))
            root.after(0, _extra_popup)
    threading.Thread(target=_spam, daemon=True).start()

    # Also do fake BSOD flash
    root.after(15000, _fake_bsod_flash)

def _fake_bsod_flash():
    """Brief BSOD flash (not permanent — flashes and fades)."""
    b = toplevel(w=SW, h=SH, bg='#0000AA', x=0, y=0)
    STOP_CODE = random.choice(['0x0000007E','0x00000050','0xC000021A','0xDEADBEEF'])
    tk.Label(b, text=':(',
             font=('Segoe UI', max(80, SW//11)), fg='white', bg='#0000AA').pack(pady=(80,10))
    tk.Label(b, text="Your PC ran into a problem and needs to restart. We're\njust collecting some error info, then we'll restart for you.",
             font=('Segoe UI', 18), fg='white', bg='#0000AA', justify='left').pack(pady=10)
    pf = tk.Frame(b, bg='#0000AA'); pf.pack(pady=20)
    pct_v = tk.StringVar(value='0% complete')
    tk.Label(pf, textvariable=pct_v, font=('Segoe UI',16), fg='white', bg='#0000AA').pack()
    tk.Label(b, text=f'Stop code: RANSOMWARE_DETECTED_{STOP_CODE}',
             font=('Consolas',13), fg='white', bg='#0000AA').pack(pady=8)

    p = [0]
    def _count():
        if not b.winfo_exists(): return
        p[0] = min(p[0]+1, 30)
        pct_v.set(f'{p[0]}% complete')
        if p[0] < 30: b.after(80, _count)
        else:
            b.after(1500, lambda: b.destroy() if b.winfo_exists() else None)
    _count()

# ══════════════════════════════════════════════════════════════════════════════
# Entry point — cascade of popups spawns immediately
# ══════════════════════════════════════════════════════════════════════════════
# Fire initial wave of extra popups simultaneously
for delay in [200, 800, 1500, 2500]:
    root.after(delay, _extra_popup)
root.after(300, _process_popup)

# Start Phase 1 after brief delay (mimics real malware "waking up")
root.after(1200, phase1_defender_alert)

root.mainloop()
