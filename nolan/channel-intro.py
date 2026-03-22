from manim import *
import numpy as np

BG      = "#0A0A0F"
RED_    = "#BF1F24"
DARK_   = "#231F20"
WHITE_  = "#F0F0F8"
WARM    = "#C8A96E"
GOLD    = "#D4AF37"
DIM     = "#2A2A3A"


# ══════════════════════════════════════════════════════════════════════════════
# BİLİMETRİ LOGO (SVG verisinden rebuild — Manim objeleri)
# viewBox: 270.06 × 297.33  →  normalize: 1 birim = 1/60
# Sol sütun: rect(0, 0, 86.67, 297.33, rx=10)
# Kırmızı bloklar:
#   (97.47, 0,      144.94, 55.55)
#   (97.47, 241.78, 144.94, 55.55)
#   (97.47, 120.89, 120.94, 55.55)
#   (184.89, 65.08,  85.17, 46.28)
#   (184.89, 185.97, 85.17, 46.28)
# ══════════════════════════════════════════════════════════════════════════════

def build_logo(scale=0.022) -> VGroup:
    """
    SVG koordinatlarını Manim'e çevirir.
    SVG'de y ekseni aşağı, Manim'de yukarı → y'yi çevir.
    Orijin: viewBox merkezine (135.03, 148.665) al.
    """
    VB_W, VB_H = 270.06, 297.33
    cx, cy = VB_W / 2, VB_H / 2

    def r(x, y, w, h, color, rx=10):
        """SVG rect → Manim RoundedRectangle, merkezlenmiş."""
        mx = (x + w/2 - cx) * scale
        my = -(y + h/2 - cy) * scale   # y eksenini çevir
        rect = RoundedRectangle(
            corner_radius=rx * scale,
            width=w * scale, height=h * scale,
            fill_color=color, fill_opacity=1,
            stroke_width=0,
        )
        rect.move_to([mx, my, 0])
        return rect

    col   = r(0,      0,      86.67,  297.33, DARK_)
    top   = r(97.47,  0,      144.94,  55.55, RED_)
    bot   = r(97.47,  241.78, 144.94,  55.55, RED_)
    mid   = r(97.47,  120.89, 120.94,  55.55, RED_)
    right_top = r(184.89, 65.08,  85.17,  46.28, RED_)
    right_bot = r(184.89, 185.97, 85.17,  46.28, RED_)

    return VGroup(col, top, bot, mid, right_top, right_bot)


class IntroScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 1 — FİLM ŞERİDİ EKRANI SOLDAN TARAR
        # ══════════════════════════════════════════════════════════════════

        # Yatay film şeridi — belirgin, gövdeli, sürekli akan
        PERF_COUNT = 32
        PERF_W, PERF_H = 0.18, 0.28
        PERF_STEP   = 0.58
        STRIP_BODY_H = 0.55
        STRIP_TOTAL_W = PERF_COUNT * PERF_STEP + 2.0   # ekstra padding

        def make_strip(y_pos, body_color="#1C1C2C", perf_color="#2A2A4A"):
            body = Rectangle(
                width=STRIP_TOTAL_W, height=STRIP_BODY_H,
                fill_color=body_color, fill_opacity=1,
                stroke_color="#3A3A5A", stroke_width=1.5,
            ).move_to([0, y_pos, 0])
            perfs = VGroup()
            for i in range(PERF_COUNT):
                x = -STRIP_TOTAL_W/2 + i * PERF_STEP + PERF_STEP
                hole = RoundedRectangle(
                    corner_radius=0.05, width=PERF_W, height=PERF_H,
                    fill_color=BG, fill_opacity=1,
                    stroke_color=perf_color, stroke_width=1.2,
                )
                hole.move_to([x, y_pos, 0])
                perfs.add(hole)
            return VGroup(body, perfs)

        top_strip = make_strip( 3.55)
        bot_strip = make_strip(-3.55)

        # Şeritler karşı yönlerden girer
        top_strip.shift(LEFT * 20)
        bot_strip.shift(RIGHT * 20)

        self.play(
            top_strip.animate.shift(RIGHT * 20),
            bot_strip.animate.shift(LEFT * 20),
            run_time=0.7, rate_func=rush_from,
        )

        # Şeritler sürekli akmaya devam eder — updater ile
        SCROLL_SPEED = 2.2   # birim/saniye
        WRAP_W       = STRIP_TOTAL_W

        def scroll_right(mob, dt):
            mob.shift(RIGHT * SCROLL_SPEED * dt)
            if mob.get_left()[0] > WRAP_W / 2:
                mob.shift(LEFT * WRAP_W)

        def scroll_left(mob, dt):
            mob.shift(LEFT * SCROLL_SPEED * dt)
            if mob.get_right()[0] < -WRAP_W / 2:
                mob.shift(RIGHT * WRAP_W)

        top_strip.add_updater(scroll_right)
        bot_strip.add_updater(scroll_left)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 2 — PROJEKTOR IŞIK HUZMESİ
        # ══════════════════════════════════════════════════════════════════

        # Sol üstten gelen projeksiyon konisi
        cone_tip   = np.array([-7.5, 4.5, 0])
        cone_end_t = np.array([ 7.5, 3.2, 0])
        cone_end_b = np.array([ 7.5,-3.2, 0])

        cone = Polygon(
            cone_tip, cone_end_t, cone_end_b,
            fill_color=WARM, fill_opacity=0,
            stroke_width=0,
        )
        self.add(cone)
        self.play(cone.animate.set_fill(opacity=0.04),
                  run_time=0.8, rate_func=smooth)

        # Projektor ışını — ince parlak merkez çizgisi
        beam = Line(cone_tip,
                    (np.array(cone_end_t) + np.array(cone_end_b)) / 2,
                    stroke_color=WARM, stroke_width=1.0,
                    stroke_opacity=0.25)
        self.add(beam)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 3 — LOGO PARÇA PARÇA AÇILIR
        # ══════════════════════════════════════════════════════════════════

        logo = build_logo(scale=0.010)
        logo.move_to(LEFT*2.8)

        col, top, bot, mid, rt, rb = logo

        # Önce koyu sütun yukarıdan iner
        col.shift(UP * 8)
        self.play(col.animate.shift(DOWN * 8),
                  run_time=0.6, rate_func=rush_from)

        # Kırmızı bloklar sırayla soldan fırlar
        for block, delay in [(top, 0.0), (bot, 0.08),
                              (mid, 0.16), (rt, 0.10), (rb, 0.10)]:
            block.shift(LEFT * 5)

        self.play(
            LaggedStart(
                top.animate.shift(RIGHT * 5),
                bot.animate.shift(RIGHT * 5),
                mid.animate.shift(RIGHT * 5),
                rt.animate.shift(RIGHT * 5),
                rb.animate.shift(RIGHT * 5),
                lag_ratio=0.12,
            ),
            run_time=0.9, rate_func=rush_from,
        )
        self.wait(0.2)

        # Logo hafif scale pulse
        self.play(logo.animate.scale(1.08), run_time=0.18)
        self.play(logo.animate.scale(1/1.08), run_time=0.18)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 4 — "BİLİMETRİ" YAZI SAĞDAN GELİR
        # ══════════════════════════════════════════════════════════════════

        channel_name = Text("Bilimetri",
                            font="Belanosima", weight=BOLD,
                            font_size=62, color=WHITE_)
        channel_name.move_to(RIGHT*1.5 + UP*0.35)
        channel_name.set_opacity(0)
        channel_name.shift(RIGHT * 1.5)

        tagline = Text("Herkes için bilim!",
                       font="Courier New", font_size=20, color=WHITE_)
        tagline.move_to(RIGHT*1.5 + DOWN*0.55)
        tagline.set_opacity(0)

        self.play(
            channel_name.animate.shift(LEFT * 1.5).set_opacity(1),
            run_time=0.7, rate_func=smooth,
        )
        self.play(tagline.animate.set_opacity(1), run_time=0.6)
        self.wait(0.5)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 5 — KIRMIZI VURGU ÇİZGİSİ + VİDEO BAŞLIĞI
        # ══════════════════════════════════════════════════════════════════

        # İnce kırmızı yatay çizgi "BİLİMETRİ" altında büyür
        red_line = Line(ORIGIN, ORIGIN,
                        stroke_color=RED_, stroke_width=3)
        red_line.move_to(RIGHT*1.5 + DOWN*0.08)

        self.play(
            red_line.animate.put_start_and_end_on(
                RIGHT*-0.8 + DOWN*0.08,
                RIGHT*3.8 + DOWN*0.08,
            ),
            run_time=0.5, rate_func=smooth,
        )

        # Video başlığı
        video_title = Text("En İyi Filmler Neden\nIMAX Kullanıyor?",
                           font="Courier New", font_size=22,
                           color=WARM, line_spacing=1.2)
        video_title.move_to(RIGHT*1.5 + DOWN*1.5)
        video_title.set_opacity(0)

        self.play(video_title.animate.set_opacity(1),
                  run_time=0.8, rate_func=smooth)
        self.wait(1.0)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 6 — KAPANIŞ: HER ŞEY MERKEZDE TOPLANIR, FADE OUT
        # ══════════════════════════════════════════════════════════════════

        all_visible = VGroup(
            logo, channel_name, tagline,
            red_line, video_title,
            top_strip, bot_strip,
            cone, beam,
        )

        # Logo + isim merkezde büyür, rest solar
        # Şerit updater'larını durdur
        top_strip.remove_updater(scroll_right)
        bot_strip.remove_updater(scroll_left)

        self.play(
            FadeOut(VGroup(tagline, video_title,
                           top_strip, bot_strip, cone, beam)),
            run_time=0.6,
        )
        self.play(
            logo.animate.scale(0.9).move_to(LEFT*2.8),
            channel_name.animate.scale(0.88).move_to(RIGHT*1.0 + UP*0.1),
            red_line.animate.set_opacity(0),
            run_time=0.5, rate_func=smooth,
        )
        self.wait(0.4)

        # Son beyaz flash
        flash = Rectangle(width=16, height=10,
                          fill_color=WHITE_, fill_opacity=0,
                          stroke_width=0)
        self.add(flash)
        self.play(flash.animate.set_fill(opacity=0.18), run_time=0.08)
        self.play(flash.animate.set_fill(opacity=0.0),  run_time=0.25)
        self.remove(flash)

        self.play(
            VGroup(logo, channel_name).animate.set_opacity(0),
            run_time=0.9, rate_func=smooth,
        )
        self.wait(0.1)