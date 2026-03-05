from manim import *

class PreReqs(Scene):
    def construct(self):

        # --- Title ---
        title = Text(
            "Bu video kimlere hitap ediyor:",
            font_size=36,
            color=WHITE
        ).to_edge(UP, buff=0.6)

        self.play(FadeIn(title), run_time=1)
        self.wait(0.5)

        # --- Maddeler ---
        maddeler = [
            "İntegralin i'sini bile bilmeyenler",
            "Lise matematiği seviyesinde\nbilgisi az olanlar",
            "Matematiğe merakı olanlar",
            "Bilimetri'yi seven güzel insanlar",
        ]

        tick = "✓"
        group = VGroup()

        for text in maddeler:
            tick_obj = Text(tick, font_size=32, color=GREEN)
            text_obj = Text(text, font_size=28, color=WHITE)
            satir = VGroup(tick_obj, text_obj).arrange(RIGHT, buff=0.3)
            group.add(satir)

        group.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        group.move_to(ORIGIN + DOWN * 0.3)

        # Show items
        for satir in group:
            self.play(FadeIn(satir, shift=RIGHT * 0.3), run_time=1.5)
            self.wait(1)

        self.wait(4)

        # Clear the scene
        self.play(
            FadeOut(title),
            FadeOut(group),
            run_time=1.2
        )
        self.wait(0.5)