from manim import *
import math

config.pixel_width  = 1080
config.pixel_height = 1920
config.frame_rate   = 60
config.background_color = "#08080C"

def collatz(n):
    seq = [n]
    while n != 1:
        n = 3*n+1 if n % 2 else n//2
        seq.append(n)
    return seq

SAYILAR  = [6, 7, 9, 25, 11]
DIZILER  = [collatz(n) for n in SAYILAR]
DOGU_IDX = [d.index(16) for d in DIZILER]   # 16'nın indexi
DORT_IDX = [d.index(4)  for d in DIZILER]   # 4'ün indexi (16+2)

RENKLER = ["#F5A623", "#3BE8A0", "#FF6B9D", "#7EB8F7", "#C084FC"]
BEYAZ   = "#F0EDE8"
BG      = "#0D0D0D"

BOX_W   = 1.75
BOX_H   = 1.55
BOX_GAP = 0.18
STEP_W  = BOX_W + BOX_GAP

ROW_Y = [6.2, 3.6, 1.0, -1.6, -4.2]


class CollatzNumbers(Scene):

    def construct(self):

        EX = config.frame_width / 2

        CLIP_TOP = ROW_Y[0] + BOX_H / 2 + 0.1
        CLIP_BOT = ROW_Y[4] - BOX_H / 2 - 0.1

        perde_ust = Rectangle(
            width=30, height=8,
            fill_color=BG, fill_opacity=1, stroke_width=0,
        ).move_to(UP * (CLIP_TOP + 4.0))

        perde_alt = Rectangle(
            width=30, height=8,
            fill_color=BG, fill_opacity=1, stroke_width=0,
        ).move_to(UP * (CLIP_BOT - 4.0))

        N     = 30
        F_TOP = 1.4
        F_W   = F_TOP / N

        def fade_rect(cx, op):
            return Rectangle(
                width=F_W + 0.005, height=30,
                fill_color=BG,
                fill_opacity=max(0.0, min(1.0, op)),
                stroke_width=0,
            ).move_to(RIGHT * cx)

        sol_fade = VGroup(*[
            fade_rect(-EX + F_W*0.5 + i*F_W,
                      math.cos((i/N)*math.pi/2)**2)
            for i in range(N)
        ])
        sag_fade = VGroup(*[
            fade_rect( EX - F_W*0.5 - i*F_W,
                      math.cos((i/N)*math.pi/2)**2)
            for i in range(N)
        ])

        def kutu(val, renk):
            rect = RoundedRectangle(
                corner_radius=0.22,
                width=BOX_W, height=BOX_H,
                fill_color="#111111", fill_opacity=1,
                stroke_color=renk, stroke_width=2.5,
            )
            num = Text(str(val), font="Courier New",
                       font_size=46, color=renk, weight=BOLD)
            num.move_to(rect.get_center())
            return VGroup(rect, num)

        X0 = -EX + BOX_W / 2

        bant_gruplari = []
        for i, (dizi, renk) in enumerate(zip(DIZILER, RENKLER)):
            grp = VGroup()
            for j, val in enumerate(dizi):
                k = kutu(val, renk)
                k.move_to(RIGHT * (X0 + j * STEP_W) + UP * ROW_Y[i])
                grp.add(k)
            bant_gruplari.append(grp)

        for grp in bant_gruplari:
            self.add(grp)
        self.add(perde_ust, perde_alt, sol_fade, sag_fade)

        self.wait(0.3)

        # ── 1. Kayış: 16 kutusunu ortaya getir ───────────────────────
        anim1 = []
        for grp, d_idx in zip(bant_gruplari, DOGU_IDX):
            kayma = X0 + d_idx * STEP_W
            anim1.append(grp.animate(rate_func=linear).shift(LEFT * kayma))
        self.play(*anim1, run_time=5.5)
        self.wait(0.3)

        # ── 2. Kayış: 2 adım daha → 4 kutusunu ortaya getir ──────────
        anim2 = []
        for grp in bant_gruplari:
            anim2.append(grp.animate(rate_func=linear).shift(LEFT * 2 * STEP_W))
        self.play(*anim2, run_time=1.0)
        self.wait(0.3)

        # ── Perdeler ve fade kaldır ───────────────────────────────────
        self.play(
            FadeOut(perde_ust), FadeOut(perde_alt),
            FadeOut(sol_fade),  FadeOut(sag_fade),
            run_time=0.3,
        )

        # ── 4, 2, 1 kutularını bantlardan çek, ortaya taşı ─────────────
        # Her bantta 4=DORT_IDX, 2=DORT_IDX+1, 1=DORT_IDX+2
        dort_kutulari = []
        iki_kutulari  = []
        bir_kutulari  = []

        for i, (grp, d4) in enumerate(zip(bant_gruplari, DORT_IDX)):
            dort_kutulari.append(grp[d4])
            iki_kutulari.append(grp[d4 + 1])
            bir_kutulari.append(grp[d4 + 2])

        # Hedef konumlar: her satırın y'sinde, sırayla 4/2/1 yan yana
        # 4 → sol, 2 → orta, 1 → sağ; her satır kendi y'sinde
        GAP = BOX_W + 0.3
        for i in range(5):
            ry = ROW_Y[i]
            dort_kutulari[i].generate_target()
            iki_kutulari[i].generate_target()
            bir_kutulari[i].generate_target()
            dort_kutulari[i].target.move_to(LEFT  * GAP + UP * ry)
            iki_kutulari[i].target.move_to(ORIGIN        + UP * ry)
            bir_kutulari[i].target.move_to(RIGHT * GAP   + UP * ry)

        # Diğer kutular (4/2/1 dışındakiler) fade out
        diger_kutular = []
        for i, (grp, d4) in enumerate(zip(bant_gruplari, DORT_IDX)):
            for j, k in enumerate(grp):
                if j not in (d4, d4+1, d4+2):
                    diger_kutular.append(k)

        self.play(
            *[FadeOut(k, run_time=0.5) for k in diger_kutular],
            *[MoveToTarget(dort_kutulari[i], run_time=0.8) for i in range(5)],
            *[MoveToTarget(iki_kutulari[i],  run_time=0.8) for i in range(5)],
            *[MoveToTarget(bir_kutulari[i],  run_time=0.8) for i in range(5)],
        )
        self.wait(0.5)

        # ── Satırları tek tek fade out → ortada tek 4-2-1 üçlüsü ─────
        # Hepsini aynı anda soluklaştır, ortalama konuma topla
        tum_421 = VGroup(
            *dort_kutulari, *iki_kutulari, *bir_kutulari
        )
        self.play(FadeOut(tum_421), run_time=0.5)

        # ════════════════════════════════════════════════════════════════
        # DÖNGÜ SAHNESİ: üçgen 4 → 2 → 1
        # ════════════════════════════════════════════════════════════════

        P4 = LEFT  * 2.2 + UP * 1.8
        P2 = RIGHT * 2.2 + UP * 1.8
        P1 = ORIGIN + DOWN * 2.2

        def dongu_kutu(val, renk):
            r = RoundedRectangle(
                corner_radius=0.3,
                width=2.4, height=2.4,
                fill_color="#111111", fill_opacity=1,
                stroke_color=renk, stroke_width=3,
            )
            t = Text(str(val), font="Courier New",
                     font_size=100, color=renk, weight=BOLD)
            t.move_to(r.get_center())
            return VGroup(r, t)

        k4 = dongu_kutu(4, "#F5A623").move_to(P4)
        k2 = dongu_kutu(2, "#3BE8A0").move_to(P2)
        k1 = dongu_kutu(1, "#FF6B9D").move_to(P1)

        ok42 = CurvedArrow(P4 + RIGHT*1.25, P2 + LEFT *1.25,
                           angle=-0.4, color="#F5A623", stroke_width=5, tip_length=0.25)
        ok21 = CurvedArrow(P2 + DOWN *1.25, P1 + RIGHT*1.1,
                           angle=-0.4, color="#3BE8A0", stroke_width=5, tip_length=0.25)
        ok14 = CurvedArrow(P1 + LEFT *1.1,  P4 + DOWN *1.25,
                           angle=-0.4, color="#FF6B9D", stroke_width=5, tip_length=0.25)

        dongu_grp = VGroup(k4, k2, k1, ok42, ok21, ok14)

        self.play(
            FadeIn(k4, scale=0.5),
            FadeIn(k2, scale=0.5),
            FadeIn(k1, scale=0.5),
            run_time=0.7,
        )
        self.play(Create(ok42), Create(ok21), Create(ok14), run_time=0.8)
        self.wait(0.3)

        # ── Giderek hızlanan döngü vurgulaması ────────────────────────
        renk4, renk2, renk1 = "#F5A623", "#3BE8A0", "#FF6B9D"

        for tur in range(9):
            hiz = max(0.06, 0.32 - tur * 0.03)

            self.play(k4[0].animate.set_stroke(BEYAZ).set_fill(BEYAZ, opacity=0.15),
                      k4[1].animate.set_color(BEYAZ), run_time=hiz)
            self.play(k4[0].animate.set_stroke(renk4).set_fill("#111111", opacity=1),
                      k4[1].animate.set_color(renk4), run_time=hiz*0.35)
            self.play(ok42.animate.set_color(BEYAZ), run_time=hiz*0.5)
            self.play(ok42.animate.set_color(renk4), run_time=hiz*0.25)

            self.play(k2[0].animate.set_stroke(BEYAZ).set_fill(BEYAZ, opacity=0.15),
                      k2[1].animate.set_color(BEYAZ), run_time=hiz)
            self.play(k2[0].animate.set_stroke(renk2).set_fill("#111111", opacity=1),
                      k2[1].animate.set_color(renk2), run_time=hiz*0.35)
            self.play(ok21.animate.set_color(BEYAZ), run_time=hiz*0.5)
            self.play(ok21.animate.set_color(renk2), run_time=hiz*0.25)

            self.play(k1[0].animate.set_stroke(BEYAZ).set_fill(BEYAZ, opacity=0.15),
                      k1[1].animate.set_color(BEYAZ), run_time=hiz)
            self.play(k1[0].animate.set_stroke(renk1).set_fill("#111111", opacity=1),
                      k1[1].animate.set_color(renk1), run_time=hiz*0.35)
            self.play(ok14.animate.set_color(BEYAZ), run_time=hiz*0.5)
            self.play(ok14.animate.set_color(renk1), run_time=hiz*0.25)

        # ── Kapanış: 4→2→1 patlar ────────────────────────────────────
        self.play(FadeOut(dongu_grp), run_time=0.3)

        son = Text("4→2→1", font="Courier New",
                   font_size=180, color=BEYAZ, weight=BOLD)
        son.move_to(ORIGIN)

        self.play(FadeIn(son, scale=0.04), run_time=0.45)
        self.wait(2.2)
        self.play(FadeOut(son), run_time=0.5)