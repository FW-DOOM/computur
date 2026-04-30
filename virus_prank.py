import tkinter as tk
import random
import threading
import time
import math

MEMES = [
    "YIKES", "L + RATIO", "GET REKT", "SKILL ISSUE", "COPE HARDER",
    "NO CAP FR FR", "BRUH MOMENT", "IT'S JOEVER", "CAUGHT IN 4K",
    "W RIZZ", "SUSSY BAKA", "BASED", "TOUCH GRASS", "GG EZ",
    "YOU JUST LOST", "BRO IS COOKED", "NOT REAL", "THE GOAT",
    "SHEESH", "LOWKEY COOKED", "FR THO", "NGL THOUGH", "POOKIE",
    "ABSOLUTE W", "RENT FREE", "MAIN CHARACTER", "CERTIFIED HOOD CLASSIC",
    "UNALIVED", "DOWN BAD", "UNDERSTOOD THE ASSIGNMENT",
]

ERRORS = [
    ("Windows Security", "Threat found: Trojan:Win32/Wacatac.H!ml\nSeverity: Severe | Status: Active\nRegistry changes detected."),
    ("Disk Failure", "SMART Failure on Disk 0: WDC WD10EZEX\nFailure imminent. Error: 0x800701E3"),
    ("System Critical", "Stop: 0x0000007E — SYSTEM_THREAD_EXCEPTION\nntoskrnl.exe failed. Dump saved."),
    ("Memory Error", "Memory corruption at 0xFFFFFA8003B2C000\nContact hardware manufacturer."),
    ("Windows Defender", "Ransom:Win32/Petya.A active on your system.\nFile: C:\\Windows\\System32\\lsass.exe"),
    ("Drive Error", "Disk read error: \\Windows\\system32\\winload.exe\nStatus: 0xc000000e — File corrupt."),
    ("Network Alert", "Unauthorized access from 185.220.101.47\nFirewall rule violation: svchost.exe PID 4812"),
    ("Boot Critical", "File: \\Windows\\system32\\drivers\\ntfs.sys\nStatus: 0xc000014c — Unrecoverable volume error"),
]

root = tk.Tk()
root.withdraw()

SW = root.winfo_screenwidth()
SH = root.winfo_screenheight()

chaos_running = [False]
bouncing_windows = []

# ---- BOUNCING MEME WINDOWS ----
class BouncingWindow:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)

        w = random.randint(120, 220)
        h = random.randint(55, 90)
        self.x = random.uniform(0, SW - w)
        self.y = random.uniform(0, SH - h)
        self.dx = random.uniform(-14, 14)
        self.dy = random.uniform(-12, 12)
        if abs(self.dx) < 4: self.dx = 4 * (1 if self.dx >= 0 else -1)
        if abs(self.dy) < 4: self.dy = 4 * (1 if self.dy >= 0 else -1)
        self.w = w
        self.h = h

        colors = ["#ff0000","#ff6600","#ffcc00","#00cc00","#0099ff","#cc00ff","#ff0099","#ffffff"]
        bg = random.choice(colors)
        fg = "#000000" if bg in ["#ffcc00","#ffffff","#00cc00"] else "#ffffff"

        self.win.configure(bg=bg)
        self.win.geometry(f"{w}x{h}+{int(self.x)}+{int(self.y)}")

        text = random.choice(MEMES)
        tk.Label(self.win, text=text, font=("Impact", random.randint(14, 22), "bold"),
                 bg=bg, fg=fg, wraplength=w-10).pack(expand=True)

        bouncing_windows.append(self)
        self.move()

    def move(self):
        if not chaos_running[0]:
            try: self.win.destroy()
            except: pass
            return
        self.x += self.dx
        self.y += self.dy
        if self.x <= 0 or self.x + self.w >= SW:
            self.dx *= -1
            self.x = max(0, min(SW - self.w, self.x))
        if self.y <= 0 or self.y + self.h >= SH:
            self.dy *= -1
            self.y = max(0, min(SH - self.h, self.y))
        try:
            self.win.geometry(f"{self.w}x{self.h}+{int(self.x)}+{int(self.y)}")
            self.win.after(16, self.move)
        except:
            pass

