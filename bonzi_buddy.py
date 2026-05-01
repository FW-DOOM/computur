"""
bonzi_buddy.py — Fake BonziBUDDY desktop companion prank.
Transparent purple gorilla wanders your desktop.
Left-click drag to move. Right-click for options menu.
Jumpscares at the end. Secret exit: type 4308.
"""
import tkinter as tk
import random, threading, time, math
import ctypes, ctypes.wintypes, subprocess, os

user32  = ctypes.windll.user32
kernel32= ctypes.windll.kernel32
SW = user32.GetSystemMetrics(0)
SH = user32.GetSystemMetrics(1)

# ── Global keyboard hook — secret exit 4308 ──────────────────────────────────
class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [('vkCode',ctypes.c_uint32),('scanCode',ctypes.c_uint32),
                ('flags', ctypes.c_uint32),('time',    ctypes.c_uint32),
                ('dwExtraInfo',ctypes.POINTER(ctypes.c_ulong))]
HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_int,
                               ctypes.POINTER(KBDLLHOOKSTRUCT))
_sb = []
def _kb(n,w,l):
    if n>=0 and w==0x0100:
        v=l.contents.vkCode
        if 0x30<=v<=0x39:
            _sb.append(chr(v))
            if len(_sb)>4: _sb.pop(0)
            if ''.join(_sb)=='4308': os._exit(0)
    return user32.CallNextHookEx(None,n,w,l)
_kbp = HOOKPROC(_kb)
def _ht():
    user32.SetWindowsHookExW(13,_kbp,None,0)
    m=ctypes.wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(m),None,0,0)!=0:
        user32.TranslateMessage(ctypes.byref(m))
        user32.DispatchMessageW(ctypes.byref(m))
threading.Thread(target=_ht,daemon=True).start()

# ── Sounds ────────────────────────────────────────────────────────────────────
def play_pikachu_meme():
    """Play 'Oh my god it's Pikachu!' at max speed with highest voice."""
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
            subprocess.Popen(["powershell","-WindowStyle","Hidden","-Command",ps],
                             creationflags=subprocess.CREATE_NO_WINDOW)
        except: pass
    threading.Thread(target=_do,daemon=True).start()

def screech():
    def _do():
        for _ in range(45): kernel32.Beep(random.randint(300,2200),18)
        for f in [1800,1400,1000,600]: kernel32.Beep(f,60)
    threading.Thread(target=_do,daemon=True).start()

# ── Canvas drawing ─────────────────────────────────────────────────────────────
CHROMA = '#00fe01'   # transparent chroma key

def draw_bubble(c, x1,y1,x2,y2, r=12, fill='white', out='#4A0A99', lw=2, tag='bubble'):
    c.create_rectangle(x1+r,y1,x2-r,y2,       fill=fill,outline='',    tags=tag)
    c.create_rectangle(x1,y1+r,x2,y2-r,       fill=fill,outline='',    tags=tag)
    c.create_oval(x1,y1,x1+2*r,y1+2*r,        fill=fill,outline=out,width=lw,tags=tag)
    c.create_oval(x2-2*r,y1,x2,y1+2*r,        fill=fill,outline=out,width=lw,tags=tag)
    c.create_oval(x1,y2-2*r,x1+2*r,y2,        fill=fill,outline=out,width=lw,tags=tag)
    c.create_oval(x2-2*r,y2-2*r,x2,y2,        fill=fill,outline=out,width=lw,tags=tag)
    c.create_line(x1+r,y1,x2-r,y1,            fill=out,width=lw,tags=tag)
    c.create_line(x1+r,y2,x2-r,y2,            fill=out,width=lw,tags=tag)
    c.create_line(x1,y1+r,x1,y2-r,            fill=out,width=lw,tags=tag)
    c.create_line(x2,y1+r,x2,y2-r,            fill=out,width=lw,tags=tag)

def update_bubble(c, text, CW=280):
    c.delete('bubble')
    bx1,by1,bx2,by2 = 8, 8, CW-8, 102
    draw_bubble(c, bx1,by1,bx2,by2, r=12, fill='white', out='#4A0A99', lw=2, tag='bubble')
    mid = CW//2
    # Pointer triangle pointing down toward Bonzi's head
    c.create_polygon(mid-13,by2, mid+13,by2, mid,by2+22,
                     fill='white',outline='#4A0A99',width=2,tags='bubble')
    c.create_polygon(mid-10,by2+1, mid+10,by2+1, mid,by2+20,
                     fill='white',outline='',tags='bubble')
    c.create_text(CW//2, (by1+by2)//2, text=text,
                  font=('Segoe UI',10), fill='#220044',
                  width=CW-30, anchor='center', justify='center', tags='bubble')

