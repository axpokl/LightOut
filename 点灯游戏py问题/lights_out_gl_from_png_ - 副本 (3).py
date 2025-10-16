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

def _queue_opacity_anim(mobj, target, anims):
    cur = mobj.get_opacity()
    if abs(cur - target) > 1e-6:
        anims.append(ApplyMethod(mobj.set_opacity, float(target)))

def press(scene, G, i, j, wait=0.0, anim=0.3, include_center=True):
    clear_all_bd(G)
    anims = []
    G["btn"][j][i] = not G["btn"][j][i]
    set_bd(G, "btn", i, j, True)
    _queue_opacity_anim(G["btn_sp"][j][i], 1.0 if G["btn"][j][i] else 0.0, anims)
    w = G["params"]["w"]
    h = G["params"]["h"]
    cells = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    if include_center:
        cells.insert(0, (i, j))
    for x, y in cells:
        if 0 <= x < w and 0 <= y < h:
            G["lgt"][y][x] = not G["lgt"][y][x]
            set_bd(G, "lgt", x, y, True)
            _queue_opacity_anim(G["lgt_sp"][y][x], 1.0 if G["lgt"][y][x] else 0.0, anims)
    if anims:
        scene.play(*anims, run_time=anim)
    if wait > 0:
        scene.wait(wait)

def apply_matrix(scene, G, MAT, step_anim=0.0, clear_end=True):
    h = len(MAT)
    w = len(MAT[0]) if h > 0 else 0
    for j in range(h):
        for i in range(w):
            if MAT[j][i] == 1:
                press(scene, G, i, j, wait=0, anim=step_anim)
    if clear_end:
        clear_all_bd(G)

def destroy_grids(scene, grids, rt=0.3, keep_borders=False, reset_state=True):
    if keep_borders:
        # 保留边框：内容与高亮做“透明度动画到 0”，不要从场景 remove
        anims = []
        for G in grids:
            h = G["params"]["h"]
            w = G["params"]["w"]
            # 高亮透明
            for j in range(h):
                for i in range(w):
                    G["lgt_bd_hl"][j][i].set_stroke(opacity=0)
                    if G["flags"]["render_btn_bd"]:
                        G["btn_bd_hl"][j][i].set_stroke(opacity=0)
            # 内容淡出
            anims.append(ApplyMethod(G["groups"]["lgt_sp"].set_opacity, 0.0))
            anims.append(ApplyMethod(G["groups"]["btn_sp"].set_opacity, 0.0))
        scene.play(*anims, run_time=rt)

        if reset_state:
            for G in grids:
                h = G["params"]["h"]; w = G["params"]["w"]
                for j in range(h):
                    for i in range(w):
                        G["lgt"][j][i] = False
                        G["btn"][j][i] = False
                        G["lgt_sel"][j][i] = False
                        G["btn_sel"][j][i] = False
                # 保留边框可见性（不动 lgt_bd_base / btn_bd_base）

    else:
        # 整组移除（与原逻辑一致）：可见物体先淡出再 remove
        targets = []
        for G in grids:
            grps = G["groups"]
            targets += [grps["lgt_sp"], grps["btn_sp"], grps["lgt_bd_hl"], grps["lgt_bd_base"]]
            if G["flags"]["render_btn_bd"]:
                targets += [grps["btn_bd_hl"], grps["btn_bd_base"]]
        anims = [FadeOut(t, run_time=rt) for t in targets]
        if anims:
            scene.play(*anims)
        try:
            scene.remove(*targets)
        except Exception:
            pass

        if reset_state:
            for G in grids:
                h = G["params"]["h"]; w = G["params"]["w"]
                for j in range(h):
                    for i in range(w):
                        G["lgt"][j][i] = False
                        G["btn"][j][i] = False
                        G["lgt_sel"][j][i] = False
                        G["btn_sel"][j][i] = False
                # 基础边框设为透明，等下次 add/淡入
                G["groups"]["lgt_bd_base"].set_stroke(opacity=0)
                if G["flags"]["render_btn_bd"]:
                    G["groups"]["btn_bd_base"].set_stroke(opacity=0)

