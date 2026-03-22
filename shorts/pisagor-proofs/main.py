"""
Pisagor Teoremi – İspat 2: 4 Üçgen Yerleştirme  |  YouTube Shorts
==================================================================
Bu dosya yalnızca 4 Üçgen ispatını kapsar; daha uzun ve daha ayrıntılı
animasyonlarla ~50-55 saniye sürer.

RENDER:
    manim -pqh ispat2_dort_ucgen.py DortUcgenIspat

Hızlı önizleme:
    manim -pql ispat2_dort_ucgen.py DortUcgenIspat
"""

from manim import *
import numpy as np

# ── YouTube Shorts: 1080 × 1920 ──────────────────────────────────────────────
config.pixel_width  = 1080
config.pixel_height = 1920
config.frame_rate   = 60
config.frame_width  = 9          # x ∈ [-4.5, 4.5]  |  y ≈ [-8, 8]

# ── Renk paleti ───────────────────────────────────────────────────────────────
ALTIN   = "#F1C40F"
MAVI    = "#3B82F6"
KIRMIZI = "#EF4444"
YESIL   = "#22C55E"
TURUNCU = "#F97316"
BG_DARK = "#0F172A"   # arka plan tonlama için (isteğe bağlı)


# ─────────────────────────────────────────────────────────────────────────────
# Yardımcı: kenar üzerine 'a' veya 'b' etiketi yerleştir
# ─────────────────────────────────────────────────────────────────────────────
def kenar_etiketi(tex: str, p1, p2, renk, buff=0.22, font_size=38):
    lbl = MathTex(tex, font_size=font_size, color=renk)
    mid = (p1 + p2) / 2
    normal = np.array([-(p2 - p1)[1], (p2 - p1)[0], 0])
    n = np.linalg.norm(normal)
    if n > 1e-9:
        normal = normal / n
    lbl.move_to(mid + normal * buff)
    return lbl


