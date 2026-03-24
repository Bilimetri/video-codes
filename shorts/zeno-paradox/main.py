from manim import *

config.pixel_width  = 1080
config.pixel_height = 1920
config.frame_rate   = 60

BG     = "#07080F"
GOLD   = ManimColor("#F0C040")
CREAM  = ManimColor("#EDE8DC")
TEAL   = ManimColor("#00BFA5")
PURPLE = ManimColor("#E040FB")
RED    = ManimColor("#FF6B6B")
BLUE   = ManimColor("#40C4FF")
GREEN  = ManimColor("#B2FF59")
DIM    = ManimColor("#1A1D2E")

STEP_COLORS = [GOLD, TEAL, PURPLE, RED, BLUE, GREEN]


class ZenoParadox(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG
        self.camera.frame.save_state()

        # ═══════════════════════════════════════════════════════════
        # BÖLÜM 1  [0–3 sn]
        # "MÖ 450. Elea'lı Zeno, tek bir soruyla antik dünyanın
        #  zihnini kilitledi."
        # → Karanlıkta altın nokta doğar; ardından MÖ 450 yazısı
        #   silik bir şekilde belirir ve solar.
        # ═══════════════════════════════════════════════════════════
        origin_dot = Dot(ORIGIN, radius=0.20, color=GOLD)
        glow = (
            origin_dot.copy()
            .set_color(GOLD)
            .set_opacity(0.12)
            .scale(6)
        )
        year_text = Text("MÖ 450", font="serif", color=CREAM).scale(0.7)
        year_text.next_to(origin_dot, UP, buff=0.55).set_opacity(0)

        self.play(
            FadeIn(origin_dot, scale=0.1, run_time=1.0),
            FadeIn(glow, run_time=1.4),
        )
        self.play(year_text.animate.set_opacity(0.55), run_time=0.7)
        self.wait(0.5)
        self.play(FadeOut(year_text, run_time=0.5), FadeOut(glow, run_time=0.5))

        # ═══════════════════════════════════════════════════════════
        # BÖLÜM 2  [3–7 sn]
        # "Akhilleus koşuyor. Önünde bir hedef var.
        #  Aralarında sonlu bir mesafe. Ama Zeno'ya göre… hiç kapanmayacak."
        # → Çizgi açılır. Koşucu (teal) solda, hedef (altın) sağda belirir.
        #   İnce bir "sonlu mesafe" yay/köprüsü ikisini bağlar.
        # ═══════════════════════════════════════════════════════════
        track_y = -0.5
        track = Line(
            LEFT * 4.5, RIGHT * 4.5,
            color=CREAM, stroke_width=1.2, stroke_opacity=0.35,
        ).shift(DOWN * 0.5)

        runner_start = LEFT * 3.8 + UP * (track_y + 0.5)
        target_pos   = RIGHT * 2.6 + UP * (track_y + 0.5)

        runner = Dot(runner_start, radius=0.15, color=TEAL)
        target = Dot(target_pos,   radius=0.12, color=GOLD)

        # Mesafeyi gösteren ince yay
        brace_line = DashedLine(
            runner_start, target_pos,
            color=CREAM, stroke_width=1.0,
            stroke_opacity=0.4, dash_length=0.15,
        ).shift(DOWN * 0.35)

        self.play(
            origin_dot.animate.move_to(runner_start),
            Create(track, run_time=1.0),
        )
        self.play(
            Transform(origin_dot, runner),
            FadeIn(target, scale=0.4),
            run_time=0.7,
        )
        self.play(Create(brace_line, run_time=0.8))
        self.wait(0.8)

        # ═══════════════════════════════════════════════════════════
        # BÖLÜM 3  [7–30 sn]  — YARIYA BÖLME ADIMLAR
        # Her adımda:
        #   • Renkli segment çizilir
        #   • Orta noktaya küçük halka patlıyor
        #   • Koşucu orta noktaya taşınıyor
        #   • Adım numarası (1/2, 1/4, …) solda yığılıyor
        # ═══════════════════════════════════════════════════════════
        self.play(FadeOut(brace_line, run_time=0.3))

        runner_pos = np.array(runner_start)
        tgt_pos    = np.array(target_pos)

        segments  = VGroup()
        mid_dots  = VGroup()
        frac_stack = VGroup()   # sol kenarda biriken kesirler

        for i in range(6):
            mid_pos = (runner_pos + tgt_pos) / 2
            col     = STEP_COLORS[i]

            seg = Line(
                runner_pos, mid_pos,
                color=col,
                stroke_width=max(5.5 - i * 0.7, 2.0),
            )
            mdot = Dot(mid_pos, radius=max(0.13 - i * 0.016, 0.04), color=col)

            ring = Circle(
                radius=max(0.22 - i * 0.025, 0.07),
                color=col, stroke_width=1.8,
            ).move_to(mid_pos).set_opacity(0.45)

            # Kesir etiketi  (1/2, 1/4, 1/8 …)
            denom = 2 ** (i + 1)
            frac  = MathTex(
                rf"\frac{{1}}{{{denom}}}",
                color=col,
            ).scale(0.55)
            frac.move_to(LEFT * 4.1 + UP * (1.8 - i * 0.55))

            speed = max(1.5 - i * 0.20, 0.45)
            self.play(
                Create(seg),
                FadeIn(mdot, scale=0.25),
                FadeIn(ring, scale=0.25),
                origin_dot.animate.move_to(mid_pos),
                FadeIn(frac, shift=RIGHT * 0.15),
                run_time=speed,
                rate_func=smooth,
            )
            self.play(FadeOut(ring, scale=2.5), run_time=0.25)

            segments.add(seg)
            mid_dots.add(mdot)
            frac_stack.add(frac)
            runner_pos = mid_pos

        self.wait(0.5)

        # ═══════════════════════════════════════════════════════════
        # BÖLÜM 4  [30–36 sn]
        # "İşte paradoks burada. Her adımın uzunluğu sıfıra yaklaşır.
        #  Ama adım sayısı sonsuz olunca… toplam ne olur?"
        # → Kamera son noktaya yakınlaşır. Kesirler kaybolur.
        #   Nokta titreşir — hedefe değemez.
        # ═══════════════════════════════════════════════════════════
        self.play(FadeOut(frac_stack, run_time=0.4))

        self.play(
            self.camera.frame.animate
                .scale(0.16)
                .move_to(runner_pos),
            run_time=2.8,
            rate_func=smooth,
        )
        self.wait(0.6)

        # Titreşim — sıkışmışlık hissi
        for _ in range(4):
            self.play(
                origin_dot.animate.scale(1.8),
                run_time=0.18,
                rate_func=there_and_back,
            )
        self.wait(0.3)

        # ═══════════════════════════════════════════════════════════
        # BÖLÜM 5  [36–39 sn]
        # "Zeno sonsuzluğun toplamının da sonsuz olduğunu varsaydı.
        #  Yanıldı — ama bu yanılgı iki bin yıl boyunca fark edilmedi."
        # → Kamera geri çekilir. "∞ ≠ ∞?" işareti kısa belirir.
        # ═══════════════════════════════════════════════════════════
        self.play(
            Restore(self.camera.frame),
            run_time=2.0,
            rate_func=smooth,
        )

        # "∞ ≠ ?" — kısa bir vizüel soru
        inf_question = MathTex(r"\infty \stackrel{?}{=} \infty", color=RED).scale(1.1)
        inf_question.to_edge(UP, buff=0.8)
        self.play(FadeIn(inf_question, shift=DOWN * 0.2, run_time=0.5))
        self.wait(0.9)
        self.play(FadeOut(inf_question, run_time=0.5))

        # ═══════════════════════════════════════════════════════════
        # BÖLÜM 6  [39–48 sn]
        # "Cauchy ve Weierstrass 1800'lerde ispatladı:
        #  ortak oranı birden küçük olan geometrik seriler yakınsar.
        #  Yarı artı çeyrek artı sekizde bir… tam olarak bire eşittir.
        #  Sonsuz adım. Sonlu mesafe. Sonlu süre."
        # → Renkli segmentler silinir. Tek altın çizgi doğar.
        #   Altında geometrik seri formülü belirir; üstündeki = 1.
        #   Sonra dalgalar.
        # ═══════════════════════════════════════════════════════════
        full_line = Line(
            track.get_left() + RIGHT * 0.01,
            target_pos,
            color=GOLD,
            stroke_width=5,
        )

        self.play(
            FadeOut(segments),
            FadeOut(mid_dots),
            FadeOut(origin_dot),
            run_time=0.55,
        )
        self.play(Create(full_line, run_time=1.4, rate_func=smooth))

        # Seri formülü
        formula = MathTex(
            r"\sum_{n=1}^{\infty} \frac{1}{2^n} \;=\; 1",
            color=CREAM,
        ).scale(0.88)
        formula.next_to(track, DOWN, buff=0.7)

        self.play(Write(formula, run_time=1.2))
        self.wait(0.3)

        # Hedef noktasından yayılan dalgalar
        for r in [0.25, 0.55, 0.95]:
            pulse = Circle(
                radius=r, color=GOLD,
                stroke_width=max(2.0 - r, 0.4),
            ).move_to(target_pos).set_opacity(0.6)
            self.play(
                FadeIn(pulse, scale=0.05),
                FadeOut(pulse, scale=4),
                run_time=0.5,
            )

        self.wait(0.5)

        # ═══════════════════════════════════════════════════════════
        # BÖLÜM 7  [48–55 sn]  — BEYAZ FLAŞ  "Convergence."
        # → Ekran beyaza yanar, söner.
        #   Flaştan hemen önce "Convergence" kelimesi küçük ve ortalı
        #   çıkar — flaşa karışır.
        # ═══════════════════════════════════════════════════════════
        conv_word = Text("Convergence", font="serif", color=CREAM).scale(0.9)
        conv_word.move_to(UP * 2.5)

        self.play(
            FadeOut(full_line),
            FadeOut(track),
            FadeOut(target),
            FadeOut(formula),
            run_time=0.4,
        )
        self.play(FadeIn(conv_word, scale=0.8, run_time=0.6))
        self.wait(0.3)

        flash_rect = Rectangle(
            width=20, height=40,
            fill_color=WHITE,
            fill_opacity=0,
            stroke_width=0,
        )
        self.add(flash_rect)
        self.play(flash_rect.animate.set_fill(opacity=1), run_time=1.0, rate_func=smooth)
        self.play(flash_rect.animate.set_fill(opacity=0), run_time=1.4, rate_func=smooth)
        self.play(FadeOut(conv_word, run_time=0.4))

        # ═══════════════════════════════════════════════════════════
        # BÖLÜM 8  [55–63 sn]
        # "Zeno haklıydı: sonsuz adım gerçekten var.
        #  Ama her adım bir öncekinin yarısı kadar zaman alıyorsa…
        #  o sonsuz adımların toplamı, sonlu bir anda biter.
        #  Hareket bir yanılsama değil. Sonsuzluk bir engel değil.
        #  Sadece… farklı türden bir gerçek."
        # → Teal→Altın spiral yavaşça açılır, merkezde yok olur.
        # ═══════════════════════════════════════════════════════════
        spiral_dots = VGroup()
        n = 150
        for k in range(n):
            angle = k * TAU / 16
            r_val = 0.055 * k ** 0.58
            x, y  = r_val * np.cos(angle), r_val * np.sin(angle)
            alpha = k / n
            d = Dot(
                [x, y, 0],
                radius=max(0.045 * (1 - alpha * 0.55), 0.012),
                color=interpolate_color(TEAL, GOLD, alpha),
            )
            spiral_dots.add(d)

        spiral_dots.move_to(ORIGIN)

        self.play(
            LaggedStart(
                *[FadeIn(d, scale=0.15) for d in spiral_dots],
                lag_ratio=0.012,
                run_time=3.5,
            ),
        )
        self.wait(0.5)
        self.play(
            spiral_dots.animate.scale(0.01).set_opacity(0),
            run_time=1.8,
            rate_func=smooth,
        )
        self.wait(0.6)