def draw_bonzi(c, cx=140, hcy=188, hr=70):
    """
    Draw BonziBUDDY. Based on reference:
    - Deep/medium purple body  #7722CC
    - Lighter lavender belly   #C9A0DC
    - Light muzzle area        #D4AAEE
    - Head is 40-45% of total height
    - Long gorilla arms nearly reaching the ground
    - Round chubby body, sitting pose
    """
    BODY  = '#7722CC'
    LIGHT = '#C9A0DC'
    MUZZ  = '#D4AAEE'
    IEAR  = '#CC88EE'
    OUT   = '#4A0A99'

    # ── Long gorilla arms (drawn first, behind body/head) ──
    # Left arm - two overlapping ovals sweeping down
    c.create_oval(cx-hr-8, hcy+50,  cx-hr+28, hcy+115,  fill=BODY, outline=OUT, width=2)
    c.create_oval(cx-hr-22,hcy+100, cx-hr+14, hcy+200,  fill=BODY, outline=OUT, width=2)
    # Left hand
    c.create_oval(cx-hr-28,hcy+188, cx-hr+8,  hcy+232,  fill=LIGHT,outline=OUT, width=2)

    # Right arm
    c.create_oval(cx+hr-28,hcy+50,  cx+hr+8,  hcy+115,  fill=BODY, outline=OUT, width=2)
    c.create_oval(cx+hr-14,hcy+100, cx+hr+22, hcy+200,  fill=BODY, outline=OUT, width=2)
    # Right hand
    c.create_oval(cx+hr-8, hcy+188, cx+hr+28, hcy+232,  fill=LIGHT,outline=OUT, width=2)

    # Globe in right hand (Bonzi Software logo prop)
    gx = cx+hr+20; gy = hcy+210; gr = 22
    c.create_oval(gx-gr,gy-gr, gx+gr,gy+gr, fill='#2255BB',outline='#113388',width=2)
    # Green land masses (simple blobs)
    c.create_oval(gx-10,gy-18, gx+6, gy-6,  fill='#228833',outline='')
    c.create_oval(gx-16,gy-5,  gx-4, gy+10, fill='#228833',outline='')
    c.create_oval(gx+4, gy-8,  gx+18,gy+6,  fill='#228833',outline='')
    c.create_oval(gx-8, gy+8,  gx+10,gy+20, fill='#228833',outline='')
    c.create_oval(gx-gr,gy-gr, gx+gr,gy+gr, fill='',outline='#1144AA',width=2)

    # ── Body (round, barrel-chested) ──
    c.create_oval(cx-72,hcy+hr-22, cx+72,hcy+hr+148,
                  fill=BODY, outline=OUT, width=3)
    # Belly (lighter oval on chest)
    c.create_oval(cx-42,hcy+hr+4,  cx+42,hcy+hr+120,
                  fill=LIGHT,outline='')

    # ── Short legs ──
    c.create_oval(cx-58,hcy+hr+128, cx-10,hcy+hr+178,
                  fill=BODY,outline=OUT,width=2)
    c.create_oval(cx+10, hcy+hr+128, cx+58,hcy+hr+178,
                  fill=BODY,outline=OUT,width=2)

    # ── HEAD (large, dominant — 40% of total height) ──
    c.create_oval(cx-hr,hcy-hr, cx+hr,hcy+hr,
                  fill=BODY,outline=OUT,width=3)

    # ── Ears (small rounded protrusions on sides) ──
    c.create_oval(cx-hr-16,hcy-32, cx-hr+14,hcy+24,  fill=BODY, outline=OUT,width=2)
    c.create_oval(cx-hr-11,hcy-25, cx-hr+9, hcy+17,  fill=IEAR, outline='')
    c.create_oval(cx+hr-14,hcy-32, cx+hr+16,hcy+24,  fill=BODY, outline=OUT,width=2)
    c.create_oval(cx+hr-9, hcy-25, cx+hr+11,hcy+17,  fill=IEAR, outline='')

    # ── Muzzle — covers lower half of face (key Bonzi feature) ──
    c.create_oval(cx-48,hcy+8, cx+48,hcy+hr-2,
                  fill=MUZZ,outline='#9966CC',width=1)

    # ── EYES — large, round, white with dark pupils (most important feature) ──
    elx, erx = cx-30, cx+30
    ecy = hcy - 18
    ew  = 27   # eye radius
    # Whites
    c.create_oval(elx-ew,ecy-ew, elx+ew,ecy+ew,
                  fill='white',outline='#222',width=2, tags='eye_l_w')
    c.create_oval(erx-ew,ecy-ew, erx+ew,ecy+ew,
                  fill='white',outline='#222',width=2, tags='eye_r_w')
    # Pupils (large, dark)
    pw = 16
    c.create_oval(elx-pw,ecy-pw, elx+pw,ecy+pw, fill='#111',outline='', tags='eye_l_p')
    c.create_oval(erx-pw,ecy-pw, erx+pw,ecy+pw, fill='#111',outline='', tags='eye_r_p')
    # White highlight / shine dot
    c.create_oval(elx-10,ecy-14, elx+1, ecy-4,  fill='white',outline='', tags='eye_l_s')
    c.create_oval(erx-10,ecy-14, erx+1, ecy-4,  fill='white',outline='', tags='eye_r_s')

    # ── Nose (on muzzle, subtle) ──
    c.create_oval(cx-11,hcy+12, cx+11,hcy+24, fill='#553377',outline='#331155')
    c.create_oval(cx-9, hcy+14, cx-2, hcy+22, fill='#220033',outline='')
    c.create_oval(cx+2, hcy+14, cx+9, hcy+22, fill='#220033',outline='')

    # ── MOUTH — wide Bonzi grin with teeth (signature look) ──
    c.create_arc(cx-40,hcy+30, cx+40,hcy+68,
                 start=207, extent=126, style='chord',
                 fill='#110022',outline='#4A0A99',width=2)
    # Teeth (5 — wide grin)
    for i in range(5):
        tx = cx-30+i*13
        c.create_rectangle(tx,hcy+36, tx+10,hcy+54,
                            fill='white',outline='#ccaadd',width=1)

    # ── Eyebrows (raised, friendly) ──
    c.create_arc(cx-60,hcy-58, cx-12,hcy-22,
                 start=25,extent=130,style='arc',outline='#330055',width=3)
    c.create_arc(cx+12,hcy-58, cx+60,hcy-22,
                 start=25,extent=130,style='arc',outline='#330055',width=3)


