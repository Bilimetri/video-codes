from manim import *

class Opening(Scene):
    def construct(self):

        # --- "0! = 1" appears in center ---
        equation = MathTex(r"0! = 1", font_size=120, color=WHITE)
        equation.move_to(ORIGIN)

        self.play(Write(equation), run_time=2)
        self.wait(1)

        # --- Question mark appears next to it ---
        question_mark = Text("?", font_size=100, color="#c0392b")
        question_mark.next_to(equation, RIGHT, buff=0.3)

        self.play(FadeIn(question_mark, scale=1.5), run_time=0.6)
        self.wait(1)

        # --- Both shift up together ---
        self.play(
            VGroup(equation, question_mark).animate.move_to(UP * 2.5).scale(0.7),
            run_time=1.2
        )

        # --- Subtitle appears ---
        subtitle = Text(
            '"Bu nereden çıktı?"',
            font_size=42,
            color=WHITE,
            slant=ITALIC
        )
        subtitle.set_opacity(0.7)
        subtitle.move_to(ORIGIN)

        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=1)
        self.wait(3)

        # --- Subtitle fades, factorial definition appears ---
        self.play(FadeOut(subtitle), run_time=0.6)

        # --- Factorial definition ---
        definition = MathTex(
            r"n! = n \times (n-1) \times (n-2) \times \cdots \times 1",
            font_size=40,
            color=WHITE
        )
        definition.set_opacity(0.85)
        definition.move_to(ORIGIN + UP * 0.5)

        self.play(Write(definition), run_time=2)
        self.wait(15)

        # --- Concrete example ---
        example = MathTex(
            r"5! = 5 \times 4 \times 3 \times 2 \times 1 = 120",
            font_size=44,
            color="#5dade2"
        )
        example.next_to(definition, DOWN, buff=0.6)

        self.play(Write(example), run_time=2)
        self.wait(10)

        # --- Clear scene for next section ---
        self.play(
            FadeOut(equation),
            FadeOut(question_mark),
            FadeOut(definition),
            FadeOut(example),
            run_time=1.2
        )
        self.wait(0.5)