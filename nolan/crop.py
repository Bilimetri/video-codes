from manim import *
import numpy as np

BG     = "#0A0A0F"
WARM   = "#C8A96E"
COLD   = "#4FC3F7"
ACCENT = "#FF4444"
WHITE_ = "#F0F0F8"
DIM    = "#3A3A5A"
GOLD   = "#D4AF37"
GREEN  = "#4ADE80"


class CroppingScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 1 — TAM IMAX KARESİ (1.43:1)
        # ══════════════════════════════════════════════════════════════════

        title = Text("Sinemada Kaybedilen Dünya",
                     font="Courier New", weight=BOLD,
                     font_size=28, color=WARM).move_to(UP*3.5)
        self.play(Write(title), run_time=1.0)

        # IMAX 1.43:1 oranı — neredeyse kare
        # Manim'de: genişlik 8.0, yükseklik 8.0/1.43 ≈ 5.6
        IMAX_W = 8.5
        IMAX_H = 8.5 / 1.43   # ≈ 5.94

        imax_frame = Rectangle(
            width=IMAX_W, height=IMAX_H,
            fill_color="#0A1018", fill_opacity=1,
            stroke_color=WARM, stroke_width=3,
        ).move_to(DOWN*0.2)

        # İç manzara — soyut peyzaj
        sky = Rectangle(width=IMAX_W-0.1, height=IMAX_H*0.45,
                        fill_color="#0D1F35", fill_opacity=1,
                        stroke_width=0)
        sky.move_to(imax_frame.get_center() + UP*(IMAX_H*0.275))

        ground = Rectangle(width=IMAX_W-0.1, height=IMAX_H*0.55,
                           fill_color="#0F1A10", fill_opacity=1,
                           stroke_width=0)
        ground.move_to(imax_frame.get_center() + DOWN*(IMAX_H*0.225))

        # Dağlar
        mountains = VGroup()
        for mx, mh, mc in [(-2.8, 1.6, "#1A2A1A"), (0.0, 2.1, "#223322"),
                            (2.5, 1.4, "#1A2A1A"), (-3.2, 1.2, "#152015"),
                            (3.2, 1.0, "#152015")]:
            tri = Triangle(fill_color=mc, fill_opacity=1, stroke_width=0)
            tri.stretch_to_fit_width(mh*1.3).stretch_to_fit_height(mh)
            tri.move_to(imax_frame.get_center() + RIGHT*mx + DOWN*(IMAX_H*0.10))
            mountains.add(tri)

        # Yıldızlar
        stars = VGroup()
        rng = np.random.default_rng(5)
        for _ in range(40):
            sx = rng.uniform(-IMAX_W/2+0.2, IMAX_W/2-0.2)
            sy = rng.uniform(0.2, IMAX_H/2-0.3)
            s  = Dot(radius=0.03, color=WHITE_, fill_opacity=rng.uniform(0.4, 0.9))
            s.move_to(imax_frame.get_center() + RIGHT*sx + UP*sy)
            stars.add(s)

        imax_content = VGroup(sky, ground, mountains, stars)

        imax_label = Text("Tam IMAX Karesi (1.43:1) — Yönetmenin Vizyonu",
                          font="Courier New", font_size=18, color=WARM)
        imax_label.next_to(imax_frame, DOWN, buff=0.28)

        # Giriş animasyonu
        imax_frame.scale(0.01)
        imax_content.scale(0.01).move_to(imax_frame.get_center())

        self.play(
            imax_frame.animate.scale(100),
            imax_content.animate.scale(100),
            run_time=1.0, rate_func=rush_from,
        )
        self.play(Write(imax_label), run_time=0.8)
        self.wait(1.0)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 2 — STANDART SİNEMA DİKDÖRTGENİ (2.39:1) ORTAYA YERLEŞİR
        # ══════════════════════════════════════════════════════════════════

        # 2.39:1 dikdörtgeni — aynı genişlik, daha kısa
        STD_W = IMAX_W
        STD_H = IMAX_W / 2.39   # ≈ 3.56

        std_frame = Rectangle(
            width=STD_W, height=STD_H,
            fill_opacity=0,
            stroke_color=COLD, stroke_width=2.5,
        ).move_to(imax_frame.get_center())

        std_label = Text("Standart Sinema (2.39:1)",
                         font="Courier New", font_size=16, color=COLD)
        std_label.next_to(std_frame, UP, buff=0.15)

        self.play(Create(std_frame), run_time=0.9)
        self.play(Write(std_label), run_time=0.6)
        self.wait(0.6)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 3 — DIŞARIDA KALAN ALANLAR KIRMIZIYA DÖNER
        # ══════════════════════════════════════════════════════════════════

        # Üst şerit (crop alanı)
        top_crop_h = (IMAX_H - STD_H) / 2
        top_crop = Rectangle(
            width=IMAX_W - 0.1, height=top_crop_h,
            fill_color=ACCENT, fill_opacity=0,
            stroke_width=0,
        )
        top_crop.move_to(
            imax_frame.get_center() + UP*(STD_H/2 + top_crop_h/2)
        )

        bot_crop = Rectangle(
            width=IMAX_W - 0.1, height=top_crop_h,
            fill_color=ACCENT, fill_opacity=0,
            stroke_width=0,
        )
        bot_crop.move_to(
            imax_frame.get_center() + DOWN*(STD_H/2 + top_crop_h/2)
        )

        self.add(top_crop, bot_crop)

        # Kırmızıya dön
        self.play(
            top_crop.animate.set_fill(opacity=0.55),
            bot_crop.animate.set_fill(opacity=0.55),
            run_time=0.9, rate_func=smooth,
        )

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 4 — "KAYIP BİLGİ" ÇARPI İŞARETLERİ
        # ══════════════════════════════════════════════════════════════════

        lost_labels = VGroup()
        for crop_rect, sign in [(top_crop, 1), (bot_crop, -1)]:
            cx = crop_rect.get_center()

            # ✕ işareti
            cross = VGroup(
                Line(LEFT*0.22 + UP*0.22, RIGHT*0.22 + DOWN*0.22,
                     stroke_color=WHITE_, stroke_width=2.5),
                Line(LEFT*0.22 + DOWN*0.22, RIGHT*0.22 + UP*0.22,
                     stroke_color=WHITE_, stroke_width=2.5),
            ).move_to(cx + LEFT*2.5)

            lost_txt = Text("KAYIP BİLGİ", font="Courier New",
                            weight=BOLD, font_size=14, color=WHITE_)
            lost_txt.move_to(cx)

            lost_info = Text("(LOST INFO)", font="Courier New",
                             font_size=11, color=WHITE_, slant=ITALIC)
            lost_info.next_to(lost_txt, RIGHT, buff=0.2)

            lost_labels.add(VGroup(cross, lost_txt, lost_info))

        self.play(
            LaggedStart(
                *[FadeIn(l, scale=0.7) for l in lost_labels],
                lag_ratio=0.25,
            ),
            run_time=0.9,
        )
        self.wait(0.8)

        # Alan oranı notu
        crop_pct = (1 - STD_H / IMAX_H) * 100
        pct_lbl = Text(
            f"Kaybedilen alan:  %{crop_pct:.0f}",
            font="Courier New", weight=BOLD, font_size=20, color=ACCENT,
        )
        pct_lbl.next_to(imax_frame, DOWN, buff=0.1)

        self.play(
            FadeOut(imax_label),
            Write(pct_lbl),
            run_time=0.7,
        )
        self.wait(0.8)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 5 — KIRMIZI ALANLAR SOLAR, SADECE STANDART ŞERİT KALIR
        # ══════════════════════════════════════════════════════════════════

        # İçerik ve crop alanları fade-out
        self.play(
            top_crop.animate.set_fill(color="#000000", opacity=0.92),
            bot_crop.animate.set_fill(color="#000000", opacity=0.92),
            FadeOut(lost_labels),
            run_time=1.4, rate_func=smooth,
        )
        self.wait(0.3)

        # Standart şerit dışındaki her şeyi siyaha göm
        mask_top = Rectangle(
            width=IMAX_W + 0.2, height=top_crop_h + 0.05,
            fill_color="#000000", fill_opacity=1, stroke_width=0,
        ).move_to(top_crop.get_center())
        mask_bot = Rectangle(
            width=IMAX_W + 0.2, height=top_crop_h + 0.05,
            fill_color="#000000", fill_opacity=1, stroke_width=0,
        ).move_to(bot_crop.get_center())

        self.play(FadeIn(mask_top), FadeIn(mask_bot), run_time=0.6)

        # Standart çerçeve vurgusu
        self.play(
            std_frame.animate.set_stroke(color=COLD, width=4),
            run_time=0.3,
        )
        self.play(
            std_frame.animate.set_stroke(width=2.5),
            run_time=0.3,
        )

        final_lbl = Text("İzleyici yalnızca bu daracık şeridi izler.",
                         font="Courier New", font_size=18, color=COLD)
        final_lbl.next_to(imax_frame, DOWN, buff=0.12)

        self.play(FadeOut(pct_lbl), FadeOut(std_label), run_time=0.4)
        self.play(Write(final_lbl), run_time=0.9)
        self.wait(0.8)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 6 — MATEMATİKSEL NET LİK
        # Önce her şey küçülüp yukarı kayar, sonra kutu gelir
        # ══════════════════════════════════════════════════════════════════

        # Sahnedeki tüm objeleri bir gruba topla ve yukarı kaydır
        scene_group = VGroup(
            imax_frame, imax_content,
            std_frame, top_crop, bot_crop,
            mask_top, mask_bot,
            final_lbl, title,
        )

        self.play(
            scene_group.animate.scale(0.55).move_to(UP * 1.8),
            run_time=1.0, rate_func=smooth,
        )
        self.wait(0.2)

        # Kutu yerden 3 birim yukarıda → DOWN*1 (ekran merkezi 0, alt kenar ~-4)
        note_bg = RoundedRectangle(
            corner_radius=0.3, width=11.5, height=1.55,
            fill_color="#000000", fill_opacity=0.85,
            stroke_color=GOLD, stroke_width=2.2,
        ).move_to(DOWN * 2.5)

        imax_area = IMAX_W * IMAX_H
        std_area  = STD_W  * STD_H
        ratio     = imax_area / std_area

        note_line1 = Text(
            f"IMAX karesi: {IMAX_W:.1f} × {IMAX_H:.1f}  |  "
            f"Standart: {STD_W:.1f} × {STD_H:.1f}",
            font="Courier New", font_size=17, color=WHITE_,
        ).move_to(note_bg.get_center() + UP*0.30)

        note_line2 = Text(
            f"IMAX'in standart sinema şeridine oranı: {ratio:.1f} kat daha fazla görüntü",
            font="Courier New", weight=BOLD, font_size=18, color=GOLD,
        ).move_to(note_bg.get_center() + DOWN*0.28)

        self.play(FadeIn(note_bg, scale=0.92), run_time=0.6)
        self.play(Write(note_line1), run_time=1.0)
        self.play(Write(note_line2), run_time=1.1)
        self.wait(2.8)