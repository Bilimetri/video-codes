from manim import *

# ── RENK PALETİ ──────────────────────────────────────────────────────────────
BG        = "#0A0A0F"
FILM_BODY = "#1A1A2A"
PERF_CLR  = "#0A0A0F"
FRAME_CLR = "#C8A96E"
IMAX_CLR  = "#4FC3F7"
TEXT_CLR  = "#E8E8F0"
DIM_CLR   = "#5A5A7A"
ACCENT    = "#FF6B6B"


# ── 35mm: perforasyon sol/sağda dikey ────────────────────────────────────────
def make_35mm_strip(frame_w=2.20, frame_h=1.60, n_perfs=4) -> VGroup:
    """
    35mm film karesi: perforasyonlar görüntü karesinin
    SOL ve SAĞ kenarında dikey sütunlar halinde.
    """
    PERF_W   = 0.16
    PERF_H   = 0.22
    SIDE_PAD = 0.32
    strip_w  = frame_w + 2 * SIDE_PAD
    strip_h  = frame_h + 0.20

    body = Rectangle(
        width=strip_w, height=strip_h,
        fill_color=FILM_BODY, fill_opacity=1,
        stroke_color=DIM_CLR, stroke_width=1.5,
    )
    frame_rect = Rectangle(
        width=frame_w, height=frame_h,
        fill_color="#000008", fill_opacity=1,
        stroke_color=FRAME_CLR, stroke_width=2,
    )

    parts = VGroup(body, frame_rect)

    perf_gap = frame_h / n_perfs
    for col_x in [-frame_w / 2 - SIDE_PAD / 2, frame_w / 2 + SIDE_PAD / 2]:
        for i in range(n_perfs):
            y = frame_h / 2 - perf_gap * (i + 0.5)
            hole = RoundedRectangle(
                corner_radius=0.04,
                width=PERF_W, height=PERF_H,
                fill_color=PERF_CLR, fill_opacity=1,
                stroke_color="#3A3A5A", stroke_width=1,
            ).move_to([col_x, y, 0])
            parts.add(hole)

    return parts


# ── IMAX/70mm: perforasyon üst ve altta yatay ────────────────────────────────
def make_imax_strip(frame_w=4.60, frame_h=2.80, n_perfs=15) -> VGroup:
    PERF_W    = 0.13
    PERF_H    = 0.20
    strip_len = frame_w + 2.0
    strip_h   = frame_h + 0.65

    body = Rectangle(
        width=strip_len, height=strip_h,
        fill_color="#0D1A2A", fill_opacity=1,
        stroke_color=DIM_CLR, stroke_width=1.5,
    )
    frame_rect = Rectangle(
        width=frame_w, height=frame_h,
        fill_color="#000008", fill_opacity=1,
        stroke_color=IMAX_CLR, stroke_width=2,
    )

    parts = VGroup(body, frame_rect)

    perf_gap = strip_len / n_perfs
    perf_y   = strip_h / 2 - 0.18

    perfs_top = VGroup()
    perfs_bot = VGroup()

    for i in range(n_perfs):
        x = -strip_len / 2 + perf_gap * (i + 0.5)
        for (grp, sign) in [(perfs_top, 1), (perfs_bot, -1)]:
            hole = RoundedRectangle(
                corner_radius=0.04,
                width=PERF_W, height=PERF_H,
                fill_color=PERF_CLR, fill_opacity=1,
                stroke_color="#3A3A5A", stroke_width=1,
            ).move_to([x, sign * perf_y, 0])
            grp.add(hole)

    parts.add(perfs_top)   # index 2
    parts.add(perfs_bot)   # index 3
    return parts


