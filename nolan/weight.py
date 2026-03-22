from manim import *
import numpy as np

BG       = "#0A0A0F"
TEXT_CLR = "#E8E8F0"
DIM_CLR  = "#5A5A7A"
ACCENT   = "#FF6B6B"
GOLD     = "#C8A96E"
SILVER   = "#A8B8C8"
WOOD_CLR = "#8B6914"
WOOD_DRK = "#5C4510"
METAL    = "#4A5A6A"
GROUND_Y = -3.0


# ── ZEMIN ─────────────────────────────────────────────────────────────────────
def make_ground() -> VGroup:
    line   = Line(LEFT * 8, RIGHT * 8,
                  stroke_color="#C8D8E8", stroke_width=4).move_to([0, GROUND_Y, 0])
    glow   = Line(LEFT * 8, RIGHT * 8,
                  stroke_color=WHITE, stroke_width=1.5,
                  stroke_opacity=0.5).move_to([0, GROUND_Y, 0])
    shadow = Rectangle(width=16, height=0.4,
                       fill_color="#000000", fill_opacity=0.75,
                       stroke_width=0).move_to([0, GROUND_Y - 0.20, 0])
    grid   = VGroup(*[
        Line(LEFT * 8, RIGHT * 8, stroke_color="#1A2A3A",
             stroke_width=0.8, stroke_opacity=0.45)
        .move_to([0, GROUND_Y - i * 0.20, 0])
        for i in range(1, 5)
    ])
    return VGroup(shadow, grid, line, glow)


# ── ÜÇGEN DESTEK (fulcrum) ─────────────────────────────────────────────────────
def make_fulcrum(height=0.9) -> VGroup:
    tri = Triangle(fill_color=METAL, fill_opacity=1,
                   stroke_color=SILVER, stroke_width=2)
    tri.stretch_to_fit_height(height).stretch_to_fit_width(height * 1.1)
    tri.move_to([0, GROUND_Y + height / 2, 0])

    base = Rectangle(width=height * 1.4, height=0.18,
                     fill_color="#2A3A4A", fill_opacity=1,
                     stroke_color=SILVER, stroke_width=1.5)
    base.move_to([0, GROUND_Y + 0.09, 0])
    return VGroup(tri, base)


# ── TAHTEREVALLİ TAHTASI ───────────────────────────────────────────────────────
def make_board(length=10.0) -> VGroup:
    plank = RoundedRectangle(corner_radius=0.12,
                             width=length, height=0.30,
                             fill_color=WOOD_CLR, fill_opacity=1,
                             stroke_color=WOOD_DRK, stroke_width=2)
    # tahta dokusu için yatay çizgiler
    grain = VGroup(*[
        Line(LEFT * (length / 2 - 0.1), RIGHT * (length / 2 - 0.1),
             stroke_color=WOOD_DRK, stroke_width=0.7, stroke_opacity=0.5)
        .move_to([0, y, 0])
        for y in [-0.07, 0.0, 0.07]
    ])
    return VGroup(plank, grain)


# ── RED/ARRI DİJİTAL KAMERA ───────────────────────────────────────────────────
def make_digital_camera() -> VGroup:
    # Gövde
    body = RoundedRectangle(corner_radius=0.12, width=1.0, height=0.72,
                            fill_color="#1A1A1A", fill_opacity=1,
                            stroke_color="#3A3A3A", stroke_width=2)
    # Lens
    lens_outer = Circle(radius=0.30,
                        fill_color="#0A0A14", fill_opacity=1,
                        stroke_color="#5A5A6A", stroke_width=2)
    lens_inner = Circle(radius=0.18,
                        fill_color="#050510", fill_opacity=1,
                        stroke_color="#3A3A8A", stroke_width=1.5)
    lens_shine = Circle(radius=0.06,
                        fill_color="#6A8AFF", fill_opacity=0.6,
                        stroke_width=0)
    lens_shine.move_to(lens_outer.get_center() + UP * 0.07 + LEFT * 0.07)
    lens_group = VGroup(lens_outer, lens_inner, lens_shine)
    lens_group.move_to(body.get_left() + RIGHT * 0.36)

    # Üst aksesuar ray
    rail = Rectangle(width=0.85, height=0.10,
                     fill_color="#2A2A2A", fill_opacity=1,
                     stroke_color="#4A4A4A", stroke_width=1)
    rail.move_to(body.get_top() + DOWN * 0.05)

    # "RED" logosu
    red_logo = Text("RED", font="Courier New", weight=BOLD,
                    font_size=13, color=ACCENT)
    red_logo.move_to(body.get_center() + RIGHT * 0.18 + UP * 0.12)

    # Kayıt butonu
    rec_dot = Circle(radius=0.055,
                     fill_color=ACCENT, fill_opacity=1, stroke_width=0)
    rec_dot.move_to(body.get_right() + LEFT * 0.15 + UP * 0.18)

    # Kablo
    cable = CubicBezier(
        body.get_bottom() + DOWN * 0.0,
        body.get_bottom() + DOWN * 0.2 + RIGHT * 0.15,
        body.get_bottom() + DOWN * 0.35 + RIGHT * 0.05,
        body.get_bottom() + DOWN * 0.45,
        stroke_color="#2A2A2A", stroke_width=2,
    )

    cam = VGroup(body, lens_group, rail, red_logo, rec_dot, cable)
    return cam