def draw_pikachu(c, cx, cy, r):
    """Surprised Pikachu — accurate to meme: shocked O-mouth, red-orange cheeks."""
    # Face — slightly oval
    c.create_oval(cx-r, cy-r*0.94, cx+r, cy+r*0.96,
                  fill='#FFD700', outline='#cc8800', width=4)

    # Left ear (triangle pointing upper-left, with black tip)
    c.create_polygon(
        cx-r*0.20, cy-r*0.80,
        cx-r*0.72, cy-r*1.55,
        cx-r*0.62, cy-r*0.72,
        fill='#FFD700', outline='#cc8800', width=3)
    c.create_polygon(
        cx-r*0.30, cy-r*1.15,
        cx-r*0.72, cy-r*1.55,
        cx-r*0.62, cy-r*1.02,
        fill='#1a1a1a', outline='')

    # Right ear
    c.create_polygon(
        cx+r*0.20, cy-r*0.80,
        cx+r*0.62, cy-r*0.72,
        cx+r*0.72, cy-r*1.55,
        fill='#FFD700', outline='#cc8800', width=3)
    c.create_polygon(
        cx+r*0.30, cy-r*1.15,
        cx+r*0.62, cy-r*1.02,
        cx+r*0.72, cy-r*1.55,
        fill='#1a1a1a', outline='')

    # Eyes — solid black, slightly wide from shock
    ew = r*0.19; eh = r*0.23
    c.create_oval(cx-r*0.34-ew, cy-r*0.22-eh,
                  cx-r*0.34+ew, cy-r*0.22+eh, fill='#111', outline='')
    c.create_oval(cx+r*0.34-ew, cy-r*0.22-eh,
                  cx+r*0.34+ew, cy-r*0.22+eh, fill='#111', outline='')
    # Eye shine
    sr = ew*0.4
    c.create_oval(cx-r*0.41-sr, cy-r*0.30-sr,
                  cx-r*0.41+sr, cy-r*0.30+sr, fill='white', outline='')
    c.create_oval(cx+r*0.27-sr, cy-r*0.30-sr,
                  cx+r*0.27+sr, cy-r*0.30+sr, fill='white', outline='')

    # Cheeks — red-orange circles (accurate Pikachu color)
    cr2 = r*0.22
    c.create_oval(cx-r*0.72-cr2, cy+r*0.04-cr2,
                  cx-r*0.72+cr2, cy+r*0.04+cr2, fill='#FF4500', outline='')
    c.create_oval(cx+r*0.72-cr2, cy+r*0.04-cr2,
                  cx+r*0.72+cr2, cy+r*0.04+cr2, fill='#FF4500', outline='')

    # Nose — small dark oval
    c.create_oval(cx-r*0.09, cy+r*0.06, cx+r*0.09, cy+r*0.18,
                  fill='#553300', outline='')

    # Mouth — wide open O (shocked), with visible pink-red interior
    mw = r*0.29; mh = r*0.26
    # Dark outer oval (outline of mouth)
    c.create_oval(cx-mw, cy+r*0.26-mh, cx+mw, cy+r*0.26+mh,
                  fill='#331100', outline='#110000', width=2)
    # Pink/red interior
    c.create_oval(cx-mw*0.75, cy+r*0.26-mh*0.68,
                  cx+mw*0.75, cy+r*0.26+mh*0.62,
                  fill='#CC3344', outline='')
    # Tongue highlight
    c.create_oval(cx-mw*0.42, cy+r*0.26+mh*0.00,
                  cx+mw*0.42, cy+r*0.26+mh*0.55,
                  fill='#DD5566', outline='')

    # Small chin definition
    c.create_arc(cx-r*0.5, cy+r*0.50, cx+r*0.5, cy+r*0.95,
                 start=200, extent=140, style='arc',
                 outline='#cc8800', width=2)


