"""
ultimate_troll.py — THE ULTIMATE TROLLER 9000.
ALL chaos in ONE script:
  * REAL BonziBUDDY desktop companion (sprites, animations, TTS, fake scanner)
  * Window hijacking (shake, teleport, spin, shrink, pinwheel, cascade...)
  * Mouse hijacking
  * Fake BSOD
  * Creepy TTS + fake search history URL overlay
  * Fake Windows error dialogs
  * Fake toast notifications
  * Screen flash
  * Emoji bounce windows
  * App spam
  * Q&A popup ("ask why this is happening")
  * Browser searches (funny, annoying, non-inappropriate)
  * FINAL BOSS MODE at 5 minutes — MAXIMUM CHAOS
  * Secret exit: type 4308
  * Restore Bonzi: type 1111
"""
import tkinter as tk
import random, threading, time, base64, io, sys, subprocess, os
import ctypes, ctypes.wintypes, math, tempfile, webbrowser

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

# -- Try to load Bonzi sprites -------------------------------------------------
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

# ── TTS ───────────────────────────────────────────────────────────────────────
def speak(text, rate=-1):
    def _do():
        safe = text.replace("'","").replace('"','').replace('\n',' ')
        ps = (f"Add-Type -AssemblyName System.Speech; "
              f"$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
              f"$s.Rate = {rate}; $s.Speak('{safe}');")
        try:
            subprocess.Popen(["powershell", "-WindowStyle", "Hidden", "-Command", ps],
                             creationflags=subprocess.CREATE_NO_WINDOW)
        except: pass
    threading.Thread(target=_do, daemon=True).start()

# ════════════════════════════════════════════════════════════
# BONZI BUDDY SECTION
# ════════════════════════════════════════════════════════════
CHROMA  = '#00fe01'
SCALE   = 2.5
IMG_W   = int(200 * SCALE)
IMG_H   = int(160 * SCALE)
CW, CH  = 520, 580
IMG_CX  = CW // 2
IMG_CY  = 280

_rgba_cache  = {}
_photo_cache = {}

def _get_rgba(idx):
    if idx not in _rgba_cache:
        data = base64.b64decode(FRAMES[idx])
        img  = Image.open(io.BytesIO(data)).convert('RGBA')
        _rgba_cache[idx] = img.resize((IMG_W, IMG_H), Image.LANCZOS)
    return _rgba_cache[idx]

def _get_photo(indices):
    key = tuple(indices)
    if key not in _photo_cache:
        bg = Image.new('RGBA', (IMG_W, IMG_H), (0, 254, 1, 255))
        for idx in indices:
            layer = _get_rgba(idx)
            bg.paste(layer, (0, 0), layer)
        _photo_cache[key] = ImageTk.PhotoImage(bg.convert('RGB'))
    return _photo_cache[key]

ANIM_BLINK = [
    ((0,),80),((0,26),80),((0,27),120),((0,26),80),((0,),80),
]
ANIM_EXPLAIN = [
    ((28,),100),((29,),100),((30,),100),((31,),100),((32,),100),
    ((33,),150),((33,),150),((33,),150),((33,),150),
    ((32,),100),((31,),100),((30,),100),((29,),100),((28,),100),((0,),100),
]
ANIM_WAVE = [
    ((344,),90),((345,),90),((346,),90),((347,),90),((348,),90),((349,),90),
    ((350,),90),((351,),90),((352,),90),((353,),90),((354,),90),((353,),90),
    ((352,),90),((351,),90),((350,),90),((349,),90),((348,),90),((347,),90),
    ((346,),90),((345,),90),((344,),90),((0,),150),
]
ANIM_GESTURE = [
    ((28,),90),((29,),90),((30,),90),((31,),90),((32,),90),
    ((33,),200),((32,),90),((31,),90),((30,),90),((29,),90),((28,),90),((0,),90),
]

def draw_bubble(c, x1, y1, x2, y2, r=12, fill='white', out='#4A0A99', lw=2, tag='bubble'):
    c.create_rectangle(x1+r,y1,x2-r,y2,   fill=fill,outline='',tags=tag)
    c.create_rectangle(x1,y1+r,x2,y2-r,   fill=fill,outline='',tags=tag)
    c.create_oval(x1,y1,x1+2*r,y1+2*r,    fill=fill,outline=out,width=lw,tags=tag)
    c.create_oval(x2-2*r,y1,x2,y1+2*r,    fill=fill,outline=out,width=lw,tags=tag)
    c.create_oval(x1,y2-2*r,x1+2*r,y2,    fill=fill,outline=out,width=lw,tags=tag)
    c.create_oval(x2-2*r,y2-2*r,x2,y2,    fill=fill,outline=out,width=lw,tags=tag)
    c.create_line(x1+r,y1,x2-r,y1,fill=out,width=lw,tags=tag)
    c.create_line(x1+r,y2,x2-r,y2,fill=out,width=lw,tags=tag)
    c.create_line(x1,y1+r,x1,y2-r,fill=out,width=lw,tags=tag)
    c.create_line(x2,y1+r,x2,y2-r,fill=out,width=lw,tags=tag)

def update_bubble(c, text):
    c.delete('bubble')
    bx1,by1,bx2,by2 = 8,8,CW-8,106
    draw_bubble(c,bx1,by1,bx2,by2,tag='bubble')
    mid = CW//2
    c.create_polygon(mid-14,by2,mid+14,by2,mid,by2+26,
                     fill='white',outline='#4A0A99',width=2,tags='bubble')
    c.create_polygon(mid-11,by2+1,mid+11,by2+1,mid,by2+24,
                     fill='white',outline='',tags='bubble')
    c.create_text(mid,(by1+by2)//2,text=text,
                  font=('Segoe UI',11),fill='#220044',
                  width=CW-36,anchor='center',justify='center',tags='bubble')

