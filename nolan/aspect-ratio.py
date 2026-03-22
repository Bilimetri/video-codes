from manim import *
import numpy as np

BG     = "#0A0A0F"
WARM   = "#C8A96E"
COLD   = "#4FC3F7"
WHITE_ = "#F0F0F8"
DIM    = "#3A3A5A"
GOLD   = "#D4AF37"
ACCENT = "#FF6B6B"
GREEN  = "#4ADE80"

# Nolan filmlerindeki gerçek aspect ratio'lar
RATIOS = {
    "IMAX  (1.43:1)":         1.43,
    "Standart  (1.85:1)":     1.85,
    "Standart Geniş  (2.39:1)": 2.39,
}

# Oppenheimer sahnelerinden esinlenen arka plan renkleri
SCENE_PALETTES = [
    ("#0A1A2A", "#1A2A3A"),   # gece / mavi
    ("#1A0A08", "#2A1510"),   # ateş / kırmızı
    ("#0A0A0A", "#1A1A1A"),   # siyah / nükleer
]


def make_screen(width, height, fill_top, fill_bot,
                border_color=WHITE_, border_w=2.5) -> VGroup:
    """Gradient hissi veren iki katmanlı ekran."""
    top = Rectangle(width=width, height=height/2,
                    fill_color=fill_top, fill_opacity=1,
                    stroke_width=0)
    top.move_to([0, height/4, 0])
    bot = Rectangle(width=width, height=height/2,
                    fill_color=fill_bot, fill_opacity=1,
                    stroke_width=0)
    bot.move_to([0, -height/4, 0])
    border = Rectangle(width=width, height=height,
                       fill_opacity=0,
                       stroke_color=border_color,
                       stroke_width=border_w)
    return VGroup(top, bot, border)


def make_bars(screen_h, max_h, color="#000000") -> VGroup:
    """Letterbox barları (üst ve alt siyah bant)."""
    bar_h = (max_h - screen_h) / 2
    if bar_h <= 0:
        return VGroup()
    top_bar = Rectangle(width=16, height=bar_h,
                        fill_color=color, fill_opacity=1,
                        stroke_width=0)
    top_bar.move_to(UP * (screen_h/2 + bar_h/2))
    bot_bar = Rectangle(width=16, height=bar_h,
                        fill_color=color, fill_opacity=1,
                        stroke_width=0)
    bot_bar.move_to(DOWN * (screen_h/2 + bar_h/2))
    return VGroup(top_bar, bot_bar)


class AspectRatioScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        SCREEN_W = 9.5   # sabit genişlik
        MAX_H    = 5.8   # IMAX yüksekliği (referans)

        # ══════════════════════════════════════════════════════════════════
        # BAŞLIK
        # ══════════════════════════════════════════════════════════════════
        title = Text("En-Boy Oranı (Aspect Ratio)",
                     font="Courier New", weight=BOLD,
                     font_size=26, color=WARM).move_to(UP*3.6)
        self.play(Write(title), run_time=0.9)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 1 — IMAX 1.43:1  (neredeyse tam kare, devasa)
        # ══════════════════════════════════════════════════════════════════

        ratio_143  = 1.43
        h_143      = SCREEN_W / ratio_143   # ≈ 6.64 → clip to MAX_H
        h_143      = min(h_143, MAX_H)

        screen_143 = make_screen(SCREEN_W, h_143, "#0A1A2A", "#1A2A3A",
                                 border_color=WARM, border_w=3)
        screen_143.move_to(DOWN * 0.15)

        # İç içerik — basit sahne çizgileri
        horizon = Line(LEFT*4.5, RIGHT*4.5,
                       stroke_color="#2A4A6A", stroke_width=1.5,
                       stroke_opacity=0.7)
        horizon.move_to(DOWN*0.5)

        # Küçük insan silueti (tam IMAX'te küçük kalır)
        silhouette = VGroup(
            Circle(radius=0.12, fill_color=WHITE_, fill_opacity=0.9,
                   stroke_width=0),
            Rectangle(width=0.22, height=0.38, fill_color=WHITE_,
                      fill_opacity=0.9, stroke_width=0).shift(DOWN*0.28),
        )
        silhouette.move_to(DOWN*0.35)

        lbl_143 = Text("IMAX  1.43:1  —  Tam Kare",
                       font="Courier New", weight=BOLD,
                       font_size=20, color=WARM)
        lbl_143.move_to(DOWN*3.2)

        sub_143 = Text("Oppenheimer, Interstellar, Dunkirk — IMAX sahneleri",
                       font="Courier New", font_size=14, color=DIM)
        sub_143.next_to(lbl_143, DOWN, buff=0.15)

        # Boyut etiketi (köşede)
        dim_lbl_143 = Text(f"{SCREEN_W:.1f} × {h_143:.2f}",
                           font="Courier New", font_size=13, color=DIM)
        dim_lbl_143.move_to(screen_143[2].get_corner(UR) + LEFT*0.8 + DOWN*0.22)

        # Giriş: ekran yukarıdan aşağı açılır
        screen_143.stretch_to_fit_height(0.01)
        self.play(
            screen_143.animate.stretch_to_fit_height(h_143),
            run_time=1.0, rate_func=smooth,
        )
        self.play(
            FadeIn(horizon),
            FadeIn(silhouette),
            FadeIn(dim_lbl_143),
            run_time=0.5,
        )
        self.play(Write(lbl_143), FadeIn(sub_143), run_time=0.7)
        self.wait(1.2)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 2 — 1.85:1'E GEÇİŞ (siyah bantlar yukarı-aşağı iner)
        # ══════════════════════════════════════════════════════════════════

        ratio_185 = 1.85
        h_185     = SCREEN_W / ratio_185   # ≈ 5.13

        # Siyah letterbox bantları
        bar_h_185 = (h_143 - h_185) / 2
        bars_185  = make_bars(h_185, h_143, color="#000000")

        lbl_185 = Text("Standart  1.85:1",
                       font="Courier New", weight=BOLD,
                       font_size=20, color=COLD)
        lbl_185.move_to(DOWN*3.2)
        sub_185 = Text("Geleneksel Hollywood formatı",
                       font="Courier New", font_size=14, color=DIM)
        sub_185.next_to(lbl_185, DOWN, buff=0.15)

        dim_lbl_185 = Text(f"{SCREEN_W:.1f} × {h_185:.2f}",
                           font="Courier New", font_size=13, color=DIM)
        dim_lbl_185.move_to(screen_143[2].get_corner(UR) + LEFT*0.8 + DOWN*0.22)

        self.play(
            FadeOut(lbl_143), FadeOut(sub_143), FadeOut(dim_lbl_143),
            run_time=0.3,
        )

        # Bantlar iner
        bars_185[0].shift(UP * bar_h_185)
        bars_185[1].shift(DOWN * bar_h_185)
        self.play(
            bars_185[0].animate.shift(DOWN * bar_h_185),
            bars_185[1].animate.shift(UP   * bar_h_185),
            run_time=0.9, rate_func=smooth,
        )

        # Ekran rengi değişir (IMAX → Standart)
        self.play(
            screen_143[0].animate.set_fill(color="#0D0D1A"),
            screen_143[1].animate.set_fill(color="#1A1A2A"),
            screen_143[2].animate.set_stroke(color=COLD),
            run_time=0.5,
        )

        self.play(
            Write(lbl_185), FadeIn(sub_185), FadeIn(dim_lbl_185),
            run_time=0.7,
        )
        self.wait(1.0)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 3 — 2.39:1'E GEÇİŞ (bantlar daha da iner)
        # ══════════════════════════════════════════════════════════════════

        ratio_239  = 2.39
        h_239      = SCREEN_W / ratio_239   # ≈ 3.97
        bar_h_239  = (h_143 - h_239) / 2
        extra_drop = bar_h_239 - bar_h_185

        lbl_239 = Text("Sinema Skop  2.39:1",
                       font="Courier New", weight=BOLD,
                       font_size=20, color=ACCENT)
        lbl_239.move_to(DOWN*3.2)
        sub_239 = Text("Çoğu aksiyon ve epik film formatı",
                       font="Courier New", font_size=14, color=DIM)
        sub_239.next_to(lbl_239, DOWN, buff=0.15)

        dim_lbl_239 = Text(f"{SCREEN_W:.1f} × {h_239:.2f}",
                           font="Courier New", font_size=13, color=DIM)
        dim_lbl_239.move_to(screen_143[2].get_corner(UR) + LEFT*0.8 + DOWN*0.22)

        self.play(
            FadeOut(lbl_185), FadeOut(sub_185), FadeOut(dim_lbl_185),
            run_time=0.3,
        )
        self.play(
            bars_185[0].animate.shift(DOWN * extra_drop),
            bars_185[1].animate.shift(UP   * extra_drop),
            run_time=0.9, rate_func=smooth,
        )
        self.play(
            screen_143[0].animate.set_fill(color="#1A0A05"),
            screen_143[1].animate.set_fill(color="#2A1008"),
            screen_143[2].animate.set_stroke(color=ACCENT),
            run_time=0.5,
        )
        self.play(
            Write(lbl_239), FadeIn(sub_239), FadeIn(dim_lbl_239),
            run_time=0.7,
        )
        self.wait(1.0)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 4 — GERİ IMAX'E: BANTLAR KALKAR, EKRAN AÇILIR
        # ══════════════════════════════════════════════════════════════════

        lbl_back = Text("IMAX'e geri dön  →  1.43:1",
                        font="Courier New", weight=BOLD,
                        font_size=20, color=WARM)
        lbl_back.move_to(DOWN*3.2)
        sub_back = Text("Nolan bu geçişi dramatik etki için kullanır",
                        font="Courier New", font_size=14, color=DIM)
        sub_back.next_to(lbl_back, DOWN, buff=0.15)

        self.play(
            FadeOut(lbl_239), FadeOut(sub_239), FadeOut(dim_lbl_239),
            run_time=0.3,
        )

        # Bantlar kalkar — daha yavaş ve dramatik
        self.play(
            bars_185[0].animate.shift(UP   * bar_h_239),
            bars_185[1].animate.shift(DOWN * bar_h_239),
            screen_143[0].animate.set_fill(color="#0A1A2A"),
            screen_143[1].animate.set_fill(color="#1A2A3A"),
            screen_143[2].animate.set_stroke(color=WARM, width=3.5),
            run_time=1.4, rate_func=smooth,
        )

        self.play(Write(lbl_back), FadeIn(sub_back), run_time=0.7)
        self.wait(0.8)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 5 — YAN YANA KARŞILAŞTIRMA
        # ══════════════════════════════════════════════════════════════════

        self.play(
            FadeOut(VGroup(
                screen_143, bars_185, horizon, silhouette,
                lbl_back, sub_back, title,
            )),
            run_time=0.8,
        )
        self.wait(0.2)

        compare_title = Text("Yan Yana Karşılaştırma",
                             font="Courier New", weight=BOLD,
                             font_size=24, color=WARM).move_to(UP*3.5)
        self.play(Write(compare_title), run_time=0.7)

        # Üç ekran yan yana — aynı genişlikte
        COMP_W = 2.8
        ratios_comp = [
            ("IMAX\n1.43:1",        1.43, WARM,   LEFT*4.2),
            ("Standart\n1.85:1",    1.85, COLD,   ORIGIN),
            ("Skop\n2.39:1",        2.39, ACCENT, RIGHT*4.2),
        ]
        fills = [
            ("#0A1A2A", "#1A2A3A"),
            ("#0D0D1A", "#1A1A2A"),
            ("#1A0A05", "#2A1008"),
        ]

        comp_screens = VGroup()
        comp_labels  = VGroup()

        for (name, ratio, color, pos), (ft, fb) in zip(ratios_comp, fills):
            h = COMP_W / ratio
            scr = make_screen(COMP_W, h, ft, fb,
                              border_color=color, border_w=2.2)
            scr.move_to(np.array([pos[0], -0.3 + (MAX_H/1.43 - h)/2, 0])
                        if False else np.array([pos[0], 0.0, 0]))

            # Ekranı ortaya hizala — üst kenar sabit
            scr.move_to(pos)
            scr.shift(UP * (COMP_W/1.43/2 - h/2))  # üst kenar hizala

            lbl = Text(name, font="Courier New", font_size=15,
                       color=color, line_spacing=1.1)
            lbl.next_to(scr, DOWN, buff=0.25)

            h_lbl = Text(f"×{COMP_W/1.43/h:.2f} kayıp" if ratio > 1.43
                         else "TAM KARE",
                         font="Courier New", font_size=12,
                         color=color if ratio == 1.43 else DIM)
            h_lbl.next_to(lbl, DOWN, buff=0.1)

            comp_screens.add(VGroup(scr, lbl, h_lbl))

        self.play(
            LaggedStart(
                *[FadeIn(s, scale=0.88) for s in comp_screens],
                lag_ratio=0.2,
            ),
            run_time=1.4,
        )
        self.wait(0.8)

        # IMAX vurgusu — pulse + büyüme
        imax_screen = comp_screens[0]
        self.play(
            imax_screen.animate.scale(1.1),
            run_time=0.3, rate_func=smooth,
        )
        self.play(
            imax_screen.animate.scale(1/1.1),
            run_time=0.3, rate_func=smooth,
        )
        self.wait(0.5)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 6 — ALAN KAYBI VURGUSU (kırmızı kayıp alanlar)
        # ══════════════════════════════════════════════════════════════════

        imax_scr  = comp_screens[0][0]
        std_scr   = comp_screens[1][0]
        skop_scr  = comp_screens[2][0]

        imax_h  = COMP_W / 1.43
        std_h   = COMP_W / 1.85
        skop_h  = COMP_W / 2.39

        def lost_overlay(ref_scr, ref_h, target_h, color=ACCENT):
            """Üst ve altta kayıp alan kırmızı şeridi."""
            lost_h = (ref_h - target_h) / 2
            if lost_h <= 0.01:
                return VGroup()
            top_lost = Rectangle(
                width=COMP_W - 0.04, height=lost_h,
                fill_color=color, fill_opacity=0.45, stroke_width=0,
            ).move_to(ref_scr.get_center() + UP*(target_h/2 + lost_h/2))
            bot_lost = Rectangle(
                width=COMP_W - 0.04, height=lost_h,
                fill_color=color, fill_opacity=0.45, stroke_width=0,
            ).move_to(ref_scr.get_center() + DOWN*(target_h/2 + lost_h/2))
            return VGroup(top_lost, bot_lost)

        lost_std  = lost_overlay(imax_scr, imax_h, std_h)
        lost_skop = lost_overlay(skop_scr, imax_h, skop_h)

        # Standart formatın IMAX'e göre kaybı
        lost_std_pct  = (1 - std_h/imax_h)  * 100
        lost_skop_pct = (1 - skop_h/imax_h) * 100

        lost_std_lbl  = Text(f"−%{lost_skop_pct:.0f} görüntü",
                             font="Courier New", font_size=13,
                             color=ACCENT)
        lost_skop_lbl = Text(f"−%{lost_skop_pct:.0f} görüntü",
                             font="Courier New", font_size=13,
                             color=ACCENT)
        lost_std_lbl.next_to(comp_screens[1], UP, buff=0.15)
        lost_skop_lbl.next_to(comp_screens[2], UP, buff=0.15)

        self.play(
            FadeIn(lost_std), FadeIn(lost_skop),
            run_time=0.8,
        )
        self.play(
            Write(lost_std_lbl), Write(lost_skop_lbl),
            run_time=0.7,
        )
        self.wait(1.0)

        # ── Son not ───────────────────────────────────────────────────────
        note_bg = RoundedRectangle(
            corner_radius=0.28, width=13, height=0.82,
            fill_color="#000000", fill_opacity=0.82,
            stroke_color=GOLD, stroke_width=2,
        ).move_to(DOWN*3.5)
        note_txt = Text(
            "Nolan'ın IMAX sahnelerinde ekran büyür,"
            "izleyici bunu bilinçaltında hisseder.",
            font="Courier New", font_size=17, color=WHITE_,
        ).move_to(note_bg.get_center())

        self.play(FadeIn(note_bg), Write(note_txt), run_time=1.2)
        self.wait(2.5)