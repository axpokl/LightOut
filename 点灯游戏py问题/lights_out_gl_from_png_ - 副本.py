from manimlib import *
import numpy as np

LIGHT_BLUE = "#55aaff"
PINK = "#ff55aa"

BD_W = 2
BD_W_SEL = 8
HL_COLOR = RED


def make_grid(scene, w, h, lgt_sft=0.0, btn_sft=0.0, sz=1.0, t=0):
    lgt = [[False for _ in range(w)] for _ in range(h)]
    btn = [[False for _ in range(w)] for _ in range(h)]
    lgt_sel = [[False for _ in range(w)] for _ in range(h)]
    btn_sel = [[False for _ in range(w)] for _ in range(h)]

    start_x = -(w - 1) * sz / 2.0
    start_y = (h - 1) * sz / 2.0

    lgt_shift = np.array([lgt_sft, 0.0, 0.0])
    btn_shift = np.array([btn_sft, 0.0, 0.0])

    lgt_bd_base_grp = VGroup()
    btn_bd_base_grp = VGroup()
    lgt_bd_hl_grp = VGroup()
    btn_bd_hl_grp = VGroup()
    lgt_sp_grp = VGroup()
    btn_sp_grp = VGroup()

    lgt_sz = 0.85 * sz
    btn_sz = 0.7 * sz / 2.0

    lgt_bd_base = [[None] * w for _ in range(h)]
    btn_bd_base = [[None] * w for _ in range(h)]
    lgt_bd_hl = [[None] * w for _ in range(h)]
    btn_bd_hl = [[None] * w for _ in range(h)]
    lgt_sp = [[None] * w for _ in range(h)]
    btn_sp = [[None] * w for _ in range(h)]

    for j in range(h):
        for i in range(w):
            center = np.array([start_x + i * sz, start_y - j * sz, 0.0])

            lbd = Square(side_length=sz).set_fill(opacity=0).set_stroke(WHITE, BD_W, 0)
            lbd.move_to(center + lgt_shift)
            lgt_bd_base[j][i] = lbd
            lgt_bd_base_grp.add(lbd)

            bbd = Square(side_length=sz).set_fill(opacity=0).set_stroke(WHITE, BD_W, 0)
            bbd.move_to(center + btn_shift)
            btn_bd_base[j][i] = bbd
            btn_bd_base_grp.add(bbd)

            lbd_hl = lbd.copy().set_stroke(HL_COLOR, BD_W_SEL, 0).set_fill(opacity=0)
            lgt_bd_hl[j][i] = lbd_hl
            lgt_bd_hl_grp.add(lbd_hl)

            bbd_hl = bbd.copy().set_stroke(HL_COLOR, BD_W_SEL, 0).set_fill(opacity=0)
            btn_bd_hl[j][i] = bbd_hl
            btn_bd_hl_grp.add(bbd_hl)

            lsp = Square(side_length=lgt_sz).set_stroke(width=0, opacity=0).set_fill(LIGHT_BLUE, 1)
            lsp.move_to(center + lgt_shift)
            lgt_sp[j][i] = lsp
            lgt_sp_grp.add(lsp)

            bsp = Circle(radius=btn_sz).set_stroke(width=0, opacity=0).set_fill(PINK, 1)
            bsp.move_to(center + btn_shift)
            btn_sp[j][i] = bsp
            btn_sp_grp.add(bsp)

    for j in range(h):
        for i in range(w):
            if not lgt[j][i]:
                lgt_sp[j][i].set_opacity(0)
            if not btn[j][i]:
                btn_sp[j][i].set_opacity(0)

    render_btn_bd = not np.isclose(btn_sft, lgt_sft)

    if render_btn_bd:
        scene.add(lgt_bd_base_grp, btn_bd_base_grp, lgt_sp_grp, btn_sp_grp, btn_bd_hl_grp, lgt_bd_hl_grp)
        if t > 0:
            scene.play(
                lgt_bd_base_grp.animate.set_stroke(opacity=1),
                btn_bd_base_grp.animate.set_stroke(opacity=1),
                run_time=t
            )
        else:
            lgt_bd_base_grp.set_stroke(opacity=1)
            btn_bd_base_grp.set_stroke(opacity=1)
    else:
        scene.add(lgt_bd_base_grp, lgt_sp_grp, btn_sp_grp, lgt_bd_hl_grp)
        if t > 0:
            scene.play(lgt_bd_base_grp.animate.set_stroke(opacity=1), run_time=t)
        else:
            lgt_bd_base_grp.set_stroke(opacity=1)

    return {
        "lgt": lgt,
        "btn": btn,
        "lgt_sel": lgt_sel,
        "btn_sel": btn_sel,
        "lgt_bd_base": lgt_bd_base,
        "btn_bd_base": btn_bd_base,
        "lgt_bd_hl": lgt_bd_hl,
        "btn_bd_hl": btn_bd_hl,
        "lgt_sp": lgt_sp,
        "btn_sp": btn_sp,
        "groups": {
            "lgt_bd_base": lgt_bd_base_grp,
            "btn_bd_base": btn_bd_base_grp,
            "lgt_bd_hl": lgt_bd_hl_grp,
            "btn_bd_hl": btn_bd_hl_grp,
            "lgt_sp": lgt_sp_grp,
            "btn_sp": btn_sp_grp
        },
        "flags": {"render_btn_bd": render_btn_bd},
        "params": {"w": w, "h": h, "sz": sz, "lgt_sft": lgt_sft, "btn_sft": btn_sft}
    }