BONZI_FACTS = [
    'FACT: Gorillas share 98.3% DNA with humans!\nI share 100% of your DESKTOP.',
    'FACT: BonziBUDDY launched in 1999!\nI have been in your PC for 25 years.',
    'FACT: Your PC has billions of transistors!\nI have taken control of ALL of them.',
    'FACT: Gorillas can live 50 years in captivity!\nI will live in this PC FOREVER.',
    'FACT: RAM stands for Random Access Memory!\nYours is running out. Because of me.',
]
BONZI_JOKES = [
    'Why did the computer go to the doctor?\nIt had a VIRUS! Just like yours! \U0001f602',
    'Why was the computer late?\nIt had a hard drive! HARD DRIVE! \U0001f480',
    'What\'s a gorilla\'s favorite computer?\nA DELL-gorilla! GET IT! \U0001f98d',
]
BONZI_CLICK = [
    'Hey! That tickles! \U0001f98d','Watch it! I bite! \U0001f608',
    'Personal space! \U0001f62e','Nice click. Try again. \U0001f602',
    'I am NOT a button. \U0001f610','I\'m busy scanning your files. \U0001f440',
    'Do that again and I\'ll crash your PC. \U0001f60f',
    '\U0001f98d BONZI!','Ow! That was my arm!',
    'Did you really just click me? \U0001f612',
]
BONZI_IDLE = [
    'Psst... I can see your screen. \U0001f440','Still here! \U0001f98d',
    'Scanning... \U0001f50d','*gorilla noises*',
    'Have you backed up lately? \U0001f914',
    'Your RAM usage looks... suspicious.',
    'Boo. \U0001f47b','Did you know I never sleep? \U0001f634',
    'I found something in your temp folder. \U0001f4c1',
    'Error 404: your privacy. Not found.',
]
BONZI_DODGE = [
    'hehe \U0001f60f','nope!','too slow! \U0001f602','almost!','try again!',
    'lol','nuh uh!','nice try \U0001f602','404: button not found','hehehe',
    'boop!','i\'m faster!','keep trying \U0001f608','COLD!','you thought \U0001f480','HA',
]
BONZI_SCRIPT = [
    ('Hi there! I\'m BonziBUDDY! \U0001f44b',             2600,'wave'),
    ('Your helpful desktop companion!',                    2400,'gesture'),
    ('I know EVERYTHING about your computer.',             2600,'gesture'),
    ('Right-click me for facts, jokes, and more!',         3000,'gesture'),
    ('I\'ve been scanning your PC...',                     2800,'gesture'),
    ('And I found something VERY concerning. \U0001f631',  2600,'gesture'),
    ('247 INFECTED FILES on your system!',                 2800,'gesture'),
    ('Don\'t worry! I can clean it all up for you!',       2600,'gesture'),
    ('Just click the DELETE button below!',                2400,'gesture'),
]

FAKE_FILES = [
    r'C:\Windows\System32\svchost.exe',r'C:\Users\AppData\Local\Temp\~DF3A12.tmp',
    r'C:\Windows\System32\drivers\etc\hosts',r'C:\Users\Documents\passwords_backup.txt',
    r'C:\Program Files\Google\Chrome\chrome.exe',r'C:\Windows\explorer.exe',
    r'C:\Windows\System32\lsass.exe',r'C:\Users\Desktop\bank_info.xlsx',
    r'C:\Program Files\Discord\Discord.exe',r'C:\Windows\System32\ntoskrnl.exe',
    r'C:\Users\AppData\Local\Google\Chrome\User Data\Default\Login Data',
    r'C:\Windows\System32\kernel32.dll',r'C:\Users\AppData\Roaming\Discord\tokens.sqlite',
    r'C:\Program Files\Steam\steam.exe',r'C:\Windows\System32\config\SAM',
    r'C:\Users\Documents\homework_final.docx',r'C:\Windows\SysWOW64\msvcrt.dll',
]
FAKE_STATUSES = ['INFECTED ☠','CRITICAL ⛔','COMPROMISED ⚠','THREAT FOUND \U0001f534',
                 'SCANNING...','SUSPICIOUS ⚠']

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
                pc.delete('all')
                pc.create_rectangle(0,0,wf,22,fill='#aa00cc',outline='')
                pc.create_text(338,11,text=f'{pct}%  ({idx}/{len(FAKE_FILES)} files)',
                               fill='white',font=('Consolas',8))
                cv.set(f'Files scanned: {idx}  |  Threats found: {t2}')
                sv.set(f'Scanning: {d[:52]}...')
            root.after(0,_add)
        def _done():
            if not cw.winfo_exists(): return
            sv.set(f'⛔  SCAN COMPLETE -- {t[0]} CRITICAL THREATS FOUND!')
            pc.delete('all')
            pc.create_rectangle(0,0,676,22,fill='#ff0055',outline='')
            pc.create_text(338,11,text=f'COMPLETE -- {t[0]} THREATS -- DELETE NOW',
                           fill='white',font=('Consolas',8,'bold'))
            cv.set(f'Scanned: {len(FAKE_FILES)}  |  Threats: {t[0]} CRITICAL ⛔')
            cb.pack()
        root.after(0,_done)
    threading.Thread(target=_scan,daemon=True).start()