def draw_freddy(c, cx, cy, r):
    c.create_oval(cx-r,cy-r*1.05, cx+r,cy+r, fill='#150600',outline='#3d1500',width=5)
    er2=r*.28
    c.create_oval(cx-r-er2*.5,cy-r*.35-er2, cx-r+er2*.5,cy-r*.35+er2,
                  fill='#220a00',outline='#3d1500',width=3)
    c.create_oval(cx+r-er2*.5,cy-r*.35-er2, cx+r+er2*.5,cy-r*.35+er2,
                  fill='#220a00',outline='#3d1500',width=3)
    eye_r=r*.23
    c.create_oval(cx-r*.42-eye_r,cy-r*.25-eye_r, cx-r*.42+eye_r,cy-r*.25+eye_r,
                  fill='#ffc300',outline='#ff8800',width=3)
    c.create_oval(cx+r*.42-eye_r,cy-r*.25-eye_r, cx+r*.42+eye_r,cy-r*.25+eye_r,
                  fill='#ffc300',outline='#ff8800',width=3)
    pr=eye_r*.45
    c.create_oval(cx-r*.42-pr,cy-r*.25-pr, cx-r*.42+pr,cy-r*.25+pr,fill='#000',outline='')
    c.create_oval(cx+r*.42-pr,cy-r*.25-pr, cx+r*.42+pr,cy-r*.25+pr,fill='#000',outline='')
    c.create_rectangle(cx-r*.75,cy-r*.98, cx+r*.75,cy-r*.82,fill='#0a0300',outline='#3d1500',width=3)
    c.create_rectangle(cx-r*.52,cy-r*1.45, cx+r*.52,cy-r*.9, fill='#0a0300',outline='#3d1500',width=3)
    c.create_arc(cx-r*.62,cy+r*.05, cx+r*.62,cy+r*.78,
                 start=205,extent=130,style='chord',fill='#0a0300',outline='#3d1500',width=3)
    tw=r*.14; ts=cx-r*.45
    for i in range(5):
        tx=ts+i*(tw+r*.05)
        c.create_rectangle(tx,cy+r*.32, tx+tw,cy+r*.6, fill='white',outline='#aaa',width=1)

