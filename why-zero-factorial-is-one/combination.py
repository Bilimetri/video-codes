from manim import *

class Combination(Scene):
    def construct(self):
        
        # --- Combination formula ---
        formula = MathTex(
            r"\binom{n}{k} = \frac{n!}{k!(n-k)!}",
            font_size=48,
            color=WHITE
        )
        formula.move_to(UP * 0.8)

        self.play(Write(formula), run_time=2)
        self.wait(1)

        # --- Explanation ---
        explanation = Text(
            "n nesne arasından k tanesini seçmenin yolu",
            font_size=32,
            color=WHITE
        )
        explanation.set_opacity(0.6)
        explanation.next_to(formula, DOWN, buff=0.4)

        self.play(FadeIn(explanation, shift=UP * 0.2), run_time=0.8)
        self.wait(10)

        # --- Shift up, bring special case ---
        self.play(
            VGroup(formula, explanation).animate.move_to(UP * 2.8).scale(0.75),
            run_time=1
        )

        # --- Special case: choose all n ---
        special_title = Text(
            "Peki n nesnenin hepsini seçersek?",
            font_size=36,
            color="#5dade2"
        )
        special_title.move_to(UP * 1.2)

        self.play(FadeIn(special_title, shift=DOWN * 0.2), run_time=0.8)
        self.wait(1.5)

        # --- k = n substitution ---
        substitution = MathTex(
            r"\binom{n}{n} = \frac{n!}{n! \cdot (n-n)!} = \frac{n!}{n! \cdot 0!}",
            font_size=48,
            color=WHITE
        )
        substitution.move_to(ORIGIN)

        self.play(Write(substitution), run_time=5)
        self.wait(1)

        # --- This must equal 1 ---
        must_be = MathTex(
            r"\binom{n}{n} = 1",
            font_size=52,
            color="#f39c12"
        )
        must_be.next_to(substitution, DOWN, buff=0.5)

        reason = Text(
            "çünkü n nesneyi seçmenin tek bir yolu vardır",
            font_size=30,
            color=WHITE
        )
        reason.set_opacity(0.6)
        reason.next_to(must_be, DOWN, buff=0.3)

        self.play(Write(must_be), run_time=1)
        self.play(FadeIn(reason, shift=UP * 0.2), run_time=0.8)
        self.wait(6)

        # --- Therefore 0! = 1 ---
        self.play(
            FadeOut(special_title),
            FadeOut(substitution),
            FadeOut(must_be),
            FadeOut(reason),
            run_time=0.8
        )

        # --- Logical chain ---
        line1 = MathTex(
            r"\frac{n!}{n! \cdot 0!} = 1",
            font_size=52, color=WHITE
        )
        line2 = MathTex(
            r"\Rightarrow n! = n! \cdot 0!",
            font_size=52, color=WHITE
        )
        line3 = MathTex(
            r"\Rightarrow 0! = 1",
            font_size=56, color="#c0392b"
        )

        chain = VGroup(line1, line2, line3).arrange(DOWN, buff=0.5)
        chain.move_to(ORIGIN + DOWN * 0.3)

        self.play(Write(line1), run_time=1)
        self.wait(3)
        self.play(Write(line2), run_time=1)
        self.wait(3)
        self.play(Write(line3), run_time=1)
        self.wait(3)

        # --- Box around conclusion ---
        box = SurroundingRectangle(line3, color="#c0392b", buff=0.2)
        self.play(Create(box), run_time=0.6)
        self.wait(5)

        # --- Clear scene ---
        self.play(
            FadeOut(VGroup(formula, explanation)),
            FadeOut(chain),
            FadeOut(box),
            run_time=1
        )
        self.wait(0.5)