# ─────────────────────────────────────────────────────────────────────────────
class DortUcgenIspat(Scene):
    """4 Üçgen Yerleştirme İspatı – adım adım, ~50 s"""

    # ── boyutlar ─────────────────────────────────────────────────────────────
    A = 1.15    # kısa dik kenar
    B = 1.70    # uzun dik kenar

    def construct(self):
        self._giris()           # 0 – başlık
        self._bir_ucgen()       # 1 – tek üçgen tanıt
        self._buyuk_kare()      # 2 – (a+b)² karesi
        self._dort_ucgen()      # 3 – 4 üçgeni yerleştir
        self._ic_kare()         # 4 – iç c²-kare belirginleş
        self._alan_denklemi()   # 5 – cebirsel adımlar
        self._sonuc()           # 6 – kapanış

    # ══════════════════════════════════════════════════════════════════════════
    # 0 – GİRİŞ BAŞLIĞI
    # ══════════════════════════════════════════════════════════════════════════
    def _giris(self):
        ust = Text("Pisagor Teoremi", font_size=52, weight=BOLD, color=ALTIN)
        alt = Text("4 Üçgen Yerleştirme İspatı", font_size=38, color=WHITE)
        ust.move_to(UP * 7.0)
        alt.next_to(ust, DOWN, buff=0.3)

        self.play(Write(ust), run_time=0.9)
        self.play(FadeIn(alt, shift=UP * 0.15), run_time=0.7)
        self.wait(1.0)
        self.play(FadeOut(VGroup(ust, alt)), run_time=0.4)

    # ══════════════════════════════════════════════════════════════════════════
    # 1 – TEK ÜÇGEN
    # ══════════════════════════════════════════════════════════════════════════
    def _bir_ucgen(self):
        a, b = self.A, self.B

        # Dik açı sol-altta; yatay = a, dikey = b
        O  = np.array([-a/2, -b/2, 0])
        Ax = O + RIGHT * a
        By = O + UP    * b

        ucgen = Polygon(
            O, Ax, By,
            color=WHITE,
            fill_color=MAVI,
            fill_opacity=0.55,
            stroke_width=2.5,
        )
        ra = RightAngle(Line(Ax, O), Line(O, By), length=0.22, color=WHITE)

        # Etiketler
        lbl_a = kenar_etiketi("a", O, Ax, ALTIN,   buff=-0.28)   # aşağı
        lbl_b = kenar_etiketi("b", O, By, ALTIN,   buff=-0.28)   # sola
        lbl_c = kenar_etiketi("c", Ax, By, KIRMIZI, buff= 0.30)  # dışa

        aciklama = Text("Dik kenaklar: a ve b\nHipotenüs: c", font_size=34, color=WHITE, line_spacing=1.2)
        aciklama.move_to(DOWN * 3.8)

        self.play(Create(ucgen), Create(ra), run_time=0.9)
        self.play(Write(lbl_a), Write(lbl_b), Write(lbl_c), run_time=0.7)
        self.play(FadeIn(aciklama), run_time=0.6)
        self.wait(1.5)
        self.play(FadeOut(VGroup(ucgen, ra, lbl_a, lbl_b, lbl_c, aciklama)), run_time=0.5)

    # ══════════════════════════════════════════════════════════════════════════
    # 2 – BÜYÜK (a+b)² KARESİ
    # ══════════════════════════════════════════════════════════════════════════
    def _buyuk_kare(self):
        a, b  = self.A, self.B
        s     = a + b
        self._s = s                   # sonraki adımlara aktar
        merkez = UP * 0.5
        self._merkez = merkez

        h = s / 2
        BL = merkez + np.array([-h, -h, 0])
        BR = merkez + np.array([ h, -h, 0])
        TR = merkez + np.array([ h,  h, 0])
        TL = merkez + np.array([-h,  h, 0])
        self._BL, self._BR, self._TR, self._TL = BL, BR, TR, TL

        kare = Polygon(BL, BR, TR, TL,
                       color=WHITE, fill_color="#1E293B",
                       fill_opacity=0.6, stroke_width=3)
        self._buyuk_kare_mob = kare

        # Kenar etiketleri (her iki yan)
        lbl_top   = MathTex("a+b", font_size=38, color=WHITE).next_to(kare, UP,    buff=0.18)
        lbl_right = MathTex("a+b", font_size=38, color=WHITE).next_to(kare, RIGHT, buff=0.18)

        lbl_alan = MathTex(r"\text{Alan} = (a+b)^2", font_size=40, color=WHITE)
        lbl_alan.move_to(DOWN * 4.2)

        self.play(DrawBorderThenFill(kare), run_time=1.0)
        self.play(Write(lbl_top), Write(lbl_right), run_time=0.7)
        self.play(Write(lbl_alan), run_time=0.7)
        self.wait(1.2)
        self.play(FadeOut(VGroup(lbl_top, lbl_right, lbl_alan)), run_time=0.4)

    # ══════════════════════════════════════════════════════════════════════════
    # 3 – 4 ÜÇGEN'İ BİR BİR YERLEŞTİR
    # ══════════════════════════════════════════════════════════════════════════
    def _dort_ucgen(self):
        a, b  = self.A, self.B
        BL, BR, TR, TL = self._BL, self._BR, self._TR, self._TL

        # c²-karesinin köşeleri (iç döndürülmüş kare)
        # Her kenar üzerinde b kadar ilerleniyor (saat yönü sıralaması)
        P1 = BL + RIGHT * b        # alt kenar üzerinde
        P2 = BR + UP    * b        # sağ kenar üzerinde
        P3 = TR + LEFT  * b        # üst kenar üzerinde
        P4 = TL + DOWN  * b        # sol kenar üzerinde
        self._P1, self._P2, self._P3, self._P4 = P1, P2, P3, P4

        renkler = [MAVI, KIRMIZI, YESIL, TURUNCU]
        koseler = [
            [BL, P1, P4],   # sol-alt üçgen  (BL köşesinde)
            [BR, P2, P1],   # sağ-alt üçgen  (BR köşesinde)
            [TR, P3, P2],   # sağ-üst üçgen  (TR köşesinde)
            [TL, P4, P3],   # sol-üst üçgen  (TL köşesinde)
        ]
        # Kenar etiket pozisyonları: her üçgen için (a kenarı, b kenarı)
        etiket_verileri = [
            # (a_pairli köşeler, b_pairli köşeler, normalin yönü)
            (BL, P1,  P1, P4),
            (BR, P2,  P2, P1),
            (TR, P3,  P3, P2),
            (TL, P4,  P4, P3),
        ]

        # Sırayla üçgenleri çiz + kısa açıklama
        aciklamalar = [
            "1. üçgen yerleşti",
            "2. üçgen yerleşti",
            "3. üçgen yerleşti",
            "4. üçgen yerleşti",
        ]

        self._ucgenler = VGroup()
        self._ra_grp   = VGroup()
        lbl_grp        = VGroup()

        bilgi = Text("", font_size=36, color=WHITE).move_to(DOWN * 4.2)
        self.add(bilgi)

        for i, (pts, renk, acik) in enumerate(zip(koseler, renkler, aciklamalar)):
            ucg = Polygon(
                *pts,
                color=WHITE, fill_color=renk,
                fill_opacity=0.75, stroke_width=2,
            )

            # Dik açı işareti
            p0, p1, p2 = [np.array(p) for p in pts]
            v1 = p1 - p0; v2 = p2 - p0
            ra = RightAngle(
                Line(p0 + v1 * 0.001, p0),
                Line(p0, p0 + v2 * 0.001),
                length=0.18, color=WHITE,
            )

            # a ve b etiketleri
            a_p1, a_p2, b_p1, b_p2 = etiket_verileri[i]
            lbl_a_i = kenar_etiketi("a", np.array(a_p1), np.array(a_p2), ALTIN,   font_size=32)
            lbl_b_i = kenar_etiketi("b", np.array(b_p1), np.array(b_p2), WHITE, font_size=32)

            # Yeni açıklama metni
            yeni_bilgi = Text(acik, font_size=36, color=renk).move_to(DOWN * 4.2)

            self.play(
                FadeIn(ucg, scale=0.85),
                Create(ra),
                ReplacementTransform(bilgi, yeni_bilgi),
                run_time=0.75,
            )
            self.play(FadeIn(lbl_a_i), FadeIn(lbl_b_i), run_time=0.4)
            bilgi = yeni_bilgi

            self._ucgenler.add(ucg)
            self._ra_grp.add(ra)
            lbl_grp.add(lbl_a_i, lbl_b_i)

        self.wait(0.8)
        self.play(FadeOut(VGroup(bilgi, lbl_grp)), run_time=0.4)

    # ══════════════════════════════════════════════════════════════════════════
    # 4 – İÇ c²-KARESİNİ BELİRGİNLEŞTİR
    # ══════════════════════════════════════════════════════════════════════════
    def _ic_kare(self):
        P1, P2, P3, P4 = self._P1, self._P2, self._P3, self._P4

        ic_kare = Polygon(
            P1, P2, P3, P4,
            color=ALTIN, fill_color=ALTIN,
            fill_opacity=0.40, stroke_width=3,
        )
        self._ic_kare_mob = ic_kare

        # Yanıp sönen vurgu
        self.play(Create(ic_kare), run_time=0.8)
        self.play(
            ic_kare.animate.set_fill(ALTIN, opacity=0.7),
            rate_func=there_and_back, run_time=0.7,
        )

        # c² etiketi
        lbl_c2 = MathTex("c^2", font_size=54, color=ALTIN)
        lbl_c2.move_to((P1 + P2 + P3 + P4) / 4)
        self._lbl_c2 = lbl_c2

        # Kenar = c açıklaması
        c_acik = MathTex(r"\text{(kenar} = c\text{)}", font_size=34, color=ALTIN)
        c_acik.next_to(lbl_c2, DOWN, buff=0.18)

        self.play(Write(lbl_c2), FadeIn(c_acik), run_time=0.7)
        self.wait(1.0)
        self.play(FadeOut(c_acik), run_time=0.3)

    # ══════════════════════════════════════════════════════════════════════════
    # 5 – CEBİRSEL ADIMLAR
    # ══════════════════════════════════════════════════════════════════════════
    def _alan_denklemi(self):
        # Tüm görsel öğeleri küçült ve yukarı taşı
        gorsel_grup = VGroup(
            self._buyuk_kare_mob,
            self._ucgenler,
            self._ra_grp,
            self._ic_kare_mob,
            self._lbl_c2,
        )
        self.play(
            gorsel_grup.animate.scale(0.68).move_to(UP * 4.8),
            run_time=0.9,
        )

        # ── Satır satır denklem ──────────────────────────────────────────────
        satirlar = [
            # (latex, renk, açıklama metni)
            (
                r"(a+b)^2 = 4 \times \frac{1}{2}ab + c^2",
                WHITE,
                "Büyük kare = 4 üçgen + iç kare",
            ),
            (
                r"a^2 + 2ab + b^2 = 2ab + c^2",
                WHITE,
                "Sol tarafı açalım",
            ),
            (
                r"a^2 + b^2 = c^2 \quad \checkmark",
                ALTIN,
                "2ab'yi her iki taraftan çıkar!",
            ),
        ]

        onceki = None
        acik_mob = None
        y_baslangic = UP * 1.8

        for i, (latex, renk, acik) in enumerate(satirlar):
            eq = MathTex(latex, font_size=42, color=renk)
            eq.move_to(y_baslangic + DOWN * i * 1.65)

            # Oklu geçiş oku (2. satırdan itibaren)
            if onceki is not None:
                ok = Arrow(
                    onceki.get_bottom() + DOWN * 0.05,
                    eq.get_top()        + UP   * 0.05,
                    buff=0.10, color=GRAY, stroke_width=2.5,
                    max_tip_length_to_length_ratio=0.18,
                )
                self.play(Create(ok), run_time=0.3)

            # Açıklama balonu (brace)
            acik_yeni = Text(acik, font_size=30, color=GRAY)
            acik_yeni.next_to(eq, RIGHT, buff=0.3)

            self.play(Write(eq), run_time=0.9)
            self.play(FadeIn(acik_yeni, shift=LEFT * 0.1), run_time=0.5)

            if acik_mob:
                self.play(FadeOut(acik_mob), run_time=0.2)
            acik_mob = acik_yeni
            onceki   = eq

            self.wait(0.7 if i < 2 else 1.2)

        # Son sonuç kutusu
        if onceki is not None:
            kutu = SurroundingRectangle(onceki, color=ALTIN, buff=0.18, stroke_width=2.5)
            self.play(Create(kutu), run_time=0.6)
        self.wait(1.5)

    # ══════════════════════════════════════════════════════════════════════════
    # 6 – OUTRO
    # ══════════════════════════════════════════════════════════════════════════
    def _sonuc(self):
        self.play(FadeOut(*self.mobjects), run_time=0.6)

        formul = MathTex(r"a^2 + b^2 = c^2", font_size=90, color=ALTIN)
        formul.move_to(UP * 2.0)

        alt1 = Text("İspat tamamlandı!", font_size=48, color=WHITE)
        alt1.move_to(UP * 0.3)

        alt2 = Text("4 eş dik üçgen +\nbir döndürülmüş kare.", font_size=38,
                    color=GRAY, line_spacing=1.25)
        alt2.move_to(DOWN * 1.4)

        self.play(Write(formul), run_time=1.0)
        self.play(FadeIn(alt1, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(alt2), run_time=0.6)
        self.wait(2.5)