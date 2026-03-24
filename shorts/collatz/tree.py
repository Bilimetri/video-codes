from manim import *
import math
from collections import deque

config.pixel_width  = 1080
config.pixel_height = 1920
config.frame_rate   = 60
config.background_color = "#050508"

# ── Ağaç yapısı ──────────────────────────────────────────────────────
def ebeveynler(n, max_val=999999):
    result = []
    if 2 * n <= max_val:
        result.append(2 * n)
    if (n - 1) % 3 == 0:
        m = (n - 1) // 3
        if m >= 1 and m % 2 == 1:
            result.append(m)
    return result

# Seviye sayısı 16'ya çıkarıldı! Ciddi bir işlem gücü gerektirecektir.
MAX_SEV = 16
tree    = {}
seviye  = {1: 0}
visited = {1}
queue   = deque([1])

while queue:
    n = queue.popleft()
    if seviye[n] >= MAX_SEV:
        tree[n] = []
        continue
    children = [c for c in ebeveynler(n) if c not in visited]
    tree[n]  = children
    for c in children:
        visited.add(c)
        seviye[c] = seviye[n] + 1
        queue.append(c)

all_nodes = []
q2 = deque([1])
seen = {1}
while q2:
    n = q2.popleft()
    all_nodes.append(n)
    for c in tree.get(n, []):
        if c not in seen:
            seen.add(c)
            q2.append(c)

# ── Polar koordinat hesabı ─────────────────────────────────────────
SCALE = 0.20         # Sığması için daha da küçültüldü
Y_STRETCH = 1.77     # Dikey esneme korundu

angle_range = {1: (-math.pi, math.pi)}
coords = {1: (0.0, 0.0)}

for n in all_nodes:
    children = tree.get(n, [])
    if not children:
        continue
    a_min, a_max = angle_range[n]
    span  = a_max - a_min
    r     = (seviye[n] + 1) * SCALE
    chunk = span / len(children)
    for i, c in enumerate(children):
        ca = a_min + chunk * i
        cb = a_min + chunk * (i + 1)
        cm = (ca + cb) / 2
        angle_range[c] = (ca, cb)
        coords[c]      = (r * math.cos(cm), r * math.sin(cm) * Y_STRETCH)

# ── Renk paleti ──────────────────────────────────────────────────────
PALETTE = [
    "#C084FC",  # 0 
    "#9B72F5",  # 1
    "#7B6FF5",  # 2
    "#5B8FF5",  # 3
    "#3BE8F5",  # 4 
    "#3BE8C0",  # 5
    "#3BE8A0",  # 6 
    "#8BE840",  # 7
    "#F5D020",  # 8 
    "#F5A020",  # 9 
    "#F56020",  # 10 
    "#F52020",  # 11 
    "#F5207B",  # 12 
    "#D020F5",  # 13 
    "#9B20F5",  # 14 
    "#5B20F5",  # 15 
    "#2020F5",  # 16 - Koyu Mavi
]

def seviye_rengi(s):
    return PALETTE[min(s, len(PALETTE) - 1)]


class CollatzTree(Scene):

    def construct(self):
        dot_map  = {}   
        line_map = {}   

        for n in all_nodes:
            x, y = coords[n]
            renk = seviye_rengi(seviye[n])
            # Noktalar iğne ucu kadar küçültüldü
            r    = 0.08 if seviye[n] == 0 else max(0.005, 0.06 - seviye[n] * 0.003)
            d    = Dot(point=[x, y, 0], radius=r, color=renk)
            d.set_fill(renk, opacity=0.9)
            dot_map[n] = d

        for n in all_nodes:
            for c in tree.get(n, []):
                x1, y1 = coords[n]
                x2, y2 = coords[c]
                renk = seviye_rengi(seviye[c])
                # Çizgiler saç teli kadar inceltildi
                lw   = max(0.05, 1.2 - seviye[c] * 0.07)
                ln   = Line(
                    [x1, y1, 0], [x2, y2, 0],
                    stroke_color=renk,
                    stroke_width=lw,
                    stroke_opacity=0.5,
                )
                line_map[(n, c)] = ln

        bfs_levels = {}
        for n in all_nodes:
            s = seviye[n]
            bfs_levels.setdefault(s, []).append(n)

        # ── 1. SAHNE: ağaç büyür ──────────────────────────────────────
        self.play(FadeIn(dot_map[1], scale=0.3), run_time=0.5)

        for sev in range(1, MAX_SEV + 1):
            nodes_this = bfs_levels.get(sev, [])
            if not nodes_this: continue

            anims = []
            for c in nodes_this:
                p = None
                # Ebeveyni hızlıca bulmak için optimizasyon (büyük veri seti için şart)
                for potential_parent in ebeveynler(c):
                    if potential_parent in all_nodes and c in tree.get(potential_parent, []):
                        p = potential_parent
                        break
                        
                if p is not None and (p, c) in line_map:
                    anims.append(Create(line_map[(p, c)]))
                anims.append(FadeIn(dot_map[c], scale=0.4))

            # Animasyon hızı ve bekleme süresi binlerce düğüm için inanılmaz hızlandırıldı
            hiz = max(0.05, 0.4 - sev * 0.02)
            self.play(*anims, run_time=hiz, lag_ratio=0.002)

        self.wait(0.6)

        # ── 2. SAHNE: tüm ağaç döner ──────────────────────────────────
        tum_agac = VGroup(*dot_map.values(), *line_map.values())

        self.play(
            Rotate(tum_agac, angle=2 * math.pi,
                   about_point=ORIGIN,
                   rate_func=linear),
            run_time=12.0, # Muazzam detay olduğu için dönüşü daha da yavaşlatıp izlenebilir kıldık
        )

        self.wait(0.3)

        # ── 3. SAHNE: 1'den dalgalanma (ripple) ──────────────────────
        for sev in range(0, MAX_SEV + 1):
            nodes_this = bfs_levels.get(sev, [])
            anims = []
            for n in nodes_this:
                anims.append(
                    dot_map[n].animate
                    .set_fill(WHITE, opacity=1)
                    .scale(2.5) # Küçücük noktaların parlaması için scale artırıldı
                )
            if anims:
                self.play(*anims, run_time=0.05, lag_ratio=0)
            
            geri = []
            for n in nodes_this:
                geri.append(
                    dot_map[n].animate
                    .set_fill(seviye_rengi(sev), opacity=0.9)
                    .scale(1 / 2.5)
                )
            if geri:
                self.play(*geri, run_time=0.05, lag_ratio=0)

        self.wait(0.4)

        # ── 4. SAHNE: yavaşça söner ────────────────────────────────────
        self.play(FadeOut(tum_agac), run_time=2.0)