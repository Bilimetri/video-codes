from manim import *

# YouTube Shorts: 1080x1920, 60fps
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60
config.background_color = "#0D0D0D"


class CollatzRule(Scene):
    def construct(self):

        # ── Renkler ──────────────────────────────────────────────────
        ALTIN   = "#F5A623"   # tek sayı
        NANE    = "#3BE8A0"   # çift sayı
        GECE    = "#0D0D0D"   # arka plan
        BEYAZ   = "#F0EDE8"   # birincil metin
        GRI     = "#555555"   # pasif metin / çizgi
        KOYU_S  = "#1A1200"   # altın zemin
        KOYU_N  = "#001A0D"   # nane zemin

        # ── Yardımcı: yuvarlak köşeli dikdörtgen ──────────────────────
        def kart(renk, ic_renk, genislik=7.2, yukseklik=1.6, radius=0.35):
            kutu = RoundedRectangle(
                corner_radius=radius,
                width=genislik, height=yukseklik,
                stroke_color=renk, stroke_width=3,
                fill_color=ic_renk, fill_opacity=1,
            )
            return kutu

        # ══════════════════════════════════════════════════════════════
        # SAHNE 1 — TEK SAYI (3n + 1)
        # ══════════════════════════════════════════════════════════════

        # --- başlık etiketi ---
        etiket_tek = Text("TEK SAYI", font="Courier New", font_size=36,
                          color=ALTIN, weight=BOLD)
        etiket_tek.move_to(UP * 5.8)

        # --- büyük sayı: 7 ---
        sayi_7 = Text("7", font="Courier New", font_size=260,
                      color=ALTIN, weight=BOLD)
        sayi_7.move_to(UP * 3.2)

        # --- kural kartı ---
        kart_tek = kart(ALTIN, KOYU_S)
        kart_tek.move_to(UP * 0.6)

        kural_tek = MathTex(r"3n + 1", font_size=96, color=ALTIN)
        kural_tek.move_to(kart_tek.get_center())

        # --- ok ---
        ok_tek = Arrow(
            start=UP * -0.5, end=UP * -1.9,
            color=ALTIN, stroke_width=8,
            max_tip_length_to_length_ratio=0.18,
        )

        # --- "= 22" sonuç ---
        sonuc_tek = Text("= 22", font="Courier New", font_size=130,
                         color=BEYAZ, weight=BOLD)
        sonuc_tek.move_to(UP * -3.1)

        # ── Giriş animasyonu ──
        self.play(FadeIn(etiket_tek, shift=DOWN * 0.3), run_time=0.6)
        self.play(Write(sayi_7), run_time=0.9)
        self.wait(0.4)

        self.play(
            DrawBorderThenFill(kart_tek),
            Write(kural_tek),
            run_time=0.9,
        )
        self.wait(0.3)

        self.play(GrowArrow(ok_tek), run_time=0.5)
        self.play(
            FadeIn(sonuc_tek, shift=DOWN * 0.4, scale=0.7),
            run_time=0.7,
        )
        self.wait(0.8)

        # ── Sahne temizle ──
        grup_tek = VGroup(
            etiket_tek, sayi_7, kart_tek, kural_tek,
            ok_tek, sonuc_tek,
        )
        self.play(FadeOut(grup_tek, shift=LEFT * 1.5), run_time=0.7)

        # ══════════════════════════════════════════════════════════════
        # SAHNE 2 — ÇİFT SAYI (n / 2)
        # ══════════════════════════════════════════════════════════════

        # --- başlık ---
        etiket_cift = Text("ÇİFT SAYI", font="Courier New", font_size=36,
                           color=NANE, weight=BOLD)
        etiket_cift.move_to(UP * 5.8)

        # --- büyük sayı: 22 ---
        sayi_22 = Text("22", font="Courier New", font_size=220,
                       color=NANE, weight=BOLD)
        sayi_22.move_to(UP * 3.2)

        # --- kural kartı ---
        kart_cift = kart(NANE, KOYU_N)
        kart_cift.move_to(UP * 0.6)

        kural_cift = MathTex(r"n \div 2", font_size=96, color=NANE)
        kural_cift.move_to(kart_cift.get_center())

        # --- ok ---
        ok_cift = Arrow(
            start=UP * -0.5, end=UP * -1.9,
            color=NANE, stroke_width=8,
            max_tip_length_to_length_ratio=0.18,
        )

        # --- "= 11" sonuç ---
        sonuc_cift = Text("= 11", font="Courier New", font_size=130,
                          color=BEYAZ, weight=BOLD)
        sonuc_cift.move_to(UP * -3.1)

        # ── Giriş animasyonu ──
        self.play(FadeIn(etiket_cift, shift=DOWN * 0.3), run_time=0.6)
        self.play(Write(sayi_22), run_time=0.9)
        self.wait(0.4)

        self.play(
            DrawBorderThenFill(kart_cift),
            Write(kural_cift),
            run_time=0.6,
        )
        self.wait(0.3)

        self.play(GrowArrow(ok_cift), run_time=0.5)
        self.play(
            FadeIn(sonuc_cift, shift=DOWN * 0.4, scale=0.7),
            run_time=0.7,
        )
        self.wait(0.8)

        # ── Kapanış ──
        grup_cift = VGroup(
            etiket_cift, sayi_22, kart_cift, kural_cift,
            ok_cift, sonuc_cift,
        )
        self.play(FadeOut(grup_cift, shift=LEFT * 1.5), run_time=0.8)

        # ══════════════════════════════════════════════════════════════
        # SAHNE 3 — İKİ KURAL YAN YANA (özet)
        # ══════════════════════════════════════════════════════════════

        # Sol: TEK
        sol_kart = kart(ALTIN, KOYU_S, genislik=4.6, yukseklik=3.8)
        sol_kart.move_to(LEFT * 2.55)

        sol_baslik = Text("TEK", font="Courier New", font_size=44,
                          color=ALTIN, weight=BOLD)
        sol_baslik.next_to(sol_kart.get_top(), DOWN, buff=0.35)

        sol_formul = MathTex(r"3n+1", font_size=88, color=ALTIN)
        sol_formul.move_to(sol_kart.get_center())

        sol_ornek = Text("7 → 22", font="Courier New", font_size=36, color=GRI)
        sol_ornek.next_to(sol_kart.get_bottom(), UP, buff=0.35)

        # Sağ: ÇİFT
        sag_kart = kart(NANE, KOYU_N, genislik=4.6, yukseklik=3.8)
        sag_kart.move_to(RIGHT * 2.55)

        sag_baslik = Text("ÇİFT", font="Courier New", font_size=44,
                          color=NANE, weight=BOLD)
        sag_baslik.next_to(sag_kart.get_top(), DOWN, buff=0.35)

        sag_formul = MathTex(r"n \div 2", font_size=88, color=NANE)
        sag_formul.move_to(sag_kart.get_center())

        sag_ornek = Text("22 → 11", font="Courier New", font_size=36, color=GRI)
        sag_ornek.next_to(sag_kart.get_bottom(), UP, buff=0.35)

        # Üst başlık
        ust_baslik = Text("Collatz Sanısı", font="Courier New",
                          font_size=54, color=BEYAZ, weight=BOLD)
        ust_baslik.move_to(UP * 5.5)

        alt_yazi = Text("Basit Görünümlü İmkansız Problem", font="Courier New",
                        font_size=38, color=GRI)
        alt_yazi.move_to(UP * 4.6)

        soru = Text("?", font="Courier New", font_size=200,
                    color=BEYAZ, weight=BOLD)
        soru.move_to(DOWN * 4.0)

        # Animasyon
        self.play(
            FadeIn(ust_baslik, shift=DOWN * 0.3),
            FadeIn(alt_yazi, shift=DOWN * 0.2),
            run_time=0.8,
        )
        self.play(
            DrawBorderThenFill(sol_kart),
            DrawBorderThenFill(sag_kart),
            run_time=0.8,
        )
        self.play(
            FadeIn(sol_baslik), FadeIn(sag_baslik),
            run_time=0.4,
        )
        self.play(
            Write(sol_formul), Write(sag_formul),
            run_time=0.9,
        )
        self.play(
            FadeIn(sol_ornek), FadeIn(sag_ornek),
            run_time=0.5,
        )
        self.wait(0.5)
        self.play(Write(soru), run_time=0.7)
        self.wait(0.5)

        # Son fade
        self.play(
            FadeOut(VGroup(
                ust_baslik, alt_yazi,
                sol_kart, sol_baslik, sol_formul, sol_ornek,
                sag_kart, sag_baslik, sag_formul, sag_ornek,
                soru,
            )),
            run_time=1.0,
        )