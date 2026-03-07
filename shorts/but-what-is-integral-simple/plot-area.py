from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16

class PlotArea(Scene):
    def construct(self):
        # Axes
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 6, 1],
            x_length=7,
            y_length=6,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 2)

        labels = axes.get_axis_labels(x_label="x", y_label="y")
        graph = axes.plot(lambda x: 3, x_range=[0, 7], color=RED)

        self.play(Create(axes))
        self.play(Write(labels))
        self.play(Create(graph), run_time=1)

        area = axes.get_area(graph, x_range=[0, 7], color=RED, opacity=0.4)
        self.play(FadeIn(area))
        self.wait()

        x_val_h = 0
        y_val_h = 3
        x_val_w = 7
        y_val_w = 0

        dot1 = Dot(axes.c2p(x_val_h, y_val_h), color=BLUE)
        dot2 = Dot(axes.c2p(x_val_w, y_val_w), color=BLUE)

        self.play(FadeIn(dot1))
        self.play(FadeIn(dot2))

        dots_group = VGroup(dot1, dot2)

        # Broken MathTex fixed: missing closing brace added
        area_tex = MathTex("3 \\cdot 7 = 21")
        area_tex.scale(1.4).to_edge(UP, buff=1.5)

        self.play(TransformFromCopy(dots_group, area_tex), run_time=1)
        self.wait(1)

        area_title = Text("Alan Hesabı", font_size=52)
        area_title.next_to(area_tex, DOWN, buff=0.5)

        self.play(Write(area_title), run_time=1.5)
        self.wait(5)

        self.play(FadeOut(*self.mobjects))

        question_text = Text(
            "Peki ya grafiğimiz\nsabit olmasaydı?",
            font_size=52,
            line_spacing=1.3
        ).move_to(ORIGIN)

        self.play(Write(question_text), run_time=1.5)
        self.wait(3)
        self.play(FadeOut(question_text), run_time=1)