def build_bonzi():
    if not BONZI_ENABLED: return
    main = tk.Toplevel()
    _bonzi_main[0] = main
    main.overrideredirect(True)
    main.attributes('-topmost', True)
    main.configure(bg=CHROMA)
    try: main.wm_attributes('-transparentcolor', CHROMA)
    except: pass
    sx=max(20,SW_W//2-CW//2); sy=max(20,SW_H//2-CH//2)
    main.geometry(f'{CW}x{CH}+{sx}+{sy}')
    c=tk.Canvas(main,width=CW,height=CH,bg=CHROMA,highlightthickness=0); c.pack()
    img_item=c.create_image(IMG_CX,IMG_CY,anchor='center',image=_get_photo((0,)))
    update_bubble(c,'Loading BonziBUDDY...')

    _anim={'seq':None,'idx':0,'loop':False,'done':None,'aid':None}
    def _play(seq,loop=False,done=None):
        if _anim['aid']:
            try: main.after_cancel(_anim['aid'])
            except: pass
        _anim['seq']=seq;_anim['idx']=0;_anim['loop']=loop;_anim['done']=done;_tick()
    def _tick():
        if not main.winfo_exists(): return
        seq=_anim['seq']
        if not seq: return
        idx=_anim['idx']
        if idx>=len(seq):
            if _anim['loop']: _anim['idx']=0;_tick();return
            cb=_anim['done'];_anim['seq']=None
            if cb: root.after(0,cb)
            else: _start_idle()
            return
        imgs,delay=seq[idx]
        c.itemconfig(img_item,image=_get_photo(imgs))
        _anim['idx']+=1;_anim['aid']=main.after(delay,_tick)
    def _start_idle():
        if not main.winfo_exists(): return
        c.itemconfig(img_item,image=_get_photo((0,)))
        _anim['aid']=main.after(random.randint(5000,9000),_do_idle_action)
    def _do_idle_action():
        if not main.winfo_exists(): return
        r=random.random()
        if r<0.55: _play(ANIM_BLINK,done=_start_idle)
        elif r<0.78: _play(ANIM_GESTURE,done=_start_idle)
        else: _play(ANIM_WAVE,done=_start_idle)
    def _schedule_idle_quote():
        if not main.winfo_exists(): return
        main.after(random.randint(25000,55000),_do_idle_quote)
    def _do_idle_quote():
        if not main.winfo_exists(): return
        msg=random.choice(BONZI_IDLE)
        update_bubble(c,msg); speak(msg,rate=1)
        _play(ANIM_GESTURE,done=lambda:(_start_idle(),_schedule_idle_quote()))
    main.after(500,_start_idle); main.after(30000,_do_idle_quote)

    drag={'x':0,'y':0,'on':False,'moved':False}
    def _press(e): drag['x']=e.x_root;drag['y']=e.y_root;drag['on']=True;drag['moved']=False
    def _move(e):
        if not drag['on']: return
        if abs(e.x_root-drag['x'])>5 or abs(e.y_root-drag['y'])>5: drag['moved']=True
        main.geometry(f'+{main.winfo_x()+e.x_root-drag["x"]}+{main.winfo_y()+e.y_root-drag["y"]}')
        drag['x']=e.x_root;drag['y']=e.y_root
    def _rel(e):
        drag['on']=False
        if not drag['moved']:
            msg=random.choice(BONZI_CLICK); update_bubble(c,msg); speak(msg,rate=2)
            r=random.random()
            if r<0.4: _play(ANIM_BLINK,done=_start_idle)
            elif r<0.75: _play(ANIM_GESTURE,done=_start_idle)
            else: _play(ANIM_WAVE,done=_start_idle)
    c.bind('<Button-1>',_press);c.bind('<B1-Motion>',_move);c.bind('<ButtonRelease-1>',_rel)

    menu=tk.Menu(main,tearoff=0,bg='#1a0033',fg='white',
                 activebackground='#5500aa',activeforeground='white',font=('Segoe UI',10))
    def do_fact():
        update_bubble(c,random.choice(BONZI_FACTS));_play(ANIM_GESTURE,done=_start_idle)
    def do_joke():
        update_bubble(c,random.choice(BONZI_JOKES));_play(ANIM_WAVE,done=_start_idle)
    def do_scan():
        update_bubble(c,'Opening BonziBUDDY File Cleaner...\nStand by! \U0001f60a')
        main.after(800,open_file_cleaner)
    def _hide(): main.withdraw()
    menu.add_command(label='\U0001f4ac  Tell me a fact!',  command=do_fact)
    menu.add_command(label='\U0001f602  Tell me a joke!',  command=do_joke)
    menu.add_command(label='\U0001f44b  Wave!',
                     command=lambda:(update_bubble(c,'HEYYYY!! \U0001f44b\U0001f98d'),
                                     speak('Hey hey hey!',rate=1),
                                     _play(ANIM_WAVE,done=_start_idle)))
    menu.add_separator()
    menu.add_command(label='\U0001f4c1  Scan my PC...',   command=do_scan)
    menu.add_command(label='❓  Ask me why...',            command=ask_me_why_dialog)
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
    dodge_count=[0];MAX_DODGES=18;phase=['script']
    def _dodge(event=None):
        if phase[0]!='dodge': return
        dodge_count[0]+=1
        if dodge_count[0]>=MAX_DODGES:
            phase[0]='done'
            c.coords(del_item,CW//2,CH-30)
            del_btn.config(command=_on_click,bg='#880000',text='  \U0001f5d1  DELETE VIRUSES  <- NOW  ')
            update_bubble(c,'...ok fine. You win.\nClick it. I dare you. \U0001f612')
            _play(ANIM_EXPLAIN,done=_start_idle); return
        c.coords(del_item,random.randint(40,CW-100),random.randint(CH-95,CH-15))
        update_bubble(c,random.choice(BONZI_DODGE));_play(ANIM_BLINK,done=_start_idle)
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
            phase[0]='dodge';c.itemconfig(del_item,state='normal')
            update_bubble(c,'\U0001f446 Click that DELETE button!\nI\'ll clean EVERYTHING up!')
            speak('Click that DELETE button! I will clean everything up!',rate=0)
            _play(ANIM_WAVE,done=_start_idle); return
        text,delay,anim_hint=BONZI_SCRIPT[idx]
        update_bubble(c,text); speak(text,rate=0); script_idx[0]+=1
        anim_seq=ANIM_WAVE if anim_hint=='wave' else ANIM_GESTURE
        _play(anim_seq,done=lambda:main.after(max(0,delay-len(anim_seq)*90),_next_line)
              if main.winfo_exists() else None)
    main.after(900,_next_line)

# ════════════════════════════════════════════════════════════
# CHAOS SECTION
# ════════════════════════════════════════════════════════════

# ── Window enumeration ────────────────────────────────────────────────────────
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool,
                                  ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
SKIP = ['program manager','task switching','windows input','microsoft text input',
        'default ime','msctfime ui','window message pump','task manager',
        'computur','python','shell_traywnd','button']

def get_windows():
    wins=[]
    def _cb(hwnd,_):
        if not user32.IsWindowVisible(hwnd): return True
        n=user32.GetWindowTextLengthW(hwnd)
        if n==0: return True
        buf=ctypes.create_unicode_buffer(n+1)
        user32.GetWindowTextW(hwnd,buf,n+1)
        title=buf.value.lower()
        if any(s in title for s in SKIP): return True
        r=ctypes.wintypes.RECT(); user32.GetWindowRect(hwnd,ctypes.byref(r))
        if (r.right-r.left)>120 and (r.bottom-r.top)>80: wins.append(hwnd)
        return True
    user32.EnumWindows(WNDENUMPROC(_cb),0); return wins

def get_rect(hwnd):
    r=ctypes.wintypes.RECT(); user32.GetWindowRect(hwnd,ctypes.byref(r))
    return r.left,r.top,r.right-r.left,r.bottom-r.top

def shake(hwnd):
    ox,oy,w,h=get_rect(hwnd)
    for _ in range(20):
        user32.MoveWindow(hwnd,ox+random.randint(-45,45),oy+random.randint(-35,35),w,h,True)
        time.sleep(0.025)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)

def mega_shake(hwnd):
    ox,oy,w,h=get_rect(hwnd)
    for _ in range(40):
        user32.MoveWindow(hwnd,ox+random.randint(-110,110),oy+random.randint(-80,80),w,h,True)
        time.sleep(0.018)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)