def destroy_labels(scene, *labels, rt=0.3):
    grp = VGroup(*labels)
    scene.play(FadeOut(grp, run_time=rt))
    try:
        scene.remove(grp)
    except Exception:
        pass

def brighten_all_lights(scene, G, rt=0.3, clear_highlight=True):
    if clear_highlight:
        clear_all_bd(G)
    h = G["params"]["h"]
    w = G["params"]["w"]
    anims = []
    for j in range(h):
        for i in range(w):
            if not G["lgt"][j][i]:
                G["lgt"][j][i] = True
                _queue_opacity_anim(G["lgt_sp"][j][i], 1.0, anims)
    if anims:
        scene.play(*anims, run_time=rt)

def show_subtitle(scene, text, text2=None, run_in=0.3, run_out=0.2, font="SimHei", font_size=32, line_gap=0.2, buff=0.5):
    old = getattr(scene, "_subtitle_mobj", None)
    if old is not None:
        scene.play(FadeOut(old, run_time=run_out))
        try: scene.remove(old)
        except Exception: pass
        scene._subtitle_mobj = None
    parts = []
    if isinstance(text, (list, tuple)):
        parts = [str(x) for x in text]
    else:
        if text is not None: parts.append(str(text))
        if text2 is not None: parts.append(str(text2))
    parts = [p for p in parts if p is not None]
    if len(parts) == 0 or all(p == "" for p in parts):
        return None
    lines = VGroup(*[Text(p, color=WHITE, font=font).scale(font_size/38) for p in parts])
    lines.arrange(DOWN, buff=line_gap).to_edge(DOWN, buff=buff)
    scene.add(lines)
    scene.play(FadeIn(lines, run_time=run_in))
    scene._subtitle_mobj = lines
    return lines

