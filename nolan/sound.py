from manim import *
import numpy as np

BG     = "#0A0A0F"
WARM   = "#C8A96E"
COLD   = "#4FC3F7"
GREEN  = "#4ADE80"
ACCENT = "#FF4444"
WHITE_ = "#F0F0F8"
DIM    = "#3A3A5A"
PURPLE = "#A78BFA"


def human_voice_wave(width=5.5, color=GREEN) -> VMobject:
    """Küçük, düzensiz, organik insan sesi dalgası."""
    rng = np.random.default_rng(42)
    steps = 400
    xs = np.linspace(0, width, steps)
    # Birkaç sinüs frekansının toplamı — organik, düzensiz
    ys = (
        0.18 * np.sin(2 * PI * xs * 3.1)
      + 0.10 * np.sin(2 * PI * xs * 7.3 + 0.8)
      + 0.07 * np.sin(2 * PI * xs * 14.1 + 1.2)
      + 0.04 * np.sin(2 * PI * xs * 22.7 + 2.1)
      + 0.03 * rng.uniform(-1, 1, steps)   # hafif gürültü
    )
    # Zarf — ortada güçlü, kenarlarda söner
    envelope = np.sin(PI * xs / width) ** 0.6
    ys *= envelope

    points = [[xs[i] - width/2, ys[i], 0] for i in range(steps)]
    mob = VMobject(stroke_color=color, stroke_width=2.0, stroke_opacity=0.9)
    mob.set_points_smoothly(points)
    return mob


def imax_motor_wave(width=5.5, color=ACCENT) -> VMobject:
    """Devasa, düzensiz, gürültülü IMAX motor dalgası."""
    rng = np.random.default_rng(7)
    steps = 600
    xs = np.linspace(0, width, steps)

    # Düşük frekanslı güçlü temel + yüksek frekanslı kaotik gürültü
    ys = (
        1.45 * np.sin(2 * PI * xs * 1.2)
      + 0.80 * np.sin(2 * PI * xs * 2.7 + 0.5)
      + 0.50 * np.sin(2 * PI * xs * 5.1 + 1.1)
      + 0.30 * np.sin(2 * PI * xs * 9.3 + 0.3)
      + 0.40 * rng.uniform(-1, 1, steps)   # kaotik gürültü
    )
    # Clip — gerçekçi "clipping" efekti
    ys = np.clip(ys, -1.75, 1.75)

    points = [[xs[i] - width/2, ys[i], 0] for i in range(steps)]
    mob = VMobject(stroke_color=color, stroke_width=2.5, stroke_opacity=0.95)
    mob.set_points_smoothly(points)
    return mob


def db_meter(value_db, max_db=120, height=2.5, color=GREEN) -> VGroup:
    """Dikey dB ölçer."""
    bg = Rectangle(width=0.35, height=height,
                   fill_color="#0A0A14", fill_opacity=1,
                   stroke_color=DIM, stroke_width=1.2)
    fill_h = height * (value_db / max_db)
    fill = Rectangle(width=0.25, height=fill_h,
                     fill_color=color, fill_opacity=0.9,
                     stroke_width=0)
    fill.move_to(bg.get_bottom() + UP * fill_h/2)
    return VGroup(bg, fill)


class SoundWaveScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 1 — İNSAN SESİ
        # ══════════════════════════════════════════════════════════════════

        title = Text("Ses Karşılaştırması",
                     font="Courier New", weight=BOLD,
                     font_size=30, color=WARM).move_to(UP*3.5)
        self.play(Write(title), run_time=1.0)

        # Sol panel çerçevesi
        panel_l = RoundedRectangle(
            corner_radius=0.2, width=6.2, height=3.4,
            fill_color="#07070F", fill_opacity=1,
            stroke_color=GREEN, stroke_width=1.8,
        ).move_to(LEFT*3.4 + UP*0.3)

        lbl_human = Text("İnsan Sesi", font="Courier New",
                         weight=BOLD, font_size=22, color=GREEN)
        lbl_human.move_to(panel_l.get_top() + DOWN*0.28)

        # Merkez ekseni
        axis_l = Line(LEFT*2.9, RIGHT*2.9,
                      stroke_color=DIM, stroke_width=1.0)
        axis_l.move_to(panel_l.get_center())

        self.play(FadeIn(panel_l), Write(lbl_human), run_time=0.8)
        self.play(Create(axis_l), run_time=0.4)

        # İnsan sesi waveform — Create ile çizilir
        wave_h = human_voice_wave(width=5.5, color=GREEN)
        wave_h.move_to(panel_l.get_center())

        self.play(Create(wave_h), run_time=2.2, rate_func=linear)
        self.wait(0.4)

        # dB etiketi
        db_h_bg = RoundedRectangle(corner_radius=0.15, width=1.8, height=0.5,
                                   fill_color="#000000", fill_opacity=0.7,
                                   stroke_color=GREEN, stroke_width=1.5)
        db_h_bg.move_to(panel_l.get_bottom() + UP*0.38)
        db_h_txt = Text("~60 dB", font="Courier New",
                        font_size=18, color=GREEN).move_to(db_h_bg.get_center())
        self.play(FadeIn(db_h_bg), Write(db_h_txt), run_time=0.7)
        self.wait(0.5)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 2 — IMAX MOTOR SESİ
        # ══════════════════════════════════════════════════════════════════

        panel_r = RoundedRectangle(
            corner_radius=0.2, width=6.2, height=3.4,
            fill_color="#0F0505", fill_opacity=1,
            stroke_color=ACCENT, stroke_width=1.8,
        ).move_to(RIGHT*3.4 + UP*0.3)

        lbl_imax = Text("IMAX Kamera Sesi", font="Courier New",
                        weight=BOLD, font_size=22, color=ACCENT)
        lbl_imax.move_to(panel_r.get_top() + DOWN*0.28)

        axis_r = Line(LEFT*2.9, RIGHT*2.9,
                      stroke_color=DIM, stroke_width=1.0)
        axis_r.move_to(panel_r.get_center())

        self.play(FadeIn(panel_r), Write(lbl_imax), run_time=0.8)
        self.play(Create(axis_r), run_time=0.4)

        # Ekran titreyerek giriş
        self.play(panel_r.animate.shift(RIGHT*0.08), run_time=0.06)
        self.play(panel_r.animate.shift(LEFT*0.08),  run_time=0.06)

        wave_i = imax_motor_wave(width=5.5, color=ACCENT)
        wave_i.move_to(panel_r.get_center())

        # Motor dalgası hızlı ve agresif gelir
        self.play(Create(wave_i), run_time=1.6, rate_func=linear)

        # Çerçeve kısa sarsılır
        for _ in range(3):
            self.play(panel_r.animate.shift(RIGHT*0.06 + UP*0.03), run_time=0.05)
            self.play(panel_r.animate.shift(LEFT*0.06 + DOWN*0.03), run_time=0.05)
        self.wait(0.3)

        db_i_bg = RoundedRectangle(corner_radius=0.15, width=1.8, height=0.5,
                                   fill_color="#000000", fill_opacity=0.7,
                                   stroke_color=ACCENT, stroke_width=1.5)
        db_i_bg.move_to(panel_r.get_bottom() + UP*0.38)
        db_i_txt = Text("~105 dB", font="Courier New",
                        font_size=18, color=ACCENT).move_to(db_i_bg.get_center())
        self.play(FadeIn(db_i_bg), Write(db_i_txt), run_time=0.7)
        self.wait(0.5)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 3 — BOYUT KARŞILAŞTIRMASI VURGUSU
        # ══════════════════════════════════════════════════════════════════

        # Amplitude oranı ok çifti
        arrow_up = Arrow(
            panel_l.get_right() + RIGHT*0.15,
            panel_r.get_left() + LEFT*0.15,
            stroke_color=WARM, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.15,
        )
        ratio_lbl = Text("~3,000 kat\ndaha güçlü",
                         font="Courier New", font_size=18,
                         color=WARM, line_spacing=1.2)
        ratio_lbl.move_to(arrow_up.get_center() + UP*0.5)

        self.play(GrowArrow(arrow_up), run_time=0.7)
        self.play(Write(ratio_lbl), run_time=0.9)
        self.wait(0.6)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 4 — dB BAR KARŞILAŞTIRMASI (alt kısım)
        # ══════════════════════════════════════════════════════════════════

        bar_y = DOWN*2.5
        max_db = 120
        bar_h  = 1.0

        # İnsan sesi bar
        bar_h_fill = bar_h * (60 / max_db)
        bar_human_bg = Rectangle(width=2.8, height=bar_h,
                                 fill_color="#0A0A14", fill_opacity=1,
                                 stroke_color=GREEN, stroke_width=1.2)
        bar_human_bg.move_to(LEFT*3.4 + bar_y)
        bar_human_fill = Rectangle(width=2.8 * 0.6, height=bar_h,
                                   fill_color=GREEN, fill_opacity=0.85,
                                   stroke_width=0)
        bar_human_fill.move_to(bar_human_bg.get_left() + RIGHT*(2.8*0.6)/2)
        bar_human_lbl = Text("60 dB, İnsan Sesi",
                             font="Courier New", font_size=14, color=GREEN)
        bar_human_lbl.next_to(bar_human_bg, DOWN, buff=0.12)

        # IMAX motor bar
        bar_imax_bg = Rectangle(width=2.8, height=bar_h,
                                fill_color="#0F0505", fill_opacity=1,
                                stroke_color=ACCENT, stroke_width=1.2)
        bar_imax_bg.move_to(RIGHT*3.4 + bar_y)
        bar_imax_fill = Rectangle(width=0.001, height=bar_h,
                                  fill_color=ACCENT, fill_opacity=0.9,
                                  stroke_width=0)
        bar_imax_fill.move_to(bar_imax_bg.get_left() + RIGHT*0.001)
        bar_imax_lbl = Text("105 dB, IMAX Kamera Sesi",
                            font="Courier New", font_size=14, color=ACCENT)
        bar_imax_lbl.next_to(bar_imax_bg, DOWN, buff=0.12)

        self.play(
            FadeIn(bar_human_bg), FadeIn(bar_imax_bg),
            run_time=0.5,
        )
        self.play(
            bar_human_fill.animate.move_to(
                bar_human_bg.get_left() + RIGHT*(2.8*0.60)/2
            ),
            run_time=0.001,
        )
        self.add(bar_human_fill)

        # İnsan barı sabit, IMAX barı sağa büyüyerek dolup taşar
        self.play(
            FadeIn(bar_human_fill),
            run_time=0.4,
        )
        self.play(
            Write(bar_human_lbl),
            run_time=0.6,
        )
        self.play(
            bar_imax_fill.animate
                .stretch_to_fit_width(2.8)
                .move_to(bar_imax_bg.get_center()),
            run_time=1.4, rate_func=smooth,
        )
        self.play(Write(bar_imax_lbl), run_time=0.6)

        # IMAX barı taşıyor — kırmızı parlar
        self.play(
            bar_imax_fill.animate.set_fill(color="#FF2222"),
            run_time=0.15,
        )
        self.play(
            bar_imax_fill.animate.set_fill(color=ACCENT),
            run_time=0.15,
        )
        self.wait(0.5)