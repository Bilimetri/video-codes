from manim import *
import numpy as np

BG     = "#0A0A0F"
WARM   = "#C8A96E"
COLD   = "#4FC3F7"
GREEN  = "#4ADE80"
ACCENT = "#FF6B6B"
WHITE_ = "#F0F0F8"
DIM    = "#3A3A5A"
PURPLE = "#A78BFA"


def film_strip_small(n=5, color=WARM) -> VGroup:
    cw, ch = 0.45, 0.32
    sh = ch + 0.25
    sw = n * (cw + 0.06)
    body = Rectangle(width=sw, height=sh,
                     fill_color="#1A1208", fill_opacity=1,
                     stroke_color=color, stroke_width=1.5)
    frames = VGroup()
    perfs  = VGroup()
    for i in range(n):
        x = -sw/2 + (cw+0.06)*(i+0.5) + 0.03
        fr = Rectangle(width=cw, height=ch,
                       fill_color="#0A0A14", fill_opacity=1,
                       stroke_color=color, stroke_width=0.8)
        fr.move_to([x, 0, 0])
        frames.add(fr)
        for sign in [1, -1]:
            h = RoundedRectangle(corner_radius=0.02, width=0.08, height=0.10,
                                 fill_color="#0A0A0F", fill_opacity=1,
                                 stroke_width=0)
            h.move_to([x, sign*(sh/2 - 0.07), 0])
            perfs.add(h)
    return VGroup(body, frames, perfs)


def monitor_icon(w=1.6, h=1.1, screen_color="#0A1020") -> VGroup:
    frame  = RoundedRectangle(corner_radius=0.08, width=w, height=h,
                              fill_color="#1A1A2A", fill_opacity=1,
                              stroke_color="#4A4A6A", stroke_width=2)
    screen = Rectangle(width=w-0.18, height=h-0.22,
                       fill_color=screen_color, fill_opacity=1,
                       stroke_width=0)
    stand  = Rectangle(width=0.12, height=0.26,
                       fill_color="#2A2A3A", fill_opacity=1, stroke_width=0)
    stand.next_to(frame, DOWN, buff=0)
    base   = Rectangle(width=0.5, height=0.08,
                       fill_color="#2A2A3A", fill_opacity=1, stroke_width=0)
    base.next_to(stand, DOWN, buff=0)
    return VGroup(frame, screen, stand, base)


def node_box(label, sublabel, color, pos):
    box = RoundedRectangle(corner_radius=0.18, width=2.2, height=0.85,
                           fill_color="#0D0D1A", fill_opacity=1,
                           stroke_color=color, stroke_width=2.2)
    box.move_to(pos)
    t1 = Text(label,    font="Courier New", weight=BOLD,
              font_size=17, color=color).move_to(np.array(pos) + UP*0.18)
    t2 = Text(sublabel, font="Courier New",
              font_size=12, color=DIM).move_to(np.array(pos) + DOWN*0.18)
    return VGroup(box, t1, t2)


def scissors_icon() -> VGroup:
    blade1 = Line(ORIGIN, RIGHT*0.55 + UP*0.22,   stroke_color="#C8C8D8", stroke_width=3)
    blade2 = Line(ORIGIN, RIGHT*0.55 + DOWN*0.22, stroke_color="#C8C8D8", stroke_width=3)
    pivot  = Dot(ORIGIN, radius=0.07, color="#A8A8B8")
    h1 = CubicBezier(ORIGIN, LEFT*0.15+UP*0.10,   LEFT*0.30+UP*0.25,   LEFT*0.35+UP*0.18,  stroke_color="#A8A8B8", stroke_width=2.5)
    h2 = CubicBezier(ORIGIN, LEFT*0.15+DOWN*0.10, LEFT*0.30+DOWN*0.25, LEFT*0.35+DOWN*0.18,stroke_color="#A8A8B8", stroke_width=2.5)
    return VGroup(h1, h2, blade1, blade2, pivot)


class WorkflowScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 1 — WORKFLOW ŞEMASI
        # ══════════════════════════════════════════════════════════════════

        title = Text("IMAX Post-Prodüksiyon İş Akışı",
                     font="Courier New", weight=BOLD,
                     font_size=30, color=WARM).move_to(UP*3.3)
        self.play(Write(title), run_time=1.2)
        self.wait(0.4)

        Y = 0.6
        n_film = node_box("FİLM ŞERİDİ",   "IMAX 70mm negatif",   WARM,   [-5.5, Y, 0])
        n_lab  = node_box("LABORATUVAR",    "Yıkama & baskı",      COLD,   [-2.8, Y, 0])
        n_tele = node_box("TELECİNE",       "Film → Dijital",      GREEN,  [ 0.0, Y, 0])
        n_avid = node_box("AVID / NLE",     "Dijital kurgu",       PURPLE, [ 2.8, Y, 0])
        n_edl  = node_box("EDL",            "Kurgu Karar Listesi", ACCENT, [ 5.5, Y, 0])
        n_neg  = node_box("NEGATİF KESİCİ", "Fiziksel kesim",      WARM,   [ 0.0,-1.0, 0])

        a1 = Arrow(n_film.get_right(), n_lab.get_left(),  buff=0.1, stroke_color=WARM,   stroke_width=2)
        a2 = Arrow(n_lab.get_right(),  n_tele.get_left(), buff=0.1, stroke_color=COLD,   stroke_width=2)
        a3 = Arrow(n_tele.get_right(), n_avid.get_left(), buff=0.1, stroke_color=GREEN,  stroke_width=2)
        a4 = Arrow(n_avid.get_right(), n_edl.get_left(),  buff=0.1, stroke_color=PURPLE, stroke_width=2)
        a5 = Arrow(n_edl.get_bottom(), n_neg.get_right() + RIGHT*0.05, buff=0.1, stroke_color=ACCENT, stroke_width=2)
        a6 = CurvedArrow(n_neg.get_left(), n_film.get_bottom(),
                         angle=-TAU/5, stroke_color=WARM, stroke_width=1.8, tip_length=0.18)
        lbl6 = Text("Fiziksel bant\nbirleştirme", font="Courier New",
                    font_size=12, color=WARM).move_to([-4.0, -2.0, 0])

        all_scene1 = VGroup(title, n_film, n_lab, n_tele, n_avid, n_edl, n_neg,
                            a1, a2, a3, a4, a5, a6, lbl6)

        self.play(
            LaggedStart(
                FadeIn(n_film, scale=0.88), FadeIn(n_lab,  scale=0.88),
                FadeIn(n_tele, scale=0.88), FadeIn(n_avid, scale=0.88),
                FadeIn(n_edl,  scale=0.88), FadeIn(n_neg,  scale=0.88),
                lag_ratio=0.18,
            ), run_time=2.2,
        )
        self.play(
            LaggedStart(
                Create(a1), Create(a2), Create(a3),
                Create(a4), Create(a5), Create(a6), FadeIn(lbl6),
                lag_ratio=0.15,
            ), run_time=2.0,
        )
        self.wait(2.0)
        self.play(FadeOut(all_scene1), run_time=0.9)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 2 — TELECİNE DÖNÜŞÜMÜ
        # ══════════════════════════════════════════════════════════════════

        sec2_title = Text("Adım 1  —  Telecine Dönüşümü",
                          font="Courier New", weight=BOLD,
                          font_size=24, color=GREEN).move_to(UP*3.3)
        self.play(Write(sec2_title), run_time=1.0)

        strip = film_strip_small(n=6, color=WARM).move_to(LEFT*4.8)
        strip_lbl = Text("70mm Negatif", font="Courier New",
                         font_size=18, color=WARM).next_to(strip, DOWN, buff=0.2)

        tele_box = RoundedRectangle(corner_radius=0.2, width=1.9, height=0.75,
                                    fill_color="#0A1A0A", fill_opacity=1,
                                    stroke_color=GREEN, stroke_width=2).move_to(LEFT*1.5)
        tele_t = Text("TELECINE", font="Courier New", weight=BOLD,
                      font_size=17, color=GREEN).move_to(tele_box.get_center())

        mon = monitor_icon(w=1.6, h=1.1, screen_color="#050A14").move_to(RIGHT*1.8)
        code_lines = VGroup(*[
            Text(f"FRAME_{1000+i*137:05d}.dpx", font="Courier New",
                 font_size=9, color=GREEN)
            .move_to(mon[1].get_center() + UP*(0.22 - i*0.14))
            for i in range(4)
        ])
        res_lbl = Text("1080p / 4K  DPX", font="Courier New",
                       font_size=16, color=GREEN).next_to(mon, DOWN, buff=0.2)

        tc_box = RoundedRectangle(corner_radius=0.15, width=2.6, height=0.55,
                                  fill_color="#000000", fill_opacity=0.85,
                                  stroke_color=COLD, stroke_width=1.8).move_to(RIGHT*4.5)
        tc_txt = Text("01:23:45:12", font="Courier New", weight=BOLD,
                      font_size=22, color=COLD).move_to(tc_box.get_center())
        tc_lbl = Text("Timecode", font="Courier New",
                      font_size=13, color=DIM).next_to(tc_box, DOWN, buff=0.1)

        a_st = Arrow(strip.get_right(),    tele_box.get_left(), buff=0.12, stroke_color=GREEN, stroke_width=2)
        a_tm = Arrow(tele_box.get_right(), mon.get_left(),      buff=0.12, stroke_color=GREEN, stroke_width=2)
        a_tc = Arrow(mon.get_right(),      tc_box.get_left(),   buff=0.12, stroke_color=COLD,  stroke_width=2)

        all_scene2 = VGroup(sec2_title, strip, strip_lbl, tele_box, tele_t,
                            mon, code_lines, res_lbl, tc_box, tc_txt, tc_lbl,
                            a_st, a_tm, a_tc)

        self.play(FadeIn(strip), Write(strip_lbl), run_time=0.9)
        self.play(Create(a_st), FadeIn(tele_box), Write(tele_t), run_time=0.9)

        scan = Line(tele_box.get_left()+RIGHT*0.1, tele_box.get_right()+LEFT*0.1,
                    stroke_color=GREEN, stroke_width=1.5, stroke_opacity=0.7)
        scan.move_to(tele_box.get_top())
        self.play(scan.animate.move_to(tele_box.get_bottom()),
                  run_time=0.9, rate_func=linear)
        self.remove(scan)

        self.play(Create(a_tm), FadeIn(mon), run_time=0.8)
        self.play(
            LaggedStart(*[Write(cl) for cl in code_lines], lag_ratio=0.2),
            Write(res_lbl), run_time=1.1,
        )
        self.play(Create(a_tc), FadeIn(tc_box), Write(tc_txt), Write(tc_lbl),
                  run_time=0.9)
        for frame in ["01:23:45:13", "01:23:45:14", "01:23:45:15"]:
            self.play(
                Transform(tc_txt,
                          Text(frame, font="Courier New", weight=BOLD,
                               font_size=22, color=COLD)
                          .move_to(tc_box.get_center())),
                run_time=0.25,
            )
        self.wait(1.8)
        self.play(FadeOut(all_scene2), run_time=0.9)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 3 — AVID KURGU + EDL
        # ══════════════════════════════════════════════════════════════════

        sec3_title = Text("Adım 2  —  Dijital Kurgu & EDL",
                          font="Courier New", weight=BOLD,
                          font_size=24, color=PURPLE).move_to(UP*3.3)
        self.play(Write(sec3_title), run_time=1.0)

        avid_mon = monitor_icon(w=2.2, h=1.5, screen_color="#050510").move_to(LEFT*3.2)
        timeline = VGroup()
        for i, c in enumerate([WARM, GREEN, COLD, PURPLE]):
            bar = Rectangle(width=1.5+(i%2)*0.3, height=0.14,
                            fill_color=c, fill_opacity=0.85, stroke_width=0)
            bar.move_to(avid_mon[1].get_center() + UP*(0.44-i*0.26) + LEFT*0.1)
            timeline.add(bar)
        avid_lbl = Text("AVID  /  NLE Kurgu", font="Courier New",
                        font_size=18, color=PURPLE).next_to(avid_mon, DOWN, buff=0.2)

        edl_box = RoundedRectangle(corner_radius=0.15, width=3.0, height=1.5,
                                   fill_color="#1A0A00", fill_opacity=1,
                                   stroke_color=ACCENT, stroke_width=2).move_to(RIGHT*2.5)
        edl_content = VGroup(
            Text("EDL  —  Kurgu Karar Listesi",
                 font="Courier New", weight=BOLD, font_size=14, color=ACCENT),
            Text("001  01:00:00:00  01:00:04:12", font="Courier New", font_size=11, color=DIM),
            Text("002  01:00:04:12  01:00:09:03", font="Courier New", font_size=11, color=DIM),
            Text("003  01:00:09:03  01:00:14:22", font="Courier New", font_size=11, color=DIM),
        ).arrange(DOWN, buff=0.12).move_to(edl_box.get_center())

        a_ae = Arrow(avid_mon.get_right(), edl_box.get_left(),
                     buff=0.12, stroke_color=ACCENT, stroke_width=2)

        all_scene3 = VGroup(sec3_title, avid_mon, timeline, avid_lbl,
                            edl_box, edl_content, a_ae)

        self.play(FadeIn(avid_mon), run_time=0.9)
        self.play(
            LaggedStart(*[FadeIn(b) for b in timeline], lag_ratio=0.15),
            Write(avid_lbl), run_time=1.2,
        )
        self.play(Create(a_ae), FadeIn(edl_box), run_time=0.9)
        self.play(
            LaggedStart(*[Write(l) for l in edl_content], lag_ratio=0.3),
            run_time=1.4,
        )
        self.wait(1.8)
        self.play(FadeOut(all_scene3), run_time=0.9)

        # ══════════════════════════════════════════════════════════════════
        # BÖLÜM 4 — NEGATİF KESİCİ  (tam ekran, yavaş)
        # ══════════════════════════════════════════════════════════════════

        sec4_title = Text("Adım 3  —  Negatif Kesici",
                          font="Courier New", weight=BOLD,
                          font_size=24, color=WARM).move_to(UP*3.5)
        self.play(Write(sec4_title), run_time=1.0)

        # ── İki ayrı şerit soldan gelir ───────────────────────────────────
        strip_a = film_strip_small(n=5, color=WARM)
        strip_b = film_strip_small(n=5, color=COLD)
        strip_a.move_to(LEFT*4.2 + UP*1.1)
        strip_b.move_to(LEFT*4.2 + DOWN*0.3)

        lbl_a = Text("Sahne A  (70mm negatif)", font="Courier New",
                     font_size=15, color=WARM).next_to(strip_a, RIGHT, buff=0.3)
        lbl_b = Text("Sahne B  (70mm negatif)", font="Courier New",
                     font_size=15, color=COLD).next_to(strip_b, RIGHT, buff=0.3)

        self.play(
            FadeIn(strip_a, shift=RIGHT*0.5),
            FadeIn(strip_b, shift=RIGHT*0.5),
            run_time=1.1,
        )
        self.play(Write(lbl_a), Write(lbl_b), run_time=0.9)
        self.wait(0.8)

        # ── Makas belirir, keser ──────────────────────────────────────────
        sc = scissors_icon()
        sc.scale(1.5).move_to(RIGHT*2.2 + UP*0.4)
        self.play(FadeIn(sc, scale=0.7), run_time=0.7)
        self.wait(0.4)

        # Makas kesme hareketi
        self.play(sc.animate.rotate(-25*DEGREES), run_time=0.2)
        self.play(sc.animate.rotate( 25*DEGREES), run_time=0.2)
        self.wait(0.3)

        # ── Şeritler birleşme noktasına kayar ────────────────────────────
        self.play(
            strip_a.animate.move_to(LEFT*1.5 + UP*0.4),
            strip_b.animate.move_to(RIGHT*1.5 + UP*0.4),
            FadeOut(lbl_a), FadeOut(lbl_b),
            FadeOut(sc),
            run_time=1.4, rate_func=smooth,
        )

        # Birleşme noktası — beyaz bant çizgisi
        join = Line(UP*0.72, DOWN*0.12,
                    stroke_color=WHITE_, stroke_width=4)
        join.move_to(UP*0.4)

        flash = Rectangle(width=1.4, height=0.9,
                          fill_color=WHITE_, fill_opacity=0,
                          stroke_width=0).move_to(UP*0.4)
        self.add(flash)
        self.play(flash.animate.set_fill(opacity=0.45), run_time=0.07)
        self.play(flash.animate.set_fill(opacity=0.0),  run_time=0.20)
        self.remove(flash)
        self.play(Create(join), run_time=0.5)

        join_lbl = Text("mikro bant (splice)", font="Courier New",
                        font_size=13, color=WHITE_).next_to(join, UP, buff=0.18)
        self.play(FadeIn(join_lbl), run_time=0.6)
        self.wait(0.6)

        # ── Uzun birleşik şerit aşağıda belirir ──────────────────────────
        merged_strip = film_strip_small(n=12, color=WHITE_)
        merged_strip.move_to(DOWN*1.5)

        # Ortasında renk geçiş bandı (amber → beyaz → mavi)
        mid_mark = Rectangle(
            width=0.06, height=merged_strip.height,
            fill_color=WHITE_, fill_opacity=1, stroke_width=0,
        ).move_to(merged_strip.get_center())

        merged_lbl = Text("Birleşik Film Şeridi  —  Nihai Negatif",
                          font="Courier New", font_size=17, color=WHITE_)
        merged_lbl.next_to(merged_strip, DOWN, buff=0.22)

        self.play(
            FadeIn(merged_strip, scale=0.88),
            run_time=1.2,
        )
        self.play(
            FadeIn(mid_mark),
            Write(merged_lbl),
            run_time=0.9,
        )
        self.wait(0.6)

        # ── Son not ───────────────────────────────────────────────────────
        note_bg = RoundedRectangle(corner_radius=0.3, width=11.2, height=1.3,
                                   fill_color="#000000", fill_opacity=0.82,
                                   stroke_color=WARM, stroke_width=2)
        note_bg.move_to(DOWN*3.2)
        note_txt = Text(
            "İzlediğiniz her pürüzsüz geçiş aslında mikroskobik bantlarla\n"
            "fiziksel olarak birbirine yapıştırılmış film parçalarıdır.",
            font="Courier New", font_size=20, color=WHITE_, line_spacing=1.3,
        ).move_to(note_bg.get_center())

        self.play(FadeIn(note_bg), run_time=0.6)
        self.play(Write(note_txt), run_time=1.8)
        self.wait(2.8)