# ── ANA SAHNE ─────────────────────────────────────────────────────────────────
class FilmComparisonScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ══════════════════════════════════════════════════════════════════════
        # BÖLÜM 1 — 35mm film karesi ortada belirir
        # ══════════════════════════════════════════════════════════════════════
        strip35 = make_35mm_strip()
        strip35.move_to(ORIGIN)
        label_35 = Text("35mm Standart Format", font="Courier New", font_size=30,
                        color=FRAME_CLR).next_to(strip35, DOWN, buff=0.5)

        strip35.shift(LEFT * 10)
        label_35.shift(LEFT * 10)

        self.play(
            strip35.animate.shift(RIGHT * 10),
            label_35.animate.shift(RIGHT * 10),
            run_time=1.3, rate_func=rush_from,
        )
        self.wait(1.4)

        # ══════════════════════════════════════════════════════════════════════
        # BÖLÜM 2 — 35mm sola kayar, IMAX yatay akar
        # ══════════════════════════════════════════════════════════════════════
        strip_imax = make_imax_strip()
        strip_imax.move_to(RIGHT * 17 + UP * 0.9)

        self.play(
            strip35.animate.scale(0.52).move_to(LEFT * 4.5 + UP * 1.1),
            label_35.animate.scale(0.72).move_to(LEFT * 4.5 + DOWN * 0.6),
            strip_imax.animate.move_to(RIGHT * 1.8 + UP * 0.9),
            run_time=1.7, rate_func=smooth,
        )

        label_imax = Text("IMAX/70mm Format", font="Courier New", font_size=30,
                          color=IMAX_CLR).next_to(strip_imax, DOWN, buff=0.45)
        self.play(FadeIn(label_imax), run_time=0.7)
        self.wait(1.0)

        # ══════════════════════════════════════════════════════════════════════
        # BÖLÜM 3 — 15 perforasyon sayımı
        # ══════════════════════════════════════════════════════════════════════
        perf_row = strip_imax[2]   # perfs_top

        counter_bg = RoundedRectangle(
            corner_radius=0.2, width=4.0, height=0.65,
            fill_color="#0D0D1A", fill_opacity=1,
            stroke_color=IMAX_CLR, stroke_width=1.5,
        ).to_corner(DR).shift(UP * 0.25 + LEFT * 0.2)

        counter_label = Text("Perforasyon:", font="Courier New", font_size=22,
                             color=TEXT_CLR).move_to(counter_bg).shift(LEFT * 0.75)
        counter_num = Integer(0, font_size=30, color=IMAX_CLR)
        counter_num.next_to(counter_label, RIGHT, buff=0.25)

        self.play(FadeIn(counter_bg), FadeIn(counter_label), FadeIn(counter_num),
                  run_time=0.5)

        highlights = VGroup()
        for i, hole in enumerate(perf_row):
            hl = hole.copy().set_stroke(color=YELLOW, width=3) \
                     .set_fill(color=YELLOW, opacity=0.55)
            highlights.add(hl)
            self.play(
                FadeIn(hl),
                ChangeDecimalToValue(counter_num, i + 1),
                run_time=0.24,
            )

        self.wait(0.9)
        self.play(
            FadeOut(counter_bg), FadeOut(counter_label),
            FadeOut(counter_num), FadeOut(highlights),
            run_time=0.6,
        )

        # ══════════════════════════════════════════════════════════════════════
        # BÖLÜM 4 — Şeritler üste, formüller ortada
        # ══════════════════════════════════════════════════════════════════════
        self.play(
            strip35.animate.scale(0.65).move_to(LEFT * 4.8 + UP * 3.1),
            label_35.animate.move_to(LEFT * 4.8 + UP * 2.25),
            strip_imax.animate.scale(0.36).move_to(RIGHT * 3.8 + UP * 3.1),
            label_imax.animate.move_to(RIGHT * 3.8 + UP * 2.25),
            run_time=1.3, rate_func=smooth,
        )
        self.wait(0.5)

        formula_title = MathTex(
            r"\text{Alan} = \text{Genişlik} \times \text{Yükseklik}",
            font_size=40, color=TEXT_CLR,
        ).move_to(UP * 1.1)
        self.play(Write(formula_title), run_time=1.3)
        self.wait(0.6)

        calc_35 = MathTex(
            r"A_{35mm}", r"= 22 \times 16 =", r"352 \text{ mm}^2",
            font_size=38,
        ).move_to(UP * 0.1)
        calc_35[0].set_color(FRAME_CLR)
        calc_35[1].set_color(TEXT_CLR)
        calc_35[2].set_color(FRAME_CLR)
        self.play(Write(calc_35), run_time=1.3)
        self.wait(0.6)

        calc_imax = MathTex(
            r"A_{IMAX}", r"= 70 \times 48.5 =", r"2{,}915 \text{ mm}^2",
            font_size=38,
        ).move_to(DOWN * 0.9)
        calc_imax[0].set_color(IMAX_CLR)
        calc_imax[1].set_color(TEXT_CLR)
        calc_imax[2].set_color(IMAX_CLR)
        self.play(Write(calc_imax), run_time=1.3)
        self.wait(1.0)

        # ══════════════════════════════════════════════════════════════════════
        # BÖLÜM 5 — Büyük oran: ×8.3  (önce HER ŞEY temizlenir)
        # ══════════════════════════════════════════════════════════════════════
        self.play(
            FadeOut(formula_title),
            FadeOut(calc_35),
            FadeOut(calc_imax),
            FadeOut(strip35),
            FadeOut(label_35),
            FadeOut(strip_imax),
            FadeOut(label_imax),
            run_time=0.9,
        )
        self.wait(0.2)

        ratio_bg = RoundedRectangle(
            corner_radius=0.45, width=10.2, height=3.4,
            fill_color="#0D0D1A", fill_opacity=1,
            stroke_color=IMAX_CLR, stroke_width=2.5,
        ).move_to(DOWN * 0.1)

        ratio_line1 = Text("IMAX, 35mm'den", font="Courier New", font_size=34,
                           color=TEXT_CLR).move_to(UP * 0.75)

        ratio_number = Text("≈ 8.3×", font="Courier New", font_size=88,
                            color=ACCENT).move_to(DOWN * 0.1)

        ratio_line2 = Text("daha büyük bir kareye sahiptir!",
                           font="Courier New", font_size=32,
                           color=TEXT_CLR).move_to(DOWN * 1.15)

        ratio_number.scale(0.05).set_opacity(0)

        self.play(FadeIn(ratio_bg, scale=0.88), run_time=0.7)
        self.play(Write(ratio_line1), run_time=0.9)
        self.play(
            ratio_number.animate.scale(20).set_opacity(1),
            run_time=1.0, rate_func=rush_from,
        )
        self.play(Write(ratio_line2), run_time=0.9)

        self.play(ratio_number.animate.scale(1.1), run_time=0.3, rate_func=smooth)
        self.play(ratio_number.animate.scale(1 / 1.1), run_time=0.3, rate_func=smooth)

        self.wait(2.2)