# ── IMAX KAMERA ───────────────────────────────────────────────────────────────
def make_imax_camera() -> VGroup:
    # Ana gövde — büyük ve sağlam
    body = RoundedRectangle(corner_radius=0.14, width=2.0, height=1.55,
                            fill_color="#2A2A2A", fill_opacity=1,
                            stroke_color="#5A5A5A", stroke_width=2.5)
    # Film kapağı (sol taraf — film girişi)
    film_door = Rectangle(width=0.28, height=1.20,
                          fill_color="#1A1A1A", fill_opacity=1,
                          stroke_color="#3A3A3A", stroke_width=1.5)
    film_door.move_to(body.get_left() + RIGHT * 0.14)

    # Lens — büyük ve derin
    lens_outer = Circle(radius=0.42,
                        fill_color="#080810", fill_opacity=1,
                        stroke_color="#6A6A7A", stroke_width=3)
    lens_ring1 = Circle(radius=0.34,
                        fill_opacity=0, stroke_color="#4A4A5A", stroke_width=1.5)
    lens_inner = Circle(radius=0.24,
                        fill_color="#030308", fill_opacity=1,
                        stroke_color="#3A3ABA", stroke_width=2)
    lens_shine = Circle(radius=0.08,
                        fill_color="#8AAAFF", fill_opacity=0.55, stroke_width=0)
    lens_shine.move_to(lens_outer.get_center() + UP * 0.12 + LEFT * 0.10)

    lens_group = VGroup(lens_outer, lens_ring1, lens_inner, lens_shine)
    lens_group.move_to(body.get_left() + RIGHT * 0.72)

    # Üst film bobini yuvası
    mag_top = Circle(radius=0.38,
                     fill_color="#1A1A1A", fill_opacity=1,
                     stroke_color="#4A4A4A", stroke_width=2)
    mag_top.move_to(body.get_top() + UP * 0.28 + RIGHT * 0.25)
    mag_hub = Circle(radius=0.10,
                     fill_color="#2A2A2A", fill_opacity=1,
                     stroke_color="#5A5A5A", stroke_width=1.5)
    mag_hub.move_to(mag_top.get_center())

    # Viewfinder (sağ tarafta)
    vf = RoundedRectangle(corner_radius=0.06, width=0.55, height=0.30,
                          fill_color="#111111", fill_opacity=1,
                          stroke_color="#3A3A3A", stroke_width=1.5)
    vf.move_to(body.get_right() + LEFT * 0.30 + UP * 0.25)
    vf_eye = Circle(radius=0.08,
                    fill_color="#050505", fill_opacity=1,
                    stroke_color="#2A2A2A", stroke_width=1)
    vf_eye.move_to(vf.get_right() + LEFT * 0.08)

    # Tutma kolu
    handle = RoundedRectangle(corner_radius=0.10, width=0.30, height=0.65,
                              fill_color="#1E1E1E", fill_opacity=1,
                              stroke_color="#3A3A3A", stroke_width=1.5)
    handle.move_to(body.get_bottom() + DOWN * 0.28 + RIGHT * 0.55)

    # IMAX etiketi
    imax_lbl = Text("IMAX", font="Courier New", weight=BOLD,
                    font_size=16, color=GOLD)
    imax_lbl.move_to(body.get_center() + RIGHT * 0.55 + DOWN * 0.18)

    # Vidalar
    screws = VGroup(*[
        Circle(radius=0.05, fill_color="#3A3A3A", fill_opacity=1,
               stroke_color="#5A5A5A", stroke_width=1)
        .move_to(body.get_corner(corner) + np.array([-s1 * 0.18, s2 * 0.18, 0]))
        for corner, s1, s2 in [
            (UL, -1, 1), (UR, 1, 1), (DL, -1, -1), (DR, 1, -1)
        ]
    ])

    cam = VGroup(body, film_door, lens_group, mag_top, mag_hub,
                 vf, vf_eye, handle, imax_lbl, screws)
    return cam


