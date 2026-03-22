from manim import *
import numpy as np

BG     = "#0A0A0F"
WARM   = "#C8A96E"
COLD   = "#4FC3F7"
GREEN  = "#4ADE80"
ACCENT = "#FF6B6B"
WHITE_ = "#F0F0F8"
DIM    = "#3A3A5A"
PURPLE = "#A78BFA"


# ══════════════════════════════════════════════════════════════════════════════
# YARDIMCILAR
# ══════════════════════════════════════════════════════════════════════════════

def eye_icon(scale=1.0) -> VGroup:
    """Stilize insan gözü."""
    outer = Ellipse(width=1.8*scale, height=0.9*scale,
                    fill_color="#0A0A14", fill_opacity=1,
                    stroke_color=WHITE_, stroke_width=2)
    iris  = Circle(radius=0.28*scale,
                   fill_color="#3A5A8A", fill_opacity=1,
                   stroke_color=COLD, stroke_width=1.5)
    pupil = Circle(radius=0.14*scale,
                   fill_color="#000000", fill_opacity=1,
                   stroke_width=0)
    shine = Circle(radius=0.05*scale,
                   fill_color=WHITE_, fill_opacity=0.7,
                   stroke_width=0)
    shine.move_to(iris.get_center() + UP*0.08*scale + LEFT*0.06*scale)
    return VGroup(outer, iris, pupil, shine)


def fov_cone(half_angle_deg, length, color, opacity=0.18, stroke_w=2.0):
    """FOV konisi — iki çizgi + dolu üçgen."""
    ha = half_angle_deg * DEGREES
    tip = ORIGIN
    top_end = np.array([length * np.cos(ha),  length * np.sin(ha), 0])
    bot_end = np.array([length * np.cos(ha), -length * np.sin(ha), 0])

    cone_fill = Polygon(tip, top_end, bot_end,
                        fill_color=color, fill_opacity=opacity,
                        stroke_width=0)
    top_line  = Line(tip, top_end, stroke_color=color,
                     stroke_width=stroke_w, stroke_opacity=0.9)
    bot_line  = Line(tip, bot_end, stroke_color=color,
                     stroke_width=stroke_w, stroke_opacity=0.9)
    arc       = Arc(radius=length*0.25, start_angle=-ha, angle=2*ha,
                    arc_center=tip, stroke_color=color, stroke_width=1.8)
    return VGroup(cone_fill, top_line, bot_line, arc)


def screen_rect(width, height, color, label_text, label_color=None):
    if label_color is None:
        label_color = color
    rect = Rectangle(width=width, height=height,
                     fill_color="#050510", fill_opacity=1,
                     stroke_color=color, stroke_width=2.5)
    lbl  = Text(label_text, font="Courier New", weight=BOLD,
                font_size=16, color=label_color)
    lbl.next_to(rect, DOWN, buff=0.2)
    return VGroup(rect, lbl)


# ══════════════════════════════════════════════════════════════════════════════
# SAHNE
# ══════════════════════════════════════════════════════════════════════════════

class FOVScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ── Başlık ────────────────────────────────────────────────────────
        title = Text("İzleyici Görüş Alanı  (Field of View)",
                     font="Courier New", weight=BOLD,
                     font_size=28, color=WARM).move_to(UP*3.5)
        self.play(Write(title), run_time=1.0)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 1 — İNSAN GÖZÜ FOV TANIMI
        # ══════════════════════════════════════════════════════════════════

        # Göz solda
        eye = eye_icon(scale=1.0)
        eye.move_to(LEFT*5.5)

        eye_lbl = Text("İnsan Gözü", font="Courier New",
                       font_size=18, color=WHITE_).next_to(eye, DOWN, buff=0.22)

        self.play(FadeIn(eye, scale=0.7), Write(eye_lbl), run_time=0.9)
        self.wait(0.3)

        # Toplam görüş alanı (~200° yatay, ama binoküler 120°)
        # Binoküler net görüş konisi: ~120°
        cone_total = fov_cone(100, length=4.5, color=DIM,
                              opacity=0.10, stroke_w=1.2)
        cone_total.move_to(LEFT*5.5)
        cone_total.shift(RIGHT * 0.0)   # göz merkezinden

        cone_binocular = fov_cone(60, length=4.5, color=WHITE_,
                                  opacity=0.15, stroke_w=1.8)
        cone_binocular.move_to(LEFT*5.5)

        lbl_total = Text("~200°  toplam görüş", font="Courier New",
                         font_size=13, color=DIM)
        lbl_total.move_to(LEFT*3.0 + UP*2.2)

        lbl_bino = Text("~120°  net / binoküler", font="Courier New",
                        font_size=13, color=WHITE_)
        lbl_bino.move_to(LEFT*3.0 + UP*1.7)

        self.play(FadeIn(cone_total), run_time=0.7)
        self.play(FadeIn(cone_binocular), run_time=0.7)
        self.play(Write(lbl_total), Write(lbl_bino), run_time=0.8)
        self.wait(1.0)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 2 — ÜÇ PERDE: EV / SİNEMA / IMAX
        # ══════════════════════════════════════════════════════════════════

        # FOV açıları (izleyici mesafesine göre yaklaşık)
        # Ev TV 55" @ 2.5m   → ~30° yatay
        # Standart sinema    → ~45° yatay
        # IMAX               → ~70° yatay (eğri perde)

        EYE_POS = LEFT*5.2

        cone_tv    = fov_cone(15,  length=4.0, color="#888888",
                              opacity=0.12, stroke_w=1.5)
        cone_cine  = fov_cone(22,  length=4.0, color=COLD,
                              opacity=0.14, stroke_w=1.8)
        cone_imax  = fov_cone(35,  length=4.0, color=WARM,
                              opacity=0.20, stroke_w=2.2)

        for c in [cone_tv, cone_cine, cone_imax]:
            c.move_to(EYE_POS)

        # Perdeler
        SCREEN_X = EYE_POS[0] + 4.0

        def screen_h_from_angle(half_deg, dist=4.0):
            return 2 * dist * np.tan(half_deg * DEGREES)

        screen_tv   = screen_rect(0.08, screen_h_from_angle(15),
                                  "#888888", "TV\n~30°", "#888888")
        screen_cine = screen_rect(0.08, screen_h_from_angle(22),
                                  COLD,     "Sinema\n~45°")
        screen_imax = screen_rect(0.08, screen_h_from_angle(35),
                                  WARM,     "IMAX\n~70°")

        for s, x_off in [(screen_tv, 0.0),
                         (screen_cine, 0.35),
                         (screen_imax, 0.70)]:
            s.move_to([SCREEN_X + x_off, EYE_POS[1], 0])

        # Göz üstüne yeni bir göz (önceki FOV taşındı)
        self.play(
            FadeOut(cone_total), FadeOut(cone_binocular),
            FadeOut(lbl_total), FadeOut(lbl_bino),
            run_time=0.6,
        )
        self.wait(0.2)

        # TV konisi + perde
        self.play(
            FadeIn(cone_tv), FadeIn(screen_tv[0]),
            run_time=0.9,
        )
        self.play(Write(screen_tv[1]), run_time=0.6)
        self.wait(0.4)

        # Sinema konisi + perde
        self.play(
            FadeIn(cone_cine), FadeIn(screen_cine[0]),
            run_time=0.9,
        )
        self.play(Write(screen_cine[1]), run_time=0.6)
        self.wait(0.4)

        # IMAX konisi + perde — en büyük, vurgulu
        self.play(
            FadeIn(cone_imax), FadeIn(screen_imax[0]),
            run_time=1.0,
        )
        self.play(Write(screen_imax[1]), run_time=0.6)

        # IMAX vurgu: koni bir kez genişler
        self.play(
            screen_imax[0].animate.set_stroke(color=WARM, width=4),
            run_time=0.3,
        )
        self.play(
            screen_imax[0].animate.set_stroke(width=2.5),
            run_time=0.3,
        )
        self.wait(1.0)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 3 — YÜZDE FOV KARŞILAŞTIRMASI (Pasta / Bar)
        # ══════════════════════════════════════════════════════════════════

        # Önceki konileri/ekranları temizle
        self.play(
            FadeOut(VGroup(
                eye, eye_lbl,
                cone_tv, cone_cine, cone_imax,
                screen_tv, screen_cine, screen_imax,
            )),
            run_time=0.8,
        )
        self.wait(0.2)

        # Başlık güncelle
        sub_title = Text("Görüş Alanının Yüzde Kaçı Dolduruluyor?",
                         font="Courier New", weight=BOLD,
                         font_size=24, color=WARM).move_to(UP*2.9)
        self.play(Transform(title, sub_title), run_time=0.7)

        # Veriler: görüş alanı kapsamı (alan bazında)
        # Alan ∝ açı² → (30/120)²×100 ≈ 6%, (45/120)²×100 ≈ 14%, (70/120)²×100 ≈ 34%
        data = [
            ("Ev, TV",      6,   "#888888"),
            ("Standart\nSinema", 14,  COLD),
            ("IMAX",       34,  WARM),
        ]

        bar_w_max = 5.5
        bar_h     = 0.55
        bar_gap   = 0.95
        bar_start_y = UP*1.6

        bars    = VGroup()
        bar_bgs = VGroup()
        labels  = VGroup()
        pct_lbs = VGroup()

        for i, (name, pct, color) in enumerate(data):
            y = bar_start_y[1] - i * bar_gap

            # Arka plan (tam uzunluk)
            bg = Rectangle(width=bar_w_max, height=bar_h,
                           fill_color="#0A0A14", fill_opacity=1,
                           stroke_color=DIM, stroke_width=1)
            bg.move_to([1.5, y, 0])

            # Dolu kısım (başlangıçta sıfır genişlik)
            fill = Rectangle(width=0.001, height=bar_h,
                             fill_color=color, fill_opacity=0.9,
                             stroke_width=0)
            fill.move_to(bg.get_left() + RIGHT*0.001/2)

            # İsim etiketi
            lbl = Text(name, font="Courier New", font_size=16, color=color)
            lbl.move_to([-3.2, y, 0])

            # Yüzde etiketi
            pct_lbl = Text(f"%{pct}", font="Courier New",
                           weight=BOLD, font_size=18, color=color)
            pct_lbl.move_to([bg.get_right()[0] + 0.55, y, 0])

            bar_bgs.add(bg)
            bars.add(fill)
            labels.add(lbl)
            pct_lbs.add(pct_lbl)

        self.play(
            LaggedStart(*[FadeIn(bg) for bg in bar_bgs], lag_ratio=0.15),
            LaggedStart(*[Write(lbl) for lbl in labels], lag_ratio=0.15),
            run_time=1.0,
        )

        # Barlar dolup büyür
        target_widths = [bar_w_max * pct/100 for _, pct, _ in data]
        for i, (fill, tw) in enumerate(zip(bars, target_widths)):
            self.add(fill)
            self.play(
                fill.animate
                    .stretch_to_fit_width(tw)
                    .move_to([bar_bgs[i].get_left()[0] + tw/2,
                               fill.get_center()[1], 0]),
                run_time=1.0, rate_func=smooth,
            )
            self.play(Write(pct_lbs[i]), run_time=0.4)
            self.wait(0.2)

        self.wait(0.6)

        # IMAX vurgusu — kısa pulse
        self.play(bars[2].animate.set_fill(color="#FFD700"), run_time=0.2)
        self.play(bars[2].animate.set_fill(color=WARM),      run_time=0.2)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 4 — EĞRI PERDE NOTU
        # ══════════════════════════════════════════════════════════════════

        curve_note_bg = RoundedRectangle(
            corner_radius=0.28, width=10.5, height=1.45,
            fill_color="#000000", fill_opacity=0.80,
            stroke_color=WARM, stroke_width=2,
        ).move_to(DOWN*2.5)

        curve_note = Text(
            "IMAX perdesi eğridir. Işık gözün tüm\n"
            "alıcı hücrelerine eşit açıyla çarpar.\n"
            "Beyin bunu gerçeklik olarak algılar.",
            font="Courier New", font_size=17,
            color=WHITE_, line_spacing=1.3,
        ).move_to(curve_note_bg.get_center())

        self.play(FadeIn(curve_note_bg), run_time=0.5)
        self.play(Write(curve_note), run_time=1.6)
        self.wait(2.8)