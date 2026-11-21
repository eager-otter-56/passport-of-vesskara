#!/usr/bin/env python3
"""Write /output/entry.png: an open passport spread of the Republic of
Vesskara, an island country that does not exist. Pure stdlib drawing."""
import os, struct, zlib, math, random

W, H = 1024, 720
PX = bytearray(W * H * 3)

def put(x, y, c, a=1.0):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        if a >= 1.0:
            PX[i], PX[i + 1], PX[i + 2] = c
        else:
            PX[i] = int(PX[i] * (1 - a) + c[0] * a)
            PX[i + 1] = int(PX[i + 1] * (1 - a) + c[1] * a)
            PX[i + 2] = int(PX[i + 2] * (1 - a) + c[2] * a)

def rect(x0, y0, x1, y1, c, a=1.0):
    for y in range(y0, y1):
        for x in range(x0, x1):
            put(x, y, c, a)

def frame(x0, y0, x1, y1, c, t=2, a=1.0):
    rect(x0, y0, x1, y0 + t, c, a); rect(x0, y1 - t, x1, y1, c, a)
    rect(x0, y0, x0 + t, y1, c, a); rect(x1 - t, y0, x1, y1, c, a)

def line(x0, y0, x1, y1, c, t=1, a=1.0):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k // n; y = y0 + (y1 - y0) * k // n
        for dx in range(t):
            for dy in range(t):
                put(x + dx, y + dy, c, a)

def disc(cx, cy, r, c, a=1.0):
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                put(x, y, c, a)

def ring(cx, cy, r, c, t=2, a=1.0):
    for y in range(cy - r - t, cy + r + t + 1):
        for x in range(cx - r - t, cx + r + t + 1):
            d = math.hypot(x - cx, y - cy)
            if r - t / 2 <= d <= r + t / 2:
                put(x, y, c, a)

def oval(cx, cy, rx, ry, c, a=1.0):
    for y in range(cy - ry, cy + ry + 1):
        for x in range(cx - rx, cx + rx + 1):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                put(x, y, c, a)

FONT = {
 'A':[14,17,17,31,17,17,17],'B':[30,17,17,30,17,17,30],'C':[14,17,16,16,16,17,14],
 'D':[30,17,17,17,17,17,30],'E':[31,16,16,30,16,16,31],'F':[31,16,16,30,16,16,16],
 'G':[14,17,16,23,17,17,15],'H':[17,17,17,31,17,17,17],'I':[14,4,4,4,4,4,14],
 'J':[7,2,2,2,2,18,12],'K':[17,18,20,24,20,18,17],'L':[16,16,16,16,16,16,31],
 'M':[17,27,21,21,17,17,17],'N':[17,25,21,19,17,17,17],'O':[14,17,17,17,17,17,14],
 'P':[30,17,17,30,16,16,16],'Q':[14,17,17,17,21,18,13],'R':[30,17,17,30,20,18,17],
 'S':[15,16,16,14,1,1,30],'T':[31,4,4,4,4,4,4],'U':[17,17,17,17,17,17,14],
 'V':[17,17,17,17,17,10,4],'W':[17,17,17,21,21,27,17],'X':[17,10,4,4,4,10,17],
 'Y':[17,10,4,4,4,4,4],'Z':[31,1,2,4,8,16,31],
 '0':[14,17,19,21,25,17,14],'1':[4,12,4,4,4,4,14],'2':[14,17,1,2,4,8,31],
 '3':[30,1,1,14,1,1,30],'4':[2,6,10,18,31,2,2],'5':[31,16,30,1,1,17,14],
 '6':[6,8,16,30,17,17,14],'7':[31,1,2,4,8,8,8],'8':[14,17,17,14,17,17,14],
 '9':[14,17,17,15,1,2,12],' ':[0,0,0,0,0,0,0],'.':[0,0,0,0,0,12,12],
 ',':[0,0,0,0,12,4,8],'-':[0,0,0,31,0,0,0],'/':[1,1,2,4,8,16,16],
 ':':[0,12,12,0,12,12,0],'(':[2,4,8,8,8,4,2],')':[8,4,2,2,2,4,8],
 '<':[2,4,8,16,8,4,2],'>':[8,4,2,1,2,4,8],"'":[4,4,8,0,0,0,0],
 '&':[12,18,20,8,21,18,13],'No':[0,0,0,0,0,0,0]}

