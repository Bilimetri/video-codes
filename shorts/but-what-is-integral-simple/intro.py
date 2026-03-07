from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16

class Opening(Scene):
    def construct(self):
        title = Tex(r"İntegral", font_size=72)
        integral = MathTex(r"\int", font_size=120)
        text = Tex(r"Peki nedir bu sembol?", font_size=52)

        # Dikey düzende title üstte, integral ortada
        VGroup(title, integral).arrange(DOWN, buff=0.8).move_to(ORIGIN)

        self.play(
            Write(title),
            FadeIn(integral, shift=DOWN),
        )
        self.wait(0.5)

        # Integral yukarı kayıyor, text altına yerleşiyor
        self.play(integral.animate.shift(UP * 4.8))
        text.next_to(integral, DOWN, buff=2.5)
        self.play(Write(text), run_time=1)
        self.wait(0.5)

        self.play(FadeOut(integral, text, title))