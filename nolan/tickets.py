from manim import *
import numpy as np

BG     = "#0A0A0F"
WARM   = "#C8A96E"
COLD   = "#4FC3F7"
GREEN  = "#4ADE80"
ACCENT = "#FF6B6B"
WHITE_ = "#F0F0F8"
DIM    = "#3A3A5A"
GOLD   = "#D4AF37"
PURPLE = "#A78BFA"


class TicketRevenueScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ══════════════════════════════════════════════════════════════════
        # BAŞLIK
        # ══════════════════════════════════════════════════════════════════
        title = Text("Bilet Geliri Karşılaştırması",
                     font="Courier New", weight=BOLD,
                     font_size=30, color=WARM).move_to(UP*3.5)
        self.play(Write(title), run_time=1.0)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 1 — BİLET FİYATI KARŞILAŞTIRMASI (yatay bar)
        # ══════════════════════════════════════════════════════════════════

        price_title = Text("Ortalama Bilet Fiyatı  (ABD, 2023)",
                           font="Courier New", font_size=20,
                           color=DIM).move_to(UP*2.7)
        self.play(FadeIn(price_title), run_time=0.6)

        # Veriler
        price_data = [
            ("Matine",          9,   "#555577"),
            ("Standart",        15,  COLD),
            ("3D",              19,  PURPLE),
            ("IMAX  Dijital",   23,  GREEN),
            ("IMAX  70mm Film", 32,  WARM),
        ]
        MAX_PRICE  = 35
        BAR_W_MAX  = 6.0
        BAR_H      = 0.42
        BAR_GAP    = 0.72
        BAR_START_Y = 1.9
        BAR_X_LEFT  = -0.5   # barların sol kenarı

        price_bars   = []
        price_labels = VGroup()
        price_vals   = VGroup()

        for i, (name, price, color) in enumerate(price_data):
            y = BAR_START_Y - i * BAR_GAP

            # Arka plan
            bg = Rectangle(width=BAR_W_MAX, height=BAR_H,
                           fill_color="#0A0A14", fill_opacity=1,
                           stroke_color=DIM, stroke_width=0.8)
            bg.move_to([BAR_X_LEFT + BAR_W_MAX/2, y, 0])

            # Dolu kısım
            fill_w = BAR_W_MAX * (price / MAX_PRICE)
            fill = Rectangle(width=0.001, height=BAR_H,
                             fill_color=color, fill_opacity=0.88,
                             stroke_width=0)
            fill.move_to([BAR_X_LEFT + 0.001/2, y, 0])

            # İsim
            lbl = Text(name, font="Courier New", font_size=15, color=color)
            lbl.move_to([BAR_X_LEFT - 1.55, y, 0])

            # Fiyat
            val = Text(f"${price}", font="Courier New",
                       weight=BOLD, font_size=16, color=color)
            val.move_to([BAR_X_LEFT + BAR_W_MAX + 0.5, y, 0])

            price_bars.append((bg, fill, fill_w, val))
            price_labels.add(lbl)
            price_vals.add(val)

        # Önce arka planlar ve isimler
        self.play(
            LaggedStart(
                *[FadeIn(b[0]) for b in price_bars],
                lag_ratio=0.1,
            ),
            LaggedStart(
                *[Write(lbl) for lbl in price_labels],
                lag_ratio=0.1,
            ),
            run_time=1.2,
        )

        # Barlar sırayla büyür
        for bg, fill, fill_w, val in price_bars:
            self.add(fill)
            self.play(
                fill.animate
                    .stretch_to_fit_width(fill_w)
                    .move_to([BAR_X_LEFT + fill_w/2,
                               bg.get_center()[1], 0]),
                run_time=0.55, rate_func=smooth,
            )
            self.play(FadeIn(val), run_time=0.2)

        # IMAX 70mm barı pulse
        imax_fill = price_bars[-1][1]
        self.play(imax_fill.animate.set_fill(color=GOLD), run_time=0.2)
        self.play(imax_fill.animate.set_fill(color=WARM), run_time=0.2)
        self.wait(0.8)

        # Fiyat bölümünü temizle (barlar üstte küçük kalsın)
        price_group = VGroup(price_title,
                             *[b[0] for b in price_bars],
                             *[b[1] for b in price_bars],
                             *[b[3] for b in price_bars],
                             price_labels)
        self.play(
            price_group.animate.scale(0.52).move_to(LEFT*3.8 + UP*1.8),
            run_time=0.9, rate_func=smooth,
        )

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 2 — KOLTUK BAŞINA GELİR (sütun grafik)
        # ══════════════════════════════════════════════════════════════════

        col_title = Text("Oppenheimer — Koltuk Başına Ortalama Gelir",
                         font="Courier New", font_size=18,
                         color=DIM).move_to(RIGHT*2.5 + UP*2.85)
        self.play(Write(col_title), run_time=0.7)

        # Eksen
        axis_origin = np.array([0.0, -1.0, 0])
        axis_x = Line(axis_origin, axis_origin + RIGHT*6.5,
                      stroke_color=DIM, stroke_width=1.5)
        axis_y = Line(axis_origin, axis_origin + UP*3.5,
                      stroke_color=DIM, stroke_width=1.5)

        self.play(Create(axis_x), Create(axis_y), run_time=0.6)

        # Sütun verileri  ($ / koltuk başına, tüm sürece göre ortalama)
        col_data = [
            ("Standart\n2D",    18,  COLD),
            ("Standart\n3D",    24,  PURPLE),
            ("IMAX\nDijital",   31,  GREEN),
            ("IMAX\n70mm",      47,  WARM),
        ]
        MAX_COL   = 55
        COL_W     = 0.85
        COL_GAP   = 0.55
        COL_MAX_H = 3.2
        COL_START_X = axis_origin[0] + 0.85

        col_rects  = []
        col_labels = VGroup()
        col_vals   = VGroup()

        for i, (name, val, color) in enumerate(col_data):
            x = COL_START_X + i * (COL_W + COL_GAP)
            target_h = COL_MAX_H * (val / MAX_COL)

            col_bg = Rectangle(
                width=COL_W, height=COL_MAX_H,
                fill_color="#0A0A14", fill_opacity=1,
                stroke_color=DIM, stroke_width=0.5,
            ).move_to([x, axis_origin[1] + COL_MAX_H/2, 0])

            col_fill = Rectangle(
                width=COL_W, height=0.001,
                fill_color=color, fill_opacity=0.9,
                stroke_width=0,
            ).move_to([x, axis_origin[1] + 0.001/2, 0])

            lbl = Text(name, font="Courier New", font_size=13,
                       color=color, line_spacing=1.1)
            lbl.move_to([x, axis_origin[1] - 0.55, 0])

            v_lbl = Text(f"${val}", font="Courier New",
                         weight=BOLD, font_size=16, color=color)
            v_lbl.move_to([x, axis_origin[1] + target_h + 0.25, 0])

            col_rects.append((col_bg, col_fill, target_h, v_lbl, x))
            col_labels.add(lbl)

        # Yatay yardımcı çizgiler
        for dollar in [10, 20, 30, 40, 50]:
            h = COL_MAX_H * (dollar / MAX_COL)
            grid_line = DashedLine(
                axis_origin + RIGHT*0.1,
                axis_origin + RIGHT*6.2,
                stroke_color=DIM, stroke_width=0.7,
                stroke_opacity=0.5, dash_length=0.15,
            ).move_to([axis_origin[0] + 3.15,
                        axis_origin[1] + h, 0])
            grid_lbl = Text(f"${dollar}", font="Courier New",
                            font_size=11, color=DIM)
            grid_lbl.move_to([axis_origin[0] - 0.45, axis_origin[1] + h, 0])
            self.add(grid_line, grid_lbl)

        self.play(
            LaggedStart(*[FadeIn(r[0]) for r in col_rects], lag_ratio=0.1),
            LaggedStart(*[Write(lbl) for lbl in col_labels], lag_ratio=0.1),
            run_time=1.0,
        )

        # Sütunlar yukarı büyür
        for col_bg, col_fill, target_h, v_lbl, x in col_rects:
            self.add(col_fill)
            self.play(
                col_fill.animate
                    .stretch_to_fit_height(target_h)
                    .move_to([x, axis_origin[1] + target_h/2, 0]),
                run_time=0.7, rate_func=smooth,
            )
            self.play(FadeIn(v_lbl), run_time=0.25)

        # IMAX 70mm sütunu altın pulse
        imax_col = col_rects[-1][1]
        self.play(imax_col.animate.set_fill(color=GOLD), run_time=0.2)
        self.play(imax_col.animate.set_fill(color=WARM), run_time=0.2)
        self.wait(0.6)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 3 — IMAX GELİR PAYI  (sol boşlukta)
        # ══════════════════════════════════════════════════════════════════

        PIE_CENTER   = np.array([-4.5, -1.5, 0])
        PIE_R        = 1.1
        IMAX_SHARE   = 0.225
        STD_ANGLE    = TAU * (1 - IMAX_SHARE)
        IMAX_ANGLE   = TAU * IMAX_SHARE
        START        = PI / 2

        pie_title = Text("Oppenheimer Gişesi\n$952M toplam",
                         font="Courier New", font_size=16,
                         color=WHITE_, line_spacing=1.2)
        pie_title.move_to(PIE_CENTER + UP*1.55)

        def make_sector(center, radius, start_angle, angle, color, opacity=0.88):
            n_pts  = max(60, int(abs(angle) / TAU * 120))
            angles = np.linspace(start_angle, start_angle + angle, n_pts)
            verts  = [center]
            for a in angles:
                verts.append(center + radius * np.array([np.cos(a), np.sin(a), 0]))
            verts.append(center)
            return Polygon(*verts,
                           fill_color=color, fill_opacity=opacity,
                           stroke_color=BG, stroke_width=1.5)

        std_sector  = make_sector(PIE_CENTER, PIE_R,
                                  START, STD_ANGLE, COLD,  opacity=0.75)
        imax_sector = make_sector(PIE_CENTER, PIE_R,
                                  START + STD_ANGLE, IMAX_ANGLE, WARM, opacity=0.95)

        pie_outline = Circle(radius=PIE_R, fill_opacity=0,
                             stroke_color=DIM, stroke_width=1.5)
        pie_outline.move_to(PIE_CENTER)

        std_mid_a  = START + STD_ANGLE / 2
        imax_mid_a = START + STD_ANGLE + IMAX_ANGLE / 2

        pie_lbl_std = Text("Standart\n%77.5",
                           font="Courier New", font_size=13, color=WHITE_)
        pie_lbl_std.move_to(
            PIE_CENTER + 0.62 * PIE_R * np.array([np.cos(std_mid_a),
                                                    np.sin(std_mid_a), 0])
        )

        imax_tip     = PIE_CENTER + 1.18 * PIE_R * np.array([np.cos(imax_mid_a), np.sin(imax_mid_a), 0])
        imax_lbl_pos = PIE_CENTER + 1.70 * PIE_R * np.array([np.cos(imax_mid_a), np.sin(imax_mid_a), 0])
        pie_lbl_imax = Text("IMAX\n%22.5", font="Courier New",
                            font_size=14, color=WHITE_, weight=BOLD)
        pie_lbl_imax.move_to(imax_lbl_pos)

        imax_ptr = Line(imax_tip,
                        PIE_CENTER + 1.38 * PIE_R * np.array([np.cos(imax_mid_a), np.sin(imax_mid_a), 0]),
                        stroke_color=WARM, stroke_width=1.8)

        self.play(Write(pie_title), run_time=0.7)
        self.play(FadeIn(std_sector), run_time=0.7)
        self.play(FadeIn(imax_sector), run_time=0.5)
        self.play(FadeIn(pie_outline), run_time=0.3)
        self.play(Write(pie_lbl_std), Write(pie_lbl_imax), Create(imax_ptr), run_time=0.9)

        explode_vec = 0.18 * np.array([np.cos(imax_mid_a), np.sin(imax_mid_a), 0])
        self.play(imax_sector.animate.shift(explode_vec), run_time=0.5)
        self.wait(0.8)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 4 — SON NOT
        # ══════════════════════════════════════════════════════════════════

        note_bg = RoundedRectangle(
            corner_radius=0.28, width=12.8, height=0.88,
            fill_color="#000000", fill_opacity=0.82,
            stroke_color=GOLD, stroke_width=2,
        ).move_to(DOWN*3.3)

        note_txt = Text(
            "IMAX salonları toplam koltukların %4'ü iken gelirin %22'sini tek başına üretiyor.",
            font="Courier New", weight=BOLD, font_size=19, color=GOLD,
        ).move_to(note_bg.get_center())

        self.play(FadeIn(note_bg), run_time=0.5)
        self.play(Write(note_txt), run_time=1.4)
        self.wait(2.8)