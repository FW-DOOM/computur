import tkinter as tk
import random
import math

root = tk.Tk()
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.overrideredirect(True)
root.configure(bg="black")

canvas = tk.Canvas(root, bg="#0a0500", highlightthickness=0)
canvas.pack(fill="both", expand=True)

W = root.winfo_screenwidth()
H = root.winfo_screenheight()

def crack(x, y, length, angle, depth, thickness=1):
    if depth == 0 or length < 3:
        return
    rad = math.radians(angle)
    # slight wobble for realism
    wobble_x = random.uniform(-4, 4)
    wobble_y = random.uniform(-4, 4)
    x2 = x + math.cos(rad) * length + wobble_x
    y2 = y + math.sin(rad) * length + wobble_y
    shade = random.choice(["#ffffff", "#dddddd", "#eeeeee", "#cccccc", "#ffffff"])
    canvas.create_line(x, y, x2, y2, fill=shade, width=max(1, thickness), capstyle="round")

    # main branch continues
    crack(x2, y2, length * random.uniform(0.55, 0.82),
          angle + random.uniform(-15, 15), depth - 1, max(1, thickness - 0.4))

    # side branches
    num_branches = random.randint(0, 2) if depth > 3 else random.randint(0, 1)
    for _ in range(num_branches):
        branch_angle = angle + random.uniform(-70, 70)
        branch_len = length * random.uniform(0.3, 0.65)
        crack(x2, y2, branch_len, branch_angle, depth - 2, max(1, thickness - 0.8))

def add_impact(ix, iy, num_arms=14, thickness=3):
    # impact ring
    r1 = random.randint(10, 22)
    r2 = random.randint(25, 45)
    canvas.create_oval(ix-r1, iy-r1, ix+r1, iy+r1, outline="#ffffff", width=2)
    canvas.create_oval(ix-r2, iy-r2, ix+r2, iy+r2, outline="#aaaaaa", width=1)

    for i in range(num_arms):
        angle = (360 / num_arms) * i + random.uniform(-10, 10)
        length = random.randint(120, 320)
        depth = random.randint(7, 10)
        crack(ix, iy, length, angle, depth, thickness)

# 3 impact points like the reference
impacts = [
    (int(W * 0.28), int(H * 0.30)),
    (int(W * 0.55), int(H * 0.52)),
    (int(W * 0.74), int(H * 0.60)),
]

for ix, iy in impacts:
    add_impact(ix, iy, num_arms=random.randint(10, 16), thickness=random.uniform(2, 4))

# scattered glass fragment dots
for _ in range(1800):
    px = random.randint(0, W)
    py = random.randint(0, H)
    r = random.randint(1, 3)
    brightness = random.choice(["#ffffff", "#dddddd", "#aaaaaa", "#888888"])
    if random.random() < 0.6:
        canvas.create_oval(px, py, px+r, py+r, fill=brightness, outline="")
    else:
        canvas.create_rectangle(px, py, px+2, py+2, fill=brightness, outline="")

# very faint dark vignette corners
for i in range(30):
    alpha_color = f"#{hex(8 + i)[2:]:0>2}{hex(4 + i//2)[2:]:0>2}00"
    canvas.create_rectangle(i*3, i*3, W-i*3, H-i*3, outline=alpha_color)

secret = [0]
sequence = [str(d) for d in [4, 3, 0, 8]]
def on_key(event):
    ch = event.char
    if ch == sequence[secret[0]]:
        secret[0] += 1
        if secret[0] == len(sequence):
            root.destroy()
    else:
        secret[0] = 0
root.bind("<Key>", on_key)
root.mainloop()
