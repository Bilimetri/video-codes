from manim import *

class SmartphoneScene(Scene):
    def construct(self):
        self.camera.background_color = "#0A0A0F"

        # ── TELEFON GÖVDESI ──────────────────────────────────────────
        body = RoundedRectangle(
            corner_radius=0.35,
            width=2.2,
            height=4.4,
            fill_color="#1C1C2E",
            fill_opacity=1,
            stroke_color="#4A4A6A",
            stroke_width=3,
        )

        # Ekran çerçevesi
        screen = RoundedRectangle(
            corner_radius=0.22,
            width=1.85,
            height=3.5,
            fill_color="#0D0D1A",
            fill_opacity=1,
            stroke_color="#2A2A4A",
            stroke_width=1.5,
        ).move_to(body.get_center() + UP * 0.12)

        # Kamera deliği (punch-hole)
        camera_dot = Circle(radius=0.08, fill_color="#0A0A0F", fill_opacity=1,
                            stroke_color="#3A3A5A", stroke_width=1)
        camera_dot.move_to(screen.get_center() + UP * 1.55)

        # Alt home bar
        home_bar = RoundedRectangle(corner_radius=0.05, width=0.7, height=0.07,
                                    fill_color="#3A3A5A", fill_opacity=1, stroke_width=0)
        home_bar.move_to(body.get_center() + DOWN * 1.95)

        # Yan butonlar
        vol_up = RoundedRectangle(corner_radius=0.05, width=0.08, height=0.35,
                                  fill_color="#2A2A4A", fill_opacity=1, stroke_width=0)
        vol_up.move_to(body.get_left() + RIGHT * 0.04 + UP * 0.5)

        vol_down = RoundedRectangle(corner_radius=0.05, width=0.08, height=0.35,
                                    fill_color="#2A2A4A", fill_opacity=1, stroke_width=0)
        vol_down.move_to(body.get_left() + RIGHT * 0.04 + UP * 0.0)

        power_btn = RoundedRectangle(corner_radius=0.05, width=0.08, height=0.45,
                                     fill_color="#2A2A4A", fill_opacity=1, stroke_width=0)
        power_btn.move_to(body.get_right() + LEFT * 0.04 + UP * 0.3)

        phone = VGroup(body, screen, camera_dot, home_bar, vol_up, vol_down, power_btn)
        phone.move_to(ORIGIN)

        # ── EKRAN PARLAMA GRADYANI ──────────────────────────────────
        screen_glow = Circle(
            radius=1.4,
            fill_color="#3B5BDB",
            fill_opacity=0,
            stroke_width=0,
        ).move_to(screen.get_center())

        # ── 4K ve 8K YAZILARI ──────────────────────────────────────
        label_4k = Text("4K", font="SF Pro Display", weight=BOLD, font_size=52,
                        color=WHITE).set_opacity(0)
        label_8k = Text("8K", font="SF Pro Display", weight=BOLD, font_size=52,
                        color=WHITE).set_opacity(0)

        # Telefon solunda / sağında konumlandır
        label_4k.move_to(phone.get_center() + LEFT * 3.2 + UP * 0.4)
        label_8k.move_to(phone.get_center() + RIGHT * 3.2 + UP * 0.4)

        # Parıltı halkaları (4K ve 8K için)
        def glow_ring(center, color):
            return Circle(radius=0.55, stroke_color=color, stroke_width=2,
                          fill_opacity=0).move_to(center)

        ring_4k = glow_ring(label_4k.get_center(), "#74C0FC")
        ring_8k = glow_ring(label_8k.get_center(), "#A9E34B")

        # Ekrandan çıkan ışık çizgileri
        def light_ray(start, end, color):
            return Line(start, end, stroke_color=color, stroke_width=1.5,
                        stroke_opacity=0.6)

        rays_4k = VGroup(*[
            light_ray(screen.get_center() + LEFT * 0.9, label_4k.get_center() + d, "#74C0FC")
            for d in [RIGHT * 0.4 + UP * 0.2, RIGHT * 0.4, RIGHT * 0.4 + DOWN * 0.2]
        ])
        rays_8k = VGroup(*[
            light_ray(screen.get_center() + RIGHT * 0.9, label_8k.get_center() + d, "#A9E34B")
            for d in [LEFT * 0.4 + UP * 0.2, LEFT * 0.4, LEFT * 0.4 + DOWN * 0.2]
        ])

        # ── ANİMASYON SIRASI ────────────────────────────────────────

        # 1. Telefon sahneye giriş — hızlı scale-in
        phone.scale(0.01)
        self.play(
            phone.animate.scale(100),   # 0.01 * 100 = 1.0
            rate_func=rush_from,
            run_time=0.7,
        )
        self.play(
            phone.animate.shift(ORIGIN),  # yerinde hafif titreme yerine
            rate_func=there_and_back,
            run_time=0.25,
        )

        # 2. Ekran ışığı parlama
        self.play(
            screen_glow.animate.set_opacity(0.18).scale(1.6),
            run_time=0.5,
            rate_func=smooth,
        )

        # 3. Işın çizgileri ve yazılar eş zamanlı
        self.play(
            LaggedStart(
                AnimationGroup(
                    Create(rays_4k, lag_ratio=0.15),
                    label_4k.animate.set_opacity(1),
                    ring_4k.animate.scale(1.4).set_opacity(0),
                    lag_ratio=0.1,
                ),
                AnimationGroup(
                    Create(rays_8k, lag_ratio=0.15),
                    label_8k.animate.set_opacity(1),
                    ring_8k.animate.scale(1.4).set_opacity(0),
                    lag_ratio=0.1,
                ),
                lag_ratio=0.15,
            ),
            run_time=1.0,
            rate_func=smooth,
        )

        # 4. 4K ve 8K yazıları üzerinde kısa parıltı dalgası
        for _ in range(2):
            self.play(
                label_4k.animate.set_color("#74C0FC"),
                label_8k.animate.set_color("#A9E34B"),
                run_time=0.25,
                rate_func=there_and_back,
            )
            self.play(
                label_4k.animate.set_color(WHITE),
                label_8k.animate.set_color(WHITE),
                run_time=0.25,
            )

        # 5. Son kare — 1 sn dur
        self.wait(1.0)