def toggle_lgt(G, i, j):
    G["lgt"][j][i] = not G["lgt"][j][i]
    m = G["lgt_sp"][j][i]
    m.set_stroke(width=0, opacity=0)
    m.set_opacity(1 if G["lgt"][j][i] else 0)


def toggle_btn(G, i, j):
    G["btn"][j][i] = not G["btn"][j][i]
    m = G["btn_sp"][j][i]
    m.set_stroke(width=0, opacity=0)
    m.set_opacity(1 if G["btn"][j][i] else 0)


def set_bd(G, kind, i, j, selected):
    if kind == "lgt":
        G["lgt_sel"][j][i] = selected
        G["lgt_bd_hl"][j][i].set_stroke(opacity=1 if selected else 0)
        return
    if not G["flags"]["render_btn_bd"]:
        return
    G["btn_sel"][j][i] = selected
    G["btn_bd_hl"][j][i].set_stroke(opacity=1 if selected else 0)


def toggle_lgt_bd(G, i, j):
    sel = not G["lgt_sel"][j][i]
    set_bd(G, "lgt", i, j, sel)


def toggle_btn_bd(G, i, j):
    sel = not G["btn_sel"][j][i]
    set_bd(G, "btn", i, j, sel)


def clear_all_bd(G):
    w = G["params"]["w"]
    h = G["params"]["h"]
    for j in range(h):
        for i in range(w):
            if G["lgt_sel"][j][i]:
                G["lgt_sel"][j][i] = False
                G["lgt_bd_hl"][j][i].set_opacity(0)
            if G["flags"]["render_btn_bd"] and G["btn_sel"][j][i]:
                G["btn_sel"][j][i] = False
                G["btn_bd_hl"][j][i].set_opacity(0)


def press(scene, G, i, j, wait=0.0, include_center=True):
    clear_all_bd(G)
    toggle_btn(G, i, j)
    set_bd(G, "btn", i, j, True)

    w = G["params"]["w"]
    h = G["params"]["h"]
    cells = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    if include_center:
        cells.insert(0, (i, j))

    for x, y in cells:
        if 0 <= x < w and 0 <= y < h:
            toggle_lgt(G, x, y)
            set_bd(G, "lgt", x, y, True)

    if wait > 0:
        scene.wait(wait)


def apply_matrix(scene, G, MAT, step_wait=0.0, clear_end=True):
    h = len(MAT)
    w = len(MAT[0]) if h > 0 else 0
    for j in range(h):
        for i in range(w):
            if MAT[j][i] == 1:
                press(scene, G, i, j, wait=step_wait)
    if clear_end:
        clear_all_bd(G)


MAT5 = [
    [1, 1, 0, 0, 0],
    [1, 1, 0, 1, 1],
    [0, 0, 1, 1, 1],
    [0, 1, 1, 1, 0],
    [0, 1, 1, 0, 1],
]

MAT7 = [
    [1, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 1, 1, 0, 1, 1, 0],
    [1, 0, 0, 1, 0, 0, 1],
    [0, 1, 1, 0, 1, 1, 0],
    [1, 1, 1, 0, 1, 1, 1],
    [1, 1, 0, 1, 0, 1, 1],
]

MAT11 = [
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0],
    [0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0],
]


class Demo(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        G5 = make_grid(self, w=5, h=5, lgt_sft=-4.5, btn_sft=-4.5, sz=0.6, t=0.2)
        G7 = make_grid(self, w=7, h=7, lgt_sft=0.0, btn_sft=0.0, sz=0.5, t=0.2)
        G11 = make_grid(self, w=11, h=11, lgt_sft=4.5, btn_sft=4.5, sz=0.35, t=0.2)

        t5 = Text("N=5", color=WHITE).next_to(G5["groups"]["lgt_bd_base"], UP, buff=0.3)
        t7 = Text("N=7", color=WHITE).next_to(G7["groups"]["lgt_bd_base"], UP, buff=0.3)
        t11 = Text("N=11", color=WHITE).next_to(G11["groups"]["lgt_bd_base"], UP, buff=0.3)

        self.play(FadeIn(t5), FadeIn(t7), FadeIn(t11), run_time=0.4)

        apply_matrix(self, G5, MAT5, step_wait=0.15)
        apply_matrix(self, G7, MAT7, step_wait=0.10)
        apply_matrix(self, G11, MAT11, step_wait=0.05)