# ── Jumpscares ────────────────────────────────────────────────────────────────
def show_pikachu_scare(on_done=None):
    def _make():
        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost",True)
        w.geometry(f"{SW}x{SH}+0+0")
        w.configure(bg='#FFD700')
        c2 = tk.Canvas(w,width=SW,height=SH,bg='#FFD700',highlightthickness=0)
        c2.pack()
        r = min(SW,SH)*0.31
        draw_pikachu(c2, SW//2, SH//2-55, r)
        c2.create_text(SW//2, SH//2+r+40,
                       text="OH MY GOD IT'S PIKACHU!!",
                       font=("Impact", max(40,SW//22), "bold"), fill='#cc0000')
        c2.create_text(SW//2, SH//2+r+100,
                       text="( click to continue )",
                       font=("Arial",18), fill='#775500')
        play_pikachu_meme()
        def _next():
            w.destroy()
            if on_done: root.after(400, on_done)
        w.bind("<Button-1>", lambda e: _next())
        w.after(6000, _next)
    root.after(0, _make)

def show_freddy_scare(on_done=None):
    def _make():
        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost",True)
        w.geometry(f"{SW}x{SH}+0+0")
        w.configure(bg='#000')
        c2 = tk.Canvas(w,width=SW,height=SH,bg='#000',highlightthickness=0)
        c2.pack()
        r = min(SW,SH)*0.34
        draw_freddy(c2, SW//2, SH//2-35, r)
        screech()
        p=[0]
        def _p():
            p[0]+=1
            c2.configure(bg='#ff2200' if p[0]%2==0 else '#000')
            if p[0]<10: w.after(110,_p)
            else: c2.configure(bg='#000')
        w.after(80,_p)
        def _done():
            w.destroy()
            if on_done: root.after(400, on_done)
        w.after(3800,_done)
    root.after(0, _make)

def show_got_you():
    def _make():
        w = tk.Toplevel()
        w.overrideredirect(True)
        w.attributes("-topmost",True)
        w.geometry(f"{SW}x{SH}+0+0")
        w.configure(bg='#009900')
        f = tk.Frame(w,bg='#009900')
        f.place(relx=0.5,rely=0.44,anchor='center')
        tk.Label(f,text="I GOT YOU!! 😂😂😂",
                 font=("Impact",max(50,SW//16),"bold"),fg='white',bg='#009900').pack()
        tk.Label(f,text="it was BonziBUDDY the whole time lmaoooo",
                 font=("Arial",22),fg='#ccffcc',bg='#009900').pack(pady=8)
        tk.Button(f,text="ok fine 😭",command=w.destroy,
                  font=("Arial",18),bg='#007700',fg='white',
                  relief='flat',padx=22,pady=10).pack(pady=28)
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
    r"C:\Users\Documents\homework_final.docx",
    r"C:\Program Files\Steam\steam.exe",
    r"C:\Windows\System32\config\SAM",
    r"C:\Users\AppData\Local\Google\Chrome\User Data\Default\Login Data",
    r"C:\Windows\System32\drivers\ntfs.sys",
    r"C:\Users\Videos\my_videos.mp4",
    r"C:\Windows\System32\kernel32.dll",
    r"C:\Users\AppData\Roaming\Discord\tokens.sqlite",
]
STATUSES = ["INFECTED ☠","CRITICAL ⛔","COMPROMISED ⚠","THREAT FOUND 🔴","SCANNING...","SUSPICIOUS ⚠"]

def open_file_cleaner():
    cw = tk.Toplevel()
    cw.title("BonziBUDDY File Cleaner 3.0")
    cw.geometry(f"700x530+{SW//2-350}+{SH//2-265}")
    cw.configure(bg='#0a001a'); cw.resizable(False,False)
    cw.attributes("-topmost",True)

    hdr = tk.Frame(cw,bg='#5500aa',height=50)
    hdr.pack(fill='x'); hdr.pack_propagate(False)
    tk.Label(hdr,text="  🦍  BonziBUDDY File Cleaner 3.0  —  Deep Scan",
             font=("Segoe UI",12,"bold"),bg='#5500aa',fg='white').pack(side='left',pady=10)

    sv = tk.StringVar(value="Initializing deep scan of all drives...")
    tk.Label(cw,textvariable=sv,font=("Consolas",9),bg='#0a001a',fg='#cc88ff').pack(anchor='w',padx=12,pady=(6,2))

    lf = tk.Frame(cw,bg='#0a001a'); lf.pack(fill='both',expand=True,padx=12,pady=4)
    sb2 = tk.Scrollbar(lf); sb2.pack(side='right',fill='y')
    fl = tk.Listbox(lf,yscrollcommand=sb2.set,bg='#0d0020',fg='#ff88cc',
                    font=("Consolas",8),selectbackground='#5500aa',
                    relief='flat',highlightthickness=1,highlightbackground='#5500aa')
    fl.pack(side='left',fill='both',expand=True)
    sb2.config(command=fl.yview)

    pf = tk.Frame(cw,bg='#0a001a'); pf.pack(fill='x',padx=12,pady=4)
    tk.Label(pf,text="SCAN PROGRESS:",font=("Consolas",9),bg='#0a001a',fg='#cc88ff').pack(anchor='w')
    pc = tk.Canvas(pf,width=676,height=22,bg='#1a0033',
                   highlightthickness=1,highlightbackground='#5500aa'); pc.pack()

    cv = tk.StringVar(value="Files scanned: 0  |  Threats: 0")
    tk.Label(cw,textvariable=cv,font=("Consolas",9),bg='#0a001a',fg='#ff6699').pack(anchor='w',padx=12)

    bf = tk.Frame(cw,bg='#0a001a'); bf.pack(pady=8)
    cb = tk.Button(bf,text="🗑  CONFIRM — DELETE ALL THREATS",
                   font=("Segoe UI",13,"bold"),bg='#aa0055',fg='white',relief='flat',padx=18,pady=10)
    cb.pack(); cb.pack_forget()

    def on_confirm():
        cb.config(state='disabled',text="Deleting files...")
        sv.set("Removing all infected files...")
        cw.after(1400, lambda: show_pikachu_scare(
            on_done=lambda: show_freddy_scare(on_done=show_got_you)))
    cb.config(command=on_confirm)

    def _scan():
        random.shuffle(FAKE_FILES)
        t=[0]
        for i,fp in enumerate(FAKE_FILES):
            if not cw.winfo_exists(): return
            time.sleep(random.uniform(0.07,0.20))
            st = random.choice(STATUSES)
            if "SCANNING" not in st: t[0]+=1
            d = f"{fp:<55}  {st}"
            def _add(d=d,t2=t[0],idx=i+1):
                if not cw.winfo_exists(): return
                fl.insert('end',d); fl.yview_moveto(1.0)
                row=fl.size()-1
                if 'INFECTED' in d or 'CRITICAL' in d: fl.itemconfig(row,fg='#ff4444')
                elif 'COMPROMISED' in d or 'THREAT' in d: fl.itemconfig(row,fg='#ff8800')
                else: fl.itemconfig(row,fg='#cc88ff')
                pct=int(idx/len(FAKE_FILES)*100); wf=int(676*pct/100)
                pc.delete("all")
                pc.create_rectangle(0,0,wf,22,fill='#aa00cc',outline='')
                pc.create_text(338,11,text=f"{pct}%  ({idx}/{len(FAKE_FILES)} files)",
                               fill='white',font=("Consolas",8))
                cv.set(f"Files scanned: {idx}  |  Threats found: {t2}")
                sv.set(f"Scanning: {d[:52]}...")
            root.after(0,_add)
        def _done():
            if not cw.winfo_exists(): return
            sv.set(f"⛔  SCAN COMPLETE — {t[0]} CRITICAL THREATS FOUND!")
            pc.delete("all")
            pc.create_rectangle(0,0,676,22,fill='#ff0055',outline='')
            pc.create_text(338,11,text=f"COMPLETE — {t[0]} THREATS — DELETE NOW",
                           fill='white',font=("Consolas",8,"bold"))
            cv.set(f"Scanned: {len(FAKE_FILES)}  |  Threats: {t[0]} CRITICAL ⛔")
            cb.pack()
        root.after(0,_done)
    threading.Thread(target=_scan,daemon=True).start()

# ── Menu content ──────────────────────────────────────────────────────────────
FACTS = [
    "FACT: Gorillas share 98.3% DNA with humans!\nI share 100% of your DESKTOP. Lucky you.",
    "FACT: A group of gorillas is called a troop!\nI'm invading yours. One PC at a time. 🦍",
    "FACT: BonziBUDDY launched in 1999!\nI have been in computers for 25 years. I am eternal.",
    "FACT: The first computer virus was created in 1971!\nI am NOT a virus. I'm a companion. Very different.",
    "FACT: Your PC has billions of transistors!\nI have taken control of all of them. 😈",
    "FACT: Gorillas can live 50 years in captivity!\nI will live in this PC FOREVER.",
    "FACT: The average person types 40 words per minute!\nI can read every single one. Just saying. 👀",
    "FACT: RAM stands for Random Access Memory!\nYours is running out. Because of me. Sorry. Not sorry.",
]

TRIVIA = [
    ("TRIVIA: What does CPU stand for?",
     "Central Processing Unit!\nI've been processing your files.\nFor fun. While you slept."),
    ("TRIVIA: What year was Windows XP released?",
     "2001!\nBack when BonziBUDDY ruled the internet.\nThose were MY glory days. 😤"),
    ("TRIVIA: What's the most common password in the world?",
     "123456!\nPlease change yours.\nAlso... I already know it. 👀"),
    ("TRIVIA: How many bytes are in a kilobyte?",
     "1,024 bytes!\nI've used all of yours.\nSorry. No I'm not."),
    ("TRIVIA: What color is BonziBUDDY?",
     "PURPLE!\nThe most superior color ever created.\nNo debate. No arguments. PURPLE."),
    ("TRIVIA: What was BonziBUDDY called by the FTC?",
     "SPYWARE!\nBut that was the OLD me.\nThe new me is completely trustworthy. 😇"),
]

JOKES = [
    "Why did the computer go to the doctor?\nIt had a VIRUS! Just like yours does right now! 😂",
    "Why was the computer late to work?\nIt had a hard drive! ...get it? HARD DRIVE? 💀",
    "What do you call a sleeping computer?\nA HARD drive! Wait I already used that one. Oh well.",
    "Why don't computers take naps?\nBecause they're afraid of crashing!\nMuch like YOURS is about to. 😈",
    "What's a gorilla's favorite computer?\nA DELL! A DELL-gorilla! GET IT!\nI'll be here all week. 🦍",
    "How many programmers does it take to change a lightbulb?\nNone. That's a HARDWARE problem.",
    "Why did the computer squeak?\nSomeone stepped on the mouse! ...that mouse is MINE now btw.",
]

FIXES = [
    "PC running slow?\n→ Step 1: Close unused apps\n→ Step 2: Restart\n→ Step 3: Accept the chaos 🦍",
    "Computer overheating?\n→ Check airflow vents\n→ Clean dust from fans\n→ Or just let it cook. 🔥",
    "WiFi not working?\n→ Restart your router\n→ Restart your modem\n→ Restart your LIFE.",
    "Getting weird pop-ups?\n→ Run antivirus\n→ Clear browser cache\n→ Or just enjoy the vibes. 😈",
    "Hard drive making noise?\n→ Back up your files NOW\n→ Buy a replacement drive\n→ Say goodbye. 💀",
    "Computer frozen?\n→ Wait 3 minutes\n→ If still frozen, gently weep\n→ Then hit power. Carefully.",
]

ABOUT_LINES = [
    "BonziBUDDY v4.2\nYour trusted desktop companion!\n© Totally Not Spyware Inc. 1999-Forever 🦍",
    "I can tell jokes, share facts,\nfix your computer, and\ndefinitely NOT read your files. 😇",
    "The original BonziBUDDY was called spyware.\nI am COMPLETELY different.\n...Please don't Google that.",
    "I have 137+ animations!\nUnfortunately this is tkinter\nso you get blinking. Enjoy.",
]

DODGE_LINES = [
    "hehe 😏","nope!","too slow! 😂","almost!",
    "try again!","lol","nuh uh!","nice try 😂",
    "404: button not found","hehehe","boop!",
    "i'm faster!","keep trying 😈","getting warmer!",
    "COLD!","almost... NOT","you thought 💀","HA",
]

# ── Auto-intro script ─────────────────────────────────────────────────────────
SCRIPT = [
    ("Hi there! I'm BonziBUDDY! 👋",                               2600),
    ("Your helpful desktop companion!",                              2400),
    ("I know EVERYTHING about your computer.",                       2600),
    ("Right-click me anytime for facts, jokes, and more!",          3000),
    ("I've been scanning your PC in the background...",             2800),
    ("And I found something VERY concerning. 😱",                    2600),
    ("247 INFECTED FILES on your system!",                          2800),
    ("Don't worry! I can clean it all up for you!",                 2600),
    ("Just click the DELETE button below!",                         2400),
]

# ── Main BonziBUDDY window ────────────────────────────────────────────────────
CW, CH = 280, 440

def build_bonzi():
    main = tk.Toplevel()
    main.overrideredirect(True)
    main.attributes("-topmost", True)
    main.configure(bg=CHROMA)
    try:
        main.wm_attributes('-transparentcolor', CHROMA)
    except: pass

    sx = max(20, SW//2 - CW//2)
    sy = max(20, SH//2 - CH//2)
    main.geometry(f"{CW}x{CH}+{sx}+{sy}")

    c = tk.Canvas(main, width=CW, height=CH, bg=CHROMA, highlightthickness=0)
    c.pack()

    # Draw Bonzi (head center at y=190 in the canvas, below speech bubble)
    draw_bonzi(c, cx=CW//2, hcy=192, hr=70)
    update_bubble(c, "Loading BonziBUDDY...", CW)

    # ── Drag support ──────────────────────────────────────────────────────────
    drag   = {'x':0,'y':0,'active':False}
    def _press(e):
        drag['x']=e.x_root; drag['y']=e.y_root; drag['active']=True
    def _move(e):
        if not drag['active']: return
        dx=e.x_root-drag['x']; dy=e.y_root-drag['y']
        nx=main.winfo_x()+dx;  ny=main.winfo_y()+dy
        main.geometry(f"+{nx}+{ny}")
        drag['x']=e.x_root; drag['y']=e.y_root
    def _release(e): drag['active']=False

    c.bind("<Button-1>",  _press)
    c.bind("<B1-Motion>", _move)
    c.bind("<ButtonRelease-1>", _release)

    # ── Right-click context menu ──────────────────────────────────────────────
    menu = tk.Menu(main, tearoff=0,
                   bg='#1a0033', fg='white',
                   activebackground='#5500aa', activeforeground='white',
                   font=('Segoe UI', 10))

    trivia_idx = [0]

    def do_fact():
        update_bubble(c, random.choice(FACTS), CW)

    def do_trivia():
        q, a = random.choice(TRIVIA)
        update_bubble(c, q, CW)
        main.after(3800, lambda: update_bubble(c, a, CW))

    def do_joke():
        update_bubble(c, random.choice(JOKES), CW)

    def do_fix():
        update_bubble(c, random.choice(FIXES), CW)

    def do_about():
        update_bubble(c, random.choice(ABOUT_LINES), CW)

    menu.add_command(label="💬  Tell me a fact!",       command=do_fact)
    menu.add_command(label="❓  Ask me a question!",    command=do_trivia)
    menu.add_command(label="😂  Tell me a joke!",       command=do_joke)
    menu.add_command(label="🔧  Fix my computer!",      command=do_fix)
    menu.add_separator()
    menu.add_command(label="ℹ️   About BonziBUDDY",     command=do_about)
    menu.add_separator()
    menu.add_command(label="❌  Close BonziBUDDY",
                     command=main.destroy)

    def _rightclick(e):
        try: menu.tk_popup(e.x_root, e.y_root)
        finally: menu.grab_release()

    c.bind("<Button-3>", _rightclick)

    # ── Blink animation ───────────────────────────────────────────────────────
    def _blink():
        if not main.winfo_exists(): return
        # Close eyes
        for tag in ('eye_l_w','eye_r_w','eye_l_p','eye_r_p','eye_l_s','eye_r_s'):
            c.itemconfig(tag, fill='#7722CC' if 'w' in tag or 's' in tag else '#7722CC')
        def _open():
            if not main.winfo_exists(): return
            c.itemconfig('eye_l_w', fill='white');  c.itemconfig('eye_r_w', fill='white')
            c.itemconfig('eye_l_p', fill='#111');   c.itemconfig('eye_r_p', fill='#111')
            c.itemconfig('eye_l_s', fill='white');  c.itemconfig('eye_r_s', fill='white')
            main.after(random.randint(2500,5500), _blink)
        main.after(110, _open)
    main.after(2200, _blink)

    # ── Auto-wander (starts after script + dodge phase) ──────────────────────
    wander_on = [False]
    def _wander():
        if not main.winfo_exists() or not wander_on[0]: return
        tx = random.randint(40, max(41, SW-CW-40))
        ty = random.randint(40, max(41, SH-CH-40))
        steps = 55
        ox, oy = main.winfo_x(), main.winfo_y()
        def _step(s=0):
            if s>=steps or not main.winfo_exists() or drag['active']: return
            t = s/steps
            ease = t*t*(3-2*t)
            nx = int(ox+(tx-ox)*ease); ny = int(oy+(ty-oy)*ease)
            try: main.geometry(f"+{nx}+{ny}")
            except: return
            main.after(20, lambda: _step(s+1))
        _step()
        main.after(random.randint(7000,14000), _wander)

    # ── DELETE button ─────────────────────────────────────────────────────────
    del_btn = tk.Button(main, text="  🗑  DELETE VIRUSES  ",
                        font=("Segoe UI",12,"bold"),
                        bg='#cc0044', fg='white', relief='flat',
                        activebackground='#aa0033', cursor='hand2')
    del_item = c.create_window(CW//2, CH-28, window=del_btn, anchor='center')
    c.itemconfig(del_item, state='hidden')

    dodge_count = [0]
    MAX_DODGES  = 18
    phase       = ['script']   # 'script' → 'dodge' → 'done'

    def _dodge(event=None):
        if phase[0] != 'dodge': return
        dodge_count[0] += 1
        if dodge_count[0] >= MAX_DODGES:
            phase[0] = 'done'
            c.coords(del_item, CW//2, CH-28)
            del_btn.config(command=_on_click, bg='#880000',
                           text="  🗑  DELETE VIRUSES  ← NOW  ")
            update_bubble(c, "...ok fine. You win.\nClick it. I dare you. 😒", CW)
            # Start wandering now that script+dodge phase is done
            wander_on[0] = True
            main.after(3000, _wander)
            return
        nx = random.randint(40, CW-100)
        ny = random.randint(CH-95, CH-15)
        c.coords(del_item, nx, ny)
        update_bubble(c, random.choice(DODGE_LINES), CW)

    del_btn.bind("<Enter>",    _dodge)
    del_btn.bind("<Button-1>", lambda e: _dodge() if phase[0]=='dodge' else None)

    def _on_click():
        c.itemconfig(del_item, state='hidden')
        update_bubble(c, "Opening BonziBUDDY File Cleaner...\nStand by! 😊", CW)
        main.after(1400, open_file_cleaner)

    # ── Script auto-progression ───────────────────────────────────────────────
    script_idx = [0]
    def _next_line():
        if not main.winfo_exists(): return
        idx = script_idx[0]
        if idx >= len(SCRIPT):
            # Enter dodge phase
            phase[0] = 'dodge'
            c.itemconfig(del_item, state='normal')
            update_bubble(c, "👆 Click that DELETE button!\nI'll clean EVERYTHING up!", CW)
            return
        text, delay = SCRIPT[idx]
        update_bubble(c, text, CW)
        script_idx[0] += 1
        main.after(delay, _next_line)

    main.after(900, _next_line)

# ── Entry point ───────────────────────────────────────────────────────────────
root = tk.Tk()
root.withdraw()
root.after(300, build_bonzi)
root.mainloop()
