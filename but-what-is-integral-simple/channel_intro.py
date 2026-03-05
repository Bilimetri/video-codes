# This intro will be used in every Bilimetri math (or physics, etc.) video, I did this intro while I'm working on this video
# I wanted to show a bunch of math formulas flying around and then they all come together to form the Bilimetri logo, I think it turned out pretty good, I hope you like it too :)
# signed by Çınar Civan :)

from manim import *
import random
import math

class Intro(Scene):
    def construct(self):

        formulas = [
            r"\int_a^b f(x)\,dx",
            r"e^{i\pi} + 1 = 0",
            r"\frac{d}{dx}x^n = nx^{n-1}",
            r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}",
            r"F = ma",
            r"\nabla \cdot E = \frac{\rho}{\epsilon_0}",
            r"a^2 + b^2 = c^2",
            r"\lim_{x \to 0} \frac{\sin x}{x} = 1",
            r"E = mc^2",
            r"S = k_B \ln \Omega",
            r"i\hbar \frac{\partial}{\partial t}\psi = \hat{H}\psi",
            r"\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}",
            r"\sin^2\theta + \cos^2\theta = 1",
            r"f'(x) = \lim_{h \to 0} \frac{f(x+h)-f(x)}{h}",
            r"\vec{\nabla} \times \vec{E} = -\frac{\partial \vec{B}}{\partial t}",
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
        ]

        random.seed(7)

        # Divide screen to 4x4 grid, math formula for every cell
        cols, rows = 4, 4
        cell_w = 14.0 / cols   # screen width ~14
        cell_h = 8.0 / rows    # screen height ~8

        f_obj = []
        positions = []

        for row in range(rows):
            for col in range(cols):
                # Center of the cell
                cx = -7.0 + cell_w * col + cell_w / 2
                cy = 4.0 - cell_h * row - cell_h / 2
                # Add some random jitter to make it look more dynamic
                jx = random.uniform(-cell_w * 0.2, cell_w * 0.2)
                jy = random.uniform(-cell_h * 0.2, cell_h * 0.2)
                positions.append((cx + jx, cy + jy))

        random.shuffle(positions)

        for i, f in enumerate(formulas):
            obj = MathTex(f, font_size=random.randint(26, 38), color=WHITE)
            obj.set_opacity(random.uniform(0.5, 0.9))
            px, py = positions[i]
            obj.move_to([px, py, 0])
            f_obj.append(obj)

        self.play(
            *[FadeIn(obj, scale=0.8) for obj in f_obj],
            run_time=1.2
        )

        self.play(
            *[
                obj.animate
                    .move_to(ORIGIN)
                    .scale(0.1)
                    .set_opacity(0)
                for obj in f_obj
            ],
            run_time=2.0,
            rate_func=rush_into
        )

        self.remove(*f_obj)

        bg = Circle(
            radius=2.2,
            fill_color=WHITE,
            fill_opacity=0,
            stroke_width=0
        )
        bg.move_to(ORIGIN)

        logo = ImageMobject("Bilimetri_transparent.png") # our precious
        logo.set_height(2.8)
        logo.move_to(ORIGIN)
        logo.set_opacity(0)

        self.add(bg, logo)
        self.play(
            logo.animate.set_opacity(1),
            bg.animate.set_fill(WHITE, opacity=1),
            run_time=0.8,
            rate_func=smooth
        )

        self.wait(1.5)

        self.play( # Fade out the logo and background
            FadeOut(logo),
            FadeOut(bg),
            run_time=0.8
        )
        self.wait(0.3)