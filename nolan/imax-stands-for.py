from manim import *
import numpy as np

BG     = "#0A0A0F"
WARM   = "#C8A96E"
COLD   = "#4FC3F7"
WHITE_ = "#F0F0F8"
DIM    = "#3A3A5A"
GOLD   = "#D4AF37"
ACCENT = "#FF4444"
GREEN  = "#4ADE80"


class IMAXAcronymScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 1 — "IMAX" harfleri ortada, renkli, aralıklı
        # ══════════════════════════════════════════════════════════════════

        LETTER_Y = 0.6
        GAP      = 1.9
        xs       = [-GAP*1.5, -GAP*0.5, GAP*0.5, GAP*1.5]
        chars    = ["I",    "M",    "A",    "X"   ]
        colors   = [COLD,   GREEN,  WARM,   ACCENT]

        letter_mobs = VGroup()
        for ch, color, x in zip(chars, colors, xs):
            mob = Text(ch, font="Courier New", weight=BOLD,
                       font_size=110, color=color)
            mob.move_to([x, LETTER_Y, 0])
            mob.set_opacity(0)
            letter_mobs.add(mob)

        # Harfler soldan sağa birer birer düşer
        for mob in letter_mobs:
            mob.shift(UP * 1.5)

        self.play(
            LaggedStart(
                *[mob.animate.shift(DOWN*1.5).set_opacity(1)
                  for mob in letter_mobs],
                lag_ratio=0.18,
            ),
            run_time=1.4, rate_func=rush_from,
        )
        self.wait(0.5)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 2 — OKLAR VE İNGİLİZCE AÇILIM
        # ══════════════════════════════════════════════════════════════════

        # "I" → "Image"  (sol taraf, aşağı ok)
        # "MAX" → "Maximum" (sağ taraf, aşağı ok)

        WORD_Y   = -1.55
        ARROW_TIP_Y = LETTER_Y - 0.72

        # I → Image
        arrow_i = Arrow(
            start=[xs[0], ARROW_TIP_Y, 0],
            end  =[xs[0], WORD_Y + 0.38, 0],
            stroke_color=COLD, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.22, buff=0.05,
        )
        word_i = Text("Image", font="Courier New", weight=BOLD,
                      font_size=36, color=COLD)
        word_i.move_to([xs[0], WORD_Y, 0])
        word_i.set_opacity(0)

        # MAX → Maximum  (M, A, X'in ortasına)
        max_cx = (xs[1] + xs[2] + xs[3]) / 3
        arrow_max = Arrow(
            start=[max_cx, ARROW_TIP_Y, 0],
            end  =[max_cx, WORD_Y + 0.38, 0],
            stroke_color=GOLD, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.22, buff=0.05,
        )
        word_max = VGroup(
            Text("Max", font="Courier New", weight=BOLD,
                 font_size=36, color=GOLD),
            Text("imum", font="Courier New",
                 font_size=36, color=WHITE_),
        ).arrange(RIGHT, buff=0.0)
        word_max.move_to([max_cx, WORD_Y, 0])
        word_max.set_opacity(0)

        # I okunu ve kelimesini göster
        self.play(GrowArrow(arrow_i), run_time=0.6)
        self.play(word_i.animate.set_opacity(1), run_time=0.5)
        self.wait(0.2)

        # MAX okunu ve kelimesini göster
        self.play(GrowArrow(arrow_max), run_time=0.6)
        self.play(word_max.animate.set_opacity(1), run_time=0.5)
        self.wait(1.2)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 3 — İNGİLİZCE KAYBOLUR, TÜRKÇE BELİRİR
        # ══════════════════════════════════════════════════════════════════

        # Türkçe "Maksimum Görüntü" tam ortada
        turkish = VGroup(
            Text("Maksimum", font="Courier New", weight=BOLD,
                 font_size=44, color=GOLD),
            Text("Görüntü", font="Courier New", weight=BOLD,
                 font_size=44, color=COLD),
        ).arrange(RIGHT, buff=0.35)
        turkish.move_to([0, WORD_Y, 0])
        turkish.set_opacity(0)

        self.play(
            FadeOut(VGroup(arrow_i, arrow_max, word_i, word_max)),
            run_time=0.6,
        )
        self.play(turkish.animate.set_opacity(1),
                  run_time=0.9, rate_func=smooth)
        self.wait(1.5)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 4 — EKRAN YAVAŞÇA SOLAR
        # ══════════════════════════════════════════════════════════════════

        self.play(
            VGroup(letter_mobs, turkish).animate.set_opacity(0),
            run_time=1.8, rate_func=smooth,
        )
        self.wait(0.3)