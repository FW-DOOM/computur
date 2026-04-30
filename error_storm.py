import tkinter as tk
import random
import threading
import time
import os
import ctypes

# ── beep via Windows API (always in its own thread so it never blocks) ──
def beep(freq=1000, dur=100):
    try: ctypes.windll.kernel32.Beep(freq, dur)
    except: pass

def alarm():
    threading.Thread(target=lambda: [beep(1200,80), time.sleep(0.13), beep(800,80)], daemon=True).start()

def scream():
    def _s():
        for f in [300,480,600,780,900,1100,800,500]:
            beep(f,55); time.sleep(0.05)
    threading.Thread(target=_s, daemon=True).start()

ERRORS = [
    ("Microsoft Windows", "Windows has detected a hard disk problem.\n\nBack up your files immediately.\nError: 0x00000024  NTFS_FILE_SYSTEM"),
    ("Windows Security", "Threat found: Trojan:Win32/Wacatac.H!ml\nSeverity: Severe  |  Status: Active\nRegistry changes detected."),
    ("Windows — No Disk", "Exception Processing Message 0xc0000013\nParameters 0x75B6BF9C  0x4  0x75B6BF9C\n\nPlease insert a disk into drive C:."),
    ("Windows Memory Diagnostic", "Memory corruption at 0xFFFFFA8003B2C000\n\nContact your hardware manufacturer."),
    ("System — Critical", "Stop: 0x0000007E (0xFFFFFFFFC0000005,\n0xFFFFF80002A3B5A0, 0xFFFFF98000C79480)"),
    ("Windows Defender", "CRITICAL: Ransom:Win32/Petya.A detected.\nFile: C:\\Windows\\System32\\lsass.exe\nRestart now to complete removal."),
    ("Drive Health Warning", "SMART Failure Predicted — WDC WD10EZEX\nFailure imminent. Error: 0x800701E3"),
    ("Windows — System Error", "Memory at 0x00000010 could not be 'read'.\n\nClick OK to terminate the program."),
    ("Windows Update", "Update failed — Error code: 0x800f0900\nSystem reverting. Do not turn off PC."),
    ("NVIDIA Display Driver", "nvlddmkm stopped responding. Event ID: 4101\nSystem stability compromised."),
    ("Windows — Corrupted File", "Resource Protection found corrupt files\nbut was UNABLE to fix them.\nError: STATUS_ACCESS_VIOLATION"),
    ("Disk Error", "File: \\Windows\\system32\\winload.exe\nStatus: 0xc000000e — Missing or corrupt."),
    ("Security Alert", "Firewall breach: svchost.exe PID 4812\nUnauthorized access: 185.220.101.47"),
    ("Event Viewer — Critical", "Bugcheck: 0x0000009f\nDump: C:\\Windows\\MEMORY.DMP"),
    ("Windows — Low Memory", "Available physical memory: 14 MB\nClose all programs immediately."),
    ("Boot Error", "Boot file corrupt: ntfs.sys\nStatus: 0xc000014c — Volume error."),
    ("Windows Activation", "Not activated. Error: 0xC004F074\nPersonal files deleted in 3 days."),
    ("Network Error", "DNS server not responding.\nNetwork adapter may be damaged."),
    ("Application Error", "chrome.exe stopped working.\nFault offset: 0x000000000325c5c4"),
    ("System32 Integrity", "C:\\Windows\\System32\\hal.dll — Hash mismatch.\nSystem integrity compromised."),
]

POPUP_W, POPUP_H = 400, 200
SPAWN_PER_SEC = 4      # 4 per second — still chaotic, won't freeze PC
MAX_WINDOWS   = 20     # hard cap so memory doesn't explode
open_windows = []
lock = threading.Lock()

root = tk.Tk()
root.withdraw()
root.update()
SW = root.winfo_screenwidth()
SH = root.winfo_screenheight()

total_sec = [300]
countdown_running = [True]
warned_shown = [False]

# ── COUNTDOWN WINDOW ──
cwin = tk.Toplevel()
cwin.overrideredirect(True)
cwin.attributes("-topmost", True)
cwin.configure(bg="#1a0000")
CW, CH = 420, 90
cwin.geometry(f"{CW}x{CH}+{SW//2 - CW//2}+0")
cwin.protocol("WM_DELETE_WINDOW", lambda: None)

