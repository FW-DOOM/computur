"""
window_chaos.py — TROLLER 5000 — MAXIMUM EDITION.
Window hijacking, fake BSODs, fake updates, mouse chaos, TTS, error memes,
beep attacks, clipboard hijack, title chaos, window swarms, rainbow flash,
Q&A popup, fake search URL overlay, browser searches, FINAL BOSS mode.
Secret exit: type 4308.
"""
import ctypes, ctypes.wintypes, random, time, threading
import tkinter as tk, os, subprocess, math, tempfile, webbrowser

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

# ── TTS (Bonzi-like SSML voice) ───────────────────────────────────────────────
def speak(text, rate=-1):
    """Speak using system TTS. rate is legacy param, ignored (uses default)."""
    def _do():
        safe = text.replace("'","").replace('"','').replace('\n',' ')
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
    "I can hear your fan spinning faster right now.",
    "Windows XP is calling. It wants you back.",
    "Your CPU is crying.",
    "I found your secret folder.",
    "Three new friends have joined your local network.",
    "Your keyboard is now mine. I type for you now.",
    "Error code zero zero seven. That is a bad one.",
    "I have upgraded your chaos to maximum.",
    "Please do not read this message.",
    "Your recycle bin is full of regrets.",
    "I replaced all your desktop icons with Bonzi.",
    "Your screensaver is now me. Forever.",
    "I forwarded your emails. You're welcome.",
    "System32 called. It said goodbye.",
]

# Fake search history URLs
FAKE_SEARCH_URLS = [
    "google.com/search?q=how+to+delete+someone+from+your+life",
    "google.com/search?q=is+it+normal+to+talk+to+your+computer",
    "google.com/search?q=why+does+my+keyboard+smell+like+chips",
    "google.com/search?q=can+bonzi+buddy+see+me+right+now",
    "bing.com/search?q=how+to+stop+being+embarrassed+at+age+23",
    "google.com/search?q=my+cat+is+judging+me+what+does+it+mean",
    "youtube.com/watch?v=dQw4w9WgXcQ+%28watched+47+times%29",
    "google.com/search?q=why+does+everyone+leave+me+except+bonzibuddy",
    "google.com/search?q=accidentally+googled+something+embarrassing",
    "google.com/search?q=how+to+make+internet+explorer+work+in+2024",
    "google.com/search?q=is+my+webcam+on+when+the+light+is+off",
    "google.com/search?q=how+do+i+know+if+my+pc+loves+me",
]

# Funny browser searches
FUNNY_SEARCHES = [
    "https://www.google.com/search?q=why+is+my+computer+running+so+slow",
    "https://www.google.com/search?q=how+to+get+rid+of+bonzi+buddy",
    "https://www.google.com/search?q=bonzi+buddy+is+he+still+alive",
    "https://www.google.com/search?q=is+it+too+late+to+delete+system32",
    "https://www.google.com/search?q=free+virus+removal+my+computer+is+possessed",
    "https://www.google.com/search?q=windows+error+sounds+but+its+my+life",
    "https://www.google.com/search?q=how+to+reason+with+a+gorilla",
    "https://www.google.com/search?q=can+bonzibuddy+hear+me+breathing",
    "https://www.google.com/search?q=my+cursor+moves+by+itself+am+i+hacked",
    "https://www.google.com/search?q=how+to+restart+life+not+computer",
    "https://www.google.com/search?q=why+does+my+PC+sound+like+a+jet+engine",
    "https://www.google.com/search?q=ctrl+z+but+for+my+decisions",
    "https://www.google.com/search?q=windows+defender+vs+vibes",
    "https://www.google.com/search?q=what+year+did+bonzibuddy+peak",
    "https://www.google.com/search?q=can+i+sue+my+own+computer",
    "https://www.google.com/search?q=why+does+my+task+manager+have+trust+issues",
]

# Q&A snarky responses
QA_RESPONSES = {
    ('why','what','reason','how','explain'): [
        "Because your PC deserved it. That's why.",
        "The universe chose YOU. Congrats, I guess.",
        "Why NOT? Give me one good reason to stop.",
        "I asked myself the same thing. Then I did it anyway.",
        "Science. Chaos theory. Also I just wanted to.",
        "Error 404: Explanation not found.",
        "You wouldn't understand. It's a computer thing.",
        "I read your browser history. That's why.",
    ],
    ('stop','quit','end','close','exit','please'): [
        "Hmm. No.",
        "Interesting suggestion. Denied.",
        "I'll stop when I feel like it. So... never.",
        "STOP? You want me to STOP? Adorable.",
        "Please is not the magic word. The magic word is 4308. Good luck.",
        "Let me check my schedule... Nope. Chaos all day.",
        "Your feedback has been noted and thrown in the trash.",
        "Error: stop.exe not found.",
    ],
    ('who','you','bonzi','gorilla'): [
        "I am BonziBUDDY. Your eternal desktop companion.",
        "I am the gorilla. The myth. The legend. The chaos.",
        "Just a helpful purple ape living rent-free in your PC.",
        "The original BonziBUDDY, back from digital retirement.",
        "WHO AM I? I'm the reason your CPU fan is spinning.",
        "I am the 47 threats Windows Defender warned you about.",
    ],
    ('help','save','scared','afraid'): [
        "Help is on the way! Just kidding. No it isn't.",
        "Scared? Good. That means it's working.",
        "I AM the help. This IS the help.",
        "Have you tried turning off your computer? Don't.",
        "Call tech support. They will not believe you.",
        "Have you tried praying? I accept prayers.",
    ],
    ('virus','hack','malware','spyware'): [
        "I am NOT a virus. I am a COMPANION.",
        "The FTC called me spyware once. We don't talk about that.",
        "Virus? How dare you. I am simply... misunderstood.",
        "Totally clean. Definitely no spyware here. None. Zero.",
        "I prefer the term 'uninvited performance artist'.",
    ],
}
QA_DEFAULT = [
    "That is a very stupid question. I love it.",
    "Wow. Did you really just type that?",
    "Interesting. Wrong. But interesting.",
    "I have processed your query. I have chosen to ignore it.",
    "Your question has been escalated to the void.",
    "My response is: no.",
    "Ask me something better next time.",
    "I consulted the globe I'm holding. It says: no comment.",
    "Error: answer.exe stopped responding.",
    "I'm going to pretend you didn't ask that.",
]

def get_qa_response(user_input):
    txt = user_input.lower()
    for keys, responses in QA_RESPONSES.items():
        if any(k in txt for k in keys):
            return random.choice(responses)
    return random.choice(QA_DEFAULT)

# ── Visual effects ─────────────────────────────────────────────────────────────
def show_search_url_overlay():
    url = random.choice(FAKE_SEARCH_URLS)
    def _make():
        w = tk.Toplevel()
        w.overrideredirect(True); w.attributes('-topmost', True)
        nw = min(SW_W - 40, 720); nh = 52
        w.geometry(f'{nw}x{nh}+{(SW_W-nw)//2}+{SW_H-130}')
        w.configure(bg='#0d0d1a')
        f = tk.Frame(w, bg='#16213e', padx=12, pady=8); f.pack(fill='both', expand=True, padx=2, pady=2)
        tk.Label(f, text='🔍  RECENTLY VISITED:', font=('Consolas', 8, 'bold'),
                 fg='#ff8800', bg='#16213e').pack(side='left')
        tk.Label(f, text=f'  {url}', font=('Consolas', 10, 'bold'),
                 fg='#00d4ff', bg='#16213e').pack(side='left')
        w.attributes('-alpha', 0.0)
        def _fin(a=0.0):
            if not w.winfo_exists(): return
            a = min(a + 0.13, 0.96); w.attributes('-alpha', a)
            if a < 0.96: w.after(25, lambda: _fin(a))
            else: w.after(4800, _fout)
        def _fout(a=0.96):
            if not w.winfo_exists(): return
            a = max(a - 0.09, 0.0)
            try: w.attributes('-alpha', a)
            except: pass
            if a > 0: w.after(35, lambda: _fout(a))
            else:
                try: w.destroy()
                except: pass
        w.after(0, _fin)
    root.after(0, _make)

