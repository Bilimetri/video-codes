from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60
config.background_color = "#08080C"

# 27 sayısının tam Collatz dizisi
DIZI = [27,82,41,124,62,31,94,47,142,71,214,107,322,161,484,242,121,364,182,91,
        274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,
        1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,
        638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,
        2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,
        650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,
        16,8,4,2,1]

ALTIN  = "#F5A623"
NANE   = "#3BE8A0"
BEYAZ  = "#F0EDE8"
GRI    = "#444444"
KIRMIZI = "#FF4C4C"


class CollatzGraph(Scene):
    def construct(self):

        # ── Grafik alanı boyutları ─────────────────────────────────────
        # Shorts ekranı: yaklaşık 14 birim yüksek, 8 birim geniş
        # Grafik kutusunu ortaya yerleştiriyoruz
        G_LEFT   = -3.6
        G_RIGHT  =  3.6
        G_BOTTOM = -4.2
        G_TOP    =  3.8

        g_w = G_RIGHT - G_LEFT    # 7.2
        g_h = G_TOP   - G_BOTTOM  # 8.0

        n_pts  = len(DIZI)        # 112 nokta (0..111)
        y_max  = max(DIZI)        # 9232
        zirve_idx = DIZI.index(y_max)  # 78

        def grafik_nokta(i, val):
            x = G_LEFT + (i / (n_pts - 1)) * g_w
            y = G_BOTTOM + (val / y_max) * g_h
            return np.array([x, y, 0])

        # ── 1. BAŞLIK ────────────────────────────────────────────────
        baslik = Text("27", font="Courier New", font_size=110,
                      color=ALTIN, weight=BOLD)
        baslik.move_to(UP * 7.8)

        self.play(FadeIn(baslik, shift=DOWN * 0.3), run_time=0.5)
        self.wait(0.3)

        # ── 2. EKSEN ─────────────────────────────────────────────────
        x_eksen = Line(
            start=[G_LEFT,  G_BOTTOM, 0],
            end=  [G_RIGHT, G_BOTTOM, 0],
            color=GRI, stroke_width=1.5,
        )
        y_eksen = Line(
            start=[G_LEFT, G_BOTTOM, 0],
            end=  [G_LEFT, G_TOP,    0],
            color=GRI, stroke_width=1.5,
        )

        # Y ekseni etiketleri
        def y_etiket(val, label_str):
            y = G_BOTTOM + (val / y_max) * g_h
            cizgi = Line(
                [G_LEFT - 0.15, y, 0],
                [G_LEFT + 0.15, y, 0],
                color=GRI, stroke_width=1,
            )
            etiket = Text(label_str, font="Courier New",
                          font_size=22, color=GRI)
            etiket.next_to(cizgi, LEFT, buff=0.12)
            return VGroup(cizgi, etiket)

        y_etiketler = VGroup(
            y_etiket(0,    "0"),
            y_etiket(2000, "2k"),
            y_etiket(4000, "4k"),
            y_etiket(6000, "6k"),
            y_etiket(8000, "8k"),
            y_etiket(9232, "9232"),
        )

        # X ekseni etiketleri
        def x_etiket(i, label_str):
            x = G_LEFT + (i / (n_pts - 1)) * g_w
            cizgi = Line(
                [x, G_BOTTOM - 0.12, 0],
                [x, G_BOTTOM + 0.12, 0],
                color=GRI, stroke_width=1,
            )
            etiket = Text(label_str, font="Courier New",
                          font_size=22, color=GRI)
            etiket.next_to(cizgi, DOWN, buff=0.12)
            return VGroup(cizgi, etiket)

        x_etiketler = VGroup(
            x_etiket(0,   "0"),
            x_etiket(27,  "27"),
            x_etiket(55,  "55"),
            x_etiket(83,  "83"),
            x_etiket(111, "111"),
        )

        eksen_grubu = VGroup(x_eksen, y_eksen, y_etiketler, x_etiketler)
        self.play(Create(x_eksen), Create(y_eksen), run_time=0.6)
        self.play(FadeIn(y_etiketler), FadeIn(x_etiketler), run_time=0.4)

        # ── 3. GRAFİĞİ ÇİZ (hızlı akış) ────────────────────────────
        # Tek renkli VMobject olarak tüm eğri
        noktalar = [grafik_nokta(i, v) for i, v in enumerate(DIZI)]

        egri = VMobject(stroke_color=ALTIN, stroke_width=2.5, stroke_opacity=0.9)
        egri.set_points_as_corners(noktalar)

        # Hareketli nokta (grafik boyunca ilerleyen)
        hareketli_nokta = Dot(radius=0.10, color=BEYAZ)
        hareketli_nokta.move_to(noktalar[0])

        # Anlık değer etiketi (nokta yanında)
        deger_etiketi = Text("27", font="Courier New",
                             font_size=30, color=BEYAZ)
        deger_etiketi.next_to(hareketli_nokta, RIGHT, buff=0.15)

        self.play(FadeIn(hareketli_nokta), FadeIn(deger_etiketi), run_time=0.3)

        # Eğriyi Create ile çiz, nokta güncelleme tracker ile
        # Tracker üzerinden nokta takibi
        alpha_tracker = ValueTracker(0)

        def nokta_guncelle(mob):
            a = alpha_tracker.get_value()
            idx = int(a * (n_pts - 1))
            idx = min(idx, n_pts - 1)
            mob.move_to(noktalar[idx])

        def etiket_guncelle(mob):
            a = alpha_tracker.get_value()
            idx = int(a * (n_pts - 1))
            idx = min(idx, n_pts - 1)
            val = DIZI[idx]
            mob.become(
                Text(str(val), font="Courier New",
                     font_size=30, color=BEYAZ)
                .next_to(hareketli_nokta, RIGHT, buff=0.15)
            )

        hareketli_nokta.add_updater(nokta_guncelle)
        deger_etiketi.add_updater(etiket_guncelle)

        self.play(
            Create(egri, rate_func=linear),
            alpha_tracker.animate.set_value(1),
            run_time=7.0,
        )

        hareketli_nokta.remove_updater(nokta_guncelle)
        deger_etiketi.remove_updater(etiket_guncelle)

        # ── 4. ZİRVE VURGUSU ─────────────────────────────────────────
        zirve_pos = grafik_nokta(zirve_idx, y_max)

        zirve_nokta = Dot(radius=0.18, color=KIRMIZI)
        zirve_nokta.move_to(zirve_pos)

        zirve_cizgi = DashedLine(
            start=[G_LEFT, zirve_pos[1], 0],
            end=zirve_pos,
            color=KIRMIZI, stroke_width=1.5, dash_length=0.12,
        )

        zirve_yazi = Text("9232", font="Courier New",
                          font_size=34, color=KIRMIZI, weight=BOLD)
        zirve_yazi.next_to(zirve_nokta, UP + RIGHT, buff=0.15)

        self.play(
            FadeIn(zirve_nokta, scale=0.3),
            Create(zirve_cizgi),
            run_time=0.6,
        )
        self.play(FadeIn(zirve_yazi, shift=UP * 0.2), run_time=0.4)
        self.wait(0.3)

        # ── 5. BİTİŞ NOKTASI (1'e iniş) ─────────────────────────────
        bitis_pos = grafik_nokta(n_pts - 1, 1)

        bitis_nokta = Dot(radius=0.18, color=NANE)
        bitis_nokta.move_to(bitis_pos)

        bitis_yazi = Text("1 !", font="Courier New",
                          font_size=44, color=NANE, weight=BOLD)
        bitis_yazi.next_to(bitis_nokta, UP + LEFT, buff=0.18)

        self.play(
            FadeIn(bitis_nokta, scale=0.3),
            run_time=0.5,
        )
        self.play(
            Write(bitis_yazi),
            run_time=0.6,
        )
        self.wait(0.5)

        # ── 6. ALT BİLGİ ─────────────────────────────────────────────
        bilgi = VGroup(
            Text("111 Adım", font="Courier New",
                 font_size=40, color=ALTIN, weight=BOLD),
            Text("4-2-1 Döngüsü!", font="Courier New",
                 font_size=32, color=GRI),
        ).arrange(DOWN, buff=0.2)
        bilgi.move_to(DOWN * 6.8)

        self.play(FadeIn(bilgi, shift=UP * 0.3), run_time=0.7)
        self.wait(1)

        # ── Kapanış ──────────────────────────────────────────────────
        self.play(
            FadeOut(VGroup(
                baslik, eksen_grubu, egri,
                hareketli_nokta, deger_etiketi,
                zirve_nokta, zirve_cizgi, zirve_yazi,
                bitis_nokta, bitis_yazi, bilgi,
            )),
            run_time=1.0,
        )