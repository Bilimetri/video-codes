from manim import *

class Opening(Scene):
    def construct(self):
        title = Tex(r"İntegral")
        integral = MathTex(r"\int")
        text = Tex(r"Peki nedir bu sembol?")
        VGroup(title, integral).arrange(DOWN)
        self.play(
            Write(title),
            FadeIn(integral, shift=DOWN),
        )
        self.play(integral.animate.shift(LEFT*3)),
        text.next_to(integral, RIGHT)
        self.play(Write(text))

        self.wait(3)

        self.play(
            FadeOut(integral, text, title)
        )