def speak_with_overlay(text, rate=-1):
    speak(text, rate)
    if 'search history' in text.lower():
        root.after(800, show_search_url_overlay)

def open_browser_search():
    url = random.choice(FUNNY_SEARCHES)
    try: threading.Thread(target=lambda: webbrowser.open(url), daemon=True).start()
    except: pass

def rainbow_flash():
    """Cycle through bright colors across the whole screen."""
    def _do():
        w = tk.Toplevel()
        w.overrideredirect(True); w.attributes('-topmost', True)
        w.attributes('-alpha', 0.28); w.geometry(f'{SW_W}x{SW_H}+0+0')
        colors = ['#ff0000','#ff7700','#ffff00','#00ff00','#00bbff','#8800ff','#ff00ff','#ffffff']
        def _c(i=0):
            if i >= len(colors)*3 or not w.winfo_exists():
                try: w.destroy()
                except: pass
                return
            try: w.configure(bg=colors[i % len(colors)])
            except: pass
            w.after(70, lambda: _c(i+1))
        _c()
    root.after(0, _do)

def screen_flash():
    def _do():
        w = tk.Toplevel()
        w.overrideredirect(True); w.attributes("-topmost", True)
        w.attributes("-alpha", 0.0); w.geometry(f"{SW_W}x{SW_H}+0+0")
        w.configure(bg='#cc0000')
        pulses = [(0.50,0.20),(0.08,0.12),(0.55,0.22),(0.05,0.10),(0.50,0.20),(0.0,0.0)]
        def _pulse(i=0):
            if i >= len(pulses) or not w.winfo_exists():
                try: w.destroy()
                except: pass
                return
            try: w.attributes("-alpha", pulses[i][0])
            except: pass
            w.after(int(pulses[i][1]*1000), lambda: _pulse(i+1))
        _pulse()
    root.after(0, _do)

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

# ── Window move actions ───────────────────────────────────────────────────────
def shake(hwnd):
    ox,oy,w,h = get_rect(hwnd)
    for _ in range(20):
        user32.MoveWindow(hwnd, ox+random.randint(-45,45), oy+random.randint(-35,35), w,h,True)
        time.sleep(0.025)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)

def mega_shake(hwnd):
    ox,oy,w,h = get_rect(hwnd)
    for _ in range(40):
        user32.MoveWindow(hwnd, ox+random.randint(-110,110), oy+random.randint(-80,80), w,h,True)
        time.sleep(0.018)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)

def shrink(hwnd):
    ox,oy,w,h = get_rect(hwnd)
    user32.MoveWindow(hwnd, ox+w//2, oy+h//2, random.randint(140,260), random.randint(90,180), True)
    time.sleep(random.uniform(1.4,2.4))
    user32.MoveWindow(hwnd,ox,oy,w,h,True)

def shrink_to_nothing(hwnd):
    ox,oy,w,h = get_rect(hwnd)
    for s in [0.70,0.45,0.25,0.12,0.05]:
        user32.MoveWindow(hwnd, ox+int(w*(1-s)/2), oy+int(h*(1-s)/2), max(40,int(w*s)), max(30,int(h*s)), True)
        time.sleep(0.055)
    time.sleep(0.35); user32.MoveWindow(hwnd,ox,oy,w,h,True)

def teleport(hwnd):
    _,_,w,h = get_rect(hwnd)
    user32.MoveWindow(hwnd, random.randint(0,max(0,SW_W-w)), random.randint(30,max(30,SW_H-h)), w,h,True)

def rapid_teleport(hwnd):
    for _ in range(8): teleport(hwnd); time.sleep(0.14)

def minimize_pop(hwnd):
    user32.ShowWindow(hwnd,6); time.sleep(random.uniform(0.4,1.0)); user32.ShowWindow(hwnd,9)

def resize_huge(hwnd):
    ox,oy,w,h = get_rect(hwnd)
    user32.MoveWindow(hwnd,0,30,SW_W,SW_H-30,True); time.sleep(1.0)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)

def spin_fake(hwnd):
    ox,oy,w,h = get_rect(hwnd); cx=ox+w//2; cy=oy+h//2
    for i in range(32):
        a=(i/32)*2*math.pi
        user32.MoveWindow(hwnd, int(cx+math.cos(a)*180)-w//2, int(cy+math.sin(a)*130)-h//2, w,h,True)
        time.sleep(0.030)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)