c_label = tk.Label(cwin, text="⚠  FILE ENCRYPTION BEGINS IN",
                   font=("Segoe UI", 10, "bold"), bg="#1a0000", fg="#ff5555")
c_label.pack(pady=(8,0))

c_timer = tk.Label(cwin, text="05:00",
                   font=("Consolas", 36, "bold"), bg="#1a0000", fg="#ff1111")
c_timer.pack()

c_sub = tk.Label(cwin, text="Files will be permanently encrypted",
                 font=("Segoe UI", 8), bg="#1a0000", fg="#883333")
c_sub.pack()

# ── FAKE BSOD ──
def fake_bsod():
    bsod = tk.Toplevel()
    bsod.attributes("-fullscreen", True)
    bsod.attributes("-topmost", True)
    bsod.configure(bg="#0000aa")
    bsod.overrideredirect(True)

    frame = tk.Frame(bsod, bg="#0000aa")
    frame.place(relx=0.12, rely=0.18)
    tk.Label(frame, text=":(", font=("Consolas", 90, "bold"), fg="white", bg="#0000aa").pack(anchor="w")
    tk.Label(frame,
        text="\nYour PC ran into a problem and needs to restart.\nWe're just collecting some error info, and then\nwe'll restart for you.",
        font=("Consolas", 19), fg="white", bg="#0000aa", justify="left").pack(anchor="w")
    pct_label = tk.Label(frame, text="0% complete", font=("Consolas", 19), fg="white", bg="#0000aa")
    pct_label.pack(anchor="w", pady=(15,0))

    bot = tk.Frame(bsod, bg="#0000aa")
    bot.place(relx=0.12, rely=0.72)
    tk.Label(bot, text="Stop code:  CRITICAL_PROCESS_DIED",
             font=("Consolas", 14, "bold"), fg="white", bg="#0000aa").pack(anchor="w")
    tk.Label(bot, text="What failed:  ntoskrnl.exe",
             font=("Consolas", 12), fg="white", bg="#0000aa").pack(anchor="w")

    pct = [0]
    def count_up():
        while pct[0] < 100:
            time.sleep(random.uniform(0.04, 0.1))
            pct[0] = min(pct[0] + random.randint(1,4), 100)
            try: pct_label.config(text=f"{pct[0]}% complete")
            except: return
        time.sleep(2)
        try: bsod.destroy()
        except: pass
        # reboot back into chaos with 60s
        total_sec[0] = 60
        warned_shown[0] = False
        countdown_running[0] = True
        for _ in range(20):
            root.after(random.randint(0, 500), make_error_window)

    threading.Thread(target=count_up, daemon=True).start()
    bsod.protocol("WM_DELETE_WINDOW", lambda: None)
    threading.Thread(target=scream, daemon=True).start()


