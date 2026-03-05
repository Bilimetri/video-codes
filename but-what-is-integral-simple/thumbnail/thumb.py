from manim import *

class Kapak(Scene):
    def construct(self):

        self.camera.background_color = "#0a0a0f"

        # --- Eksenler ---
        axes = Axes(
            x_range=[0, 7.5, 1],
            y_range=[0, 7.5, 1],
            x_length=8,
            y_length=5.5,
            axis_config={
                "include_numbers": False,
                "include_tip": True,
                "stroke_color": WHITE,
                "stroke_opacity": 0.5,
            },
        ).shift(LEFT * 2.5 + DOWN * 0.5)

        def f(x):
            return min(0.1*x**3 - x**2 + 3*x, 6)

        graph = axes.plot(f, x_range=[0, 7], color="#5dade2", stroke_width=4)

        alan = axes.get_area(
            graph,
            x_range=[0, 7],
            color=["#2980b9", "#1a5276"],
            opacity=0.45
        )

        # --- Dev integral sembolü (arka planda soluk) ---
        integral_ghost = MathTex(r"\int", font_size=600, color=WHITE)
        integral_ghost.set_opacity(0.04)
        integral_ghost.move_to(RIGHT * 3.5)

        # --- Ana integral sembolü ---
        integral_main = MathTex(r"\int", font_size=280)
        integral_main.set_color_by_gradient("#e8e8e8", "#c0392b", "#8e1a0e")
        integral_main.move_to(RIGHT * 3.2 + DOWN * 0.2)

        # --- Başlık ---
        baslik_1 = Text("İntegral basitçe", font="Georgia", font_size=56, color=WHITE, weight=BOLD)
        baslik_2 = Text("nedir?", font="Georgia", font_size=56, color="#c0392b", weight=BOLD)
        baslik = VGroup(baslik_1, baslik_2).arrange(DOWN, buff=0.15, aligned_edge=RIGHT)
        baslik.move_to(RIGHT * 3.5 + DOWN * 1.8)

        # --- Dekoratif çizgi ---
        cizgi = Line(LEFT * 0, RIGHT * 2.6, color="#c0392b", stroke_width=1.5)
        cizgi.set_opacity(0.7)
        cizgi.next_to(baslik, UP, buff=0.25).align_to(baslik, RIGHT)

        # --- Parıltı efekti ---
        glow = Circle(radius=1.8, color="#c0392b", fill_opacity=0)
        glow.set_stroke(color="#c0392b", opacity=0.08, width=80)
        glow.move_to(integral_main.get_center())

        # --- Formül — grafiğin sol üst köşesine ---
        formul = MathTex(r"\int_a^b f(x)\,dx", font_size=48, color=WHITE)
        formul.set_opacity(0.75)
        formul.move_to(LEFT * 3.1 + UP * 1.2)

        # --- Logo sol üst köşe ---
        logo = ImageMobject("Bilimetri_Light.png")
        logo.set_height(0.7)
        logo.move_to(LEFT * 5.2 + UP * 3.2)

        # --- Hepsini ekle ---
        self.add(
            integral_ghost,
            glow,
            alan,
            graph,
            axes,
            formul,
            integral_main,
            cizgi,
            baslik,
            logo,
        )

        self.wait(1)