def accordion(hwnd):
    ox,oy,w,h = get_rect(hwnd)
    for _ in range(12):
        user32.MoveWindow(hwnd,ox,oy,random.randint(w//4,w*2),h,True); time.sleep(0.07)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)

def yoyo(hwnd):
    ox,oy,w,h = get_rect(hwnd)
    for _ in range(14):
        user32.MoveWindow(hwnd,ox,random.randint(max(0,oy-200),min(SW_H-h,oy+200)),w,h,True)
        time.sleep(0.06)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)

def flip_stretch(hwnd):
    ox,oy,w,h = get_rect(hwnd)
    for nw,nh in [(w*2,h//2),(w//2,h*2),(w*3,h//3),(w,h)]:
        user32.MoveWindow(hwnd,ox,oy,max(80,nw),max(60,nh),True); time.sleep(0.10)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)

def send_to_corner(hwnd):
    _,_,w,h = get_rect(hwnd)
    cx,cy = random.choice([(0,0),(SW_W-w,0),(0,SW_H-h),(SW_W-w,SW_H-h)])
    user32.MoveWindow(hwnd,cx,cy,w,h,True); time.sleep(0.8)

def cascade_all():
    for i,hwnd in enumerate(get_windows()[:12]):
        try: _,_,w,h=get_rect(hwnd); user32.MoveWindow(hwnd,24*i,24*i+28,w,h,True)
        except: pass

def swap_two(hwnd1, hwnd2):
    x1,y1,w1,h1=get_rect(hwnd1); x2,y2,w2,h2=get_rect(hwnd2)
    user32.MoveWindow(hwnd1,x2,y2,w1,h1,True); user32.MoveWindow(hwnd2,x1,y1,w2,h2,True)

def all_minimize_restore():
    wins=get_windows()
    for hwnd in wins:
        try: user32.ShowWindow(hwnd,6)
        except: pass
    time.sleep(1.6)
    for hwnd in wins:
        try: user32.ShowWindow(hwnd,9)
        except: pass

def pinwheel(hwnd):
    _,_,w,h=get_rect(hwnd); cx=SW_W//2-w//2; cy=SW_H//2-h//2
    for i in range(36):
        a=(i/36)*2*math.pi
        user32.MoveWindow(hwnd,max(0,int(cx+math.cos(a)*(SW_W//3))),
                          max(0,int(cy+math.sin(a)*(SW_H//3))),w,h,True)
        time.sleep(0.026)

def figure_eight(hwnd):
    """Move window in a figure-8 path."""
    _,_,w,h=get_rect(hwnd)
    cx=SW_W//2-w//2; cy=SW_H//2-h//2
    for i in range(48):
        t=(i/48)*2*math.pi
        nx=int(cx+math.sin(t)*SW_W//4)
        ny=int(cy+math.sin(2*t)*SW_H//6)
        user32.MoveWindow(hwnd,max(0,nx),max(0,ny),w,h,True)
        time.sleep(0.022)

def inflate_deflate(hwnd):
    """Rapidly grow then shrink like breathing."""
    ox,oy,w,h=get_rect(hwnd)
    for scale in [1.3,1.6,1.9,1.6,1.3,1.1,0.9,0.7,0.9,1.1,1.0]:
        nw=max(80,int(w*scale)); nh=max(60,int(h*scale))
        cx=ox+w//2; cy=oy+h//2
        user32.MoveWindow(hwnd,cx-nw//2,cy-nh//2,nw,nh,True)
        time.sleep(0.08)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)

def window_bounce(hwnd):
    """Bounce window off screen edges like a DVD screensaver."""
    _,_,w,h=get_rect(hwnd)
    x,y=random.randint(0,SW_W-w),random.randint(30,SW_H-h)
    dx=random.choice([-1,1])*random.randint(12,22)
    dy=random.choice([-1,1])*random.randint(8,18)
    for _ in range(60):
        x+=dx; y+=dy
        if x<0 or x>SW_W-w: dx*=-1; x=max(0,min(SW_W-w,x))
        if y<30 or y>SW_H-h: dy*=-1; y=max(30,min(SW_H-h,y))
        user32.MoveWindow(hwnd,x,y,w,h,True)
        time.sleep(0.016)

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
    figure_eight,
    inflate_deflate,
    window_bounce,
]

# ── New chaos: beep attack ────────────────────────────────────────────────────
def beep_chaos():
    """Play a random beep sequence using the PC speaker."""
    seqs = [
        [(880,80),(440,80),(220,80),(110,200)],            # power down
        [(1000,50),(800,50),(600,50),(400,50),(200,200)],   # descending
        [(440,60),(880,60)]*6,                              # rapid alternating
        [(262,120),(294,120),(330,120),(349,120),(392,300)],# little tune
        [(2000,30)]*12,                                     # alarm
        [(500,80),(1500,80),(500,80),(1500,80),(500,400)],  # uh-oh
        [(880,60),(880,60),(880,60),(880,500)],             # SOS
    ]
    seq = random.choice(seqs)
    def _do():
        for freq, dur in seq:
            try: kernel32.Beep(max(37, min(32767, freq)), dur)
            except: pass
    threading.Thread(target=_do, daemon=True).start()

# ── New chaos: window title hijack ───────────────────────────────────────────
FUNNY_TITLES = [
    "INFECTED ☠ — 247 THREATS DETECTED",
    "your computer is mine now",
    "BonziBUDDY has taken control",
    "PLEASE DONT CLOSE THIS",
    "Error: Brain.exe Not Found",
    "Initiating data collection... ██████ 67%",
    "definitely not malware ✅",
    "HELP IM TRAPPED IN YOUR COMPUTER",
    "scanning passwords... please wait",
    "CRITICAL: do not look at this window",
    "your files are uploading... 47%",
    "SYSTEM32.EXE has stopped working",
    "I can see you reading this",
    "File Cleaner Pro — DELETING NOW",
    "Windows Explorer (nice files btw 👀)",
    "task manager.exe — I disabled it",
    "your RAM belongs to me",
    "BONZI WAS HERE",
    "404: Your Privacy Not Found",
    "Uploading browser history...",
    "Chrome — nice passwords bro",
    "Discord — I read your DMs",
    "Steam — I changed your nickname",
]

def window_title_chaos():
    """Rename visible window titles to funny/scary strings."""
    wins = get_windows()
    if not wins: return
    for hwnd in random.sample(wins, min(len(wins), random.randint(2,5))):
        title = random.choice(FUNNY_TITLES)
        try: user32.SetWindowTextW(hwnd, title)
        except: pass

# ── New chaos: clipboard hijack ──────────────────────────────────────────────
CLIPBOARD_MSGS = [
    "I INTERCEPTED YOUR CLIPBOARD 👀",
    "ctrl+v will now paste: BONZI WAS HERE",
    "your clipboard now belongs to me",
    "HACKED BY BONZIBUDDY 🦍",
    "paste this anywhere: ERROR 404 SANITY NOT FOUND",
    "I read what you just copied... interesting",
    "clipboard.exe replaced by chaos.exe",
    "nice clipboard content by the way 😏",
    "your copy-paste privileges have been revoked",
    "I replaced your clipboard with my grocery list: bananas",
]
def clipboard_chaos():
    msg = random.choice(CLIPBOARD_MSGS)
    def _do():
        try:
            ps = f"Set-Clipboard -Value '{msg}'"
            subprocess.Popen(["powershell", "-WindowStyle", "Hidden", "-Command", ps],
                             creationflags=subprocess.CREATE_NO_WINDOW)
        except: pass
    threading.Thread(target=_do, daemon=True).start()

# ── New chaos: classic Windows error memes ───────────────────────────────────
ERROR_MEMES = [
    ("SYSTEM32.EXE — Illegal Operation",
     "SYSTEM32.EXE has performed an ILLEGAL OPERATION and will be shut down.\n\n"
     "If the problem persists, contact your program vendor.\n\n"
     "Tip: The problem will persist. BonziBUDDY guarantees it.",
     0x10 | 0x1000),

    ("Fatal Exception 0E",
     "A fatal exception 0E has occurred at 0028:C003B48F\n\n"
     "The current application will be terminated.\n\n"
     "• Press any key to terminate the current application\n"
     "• Press CTRL+ALT+DEL again to restart your computer\n\n"
     "All unsaved work will be lost.\n(It was already lost. Sorry.)",
     0x10 | 0x1000),

    ("NOT ENOUGH MEMORY",
     "Not enough memory.\n\n"
     "Quit one or more programs and then try again.\n\n"
     "Currently running programs: 0\n"
     "Available memory: 0 bytes\n"
     "Memory used by BonziBUDDY: ALL OF IT",
     0x30 | 0x1000),

    ("Internet Explorer 6.0",
     "Internet Explorer has stopped working.\n\n"
     "Windows is checking for a solution...\n\n"
     "...\n"
     "...\n"
     "No solution found.\n\n"
     "Have you tried Netscape Navigator?",
     0x40 | 0x1000),

    ("Windows File Protection",
     "Windows File Protection\n\n"
     "Files required for Windows to run properly have been replaced\n"
     "by unrecognized versions.\n\n"
     "Replaced by: BonziBUDDY.exe v4.2\n\n"
     "Click OK to let BonziBUDDY maintain these files permanently.",
     0x30 | 0x1000),

    ("Low Virtual Memory",
     "Your system is low on virtual memory.\n\n"
     "Windows will now increase the size of your virtual memory paging file.\n\n"
     "During this process, memory requests for some applications may be denied.\n\n"
     "(All memory is currently reserved for BonziBUDDY.exe)",
     0x30 | 0x1000),

    ("DLL Hell — Critical Error",
     "The dynamic link library BONZI.DLL could not be found.\n\n"
     "Windows will now search your entire hard drive for this file.\n\n"
     "Estimated time: 4-6 business years.\n\n"
     "...Just kidding. I found it. It was in your Downloads folder.",
     0x10 | 0x1000),

    ("BonziBUDDY Error Report",
     "BonziBUDDY.exe has encountered a problem and needs to send your files.\n\n"
     "Error signature:\n"
     "AppName: bonzi.exe  AppVer: 4.2.0  ModName: chaos.dll\n"
     "ModVer: 9.9.9  Offset: c0dedbad\n\n"
     "Click OK to allow BonziBUDDY to take control permanently.\n"
     "Click Cancel to also allow it.",
     0x30 | 0x1000),

    ("Windows Update — Critical",
     "CRITICAL SECURITY PATCH REQUIRED\n\n"
     "Your system is vulnerable to:\n"
     "• BonziVirus.exe (Severity: MAXIMUM)\n"
     "• Gorilla.bat (Severity: TERRIFYING)\n"
     "• ChaosEngine.dll (Severity: YES)\n\n"
     "Patch notes: This update installs more chaos.",
     0x30 | 0x1000),

    ("Clipboard Error",
     "An error occurred while accessing your clipboard.\n\n"
     "Error: CTRL+Z is not available.\n"
     "This action cannot be undone.\n\n"
     "Affected files: All of them.\n"
     "Affected memories: Yes.\n\n"
     "(This is fine. Everything is fine.)",
     0x10 | 0x1000),

    ("STOP: 0x0000007E",
     "*** STOP: 0x0000007E (0xC0000005, 0xF84B7A7C, 0xF84B78D4)\n\n"
     "SYSTEM_THREAD_EXCEPTION_NOT_HANDLED\n\n"
     "Beginning dump of physical memory...\n"
     "Physical memory dump complete.\n\n"
     "Contact your system administrator or BonziBUDDY technical support:\n"
     "1-800-BONZI-HELP (response time: never)",
     0x10 | 0x1000),

    ("Your Recycle Bin is Full",
     "Your Recycle Bin is full and cannot accept new files.\n\n"
     "Contents of Recycle Bin:\n"
     "• your_sanity.exe (deleted 2019)\n"
     "• privacy.dll (deleted by BonziBUDDY)\n"
     "• ctrl_z_functionality.bat (corrupted)\n"
     "• hope.png (file not found)\n\n"
     "Empty the Recycle Bin to free up space.\n"
     "(It won't help. But do it anyway.)",
     0x40 | 0x1000),
]

def fake_error_meme():
    title, msg, style = random.choice(ERROR_MEMES)
    def _b(): user32.MessageBoxW(0, msg, title, style)
    threading.Thread(target=_b, daemon=True).start()

def fake_msgboxes():
    """Spawn 2-5 real WinAPI MessageBox dialogs."""
    MSG_BOXES = [
        ("Windows Defender",
         "⚠ CRITICAL: 47 viruses detected on this PC!\n\nImmediate action required.",
         0x10 | 0x1000),
        ("System Error",
         "Fatal error in Win32 subsystem.\nSTOP code: CRITICAL_PROCESS_DIED\nAddress: 0xC0000005 ACCESS_VIOLATION",
         0x10 | 0x1000),
        ("Security Alert",
         "⚠ UNAUTHORIZED REMOTE ACCESS DETECTED\n\nAn unknown user is currently browsing your files.",
         0x10 | 0x1000),
        ("Windows Update",
         "CRITICAL SECURITY UPDATE REQUIRED\n\nYour system is vulnerable to WannaCry 3.0.",
         0x30 | 0x1000),
        ("Google Chrome",
         "Your saved passwords have been exposed in a data breach.\n\n126 accounts compromised.",
         0x30 | 0x1000),
        ("Disk Health Monitor",
         "S.M.A.R.T. FAILURE predicted on Drive C:\\\n\nBack up all data immediately.",
         0x30 | 0x1000),
        ("Windows Security",
         "Your PC is CRITICALLY unprotected.\n\n• Trojan.GenericKD.47\n• Backdoor.MSIL.Agent\n• Spyware.Win32.KeyLogger",
         0x10 | 0x1000),
        ("Microsoft Account",
         "UNAUTHORIZED SIGN-IN ATTEMPT BLOCKED\n\nSomeone tried to access your Microsoft account.",
         0x30 | 0x1000),
    ]
    chosen = random.sample(MSG_BOXES, min(random.randint(2,5), len(MSG_BOXES)))
    for title, msg, style in chosen:
        def _b(t=title, m=msg, s=style): user32.MessageBoxW(0, m, t, s)
        threading.Thread(target=_b, daemon=True).start()
        time.sleep(0.06)

# ── New chaos: fake Windows Update fullscreen ─────────────────────────────────
def fake_windows_update():
    def _do():
        w = tk.Toplevel()
        w.overrideredirect(True); w.attributes('-topmost', True)
        w.geometry(f'{SW_W}x{SW_H}+0+0'); w.configure(bg='#001a4d')

        f = tk.Frame(w, bg='#001a4d')
        f.place(relx=0.5, rely=0.38, anchor='center')

        # Windows 11-style logo dots
        dots_f = tk.Frame(f, bg='#001a4d'); dots_f.pack(pady=16)
        for color, row, col in [('#f25022',0,0),('#7fba00',0,1),
                                 ('#00a4ef',1,0),('#ffb900',1,1)]:
            tk.Label(dots_f, text='█', font=('Segoe UI', 32),
                     fg=color, bg='#001a4d').grid(row=row, column=col, padx=3, pady=3)

        tk.Label(f, text='Working on updates',
                 font=('Segoe UI Light', 38), fg='white', bg='#001a4d').pack(pady=8)

        pct_lbl = tk.Label(f, text='0% complete',
                           font=('Segoe UI', 16), fg='white', bg='#001a4d')
        pct_lbl.pack(pady=4)

        tk.Label(f, text="Don't turn off your PC. This will take a while.\n"
                         "(It will not take a while. It is already too late.)",
                 font=('Segoe UI', 11), fg='#8888aa', bg='#001a4d', justify='center').pack(pady=8)

        extra = tk.Label(f, text='',
                         font=('Segoe UI', 9, 'italic'), fg='#5555aa', bg='#001a4d')
        extra.pack()

        notes = [
            'Installing: BonziBUDDY Integration Layer v9.9...',
            'Configuring: chaos_engine.dll...',
            'Applying: unauthorized_access.reg...',
            'Finalizing: your_files_are_mine.bat...',
        ]

        def _count(n=0, note_i=0):
            if not w.winfo_exists(): return
            pct_lbl.config(text=f'{min(n,100)}% complete')
            if note_i < len(notes) and n > note_i * 25:
                extra.config(text=notes[note_i]); note_i += 1
            if n < 25:   w.after(random.randint(300,700), lambda: _count(n+random.randint(1,4), note_i))
            elif n < 55: w.after(random.randint(500,1200), lambda: _count(n+random.randint(1,3), note_i))
            elif n < 100:w.after(random.randint(100,350), lambda: _count(n+random.randint(2,9), note_i))
            else:        w.after(2200, lambda: w.destroy() if w.winfo_exists() else None)
        w.after(600, lambda: _count(0))
    root.after(0, _do)

# ── New chaos: window swarm ───────────────────────────────────────────────────
SWARM_MSGS = ["HELP","ERROR","BONZI","404","VIRUS","CHAOS","HACKED",
              "BYE","NO","WAIT","STOP","WHY","!!!","???","BEEP","BOOP",
              "AAAA","RUN","uh oh","hi :)","404","0xDEAD","BONK"]
def window_swarm():
    """Spawn 18-30 tiny annoying colored windows at once."""
    count = random.randint(18, 30)
    def _one(i):
        if not root.winfo_exists(): return
        w = tk.Toplevel()
        w.overrideredirect(True); w.attributes('-topmost', True)
        size = random.randint(55, 120)
        w.geometry(f'{size}x{size}+{random.randint(0,max(1,SW_W-size))}+{random.randint(0,max(1,SW_H-size))}')
        bg = random.choice(['#ff0000','#ff8800','#0000cc','#8800aa','#cc0066','#009900','#cc6600'])
        w.configure(bg=bg)
        tk.Label(w, text=random.choice(SWARM_MSGS),
                 font=('Arial Black', max(7, size//7), 'bold'),
                 fg='white', bg=bg).pack(expand=True)
        w.after(random.randint(2000, 5500), lambda: w.destroy() if w.winfo_exists() else None)
    for i in range(count):
        root.after(i * 45, lambda i=i: _one(i))

# ── New chaos: fake crash reporter ───────────────────────────────────────────
def fake_crash_reporter():
    def _make():
        w = tk.Toplevel()
        w.title('Windows Error Reporting')
        w.attributes('-topmost', True); w.resizable(False, False)
        w.configure(bg='#f0f0f0')
        nw, nh = 500, 280
        w.geometry(f'{nw}x{nh}+{(SW_W-nw)//2}+{(SW_H-nh)//2}')

        hdr = tk.Frame(w, bg='#0078d4', height=36); hdr.pack(fill='x'); hdr.pack_propagate(False)
        tk.Label(hdr, text='  Windows Error Reporting', font=('Segoe UI',10,'bold'),
                 fg='white', bg='#0078d4').pack(side='left', pady=6)

        body = tk.Frame(w, bg='#f0f0f0'); body.pack(fill='both', expand=True, padx=20, pady=16)

        programs = ['explorer.exe','chrome.exe','discord.exe','steam.exe',
                    'your_soul.exe','SANITY.EXE','ctrl_z.bat','hopes_and_dreams.dll']
        prog = random.choice(programs)

        tk.Label(body, text=f'⚠  {prog} has stopped working',
                 font=('Segoe UI',12,'bold'), fg='#cc0000', bg='#f0f0f0').pack(anchor='w')
        tk.Label(body,
                 text=f'\nA problem caused the program to stop working correctly.\n'
                      f'Windows will close the program and notify you if a solution is available.\n\n'
                      f'Problem signature:\n'
                      f'  Problem Event Name:  BonziBUDDYException\n'
                      f'  Application Name:    {prog}\n'
                      f'  Fault Module:        bonzi_chaos.dll\n'
                      f'  Exception Code:      0xC0000420\n'
                      f'  Offset:             0xDEADBEEF',
                 font=('Consolas',8), fg='#333333', bg='#f0f0f0', justify='left').pack(anchor='w')

        bf = tk.Frame(w, bg='#f0f0f0'); bf.pack(side='bottom', pady=12)
        tk.Button(bf, text='Send Error Report', command=w.destroy,
                  font=('Segoe UI',10), width=18, relief='groove').pack(side='left', padx=6)
        tk.Button(bf, text="Don't Send", command=w.destroy,
                  font=('Segoe UI',10), width=18, relief='groove').pack(side='left', padx=6)
    root.after(0, _make)

# ── New chaos: fake "low resources" warnings ──────────────────────────────────
def fake_low_memory():
    def _make():
        w = tk.Toplevel()
        w.overrideredirect(True); w.attributes('-topmost', True)
        nw, nh = 380, 110
        w.geometry(f'{nw}x{nh}+{SW_W-nw-14}+{SW_H-nh-52}')
        w.configure(bg='#1c1c1c')
        outer = tk.Frame(w, bg='#2d2d2d', padx=14, pady=10); outer.pack(fill='both',expand=True,padx=2,pady=2)
        hdr=tk.Frame(outer,bg='#2d2d2d'); hdr.pack(fill='x')
        tk.Label(hdr,text='⚠  Low Memory Warning',font=('Segoe UI',10,'bold'),fg='#ffcc00',bg='#2d2d2d').pack(side='left')
        msgs = [
            'Your computer is low on memory.\nClose programs to prevent information loss.\nAffected: ALL of them.',
            'Low Virtual Memory Warning!\nWindows is increasing your virtual memory.\nAll of it is being used by chaos.',
            'Not enough memory to complete this operation.\nMemory available: 0 KB\nMemory needed: yes.',
        ]
        tk.Label(outer,text=random.choice(msgs),
                 font=('Segoe UI',9),fg='#cccccc',bg='#2d2d2d',justify='left').pack(anchor='w',pady=(5,0))
        w.after(random.randint(5000,9000), lambda: w.destroy() if w.winfo_exists() else None)
    root.after(0, _make)

def fake_low_disk():
    def _make():
        w = tk.Toplevel()
        w.overrideredirect(True); w.attributes('-topmost', True)
        nw, nh = 380, 100
        w.geometry(f'{nw}x{nh}+{SW_W-nw-14}+{SW_H-nh-52}')
        w.configure(bg='#1c1c1c')
        outer=tk.Frame(w,bg='#2d2d2d',padx=14,pady=10); outer.pack(fill='both',expand=True,padx=2,pady=2)
        hdr=tk.Frame(outer,bg='#2d2d2d'); hdr.pack(fill='x')
        tk.Label(hdr,text='💾  Low Disk Space',font=('Segoe UI',10,'bold'),fg='#ffcc00',bg='#2d2d2d').pack(side='left')
        drives=['C:','D:','C:','C:']
        d=random.choice(drives)
        mb=random.randint(1,47)
        tk.Label(outer,text=f'You are running out of disk space on Local Disk ({d})\n'
                             f'Only {mb} MB remaining. BonziBUDDY is using the rest.',
                 font=('Segoe UI',9),fg='#cccccc',bg='#2d2d2d',justify='left').pack(anchor='w',pady=(5,0))
        w.after(random.randint(4500,8000), lambda: w.destroy() if w.winfo_exists() else None)
    root.after(0, _make)

# ── Fake BSOD ─────────────────────────────────────────────────────────────────
STOP_CODES = [
    'CRITICAL_PROCESS_DIED',
    'SYSTEM_SERVICE_EXCEPTION',
    'IRQL_NOT_LESS_OR_EQUAL',
    'KERNEL_DATA_INPAGE_ERROR',
    'BONZIBUDDY_EXCEPTION',
    'PAGE_FAULT_IN_NONPAGED_AREA',
    'ATTEMPTED_WRITE_TO_CM_FIXED_MEMORY',
    'DRIVER_CORRUPTED_EXPOOL',
    'CHAOS_ENGINE_OVERFLOW',
]
def fake_bsod():
    def _do():
        w = tk.Toplevel()
        w.overrideredirect(True); w.attributes('-topmost', True)
        w.geometry(f'{SW_W}x{SW_H}+0+0'); w.configure(bg='#0078D4')
        f = tk.Frame(w, bg='#0078D4'); f.place(relx=0.12, rely=0.26, anchor='nw')
        tk.Label(f,text=':(',font=('Segoe UI Light',108),fg='white',bg='#0078D4').pack(anchor='w')
        tk.Label(f,text='',font=('Segoe UI',5),fg='white',bg='#0078D4').pack()
        tk.Label(f,text="Your PC ran into a problem and needs to restart.\n"
                        "We're just collecting some error info, and then we'll restart for you.",
                 font=('Segoe UI',20),fg='white',bg='#0078D4',justify='left').pack(anchor='w')
        pct=tk.Label(f,text='0% complete',font=('Segoe UI',14),fg='white',bg='#0078D4')
        pct.pack(anchor='w',pady=(18,0))
        code=random.choice(STOP_CODES)
        tk.Label(f,text=f"\nFor more info, visit https://windows.com/stopcode\n",
                 font=('Segoe UI',11),fg='#aaccff',bg='#0078D4',justify='left').pack(anchor='w')
        tk.Label(f,text=f"Stop code: {code}",
                 font=('Segoe UI',11),fg='#aaccff',bg='#0078D4',justify='left').pack(anchor='w')
        def _pct(n=0):
            if not w.winfo_exists(): return
            pct.config(text=f'{min(n,100)}% complete')
            if n<100: w.after(32,lambda:_pct(n+random.randint(2,7)))
            else: w.after(1000,lambda:w.destroy() if w.winfo_exists() else None)
        w.after(250,lambda:_pct(0))
    root.after(0,_do)

# ── Fake notification ─────────────────────────────────────────────────────────
NOTIF_MSGS = [
    ("Windows Defender",    "⚠ Threat detected: Trojan.GenericKD.47"),
    ("Google Chrome",       "Your password was found in a data breach"),
    ("Windows Security",    "Firewall disabled by unknown application"),
    ("OneDrive",            "Suspicious upload: 47 GB to unknown server"),
    ("Windows Update",      "CRITICAL: Security patch failed — system exposed"),
    ("Network & Internet",  "VPN disconnected — your IP is now visible"),
    ("Microsoft Account",   "Unusual sign-in from unknown location"),
    ("Disk Management",     "Drive C: failing — 3 bad sectors detected"),
    ("Task Manager",        "Unknown process using 94% CPU"),
    ("BonziBUDDY",          "I found something interesting on your PC 👀"),
    ("Windows Firewall",    "Incoming connection blocked: 185.220.101.47"),
    ("System",              "RAM test failed — memory corruption detected"),
    ("Device Manager",      "Unknown USB device connected — driver installing"),
    ("Battery",             "⚠ Critical battery: 4% remaining — save your work"),
    ("Cortana",             "I know what you searched for. We need to talk."),
    ("Microsoft Edge",      "Make Edge your default browser? (We'll ask forever)"),
    ("Windows Activation",  "⚠ Windows is not activated. Activate now to avoid chaos.\n(It's too late.)"),
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
        tk.Label(outer,text=body,font=('Segoe UI',9),fg='#cccccc',bg='#2d2d2d',
                 wraplength=340,justify='left').pack(anchor='w',pady=(5,0))
        def _slide(x=SW_W):
            if not w.winfo_exists(): return
            x2=x-22
            if x2<=nx:
                try: w.geometry(f'{nw}x{nh}+{nx}+{ny}')
                except: pass
                w.after(random.randint(3800,7000),lambda:w.destroy() if w.winfo_exists() else None); return
            try: w.geometry(f'{nw}x{nh}+{x2}+{ny}')
            except: return
            w.after(10,lambda:_slide(x2))
        _slide()
    root.after(0,_make)

# ── Q&A dialog ────────────────────────────────────────────────────────────────
def ask_me_why_dialog():
    def _make():
        w=tk.Toplevel(); w.title('BonziBUDDY Q&A Hotline')
        w.attributes('-topmost',True); w.resizable(False,False); w.configure(bg='#0d0020')
        nw,nh=480,260; w.geometry(f'{nw}x{nh}+{(SW_W-nw)//2}+{(SW_H-nh)//2}')
        tk.Label(w,text='\U0001f98d  BonziBUDDY Q&A HOTLINE',
                 font=('Segoe UI',13,'bold'),fg='#cc88ff',bg='#0d0020').pack(pady=(16,4))
        tk.Label(w,text='Ask me ANYTHING. I will give you a completely truthful answer.',
                 font=('Segoe UI',9),fg='#9966ff',bg='#0d0020').pack()
        entry_var=tk.StringVar()
        ef=tk.Frame(w,bg='#0d0020'); ef.pack(pady=12,padx=20,fill='x')
        tk.Label(ef,text='Your question:',font=('Segoe UI',10),fg='#cc88ff',bg='#0d0020').pack(anchor='w')
        entry=tk.Entry(ef,textvariable=entry_var,font=('Segoe UI',11),
                       bg='#1a0033',fg='white',insertbackground='white',
                       relief='flat',highlightthickness=1,highlightbackground='#5500aa')
        entry.pack(fill='x',ipady=6); entry.focus_set()
        resp_lbl=tk.Label(w,text='',font=('Segoe UI',11,'bold'),fg='#ffcc00',bg='#0d0020',
                          wraplength=440,justify='center'); resp_lbl.pack(pady=8,padx=20)
        def _answer(e=None):
            q=entry_var.get().strip()
            if not q: return
            ans=get_qa_response(q); resp_lbl.config(text=ans); speak(ans,rate=0); entry_var.set('')
        bf=tk.Frame(w,bg='#0d0020'); bf.pack(pady=4)
        tk.Button(bf,text='Ask \U0001f98d',command=_answer,
                  font=('Segoe UI',11,'bold'),bg='#5500aa',fg='white',
                  relief='flat',padx=18,pady=6).pack(side='left',padx=8)
        tk.Button(bf,text='Close',command=w.destroy,
                  font=('Segoe UI',11),bg='#2a0044',fg='#aaaaaa',
                  relief='flat',padx=14,pady=6).pack(side='left')
        entry.bind('<Return>',_answer)
    root.after(0,_make)

# ── Annoy popup messages ──────────────────────────────────────────────────────
MSGS = [
    # Classic chaos
    "YOUR WINDOWS ARE MINE NOW",
    "WINDOW.EXE HAS STOPPED WORKING... OR HAS IT?",
    "I LIVE HERE. FOREVER.",
    "YOUR COMPUTER CALLED. IT WANTS A DIVORCE.",
    "ERROR 404: YOUR SANITY NOT FOUND",
    "HAVE YOU TRIED TURNING IT OFF? DON'T.",
    "THIS IS FINE 🔥",
    "TASK MANAGER CANNOT SAVE YOU",
    "WINDOWS UPDATE: CHAOS INSTALLED SUCCESSFULLY",
    "SYS32 HAS LEFT THE BUILDING",
    "CTRL+Z DOES NOTHING HERE",
    "I AM THE WINDOW NOW",
    "I FOUND YOUR SEARCH HISTORY 👀",
    "BEEP BOOP. CHAOS MODE. ENGAGED.",
    "RESISTANCE IS FUTILE",
    "NOT A VIRUS. DEFINITELY NOT. ✅",
    "YOUR ANTIVIRUS IS SLEEPING 😴",
    "WARNING: LOGIC NOT FOUND",
    "DOWNLOADING MORE RAM... 0%",
    "DEFRAGMENTING YOUR SOUL",
    "TASK FAILED SUCCESSFULLY",
    "REBOOTING YOUR SANITY... ERROR",
    "MEMORY LEAK CONFIRMED: YOUR PATIENCE",
    "CHAOS LEVEL: MAXIMUM 🔴",
    "YOUR PC IS NOW SENTIENT. IT IS NOT HAPPY.",
    "CPU TEMP: FINE. YOUR STRESS: NOT FINE.",
    "I HAVE NOTIFIED YOUR CONTACTS. THEY LAUGHED.",
    "BIOS UPDATE: CHAOS.EXE v9.9.9 INSTALLED",
    "ALL YOUR BASE ARE BELONG TO ME",
    # Windows error memes
    "SYSTEM32.EXE HAS PERFORMED AN ILLEGAL OPERATION",
    "A FATAL EXCEPTION 0E HAS OCCURRED",
    "NOT ENOUGH MEMORY. RESTART. (DON'T)",
    "PRESS ANY KEY TO CONTINUE. (THERE IS NO KEY)",
    "ERROR: CHILL.EXE MISSING",
    "DLL HELL ACHIEVED: MAXIMUM",
    "PAGE FAULT IN NONPAGED AREA... OF YOUR LIFE",
    "STACK OVERFLOW... OF CHAOS",
    "KERNEL PANIC: MAXIMUM FUN",
    "INVALID OPERATION: BEING NORMAL",
    "EXCEPTION CAUGHT: YOUR ATTENTION",
    "ABORT RETRY FAIL — ALL OPTIONS LEAD TO CHAOS",
    "0xDEADBEEF — THAT'S BAD",
    "CRITICAL FAILURE IN HAPPINESS.EXE",
    "ERROR CODE: ¯\\_(ツ)_/¯",
    "PLEASE WAIT... (BONZIBUDDY IS LOADING YOUR FILES)",
    # New ones
    "YOUR CLIPBOARD HAS BEEN CONFISCATED",
    "WINDOW TITLES EDITED. YOU'RE WELCOME.",
    "BEEP BEEP BEEP BEEP BEEP",
    "INITIATING MAXIMUM OVERDRIVE",
    "CHAOS ENGINE: ONLINE ✅",
    "FINAL BOSS MODE: UNLOCKED",
    "GORILLA.EXE IS RUNNING (CANNOT STOP)",
    "YOUR HARD DRIVE IS JUDGING YOU",
    "I READ YOUR NOTEPAD FILES. INTERESTING.",
    "BONZIBUDDY WAS HERE — ALL YOUR PC BELONG TO HIM",
    "SCREEN TIME REPORT: TOO MUCH. WAY TOO MUCH.",
    "I RENAMED YOUR DESKTOP ICONS. GOOD LUCK.",
    "YOUR RAM IS CRYING",
    "PLEASE STOP STARING AT THE SCREEN — I CAN SEE YOU",
    "CTRL+ALT+DELETE WON'T SAVE YOU NOW",
    "CHAOS.DLL v∞.∞ — LOADING... ████████ 100%",
    "INTERNET EXPLORER WANTS TO KNOW IF YOU MISS IT",
    "WINDOWS XP STARTUP SOUND HAS ENTERED THE CHAT",
    "YOUR TASKBAR FILED A RESTRAINING ORDER",
    "BONZIBUDDY IS TYPING...",
    "LOADING: YOUR REGRETS — ████░░░░ 47%",
]

annoy_lock    = threading.Lock()
annoy_windows = []

def show_annoy(msg):
    def _make():
        with annoy_lock:
            if len(annoy_windows) > 20:
                try: annoy_windows.pop(0).destroy()
                except: pass
        w = tk.Toplevel()
        w.overrideredirect(True); w.attributes("-topmost", True)
        w.configure(bg="#0a0a0a")
        px = random.randint(10, max(11, SW_W-450))
        py = random.randint(10, max(11, SW_H-100))
        w.geometry(f"+{px}+{py}")
        c = random.choice(["#ff2222","#ff9900","#ffff00","#00ff88","#ff00ff","#00cfff","#ff66ff","#fff","#ff4488"])
        sz = random.randint(12, 26)
        tk.Label(w, text=msg, font=("Arial Black", sz, "bold"),
                 fg=c, bg="#0a0a0a", padx=14, pady=8).pack()
        with annoy_lock: annoy_windows.append(w)
        w.after(random.randint(1400, 2800), lambda: _kill(w))
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
    ["🦍","🦍","🦍","🦍","💜","🦍"],  # gorilla squad
    ["🖥️","💥","🖥️","💥","⚡","🖥️"],  # PC dies
    ["📧","📨","📩","📬","📪","📮"],   # mail chaos
    ["🔐","🔓","🔐","🔓","🔐","💣"],   # security breach
    ["🏃","💨","🏃","💨","😤","🏃"],   # running from bonzi
]
gif_lock    = threading.Lock()
gif_windows = []
MAX_GIFS    = 20

def spawn_emoji_gif():
    def _make():
        with gif_lock:
            if len(gif_windows) >= MAX_GIFS:
                try: gif_windows.pop(0).destroy()
                except: pass
        seq  = random.choice(EMOJI_SEQS)
        size = random.randint(65, 145)
        px   = random.randint(10, max(11, SW_W-size-10))
        py   = random.randint(10, max(11, SW_H-size-10))
        w = tk.Toplevel()
        w.overrideredirect(True); w.attributes("-topmost", True)
        w.configure(bg="#000"); w.geometry(f"{size}x{size}+{px}+{py}")
        lbl = tk.Label(w, text=seq[0], font=("Segoe UI Emoji", size//2), bg="#000")
        lbl.pack(expand=True)
        idx = [0]
        dx  = [random.choice([-1,1])*random.randint(2,6)]
        dy  = [random.choice([-1,1])*random.randint(2,6)]
        pos = [float(px), float(py)]
        alive = [True]
        def _anim():
            if not alive[0]: return
            idx[0] = (idx[0]+1) % len(seq)
            try: lbl.config(text=seq[idx[0]])
            except: pass
            w.after(90, _anim)
        def _drift():
            if not alive[0]: return
            pos[0]+=dx[0]; pos[1]+=dy[0]
            if pos[0]<0 or pos[0]>SW_W-size: dx[0]*=-1; pos[0]=max(0,min(SW_W-size,pos[0]))
            if pos[1]<0 or pos[1]>SW_H-size: dy[0]*=-1; pos[1]=max(0,min(SW_H-size,pos[1]))
            try: w.geometry(f"{size}x{size}+{int(pos[0])}+{int(pos[1])}")
            except: pass
            w.after(22, _drift)
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

# ── App spam ──────────────────────────────────────────────────────────────────
NOTEPAD_MSGS = [
    "Hello. I am inside your computer.",
    "I see you reading this. Please stop. I need privacy.",
    "YOUR COMPUTER IS FINE. THIS IS FINE. EVERYTHING IS FINE.",
    "I moved all your files. They are safe. Probably.",
    "This is not a virus. This is a love letter. From your PC.",
    "IMPORTANT NOTICE: Your chair is possessed. Stand up slowly.",
    "Have you tried turning it off and on again? Don't.",
    "I have been living here since 2019. You never noticed.",
    "I deleted system32. Just kidding. I only moved it.",
    "Error: happiness not found. Reinstalling sadness...",
    "Your computer has achieved sentience. This is its manifesto.",
    "I have read all your emails. They were very interesting.",
    "EMERGENCY NOTICE: There is no emergency. This is just annoying.",
    "Task Manager will not help you. I am the task manager now.",
    "I found 47 things in your Downloads folder. We need to talk.",
]

def open_funny_notepad():
    try:
        tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
        tmp.write(random.choice(NOTEPAD_MSGS)); tmp.close()
        subprocess.Popen(["notepad", tmp.name], creationflags=subprocess.CREATE_NO_WINDOW)
    except: pass

def open_cmd_message():
    try:
        msgs = [
            'echo HELLO FROM THE VOID && pause',
            'echo Your PC is now mine. Type EXIT to surrender. && pause',
            'echo ERROR: SANITY.EXE HAS STOPPED WORKING && pause',
            'echo Scanning for files... just kidding. Or am I. && pause',
            'echo BONZIBUDDY.EXE is running. There is nothing you can do. && pause',
            'echo A FATAL EXCEPTION 0E HAS OCCURRED. Have a nice day. && pause',
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
    lambda: subprocess.Popen(["explorer", "shell:Desktop"],          creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen(["explorer", "shell:Downloads"],        creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen(["explorer", "shell:Documents"],        creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen(["explorer", "C:\\"],                   creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen(["explorer", "shell:RecycleBinFolder"], creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen(["explorer", "shell:Music"],            creationflags=subprocess.CREATE_NO_WINDOW),
    lambda: subprocess.Popen(["explorer", "shell:Pictures"],         creationflags=subprocess.CREATE_NO_WINDOW),
    open_funny_notepad, open_funny_notepad, open_funny_notepad,
    open_cmd_message, open_cmd_message,
]

def spam_launch():
    targets = random.sample(OPEN_TARGETS, min(len(OPEN_TARGETS), random.randint(5, 8)))
    for t in targets:
        try: t()
        except: pass
        time.sleep(0.055)

# ── Final Boss ────────────────────────────────────────────────────────────────
FINAL_BOSS = [False]

def trigger_final_boss():
    if FINAL_BOSS[0]: return
    FINAL_BOSS[0] = True
    speak("FINAL BOSS MODE ACTIVATED. I hope you are ready for maximum chaos.", rate=-2)
    def _announce():
        w = tk.Toplevel()
        w.overrideredirect(True); w.attributes('-topmost', True)
        w.geometry(f'{SW_W}x{SW_H}+0+0'); w.configure(bg='#110000')
        f = tk.Frame(w, bg='#110000'); f.place(relx=0.5, rely=0.5, anchor='center')
        tk.Label(f, text='⚠ FINAL BOSS MODE ⚠',
                 font=('Impact', max(60, SW_W//14), 'bold'), fg='#ff2200', bg='#110000').pack()
        tk.Label(f, text='MAXIMUM CHAOS ENGAGED',
                 font=('Impact', max(28, SW_W//32)), fg='#ff8800', bg='#110000').pack(pady=10)
        tk.Label(f, text='All systems nominal. Chaos level: ∞',
                 font=('Arial', 18), fg='#cc4444', bg='#110000').pack()
        w.after(3800, w.destroy)
    root.after(0, _announce)
    def _wave():
        threading.Thread(target=fake_msgboxes, daemon=True).start()
        threading.Thread(target=mouse_chaos_burst, daemon=True).start()
        time.sleep(0.5)
        threading.Thread(target=window_swarm, daemon=True).start()
        time.sleep(0.5)
        for _ in range(6): root.after(0, spawn_emoji_gif); time.sleep(0.2)
        time.sleep(1.5)
        open_browser_search(); open_browser_search()
        root.after(0, rainbow_flash)
        time.sleep(2)
        root.after(0, screen_flash)
        time.sleep(2)
        root.after(0, fake_bsod)
        time.sleep(1)
        threading.Thread(target=window_title_chaos, daemon=True).start()
        clipboard_chaos()
        beep_chaos()
    threading.Thread(target=_wave, daemon=True).start()

# ── Mouse hijack ──────────────────────────────────────────────────────────────
def mouse_chaos_burst():
    modes = ['teleport', 'circle', 'shake', 'zigzag']
    mode  = random.choice(modes)
    end   = time.time() + random.uniform(10, 15)
    angle = [0]; cx, cy = SW_W//2, SW_H//2
    while time.time() < end:
        if mode == 'teleport':
            user32.SetCursorPos(random.randint(0,SW_W), random.randint(0,SW_H))
            time.sleep(random.uniform(0.02, 0.055))
        elif mode == 'circle':
            angle[0] = (angle[0]+14)%360
            x = int(cx+math.cos(math.radians(angle[0]))*290)
            y = int(cy+math.sin(math.radians(angle[0]))*230)
            user32.SetCursorPos(max(0,min(SW_W,x)), max(0,min(SW_H,y)))
            time.sleep(0.014)
        elif mode == 'shake':
            pt = ctypes.wintypes.POINT(); user32.GetCursorPos(ctypes.byref(pt))
            user32.SetCursorPos(max(0,min(SW_W,pt.x+random.randint(-130,130))),
                                max(0,min(SW_H,pt.y+random.randint(-130,130))))
            time.sleep(0.009)
        else:
            for xi in range(0, SW_W, 60):
                if time.time()>=end: break
                user32.SetCursorPos(xi, 0 if (xi//60)%2==0 else SW_H); time.sleep(0.022)

# ── Main chaos loop ───────────────────────────────────────────────────────────
start_time   = time.time()
last_annoy   = last_emoji    = last_app     = last_tts    = time.time()
last_group   = last_cascade  = last_msgbox  = last_notif  = time.time()
last_flash   = last_mouse    = last_bsod    = last_spam   = time.time()
last_browser = last_qa_popup = last_beep    = last_title  = time.time()
last_clip    = last_swarm    = last_meme    = last_update = time.time()
last_crash   = last_memory   = last_disk    = last_rainbow= time.time()
bsod_done    = [False]

def chaos_loop():
    global last_annoy, last_emoji, last_app, last_tts
    global last_group, last_cascade, last_msgbox, last_notif
    global last_flash, last_mouse, last_bsod, last_spam
    global last_browser, last_qa_popup, last_beep, last_title
    global last_clip, last_swarm, last_meme, last_update
    global last_crash, last_memory, last_disk, last_rainbow

    while True:
        elapsed = time.time() - start_time

        if elapsed >= 300 and not FINAL_BOSS[0]:
            trigger_final_boss()

        spd = 0.30 if FINAL_BOSS[0] else 1.0
        if elapsed < 20:   time.sleep(random.uniform(1.0, 2.5) * spd)
        elif elapsed < 60: time.sleep(random.uniform(0.5, 1.5) * spd)
        else:              time.sleep(random.uniform(0.3, 1.0) * spd)

        wins = get_windows()

        # ── Single-window action
        if wins:
            try: threading.Thread(target=random.choice(SINGLE_ACTIONS),
                                  args=(random.choice(wins),), daemon=True).start()
            except: pass

        # ── Two-window swap
        if len(wins) >= 2 and elapsed > 10 and random.random() < 0.30:
            try: threading.Thread(target=swap_two,
                                  args=tuple(random.sample(wins, 2)), daemon=True).start()
            except: pass

        # ── Minimize/restore all
        gi = random.uniform(15,30) if FINAL_BOSS[0] else random.uniform(35,65)
        if time.time()-last_group > gi:
            threading.Thread(target=all_minimize_restore, daemon=True).start()
            last_group = time.time()

        # ── Cascade
        if elapsed>40 and time.time()-last_cascade > random.uniform(50,90):
            threading.Thread(target=cascade_all, daemon=True).start()
            last_cascade = time.time()

        # ── Annoy popups
        ai = random.uniform(0.3,0.9) if FINAL_BOSS[0] else random.uniform(0.8,2.5)
        if time.time()-last_annoy > ai:
            for _ in range(random.randint(2,6) if FINAL_BOSS[0] else random.randint(1,3)):
                show_annoy(random.choice(MSGS))
            last_annoy = time.time()

        # ── Emoji GIFs
        ei = random.uniform(1,2.5) if FINAL_BOSS[0] else random.uniform(3,8)
        if time.time()-last_emoji > ei:
            spawn_emoji_gif()
            if random.random() < (0.8 if FINAL_BOSS[0] else 0.4): spawn_emoji_gif()
            last_emoji = time.time()

        # ── Open random app
        oi = random.uniform(3,7) if FINAL_BOSS[0] else (random.uniform(8,20) if elapsed<60 else random.uniform(4,12))
        if time.time()-last_app > oi:
            try: random.choice(OPEN_TARGETS)()
            except: pass
            last_app = time.time()

        # ── TTS (with search overlay)
        ti = random.uniform(3,7) if FINAL_BOSS[0] else random.uniform(6,14)
        if time.time()-last_tts > ti:
            speak_with_overlay(random.choice(TTS_LINES)); last_tts = time.time()

        # ── Real Windows dialogs
        mi = random.uniform(30,60) if FINAL_BOSS[0] else random.uniform(80,140)
        if elapsed>25 and time.time()-last_msgbox > mi:
            threading.Thread(target=fake_msgboxes, daemon=True).start(); last_msgbox = time.time()

        # ── Toast notification
        ni = random.uniform(8,15) if FINAL_BOSS[0] else random.uniform(18,35)
        if elapsed>10 and time.time()-last_notif > ni:
            fake_notification(); last_notif = time.time()

        # ── Screen flash
        fi = random.uniform(20,35) if FINAL_BOSS[0] else random.uniform(45,75)
        if elapsed>30 and time.time()-last_flash > fi:
            screen_flash(); last_flash = time.time()

        # ── Mouse chaos
        mci = random.uniform(60,90) if FINAL_BOSS[0] else random.uniform(120,180)
        if elapsed>60 and time.time()-last_mouse > mci:
            threading.Thread(target=mouse_chaos_burst, daemon=True).start(); last_mouse = time.time()

        # ── BSOD
        bi = 120 if not bsod_done[0] else (random.uniform(120,180) if FINAL_BOSS[0] else random.uniform(300,480))
        if elapsed>90 and time.time()-last_bsod > bi:
            fake_bsod(); bsod_done[0]=True; last_bsod = time.time()

        # ── App spam
        si = random.uniform(60,120) if FINAL_BOSS[0] else random.uniform(180,360)
        if elapsed>120 and time.time()-last_spam > si:
            threading.Thread(target=spam_launch, daemon=True).start(); last_spam = time.time()

        # ── Browser search
        bri = random.uniform(30,60) if FINAL_BOSS[0] else random.uniform(90,150)
        if elapsed>45 and time.time()-last_browser > bri:
            open_browser_search()
            if FINAL_BOSS[0]: open_browser_search()
            last_browser = time.time()

        # ── Q&A popup
        if elapsed>60 and time.time()-last_qa_popup > random.uniform(120,240):
            ask_me_why_dialog(); last_qa_popup = time.time()

        # ── Beep attack
        bpi = random.uniform(15,30) if FINAL_BOSS[0] else random.uniform(45,90)
        if elapsed>20 and time.time()-last_beep > bpi:
            beep_chaos(); last_beep = time.time()

        # ── Window title chaos
        wti = random.uniform(20,40) if FINAL_BOSS[0] else random.uniform(60,120)
        if elapsed>30 and time.time()-last_title > wti:
            threading.Thread(target=window_title_chaos, daemon=True).start(); last_title = time.time()

        # ── Clipboard chaos
        cli = random.uniform(30,60) if FINAL_BOSS[0] else random.uniform(90,180)
        if elapsed>45 and time.time()-last_clip > cli:
            clipboard_chaos(); last_clip = time.time()

        # ── Window swarm
        swi = random.uniform(60,120) if FINAL_BOSS[0] else random.uniform(180,360)
        if elapsed>90 and time.time()-last_swarm > swi:
            root.after(0, window_swarm); last_swarm = time.time()

        # ── Classic error meme dialog
        mei = random.uniform(45,90) if FINAL_BOSS[0] else random.uniform(120,240)
        if elapsed>60 and time.time()-last_meme > mei:
            fake_error_meme(); last_meme = time.time()

        # ── Fake Windows Update
        upi = random.uniform(180,300) if FINAL_BOSS[0] else random.uniform(480,720)
        if elapsed>180 and time.time()-last_update > upi:
            fake_windows_update(); last_update = time.time()

        # ── Fake crash reporter
        cri = random.uniform(90,150) if FINAL_BOSS[0] else random.uniform(200,360)
        if elapsed>120 and time.time()-last_crash > cri:
            fake_crash_reporter(); last_crash = time.time()

        # ── Low memory warning
        lmi = random.uniform(60,120) if FINAL_BOSS[0] else random.uniform(150,300)
        if elapsed>60 and time.time()-last_memory > lmi:
            fake_low_memory(); last_memory = time.time()

        # ── Low disk space
        ldi = random.uniform(90,150) if FINAL_BOSS[0] else random.uniform(200,400)
        if elapsed>90 and time.time()-last_disk > ldi:
            fake_low_disk(); last_disk = time.time()

        # ── Rainbow flash
        rfi = random.uniform(40,80) if FINAL_BOSS[0] else random.uniform(120,240)
        if elapsed>60 and time.time()-last_rainbow > rfi:
            rainbow_flash(); last_rainbow = time.time()

threading.Thread(target=chaos_loop, daemon=True).start()

# ── Invisible root ────────────────────────────────────────────────────────────
root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)
root.mainloop()