# ── I WARNED YOU SCREEN ──
def show_warned():
    warned_shown[0] = True
    for w in list(open_windows):
        try: w.destroy()
        except: pass
    open_windows.clear()

    warned = tk.Toplevel()
    warned.attributes("-fullscreen", True)
    warned.attributes("-topmost", True)
    warned.overrideredirect(True)
    warned.configure(bg="#ff0000")
    warned.protocol("WM_DELETE_WINDOW", lambda: None)

    frame = tk.Frame(warned, bg="#ff0000")
    frame.place(relx=0.5, rely=0.35, anchor="center")

    title = tk.Label(frame, text="I WARNED YOU",
                     font=("Impact", 96, "bold"), fg="white", bg="#ff0000")
    title.pack()
    tk.Label(frame, text="You ignored every warning.\nYour files are now being permanently destroyed.",
             font=("Segoe UI", 18, "bold"), fg="#ffbbbb", bg="#ff0000", justify="center").pack(pady=16)

    stats_frame = tk.Frame(warned, bg="#ff0000")
    stats_frame.place(relx=0.5, rely=0.62, anchor="center")

    files_lbl  = tk.Label(stats_frame, text="0 files deleted",  font=("Consolas", 14), fg="#ffcccc", bg="#ff0000")
    reg_lbl    = tk.Label(stats_frame, text="0 registry keys wiped", font=("Consolas", 14), fg="#ffcccc", bg="#ff0000")
    mb_lbl     = tk.Label(stats_frame, text="0 MB lost", font=("Consolas", 14), fg="#ffcccc", bg="#ff0000")
    files_lbl.pack(); reg_lbl.pack(); mb_lbl.pack()

    files_n, reg_n, mb_n = [0], [0], [0]
    running_w = [True]
    def tick_stats():
        while running_w[0]:
            files_n[0] += random.randint(20,80)
            reg_n[0]   += random.randint(5,25)
            mb_n[0]    += random.randint(3,15)
            try:
                files_lbl.config(text=f"{files_n[0]:,} files deleted")
                reg_lbl.config(text=f"{reg_n[0]:,} registry keys wiped")
                mb_lbl.config(text=f"{mb_n[0]:,} MB lost")
            except: break
            time.sleep(0.35)
    threading.Thread(target=tick_stats, daemon=True).start()

    # flash background
    colors = ["#ff0000","#cc0000"]
    ci = [0]
    def flash_bg():
        if not running_w[0]: return
        ci[0] = 1 - ci[0]
        try:
            warned.configure(bg=colors[ci[0]])
            frame.configure(bg=colors[ci[0]])
            stats_frame.configure(bg=colors[ci[0]])
            for w in warned.winfo_children(): _set_bg(w, colors[ci[0]])
        except: pass
        warned.after(400, flash_bg)
    def _set_bg(w, c):
        try: w.configure(bg=c)
        except: pass
        for ch in w.winfo_children(): _set_bg(ch, c)
    warned.after(400, flash_bg)

    # screaming loop
    def scream_loop():
        while running_w[0]:
            scream(); time.sleep(1.6)
    threading.Thread(target=scream_loop, daemon=True).start()

    # BIG factory reset button
    btn_frame = tk.Frame(warned, bg="#ff0000")
    btn_frame.place(relx=0.5, rely=0.82, anchor="center")

    def do_reset():
        running_w[0] = False
        warned.destroy()
        fake_bsod()

    tk.Button(btn_frame,
              text="  ⚠   EMERGENCY FACTORY RESET   ⚠  ",
              command=do_reset,
              bg="#000000", fg="#ff0000",
              font=("Segoe UI", 16, "bold"),
              relief="flat", pady=18, padx=30,
              cursor="hand2").pack()

    tk.Label(warned, text="type 4308 to exit",
             font=("Segoe UI", 9), fg="#ff3333", bg="#ff0000").pack(side="bottom", pady=6)


# ── FACTORY RESET POPUP ──
def show_factory_reset_popup():
    popup = tk.Toplevel()
    popup.title("⚠ CRITICAL — Action Required")
    popup.attributes("-topmost", True)
    popup.resizable(False, False)
    popup.configure(bg="#0d0d0d")
    popup.geometry(f"520x290+{SW//2-260}+{SH//2-145}")
    popup.protocol("WM_DELETE_WINDOW", lambda: None)

    tk.Frame(popup, bg="#cc0000", height=8).pack(fill="x")
    tk.Label(popup, text="⚠  SYSTEM CANNOT BE RECOVERED",
             font=("Segoe UI", 14, "bold"), bg="#0d0d0d", fg="#ff3333").pack(pady=(16,4))
    tk.Label(popup,
             text="Critical system processes have failed.\nYour personal files and Windows installation are at risk.\n\nThe ONLY safe option is a Factory Reset.",
             font=("Segoe UI", 10), bg="#0d0d0d", fg="#ffaaaa", justify="center").pack(pady=6)
    tk.Frame(popup, bg="#444", height=1).pack(fill="x", padx=20)

    def do_reset():
        popup.destroy()
        fake_bsod()

    tk.Button(popup,
              text="  ⚠   FACTORY RESET  —  Recommended   ⚠  ",
              command=do_reset,
              bg="#cc0000", fg="white",
              font=("Segoe UI", 13, "bold"),
              relief="flat", pady=14, cursor="hand2").pack(fill="x", padx=30, pady=16)
    tk.Label(popup, text="This window cannot be closed.",
             font=("Segoe UI", 8), bg="#0d0d0d", fg="#444").pack()