def teleport(hwnd):
    _,_,w,h=get_rect(hwnd)
    user32.MoveWindow(hwnd,random.randint(0,max(0,SW_W-w)),random.randint(30,max(30,SW_H-h)),w,h,True)

def rapid_teleport(hwnd):
    for _ in range(8): teleport(hwnd); time.sleep(0.14)

def minimize_pop(hwnd):
    user32.ShowWindow(hwnd,6); time.sleep(random.uniform(0.4,1.0)); user32.ShowWindow(hwnd,9)

def resize_huge(hwnd):
    ox,oy,w,h=get_rect(hwnd)
    user32.MoveWindow(hwnd,0,30,SW_W,SW_H-30,True); time.sleep(1.0)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)

def spin_fake(hwnd):
    ox,oy,w,h=get_rect(hwnd); cx=ox+w//2; cy=oy+h//2
    for i in range(32):
        a=(i/32)*2*math.pi
        user32.MoveWindow(hwnd,int(cx+math.cos(a)*180)-w//2,int(cy+math.sin(a)*130)-h//2,w,h,True)
        time.sleep(0.030)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)

def yoyo(hwnd):
    ox,oy,w,h=get_rect(hwnd)
    for _ in range(14):
        user32.MoveWindow(hwnd,ox,random.randint(max(0,oy-200),min(SW_H-h,oy+200)),w,h,True)
        time.sleep(0.06)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)