def text(x, y, s, c, sc=2, a=1.0, sp=None):
    if sp is None: sp = sc
    cx = x
    for ch in s.upper():
        g = FONT.get(ch, FONT[' '])
        for r in range(7):
            for col in range(5):
                if g[r] >> (4 - col) & 1:
                    for dx in range(sc):
                        for dy in range(sc):
                            put(cx + col * sc + dx, y + r * sc + dy, c, a)
        cx += 6 * sc + sp
    return cx

def twidth(s, sc=2, sp=None):
    if sp is None: sp = sc
    return len(s) * (6 * sc + sp) - sp

def field(x, y, label, value, navy, ink):
    text(x, y, label, navy, 1)
    text(x, y + 11, value, ink, 2)
    line(x, y + 30, x + 228, y + 30, (178, 172, 152), 1)

def stamp_rect(x, y, w, h, c, lines, seed):
    rnd = random.Random(seed)
    frame(x, y, x + w, y + h, c, 3, 0.82)
    frame(x + 5, y + 5, x + w - 5, y + h - 5, c, 1, 0.7)
    ly = y + 14
    for s, sc in lines:
        text(x + (w - twidth(s, sc)) // 2, ly, s, c, sc, 0.82)
        ly += 7 * sc + 7
    for _ in range(260):
        put(x + rnd.randrange(w), y + rnd.randrange(h), (240, 236, 220), 0.5)

def stamp_round(cx, cy, r, c, l1, l2, l3, seed):
    rnd = random.Random(seed)
    ring(cx, cy, r, c, 3, 0.82); ring(cx, cy, r - 6, c, 1, 0.7)
    text(cx - twidth(l1, 1) // 2, cy - 20, l1, c, 1, 0.85)
    text(cx - twidth(l2, 2) // 2, cy - 6, l2, c, 2, 0.85)
    text(cx - twidth(l3, 1) // 2, cy + 12, l3, c, 1, 0.85)
    for _ in range(200):
        ang = rnd.uniform(0, 6.283); rr = rnd.uniform(0, r)
        put(int(cx + rr * math.cos(ang)), int(cy + rr * math.sin(ang)), (240, 236, 220), 0.5)

def shield(cx, cy, s, navy, gold):
    pts = []
    for i in range(41):
        t = i / 40
        x = cx - 26 * s + 52 * s * t
        y = cy - 30 * s + 8 * s * math.sin(t * math.pi)
        pts.append((int(x), int(y)))
    for i in range(21):
        t = i / 20
        x = cx + 26 * s - 52 * s * t
        y = cy + 4 * s + 34 * s * (1 - abs(t - 0.5) * 0.35) * (t if t < 1 else 1)
        pts.append((int(x), int(cy + 38 * s * math.sin(t * math.pi * 0.5 + 0.2))))
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    for y in range(min(ys), max(ys) + 1):
        row = [x for (x, yy) in pts if yy == y]
        if row:
            rect(min(row), y, max(row), y + 1, navy)
    for k in range(3):
        yy = cy + (2 + k * 9) * s // 1
        line(cx - 20 * s, int(yy), cx + 20 * s, int(yy), gold, max(1, s))
    disc(cx, cy - 12 * s, 7 * s, gold)
    for dx, dy in ((-14, -20), (0, -24), (14, -20)):
        line(cx, cy - 12 * s, cx + dx * s, cy + dy * s, gold, max(1, s - 1))

def portrait(x, y, w, h, ghost=False):
    base = (196, 205, 214) if not ghost else (226, 224, 210)
    rect(x, y, x + w, y + h, base)
    for gy in range(y + 6, y + h, 9):
        line(x + 3, gy, x + w - 3, gy + 3, (170, 182, 196) if not ghost else (205, 200, 180), 1, 0.6)
    skin = (198, 158, 128) if not ghost else (214, 196, 178)
    hair = (74, 52, 40) if not ghost else (170, 160, 148)
    suit = (44, 54, 74) if not ghost else (168, 170, 178)
    cx, cy = x + w // 2, y + int(h * 0.40)
    rect(x + 4, y + h - int(h * 0.26), x + w - 4, y + h, suit)
    oval(cx, y + h - int(h * 0.24), int(w * 0.44), int(h * 0.20), suit)
    rect(cx - 8, y + h - int(h * 0.28), cx + 8, y + h, (232, 230, 224))
    line(cx, y + h - int(h * 0.28), cx, y + h, (150, 40, 44), 3)
    oval(cx, cy, int(w * 0.26), int(h * 0.27), skin)
    oval(cx, cy - int(h * 0.17), int(w * 0.27), int(h * 0.11), hair)
    disc(cx - int(w * 0.09), cy + 2, 2, (40, 32, 28))
    disc(cx + int(w * 0.09), cy + 2, 2, (40, 32, 28))
    line(cx - 4, cy + int(h * 0.10), cx + 5, cy + int(h * 0.10), (150, 96, 84), 2)
    frame(x, y, x + w, y + h, (90, 96, 110), 2)

def main():
    navy = (26, 44, 88); ink = (38, 36, 32); gold = (176, 138, 52)
    rect(0, 0, W, H, (43, 56, 60))
    for i in range(90):
        disc(30 + (i * 173) % 980, 20 + (i * 389) % 690, 1, (58, 72, 76))
    rect(18, 30, 1006, 690, (120, 108, 84))
    rect(24, 36, 1000, 684, (240, 234, 216))
    for gx in range(40, 990, 7):
        for gy in range(52, 672, 7):
            v = int(6 * math.sin(gx * 0.11) * math.cos(gy * 0.09))
            put(gx, gy, (232 + v, 226 + v, 206 + v), 0.35)
    for i in range(120):
        put(506 + i // 20, 40 + i * 5, (198, 190, 168), 0.8)
        put(518 - i // 20, 40 + i * 5, (250, 246, 232), 0.8)
    line(512, 36, 512, 684, (206, 198, 176), 2)

    # left page: data page
    shield(74, 92, 1, navy, gold)
    text(118, 62, "REPUBLIC OF VESSKARA", navy, 2)
    text(120, 84, "PASSPORT", (120, 96, 40), 2)
    text(120, 106, "REIPUBLIK VESKARA - PASSEPORTE", navy, 1)
    line(48, 128, 488, 128, gold, 2)
    text(48, 136, "TYPE P  CODE VKS  PASSPORT NO VK0482716", navy, 1)

    portrait(52, 158, 150, 196)
    fx = 224
    field(fx, 152, "SURNAME", "VOSS", navy, ink)
    field(fx, 196, "GIVEN NAMES", "MARA ELISABETH", navy, ink)
    field(fx, 240, "NATIONALITY", "VESSKARAN", navy, ink)
    field(fx, 284, "DATE OF BIRTH", "14 MAR 1988", navy, ink)
    field(fx, 328, "PLACE OF BIRTH", "PORT LUMEN", navy, ink)
    fy = 386
    text(52, fy, "SEX  F", navy, 1); text(52, fy + 11, "EYES  GREY", navy, 1)
    text(52, fy + 24, "HEIGHT  168 CM", navy, 1)
    text(190, fy, "DATE OF ISSUE", navy, 1); text(190, fy + 11, "03 MAY 2021", ink, 2)
    text(190, fy + 40, "DATE OF EXPIRY", navy, 1); text(190, fy + 51, "03 MAY 2031", ink, 2)
    text(360, fy, "AUTHORITY", navy, 1)
    text(360, fy + 11, "HARBOUR", ink, 1); text(360, fy + 22, "REGISTRY", ink, 1)
    text(360, fy + 33, "PORT LUMEN", ink, 1)
    # signature: a flowing scribble
    pts = [(58, 486), (84, 462), (104, 492), (128, 458), (150, 486), (176, 466), (196, 484), (228, 470), (258, 488), (292, 472)]
    for i in range(len(pts) - 1):
        line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], (30, 34, 70), 2)
    line(52, 496, 300, 496, (178, 172, 152), 1)
    text(52, 502, "SIGNATURE OF HOLDER", navy, 1)
    portrait(392, 448, 62, 80, ghost=True)
    text(392, 534, "VK0482716", navy, 1)
    # MRZ band
    rect(36, 560, 488, 672, (250, 248, 240))
    frame(36, 560, 488, 672, (150, 144, 124), 1)
    mrz1 = "P<VKSVOSS<<MARA<ELISABETH<<<<<<<<<<<<"
    mrz2 = "VK0482716<4VKS8803145F3105038<<<<<<<06"
    text(48, 592, mrz1[:38], (30, 30, 30), 2, 1.0, -1)
    text(48, 624, mrz2[:38], (30, 30, 30), 2, 1.0, -1)
    text(52, 570, "MACHINE READABLE ZONE", (150, 144, 124), 1)

    # right page: visas
    text(560, 58, "VISAS", navy, 3)
    text(560, 86, "ENDORSEMENTS AND BORDER STAMPS", navy, 1)
    line(544, 128, 976, 128, gold, 2)
    text(920, 58, "24", navy, 2)
    stamp_rect(566, 156, 252, 104, (36, 74, 160),
               [("KORDAVIA", 2), ("ARRIVAL - OSTROV PORT", 1), ("17 JUN 2023", 2)], 11)
    stamp_round(904, 208, 62, (122, 44, 140), "THALASSIA", "DEPARTED", "02 SEP 2023", 23)
    stamp_rect(596, 300, 268, 104, (178, 42, 42),
               [("MERIDIAN UNION", 2), ("ENTRY - CALDER CROSSING", 1), ("28 NOV 2024", 2)], 37)
    stamp_round(902, 356, 58, (30, 116, 74), "VESSKARA", "EXIT", "09 JAN 2025", 41)
    stamp_rect(566, 440, 220, 88, (36, 74, 160),
               [("KORDAVIA", 2), ("DEPARTED", 1), ("11 JAN 2025", 1)], 53)
    # tide permit card: the paperwork detail that reveals the place
    rect(800, 452, 984, 640, (146, 128, 92))
    rect(806, 446, 978, 634, (246, 238, 214))
    frame(806, 446, 978, 634, (146, 128, 92), 2)
    text(822, 462, "TIDE PERMIT", (150, 40, 44), 2)
    text(822, 486, "No 311", (150, 40, 44), 1)
    line(822, 502, 962, 502, gold, 2)
    for i, s in enumerate(["HOLDER MAY BOARD THE", "PORT LUMEN FERRY ONLY", "AT HIGH TIDE. THE REEL", "CHANNEL IS DRY AT LOW", "WATER - NO ROAD LEAVES", "THE ISLAND.", "", "VALID FOR TRAVEL", "BY SEA ONLY."]):
        if s: text(822, 514 + i * 13, s, ink, 1)
    disc(950, 614, 11, (150, 40, 44), 0.85)
    text(944, 608, "VK", (250, 246, 232), 1)

    os.makedirs("/output", exist_ok=True)
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += PX[y * W * 3:(y + 1) * W * 3]
    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open("/output/entry.png", "wb") as f:
        f.write(png)

if __name__ == "__main__":
    main()