# ── ERROR POPUP ──
def make_error_window():
    if warned_shown[0]: return
    with lock:
        if len(open_windows) >= MAX_WINDOWS:
            return   # hard cap — don't create more until some are closed
    title, msg = random.choice(ERRORS)
    win = tk.Toplevel()
    win.title(title)
    win.attributes("-topmost", True)
    win.resizable(False, False)
    win.configure(bg="#f0f0f0")

    x = random.randint(0, max(1, SW - POPUP_W))
    y = random.randint(30, max(31, SH - POPUP_H))
    win.geometry(f"{POPUP_W}x{POPUP_H}+{x}+{y}")

    top = tk.Frame(win, bg="#f0f0f0")
    top.pack(fill="x", padx=10, pady=8)
    tk.Label(top, text="⛔", font=("Segoe UI", 22), bg="#f0f0f0").pack(side="left", padx=6)
    tk.Label(top, text=msg, font=("Segoe UI", 9), bg="#f0f0f0",
             fg="#222", justify="left", wraplength=320).pack(side="left", padx=4)

    tk.Frame(win, height=1, bg="#ccc").pack(fill="x")
    btn_frame = tk.Frame(win, bg="#f0f0f0")
    btn_frame.pack(pady=8, fill="x", padx=10)

    def on_ok():
        with lock:
            if win in open_windows: open_windows.remove(win)
        win.destroy()
        # spawn 2-3 more, staggered so they don't all hit at once
        for i in range(random.randint(2, 3)):
            root.after(i * 300, make_error_window)

    tk.Button(btn_frame, text="OK", command=on_ok, width=8, font=("Segoe UI", 9)).pack(side="left", padx=4)
    tk.Button(btn_frame,
              text="⚠ FACTORY RESET",
              command=lambda: [on_ok(), show_factory_reset_popup()],
              bg="#cc0000", fg="white", font=("Segoe UI", 9, "bold"),
              relief="raised", padx=10).pack(side="left", padx=4)

    # X button: show factory reset popup but ALSO free the slot so spawning continues
    def on_x():
        with lock:
            if win in open_windows: open_windows.remove(win)
        win.destroy()
        root.after(200, make_error_window)   # replace the closed one
        show_factory_reset_popup()

    win.protocol("WM_DELETE_WINDOW", on_x)
    with lock: open_windows.append(win)

    # ── AUTO-CLOSE after 9-14 seconds so the cap never gets permanently full ──
    auto_delay = random.randint(9000, 14000)
    def auto_close():
        try:
            with lock:
                if win in open_windows: open_windows.remove(win)
            win.destroy()
            # replace with 2 fresh ones
            root.after(100, make_error_window)
            root.after(400, make_error_window)
        except: pass
    win.after(auto_delay, auto_close)


# ── COUNTDOWN LOGIC ──
def run_countdown():
    beep_delay = [2500]
    last_beep  = [time.time()]

    def do_beep():
        while True:
            time.sleep(0.25)   # check 4x/sec instead of 10x/sec
            if time.time() - last_beep[0] >= beep_delay[0]/1000:
                alarm()        # already spins its own thread
                last_beep[0] = time.time()

    threading.Thread(target=do_beep, daemon=True).start()

    while countdown_running[0]:
        time.sleep(1)
        if not countdown_running[0]: break
        total_sec[0] -= 1
        s = total_sec[0]

        m = s // 60
        sec = s % 60
        txt = f"{m:02d}:{sec:02d}"

        # escalate
        if s == 120: beep_delay[0] = 1800
        if s == 60:
            beep_delay[0] = 900
            try: c_timer.config(font=("Consolas", 42, "bold"))
            except: pass
            threading.Thread(target=scream, daemon=True).start()
        if s == 30:
            beep_delay[0] = 500
            try: c_timer.config(fg="#ff0000")
            except: pass
        if s <= 10:
            beep_delay[0] = 250
            threading.Thread(target=scream, daemon=True).start()

        # flash countdown box red when <=10
        if s <= 10:
            try: cwin.configure(bg="#ff0000" if s%2==0 else "#880000")
            except: pass

        try:
            c_timer.config(text=txt)
        except: pass

        if s <= 0:
            countdown_running[0] = False
            root.after(0, show_warned)
            return

threading.Thread(target=run_countdown, daemon=True).start()

# ── SPAWN LOOP ──
def spawn_loop():
    while True:
        time.sleep(1.0 / SPAWN_PER_SEC)
        if not warned_shown[0]:
            root.after(0, make_error_window)

threading.Thread(target=spawn_loop, daemon=True).start()

# ── SECRET EXIT ──
secret = [0]
sequence = ['4','3','0','8']
def on_secret_key(event):
    if event.char == sequence[secret[0]]:
        secret[0] += 1
        if secret[0] == 4: os._exit(0)
    else: secret[0] = 0
root.bind_all("<Key>", on_secret_key)

root.mainloop()
