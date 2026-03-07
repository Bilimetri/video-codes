from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16

class RiemannStyle(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 6, 1],
            x_length=7,
            y_length=7,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 2)

        labels = axes.get_axis_labels(x_label="x", y_label="y")
        graph = axes.plot(lambda x: x + 1, x_range=[0, 4], color=BLUE)

        self.play(Create(axes))
        self.play(Write(labels))
        self.play(Create(graph), run_time=1)

        # İlk kaba yaklaşım
        rects = axes.get_riemann_rectangles(
            graph,
            x_range=[0, 4],
            dx=1,
            fill_opacity=0.6
        )
        self.play(Create(rects), run_time=1)
        self.wait()

        # Daha küçük dikdörtgenler
        rects2 = axes.get_riemann_rectangles(
            graph,
            x_range=[0, 4],
            dx=0.5,
            fill_opacity=0.6
        )
        self.play(Transform(rects, rects2), run_time=1)
        self.wait()

        # Çok daha küçük
        rects3 = axes.get_riemann_rectangles(
            graph,
            x_range=[0, 4],
            dx=0.1,
            fill_opacity=0.6
        )
        self.play(Transform(rects, rects3), run_time=1)
        self.wait()

        area = axes.get_area(graph, x_range=[0, 4], color=BLUE, opacity=0.6)
        self.play(
            FadeOut(rects),
            FadeIn(area),
            run_time=2
        )
        self.wait()

        integral = MathTex(r"\int_0^4 (x+1)\,dx", font_size=64)
        integral.to_edge(UP, buff=1.2)

        self.play(Write(integral))
        self.wait(3)
        self.play(FadeOut(*self.mobjects))