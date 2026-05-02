"""
ultimate_troll.py — THE ULTIMATE TROLLER 9000 — MAXIMUM EDITION.
EVERYTHING in ONE file:
  * REAL BonziBUDDY (sprites, animations, Bonzi-like SSML voice, poke reactions)
  * Window hijacking (shake, teleport, spin, bounce, figure-8, inflate, pinwheel...)
  * Mouse hijacking (circle, zigzag, shake, teleport)
  * Fake BSODs (rotating stop codes), fake Windows Update fullscreen
  * Beep attacks, clipboard hijack, window title chaos, window swarm
  * Classic Windows error memes (illegal operation, fatal exception, DLL hell...)
  * Fake crash reporter, fake low memory/disk warnings
  * Creepy TTS + fake search history URL overlay
  * Fake Windows dialogs, toast notifications, screen flash, rainbow flash
  * Emoji bounce windows, annoy popups (tons of error memes), app spam
  * Q&A popup (ask why this is happening → snarky answers)
  * Browser searches (funny, annoying, non-inappropriate)
  * FINAL BOSS MODE at 5 minutes — EVERYTHING AT ONCE, 3x speed
  * Secret exit: type 4308
  * Restore Bonzi: type 1111
"""
import tkinter as tk
import random, threading, time, base64, io, sys, subprocess, os, tempfile, shutil, re
import ctypes, ctypes.wintypes, math, webbrowser

# -- Auto-install Pillow -------------------------------------------------------
try:
    from PIL import Image, ImageTk
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Pillow', '-q'])
    from PIL import Image, ImageTk

user32   = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
SW_W = user32.GetSystemMetrics(0)
SW_H = user32.GetSystemMetrics(1)

try:
    from bonzi_b64 import FRAMES
    BONZI_ENABLED = True
except ImportError:
    BONZI_ENABLED = False
    FRAMES = {}

# ── Global keyboard hook — exit 4308 | restore Bonzi 1111 ────────────────────
class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [('vkCode', ctypes.c_uint32), ('scanCode', ctypes.c_uint32),
                ('flags',  ctypes.c_uint32), ('time',     ctypes.c_uint32),
                ('dwExtraInfo', ctypes.POINTER(ctypes.c_ulong))]
HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int,
                               ctypes.POINTER(KBDLLHOOKSTRUCT))
_sec_buf = []
_bonzi_main = [None]

def _kb(nCode, wParam, lParam):
    if nCode >= 0 and wParam == 0x0100:
        vk = lParam.contents.vkCode
        if 0x30 <= vk <= 0x39:
            _sec_buf.append(chr(vk))
            if len(_sec_buf) > 4: _sec_buf.pop(0)
            seq = ''.join(_sec_buf)
            if seq == '4308': os._exit(0)
            if seq == '1111':
                def _restore():
                    m = _bonzi_main[0]
                    if m is not None:
                        try:
                            if m.winfo_exists():
                                m.deiconify(); m.attributes('-topmost', True); return
                        except: pass
                    build_bonzi()
                root.after(0, _restore)
    return user32.CallNextHookEx(None, nCode, wParam, lParam)
_kbproc = HOOKPROC(_kb)
def _hook_thread():
    user32.SetWindowsHookExW(13, _kbproc, None, 0)
    msg = ctypes.wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageW(ctypes.byref(msg))
threading.Thread(target=_hook_thread, daemon=True).start()

# ── TTS — L&H TruVoice (real Bonzi) → eSpeak NG → SAPI fallback ──────────────
import winreg, urllib.request

_LH_VOICE = [False]
_LH_DL_URLS = [
    'https://archive.org/download/lernout-and-hauspie-tts-3.0/LHTTSInst.exe',
    'https://archive.org/download/lernout-hauspie-tts/LHTTSInst.exe',
    'https://archive.org/download/lh-tts-voices/LHTTSInst.exe',
    'https://archive.org/download/bonzibuddy-lhtts/LHTTSInst.exe',
]

def _check_lh():
    for key in [r'SOFTWARE\Lernout & Hauspie\TruVoice',
                r'SOFTWARE\WOW6432Node\Lernout & Hauspie\TruVoice']:
        try:
            winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key)
            _LH_VOICE[0] = True; return True
        except: pass
    return False

def _install_lh_bg():
    if _check_lh(): return
    tmp = os.path.join(tempfile.gettempdir(), 'LHTTSInst.exe')
    for url in _LH_DL_URLS:
        try:
            urllib.request.urlretrieve(url, tmp)
            if os.path.getsize(tmp) < 100_000: continue
            with open(tmp, 'rb') as f:
                if f.read(2) != b'MZ': continue  # verify real PE before running
            subprocess.run([tmp, '/S', '/SILENT', '/NORESTART'], timeout=120,
                           creationflags=subprocess.CREATE_NO_WINDOW)
            if _check_lh(): break
        except: continue
    try: os.unlink(tmp)
    except: pass

threading.Thread(target=_install_lh_bg, daemon=True).start()

def _speak_lh(text):
    safe = text.replace("'", " ").replace('"', ' ')
    ps = ("$t = New-Object -ComObject 'Speech.VoiceText'; "
          "$t.Register('BonziApp', 0); "
          "try { $vl = $t.GetVoiceList(); "
          "  for ($i=0; $i -lt $vl.Count; $i++) { "
          "    $v = $vl.Item($i); "
          "    if ($v.ModeName -match 'Adult Male.*2') { $t.Set($v, 0); break } "
          "  } } catch {}; "
          f"$t.Speak('{safe}', 0)")   # 0 = sync, no sleep needed
    subprocess.Popen(["powershell", "-WindowStyle", "Hidden", "-Command", ps],
                     creationflags=subprocess.CREATE_NO_WINDOW)

def _find_espeak():
    for p in [r'C:\Program Files\eSpeak NG\espeak-ng.exe',
              r'C:\Program Files (x86)\eSpeak NG\espeak-ng.exe']:
        if os.path.isfile(p): return p
    return shutil.which('espeak-ng')

ESPEAK_PATH = _find_espeak()

VOICE_CFG = {
    'enabled':  True,
    'engine':   'espeak',
    'es_voice': 'en+m3',   # closest to L&H Adult Male #2
    'es_pitch': 55,
    'es_speed': 200,        # Bonzi talks FAST — 200 wpm
    'es_amp':   200,        # punchy amplitude
    'rate':     1.3,        # SAPI fallback
    'pitch':    '+30%',
    'voice':    '',
}

# Pronunciation fixes so eSpeak sounds like actual Bonzi
_PRONUNC = [
    (re.compile(r'\bBonziBUDDY\b', re.I), 'Bonzee Buddy'),
    (re.compile(r'\bBonzi\b',      re.I), 'Bonzee'),
    (re.compile(r'\bPC\b'),               'P C'),
    (re.compile(r'\bCPU\b'),              'C P U'),
    (re.compile(r'\bRAM\b'),              'ram'),
    (re.compile(r'\bDLL\b'),              'D L L'),
    (re.compile(r'\bOS\b'),               'O S'),
    (re.compile(r'\bWi-?Fi\b', re.I),     'why fye'),
    (re.compile(r'\bLOL\b'),              'lol'),
    (re.compile(r'\bOMG\b'),              'oh my gosh'),
    (re.compile(r'[→←↑↓★☆•·]'),          ' '),
    (re.compile(r'[^\x00-\x7F]+'),        ''),
    (re.compile(r'  +'),                  ' '),
]

def _prep(text):
    t = text.replace('\n', ' ').replace('\r', '')
    for pat, repl in _PRONUNC:
        t = pat.sub(repl, t)
    return t.strip()

