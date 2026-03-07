from manim import *

class Factorial(Scene):
    def construct(self):

        # --- Title ---
        title = Text("Örüntüyü takip edelim", font_size=48, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.5)

        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.8)
        self.wait(0.5)

        # --- Pattern rule ---
        rule = MathTex(
            r"n! = (n+1)! \div (n+1)",
            font_size=44,
            color="#5dade2"
        )
        rule.next_to(title, DOWN, buff=0.6)

        self.play(Write(rule), run_time=1.5)
        self.wait(1)

        # --- Factorial sequence descending ---
        factorials = [
            (r"5!", r"120"),
            (r"4!", r"24"),
            (r"3!", r"6"),
            (r"2!", r"2"),
            (r"1!", r"1"),
            (r"0!", r"?"),
        ]

        colors = [WHITE, WHITE, WHITE, WHITE, WHITE, "#c0392b"]

        rows = VGroup()
        for i, (label, value) in enumerate(factorials):
            row = MathTex(
                label + r"=", value,
                font_size=46,
            )
            row.set_color(colors[i])
            rows.add(row)

        rows.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        rows.move_to(LEFT * 3 + DOWN * 0.5)

        # --- Division arrows between rows ---
        div_labels = VGroup()
        for i in range(len(factorials) - 1):
            n = 5 - i
            div = MathTex(rf"\div {n}", font_size=32, color="#f39c12")
            div_labels.add(div)

        # Show rows one by one with division label
        self.play(FadeIn(rows[0]), run_time=1.3)
        self.wait(0.3)

        for i in range(1, len(rows)):
            # Position division label between previous and current row
            mid_y = (rows[i-1].get_bottom()[1] + rows[i].get_top()[1]) / 2
            div_labels[i-1].move_to(LEFT * 1.2 + UP * mid_y * 0 + rows[i-1].get_center() * 0)
            div_labels[i-1].next_to(rows[i-1], RIGHT, buff=0.8)
            div_labels[i-1].shift(DOWN * 0.3)

            self.play(
                FadeIn(div_labels[i-1], shift=RIGHT * 0.2),
                run_time=0.4
            )
            self.play(
                FadeIn(rows[i], shift=DOWN * 1),
                run_time=0.5
            )
            self.wait(0.3)

        self.wait(1)

        # --- Highlight 0! row ---
        highlight_box = SurroundingRectangle(rows[5], color="#c0392b", buff=0.15)
        self.play(Create(highlight_box), run_time=0.6)
        self.wait(0.5)

        # --- Answer appears ---
        answer = MathTex(r"0! = 1", font_size=52, color="#c0392b")
        answer.next_to(rows[5], RIGHT, buff=2.5)

        self.play(
            Transform(rows[5][1], answer),
            run_time=0.8
        )
        self.wait(1)

        # --- Question on the right ---
        soru = Text(
            "Tanım mı,\nzorunluluk mu?",
            font_size=36,
            color=WHITE,
            line_spacing=1.3
        )
        soru.set_opacity(0.75)
        soru.move_to(RIGHT * 3.5 + DOWN * 0.5)

        self.play(FadeIn(soru, shift=UP * 0.3), run_time=1)
        self.wait(6)

        # --- Clear scene ---
        self.play(
            FadeOut(title),
            FadeOut(rule),
            FadeOut(rows),
            FadeOut(div_labels),
            FadeOut(highlight_box),
            FadeOut(soru),
            run_time=1
        )
        self.wait(0.5)