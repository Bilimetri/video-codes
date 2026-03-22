from manim import *
import numpy as np

BG     = "#0A0A0F"
GOLD   = "#C8A96E"
GREEN  = "#4ADE80"
DIM    = "#5A5A7A"
FILM_BDY = "#111120"


def make_film_frame(w=1.6, h=1.1, index=0):
    palettes = ["#0A1628","#1A0A10","#0A1A0A","#1A1008","#08101A","#180A1A"]
    fill = palettes[index % len(palettes)]
    frame = Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1,
                      stroke_color="#3A3A5A", stroke_width=1.2)
    lines = VGroup(*[
        Line(LEFT*(w/2-0.1), RIGHT*(w/2-0.1),
             stroke_color=palettes[(index+2) % len(palettes)],
             stroke_width=1.0, stroke_opacity=0.5)
        .move_to([0, (h/2-0.18) - j*(h/3), 0])
        for j in range(2)
    ])
    return VGroup(frame, lines)


def make_strip_row(y_pos, n_frames=10, frame_w=1.65, frame_h=1.10,
                   gap=0.20, body_color=FILM_BDY):
    strip_h = frame_h + 0.55
    total_w = n_frames * (frame_w + gap)
    body = Rectangle(width=total_w, height=strip_h,
                     fill_color=body_color, fill_opacity=1,
                     stroke_width=0).move_to([0, y_pos, 0])
    frames   = VGroup()
    perfs_top = VGroup()
    perfs_bot = VGroup()
    for i in range(n_frames):
        x = -total_w/2 + (frame_w+gap)*(i+0.5) + gap/2
        fr = make_film_frame(frame_w, frame_h, index=i)
        fr.move_to([x, y_pos, 0])
        frames.add(fr)
        for px in np.linspace(x - frame_w/2, x + frame_w/2, 3):
            for sign, row in [(1, perfs_top), (-1, perfs_bot)]:
                hole = RoundedRectangle(
                    corner_radius=0.03, width=0.13, height=0.18,
                    fill_color="#0A0A0F", fill_opacity=1,
                    stroke_color="#2A2A3A", stroke_width=0.8,
                ).move_to([px, y_pos + sign*(strip_h/2 - 0.15), 0])
                row.add(hole)
    return VGroup(body, frames, perfs_top, perfs_bot)


class CostCounterScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        N = 10
        FW, FH, GAP = 1.65, 1.10, 0.20
        SW = N * (FW + GAP)

        strip_top  = make_strip_row( 2.4, n_frames=N)
        strip_top2 = strip_top.copy().shift(RIGHT * SW)
        strip_bot  = make_strip_row(-2.4, n_frames=N, body_color="#0D0D1C")
        strip_bot2 = strip_bot.copy().shift(LEFT * SW)
        self.add(strip_top, strip_top2, strip_bot, strip_bot2)

        self.add(
            Rectangle(width=16, height=2.2, fill_color=BG, fill_opacity=0.58,
                      stroke_width=0).move_to([0,  2.4, 0]),
            Rectangle(width=16, height=2.2, fill_color=BG, fill_opacity=0.58,
                      stroke_width=0).move_to([0, -2.4, 0]),
        )

        # ── Sayaç kutusu ────────────────────────────────────────────────
        box = RoundedRectangle(corner_radius=0.5, width=9.5, height=3.2,
                               fill_color="#000000", fill_opacity=0.72,
                               stroke_color=GOLD, stroke_width=2.5).move_to(ORIGIN)
        self.play(FadeIn(box, scale=0.92), run_time=0.6)

        title = Text("Oppenheimer IMAX Filmi",
                     font="Courier New", font_size=28, color=GOLD)
        title.move_to(box.get_center() + UP * 1.15)
        self.play(Write(title), run_time=0.8)

        # ── $ işareti + sayaç yan yana, grup olarak ortalanmış ──────────
        dollar = Text("$", font="Courier New", weight=BOLD,
                      font_size=68, color=GREEN)

        counter = DecimalNumber(0, num_decimal_places=0,
                                font_size=68, color=GREEN)

        # Grup oluştur, ortala
        amount_group = VGroup(dollar, counter)
        amount_group.arrange(RIGHT, buff=0.18)
        amount_group.move_to(box.get_center() + DOWN * 0.10)

        self.play(FadeIn(dollar), run_time=0.3)
        self.add(counter)

        # ── 4 faz: giderek hızlanan sayaç ───────────────────────────────
        # Her fazda counter büyüyünce grup kaymasın diye
        # counter'ı sabit left anchor ile izle
        counter_left = counter.get_left().copy()

        def keep_group_centered(mob):
            amount_group.move_to(box.get_center() + DOWN * 0.10)

        counter.add_updater(keep_group_centered)

        targets   = [500_000, 5_000_000, 30_000_000, 100_000_000]
        durations = [1.4,     1.2,       1.0,         0.9]
        speeds    = [SW*0.25, SW*0.60,   SW*1.20,     SW*2.20]

        for target, dur, spd in zip(targets, durations, speeds):
            self.play(
                strip_top.animate.shift(LEFT  * spd),
                strip_top2.animate.shift(LEFT * spd),
                strip_bot.animate.shift(RIGHT  * spd),
                strip_bot2.animate.shift(RIGHT * spd),
                ChangeDecimalToValue(counter, target),
                run_time=dur, rate_func=linear,
            )

        counter.remove_updater(keep_group_centered)

        # Zirve vurgusu
        self.play(
            counter.animate.set_color(GOLD),
            dollar.animate.set_color(GOLD),
            run_time=0.3,
        )

        # Şeritler yavaşlayıp durur
        self.play(
            strip_top.animate.shift(LEFT  * SW * 0.12),
            strip_top2.animate.shift(LEFT * SW * 0.12),
            strip_bot.animate.shift(RIGHT * SW * 0.12),
            strip_bot2.animate.shift(RIGHT* SW * 0.12),
            run_time=0.7, rate_func=rate_functions.ease_out_quad,
        )

        self.wait(2.2)