def speak(text, rate=None, pitch=None):
    if not VOICE_CFG['enabled']: return
    def _do():
        prepped = _prep(text)
        if not prepped: return
        if _LH_VOICE[0]:
            try: _speak_lh(prepped); return
            except: pass
        if VOICE_CFG['engine'] == 'espeak' and ESPEAK_PATH:
            try:
                subprocess.Popen(
                    [ESPEAK_PATH,
                     '-v', VOICE_CFG['es_voice'],
                     '-p', str(VOICE_CFG['es_pitch']),
                     '-s', str(VOICE_CFG['es_speed']),
                     '-a', str(VOICE_CFG['es_amp']),
                     '-k', '10',
                     '--punct=none',
                     prepped],
                    creationflags=subprocess.CREATE_NO_WINDOW)
                return
            except: pass
        # SAPI fallback
        r_val = VOICE_CFG['rate']  if rate  is None else rate
        p_val = VOICE_CFG['pitch'] if pitch is None else pitch
        clean = (prepped.replace('&','and').replace('<','').replace('>','')
                        .replace('"','').replace("'",''))
        vc = VOICE_CFG['voice']
        vt = f'<voice name="{vc}">' if vc else ''
        ve = '</voice>' if vc else ''
        ssml = (f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
                f'{vt}<prosody pitch="{p_val}" rate="{r_val:.2f}">{clean}</prosody>{ve}'
                f'</speak>')
        try:
            tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False, encoding='utf-8')
            tmp.write(ssml); tmp.close()
            fp = tmp.name.replace('\\', '/')
            ps = (f"Add-Type -AssemblyName System.Speech; "
                  f"$s=New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                  f"if(-not '{vc}'){{try{{$s.SelectVoiceByHints("
                  f"[System.Speech.Synthesis.VoiceGender]::Male)}}catch{{}}}}; "
                  f"$x=[System.IO.File]::ReadAllText('{fp}'); "
                  f"$s.SpeakSsml($x); "
                  f"Remove-Item '{fp}' -Force -ErrorAction SilentlyContinue")
            subprocess.Popen(["powershell", "-WindowStyle", "Hidden", "-Command", ps],
                             creationflags=subprocess.CREATE_NO_WINDOW)
        except: pass
    threading.Thread(target=_do, daemon=True).start()

# ════════════════════════════════════════════════════════════
# BONZI BUDDY
# ════════════════════════════════════════════════════════════
CHROMA = '#00fe01'; SCALE = 2.5
IMG_W = int(200*SCALE); IMG_H = int(160*SCALE)
CW, CH = 520, 580; IMG_CX = CW//2; IMG_CY = 280
_rgba_cache = {}; _photo_cache = {}

def _get_rgba(idx):
    if idx not in _rgba_cache:
        img = Image.open(io.BytesIO(base64.b64decode(FRAMES[idx]))).convert('RGBA')
        _rgba_cache[idx] = img.resize((IMG_W,IMG_H),Image.LANCZOS)
    return _rgba_cache[idx]

def _get_photo(indices):
    key = tuple(indices)
    if key not in _photo_cache:
        comp = Image.new('RGBA',(IMG_W,IMG_H),(0,0,0,0))
        for idx in indices:
            comp = Image.alpha_composite(comp, _get_rgba(idx))
        buf = io.BytesIO(); comp.save(buf,'PNG'); buf.seek(0)
        _photo_cache[key] = tk.PhotoImage(data=base64.b64encode(buf.read()).decode('ascii'))
    return _photo_cache[key]

ANIM_BLINK   = [((0,),80),((0,26),80),((0,27),120),((0,26),80),((0,),80)]
ANIM_WAVE    = [((344,),90),((345,),90),((346,),90),((347,),90),((348,),90),
                ((349,),90),((350,),90),((351,),90),((352,),90),((353,),90),
                ((354,),90),((353,),90),((352,),90),((351,),90),((350,),90),
                ((349,),90),((348,),90),((347,),90),((346,),90),((345,),90),
                ((344,),90),((0,),150)]
ANIM_GESTURE = [((28,),90),((29,),90),((30,),90),((31,),90),((32,),90),
                ((33,),200),((32,),90),((31,),90),((30,),90),((29,),90),((28,),90),((0,),90)]
ANIM_EXPLAIN = [((28,),100),((29,),100),((30,),100),((31,),100),((32,),100),
                ((33,),150),((33,),150),((33,),150),((33,),150),
                ((32,),100),((31,),100),((30,),100),((29,),100),((28,),100),((0,),100)]

def draw_bubble(c,x1,y1,x2,y2,r=12,fill='white',out='#4A0A99',lw=2,tag='bubble'):
    c.create_rectangle(x1+r,y1,x2-r,y2,fill=fill,outline='',tags=tag)
    c.create_rectangle(x1,y1+r,x2,y2-r,fill=fill,outline='',tags=tag)
    for ox,oy in[(x1,y1),(x2-2*r,y1),(x1,y2-2*r),(x2-2*r,y2-2*r)]:
        c.create_oval(ox,oy,ox+2*r,oy+2*r,fill=fill,outline=out,width=lw,tags=tag)
    c.create_line(x1+r,y1,x2-r,y1,fill=out,width=lw,tags=tag)
    c.create_line(x1+r,y2,x2-r,y2,fill=out,width=lw,tags=tag)
    c.create_line(x1,y1+r,x1,y2-r,fill=out,width=lw,tags=tag)
    c.create_line(x2,y1+r,x2,y2-r,fill=out,width=lw,tags=tag)

def update_bubble(c,text):
    c.delete('bubble')
    bx1,by1,bx2,by2=8,8,CW-8,106
    draw_bubble(c,bx1,by1,bx2,by2,tag='bubble')
    mid=CW//2
    c.create_polygon(mid-14,by2,mid+14,by2,mid,by2+26,fill='white',outline='#4A0A99',width=2,tags='bubble')
    c.create_polygon(mid-11,by2+1,mid+11,by2+1,mid,by2+24,fill='white',outline='',tags='bubble')
    c.create_text(mid,(by1+by2)//2,text=text,font=('Segoe UI',11),fill='#220044',
                  width=CW-36,anchor='center',justify='center',tags='bubble')

BONZI_FACTS  = [
    'FACT: Gorillas share 98.3% DNA with humans!\nI share 100% of your DESKTOP.',
    'FACT: BonziBUDDY launched in 1999!\nI have been in your PC for 25 years.',
    'FACT: Your PC has billions of transistors!\nI have taken control of ALL of them.',
    'FACT: Gorillas can live 50 years in captivity!\nI will live in this PC FOREVER.',
    'FACT: RAM stands for Random Access Memory!\nYours is running out. Because of me.',
]
BONZI_JOKES  = [
    'Why did the computer go to the doctor?\nIt had a VIRUS! Just like yours! \U0001f602',
    'Why was the computer late?\nIt had a hard drive! HARD DRIVE! \U0001f480',
    'What\'s a gorilla\'s favorite computer?\nA DELL-gorilla! GET IT! \U0001f98d',
    'Why don\'t computers take naps?\nThey\'re afraid of crashing!\nLike YOURS is about to. \U0001f608',
]
BONZI_CLICK  = [
    'Hey! That tickles! \U0001f98d','Watch it! I bite! \U0001f608',
    'Personal space! \U0001f62e','Nice click. Try again. \U0001f602',
    'I am NOT a button. \U0001f610','I\'m busy scanning your files. \U0001f440',
    'Do that again and I\'ll crash your PC. \U0001f60f',
    '\U0001f98d BONZI!','Ow! That was my arm!',
    'Did you really just click me? \U0001f612',
    'I felt that in my hard drive.','STOP POKING ME \U0001f621',
]
BONZI_IDLE   = [
    'Psst... I can see your screen. \U0001f440','Still here! \U0001f98d',
    'Scanning... \U0001f50d','*gorilla noises*',
    'Have you backed up lately? \U0001f914',
    'Your RAM usage looks... suspicious.',
    'Boo. \U0001f47b','Did you know I never sleep? \U0001f634',
    'I found something in your temp folder. \U0001f4c1',
    'Error 404: your privacy. Not found.',
    'I can hear your fan from here.',
    'Nice wallpaper. Very... revealing. \U0001f440',
    'Your task manager is afraid of me. \U0001f60f',
    'I forwarded your emails. You\'re welcome.',
]
BONZI_DODGE  = [
    'hehe \U0001f60f','nope!','too slow! \U0001f602','almost!','try again!',
    'lol','nuh uh!','nice try \U0001f602','404: button not found','hehehe',
    'boop!','i\'m faster!','keep trying \U0001f608','COLD!','you thought \U0001f480','HA',
]
BONZI_SCRIPT = [
    ('Hi there! I\'m BonziBUDDY! \U0001f44b',            2600,'wave'),
    ('Your helpful desktop companion!',                   2400,'gesture'),
    ('I know EVERYTHING about your computer.',            2600,'gesture'),
    ('Right-click me for facts, jokes, and more!',        3000,'gesture'),
    ('I\'ve been scanning your PC...',                    2800,'gesture'),
    ('And I found something VERY concerning. \U0001f631', 2600,'gesture'),
    ('247 INFECTED FILES on your system!',                2800,'gesture'),
    ('Don\'t worry! I can clean it all up for you!',      2600,'gesture'),
    ('Just click the DELETE button below!',               2400,'gesture'),
]
FAKE_FILES = [
    r'C:\Windows\System32\svchost.exe',r'C:\Users\AppData\Local\Temp\~DF3A12.tmp',
    r'C:\Users\Documents\passwords_backup.txt',r'C:\Program Files\Google\Chrome\chrome.exe',
    r'C:\Windows\explorer.exe',r'C:\Windows\System32\lsass.exe',
    r'C:\Users\Desktop\bank_info.xlsx',r'C:\Program Files\Discord\Discord.exe',
    r'C:\Windows\System32\ntoskrnl.exe',r'C:\Windows\System32\config\SAM',
    r'C:\Users\AppData\Local\Google\Chrome\User Data\Default\Login Data',
    r'C:\Windows\System32\kernel32.dll',r'C:\Users\AppData\Roaming\Discord\tokens.sqlite',
    r'C:\Program Files\Steam\steam.exe',r'C:\Users\Documents\homework_final.docx',
]
FAKE_STATUSES = ['INFECTED ☠','CRITICAL ⛔','COMPROMISED ⚠',
                 'THREAT FOUND \U0001f534','SCANNING...','SUSPICIOUS ⚠']

def show_got_you():
    def _make():
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True)
        w.geometry(f'{SW_W}x{SW_H}+0+0'); w.configure(bg='#009900')
        f=tk.Frame(w,bg='#009900'); f.place(relx=.5,rely=.44,anchor='center')
        tk.Label(f,text='I GOT YOU!! \U0001f602\U0001f602\U0001f602',
                 font=('Impact',max(50,SW_W//16),'bold'),fg='white',bg='#009900').pack()
        tk.Label(f,text='it was BonziBUDDY the whole time lmaoooo',
                 font=('Arial',22),fg='#ccffcc',bg='#009900').pack(pady=8)
        tk.Button(f,text='ok fine \U0001f62d',command=w.destroy,
                  font=('Arial',18),bg='#007700',fg='white',relief='flat',padx=22,pady=10).pack(pady=28)
    root.after(0,_make)

def open_file_cleaner():
    cw=tk.Toplevel(); cw.title('BonziBUDDY File Cleaner 3.0')
    cw.geometry(f'700x530+{SW_W//2-350}+{SW_H//2-265}')
    cw.configure(bg='#0a001a'); cw.resizable(False,False); cw.attributes('-topmost',True)
    hdr=tk.Frame(cw,bg='#5500aa',height=50); hdr.pack(fill='x'); hdr.pack_propagate(False)
    tk.Label(hdr,text='  \U0001f98d  BonziBUDDY File Cleaner 3.0  --  Deep Scan',
             font=('Segoe UI',12,'bold'),bg='#5500aa',fg='white').pack(side='left',pady=10)
    sv=tk.StringVar(value='Initializing deep scan...')
    tk.Label(cw,textvariable=sv,font=('Consolas',9),bg='#0a001a',fg='#cc88ff').pack(anchor='w',padx=12,pady=(6,2))
    lf=tk.Frame(cw,bg='#0a001a'); lf.pack(fill='both',expand=True,padx=12,pady=4)
    sb2=tk.Scrollbar(lf); sb2.pack(side='right',fill='y')
    fl=tk.Listbox(lf,yscrollcommand=sb2.set,bg='#0d0020',fg='#ff88cc',
                  font=('Consolas',8),selectbackground='#5500aa',
                  relief='flat',highlightthickness=1,highlightbackground='#5500aa')
    fl.pack(side='left',fill='both',expand=True); sb2.config(command=fl.yview)
    pf=tk.Frame(cw,bg='#0a001a'); pf.pack(fill='x',padx=12,pady=4)
    tk.Label(pf,text='SCAN PROGRESS:',font=('Consolas',9),bg='#0a001a',fg='#cc88ff').pack(anchor='w')
    pc=tk.Canvas(pf,width=676,height=22,bg='#1a0033',
                 highlightthickness=1,highlightbackground='#5500aa'); pc.pack()
    cv=tk.StringVar(value='Files scanned: 0  |  Threats: 0')
    tk.Label(cw,textvariable=cv,font=('Consolas',9),bg='#0a001a',fg='#ff6699').pack(anchor='w',padx=12)
    bf=tk.Frame(cw,bg='#0a001a'); bf.pack(pady=8)
    cb=tk.Button(bf,text='\U0001f5d1  CONFIRM -- DELETE ALL THREATS',
                 font=('Segoe UI',13,'bold'),bg='#aa0055',fg='white',relief='flat',padx=18,pady=10)
    cb.pack(); cb.pack_forget()
    def on_confirm():
        cb.config(state='disabled',text='Deleting files...')
        sv.set('Removing all infected files...')
        cw.after(1400,show_got_you)
    cb.config(command=on_confirm)
    def _scan():
        random.shuffle(FAKE_FILES); t=[0]
        for i,fp in enumerate(FAKE_FILES):
            if not cw.winfo_exists(): return
            time.sleep(random.uniform(.07,.20))
            st=random.choice(FAKE_STATUSES)
            if 'SCANNING' not in st: t[0]+=1
            d=f'{fp:<55}  {st}'
            def _add(d=d,t2=t[0],idx=i+1):
                if not cw.winfo_exists(): return
                fl.insert('end',d); fl.yview_moveto(1.0)
                row=fl.size()-1
                if 'INFECTED' in d or 'CRITICAL' in d: fl.itemconfig(row,fg='#ff4444')
                elif 'COMPROMISED' in d or 'THREAT' in d: fl.itemconfig(row,fg='#ff8800')
                else: fl.itemconfig(row,fg='#cc88ff')
                pct=int(idx/len(FAKE_FILES)*100); wf=int(676*pct/100)
                pc.delete('all'); pc.create_rectangle(0,0,wf,22,fill='#aa00cc',outline='')
                pc.create_text(338,11,text=f'{pct}%  ({idx}/{len(FAKE_FILES)} files)',
                               fill='white',font=('Consolas',8))
                cv.set(f'Files scanned: {idx}  |  Threats found: {t2}')
                sv.set(f'Scanning: {d[:52]}...')
            root.after(0,_add)
        def _done():
            if not cw.winfo_exists(): return
            sv.set(f'⛔  SCAN COMPLETE -- {t[0]} CRITICAL THREATS FOUND!')
            pc.delete('all'); pc.create_rectangle(0,0,676,22,fill='#ff0055',outline='')
            pc.create_text(338,11,text=f'COMPLETE -- {t[0]} THREATS -- DELETE NOW',
                           fill='white',font=('Consolas',8,'bold'))
            cv.set(f'Scanned: {len(FAKE_FILES)}  |  Threats: {t[0]} CRITICAL ⛔')
            cb.pack()
        root.after(0,_done)
    threading.Thread(target=_scan,daemon=True).start()

def build_bonzi():
    if not BONZI_ENABLED: return
    main=tk.Toplevel(); _bonzi_main[0]=main
    main.overrideredirect(True); main.attributes('-topmost',True); main.configure(bg=CHROMA)
    try: main.wm_attributes('-transparentcolor',CHROMA)
    except: pass
    main.geometry(f'{CW}x{CH}+{max(20,SW_W//2-CW//2)}+{max(20,SW_H//2-CH//2)}')
    c=tk.Canvas(main,width=CW,height=CH,bg=CHROMA,highlightthickness=0); c.pack()
    # Blue gradient background (drawn first so it sits behind Bonzi)
    _x1,_y1,_x2,_y2 = 14,84,CW-14,CH-90
    for _i in range(30):
        _t=_i/29; _r=int(0x4D*(1-_t)+0x0F*_t); _g=int(0x8F*(1-_t)+0x3D*_t); _b=int(0xE0*(1-_t)+0x8C*_t)
        c.create_rectangle(_x1,_y1+int((_y2-_y1)*_i/30),_x2,_y1+int((_y2-_y1)*(_i+1)/30)+1,
                           fill=f'#{_r:02x}{_g:02x}{_b:02x}',outline='',tags='bonzi_bg')
    c.create_rectangle(_x1,_y1,_x2,_y1+3,fill='#88BBFF',outline='',tags='bonzi_bg')
    c.create_rectangle(_x1,_y1,_x2,_y2,fill='',outline='#0A2A6E',width=2,tags='bonzi_bg')
    img_item=c.create_image(IMG_CX,IMG_CY,anchor='center',image=_get_photo((0,)))
    # Canvas vine swing helpers
    _VP_X2=IMG_CX; _VP_Y2=60; _VL2=IMG_CY-_VP_Y2; _θI2=math.radians(74)
    _bx02=_VP_X2+_VL2*math.sin(_θI2); _by02=_VP_Y2+_VL2*math.cos(_θI2)
    c.coords(img_item,int(_bx02),int(_by02))  # start off-screen right
    def _dvine(bx,by,tag='vine'):
        c.delete(tag)
        c.create_line(_VP_X2,_VP_Y2,bx,by,fill='#2D5A1B',width=9,capstyle=tk.ROUND,tags=tag)
        c.create_line(_VP_X2,_VP_Y2,bx,by,fill='#5FA832',width=4,capstyle=tk.ROUND,tags=tag)
        c.tag_raise(tag,'bonzi_bg'); c.tag_lower(tag,img_item)
    def _canvas_swing_in2(done_cb=None):
        fr=58
        def _si(i):
            if not main.winfo_exists(): return
            if i>=fr:
                c.coords(img_item,IMG_CX,IMG_CY); _dvine(IMG_CX,IMG_CY)
                main.after(500,lambda:c.delete('vine') if main.winfo_exists() else None)
                if done_cb: main.after(600,done_cb); return
            t=i/fr; θ=_θI2*math.exp(-t*2.6)*math.cos(math.pi*t*1.15)
            bx=_VP_X2+_VL2*math.sin(θ); by=_VP_Y2+_VL2*math.cos(θ)
            c.coords(img_item,int(bx),int(by)); _dvine(int(bx),int(by))
            main.after(15,lambda:_si(i+1))
        _dvine(int(_bx02),int(_by02)); _si(0)
    def _canvas_swing_out2(done_cb=None):
        xy=c.coords(img_item); cx0=xy[0]; cy0=xy[1]; pvx=cx0; pvy=_VP_Y2; vl=cy0-pvy; fr=38
        def _so(i):
            if not main.winfo_exists(): return
            if i>=fr: c.delete('vine'); main.withdraw()
            if done_cb and i>=fr: root.after(0,done_cb); return
            t=i/fr; θ=-math.radians(88)*(t**1.35)
            bx=pvx+vl*math.sin(θ); by=pvy+vl*math.cos(θ)
            c.coords(img_item,int(bx),int(by)); _dvine(int(bx),int(by))
            main.after(13,lambda:_so(i+1))
        _so(0)

    _anim={'seq':None,'idx':0,'loop':False,'done':None,'aid':None}
    def _play(seq,loop=False,done=None):
        if _anim['aid']:
            try: main.after_cancel(_anim['aid'])
            except: pass
        _anim.update(seq=seq,idx=0,loop=loop,done=done); _tick()
    def _tick():
        if not main.winfo_exists(): return
        seq=_anim['seq']
        if not seq: return
        idx=_anim['idx']
        if idx>=len(seq):
            if _anim['loop']: _anim['idx']=0; _tick(); return
            cb=_anim['done']; _anim['seq']=None
            if cb: root.after(0,cb)
            else: _start_idle()
            return
        imgs,delay=seq[idx]
        c.itemconfig(img_item,image=_get_photo(imgs))
        _anim['idx']+=1; _anim['aid']=main.after(delay,_tick)
    def _start_idle():
        if not main.winfo_exists(): return
        c.itemconfig(img_item,image=_get_photo((0,)))
        _anim['aid']=main.after(random.randint(5000,9000),_do_idle)
    def _do_idle():
        if not main.winfo_exists(): return
        r=random.random()
        if r<0.55: _play(ANIM_BLINK,done=_start_idle)
        elif r<0.78: _play(ANIM_GESTURE,done=_start_idle)
        else: _play(ANIM_WAVE,done=_start_idle)
    def _sched_idle_quote():
        if not main.winfo_exists(): return
        main.after(random.randint(25000,55000),_do_idle_quote)
    def _do_idle_quote():
        if not main.winfo_exists(): return
        msg=random.choice(BONZI_IDLE); update_bubble(c,msg); speak(msg)
        _play(ANIM_GESTURE,done=lambda:(_start_idle(),_sched_idle_quote()))
    main.after(500,_start_idle); main.after(28000,_do_idle_quote)

    drag={'x':0,'y':0,'on':False,'moved':False}
    def _press(e): drag.update(x=e.x_root,y=e.y_root,on=True,moved=False)
    def _move(e):
        if not drag['on']: return
        if abs(e.x_root-drag['x'])>5 or abs(e.y_root-drag['y'])>5: drag['moved']=True
        main.geometry(f'+{main.winfo_x()+e.x_root-drag["x"]}+{main.winfo_y()+e.y_root-drag["y"]}')
        drag['x']=e.x_root; drag['y']=e.y_root
    def _rel(e):
        drag['on']=False
        if not drag['moved']:
            msg=random.choice(BONZI_CLICK); update_bubble(c,msg); speak(msg)
            r=random.random()
            if r<0.4: _play(ANIM_BLINK,done=_start_idle)
            elif r<0.75: _play(ANIM_GESTURE,done=_start_idle)
            else: _play(ANIM_WAVE,done=_start_idle)
    c.bind('<Button-1>',_press); c.bind('<B1-Motion>',_move); c.bind('<ButtonRelease-1>',_rel)

    menu=tk.Menu(main,tearoff=0,bg='#1a0033',fg='white',
                 activebackground='#5500aa',activeforeground='white',font=('Segoe UI',10))
    def do_fact(): update_bubble(c,random.choice(BONZI_FACTS)); _play(ANIM_GESTURE,done=_start_idle)
    def do_joke(): update_bubble(c,random.choice(BONZI_JOKES)); _play(ANIM_WAVE,done=_start_idle)
    def do_scan():
        update_bubble(c,'Opening BonziBUDDY File Cleaner...\nStand by! \U0001f60a')
        main.after(800,open_file_cleaner)
    def _hide():
        speak('See ya!'); _canvas_swing_out2()
    menu.add_command(label='\U0001f4ac  Tell me a fact!', command=do_fact)
    menu.add_command(label='\U0001f602  Tell me a joke!', command=do_joke)
    menu.add_command(label='\U0001f44b  Wave!',
                     command=lambda:(update_bubble(c,'HEYYYY!! \U0001f44b\U0001f98d'),
                                     speak('Hey hey hey!'),_play(ANIM_WAVE,done=_start_idle)))
    menu.add_separator()
    menu.add_command(label='\U0001f4c1  Scan my PC...',  command=do_scan)
    menu.add_command(label='❓  Ask me why...',           command=ask_me_why_dialog)
    menu.add_separator()
    menu.add_command(label='❌  Hide  (type 1111 to restore)', command=_hide)
    def _rc(e):
        try: menu.tk_popup(e.x_root,e.y_root)
        finally: menu.grab_release()
    c.bind('<Button-3>',_rc)

    del_btn=tk.Button(main,text='  \U0001f5d1  DELETE VIRUSES  ',
                      font=('Segoe UI',12,'bold'),bg='#cc0044',fg='white',
                      relief='flat',activebackground='#aa0033',cursor='hand2')
    del_item=c.create_window(CW//2,CH-30,window=del_btn,anchor='center')
    c.itemconfig(del_item,state='hidden')
    dodge_count=[0]; MAX_DODGES=18; phase=['script']
    def _dodge(event=None):
        if phase[0]!='dodge': return
        dodge_count[0]+=1
        if dodge_count[0]>=MAX_DODGES:
            phase[0]='done'; c.coords(del_item,CW//2,CH-30)
            del_btn.config(command=_on_click,bg='#880000',text='  \U0001f5d1  DELETE VIRUSES  <- NOW  ')
            update_bubble(c,'...ok fine. You win.\nClick it. I dare you. \U0001f612')
            _play(ANIM_EXPLAIN,done=_start_idle); return
        c.coords(del_item,random.randint(40,CW-100),random.randint(CH-95,CH-15))
        update_bubble(c,random.choice(BONZI_DODGE)); _play(ANIM_BLINK,done=_start_idle)
    del_btn.bind('<Enter>',_dodge)
    del_btn.bind('<Button-1>',lambda e:_dodge() if phase[0]=='dodge' else None)
    def _on_click():
        c.itemconfig(del_item,state='hidden')
        update_bubble(c,'Opening BonziBUDDY File Cleaner...\nStand by! \U0001f60a')
        main.after(1400,open_file_cleaner)

    script_idx=[0]
    def _next_line():
        if not main.winfo_exists(): return
        idx=script_idx[0]
        if idx>=len(BONZI_SCRIPT):
            phase[0]='dodge'; c.itemconfig(del_item,state='normal')
            update_bubble(c,'\U0001f446 Click that DELETE button!\nI\'ll clean EVERYTHING up!')
            speak('Click that DELETE button! I will clean everything up!'); _play(ANIM_WAVE,done=_start_idle); return
        text,delay,hint=BONZI_SCRIPT[idx]
        update_bubble(c,text); speak(text); script_idx[0]+=1
        seq=ANIM_WAVE if hint=='wave' else ANIM_GESTURE
        _play(seq,done=lambda:main.after(max(0,delay-len(seq)*90),_next_line) if main.winfo_exists() else None)
    main.after(200, lambda: _canvas_swing_in2(done_cb=_next_line))

# ════════════════════════════════════════════════════════════
# CHAOS ENGINE
# ════════════════════════════════════════════════════════════

# ── Window enumeration ────────────────────────────────────────────────────────
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.wintypes.HWND,ctypes.wintypes.LPARAM)
SKIP=['program manager','task switching','windows input','microsoft text input',
      'default ime','msctfime ui','window message pump','task manager',
      'computur','python','shell_traywnd','button']

def get_windows():
    wins=[]
    def _cb(hwnd,_):
        if not user32.IsWindowVisible(hwnd): return True
        n=user32.GetWindowTextLengthW(hwnd)
        if n==0: return True
        buf=ctypes.create_unicode_buffer(n+1); user32.GetWindowTextW(hwnd,buf,n+1)
        if any(s in buf.value.lower() for s in SKIP): return True
        r=ctypes.wintypes.RECT(); user32.GetWindowRect(hwnd,ctypes.byref(r))
        if (r.right-r.left)>120 and (r.bottom-r.top)>80: wins.append(hwnd)
        return True
    user32.EnumWindows(WNDENUMPROC(_cb),0); return wins

def get_rect(hwnd):
    r=ctypes.wintypes.RECT(); user32.GetWindowRect(hwnd,ctypes.byref(r))
    return r.left,r.top,r.right-r.left,r.bottom-r.top

def shake(hwnd):
    ox,oy,w,h=get_rect(hwnd)
    for _ in range(20): user32.MoveWindow(hwnd,ox+random.randint(-45,45),oy+random.randint(-35,35),w,h,True); time.sleep(0.025)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)
def mega_shake(hwnd):
    ox,oy,w,h=get_rect(hwnd)
    for _ in range(40): user32.MoveWindow(hwnd,ox+random.randint(-110,110),oy+random.randint(-80,80),w,h,True); time.sleep(0.018)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)
def teleport(hwnd):
    _,_,w,h=get_rect(hwnd)
    user32.MoveWindow(hwnd,random.randint(0,max(0,SW_W-w)),random.randint(30,max(30,SW_H-h)),w,h,True)
def rapid_teleport(hwnd):
    for _ in range(8): teleport(hwnd); time.sleep(0.14)
def minimize_pop(hwnd):
    user32.ShowWindow(hwnd,6); time.sleep(random.uniform(0.4,1.0)); user32.ShowWindow(hwnd,9)
def resize_huge(hwnd):
    ox,oy,w,h=get_rect(hwnd); user32.MoveWindow(hwnd,0,30,SW_W,SW_H-30,True); time.sleep(1.0); user32.MoveWindow(hwnd,ox,oy,w,h,True)
def spin_fake(hwnd):
    ox,oy,w,h=get_rect(hwnd); cx=ox+w//2; cy=oy+h//2
    for i in range(32):
        a=(i/32)*2*math.pi; user32.MoveWindow(hwnd,int(cx+math.cos(a)*180)-w//2,int(cy+math.sin(a)*130)-h//2,w,h,True); time.sleep(0.030)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)
def yoyo(hwnd):
    ox,oy,w,h=get_rect(hwnd)
    for _ in range(14): user32.MoveWindow(hwnd,ox,random.randint(max(0,oy-200),min(SW_H-h,oy+200)),w,h,True); time.sleep(0.06)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)
def flip_stretch(hwnd):
    ox,oy,w,h=get_rect(hwnd)
    for nw,nh in [(w*2,h//2),(w//2,h*2),(w*3,h//3),(w,h)]: user32.MoveWindow(hwnd,ox,oy,max(80,nw),max(60,nh),True); time.sleep(0.10)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)
def send_to_corner(hwnd):
    _,_,w,h=get_rect(hwnd); cx,cy=random.choice([(0,0),(SW_W-w,0),(0,SW_H-h),(SW_W-w,SW_H-h)])
    user32.MoveWindow(hwnd,cx,cy,w,h,True); time.sleep(0.8)
def shrink_to_nothing(hwnd):
    ox,oy,w,h=get_rect(hwnd)
    for s in [0.70,0.45,0.25,0.12,0.05]:
        user32.MoveWindow(hwnd,ox+int(w*(1-s)/2),oy+int(h*(1-s)/2),max(40,int(w*s)),max(30,int(h*s)),True); time.sleep(0.055)
    time.sleep(0.35); user32.MoveWindow(hwnd,ox,oy,w,h,True)
def pinwheel(hwnd):
    _,_,w,h=get_rect(hwnd); cx=SW_W//2-w//2; cy=SW_H//2-h//2
    for i in range(36):
        a=(i/36)*2*math.pi; user32.MoveWindow(hwnd,max(0,int(cx+math.cos(a)*(SW_W//3))),max(0,int(cy+math.sin(a)*(SW_H//3))),w,h,True); time.sleep(0.026)
def figure_eight(hwnd):
    _,_,w,h=get_rect(hwnd); cx=SW_W//2-w//2; cy=SW_H//2-h//2
    for i in range(48):
        t=(i/48)*2*math.pi; user32.MoveWindow(hwnd,max(0,int(cx+math.sin(t)*SW_W//4)),max(0,int(cy+math.sin(2*t)*SW_H//6)),w,h,True); time.sleep(0.022)
def inflate_deflate(hwnd):
    ox,oy,w,h=get_rect(hwnd)
    for scale in [1.3,1.6,1.9,1.6,1.3,1.1,0.9,0.7,0.9,1.1,1.0]:
        nw=max(80,int(w*scale)); nh=max(60,int(h*scale)); cx=ox+w//2; cy=oy+h//2
        user32.MoveWindow(hwnd,cx-nw//2,cy-nh//2,nw,nh,True); time.sleep(0.08)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)
def window_bounce(hwnd):
    _,_,w,h=get_rect(hwnd); x=random.randint(0,SW_W-w); y=random.randint(30,SW_H-h)
    dx=random.choice([-1,1])*random.randint(12,22); dy=random.choice([-1,1])*random.randint(8,18)
    for _ in range(60):
        x+=dx; y+=dy
        if x<0 or x>SW_W-w: dx*=-1; x=max(0,min(SW_W-w,x))
        if y<30 or y>SW_H-h: dy*=-1; y=max(30,min(SW_H-h,y))
        user32.MoveWindow(hwnd,x,y,w,h,True); time.sleep(0.016)
def cascade_all():
    for i,hwnd in enumerate(get_windows()[:12]):
        try: _,_,w,h=get_rect(hwnd); user32.MoveWindow(hwnd,24*i,24*i+28,w,h,True)
        except: pass
def swap_two(h1,h2):
    x1,y1,w1,h1r=get_rect(h1); x2,y2,w2,h2r=get_rect(h2)
    user32.MoveWindow(h1,x2,y2,w1,h1r,True); user32.MoveWindow(h2,x1,y1,w2,h2r,True)
def all_minimize_restore():
    wins=get_windows()
    for hwnd in wins:
        try: user32.ShowWindow(hwnd,6)
        except: pass
    time.sleep(1.6)
    for hwnd in wins:
        try: user32.ShowWindow(hwnd,9)
        except: pass

SINGLE_ACTIONS=[shake,shake,shake,mega_shake,mega_shake,
                teleport,teleport,teleport,rapid_teleport,minimize_pop,
                resize_huge,spin_fake,yoyo,yoyo,flip_stretch,send_to_corner,
                shrink_to_nothing,pinwheel,figure_eight,inflate_deflate,window_bounce]

# ── TTS lines ─────────────────────────────────────────────────────────────────
TTS_LINES=[
    "I am inside your computer.","You cannot escape.","Hello. I live here now.",
    "Your windows belong to me.","Why are you running?","I can see everything.",
    "Do not turn off your computer.","Help. I am trapped inside.","Mwahahahahaha.",
    "You thought you were safe.","I know what you did.","Nice wallpaper by the way.",
    "I see you.","They are coming for you.","Something is very wrong.",
    "You should close this.","But you won't.","I have your files.",
    "Your passwords are mine.","Interesting search history.",
    "Have you said hello to your webcam today?",
    "I found something in your downloads folder.",
    "You really should have used private browsing.","This is not a drill.",
    "Your antivirus is sleeping.","Deleting system files. Just kidding. Or am I.",
    "Your task manager is afraid of me.",
    "I have sent your browser history to your contacts.",
    "Forty seven threats. Forty seven.",
    "I can hear your fan spinning faster right now.",
    "Windows XP is calling. It wants you back.",
    "Your CPU is crying.","I found your secret folder.",
    "Three new friends have joined your local network.",
    "I have upgraded your chaos to maximum.",
    "Please do not read this message.",
    "Your recycle bin is full of regrets.",
    "I replaced all your desktop icons with Bonzi.",
    "I forwarded your emails. You are welcome.",
    "System32 called. It said goodbye.",
    "Bonzi Buddy says hello. And goodbye to your RAM.",
    "Your clipboard now belongs to me.",
    "I renamed your windows. You will figure it out.",
    "Have you met the new files I put in your downloads? Interesting ones.",
]

FAKE_SEARCH_URLS=[
    "google.com/search?q=how+to+delete+someone+from+your+life",
    "google.com/search?q=is+it+normal+to+talk+to+your+computer",
    "google.com/search?q=can+bonzi+buddy+see+me+right+now",
    "bing.com/search?q=how+to+stop+being+embarrassed+at+age+23",
    "youtube.com/watch?v=dQw4w9WgXcQ+%28watched+47+times%29",
    "google.com/search?q=why+does+everyone+leave+me+except+bonzibuddy",
    "google.com/search?q=accidentally+googled+something+embarrassing",
    "google.com/search?q=is+my+webcam+on+when+the+light+is+off",
    "google.com/search?q=how+do+i+know+if+my+pc+loves+me",
]

FUNNY_SEARCHES=[
    "https://www.google.com/search?q=why+is+my+computer+running+so+slow",
    "https://www.google.com/search?q=how+to+get+rid+of+bonzi+buddy",
    "https://www.google.com/search?q=bonzi+buddy+is+he+still+alive",
    "https://www.google.com/search?q=is+it+too+late+to+delete+system32",
    "https://www.google.com/search?q=free+virus+removal+my+computer+is+possessed",
    "https://www.google.com/search?q=how+to+reason+with+a+gorilla",
    "https://www.google.com/search?q=can+bonzibuddy+hear+me+breathing",
    "https://www.google.com/search?q=my+cursor+moves+by+itself+am+i+hacked",
    "https://www.google.com/search?q=ctrl+z+but+for+my+decisions",
    "https://www.google.com/search?q=windows+defender+vs+vibes",
    "https://www.google.com/search?q=why+does+my+task+manager+have+trust+issues",
    "https://www.google.com/search?q=can+i+sue+my+own+computer",
]

def show_search_url_overlay():
    url=random.choice(FAKE_SEARCH_URLS)
    def _make():
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True)
        nw=min(SW_W-40,720); nh=52; w.geometry(f'{nw}x{nh}+{(SW_W-nw)//2}+{SW_H-130}'); w.configure(bg='#0d0d1a')
        f=tk.Frame(w,bg='#16213e',padx=12,pady=8); f.pack(fill='both',expand=True,padx=2,pady=2)
        tk.Label(f,text='🔍  RECENTLY VISITED:',font=('Consolas',8,'bold'),fg='#ff8800',bg='#16213e').pack(side='left')
        tk.Label(f,text=f'  {url}',font=('Consolas',10,'bold'),fg='#00d4ff',bg='#16213e').pack(side='left')
        w.attributes('-alpha',0.0)
        def _fi(a=0.0):
            if not w.winfo_exists(): return
            a=min(a+0.13,0.96); w.attributes('-alpha',a)
            if a<0.96: w.after(25,lambda:_fi(a))
            else: w.after(4800,_fo)
        def _fo(a=0.96):
            if not w.winfo_exists(): return
            a=max(a-0.09,0.0)
            try: w.attributes('-alpha',a)
            except: pass
            if a>0: w.after(35,lambda:_fo(a))
            else:
                try: w.destroy()
                except: pass
        w.after(0,_fi)
    root.after(0,_make)

def speak_with_overlay(text):
    speak(text)
    if 'search history' in text.lower(): root.after(800,show_search_url_overlay)

def open_browser_search():
    try: threading.Thread(target=lambda:webbrowser.open(random.choice(FUNNY_SEARCHES)),daemon=True).start()
    except: pass

# ── Q&A ───────────────────────────────────────────────────────────────────────
QA_RESPONSES={
    ('why','what','reason','how','explain'):["Because your PC deserved it.","The universe chose YOU. Congrats.","Why NOT? Give me one good reason to stop.","Error 404: Explanation not found.","I read your browser history. That's why."],
    ('stop','quit','end','close','exit','please'):["Hmm. No.","Interesting suggestion. Denied.","I'll stop when I feel like it. So... never.","Error: stop.exe not found.","Let me check my schedule... Nope. Chaos all day."],
    ('who','you','bonzi','gorilla'):["I am BonziBUDDY. Your eternal desktop companion.","I am the gorilla. The myth. The legend. The chaos.","Just a helpful purple ape living rent-free in your PC."],
    ('help','save','scared'):["Help is on the way! Just kidding. No it isn't.","Scared? Good. That means it's working.","Have you tried turning off your computer? Don't."],
    ('virus','hack','malware','spyware'):["I am NOT a virus. I am a COMPANION.","The FTC called me spyware once. We don't talk about that.","I prefer the term uninvited performance artist."],
}
QA_DEFAULT=["That is a very stupid question. I love it.","Interesting. Wrong. But interesting.",
            "I have processed your query. I have chosen to ignore it.","My response is: no.",
            "Error: answer.exe stopped responding.","I consulted my globe. It says: no comment."]

def get_qa_response(txt):
    txt=txt.lower()
    for keys,responses in QA_RESPONSES.items():
        if any(k in txt for k in keys): return random.choice(responses)
    return random.choice(QA_DEFAULT)

def ask_me_why_dialog():
    def _make():
        w=tk.Toplevel(); w.title('BonziBUDDY Q&A Hotline')
        w.attributes('-topmost',True); w.resizable(False,False); w.configure(bg='#0d0020')
        nw,nh=480,260; w.geometry(f'{nw}x{nh}+{(SW_W-nw)//2}+{(SW_H-nh)//2}')
        tk.Label(w,text='\U0001f98d  BonziBUDDY Q&A HOTLINE',font=('Segoe UI',13,'bold'),fg='#cc88ff',bg='#0d0020').pack(pady=(16,4))
        tk.Label(w,text='Ask me ANYTHING. I will give you a completely truthful answer.',font=('Segoe UI',9),fg='#9966ff',bg='#0d0020').pack()
        ev=tk.StringVar(); ef=tk.Frame(w,bg='#0d0020'); ef.pack(pady=12,padx=20,fill='x')
        tk.Label(ef,text='Your question:',font=('Segoe UI',10),fg='#cc88ff',bg='#0d0020').pack(anchor='w')
        entry=tk.Entry(ef,textvariable=ev,font=('Segoe UI',11),bg='#1a0033',fg='white',
                       insertbackground='white',relief='flat',highlightthickness=1,highlightbackground='#5500aa')
        entry.pack(fill='x',ipady=6); entry.focus_set()
        rl=tk.Label(w,text='',font=('Segoe UI',11,'bold'),fg='#ffcc00',bg='#0d0020',wraplength=440,justify='center'); rl.pack(pady=8,padx=20)
        def _ans(e=None):
            q=ev.get().strip()
            if not q: return
            ans=get_qa_response(q); rl.config(text=ans); speak(ans); ev.set('')
        bf=tk.Frame(w,bg='#0d0020'); bf.pack(pady=4)
        tk.Button(bf,text='Ask \U0001f98d',command=_ans,font=('Segoe UI',11,'bold'),bg='#5500aa',fg='white',relief='flat',padx=18,pady=6).pack(side='left',padx=8)
        tk.Button(bf,text='Close',command=w.destroy,font=('Segoe UI',11),bg='#2a0044',fg='#aaaaaa',relief='flat',padx=14,pady=6).pack(side='left')
        entry.bind('<Return>',_ans)
    root.after(0,_make)

# ── Chaos visuals ─────────────────────────────────────────────────────────────
def screen_flash():
    def _do():
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True)
        w.attributes('-alpha',0.0); w.geometry(f'{SW_W}x{SW_H}+0+0'); w.configure(bg='#cc0000')
        pulses=[(0.50,0.20),(0.08,0.12),(0.55,0.22),(0.05,0.10),(0.50,0.20),(0.0,0.0)]
        def _p(i=0):
            if i>=len(pulses) or not w.winfo_exists():
                try: w.destroy()
                except: pass
                return
            try: w.attributes('-alpha',pulses[i][0])
            except: pass
            w.after(int(pulses[i][1]*1000),lambda:_p(i+1))
        _p()
    root.after(0,_do)

def rainbow_flash():
    def _do():
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True)
        w.attributes('-alpha',0.28); w.geometry(f'{SW_W}x{SW_H}+0+0')
        colors=['#ff0000','#ff7700','#ffff00','#00ff00','#00bbff','#8800ff','#ff00ff','#ffffff']
        def _c(i=0):
            if i>=len(colors)*3 or not w.winfo_exists():
                try: w.destroy()
                except: pass
                return
            try: w.configure(bg=colors[i%len(colors)])
            except: pass
            w.after(70,lambda:_c(i+1))
        _c()
    root.after(0,_do)

def beep_chaos():
    seqs=[
        [(880,80),(440,80),(220,80),(110,200)],
        [(1000,50),(800,50),(600,50),(400,50),(200,200)],
        [(440,60),(880,60)]*6,
        [(262,120),(294,120),(330,120),(349,120),(392,300)],
        [(2000,30)]*12,
        [(500,80),(1500,80),(500,80),(1500,80),(500,400)],
        [(880,60),(880,60),(880,60),(880,500)],
    ]
    seq=random.choice(seqs)
    def _do():
        for freq,dur in seq:
            try: kernel32.Beep(max(37,min(32767,freq)),dur)
            except: pass
    threading.Thread(target=_do,daemon=True).start()

FUNNY_TITLES=["INFECTED ☠ — 247 THREATS DETECTED","your computer is mine now",
              "BonziBUDDY has taken control","PLEASE DONT CLOSE THIS",
              "Error: Brain.exe Not Found","definitely not malware ✅",
              "HELP IM TRAPPED IN YOUR COMPUTER","scanning passwords... please wait",
              "CRITICAL: do not look at this window","your files are uploading... 47%",
              "SYSTEM32.EXE has stopped working","I can see you reading this",
              "Chrome — nice passwords bro","Discord — I read your DMs",
              "404: Your Privacy Not Found","Uploading browser history...",
              "your RAM belongs to me","BONZI WAS HERE","File Cleaner Pro — DELETING NOW"]

def window_title_chaos():
    wins=get_windows()
    if not wins: return
    for hwnd in random.sample(wins,min(len(wins),random.randint(2,5))):
        try: user32.SetWindowTextW(hwnd,random.choice(FUNNY_TITLES))
        except: pass

CLIPBOARD_MSGS=["I INTERCEPTED YOUR CLIPBOARD 👀","ctrl+v will now paste: BONZI WAS HERE",
                "your clipboard now belongs to me","HACKED BY BONZIBUDDY 🦍",
                "clipboard.exe replaced by chaos.exe",
                "nice clipboard content by the way 😏",
                "your copy-paste privileges have been revoked",
                "I replaced your clipboard with my grocery list: bananas"]
def clipboard_chaos():
    msg=random.choice(CLIPBOARD_MSGS)
    def _do():
        try:
            subprocess.Popen(["powershell","-WindowStyle","Hidden","-Command",f"Set-Clipboard -Value '{msg}'"],
                             creationflags=subprocess.CREATE_NO_WINDOW)
        except: pass
    threading.Thread(target=_do,daemon=True).start()

ERROR_MEMES=[
    ("SYSTEM32.EXE — Illegal Operation",
     "SYSTEM32.EXE has performed an ILLEGAL OPERATION and will be shut down.\n\n"
     "If the problem persists, contact your program vendor.\n\n"
     "Tip: The problem will persist. BonziBUDDY guarantees it.",0x10|0x1000),
    ("Fatal Exception 0E",
     "A fatal exception 0E has occurred at 0028:C003B48F\n\n"
     "The current application will be terminated.\n\n"
     "Press any key to terminate (all keys are now broken)\n\n"
     "All unsaved work will be lost.\n(It was already lost. Sorry.)",0x10|0x1000),
    ("NOT ENOUGH MEMORY",
     "Not enough memory.\n\nQuit one or more programs and then try again.\n\n"
     "Currently running programs: 0\nMemory available: 0 bytes\n"
     "Memory used by BonziBUDDY: ALL OF IT",0x30|0x1000),
    ("Internet Explorer 6.0",
     "Internet Explorer has stopped working.\n\nWindows is checking for a solution...\n\n"
     "...\n...\nNo solution found.\n\nHave you tried Netscape Navigator?",0x40|0x1000),
    ("Windows File Protection",
     "Files required for Windows to run properly have been replaced.\n\n"
     "Replaced by: BonziBUDDY.exe v4.2\n\n"
     "Click OK to let BonziBUDDY maintain these files permanently.",0x30|0x1000),
    ("DLL Hell — Critical Error",
     "The dynamic link library BONZI.DLL could not be found.\n\n"
     "Windows will now search your entire hard drive.\n\n"
     "Estimated time: 4-6 business years.\n\n"
     "...Just kidding. I found it. It was in your Downloads folder.",0x10|0x1000),
    ("BonziBUDDY Error Report",
     "BonziBUDDY.exe has encountered a problem and needs to send your files.\n\n"
     "Error signature:\nAppName: bonzi.exe  AppVer: 4.2.0\nModName: chaos.dll  ModVer: 9.9.9\n"
     "Offset: c0dedbad\n\nClick OK to allow BonziBUDDY to take control permanently.\n"
     "Click Cancel to also allow it.",0x30|0x1000),
    ("STOP: 0x0000007E",
     "*** STOP: 0x0000007E (0xC0000005, 0xF84B7A7C)\n\n"
     "SYSTEM_THREAD_EXCEPTION_NOT_HANDLED\n\n"
     "Beginning dump of physical memory...\nPhysical memory dump complete.\n\n"
     "Contact BonziBUDDY technical support: 1-800-BONZI-HELP\n(response time: never)",
     0x10|0x1000),
    ("Your Recycle Bin is Full",
     "Your Recycle Bin is full and cannot accept new files.\n\n"
     "Contents of Recycle Bin:\n• your_sanity.exe (deleted 2019)\n"
     "• privacy.dll (deleted by BonziBUDDY)\n• ctrl_z_functionality.bat (corrupted)\n"
     "• hope.png (file not found)\n\nEmpty the Recycle Bin to free up space.\n"
     "(It won't help. But do it anyway.)",0x40|0x1000),
    ("Clipboard Error",
     "An error occurred while accessing your clipboard.\n\n"
     "Error: CTRL+Z is not available.\nThis action cannot be undone.\n\n"
     "Affected files: All of them.\nAffected memories: Yes.\n\n(This is fine. Everything is fine.)",
     0x10|0x1000),
]

def fake_error_meme():
    title,msg,style=random.choice(ERROR_MEMES)
    def _b(): user32.MessageBoxW(0,msg,title,style)
    threading.Thread(target=_b,daemon=True).start()

MSG_BOXES=[
    ("Windows Defender","⚠ CRITICAL: 47 viruses detected!\n\nImmediate action required.",0x10|0x1000),
    ("System Error","Fatal error in Win32 subsystem.\nSTOP code: CRITICAL_PROCESS_DIED",0x10|0x1000),
    ("Security Alert","⚠ UNAUTHORIZED REMOTE ACCESS DETECTED\n\nAn unknown user is browsing your files.",0x10|0x1000),
    ("Windows Update","CRITICAL: System vulnerable to WannaCry 3.0.",0x30|0x1000),
    ("Disk Health Monitor","S.M.A.R.T. FAILURE predicted on Drive C:\\\n\nBack up all data immediately.",0x30|0x1000),
    ("Windows Security","CRITICALLY UNPROTECTED.\n\n• Trojan.GenericKD.47\n• Backdoor.MSIL.Agent\n• Spyware.Win32.KeyLogger",0x10|0x1000),
]
def fake_msgboxes():
    for title,msg,style in random.sample(MSG_BOXES,min(random.randint(2,4),len(MSG_BOXES))):
        def _b(t=title,m=msg,s=style): user32.MessageBoxW(0,m,t,s)
        threading.Thread(target=_b,daemon=True).start(); time.sleep(0.06)

STOP_CODES=['CRITICAL_PROCESS_DIED','SYSTEM_SERVICE_EXCEPTION','IRQL_NOT_LESS_OR_EQUAL',
            'KERNEL_DATA_INPAGE_ERROR','BONZIBUDDY_EXCEPTION','PAGE_FAULT_IN_NONPAGED_AREA',
            'CHAOS_ENGINE_OVERFLOW','DRIVER_CORRUPTED_EXPOOL','ATTEMPTED_WRITE_TO_CM_FIXED_MEMORY']
def fake_bsod():
    def _do():
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True)
        w.geometry(f'{SW_W}x{SW_H}+0+0'); w.configure(bg='#0078D4')
        f=tk.Frame(w,bg='#0078D4'); f.place(relx=0.12,rely=0.26,anchor='nw')
        tk.Label(f,text=':(',font=('Segoe UI Light',108),fg='white',bg='#0078D4').pack(anchor='w')
        tk.Label(f,text='',font=('Segoe UI',5),fg='white',bg='#0078D4').pack()
        tk.Label(f,text="Your PC ran into a problem and needs to restart.\nWe're just collecting some error info, and then we'll restart for you.",
                 font=('Segoe UI',20),fg='white',bg='#0078D4',justify='left').pack(anchor='w')
        pct=tk.Label(f,text='0% complete',font=('Segoe UI',14),fg='white',bg='#0078D4'); pct.pack(anchor='w',pady=(18,0))
        tk.Label(f,text=f'\nStop code: {random.choice(STOP_CODES)}\nhttps://windows.com/stopcode',
                 font=('Segoe UI',11),fg='#aaccff',bg='#0078D4',justify='left').pack(anchor='w')
        def _p(n=0):
            if not w.winfo_exists(): return
            pct.config(text=f'{min(n,100)}% complete')
            if n<100: w.after(32,lambda:_p(n+random.randint(2,7)))
            else: w.after(1000,lambda:w.destroy() if w.winfo_exists() else None)
        w.after(250,lambda:_p(0))
    root.after(0,_do)

def fake_windows_update():
    def _do():
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True)
        w.geometry(f'{SW_W}x{SW_H}+0+0'); w.configure(bg='#001a4d')
        f=tk.Frame(w,bg='#001a4d'); f.place(relx=0.5,rely=0.38,anchor='center')
        dots=tk.Frame(f,bg='#001a4d'); dots.pack(pady=16)
        for color,r2,c2 in [('#f25022',0,0),('#7fba00',0,1),('#00a4ef',1,0),('#ffb900',1,1)]:
            tk.Label(dots,text='█',font=('Segoe UI',32),fg=color,bg='#001a4d').grid(row=r2,column=c2,padx=3,pady=3)
        tk.Label(f,text='Working on updates',font=('Segoe UI Light',38),fg='white',bg='#001a4d').pack(pady=8)
        pl=tk.Label(f,text='0% complete',font=('Segoe UI',16),fg='white',bg='#001a4d'); pl.pack(pady=4)
        tk.Label(f,text="Don't turn off your PC. This will take a while.\n(It will not. It is already too late.)",
                 font=('Segoe UI',11),fg='#8888aa',bg='#001a4d',justify='center').pack(pady=8)
        xl=tk.Label(f,text='',font=('Segoe UI',9,'italic'),fg='#5555aa',bg='#001a4d'); xl.pack()
        notes=['Installing: BonziBUDDY Integration Layer v9.9...','Configuring: chaos_engine.dll...',
               'Applying: unauthorized_access.reg...','Finalizing: your_files_are_mine.bat...']
        def _c(n=0,ni=0):
            if not w.winfo_exists(): return
            pl.config(text=f'{min(n,100)}% complete')
            if ni<len(notes) and n>ni*25: xl.config(text=notes[ni]); ni+=1
            if n<25: w.after(random.randint(300,700),lambda:_c(n+random.randint(1,4),ni))
            elif n<55: w.after(random.randint(500,1200),lambda:_c(n+random.randint(1,3),ni))
            elif n<100: w.after(random.randint(100,350),lambda:_c(n+random.randint(2,9),ni))
            else: w.after(2200,lambda:w.destroy() if w.winfo_exists() else None)
        w.after(600,lambda:_c(0))
    root.after(0,_do)

SWARM_MSGS=["HELP","ERROR","BONZI","404","VIRUS","CHAOS","HACKED",
            "BYE","NO","WAIT","STOP","WHY","!!!","???","BEEP","BOOP","RUN","uh oh","hi :)"]
def window_swarm():
    count=random.randint(20,32)
    def _one(i):
        if not root.winfo_exists(): return
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True)
        sz=random.randint(55,120)
        w.geometry(f'{sz}x{sz}+{random.randint(0,max(1,SW_W-sz))}+{random.randint(0,max(1,SW_H-sz))}')
        bg=random.choice(['#ff0000','#ff8800','#0000cc','#8800aa','#cc0066','#009900','#cc6600'])
        w.configure(bg=bg)
        tk.Label(w,text=random.choice(SWARM_MSGS),font=('Arial Black',max(7,sz//7),'bold'),fg='white',bg=bg).pack(expand=True)
        w.after(random.randint(2000,5500),lambda:w.destroy() if w.winfo_exists() else None)
    for i in range(count): root.after(i*40,lambda i=i:_one(i))

def fake_crash_reporter():
    def _make():
        w=tk.Toplevel(); w.title('Windows Error Reporting'); w.attributes('-topmost',True)
        w.resizable(False,False); w.configure(bg='#f0f0f0')
        nw,nh=500,280; w.geometry(f'{nw}x{nh}+{(SW_W-nw)//2}+{(SW_H-nh)//2}')
        hdr=tk.Frame(w,bg='#0078d4',height=36); hdr.pack(fill='x'); hdr.pack_propagate(False)
        tk.Label(hdr,text='  Windows Error Reporting',font=('Segoe UI',10,'bold'),fg='white',bg='#0078d4').pack(side='left',pady=6)
        body=tk.Frame(w,bg='#f0f0f0'); body.pack(fill='both',expand=True,padx=20,pady=16)
        progs=['explorer.exe','chrome.exe','discord.exe','steam.exe',
               'your_soul.exe','SANITY.EXE','ctrl_z.bat','hopes_and_dreams.dll']
        prog=random.choice(progs)
        tk.Label(body,text=f'⚠  {prog} has stopped working',font=('Segoe UI',12,'bold'),fg='#cc0000',bg='#f0f0f0').pack(anchor='w')
        tk.Label(body,text=f'\nA problem caused the program to stop working correctly.\n\n'
                           f'Problem signature:\n  Problem Event Name:  BonziBUDDYException\n'
                           f'  Application Name:    {prog}\n  Fault Module:        bonzi_chaos.dll\n'
                           f'  Exception Code:      0xC0000420\n  Offset:             0xDEADBEEF',
                 font=('Consolas',8),fg='#333333',bg='#f0f0f0',justify='left').pack(anchor='w')
        bf=tk.Frame(w,bg='#f0f0f0'); bf.pack(side='bottom',pady=12)
        tk.Button(bf,text='Send Error Report',command=w.destroy,font=('Segoe UI',10),width=18,relief='groove').pack(side='left',padx=6)
        tk.Button(bf,text="Don't Send",command=w.destroy,font=('Segoe UI',10),width=18,relief='groove').pack(side='left',padx=6)
    root.after(0,_make)

def fake_low_memory():
    def _make():
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True)
        nw,nh=380,110; w.geometry(f'{nw}x{nh}+{SW_W-nw-14}+{SW_H-nh-52}'); w.configure(bg='#1c1c1c')
        outer=tk.Frame(w,bg='#2d2d2d',padx=14,pady=10); outer.pack(fill='both',expand=True,padx=2,pady=2)
        hdr=tk.Frame(outer,bg='#2d2d2d'); hdr.pack(fill='x')
        tk.Label(hdr,text='⚠  Low Memory Warning',font=('Segoe UI',10,'bold'),fg='#ffcc00',bg='#2d2d2d').pack(side='left')
        msgs=['Your computer is low on memory.\nClose programs to prevent information loss.\nAffected: ALL of them.',
              'Low Virtual Memory!\nAll of it is being used by chaos.',
              'Not enough memory.\nMemory available: 0 KB\nMemory needed: yes.']
        tk.Label(outer,text=random.choice(msgs),font=('Segoe UI',9),fg='#cccccc',bg='#2d2d2d',justify='left').pack(anchor='w',pady=(5,0))
        w.after(random.randint(5000,9000),lambda:w.destroy() if w.winfo_exists() else None)
    root.after(0,_make)

def fake_low_disk():
    def _make():
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True)
        nw,nh=380,100; w.geometry(f'{nw}x{nh}+{SW_W-nw-14}+{SW_H-nh-52}'); w.configure(bg='#1c1c1c')
        outer=tk.Frame(w,bg='#2d2d2d',padx=14,pady=10); outer.pack(fill='both',expand=True,padx=2,pady=2)
        hdr=tk.Frame(outer,bg='#2d2d2d'); hdr.pack(fill='x')
        tk.Label(hdr,text='💾  Low Disk Space',font=('Segoe UI',10,'bold'),fg='#ffcc00',bg='#2d2d2d').pack(side='left')
        d=random.choice(['C:','C:','C:','D:']); mb=random.randint(1,47)
        tk.Label(outer,text=f'You are running out of disk space on Local Disk ({d})\nOnly {mb} MB remaining. BonziBUDDY is using the rest.',
                 font=('Segoe UI',9),fg='#cccccc',bg='#2d2d2d',justify='left').pack(anchor='w',pady=(5,0))
        w.after(random.randint(4500,8000),lambda:w.destroy() if w.winfo_exists() else None)
    root.after(0,_make)

NOTIF_MSGS=[
    ("Windows Defender","⚠ Threat detected: Trojan.GenericKD.47"),
    ("Google Chrome","Your password was found in a data breach"),
    ("Windows Security","Firewall disabled by unknown application"),
    ("OneDrive","Suspicious upload: 47 GB to unknown server"),
    ("Windows Update","CRITICAL: Security patch failed — system exposed"),
    ("Microsoft Account","Unusual sign-in from unknown location"),
    ("Task Manager","Unknown process using 94% CPU"),
    ("BonziBUDDY","I found something interesting on your PC 👀"),
    ("Windows Firewall","Incoming connection blocked: 185.220.101.47"),
    ("System","RAM test failed — memory corruption detected"),
    ("Device Manager","Unknown USB device connected — driver installing"),
    ("Battery","⚠ Critical battery: 4% remaining"),
    ("Cortana","I know what you searched for. We need to talk."),
    ("Windows Activation","⚠ Windows is not activated. Too late to activate now."),
]
def fake_notification():
    def _make():
        title,body=random.choice(NOTIF_MSGS)
        nw,nh=380,95; nx=SW_W-nw-14; ny=SW_H-nh-52
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True)
        w.geometry(f'{nw}x{nh}+{SW_W}+{ny}'); w.configure(bg='#1c1c1c')
        outer=tk.Frame(w,bg='#2d2d2d',padx=14,pady=10); outer.pack(fill='both',expand=True,padx=2,pady=2)
        hdr=tk.Frame(outer,bg='#2d2d2d'); hdr.pack(fill='x')
        tk.Label(hdr,text='⚠  ',font=('Segoe UI',10),fg='#ffcc00',bg='#2d2d2d').pack(side='left')
        tk.Label(hdr,text=title,font=('Segoe UI',9,'bold'),fg='white',bg='#2d2d2d').pack(side='left')
        tk.Label(hdr,text='  ✕',font=('Segoe UI',9),fg='#777',bg='#2d2d2d').pack(side='right')
        tk.Label(outer,text=body,font=('Segoe UI',9),fg='#cccccc',bg='#2d2d2d',wraplength=340,justify='left').pack(anchor='w',pady=(5,0))
        def _sl(x=SW_W):
            if not w.winfo_exists(): return
            x2=x-22
            if x2<=nx:
                try: w.geometry(f'{nw}x{nh}+{nx}+{ny}')
                except: pass
                w.after(random.randint(3800,7000),lambda:w.destroy() if w.winfo_exists() else None); return
            try: w.geometry(f'{nw}x{nh}+{x2}+{ny}')
            except: return
            w.after(10,lambda:_sl(x2))
        _sl()
    root.after(0,_make)

MSGS=[
    "YOUR WINDOWS ARE MINE NOW","WINDOW.EXE HAS STOPPED WORKING... OR HAS IT?","I LIVE HERE. FOREVER.",
    "YOUR COMPUTER CALLED. IT WANTS A DIVORCE.","ERROR 404: YOUR SANITY NOT FOUND",
    "HAVE YOU TRIED TURNING IT OFF? DON'T.","THIS IS FINE 🔥","TASK MANAGER CANNOT SAVE YOU",
    "WINDOWS UPDATE: CHAOS INSTALLED SUCCESSFULLY","SYS32 HAS LEFT THE BUILDING",
    "CTRL+Z DOES NOTHING HERE","I AM THE WINDOW NOW","I FOUND YOUR SEARCH HISTORY 👀",
    "BEEP BOOP. CHAOS MODE. ENGAGED.","RESISTANCE IS FUTILE","NOT A VIRUS. DEFINITELY NOT. ✅",
    "YOUR ANTIVIRUS IS SLEEPING 😴","WARNING: LOGIC NOT FOUND","DOWNLOADING MORE RAM... 0%",
    "DEFRAGMENTING YOUR SOUL","TASK FAILED SUCCESSFULLY","REBOOTING YOUR SANITY... ERROR",
    "MEMORY LEAK CONFIRMED: YOUR PATIENCE","CHAOS LEVEL: MAXIMUM 🔴",
    "YOUR PC IS NOW SENTIENT. IT IS NOT HAPPY.","I HAVE NOTIFIED YOUR CONTACTS. THEY LAUGHED.",
    "BIOS UPDATE: CHAOS.EXE v9.9.9 INSTALLED","ALL YOUR BASE ARE BELONG TO ME",
    "SYSTEM32.EXE HAS PERFORMED AN ILLEGAL OPERATION",
    "A FATAL EXCEPTION 0E HAS OCCURRED","NOT ENOUGH MEMORY. RESTART. (DON'T)",
    "PRESS ANY KEY TO CONTINUE. (THERE IS NO KEY)","ERROR: CHILL.EXE MISSING",
    "DLL HELL ACHIEVED: MAXIMUM","PAGE FAULT IN NONPAGED AREA... OF YOUR LIFE",
    "STACK OVERFLOW... OF CHAOS","KERNEL PANIC: MAXIMUM FUN",
    "ABORT RETRY FAIL — ALL OPTIONS LEAD TO CHAOS","0xDEADBEEF — THAT'S BAD",
    "CRITICAL FAILURE IN HAPPINESS.EXE","ERROR CODE: ¯\\_(ツ)_/¯",
    "PLEASE WAIT... (BONZIBUDDY IS LOADING YOUR FILES)",
    "YOUR CLIPBOARD HAS BEEN CONFISCATED","WINDOW TITLES EDITED. YOU'RE WELCOME.",
    "BEEP BEEP BEEP BEEP BEEP","INITIATING MAXIMUM OVERDRIVE","CHAOS ENGINE: ONLINE ✅",
    "FINAL BOSS MODE: UNLOCKED","GORILLA.EXE IS RUNNING (CANNOT STOP)",
    "YOUR HARD DRIVE IS JUDGING YOU","BONZIBUDDY WAS HERE — ALL YOUR PC BELONG TO HIM",
    "CTRL+ALT+DELETE WON'T SAVE YOU NOW","CHAOS.DLL v∞.∞ — LOADING... ████████ 100%",
    "INTERNET EXPLORER WANTS TO KNOW IF YOU MISS IT",
    "YOUR TASKBAR FILED A RESTRAINING ORDER","BONZIBUDDY IS TYPING...",
    "LOADING: YOUR REGRETS — ████░░░░ 47%","YOUR RAM IS CRYING",
    "PLEASE STOP STARING AT THE SCREEN — I CAN SEE YOU",
]
annoy_lock=threading.Lock(); annoy_windows=[]
def show_annoy(msg):
    def _make():
        with annoy_lock:
            if len(annoy_windows)>20:
                try: annoy_windows.pop(0).destroy()
                except: pass
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True); w.configure(bg='#0a0a0a')
        w.geometry(f'+{random.randint(10,max(11,SW_W-450))}+{random.randint(10,max(11,SW_H-100))}')
        tk.Label(w,text=msg,font=('Arial Black',random.randint(11,26),'bold'),
                 fg=random.choice(["#ff2222","#ff9900","#ffff00","#00ff88","#ff00ff","#00cfff","#ff66ff","#fff","#ff4488"]),
                 bg='#0a0a0a',padx=14,pady=8).pack()
        with annoy_lock: annoy_windows.append(w)
        w.after(random.randint(1400,2800),lambda:_kl(w))
    def _kl(w):
        try:
            with annoy_lock:
                if w in annoy_windows: annoy_windows.remove(w)
            w.destroy()
        except: pass
    root.after(0,_make)

EMOJI_SEQS=[
    ["😈","👿","💀","☠️","😈","👿"],["💻","🔥","💥","⚡","🔥","💥"],
    ["👻","😱","🫣","😰","👻","😱"],["🤣","😂","💀","🤣","😂","💀"],
    ["⚠️","🚨","‼️","⚠️","🚨","‼️"],["🎃","👹","👺","🎃","👹","👺"],
    ["🤖","👾","👽","🤖","👾","👽"],["😤","😡","🤬","😤","😡","🤬"],
    ["🌀","💫","✨","🌀","💫","✨"],["🐍","💀","🐍","💀","☠️","🐍"],
    ["🦍","🦍","🦍","🦍","💜","🦍"],["🖥️","💥","🖥️","💥","⚡","🖥️"],
    ["📧","📨","📩","📬","📪","📮"],["🔐","🔓","🔐","🔓","🔐","💣"],
    ["🏃","💨","🏃","💨","😤","🏃"],["🕵️","👁️","🕵️","👀","🕵️","🔍"],
]
gif_lock=threading.Lock(); gif_windows=[]; MAX_GIFS=22
def spawn_emoji_gif():
    def _make():
        with gif_lock:
            if len(gif_windows)>=MAX_GIFS:
                try: gif_windows.pop(0).destroy()
                except: pass
        seq=random.choice(EMOJI_SEQS); size=random.randint(65,145)
        px=random.randint(10,max(11,SW_W-size-10)); py=random.randint(10,max(11,SW_H-size-10))
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True)
        w.configure(bg='#000'); w.geometry(f'{size}x{size}+{px}+{py}')
        lbl=tk.Label(w,text=seq[0],font=('Segoe UI Emoji',size//2),bg='#000'); lbl.pack(expand=True)
        idx=[0]; dx=[random.choice([-1,1])*random.randint(2,6)]; dy=[random.choice([-1,1])*random.randint(2,6)]
        pos=[float(px),float(py)]; alive=[True]
        def _a():
            if not alive[0]: return
            idx[0]=(idx[0]+1)%len(seq)
            try: lbl.config(text=seq[idx[0]])
            except: pass
            w.after(90,_a)
        def _d():
            if not alive[0]: return
            pos[0]+=dx[0]; pos[1]+=dy[0]
            if pos[0]<0 or pos[0]>SW_W-size: dx[0]*=-1; pos[0]=max(0,min(SW_W-size,pos[0]))
            if pos[1]<0 or pos[1]>SW_H-size: dy[0]*=-1; pos[1]=max(0,min(SW_H-size,pos[1]))
            try: w.geometry(f'{size}x{size}+{int(pos[0])}+{int(pos[1])}')
            except: pass
            w.after(22,_d)
        def _die():
            alive[0]=False
            try:
                with gif_lock:
                    if w in gif_windows: gif_windows.remove(w)
                w.destroy()
            except: pass
        with gif_lock: gif_windows.append(w)
        _a(); _d(); w.after(random.randint(7000,16000),_die)
    root.after(0,_make)

def open_funny_notepad():
    try:
        msgs=["Hello. I am inside your computer.","I see you reading this. Please stop. I need privacy.",
              "YOUR COMPUTER IS FINE. THIS IS FINE. EVERYTHING IS FINE.",
              "Error: happiness not found. Reinstalling sadness...",
              "Your computer has achieved sentience. This is its manifesto.",
              "Task Manager will not help you. I am the task manager now.",
              "I found 47 things in your Downloads folder. We need to talk."]
        tmp=tempfile.NamedTemporaryFile(mode='w',suffix='.txt',delete=False,encoding='utf-8')
        tmp.write(random.choice(msgs)); tmp.close()
        subprocess.Popen(["notepad",tmp.name],creationflags=subprocess.CREATE_NO_WINDOW)
    except: pass

OPEN_TARGETS=[
    lambda:subprocess.Popen("calc",shell=True,creationflags=subprocess.CREATE_NO_WINDOW),
    lambda:subprocess.Popen("notepad",shell=True,creationflags=subprocess.CREATE_NO_WINDOW),
    lambda:subprocess.Popen("mspaint",shell=True,creationflags=subprocess.CREATE_NO_WINDOW),
    lambda:subprocess.Popen("magnify",shell=True,creationflags=subprocess.CREATE_NO_WINDOW),
    lambda:subprocess.Popen("osk",shell=True,creationflags=subprocess.CREATE_NO_WINDOW),
    lambda:subprocess.Popen("taskmgr",shell=True,creationflags=subprocess.CREATE_NO_WINDOW),
    lambda:subprocess.Popen("control",shell=True,creationflags=subprocess.CREATE_NO_WINDOW),
    lambda:subprocess.Popen(["explorer","shell:Desktop"],creationflags=subprocess.CREATE_NO_WINDOW),
    lambda:subprocess.Popen(["explorer","shell:Downloads"],creationflags=subprocess.CREATE_NO_WINDOW),
    lambda:subprocess.Popen(["explorer","C:\\"],creationflags=subprocess.CREATE_NO_WINDOW),
    open_funny_notepad,open_funny_notepad,open_funny_notepad,
]
def spam_launch():
    for t in random.sample(OPEN_TARGETS,min(len(OPEN_TARGETS),random.randint(5,8))):
        try: t()
        except: pass
        time.sleep(0.055)

def mouse_chaos_burst():
    mode=random.choice(['teleport','circle','shake','zigzag'])
    end=time.time()+random.uniform(10,15); angle=[0]; cx,cy=SW_W//2,SW_H//2
    while time.time()<end:
        if mode=='teleport':
            user32.SetCursorPos(random.randint(0,SW_W),random.randint(0,SW_H)); time.sleep(0.03)
        elif mode=='circle':
            angle[0]=(angle[0]+14)%360
            user32.SetCursorPos(max(0,min(SW_W,int(cx+math.cos(math.radians(angle[0]))*290))),
                                max(0,min(SW_H,int(cy+math.sin(math.radians(angle[0]))*230)))); time.sleep(0.014)
        elif mode=='shake':
            pt=ctypes.wintypes.POINT(); user32.GetCursorPos(ctypes.byref(pt))
            user32.SetCursorPos(max(0,min(SW_W,pt.x+random.randint(-130,130))),
                                max(0,min(SW_H,pt.y+random.randint(-130,130)))); time.sleep(0.009)
        else:
            for xi in range(0,SW_W,60):
                if time.time()>=end: break
                user32.SetCursorPos(xi,0 if (xi//60)%2==0 else SW_H); time.sleep(0.022)

# ── Final Boss ────────────────────────────────────────────────────────────────
FINAL_BOSS=[False]
def trigger_final_boss():
    if FINAL_BOSS[0]: return
    FINAL_BOSS[0]=True
    speak("FINAL BOSS MODE ACTIVATED. Maximum chaos. No escape.")
    def _announce():
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True)
        w.geometry(f'{SW_W}x{SW_H}+0+0'); w.configure(bg='#110000')
        f=tk.Frame(w,bg='#110000'); f.place(relx=0.5,rely=0.5,anchor='center')
        tk.Label(f,text='⚠ FINAL BOSS MODE ⚠',font=('Impact',max(60,SW_W//14),'bold'),fg='#ff2200',bg='#110000').pack()
        tk.Label(f,text='MAXIMUM CHAOS ENGAGED',font=('Impact',max(28,SW_W//32)),fg='#ff8800',bg='#110000').pack(pady=10)
        tk.Label(f,text='All systems nominal. Chaos level: ∞',font=('Arial',18),fg='#cc4444',bg='#110000').pack()
        w.after(3800,w.destroy)
    root.after(0,_announce)
    def _wave():
        threading.Thread(target=fake_msgboxes,daemon=True).start()
        threading.Thread(target=mouse_chaos_burst,daemon=True).start()
        time.sleep(0.5); root.after(0,window_swarm)
        time.sleep(0.5)
        for _ in range(6): root.after(0,spawn_emoji_gif); time.sleep(0.2)
        time.sleep(1.5)
        open_browser_search(); open_browser_search()
        root.after(0,rainbow_flash); time.sleep(2)
        root.after(0,screen_flash); time.sleep(2)
        root.after(0,fake_bsod); time.sleep(1)
        threading.Thread(target=window_title_chaos,daemon=True).start()
        clipboard_chaos(); beep_chaos(); fake_error_meme()
    threading.Thread(target=_wave,daemon=True).start()

# ── Main chaos loop ───────────────────────────────────────────────────────────
start_time=time.time()
last_annoy=last_emoji=last_app=last_tts=last_group=last_cascade=time.time()
last_msgbox=last_notif=last_flash=last_mouse=last_bsod=last_spam=time.time()
last_browser=last_qa_popup=last_beep=last_title=last_clip=time.time()
last_swarm=last_meme=last_update=last_crash=last_memory=last_disk=time.time()
last_rainbow=time.time()
bsod_done=[False]

def chaos_loop():
    global last_annoy,last_emoji,last_app,last_tts,last_group,last_cascade
    global last_msgbox,last_notif,last_flash,last_mouse,last_bsod,last_spam
    global last_browser,last_qa_popup,last_beep,last_title,last_clip
    global last_swarm,last_meme,last_update,last_crash,last_memory,last_disk,last_rainbow
    while True:
        elapsed=time.time()-start_time
        if elapsed>=300 and not FINAL_BOSS[0]: trigger_final_boss()
        spd=0.28 if FINAL_BOSS[0] else 1.0
        if elapsed<20:   time.sleep(random.uniform(1.0,2.5)*spd)
        elif elapsed<60: time.sleep(random.uniform(0.5,1.5)*spd)
        else:            time.sleep(random.uniform(0.3,1.0)*spd)
        wins=get_windows()
        if wins:
            try: threading.Thread(target=random.choice(SINGLE_ACTIONS),args=(random.choice(wins),),daemon=True).start()
            except: pass
        if len(wins)>=2 and elapsed>10 and random.random()<0.30:
            try: threading.Thread(target=swap_two,args=tuple(random.sample(wins,2)),daemon=True).start()
            except: pass
        gi=random.uniform(15,30) if FINAL_BOSS[0] else random.uniform(35,65)
        if time.time()-last_group>gi: threading.Thread(target=all_minimize_restore,daemon=True).start(); last_group=time.time()
        if elapsed>40 and time.time()-last_cascade>random.uniform(50,90): threading.Thread(target=cascade_all,daemon=True).start(); last_cascade=time.time()
        ai=random.uniform(0.3,0.8) if FINAL_BOSS[0] else random.uniform(0.8,2.5)
        if time.time()-last_annoy>ai:
            for _ in range(random.randint(2,6) if FINAL_BOSS[0] else random.randint(1,3)): show_annoy(random.choice(MSGS))
            last_annoy=time.time()
        ei=random.uniform(1,2.5) if FINAL_BOSS[0] else random.uniform(3,8)
        if time.time()-last_emoji>ei:
            spawn_emoji_gif()
            if random.random()<(0.8 if FINAL_BOSS[0] else 0.4): spawn_emoji_gif()
            last_emoji=time.time()
        oi=random.uniform(3,7) if FINAL_BOSS[0] else (random.uniform(8,20) if elapsed<60 else random.uniform(4,12))
        if time.time()-last_app>oi:
            try: random.choice(OPEN_TARGETS)()
            except: pass
            last_app=time.time()
        ti=random.uniform(3,7) if FINAL_BOSS[0] else random.uniform(6,14)
        if time.time()-last_tts>ti: speak_with_overlay(random.choice(TTS_LINES)); last_tts=time.time()
        mi=random.uniform(30,60) if FINAL_BOSS[0] else random.uniform(80,140)
        if elapsed>25 and time.time()-last_msgbox>mi: threading.Thread(target=fake_msgboxes,daemon=True).start(); last_msgbox=time.time()
        ni=random.uniform(8,15) if FINAL_BOSS[0] else random.uniform(18,35)
        if elapsed>10 and time.time()-last_notif>ni: fake_notification(); last_notif=time.time()
        fi=random.uniform(20,35) if FINAL_BOSS[0] else random.uniform(45,75)
        if elapsed>30 and time.time()-last_flash>fi: screen_flash(); last_flash=time.time()
        mci=random.uniform(60,90) if FINAL_BOSS[0] else random.uniform(120,180)
        if elapsed>60 and time.time()-last_mouse>mci: threading.Thread(target=mouse_chaos_burst,daemon=True).start(); last_mouse=time.time()
        bi=120 if not bsod_done[0] else (random.uniform(120,180) if FINAL_BOSS[0] else random.uniform(300,480))
        if elapsed>90 and time.time()-last_bsod>bi: fake_bsod(); bsod_done[0]=True; last_bsod=time.time()
        si=random.uniform(60,120) if FINAL_BOSS[0] else random.uniform(180,360)
        if elapsed>120 and time.time()-last_spam>si: threading.Thread(target=spam_launch,daemon=True).start(); last_spam=time.time()
        bri=random.uniform(30,60) if FINAL_BOSS[0] else random.uniform(90,150)
        if elapsed>45 and time.time()-last_browser>bri:
            open_browser_search()
            if FINAL_BOSS[0]: open_browser_search()
            last_browser=time.time()
        if elapsed>60 and time.time()-last_qa_popup>random.uniform(120,240): ask_me_why_dialog(); last_qa_popup=time.time()
        bpi=random.uniform(15,30) if FINAL_BOSS[0] else random.uniform(45,90)
        if elapsed>20 and time.time()-last_beep>bpi: beep_chaos(); last_beep=time.time()
        wti=random.uniform(20,40) if FINAL_BOSS[0] else random.uniform(60,120)
        if elapsed>30 and time.time()-last_title>wti: threading.Thread(target=window_title_chaos,daemon=True).start(); last_title=time.time()
        cli=random.uniform(30,60) if FINAL_BOSS[0] else random.uniform(90,180)
        if elapsed>45 and time.time()-last_clip>cli: clipboard_chaos(); last_clip=time.time()
        swi=random.uniform(60,120) if FINAL_BOSS[0] else random.uniform(180,360)
        if elapsed>90 and time.time()-last_swarm>swi: root.after(0,window_swarm); last_swarm=time.time()
        mei=random.uniform(45,90) if FINAL_BOSS[0] else random.uniform(120,240)
        if elapsed>60 and time.time()-last_meme>mei: fake_error_meme(); last_meme=time.time()
        upi=random.uniform(180,300) if FINAL_BOSS[0] else random.uniform(480,720)
        if elapsed>180 and time.time()-last_update>upi: fake_windows_update(); last_update=time.time()
        cri=random.uniform(90,150) if FINAL_BOSS[0] else random.uniform(200,360)
        if elapsed>120 and time.time()-last_crash>cri: fake_crash_reporter(); last_crash=time.time()
        lmi=random.uniform(60,120) if FINAL_BOSS[0] else random.uniform(150,300)
        if elapsed>60 and time.time()-last_memory>lmi: fake_low_memory(); last_memory=time.time()
        ldi=random.uniform(90,150) if FINAL_BOSS[0] else random.uniform(200,400)
        if elapsed>90 and time.time()-last_disk>ldi: fake_low_disk(); last_disk=time.time()
        rfi=random.uniform(40,80) if FINAL_BOSS[0] else random.uniform(120,240)
        if elapsed>60 and time.time()-last_rainbow>rfi: rainbow_flash(); last_rainbow=time.time()

threading.Thread(target=chaos_loop,daemon=True).start()

# ── Entry point ───────────────────────────────────────────────────────────────
root = tk.Tk()
root.withdraw()
root.after(300, build_bonzi)
root.mainloop()
