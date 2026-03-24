from manim import *

# Shorts için dikey format ayarları
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60
config.background_color = "#08080C" # Çok koyu, gizemli bir arka plan

class IntroShorts(Scene):
    def construct(self):
        # ── Metin Hazırlığı ──
        line1 = Text("Matematiğin", font_size=42, weight=BOLD, color=GRAY_B)
        line2 = Text("En Basit Görünümlü", font_size=36, weight=MEDIUM, color=GRAY_C)
        line3 = Text("İmkansız Problemi", font_size=60, weight=HEAVY, color=YELLOW)

        # Satırları dikey olarak sırala ve aralarına boşluk koy
        title_group = VGroup(line1, line2, line3).arrange(DOWN, buff=0.35)
        # Ekranın ortasının biraz üstüne yerleştir (dikey denge için)
        title_group.move_to(UP * 0.5)

        # ── Animasyonlar ──

        # 1. İlk satır hafifçe yukarıdan inerek belirir
        self.play(
            FadeIn(line1, shift=UP*0.3),
            run_time=0.5,
            rate_func=rate_functions.ease_out_cubic # BURASI DÜZELTİLDİ
        )

        # 2. İkinci satır belirir (biraz daha hızlı)
        self.play(
            FadeIn(line2),
            run_time=0.4,
            rate_func=rate_functions.ease_out_cubic # BURASI DÜZELTİLDİ
        )

        # 3. VURGU ANI: "İmkansız Problemi" merkezden büyüyerek ve parlayarak gelir
        flash = Flash(line3, color=YELLOW, line_length=0.2, num_lines=12, flash_radius=1.5, run_time=0.6)

        self.play(
            GrowFromCenter(line3), 
            line3.animate.set_color(GOLD_B), 
            flash, 
            run_time=0.7,
            rate_func=rate_functions.ease_out_back # BURASI DÜZELTİLDİ
        )

        # ── Bekleme ve Çıkış ──
        self.wait(0.7)

        # Hızlıca yukarı doğru kaybolarak çıkış yap
        self.play(
            title_group.animate.shift(UP * 15).set_opacity(0),
            run_time=1.6,
            rate_func=rate_functions.ease_in_expo # BURASI DÜZELTİLDİ
        )