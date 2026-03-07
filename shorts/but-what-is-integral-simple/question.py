from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16

class Question(Scene):
    def construct(self):
        # --- Axes ---
        axes = Axes(
            x_range=[0, 7.5, 1],
            y_range=[0, 7.5, 1],
            x_length=7,
            y_length=7,
            axis_config={
                "include_numbers": True,
                "include_tip": True,
                "numbers_to_exclude": [0],
            },
        ).shift(DOWN * 1.5)

        labels = axes.get_axis_labels(x_label="x", y_label="y")

        def f(x):
            return min(0.1*x**3 - x**2 + 3*x, 6)

        graph = axes.plot(f, x_range=[0, 7], color=BLUE)

        # Draws axes and graph
        self.play(Create(axes), Create(labels), run_time=0.5)
        self.play(Create(graph), run_time=1)
        self.wait(0.5)

        # --- Question text ---
        question = Text(
            "Bu eğrinin altındaki\nalan nedir?",
            font_size=52,
            color=WHITE,
            line_spacing=1.2
        ).to_edge(UP, buff=1.2)

        self.play(FadeIn(question), run_time=0.5)
        self.wait(1)

        # --- Fill ---
        area = axes.get_area(
            graph,
            x_range=[0, 7],
            color=[TEAL, BLUE],
            opacity=0.5
        )
        self.play(FadeIn(area), run_time=1)
        self.wait(1)

        # --- Put question mark ---
        question_mark = Text("?", font_size=96, color=YELLOW)
        question_mark.move_to(axes.c2p(3.5, 1.5))
        self.play(FadeIn(question_mark), run_time=0.8)
        self.wait(1)

        # --- Clear the scene ---
        self.play(
            FadeOut(question),
            FadeOut(area),
            FadeOut(question_mark),
            FadeOut(graph),
            FadeOut(axes),
            FadeOut(labels),
            run_time=1.5
        )
        self.wait(0.5)