def show_title(scene, line1=None, line2=None, run_in=0.3, run_out=0.2, font="SimHei", size1=48, size2=32, line_gap=0.15, buff=0.5):
    old = getattr(scene, "_title_mobj", None)
    if old is not None:
        scene.play(FadeOut(old, run_time=run_out))
        try: scene.remove(old)
        except Exception: pass
        scene._title_mobj = None
    parts = []
    if isinstance(line1, (list, tuple)):
        parts = [str(x) for x in line1][:2]
    else:
        if line1 is not None: parts.append(str(line1))
        if line2 is not None: parts.append(str(line2))
    parts = [p for p in parts if p is not None]
    if len(parts)==0 or all(p == "" for p in parts):
        return None
    objs = []
    if len(parts)>=1 and parts[0]!="":
        t1 = Text(parts[0], color=WHITE, font=font).scale(size1/38)
        objs.append(t1)
    if len(parts)>=2 and parts[1]!="":
        t2 = Text(parts[1], color=WHITE, font=font).scale(size2/38)
        objs.append(t2)
    if not objs: return None
    grp = VGroup(*objs).arrange(DOWN, buff=line_gap).to_edge(UP, buff=buff)
    scene.add(grp)
    scene.play(FadeIn(grp, run_time=run_in))
    scene._title_mobj = grp
    return grp

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

        show_title(self, "点灯游戏的数学解法","又名：灭灯游戏,lights out game")

        G5 = make_grid(self, w=5, h=5, lgt_sft=-4.5, btn_sft=-4.5, sz=0.6, t=0.2)
        G7 = make_grid(self, w=7, h=7, lgt_sft=0.0, btn_sft=0.0, sz=0.5, t=0.2)
        G11 = make_grid(self, w=11, h=11, lgt_sft=4.5, btn_sft=4.5, sz=0.35, t=0.2)

        t5 = Text("N=5", color=WHITE).next_to(G5["groups"]["lgt_bd_base"], UP*0.5, buff=0.3)
        t7 = Text("N=7", color=WHITE).next_to(G7["groups"]["lgt_bd_base"], UP*0.5, buff=0.3)
        t11 = Text("N=11", color=WHITE).next_to(G11["groups"]["lgt_bd_base"], UP*0.5, buff=0.3)

        self.play(FadeIn(t5), FadeIn(t7), FadeIn(t11), run_time=0.4)

        apply_matrix(self, G5, MAT5, step_anim=0.15)
        apply_matrix(self, G7, MAT7, step_anim=0.10)
        apply_matrix(self, G11, MAT11, step_anim=0.05)

        self.wait(2)

        destroy_labels(self, t5, t7, t11, rt=0.3)
        destroy_grids(self, [G5, G7, G11], rt=0.3) 

        show_title(self, "游戏规则")

        show_subtitle(self, "规则：在NxN的格子内，点击一个按钮，","该格及周围的灯会被同时翻转。")

        G5 = make_grid(self, w=5, h=5, lgt_sft=0, btn_sft=0, sz=0.6, t=0.2)

        self.wait(0.5)
        press(self, G5, 1, 1, wait=2, anim=0.3)
        press(self, G5, 1, 4, wait=2, anim=0.3)
        press(self, G5, 4, 0, wait=2, anim=0.3)
        press(self, G5, 4, 1, wait=2, anim=0.3)
        press(self, G5, 4, 2, wait=2, anim=0.3)
        self.wait(2)
        destroy_grids(self, [G5], rt=0.3, keep_borders=True )

        show_subtitle(self, "目标：从全暗状态将所有灯打开（或者全亮状态将所有灯关闭）。")
        self.wait(1)
        brighten_all_lights(self, G5, rt=0.4)
        self.wait(2)
        destroy_grids(self, [G5], rt=0.3, keep_borders=True ) 
        self.wait(2)

        show_title(self, "推论")

        show_subtitle(self, "连续按按钮两次，等同于没有按")
        self.wait(0.5)
        press(self, G5, 1, 1, wait=2, anim=0.3)
        press(self, G5, 1, 1, wait=2, anim=0.3)
        press(self, G5, 4, 4, wait=2, anim=0.3)
        press(self, G5, 4, 4, wait=2, anim=0.3)
        self.wait(0.5)
        destroy_grids(self, [G5], rt=0.3, keep_borders=False ) 

        show_subtitle(self, "用不同顺序按按钮，灯的最终状态是一样的")
        G51 = make_grid(self, w=5, h=5, lgt_sft=-3, btn_sft=-3, sz=0.6, t=0.2)
        G52 = make_grid(self, w=5, h=5, lgt_sft=+3, btn_sft=+3, sz=0.6, t=0.2)
        self.wait(0.5)
        press(self, G51, 2, 1, wait=0.0, anim=0.3)
        press(self, G51, 2, 2, wait=0.0, anim=0.3)
        press(self, G51, 2, 3, wait=0.0, anim=0.3)
        press(self, G51, 3, 3, wait=0.0, anim=0.3)
        self.wait(1)
        press(self, G52, 3, 3, wait=0.0, anim=0.3)
        press(self, G52, 2, 3, wait=0.0, anim=0.3)
        press(self, G52, 2, 2, wait=0.0, anim=0.3)
        press(self, G52, 2, 1, wait=0.0, anim=0.3)
        self.wait(3)
        destroy_grids(self, [G51], rt=0.3, keep_borders=False ) 
        destroy_grids(self, [G52], rt=0.3, keep_borders=False ) 
        self.wait(0.5)

        show_subtitle(self, "因此，格子内的按钮，我们只需考虑按或不按，并且不用关心顺序")
#        show_subtitle(self, "【演示】5x5空白随机情况x3，同时显示按钮和灯状态")

        self.wait(4)

#按钮：按或者不按
#灯：亮或者不量

        show_subtitle(self, "所有按钮的状态为一组，对应一组特定状态的灯", "我们可以将按钮和灯分开表示")
#        show_subtitle(self, "【演示】5x5将上面随机格子拆分按钮和灯，按钮左灯右")

        self.wait(2)

        show_subtitle(self, "我们的目标是：找到一个按钮组，其对应灯的状态为全亮。", "那么，我们如何找到这样一个组按钮呢？")
#        show_subtitle(self, "【演示】5x5问号到灯全亮（合并刚才的3个按钮矩阵和灯矩阵）")

        self.wait(2)

        show_subtitle(self, "")


