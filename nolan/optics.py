from manim import *
import numpy as np

BG    = "#0A0A0F"
COLD  = "#4FC3F7"
WARM  = "#C8A96E"
WHITE_= "#F0F0F8"
DIM   = "#3A3A5A"
GREEN = "#4ADE80"
ACCENT= "#FF6B6B"

GROUND_Y = -3.0


def human_silhouette(height=1.8) -> VGroup:
    head = Circle(radius=height * 0.13,
                  fill_color=WHITE_, fill_opacity=1, stroke_width=0)
    body = RoundedRectangle(corner_radius=0.12,
                            width=height*0.38, height=height*0.55,
                            fill_color=WHITE_, fill_opacity=1, stroke_width=0)
    body.next_to(head, DOWN, buff=0.06)
    return VGroup(head, body)


def camera_body() -> VGroup:
    body = RoundedRectangle(corner_radius=0.10, width=1.1, height=0.78,
                            fill_color="#1A1A28", fill_opacity=1,
                            stroke_color="#4A4A6A", stroke_width=2)
    lens_ring  = Circle(radius=0.26, fill_color="#08080F", fill_opacity=1,
                        stroke_color="#5A5A7A", stroke_width=2)
    lens_inner = Circle(radius=0.16, fill_color="#020208", fill_opacity=1,
                        stroke_color=COLD, stroke_width=1.5)
    shine = Circle(radius=0.05, fill_color=COLD, fill_opacity=0.5, stroke_width=0)
    lens_ring.move_to(body.get_left() + RIGHT*0.32)
    lens_inner.move_to(lens_ring.get_center())
    shine.move_to(lens_ring.get_center() + UP*0.07 + LEFT*0.07)
    return VGroup(body, lens_ring, lens_inner, shine)


class LensOpticsScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ── BÖLÜM 1: FOV ──────────────────────────────────────────────────
        cam = camera_body().move_to(LEFT * 5.2)
        human_fov = human_silhouette(height=1.9).move_to(RIGHT * 4.2 + DOWN * 0.1)

        self.play(
            FadeIn(cam, shift=RIGHT*0.5),
            FadeIn(human_fov, shift=LEFT*0.5),
            run_time=1.2,
        )
        self.wait(0.6)

        lens_tip  = cam[1].get_right()
        HALF_IMAX = 40 * DEGREES
        HALF_NORM = 18 * DEGREES
        DIST      = 9.5

        fov_ti = Line(lens_tip, lens_tip + DIST*np.array([np.cos(HALF_IMAX),  np.sin(HALF_IMAX), 0]), stroke_color=WARM, stroke_width=2.5)
        fov_bi = Line(lens_tip, lens_tip + DIST*np.array([np.cos(HALF_IMAX), -np.sin(HALF_IMAX), 0]), stroke_color=WARM, stroke_width=2.5)
        arc_i  = Arc(radius=1.0, start_angle=-HALF_IMAX, angle=2*HALF_IMAX, arc_center=lens_tip, stroke_color=WARM, stroke_width=2)
        fov_tn = Line(lens_tip, lens_tip + DIST*np.array([np.cos(HALF_NORM),  np.sin(HALF_NORM), 0]), stroke_color=COLD, stroke_width=2)
        fov_bn = Line(lens_tip, lens_tip + DIST*np.array([np.cos(HALF_NORM), -np.sin(HALF_NORM), 0]), stroke_color=COLD, stroke_width=2)
        arc_n  = Arc(radius=0.65, start_angle=-HALF_NORM, angle=2*HALF_NORM, arc_center=lens_tip, stroke_color=COLD, stroke_width=2)

        lbl_i = Text("IMAX  ~80° FOV",  font="Courier New", font_size=18, color=WARM).move_to(lens_tip + RIGHT*2.4 + UP*2.0)
        lbl_n = Text("Dijital  ~36° FOV", font="Courier New", font_size=18, color=COLD).move_to(lens_tip + RIGHT*2.4 + UP*0.65)

        self.play(Create(fov_ti), Create(fov_bi), Create(arc_i), run_time=1.3, rate_func=smooth)
        self.play(Write(lbl_i), run_time=0.7)
        self.wait(0.4)
        self.play(Create(fov_tn), Create(fov_bn), Create(arc_n), run_time=1.1, rate_func=smooth)
        self.play(Write(lbl_n), run_time=0.7)

        note = Text("Geniş görüş → uzun odak lensi gerekir.", font="Courier New", font_size=20, color=ACCENT).move_to(DOWN*3.2)
        self.play(Write(note), run_time=1.0)
        self.wait(1.5)

        self.play(FadeOut(VGroup(cam, human_fov, fov_ti, fov_bi, arc_i, lbl_i, fov_tn, fov_bn, arc_n, lbl_n, note)), run_time=0.8)

        # ── BÖLÜM 2: LENS FORMÜLÜ ─────────────────────────────────────────
        axis = Line(LEFT*6, RIGHT*6, stroke_color=DIM, stroke_width=1.5)
        self.play(Create(axis), run_time=0.6)
        lens_line = Line(DOWN*1.8, UP*1.8, stroke_color=COLD, stroke_width=3)
        self.play(Create(lens_line), run_time=0.5)

        obj_arrow = Arrow(LEFT*4+DOWN*0.01, LEFT*4+UP*1.0, color=WARM, stroke_width=2.5, buff=0)
        obj_lbl   = Text("Nesne (d₀)", font="Courier New", font_size=18, color=WARM).next_to(obj_arrow, DOWN, buff=0.12)
        img_arrow = Arrow(RIGHT*3+DOWN*0.01, RIGHT*3+DOWN*0.8, color=GREEN, stroke_width=2.5, buff=0)
        img_lbl   = Text("Görüntü (dᵢ)", font="Courier New", font_size=18, color=GREEN).next_to(img_arrow, DOWN, buff=0.12)
        f_l = Dot(LEFT*2.2,  color=COLD, radius=0.08)
        f_r = Dot(RIGHT*2.2, color=COLD, radius=0.08)
        fl_l = Text("F", font="Courier New", font_size=16, color=COLD).next_to(f_l, DOWN, buff=0.10)
        fl_r = Text("F", font="Courier New", font_size=16, color=COLD).next_to(f_r, DOWN, buff=0.10)
        ray1 = DashedLine(LEFT*4+UP*1.0, RIGHT*3+DOWN*0.8, stroke_color="#FFD070", stroke_width=1.2, stroke_opacity=0.7, dash_length=0.12)
        ray2 = DashedLine(LEFT*4+UP*1.0, RIGHT*6,          stroke_color="#FFD070", stroke_width=1.2, stroke_opacity=0.5, dash_length=0.12)

        self.play(LaggedStart(
            FadeIn(obj_arrow), Write(obj_lbl),
            FadeIn(img_arrow), Write(img_lbl),
            FadeIn(f_l), FadeIn(fl_l), FadeIn(f_r), FadeIn(fl_r),
            lag_ratio=0.20,
        ), run_time=2.0)
        self.play(Create(ray1), Create(ray2), run_time=1.0)
        self.wait(0.4)

        formula = MathTex(r"\frac{1}{f} = \frac{1}{d_o} + \frac{1}{d_i}", font_size=44, color=WHITE_).move_to(UP*3.1)
        self.play(Write(formula), run_time=1.3)
        sub_f = Text("Sensör büyüdükçe f (odak uzaklığı) artar.", font="Courier New", font_size=19, color=ACCENT).next_to(formula, DOWN, buff=0.30)
        self.play(FadeIn(sub_f, shift=UP*0.15), run_time=0.9)
        self.wait(1.6)

        self.play(FadeOut(VGroup(axis, lens_line, obj_arrow, obj_lbl, img_arrow, img_lbl, f_l, fl_l, f_r, fl_r, ray1, ray2, formula, sub_f)), run_time=0.8)

        # ── BÖLÜM 3: DEPTH OF FIELD ───────────────────────────────────────

        # Zemin
        ground      = Line(LEFT*8, RIGHT*8, stroke_color="#C8D8E8", stroke_width=3).move_to([0, GROUND_Y, 0])
        ground_glow = Line(LEFT*8, RIGHT*8, stroke_color=WHITE_, stroke_width=1, stroke_opacity=0.4).move_to([0, GROUND_Y, 0])

        # Binalar — tabanı GROUND_Y
        rng = np.random.default_rng(9)
        buildings = VGroup()
        for i in range(9):
            bw = rng.uniform(0.7, 1.2)
            bh = rng.uniform(1.4, 3.4)
            bx = -7.0 + i * 1.7 + rng.uniform(-0.15, 0.15)
            r_ = rng.integers(18, 42); g_ = rng.integers(18, 42); b_ = rng.integers(28, 52)
            b_rect = Rectangle(width=bw, height=bh,
                               fill_color="#{:02x}{:02x}{:02x}".format(r_, g_, b_),
                               fill_opacity=0.9, stroke_width=0)
            b_rect.move_to([bx, GROUND_Y + bh/2, 0])
            buildings.add(b_rect)
            for wr in range(int(bh // 0.55)):
                for wc in range(int(bw // 0.45)):
                    win = Rectangle(width=0.18, height=0.22,
                                    fill_color="#C8D080", fill_opacity=0.65,
                                    stroke_width=0)
                    win.move_to([bx - bw/2 + 0.28 + wc*0.42,
                                 GROUND_Y + 0.35 + wr*0.52, 0])
                    buildings.add(win)

        # İnsan — tabanı GROUND_Y
        person = human_silhouette(height=2.2)
        person.shift(DOWN * (person.get_bottom()[1] - GROUND_Y))

        self.add(buildings)
        self.play(Create(ground), FadeIn(ground_glow), run_time=0.7)
        self.play(FadeIn(person, scale=0.92), run_time=1.0)
        self.wait(0.6)

        # "Medium Format Look" kutusu — ÜSTTE
        mfl_box = RoundedRectangle(corner_radius=0.3, width=7.4, height=0.72,
                                   fill_color="#000000", fill_opacity=0.75,
                                   stroke_color=WARM, stroke_width=2).move_to(UP*3.3)
        mfl_lbl = Text('Medium Format Look',
                       font="Courier New", font_size=22, color=WARM).move_to(mfl_box.get_center())
        self.play(FadeIn(mfl_box), Write(mfl_lbl), run_time=1.1)
        self.wait(0.5)

        # Odak düzlemi
        focus_line = DashedLine(LEFT*1.2, RIGHT*1.2, stroke_color=GREEN,
                                stroke_width=2, dash_length=0.18)
        focus_line.move_to([0, person.get_center()[1], 0])
        dof_lbl = Text("Odak Düzlemi", font="Courier New", font_size=17, color=GREEN)
        dof_lbl.next_to(focus_line, RIGHT, buff=0.2)
        self.play(Create(focus_line), Write(dof_lbl), run_time=1.0)
        self.wait(0.5)

        # Arka plan yavaşça solar
        self.play(buildings.animate.set_opacity(0.10), run_time=2.8, rate_func=smooth)

        blur_note = Text("Arka Plan Bulanıklığı",
                         font="Courier New", font_size=18, color=ACCENT).move_to(UP*2.4)
        self.play(Write(blur_note), run_time=1.0)

        self.wait(2.5)