# ── ANA SAHNE ──────────────────────────────────────────────────────────────────
class SeesawScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        ground  = make_ground()
        fulcrum = make_fulcrum(height=1.0)
        self.add(ground, fulcrum)

        # fulcrum pivot noktası
        pivot = fulcrum[0].get_top()   # üçgenin tepesi

        # ── Tahterevalli tahtası (başlangıç: yatay) ─────────────────────
        BOARD_LEN = 11.0
        board = make_board(BOARD_LEN)
        board.move_to(pivot + UP * 0.15)
        board_center = board.get_center().copy()

        # ── Kameralar başlangıçta tahtanın üstünde ──────────────────────
        OFFSET = 4.2   # pivot'tan uzaklık

        dig_cam  = make_digital_camera()
        imax_cam = make_imax_camera()

        # Sol taraf = dijital kamera, sağ taraf = IMAX
        def place_on_board(obj, x_offset, board_ref):
            bottom_y = board_ref.get_top()[1] + 0.02
            obj.move_to([board_ref.get_center()[0] + x_offset,
                         bottom_y + obj.height / 2, 0])

        place_on_board(dig_cam,  -OFFSET, board)
        place_on_board(imax_cam,  OFFSET, board)

        # ── Ağırlık etiketleri ───────────────────────────────────────────
        lbl_dig = VGroup(
            Text("Film Kamerası", font="Courier New", font_size=22, color=SILVER),
            Text("~4 kg",      font="Courier New", font_size=26, color=TEXT_CLR),
        ).arrange(DOWN, buff=0.10)

        lbl_imax = VGroup(
            Text("IMAX Kamera", font="Courier New", font_size=22, color=GOLD),
            Text("~60 kg",      font="Courier New", font_size=26, color=TEXT_CLR),
        ).arrange(DOWN, buff=0.10)

        lbl_dig.next_to(dig_cam, UP, buff=0.25)
        lbl_imax.next_to(imax_cam, UP, buff=0.25)

        # ── Sahneye giriş ────────────────────────────────────────────────
        self.play(
            LaggedStart(
                FadeIn(board),
                FadeIn(dig_cam),
                FadeIn(imax_cam),
                lag_ratio=0.3,
            ),
            run_time=1.2,
        )
        self.play(
            FadeIn(lbl_dig), FadeIn(lbl_imax),
            run_time=0.7,
        )
        self.wait(1.2)

        # ── Tahterevalli devrilme animasyonu ────────────────────────────
        # IMAX tarafı (sağ) aşağı çöküyor → sağ taraf CW dönüş → negatif açı
        # Dönme merkezi: pivot noktası
        TILT_ANGLE  = -28 * DEGREES   # sağ taraf aşağı

        # Birlikte döndürülecek grup
        seesaw_group = VGroup(board, dig_cam, imax_cam, lbl_dig, lbl_imax)
        seesaw_group.save_state()

        # pivot etrafında döndür
        self.play(
            Rotate(
                seesaw_group,
                angle=TILT_ANGLE,
                about_point=pivot,
                rate_func=rate_functions.ease_in_quad,
            ),
            run_time=1.0,
        )

        # Küçük sıçrama (zemine çarptı hissi)
        self.play(
            Rotate(
                seesaw_group,
                angle=3 * DEGREES,
                about_point=pivot,
                rate_func=there_and_back,
            ),
            run_time=0.35,
        )

        self.wait(0.5)

        # ── Ağırlık farkı vurgusu ────────────────────────────────────────
        ratio_lbl = Text("15 kat daha ağır!", font="Courier New",
                         font_size=38, color=ACCENT).move_to(UP * 3.2)
        sub_lbl   = Text("Sırtınızda buzdolabı taşımak gibi!",
                         font="Courier New", font_size=20,
                         color=DIM_CLR).next_to(ratio_lbl, DOWN, buff=0.28)

        self.play(Write(ratio_lbl), run_time=0.9)
        self.play(FadeIn(sub_lbl),  run_time=0.6)

        # IMAX kamerası üzerinde vurgu halkası
        ring = Circle(radius=1.05,
                      stroke_color=ACCENT, stroke_width=2.5,
                      fill_opacity=0)
        ring.move_to(imax_cam.get_center())
        self.play(Create(ring), run_time=0.6)
        self.play(ring.animate.scale(1.15).set_opacity(0), run_time=0.5)

        self.wait(2.0)