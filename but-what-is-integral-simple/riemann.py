from manim import *

class RiemannRectsSum(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 7.01, 1],
            y_range=[0, 7.01, 1],
            x_length=9,         # length of x-axis
            y_length=5,         # length of y-axis
            axis_config={
                "include_numbers": True,
                "include_tip": True,
            },
        ).shift(DOWN * 0.8 + LEFT * 0.5)  # biraz aşağı ve sola kaydır

        labels = axes.get_axis_labels(x_label="x", y_label="y")
        y_max = 6

        def f(x):
            return min(0.1*x**3 - x**2 + 3*x, y_max)

        graph = axes.plot(f, color=BLUE)

        self.play(Create(axes), run_time=2)
        self.play(Create(labels), run_time=1)
        self.play(Create(graph), run_time=3)
        self.wait(1)

        # Riemann dikdörtgenlerini manuel oluştur
        colors = [TEAL, GREEN_B, BLUE_B, TEAL_D, GREEN_D, BLUE_D]
        rects = VGroup()
        for i in range(6):
            x0 = i + 1
            x1 = i + 2
            y_val = f(x0)
            bottom = axes.c2p(x0, 0)
            top_right = axes.c2p(x1, y_val)
            w = abs(top_right[0] - bottom[0])
            h = abs(top_right[1] - bottom[1])
            rect = Rectangle(
                width=w,
                height=h,
                fill_color=colors[i],
                fill_opacity=0.6,
                stroke_color=WHITE,
                stroke_width=1
            )
            rect.move_to(axes.c2p((x0 + x1) / 2, y_val / 2))
            rects.add(rect)

        self.play(Create(rects), run_time=2)
        self.wait(2)

        # --- Parameters ---
        scale_factor = 0.5
        top_y = 2.7
        gap = 0.2                 # gap between rects and +

        small_w = [r.get_width() * scale_factor for r in rects]
        small_h = [r.get_height() * scale_factor for r in rects]
        max_h = max(small_h)

        # Symbol widths
        plus_tex = MathTex("+")
        sym_w = plus_tex.get_width()
        integral = MathTex(r"\int_1^7 f(x)\,dx").scale(1.1)
        equals_sign = MathTex("=").scale(1.1)
        integral_w = integral.get_width()
        eq_w = equals_sign.get_width()

        # Total width: rect + gap + + + gap + rect + ... + gap + = + gap + integral
        total_w = (
            sum(small_w)
            + 5 * (2 * gap + sym_w)   # 5 "+" gap
            + 2 * gap + eq_w          # "="
            + gap + integral_w        # integral
        )
        cursor = -total_w / 2.3

        # Calculate target positions
        target_positions = []   # (x, y) center
        plus_positions = []
        eq_pos = None
        integral_pos = None

        for i in range(6):
            tx = cursor + small_w[i] / 2
            ty = top_y - small_h[i] / 2 + max_h / 2
            target_positions.append((tx, ty))
            cursor += small_w[i]

            if i < 5:
                cursor += gap
                plus_positions.append(cursor + sym_w / 2)
                cursor += sym_w + gap

        cursor += gap
        eq_pos = cursor + eq_w / 2
        cursor += eq_w + gap
        integral_pos = cursor + integral_w / 2

        # Create target rectangles
        targets = []
        for i in range(6):
            tx, ty = target_positions[i]
            t = Rectangle(
                width=small_w[i],
                height=small_h[i],
                fill_color=colors[i],
                fill_opacity=0.6,
                stroke_color=WHITE,
                stroke_width=1
            )
            t.move_to([tx, ty, 0])
            targets.append(t)

        # Position the symbols
        plus_signs = [MathTex("+").scale(1.1) for _ in range(5)]
        for i, p in enumerate(plus_signs):
            p.move_to([plus_positions[i], top_y, 0])
        equals_sign.move_to([eq_pos, top_y, 0])
        integral.move_to([integral_pos, top_y, 0])

        # Move rectangles one by one, then write +
        for i in range(6):
            rc = rects[i].copy()
            self.add(rc)
            self.play(Transform(rc, targets[i]), run_time=2)
            if i < 5:
                self.play(FadeIn(plus_signs[i]), run_time=0.5)

        self.wait(0.5)

        self.play(FadeIn(equals_sign), run_time=0.4)

        # Break down the integral into parts
        int_symbol = MathTex(r"\int").scale(1.1)
        lower = MathTex(r"1").scale(1.1)
        upper = MathTex(r"7").scale(1.1)
        fx = MathTex(r"f(x)\,dx").scale(1.1)

        # Place the integral and its parts
        int_symbol.move_to([integral_pos - 0.9, top_y, 0])
        lower.move_to([integral_pos - 0.7, top_y - 0.35, 0])
        upper.move_to([integral_pos - 0.55, top_y + 0.4, 0])
        fx.move_to([integral_pos + 0.3, top_y, 0])

        # Lower limit box
        lower_box = SurroundingRectangle(lower, color=YELLOW, buff=0.08)

        # Upper limit box
        upper_box = SurroundingRectangle(upper, color=RED, buff=0.08)

        # First, define the integral symbol and f(x)dx
        self.play(FadeIn(int_symbol), FadeIn(lower), FadeIn(upper), FadeIn(fx), run_time=0.6)
        self.wait(0.5)

        # Lower limit (1) in a box

        self.play(Create(lower_box), run_time=0.5)
        self.wait(3)

        # Upper limit (7) in a box
        self.play(Create(upper_box), run_time=0.5)
        self.wait(6)

        self.play(FadeOut(*self.mobjects))
