from manim import *

config.pixel_width  = 1080
config.pixel_height = 1920
config.frame_rate   = 60
config.background_color = "#08080C"


class CollatzErdos(Scene):

    def construct(self):

        BEYAZ = "#F0EDE8"
        GRI   = "#666666"

        # ── Layout ────────────────────────────────────────────────────
        # Ekran: ~4.5 birim genişlik, ~8 birim yükseklik (Shorts)
        # Görsel: üst %55 → y ∈ [1.2, 8.8] → merkez ~5.0
        # İsim + yıl: görselin hemen altı → y ∈ [0.2, 1.0]
        # Alıntı: alt %35 → y ∈ [-7, -1.5]

        # ── Fotoğraf ──────────────────────────────────────────────────
        foto = ImageMobject("erdos.png")
        foto.set_height(10.5)
        foto.move_to(UP * 6.5)
        foto.set_opacity(0)
        self.add(foto)

        # ── İsim + yıl (görselin ALTINDA) ────────────────────────────
        isim = Text("Paul Erdős", font="Courier New",
                    font_size=85, color=BEYAZ, weight=BOLD, stroke_width=5, stroke_color=GRI)
        isim.move_to(UP * 0.05)

        yil = Text("1913 – 1996", font="Courier New",
                   font_size=45, color=GRI)
        yil.next_to(isim, DOWN, buff=0.18)

        # ── Alıntı: daktiloyla karakter karakter ──────────────────────
        # Tek bir Text nesnesi olarak oluştur, Write animasyonu
        # ile soldan sağa karakter karakter yazar gibi gelir.
        # Üç satırı ayrı ayrı Write ederek daktilo etkisi verelim.

        FONT     = "Courier New"   # monospace = daktilo hissi
        FONT_SZ  = 58
        RENK     = "#D4C9B0"       # hafif sarımsı → eski kağıt tonu

        satir1 = Text('Matematik henüz',   font=FONT, font_size=FONT_SZ, color=RENK)
        satir2 = Text("böyle sorunlar için", font=FONT, font_size=FONT_SZ, color=RENK)
        satir3 = Text('hazır değil.',       font=FONT, font_size=FONT_SZ, color=RENK)

        aliinti = VGroup(satir1, satir2, satir3).arrange(DOWN, buff=0.35, center=True)
        aliinti.move_to(DOWN * 4.4)

        # ── 1. Fotoğraf yukarıdan aşağı süzülür ──────────────────────
        foto.move_to(UP * 6.5)   # başlangıç: daha yukarıda
        self.play(
            foto.animate.set_opacity(1).move_to(UP * 4.8),
            run_time=1.4,
            rate_func=rate_functions.ease_out_cubic,
        )
        self.wait(0.2)

        # ── 2. İsim ve yıl belirir ────────────────────────────────────
        self.play(FadeIn(isim, shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(yil),                  run_time=0.4)
        self.wait(0.6)

        # ── 3. Alıntı daktilo etkisiyle satır satır yazılır ──────────
        # Write animasyonu Courier New + monospace ile gerçek daktilo hissi verir
        self.play(Write(satir1, run_time=0.6, rate_func=linear))
        self.wait(0.15)
        self.play(Write(satir2, run_time=0.3, rate_func=linear))
        self.wait(0.15)
        self.play(Write(satir3, run_time=0.5, rate_func=linear))

        self.wait(3.2)

        # ── 4. Her şey birlikte yavaşça solar ─────────────────────────
        self.play(
            FadeOut(foto,   run_time=1.8),
            FadeOut(isim,   run_time=1.8),
            FadeOut(yil,    run_time=1.8),
            FadeOut(satir1, run_time=1.8),
            FadeOut(satir2, run_time=1.8),
            FadeOut(satir3, run_time=1.8),
        )