# ---- ERROR POPUPS ----
def spawn_error():
    title, msg = random.choice(ERRORS)
    win = tk.Toplevel()
    win.title(title)
    win.attributes("-topmost", True)
    win.resizable(False, False)
    win.configure(bg="#1a1a1a")
    win.geometry(f"400x180+{random.randint(0,SW-400)}+{random.randint(0,SH-180)}")

    tk.Label(win, text="⛔  " + title, font=("Segoe UI", 10, "bold"),
             bg="#1a1a1a", fg="#ff4444").pack(anchor="w", padx=10, pady=6)
    tk.Frame(win, height=1, bg="#444").pack(fill="x")
    tk.Label(win, text=msg, font=("Consolas", 8), bg="#1a1a1a", fg="#ffaaaa",
             justify="left", wraplength=380).pack(padx=10, pady=6)

    def close_and_more():
        win.destroy()
        for _ in range(random.randint(3, 6)):
            root.after(random.randint(50, 300), spawn_error)

    win.protocol("WM_DELETE_WINDOW", close_and_more)
    tk.Button(win, text="OK", command=close_and_more,
              bg="#333", fg="white", font=("Segoe UI", 9), relief="flat").pack(pady=4)

# ---- CHAOS SPAWNER ----
def start_chaos():
    chaos_running[0] = True

    def run():
        # spawn bouncing memes
        for _ in range(30):
            root.after(random.randint(0, 2000), BouncingWindow)

        # keep spawning more bouncing windows
        def keep_bouncing():
            while chaos_running[0]:
                time.sleep(0.4)
                root.after(0, BouncingWindow)
        threading.Thread(target=keep_bouncing, daemon=True).start()

        # flood with errors 10 per second
        def keep_erroring():
            while chaos_running[0]:
                time.sleep(0.1)
                root.after(0, spawn_error)
        threading.Thread(target=keep_erroring, daemon=True).start()

    threading.Thread(target=run, daemon=True).start()

# ---- INITIAL VIRUS POPUP ----
def show_virus_alert():
    alert = tk.Toplevel()
    alert.title("Windows Security")
    alert.attributes("-topmost", True)
    alert.resizable(False, False)
    alert.geometry(f"480x280+{SW//2-240}+{SH//2-140}")
    alert.configure(bg="#1e1e1e")
    alert.protocol("WM_DELETE_WINDOW", lambda: None)

    # header
    header = tk.Frame(alert, bg="#cc0000", height=45)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(header, text="  ⚠  WINDOWS SECURITY ALERT",
             font=("Segoe UI", 13, "bold"), bg="#cc0000", fg="white").pack(side="left", pady=8)

    body = tk.Frame(alert, bg="#1e1e1e")
    body.pack(fill="both", expand=True, padx=15, pady=10)

    tk.Label(body, text="CRITICAL THREAT DETECTED",
             font=("Segoe UI", 12, "bold"), bg="#1e1e1e", fg="#ff4444").pack(anchor="w")

    info = (
        "Threat:    Trojan:Win32/Wacatac.H!ml\n"
        "Severity:  ████████ SEVERE\n"
        "Status:    ACTIVE — Spreading\n"
        "Files at risk:  1,847 personal files\n\n"
        "Recommended action: Immediate removal required.\n"
        "Your passwords and files may be compromised."
    )
    tk.Label(body, text=info, font=("Consolas", 9), bg="#1e1e1e", fg="#ffbbbb",
             justify="left").pack(anchor="w", pady=6)

    tk.Frame(alert, height=1, bg="#444").pack(fill="x")

    btn_frame = tk.Frame(alert, bg="#1e1e1e")
    btn_frame.pack(pady=12)

    def big_mistake():
        alert.destroy()
        start_chaos()

    tk.Button(btn_frame, text="I'm stupid help me",
              command=big_mistake,
              bg="#cc0000", fg="white",
              font=("Segoe UI", 12, "bold"),
              relief="flat", padx=20, pady=8,
              cursor="hand2").pack()

    tk.Label(alert, text="Windows Security  |  Protected by Microsoft Defender",
             font=("Segoe UI", 7), bg="#1e1e1e", fg="#555555").pack(pady=(0, 4))

root.after(500, show_virus_alert)
root.mainloop()
