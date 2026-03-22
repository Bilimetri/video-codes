from manim import *
import numpy as np

BG     = "#0A0A0F"
WARM   = "#C8A96E"
COLD   = "#4FC3F7"
GREEN  = "#4ADE80"
ACCENT = "#FF6B6B"
WHITE_ = "#F0F0F8"
DIM    = "#3A3A5A"
GOLD   = "#D4AF37"
PURPLE = "#A78BFA"


class FinalScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ══════════════════════════════════════════════════════════════════
        # ARKA PLAN — yavaşça akan ince dikey ışık çizgileri (film şeridi hissi)
        # ══════════════════════════════════════════════════════════════════
        streaks = VGroup()
        rng = np.random.default_rng(11)
        for _ in range(18):
            x     = rng.uniform(-7.0, 7.0)
            h     = rng.uniform(1.2, 4.5)
            alpha = rng.uniform(0.03, 0.09)
            streak = Rectangle(
                width=0.015, height=h,
                fill_color=WHITE_, fill_opacity=alpha,
                stroke_width=0,
            ).move_to([x, rng.uniform(-3.5, 3.5), 0])
            streaks.add(streak)
        self.add(streaks)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 1 — SORU: "Neden hâlâ IMAX?"
        # ══════════════════════════════════════════════════════════════════

        question = Text("Neden hâlâ IMAX?",
                        font="Courier New", weight=BOLD,
                        font_size=46, color=WHITE_)
        question.set_opacity(0)
        self.play(question.animate.set_opacity(1),
                  run_time=1.6, rate_func=smooth)
        self.wait(1.2)
        self.play(question.animate.set_opacity(0),
                  run_time=0.8, rate_func=smooth)
        self.wait(0.2)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 2 — RAKAMLAR TEK TEK DÜŞER (film kredisi stili)
        # ══════════════════════════════════════════════════════════════════

        # Her satır: (büyük sayı, açıklama, renk)
        stats = [
            ("8.3×",     "daha büyük film karesi",          WARM),
            ("18K",      "efektif çözünürlük",              COLD),
            ("60 kg",    "IMAX kamerasının ağırlığı",       ACCENT),
            ("%34",      "görüş alanı kapsamı",             GREEN),
            ("15,000 W", "projektör güç tüketimi",          GOLD),
            ("%40",      "standart sinema karesi kayıp",    PURPLE),
            ("$100M",    "Oppenheimer IMAX maliyeti",       WARM),
            ("%22",      "toplam gişenin IMAX'ten geleni",  COLD),
        ]

        # Her stat çifti: büyük rakam solda, açıklama sağda
        # Üstten aşağı doğru yığılır, ekranı doldurur

        stat_mobs = VGroup()
        LINE_H   = 0.88
        START_Y  =  2.8
        LEFT_X   = -5.8
        MID_X    = -1.8
        RIGHT_X  =  2.2

        for i, (num, desc, color) in enumerate(stats):
            y = START_Y - i * LINE_H

            num_mob = Text(num, font="Courier New", weight=BOLD,
                           font_size=32, color=color)
            num_mob.move_to([LEFT_X + 1.2, y, 0])

            # Ayırıcı çizgi
            sep = Line(UP*0.22, DOWN*0.22,
                       stroke_color=color, stroke_width=1.2,
                       stroke_opacity=0.5)
            sep.move_to([MID_X - 0.5, y, 0])

            desc_mob = Text(desc, font="Courier New",
                            font_size=18, color=WHITE_)
            desc_mob.move_to([RIGHT_X + 1.5, y, 0])

            group = VGroup(num_mob, sep, desc_mob)
            group.set_opacity(0)
            stat_mobs.add(group)

        self.add(stat_mobs)

        # Rakamlar yukarıdan birer birer düşer
        for i, group in enumerate(stat_mobs):
            group.shift(UP * 0.6)
            self.play(
                group.animate.shift(DOWN * 0.6).set_opacity(1),
                run_time=0.38,
                rate_func=rush_from,
            )
            self.wait(0.08)

        self.wait(4.0)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 3 — RAKAMLAR SOLAR, EKRAN KARARIR
        # ══════════════════════════════════════════════════════════════════

        self.play(
            stat_mobs.animate.set_opacity(0),
            streaks.animate.set_opacity(0),
            run_time=1.2, rate_func=smooth,
        )
        self.wait(0.3)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 4 — NOLAN ALINTIISI (büyük, ortalı)
        # ══════════════════════════════════════════════════════════════════

        quote_line1 = Text(
            'Kuralları çiğnemek ilginç değildir.',
            font="Courier New", font_size=28, color=WHITE_,
        ).move_to(UP*1.1)

        quote_line2 = Text(
            "Heyecanı canlı tutan şey,",
            font="Courier New", weight=BOLD,
            font_size=34, color=GOLD,
        ).move_to(UP*0.28)

        quote_line3 = Text(
            "yeni kurallar icat etmektir.",
            font="Courier New", font_size=24,
            color=WHITE_, slant=ITALIC,
        ).move_to(DOWN*0.55)

        attr = Text("— Christopher Nolan",
                    font="Courier New", font_size=20,
                    color=WARM).move_to(DOWN*1.35)

        for mob in [quote_line1, quote_line2, quote_line3, attr]:
            mob.set_opacity(0)

        self.play(
            quote_line1.animate.set_opacity(1),
            run_time=1.1, rate_func=smooth,
        )
        self.play(
            quote_line2.animate.set_opacity(1),
            run_time=1.0, rate_func=smooth,
        )
        self.play(
            quote_line3.animate.set_opacity(1),
            run_time=1.0, rate_func=smooth,
        )
        self.play(
            attr.animate.set_opacity(1),
            run_time=0.8, rate_func=smooth,
        )
        self.wait(1.8)

        # Alıntı solar
        self.play(
            VGroup(quote_line1, quote_line2, quote_line3, attr)
            .animate.set_opacity(0),
            run_time=1.0,
        )
        self.wait(0.3)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 5 — FİNAL: "IMAX" BÜYÜK PATLAMA + ALT YAZI
        # ══════════════════════════════════════════════════════════════════

        # Altın yatay çizgiler
        line_top = Line(LEFT*7, RIGHT*7,
                        stroke_color=GOLD, stroke_width=1.2,
                        stroke_opacity=0).move_to(UP*1.5)
        line_bot = Line(LEFT*7, RIGHT*7,
                        stroke_color=GOLD, stroke_width=1.2,
                        stroke_opacity=0).move_to(DOWN*1.5)

        self.play(
            line_top.animate.set_stroke(opacity=0.6),
            line_bot.animate.set_stroke(opacity=0.6),
            run_time=0.7,
        )

        imax_big = Text("IMAX", font="Courier New", weight=BOLD,
                        font_size=140, color=WARM)
        imax_big.set_opacity(0).scale(0.3)

        self.play(
            imax_big.animate.scale(10/3).set_opacity(1),
            run_time=0.8, rate_func=rush_from,
        )

        # Hafif pulse
        self.play(imax_big.animate.scale(1.06), run_time=0.2)
        self.play(imax_big.animate.scale(1/1.06), run_time=0.2)
        self.wait(0.5)

        # Alt imza
        sub1 = Text("Dijital her şeyi daha iyi yapabilir.",
                    font="Courier New", font_size=20,
                    color=WHITE_, slant=ITALIC)
        sub1.move_to(DOWN*2.2)
        sub1.set_opacity(0)

        sub2 = Text("Ama daha iyi, her zaman daha gerçek demek değildir.",
                    font="Courier New", font_size=17,
                    color=WARM)
        sub2.move_to(DOWN*2.75)
        sub2.set_opacity(0)

        self.play(sub1.animate.set_opacity(1), run_time=1.0)
        self.play(sub2.animate.set_opacity(1), run_time=0.8)
        self.wait(1.5)

        # ══════════════════════════════════════════════════════════════════
        # KAPANIŞ — her şey yavaşça söner
        # ══════════════════════════════════════════════════════════════════

        self.play(
            VGroup(imax_big, sub1, sub2, line_top, line_bot)
            .animate.set_opacity(0),
            run_time=2.2, rate_func=smooth,
        )
        self.wait(0.5)