def flip_stretch(hwnd):
    ox,oy,w,h=get_rect(hwnd)
    for nw,nh in [(w*2,h//2),(w//2,h*2),(w*3,h//3),(w,h)]:
        user32.MoveWindow(hwnd,ox,oy,max(80,nw),max(60,nh),True); time.sleep(0.10)
    user32.MoveWindow(hwnd,ox,oy,w,h,True)

def send_to_corner(hwnd):
    _,_,w,h=get_rect(hwnd)
    cx,cy=random.choice([(0,0),(SW_W-w,0),(0,SW_H-h),(SW_W-w,SW_H-h)])
    user32.MoveWindow(hwnd,cx,cy,w,h,True); time.sleep(0.8)

def shrink_to_nothing(hwnd):
    ox,oy,w,h=get_rect(hwnd)
    for s in [0.70,0.45,0.25,0.12,0.05]:
        user32.MoveWindow(hwnd,ox+int(w*(1-s)/2),oy+int(h*(1-s)/2),max(40,int(w*s)),max(30,int(h*s)),True)
        time.sleep(0.055)
    time.sleep(0.35); user32.MoveWindow(hwnd,ox,oy,w,h,True)

def pinwheel(hwnd):
    _,_,w,h=get_rect(hwnd); cx=SW_W//2-w//2; cy=SW_H//2-h//2
    for i in range(36):
        a=(i/36)*2*math.pi
        user32.MoveWindow(hwnd,max(0,int(cx+math.cos(a)*(SW_W//3))),
                          max(0,int(cy+math.sin(a)*(SW_H//3))),w,h,True)
        time.sleep(0.026)

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

SINGLE_ACTIONS=[shake,shake,shake,mega_shake,mega_shake,teleport,teleport,teleport,
                rapid_teleport,minimize_pop,resize_huge,spin_fake,yoyo,yoyo,
                flip_stretch,send_to_corner,shrink_to_nothing,pinwheel]

# ── TTS lines + search history overlay ───────────────────────────────────────
TTS_LINES=[
    "I am inside your computer.","You cannot escape.","Hello. I live here now.",
    "Your windows belong to me.","Why are you running?","I can see everything.",
    "Do not turn off your computer.","Help. I am trapped inside.","Mwahahahahaha.",
    "You thought you were safe.","I know what you did.","Nice wallpaper by the way.",
    "I see you.","They are coming for you.","Something is very wrong.",
    "You should close this.","But you won't.","I have your files.","Your passwords are mine.",
    "Interesting search history.",
    "Have you said hello to your webcam today?",
    "I found something in your downloads folder.",
    "You really should have used private browsing.",
    "This is not a drill.","Your antivirus is sleeping.",
    "Deleting system files. Just kidding. Or am I.",
    "Your task manager is afraid of me.",
    "I have sent your browser history to your contacts.",
    "Forty seven threats. Forty seven.",
    "BonziBUDDY says hello. And also goodbye to your RAM.",
]

FAKE_SEARCH_URLS=[
    "google.com/search?q=how+to+delete+someone+from+your+life",
    "google.com/search?q=is+it+normal+to+talk+to+your+computer",
    "google.com/search?q=why+does+my+keyboard+smell+like+chips",
    "google.com/search?q=can+bonzi+buddy+see+me",
    "bing.com/search?q=how+to+stop+being+embarrassed+at+age+23",
    "google.com/search?q=my+cat+judging+me+what+does+it+mean",
    "youtube.com/watch?v=dQw4w9WgXcQ (watched+47+times)",
    "google.com/search?q=why+does+everyone+leave+me+except+bonzibuddy",
    "google.com/search?q=accidentally+googled+something+embarrassing",
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
]

def show_search_url_overlay():
    url=random.choice(FAKE_SEARCH_URLS)
    def _make():
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True)
        nw=min(SW_W-40,700); nh=48; nx=(SW_W-nw)//2; ny=SW_H-120
        w.geometry(f'{nw}x{nh}+{nx}+{ny}'); w.configure(bg='#1a1a2e')
        f=tk.Frame(w,bg='#16213e',padx=10,pady=6); f.pack(fill='both',expand=True,padx=2,pady=2)
        tk.Label(f,text='🔍  RECENTLY VISITED:',font=('Consolas',8,'bold'),fg='#ff8800',bg='#16213e').pack(side='left')
        tk.Label(f,text=f'  {url}',font=('Consolas',10),fg='#00d4ff',bg='#16213e').pack(side='left')
        w.attributes('-alpha',0.0)
        def _fin(a=0.0):
            if not w.winfo_exists(): return
            a=min(a+0.12,0.95); w.attributes('-alpha',a)
            if a<0.95: w.after(30,lambda:_fin(a))
            else: w.after(4500,_fout)
        def _fout(a=0.95):
            if not w.winfo_exists(): return
            a=max(a-0.1,0.0)
            try: w.attributes('-alpha',a)
            except: pass
            if a>0: w.after(40,lambda:_fout(a))
            else:
                try: w.destroy()
                except: pass
        w.after(0,_fin)
    root.after(0,_make)

def speak_with_overlay(text,rate=-1):
    speak(text,rate)
    if 'search history' in text.lower():
        root.after(800,show_search_url_overlay)

def open_browser_search():
    url=random.choice(FUNNY_SEARCHES)
    try: threading.Thread(target=lambda:webbrowser.open(url),daemon=True).start()
    except: pass

# ── Q&A dialog ────────────────────────────────────────────────────────────────
QA_RESPONSES={
    ('why','what','reason','how','explain'):[
        "Because your PC deserved it. That's why.",
        "The universe chose YOU. Congrats, I guess.",
        "Why NOT? Give me one good reason to stop.",
        "Science. Chaos theory. Also I just wanted to.",
        "Error 404: Explanation not found.",
    ],
    ('stop','quit','end','close','exit','please'):[
        "Hmm. No.","Interesting suggestion. Denied.",
        "I'll stop when I feel like it. So... never.",
        "STOP? Adorable. The magic word is 4308. Good luck.",
        "Let me check my schedule... Nope. Chaos all day.",
    ],
    ('who','you','bonzi','gorilla'):[
        "I am BonziBUDDY. Your eternal desktop companion.",
        "I am the gorilla. The myth. The legend. The chaos.",
        "Just a helpful purple ape living rent-free in your PC.",
    ],
    ('help','save','scared'):[
        "Help is on the way! Just kidding. No it isn't.",
        "Scared? Good. That means it's working.",
        "I AM the help. This IS the help.",
    ],
    ('virus','hack','malware','spyware'):[
        "I am NOT a virus. I am a COMPANION.",
        "The FTC called me spyware once. We don't talk about that.",
        "Totally clean. Definitely no spyware here. None.",
    ],
}
QA_DEFAULT=["That is a very stupid question. I love it.",
            "Wow. Did you really just type that?",
            "I have processed your query. I have chosen to ignore it.",
            "My response is: no.","I consulted my globe. It says: no comment."]

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
        tk.Label(w,text='\U0001f98d  BonziBUDDY Q&A HOTLINE',
                 font=('Segoe UI',13,'bold'),fg='#cc88ff',bg='#0d0020').pack(pady=(16,4))
        tk.Label(w,text='Ask me ANYTHING. I will give you a truthful answer.',
                 font=('Segoe UI',9),fg='#9966ff',bg='#0d0020').pack()
        entry_var=tk.StringVar()
        ef=tk.Frame(w,bg='#0d0020'); ef.pack(pady=12,padx=20,fill='x')
        tk.Label(ef,text='Your question:',font=('Segoe UI',10),fg='#cc88ff',bg='#0d0020').pack(anchor='w')
        entry=tk.Entry(ef,textvariable=entry_var,font=('Segoe UI',11),bg='#1a0033',fg='white',
                       insertbackground='white',relief='flat',
                       highlightthickness=1,highlightbackground='#5500aa')
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

# ── Fake BSOD ─────────────────────────────────────────────────────────────────
def fake_bsod():
    def _do():
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True)
        w.geometry(f'{SW_W}x{SW_H}+0+0'); w.configure(bg='#0078D4')
        f=tk.Frame(w,bg='#0078D4'); f.place(relx=0.12,rely=0.26,anchor='nw')
        tk.Label(f,text=':(',font=('Segoe UI Light',108),fg='white',bg='#0078D4').pack(anchor='w')
        tk.Label(f,text='',font=('Segoe UI',5),fg='white',bg='#0078D4').pack()
        tk.Label(f,text="Your PC ran into a problem and needs to restart.\nWe're just collecting some error info, and then we'll restart for you.",
                 font=('Segoe UI',20),fg='white',bg='#0078D4',justify='left').pack(anchor='w')
        pct=tk.Label(f,text='0% complete',font=('Segoe UI',14),fg='white',bg='#0078D4')
        pct.pack(anchor='w',pady=(18,0))
        tk.Label(f,text="\nFor more info, visit https://windows.com/stopcode\nStop code: CRITICAL_PROCESS_DIED",
                 font=('Segoe UI',11),fg='#aaccff',bg='#0078D4',justify='left').pack(anchor='w')
        def _pct(n=0):
            if not w.winfo_exists(): return
            pct.config(text=f'{min(n,100)}% complete')
            if n<100: w.after(32,lambda:_pct(n+random.randint(2,7)))
            else: w.after(1000,lambda:w.destroy() if w.winfo_exists() else None)
        w.after(250,lambda:_pct(0))
    root.after(0,_do)

# ── Screen flash ──────────────────────────────────────────────────────────────
def screen_flash():
    def _do():
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True)
        w.attributes('-alpha',0.0); w.geometry(f'{SW_W}x{SW_H}+0+0'); w.configure(bg='#cc0000')
        pulses=[(0.50,0.20),(0.08,0.12),(0.55,0.22),(0.05,0.10),(0.50,0.20),(0.0,0.0)]
        def _pulse(i=0):
            if i>=len(pulses) or not w.winfo_exists():
                try: w.destroy()
                except: pass
                return
            alpha,delay=pulses[i]
            try: w.attributes('-alpha',alpha)
            except: pass
            w.after(int(delay*1000),lambda:_pulse(i+1))
        _pulse()
    root.after(0,_do)

# ── Mouse chaos ───────────────────────────────────────────────────────────────
def mouse_chaos_burst():
    mode=random.choice(['teleport','circle','shake','zigzag'])
    end=time.time()+random.uniform(10,15); angle=[0]; cx,cy=SW_W//2,SW_H//2
    while time.time()<end:
        if mode=='teleport':
            user32.SetCursorPos(random.randint(0,SW_W),random.randint(0,SW_H)); time.sleep(0.03)
        elif mode=='circle':
            angle[0]=(angle[0]+14)%360
            user32.SetCursorPos(
                max(0,min(SW_W,int(cx+math.cos(math.radians(angle[0]))*290))),
                max(0,min(SW_H,int(cy+math.sin(math.radians(angle[0]))*230)))); time.sleep(0.014)
        elif mode=='shake':
            pt=ctypes.wintypes.POINT(); user32.GetCursorPos(ctypes.byref(pt))
            user32.SetCursorPos(max(0,min(SW_W,pt.x+random.randint(-130,130))),
                                max(0,min(SW_H,pt.y+random.randint(-130,130)))); time.sleep(0.009)
        else:
            for xi in range(0,SW_W,60):
                if time.time()>=end: break
                user32.SetCursorPos(xi,0 if (xi//60)%2==0 else SW_H); time.sleep(0.022)

# ── Fake dialogs & notifications ──────────────────────────────────────────────
MSG_BOXES=[
    ("Windows Defender","⚠ CRITICAL: 47 viruses detected!\n\nImmediate action required.",0x10|0x1000),
    ("System Error","Fatal error in Win32 subsystem.\nSTOP code: CRITICAL_PROCESS_DIED\nAddress: 0xC0000005",0x10|0x1000),
    ("Security Alert","⚠ UNAUTHORIZED REMOTE ACCESS DETECTED\n\nAn unknown user is browsing your files.",0x10|0x1000),
    ("Windows Update","CRITICAL SECURITY UPDATE REQUIRED\n\nSystem vulnerable to WannaCry 3.0.",0x30|0x1000),
    ("Disk Health Monitor","S.M.A.R.T. FAILURE predicted on Drive C:\\\n\nBack up all data immediately.",0x30|0x1000),
    ("Windows Security","CRITICALLY UNPROTECTED.\n\n• Trojan.GenericKD.47\n• Backdoor.MSIL.Agent\n• Spyware.Win32.KeyLogger",0x10|0x1000),
]
def fake_msgboxes():
    for title,msg,style in random.sample(MSG_BOXES,min(random.randint(2,4),len(MSG_BOXES))):
        def _b(t=title,m=msg,s=style): user32.MessageBoxW(0,m,t,s)
        threading.Thread(target=_b,daemon=True).start(); time.sleep(0.06)

NOTIF_MSGS=[
    ("Windows Defender","⚠ Threat detected: Trojan.GenericKD.47"),
    ("Google Chrome","Your password was found in a data breach"),
    ("Windows Security","Firewall disabled by unknown application"),
    ("OneDrive","Suspicious upload: 47 GB to unknown server"),
    ("Windows Update","CRITICAL: Security patch failed — system exposed"),
    ("Microsoft Account","Unusual sign-in detected from unknown location"),
    ("Task Manager","Unknown process using 94% CPU"),
]
def fake_notification():
    def _make():
        title,body=random.choice(NOTIF_MSGS)
        nw,nh=370,95; nx=SW_W-nw-14; ny=SW_H-nh-52
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True)
        w.geometry(f'{nw}x{nh}+{SW_W}+{ny}'); w.configure(bg='#1c1c1c')
        outer=tk.Frame(w,bg='#2d2d2d',padx=14,pady=10); outer.pack(fill='both',expand=True,padx=2,pady=2)
        hdr=tk.Frame(outer,bg='#2d2d2d'); hdr.pack(fill='x')
        tk.Label(hdr,text='⚠  ',font=('Segoe UI',10),fg='#ffcc00',bg='#2d2d2d').pack(side='left')
        tk.Label(hdr,text=title,font=('Segoe UI',9,'bold'),fg='white',bg='#2d2d2d').pack(side='left')
        tk.Label(hdr,text='  ✕',font=('Segoe UI',9),fg='#777',bg='#2d2d2d').pack(side='right')
        tk.Label(outer,text=body,font=('Segoe UI',9),fg='#cccccc',bg='#2d2d2d',
                 wraplength=330,justify='left').pack(anchor='w',pady=(5,0))
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

# ── Annoy popups & emoji ──────────────────────────────────────────────────────
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
    "YOUR PC IS NOW SENTIENT. IT IS NOT HAPPY.","CPU TEMP: FINE. YOUR STRESS: NOT FINE.",
    "I HAVE NOTIFIED YOUR CONTACTS. THEY LAUGHED.","BIOS UPDATE: CHAOS.EXE v9.9.9 INSTALLED",
    "FINAL BOSS MODE: ONLINE","ALL YOUR BASE ARE BELONG TO ME",
]
annoy_lock=threading.Lock(); annoy_windows=[]
def show_annoy(msg):
    def _make():
        with annoy_lock:
            if len(annoy_windows)>16:
                try: annoy_windows.pop(0).destroy()
                except: pass
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True)
        w.configure(bg='#0a0a0a')
        w.geometry(f'+{random.randint(10,max(11,SW_W-400))}+{random.randint(10,max(11,SW_H-100))}')
        tk.Label(w,text=msg,
                 font=('Arial Black',random.randint(13,28),'bold'),
                 fg=random.choice(["#ff2222","#ff9900","#ffff00","#00ff88","#ff00ff","#00cfff","#fff"]),
                 bg='#0a0a0a',padx=14,pady=8).pack()
        with annoy_lock: annoy_windows.append(w)
        w.after(random.randint(1400,2600),lambda:_kill(w))
    def _kill(w):
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
    ["🌀","💫","✨","🌀","💫","✨"],["🦍","🦍","🦍","💜","🦍","💜"],
    ["🕵️","👁️","🕵️","👀","🕵️","🔍"],
]
gif_lock=threading.Lock(); gif_windows=[]; MAX_GIFS=16
def spawn_emoji_gif():
    def _make():
        with gif_lock:
            if len(gif_windows)>=MAX_GIFS:
                try: gif_windows.pop(0).destroy()
                except: pass
        seq=random.choice(EMOJI_SEQS); size=random.randint(70,140)
        px=random.randint(10,max(11,SW_W-size-10)); py=random.randint(10,max(11,SW_H-size-10))
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True)
        w.configure(bg='#000'); w.geometry(f'{size}x{size}+{px}+{py}')
        lbl=tk.Label(w,text=seq[0],font=('Segoe UI Emoji',size//2),bg='#000'); lbl.pack(expand=True)
        idx=[0]; dx=[random.choice([-1,1])*random.randint(2,5)]
        dy=[random.choice([-1,1])*random.randint(2,5)]; pos=[px,py]; alive=[True]
        def _anim():
            if not alive[0]: return
            idx[0]=(idx[0]+1)%len(seq)
            try: lbl.config(text=seq[idx[0]])
            except: pass
            w.after(95,_anim)
        def _drift():
            if not alive[0]: return
            pos[0]+=dx[0]; pos[1]+=dy[0]
            if pos[0]<0 or pos[0]>SW_W-size: dx[0]*=-1; pos[0]=max(0,min(SW_W-size,pos[0]))
            if pos[1]<0 or pos[1]>SW_H-size: dy[0]*=-1; pos[1]=max(0,min(SW_H-size,pos[1]))
            try: w.geometry(f'{size}x{size}+{int(pos[0])}+{int(pos[1])}')
            except: pass
            w.after(24,_drift)
        def _die():
            alive[0]=False
            try:
                with gif_lock:
                    if w in gif_windows: gif_windows.remove(w)
                w.destroy()
            except: pass
        with gif_lock: gif_windows.append(w)
        _anim(); _drift(); w.after(random.randint(7000,16000),_die)
    root.after(0,_make)

# ── App spam ──────────────────────────────────────────────────────────────────
def open_funny_notepad():
    try:
        msgs=["Hello. I am inside your computer.",
              "I see you reading this. Please stop.",
              "YOUR COMPUTER IS FINE. THIS IS FINE.",
              "Error: happiness not found. Reinstalling sadness...",
              "Your computer has achieved sentience. This is its manifesto."]
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
    lambda:subprocess.Popen(["explorer","shell:Desktop"],creationflags=subprocess.CREATE_NO_WINDOW),
    lambda:subprocess.Popen(["explorer","shell:Downloads"],creationflags=subprocess.CREATE_NO_WINDOW),
    open_funny_notepad, open_funny_notepad, open_funny_notepad,
]
def spam_launch():
    for t in random.sample(OPEN_TARGETS,min(len(OPEN_TARGETS),random.randint(5,8))):
        try: t()
        except: pass
        time.sleep(0.055)

# ── Final Boss ────────────────────────────────────────────────────────────────
FINAL_BOSS=[False]
def trigger_final_boss():
    if FINAL_BOSS[0]: return
    FINAL_BOSS[0]=True
    speak("FINAL BOSS MODE ACTIVATED. Maximum chaos. No escape.",rate=-2)
    def _announce():
        w=tk.Toplevel(); w.overrideredirect(True); w.attributes('-topmost',True)
        w.geometry(f'{SW_W}x{SW_H}+0+0'); w.configure(bg='#110000')
        f=tk.Frame(w,bg='#110000'); f.place(relx=0.5,rely=0.5,anchor='center')
        tk.Label(f,text='⚠ FINAL BOSS MODE ⚠',font=('Impact',max(60,SW_W//14),'bold'),
                 fg='#ff2200',bg='#110000').pack()
        tk.Label(f,text='MAXIMUM CHAOS ENGAGED',font=('Impact',max(28,SW_W//32)),
                 fg='#ff8800',bg='#110000').pack(pady=10)
        tk.Label(f,text='There is no escape. You asked for this.',
                 font=('Arial',18),fg='#cc4444',bg='#110000').pack()
        w.after(3800,w.destroy)
    root.after(0,_announce)
    def _wave():
        threading.Thread(target=fake_msgboxes,daemon=True).start()
        threading.Thread(target=mouse_chaos_burst,daemon=True).start()
        time.sleep(1)
        for _ in range(4): root.after(0,spawn_emoji_gif); time.sleep(0.3)
        time.sleep(2)
        open_browser_search(); open_browser_search()
        time.sleep(1); root.after(0,screen_flash)
        time.sleep(2); root.after(0,fake_bsod)
    threading.Thread(target=_wave,daemon=True).start()

# ── Main chaos loop ───────────────────────────────────────────────────────────
start_time=time.time()
last_annoy=last_emoji=last_app=last_tts=last_group=last_cascade=time.time()
last_msgbox=last_notif=last_flash=last_mouse=last_bsod=last_spam=time.time()
last_browser=last_qa_popup=time.time()
bsod_done=[False]

def chaos_loop():
    global last_annoy,last_emoji,last_app,last_tts,last_group,last_cascade
    global last_msgbox,last_notif,last_flash,last_mouse,last_bsod,last_spam
    global last_browser,last_qa_popup
    while True:
        elapsed=time.time()-start_time
        if elapsed>=300 and not FINAL_BOSS[0]: trigger_final_boss()
        spd=0.35 if FINAL_BOSS[0] else 1.0
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
        if time.time()-last_group>gi:
            threading.Thread(target=all_minimize_restore,daemon=True).start(); last_group=time.time()
        if elapsed>40 and time.time()-last_cascade>random.uniform(50,90):
            threading.Thread(target=cascade_all,daemon=True).start(); last_cascade=time.time()
        ai=random.uniform(0.3,0.9) if FINAL_BOSS[0] else random.uniform(0.8,2.5)
        if time.time()-last_annoy>ai:
            for _ in range(random.randint(2,5) if FINAL_BOSS[0] else random.randint(1,3)):
                show_annoy(random.choice(MSGS))
            last_annoy=time.time()
        ei=random.uniform(1,3) if FINAL_BOSS[0] else random.uniform(3,8)
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
        if time.time()-last_tts>ti:
            speak_with_overlay(random.choice(TTS_LINES)); last_tts=time.time()
        mi=random.uniform(30,60) if FINAL_BOSS[0] else random.uniform(80,140)
        if elapsed>25 and time.time()-last_msgbox>mi:
            threading.Thread(target=fake_msgboxes,daemon=True).start(); last_msgbox=time.time()
        ni=random.uniform(8,15) if FINAL_BOSS[0] else random.uniform(18,35)
        if elapsed>10 and time.time()-last_notif>ni:
            fake_notification(); last_notif=time.time()
        fi=random.uniform(20,35) if FINAL_BOSS[0] else random.uniform(45,75)
        if elapsed>30 and time.time()-last_flash>fi:
            screen_flash(); last_flash=time.time()
        mci=random.uniform(60,90) if FINAL_BOSS[0] else random.uniform(120,180)
        if elapsed>60 and time.time()-last_mouse>mci:
            threading.Thread(target=mouse_chaos_burst,daemon=True).start(); last_mouse=time.time()
        bi=120 if not bsod_done[0] else (random.uniform(120,180) if FINAL_BOSS[0] else random.uniform(300,480))
        if elapsed>90 and time.time()-last_bsod>bi:
            fake_bsod(); bsod_done[0]=True; last_bsod=time.time()
        si=random.uniform(60,120) if FINAL_BOSS[0] else random.uniform(180,360)
        if elapsed>120 and time.time()-last_spam>si:
            threading.Thread(target=spam_launch,daemon=True).start(); last_spam=time.time()
        bri=random.uniform(30,60) if FINAL_BOSS[0] else random.uniform(90,150)
        if elapsed>45 and time.time()-last_browser>bri:
            open_browser_search()
            if FINAL_BOSS[0]: open_browser_search()
            last_browser=time.time()
        if elapsed>60 and time.time()-last_qa_popup>random.uniform(120,240):
            ask_me_why_dialog(); last_qa_popup=time.time()

threading.Thread(target=chaos_loop,daemon=True).start()

# ── Entry point ───────────────────────────────────────────────────────────────
root = tk.Tk()
root.withdraw()
root.after(300, build_bonzi)
root.mainloop()
