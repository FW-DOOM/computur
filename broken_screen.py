import tkinter as tk
import random
import math

root = tk.Tk()
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.overrideredirect(True)
root.configure(bg="black")

canvas = tk.Canvas(root, bg="#000000", highlightthickness=0)
canvas.pack(fill="both", expand=True)

W = root.winfo_screenwidth()
H = root.winfo_screenheight()

def ri(a, b): return random.randint(a, b)
def rf(a, b): return random.uniform(a, b)

impacts = [
    (int(W * 0.26), int(H * 0.30)),
    (int(W * 0.55), int(H * 0.53)),
    (int(W * 0.74), int(H * 0.62)),
]

# ── 1. LCD color bleed columns ──
LCD_COLORS = [
    "#ff0000", "#ff0000",
    "#00ff00", "#00ff00",
    "#0000ff", "#0000ff",
    "#00ffff",
    "#ff00ff",
    "#ffff00",
    "#ff8800",
    "#ffffff", "#ffffff",
    "#8800ff",
    "#ff0088",
    "#000000", "#000000", "#000000",  # dead black — frequent
]

def dist_to_nearest_impact(x):
    return min(math.sqrt((x - ix)**2 + (H/2 - iy)**2) for ix, iy in impacts)

x = 0
max_dist = math.sqrt(W**2 + H**2) * 0.85
while x < W:
    col_w = ri(1, 7)
    color  = random.choice(LCD_COLORS)
    d      = dist_to_nearest_impact(x)
    alpha  = max(0.05, 1.0 - (d / max_dist) * 0.6)

    if color == "#000000":
        # draw as black rectangle (always opaque enough)
        canvas.create_rectangle(x, 0, x + col_w, H, fill="#000000", outline="")
    else:
        # tkinter has no alpha on canvas shapes — approximate with stipple
        if alpha > 0.7:
            stipple = ""
        elif alpha > 0.45:
            stipple = "gray75"
        elif alpha > 0.25:
            stipple = "gray50"
        else:
            stipple = "gray25"
        canvas.create_rectangle(x, 0, x + col_w, H,
                                 fill=color, outline="", stipple=stipple)
    x += col_w

# ── 2. Horizontal overexposed bands ──
for _ in range(ri(4, 8)):
    by = ri(0, H)
    bh = ri(15, 90)
    color = random.choice(["#cce4ff", "#ffffff", "#ddeeff"])
    canvas.create_rectangle(0, by, W, by + bh,
                             fill=color, outline="", stipple="gray50")

# ── 3. Dark dead zones at impact centers ──
for ix, iy in impacts:
    radius = ri(90, 160)
    steps  = 18
    for s in range(steps):
        frac    = s / steps
        r_now   = int(radius * (1 - frac))
        if r_now <= 0: break
        opacity = int(200 * (1 - frac))   # 0-255 scale — fake with stipple
        stipple = "gray75" if frac < 0.4 else "gray50" if frac < 0.7 else "gray25"
        x0, y0 = ix - r_now, iy - r_now
        x1, y1 = ix + r_now, iy + r_now
        canvas.create_oval(x0, y0, x1, y1, fill="#000000",
                           outline="", stipple=stipple)

# ── 4. Crack lines ──
def draw_crack(x, y, length, angle, depth, thickness):
    if depth == 0 or length < 3:
        return
    rad = math.radians(angle)
    x2  = x + math.cos(rad) * length + rf(-3, 3)
    y2  = y + math.sin(rad) * length + rf(-3, 3)
    da  = min(1.0, depth / 7)
    lw  = max(1, int(thickness))

    # glow (light blue tint — draw wide, low stipple)
    if lw >= 2:
        canvas.create_line(x, y, x2, y2,
                           fill="#88bbff", width=lw + 4,
                           capstyle=tk.ROUND, stipple="gray25")

    # red chromatic aberration offset
    canvas.create_line(x + 2, y + 1, x2 + 2, y2 + 1,
                       fill="#ff3333", width=lw,
                       capstyle=tk.ROUND, stipple="gray50")

    # blue chromatic aberration offset
    canvas.create_line(x - 2, y - 1, x2 - 2, y2 - 1,
                       fill="#3366ff", width=lw,
                       capstyle=tk.ROUND, stipple="gray50")

    # white core
    canvas.create_line(x, y, x2, y2,
                       fill="#ffffff", width=max(1, lw - 1),
                       capstyle=tk.ROUND)

    # recurse
    draw_crack(x2, y2,
               length * rf(0.55, 0.82),
               angle  + rf(-14, 14),
               depth - 1,
               max(0.5, thickness - 0.35))

    nb = ri(1, 3) if depth > 3 else ri(0, 2)
    for _ in range(nb):
        draw_crack(x2, y2,
                   length * rf(0.28, 0.62),
                   angle  + rf(-65, 65),
                   depth - 2,
                   max(0.5, thickness - 0.7))

for ix, iy in impacts:
    arms = ri(11, 16)
    for i in range(arms):
        angle = (360 / arms) * i + rf(-12, 12)
        draw_crack(ix, iy, ri(110, 280), angle, ri(7, 10), rf(2.0, 3.5))

# ── 5. Impact rings ──
for ix, iy in impacts:
    for rad, lw, color in [
        (ri(8,  18), 2, "#ffffff"),
        (ri(22, 36), 1, "#aaaaaa"),
        (ri(40, 58), 1, "#555555"),
    ]:
        canvas.create_oval(ix-rad, iy-rad, ix+rad, iy+rad,
                           outline=color, width=lw)
    canvas.create_oval(ix-4, iy-4, ix+4, iy+4, fill="#ffffff", outline="")

# ── 6. Vignette (dark border) ──
steps = 40
for i in range(steps):
    frac = i / steps
    pad  = i * 6
    canvas.create_rectangle(pad, pad, W - pad, H - pad,
                             outline="#000000", width=1,
                             stipple="gray75" if frac < 0.5 else "gray50")

# ── Secret exit: type 4308 ──
secret   = [0]
sequence = ['4', '3', '0', '8']

def on_key(event):
    if event.char == sequence[secret[0]]:
        secret[0] += 1
        if secret[0] == 4:
            root.destroy()
    else:
        secret[0] = 0

root.bind("<Key>", on_key)
root.mainloop()
