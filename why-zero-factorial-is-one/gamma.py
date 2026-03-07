from manim import *

class Bolum5(Scene):
    def construct(self):

        # --- Title ---
        title = Text("Gamma fonksiyonu ile ispat", font_size=36, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title), run_time=0.8)
        self.wait(0.5)

        # =====================
        # SAHNE 1: Tanım
        # =====================
        intro = Text(
            "Faktöriyeli tam sayıların ötesine taşıyalım:",
            font_size=28, color=WHITE
        )
        intro.set_opacity(0.7)
        intro.move_to(UP * 2.2)

        gamma_def = MathTex(
            r"\Gamma(n) = \int_0^{\infty} t^{n-1} e^{-t}\, dt",
            font_size=48, color=WHITE
        )
        gamma_def.move_to(UP * 0.8)

        property_label = Text(
            "Kritik özellik:", font_size=28, color="#5dade2"
        )
        property_label.move_to(DOWN * 0.4)

        property_eq = MathTex(
            r"\Gamma(n) = (n-1)!",
            font_size=48, color="#5dade2"
        )
        property_eq.move_to(DOWN * 1.4)

        self.play(FadeIn(intro), run_time=0.7)
        self.wait(0.3)
        self.play(Write(gamma_def), run_time=2)
        self.wait(0.5)
        self.play(FadeIn(property_label), run_time=0.5)
        self.play(Write(property_eq), run_time=1.2)
        self.wait(1.5)

        self.play(
            FadeOut(intro),
            FadeOut(gamma_def),
            FadeOut(property_label),
            FadeOut(property_eq),
            run_time=0.8
        )

        # =====================
        # SAHNE 2: Γ(1) hesabı
        # =====================
        calc_title = Text("Γ(1) hesaplayalım:", font_size=32, color="#f39c12")
        calc_title.move_to(UP * 2.8)
        self.play(FadeIn(calc_title), run_time=0.6)

        step1 = MathTex(
            r"\Gamma(1) = \int_0^{\infty} t^{0} e^{-t}\, dt",
            font_size=42, color=WHITE
        )
        step1.move_to(UP * 1.6)

        step2 = MathTex(
            r"= \int_0^{\infty} e^{-t}\, dt",
            font_size=42, color=WHITE
        )
        step2.move_to(UP * 0.4)

        step3 = MathTex(
            r"= \Big[-e^{-t}\Big]_0^{\infty}",
            font_size=42, color=WHITE
        )
        step3.move_to(DOWN * 0.8)

        step4 = MathTex(
            r"= 0 - (-1) = 1",
            font_size=42, color="#f39c12"
        )
        step4.move_to(DOWN * 2.0)

        for step in [step1, step2, step3, step4]:
            self.play(Write(step), run_time=1.0)
            self.wait(0.5)

        box = SurroundingRectangle(step4, color="#f39c12", buff=0.15)
        self.play(Create(box), run_time=0.5)
        self.wait(1.5)

        self.play(
            FadeOut(calc_title),
            FadeOut(step1),
            FadeOut(step2),
            FadeOut(step3),
            FadeOut(step4),
            FadeOut(box),
            run_time=0.8
        )

        # =====================
        # SAHNE 3: Sonuç zinciri
        # =====================
        conc1 = MathTex(r"\Gamma(1) = 1", font_size=48, color=WHITE)
        conc1.move_to(UP * 1.8)

        conc2 = MathTex(
            r"\Gamma(n) = (n-1)! \;\Rightarrow\; \Gamma(1) = 0!",
            font_size=44, color=WHITE
        )
        conc2.move_to(UP * 0.4)

        conc3 = MathTex(r"\therefore \quad 0! = 1", font_size=64, color="#c0392b")
        conc3.move_to(DOWN * 1.2)

        self.play(Write(conc1), run_time=1)
        self.wait(0.4)
        self.play(Write(conc2), run_time=1.5)
        self.wait(0.4)
        self.play(Write(conc3), run_time=1)

        final_box = SurroundingRectangle(conc3, color="#c0392b", buff=0.2)
        self.play(Create(final_box), run_time=0.6)
        self.wait(0.8)

        note = Text(
            "Salt bir tanım değil — matematiğin doğal sonucu.",
            font_size=28, color=WHITE
        )
        note.set_opacity(0.6)
        note.move_to(DOWN * 2.6)

        self.play(FadeIn(note, shift=UP * 0.2), run_time=1)
        self.wait(3)

        self.play(
            FadeOut(title),
            FadeOut(conc1),
            FadeOut(conc2),
            FadeOut(conc3),
            FadeOut(final_box),
            FadeOut(note),
            run_time=1.2
        )
        self.wait(0.5)