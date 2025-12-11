from manimlib import *
#from manimlib.config import manim_config
#manim_config.tex.template = "basic_ctex"
import numpy as np

BD_W = 2
BD_W_SEL = 8

DEFAULT_FONT = "SimHei"

SCALE_LATEX = 1.0
SCALE_SUBTITLE = 1.25
SCALE_TITLE = 1.65

REF_TEX = "N\\times N"
ADD_TEX = "<c0>Q"

FONT_COLOR_BLACK = "#333333"
FONT_SIZE_DEFAULT = 32
FONT_SIZE_LARGE = 48
FONT_SIZE_SMALL = 24

HL_COLOR_1 = RED
HL_COLOR_2 = YELLOW

L_COLOR  = "#55aaff"
E_COLOR  = "#55aaff"
B_COLOR  = "#ff55aa"
Y_COLOR  = "#ffff55"
H_COLOR  = "#55aaff"
V_COLOR  = "#aa55ff"
I_COLOR  = "#ffffff"
K_COLOR  = "#55ff55"
F_COLOR  = "#55ddff"
C_COLOR  = "#55ffaa"
P_COLOR  = "#aa55ff"
Q_COLOR  = "#ff55ff"
G_COLOR  = "#ffaaff"
R_COLOR  = "#ffffaa"
Z_COLOR  = "#ffdd55"
D_COLOR  = "#aaffff"
M_COLOR = "#ffffff"
X_COLOR  = "#ffaa55"
T_COLOR  = "#ffffaa"

COLOR_MAP = {
    "cH1": HL_COLOR_1,
    "cH2": HL_COLOR_2,
    "cL":  L_COLOR,
    "cE":  E_COLOR,
    "cB":  B_COLOR,
    "cY":  Y_COLOR,
    "cH":  H_COLOR,
    "cV":  V_COLOR,
    "cI":  I_COLOR,
    "cK":  K_COLOR,
    "cF":  F_COLOR,
    "cC":  C_COLOR,
    "cP":  P_COLOR,
    "cQ":  Q_COLOR,
    "cG":  G_COLOR,
    "cR":  R_COLOR,
    "cZ":  Z_COLOR,
    "cD":  D_COLOR,
    "cM":  M_COLOR,
    "cX":  X_COLOR,
    "cT":  T_COLOR,
    "c0":  FONT_COLOR_BLACK,
}

def make_grid(scene, w, h, lgt_x=0.0, btn_x=0.0, lgt_y=0.0, btn_y=0.0, btn_c=B_COLOR, lgt_c=L_COLOR, sz=1.0, rt=0.3, mat=None, mat_l=None, w_l=None, h_l=None, show=True, mat_g=None):
    w_l = w if w_l is None else int(w_l)
    h_l = h if h_l is None else int(h_l)
    lgt = [[False for _ in range(w_l)] for _ in range(h_l)]
    btn = [[False for _ in range(w)] for _ in range(h)]
    lgt_sel = [[False for _ in range(w_l)] for _ in range(h_l)]
    btn_sel = [[False for _ in range(w)] for _ in range(h)]
    grid_vis_lgt = [[True for _ in range(w_l)] for _ in range(h_l)]
    grid_vis_btn = [[True for _ in range(w)] for _ in range(h)]
    def _apply_mask_from(mat_mask, target, W, H):
        if mat_mask is None: return
        if isinstance(mat_mask, dict):
            _apply_mask_from(mat_mask.get("lgt"), grid_vis_lgt, w_l, h_l)
            _apply_mask_from(mat_mask.get("btn"), grid_vis_btn, w, h)
            return
        mh = len(mat_mask)
        mw = len(mat_mask[0]) if mh > 0 else 0
        Hm = min(H, mh)
        Wm = min(W, mw)
        for j in range(Hm):
            for i in range(Wm):
                v = mat_mask[j][i]
                show_cell = not (v == 0 or (isinstance(v, (int, float)) and v <= -1))
                target[j][i] = bool(show_cell)
    _apply_mask_from(mat_g, grid_vis_lgt, w_l, h_l)
    _apply_mask_from(mat_g, grid_vis_btn, w, h)
    if mat is not None:
        mh=len(mat)
        mw=len(mat[0]) if mh>0 else 0
        H=min(h,mh)
        W=min(w,mw)
        for j in range(H):
            for i in range(W):
                v=int(mat[j][i])
                if v<=-1:
                    grid_vis_btn[j][i]=False
                    if i<w_l and j<h_l: grid_vis_lgt[j][i]=False
    if mat_l is not None:
        lh=len(mat_l)
        lw=len(mat_l[0]) if lh>0 else 0
        H2=min(h_l,lh)
        W2=min(w_l,lw)
        for j in range(H2):
            for i in range(W2):
                v=int(mat_l[j][i])
                if v<=-1:
                    grid_vis_lgt[j][i]=False
                    if i<w and j<h: grid_vis_btn[j][i]=False
    lgt_start_x = -(w_l - 1) * sz / 2.0
    lgt_start_y =  (h_l - 1) * sz / 2.0
    btn_start_x = -(w   - 1) * sz / 2.0
    btn_start_y =  (h   - 1) * sz / 2.0
    lgt_shift = np.array([lgt_x, lgt_y, 0.0])
    btn_shift = np.array([btn_x, btn_y, 0.0])
    lgt_bd_base_grp = VGroup()
    btn_bd_base_grp = VGroup()
    lgt_bd_hl_grp   = VGroup()
    btn_bd_hl_grp   = VGroup()
    lgt_sp_grp      = VGroup()
    btn_sp_grp      = VGroup()
    lgt_sz = 0.85 * sz
    btn_sz = 0.7 * sz / 2.0
    lgt_bd_base = [[None] * w_l for _ in range(h_l)]
    lgt_bd_hl   = [[None] * w_l for _ in range(h_l)]
    lgt_sp      = [[None] * w_l for _ in range(h_l)]
    btn_bd_base = [[None] * w   for _ in range(h)]
    btn_bd_hl   = [[None] * w   for _ in range(h)]
    btn_sp      = [[None] * w   for _ in range(h)]
    for j in range(h_l):
        for i in range(w_l):
            center = np.array([lgt_start_x + i * sz, lgt_start_y - j * sz, 0.0])
            lbd = Square(side_length=sz).set_fill(opacity=0).set_stroke(WHITE, BD_W, 0)
            lbd.move_to(center + lgt_shift)
            if not grid_vis_lgt[j][i]: lbd.set_stroke(opacity=0)
            lgt_bd_base[j][i]=lbd
            lgt_bd_base_grp.add(lbd)
            lbd_hl = lbd.copy().set_stroke(HL_COLOR_1, BD_W_SEL, 0).set_fill(opacity=0)
            if not grid_vis_lgt[j][i]: lbd_hl.set_stroke(opacity=0)
            lgt_bd_hl[j][i]=lbd_hl
            lgt_bd_hl_grp.add(lbd_hl)
            lsp = Square(side_length=lgt_sz).set_stroke(width=0, opacity=0).set_fill(lgt_c,1)
            lsp.move_to(center + lgt_shift)
            if not grid_vis_lgt[j][i]: lsp.set_opacity(0)
            lgt_sp[j][i]=lsp
            lgt_sp_grp.add(lsp)
    for j in range(h):
        for i in range(w):
            center = np.array([btn_start_x + i * sz, btn_start_y - j * sz, 0.0])
            bbd = Square(side_length=sz).set_fill(opacity=0).set_stroke(WHITE, BD_W, 0)
            bbd.move_to(center + btn_shift)
            if not grid_vis_btn[j][i]: bbd.set_stroke(opacity=0)
            btn_bd_base[j][i]=bbd
            btn_bd_base_grp.add(bbd)
            bbd_hl = bbd.copy().set_stroke(HL_COLOR_1, BD_W_SEL, 0).set_fill(opacity=0)
            if not grid_vis_btn[j][i]: bbd_hl.set_stroke(opacity=0)
            btn_bd_hl[j][i]=bbd_hl
            btn_bd_hl_grp.add(bbd_hl)
            bsp = Circle(radius=btn_sz).set_stroke(width=0, opacity=0).set_fill(btn_c,1)
            bsp.move_to(center + btn_shift)
            if not grid_vis_btn[j][i]: bsp.set_opacity(0)
            btn_sp[j][i]=bsp
            btn_sp_grp.add(bsp)
    if mat is not None:
        mh = len(mat)
        mw = len(mat[0]) if mh > 0 else 0
        H = min(h, mh)
        W = min(w, mw)
        for j in range(H):
            for i in range(W):
                v=int(mat[j][i])
                if v<=-1: continue
                if v == 1:
                    btn[j][i] = True
                    for (x, y) in ((i, j), (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                        if 0<=x<w_l and 0<=y<h_l: lgt[y][x]=not lgt[y][x]
    if mat_l is not None:
        lh = len(mat_l)
        lw = len(mat_l[0]) if lh > 0 else 0
        H2 = min(h_l, lh)
        W2 = min(w_l, lw)
        for j in range(H2):
            for i in range(W2):
                v=int(mat_l[j][i])
                if v<=-1: continue
                lgt[j][i]=bool(v)
    for j in range(h_l):
        for i in range(w_l):
            lgt_sp[j][i].set_opacity(1 if (lgt[j][i] and grid_vis_lgt[j][i]) else 0)
    for j in range(h):
        for i in range(w):
            btn_sp[j][i].set_opacity(1 if (btn[j][i] and grid_vis_btn[j][i]) else 0)
    if show:
        scene.add(
            lgt_bd_base_grp,
            btn_bd_base_grp,
            lgt_sp_grp,
            btn_sp_grp,
            btn_bd_hl_grp,
            lgt_bd_hl_grp,
        )
        if rt > 0:
            vis_lgt_bd = VGroup(*[lgt_bd_base[j][i] for j in range(h_l) for i in range(w_l) if grid_vis_lgt[j][i]])
            vis_btn_bd = VGroup(*[btn_bd_base[j][i] for j in range(h) for i in range(w) if grid_vis_btn[j][i]])
            if len(vis_lgt_bd)>0 or len(vis_btn_bd)>0:
                anims=[]
                if len(vis_lgt_bd)>0: anims.append(vis_lgt_bd.animate.set_stroke(opacity=1))
                if len(vis_btn_bd)>0: anims.append(vis_btn_bd.animate.set_stroke(opacity=1))
                scene.play(*anims, run_time=rt)
        else:
            VGroup(*[lgt_bd_base[j][i] for j in range(h_l) for i in range(w_l) if grid_vis_lgt[j][i]]).set_stroke(opacity=1)
            VGroup(*[btn_bd_base[j][i] for j in range(h) for i in range(w) if grid_vis_btn[j][i]]).set_stroke(opacity=1)
    else:
        VGroup(*[lgt_bd_base[j][i] for j in range(h_l) for i in range(w_l) if grid_vis_lgt[j][i]]).set_stroke(opacity=1)
        VGroup(*[btn_bd_base[j][i] for j in range(h) for i in range(w) if grid_vis_btn[j][i]]).set_stroke(opacity=1)
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
        "grid_vis_lgt": grid_vis_lgt,
        "grid_vis_btn": grid_vis_btn,
        "groups": {
            "lgt_bd_base": lgt_bd_base_grp,
            "btn_bd_base": btn_bd_base_grp,
            "lgt_bd_hl": lgt_bd_hl_grp,
            "btn_bd_hl": btn_bd_hl_grp,
            "lgt_sp": lgt_sp_grp,
            "btn_sp": btn_sp_grp,
        },
        "params": {
            "w": w,
            "h": h,
            "w_l": w_l,
            "h_l": h_l,
            "sz": sz,
            "lgt_x": lgt_x,
            "lgt_y": lgt_y,
            "btn_x": btn_x,
            "btn_y": btn_y,
            "mat": mat,
            "mat_l": mat_l,
            "mat_g": mat_g,
        },
    }

def trans_grid(scene, A_from, A_to, rt=0.8, keep_from=False, target_override=None, extra_anims=None, B_from=None, B_to=None, B_target_override=None, B_extra_anims=None):
    if A_to["groups"]["lgt_bd_base"].get_stroke_opacity() == 0:
        A_to["groups"]["lgt_bd_base"].set_stroke(opacity=1)
    if A_to["groups"]["btn_bd_base"].get_stroke_opacity() == 0:
        A_to["groups"]["btn_bd_base"].set_stroke(opacity=1)
    if B_to is not None:
        if B_to["groups"]["lgt_bd_base"].get_stroke_opacity() == 0:
            B_to["groups"]["lgt_bd_base"].set_stroke(opacity=1)
        if B_to["groups"]["btn_bd_base"].get_stroke_opacity() == 0:
            B_to["groups"]["btn_bd_base"].set_stroke(opacity=1)
    def composite(G):
        return VGroup(
            G["groups"]["lgt_sp"],
            G["groups"]["lgt_bd_base"],
            G["groups"]["btn_sp"],
            G["groups"]["btn_bd_base"],
        )
    grp_from_A = composite(A_from).copy() if keep_from else composite(A_from)
    grp_to_A = target_override if target_override is not None else composite(A_to)
    if keep_from:
        scene.add(grp_from_A)
    anims = [ReplacementTransform(grp_from_A, grp_to_A)]
    grp_from_B = None
    grp_to_B = None
    if B_from is not None and B_to is not None:
        grp_from_B = composite(B_from).copy() if keep_from else composite(B_from)
        grp_to_B = B_target_override if B_target_override is not None else composite(B_to)
        if keep_from:
            scene.add(grp_from_B)
        anims.append(ReplacementTransform(grp_from_B, grp_to_B))
    if extra_anims:
        anims.extend(extra_anims)
    if B_extra_anims:
        anims.extend(B_extra_anims)
    scene.play(*anims, run_time=rt)
    if target_override is not None:
        try:
            scene.remove(grp_to_A)
        except Exception:
            pass
    if B_to is not None and B_target_override is not None and grp_to_B is not None:
        try:
            scene.remove(grp_to_B)
        except Exception:
            pass
    scene.add(A_to["groups"]["lgt_bd_hl"])
    scene.add(A_to["groups"]["btn_bd_hl"])
    if B_to is not None:
        scene.add(B_to["groups"]["lgt_bd_hl"])
        scene.add(B_to["groups"]["btn_bd_hl"])
    try:
        scene.bring_to_front(A_to["groups"]["lgt_bd_hl"])
        scene.bring_to_front(A_to["groups"]["btn_bd_hl"])
        if B_to is not None:
            scene.bring_to_front(B_to["groups"]["lgt_bd_hl"])
            scene.bring_to_front(B_to["groups"]["btn_bd_hl"])
    except Exception:
        pass
    if not keep_from:
        if B_from is not None:
            del_grids(scene, [A_from, B_from], rt=0.0)
        else:
            del_grids(scene, A_from, rt=0.0)

def add_grid(scene, A_from, A_to, B_from=None, B_to=None, rt=0.8, keep_from=True):
    ht_btn_A, wt_btn_A = A_to["params"]["h"], A_to["params"]["w"]
    hf_btn_A, wf_btn_A = A_from["params"]["h"], A_from["params"]["w"]
    ht_lgt_A = A_to["params"].get("h_l", ht_btn_A)
    wt_lgt_A = A_to["params"].get("w_l", wt_btn_A)
    hf_lgt_A = A_from["params"].get("h_l", hf_btn_A)
    wf_lgt_A = A_from["params"].get("w_l", wf_btn_A)
    btn_x_A = [[0] * wt_btn_A for _ in range(ht_btn_A)]
    for j in range(ht_btn_A):
        for i in range(wt_btn_A):
            b0 = 1 if A_to["btn"][j][i] else 0
            b1 = 1 if (j < hf_btn_A and i < wf_btn_A and A_from["btn"][j][i]) else 0
            btn_x_A[j][i] = b0 ^ b1
    lgt_x_A = [[0] * wt_lgt_A for _ in range(ht_lgt_A)]
    for j in range(ht_lgt_A):
        for i in range(wt_lgt_A):
            l0 = 1 if A_to["lgt"][j][i] else 0
            l1 = 1 if (j < hf_lgt_A and i < wf_lgt_A and A_from["lgt"][j][i]) else 0
            lgt_x_A[j][i] = l0 ^ l1
    lgt_sp_final_A = []
    for j in range(ht_lgt_A):
        for i in range(wt_lgt_A):
            m1 = A_to["lgt_sp"][j][i].copy()
            m1.set_opacity(1.0 if lgt_x_A[j][i] else 0.0)
            lgt_sp_final_A.append(m1)
    btn_sp_final_A = []
    for j in range(ht_btn_A):
        for i in range(wt_btn_A):
            m2 = A_to["btn_sp"][j][i].copy()
            m2.set_opacity(1.0 if btn_x_A[j][i] else 0.0)
            btn_sp_final_A.append(m2)
    grp_final_A = VGroup(
        VGroup(*lgt_sp_final_A),
        A_to["groups"]["lgt_bd_base"].copy(),
        VGroup(*btn_sp_final_A),
        A_to["groups"]["btn_bd_base"].copy(),
    )
    anims_A = []
    for j in range(ht_lgt_A):
        for i in range(wt_lgt_A):
            _queue_opacity_anim(A_to["lgt_sp"][j][i], 1.0 if lgt_x_A[j][i] else 0.0, anims_A)
    for j in range(ht_btn_A):
        for i in range(wt_btn_A):
            _queue_opacity_anim(A_to["btn_sp"][j][i], 1.0 if btn_x_A[j][i] else 0.0, anims_A)
    if B_from is not None and B_to is not None:
        ht_btn_B, wt_btn_B = B_to["params"]["h"], B_to["params"]["w"]
        hf_btn_B, wf_btn_B = B_from["params"]["h"], B_from["params"]["w"]
        ht_lgt_B = B_to["params"].get("h_l", ht_btn_B)
        wt_lgt_B = B_to["params"].get("w_l", wt_btn_B)
        hf_lgt_B = B_from["params"].get("h_l", hf_btn_B)
        wf_lgt_B = B_from["params"].get("w_l", wf_btn_B)
        btn_x_B = [[0] * wt_btn_B for _ in range(ht_btn_B)]
        for j in range(ht_btn_B):
            for i in range(wt_btn_B):
                b0 = 1 if B_to["btn"][j][i] else 0
                b1 = 1 if (j < hf_btn_B and i < wf_btn_B and B_from["btn"][j][i]) else 0
                btn_x_B[j][i] = b0 ^ b1
        lgt_x_B = [[0] * wt_lgt_B for _ in range(ht_lgt_B)]
        for j in range(ht_lgt_B):
            for i in range(wt_lgt_B):
                l0 = 1 if B_to["lgt"][j][i] else 0
                l1 = 1 if (j < hf_lgt_B and i < wf_lgt_B and B_from["lgt"][j][i]) else 0
                lgt_x_B[j][i] = l0 ^ l1
        lgt_sp_final_B = []
        for j in range(ht_lgt_B):
            for i in range(wt_lgt_B):
                m1 = B_to["lgt_sp"][j][i].copy()
                m1.set_opacity(1.0 if lgt_x_B[j][i] else 0.0)
                lgt_sp_final_B.append(m1)
        btn_sp_final_B = []
        for j in range(ht_btn_B):
            for i in range(wt_btn_B):
                m2 = B_to["btn_sp"][j][i].copy()
                m2.set_opacity(1.0 if btn_x_B[j][i] else 0.0)
                btn_sp_final_B.append(m2)
        grp_final_B = VGroup(
            VGroup(*lgt_sp_final_B),
            B_to["groups"]["lgt_bd_base"].copy(),
            VGroup(*btn_sp_final_B),
            B_to["groups"]["btn_bd_base"].copy(),
        )
        anims_B = []
        for j in range(ht_lgt_B):
            for i in range(wt_lgt_B):
                _queue_opacity_anim(B_to["lgt_sp"][j][i], 1.0 if lgt_x_B[j][i] else 0.0, anims_B)
        for j in range(ht_btn_B):
            for i in range(wt_btn_B):
                _queue_opacity_anim(B_to["btn_sp"][j][i], 1.0 if btn_x_B[j][i] else 0.0, anims_B)
        trans_grid(scene, A_from, A_to, rt=rt, keep_from=keep_from, target_override=grp_final_A, extra_anims=anims_A, B_from=B_from, B_to=B_to, B_target_override=grp_final_B, B_extra_anims=anims_B)
        for j in range(ht_btn_B):
            for i in range(wt_btn_B):
                B_to["btn"][j][i] = bool(btn_x_B[j][i])
                B_to["btn_sp"][j][i].set_opacity(1.0 if btn_x_B[j][i] else 0.0)
        for j in range(ht_lgt_B):
            for i in range(wt_lgt_B):
                B_to["lgt"][j][i] = bool(lgt_x_B[j][i])
                B_to["lgt_sp"][j][i].set_opacity(1.0 if lgt_x_B[j][i] else 0.0)
    else:
        trans_grid(scene, A_from, A_to, rt=rt, keep_from=keep_from, target_override=grp_final_A, extra_anims=anims_A)
    for j in range(ht_btn_A):
        for i in range(wt_btn_A):
            A_to["btn"][j][i] = bool(btn_x_A[j][i])
            A_to["btn_sp"][j][i].set_opacity(1.0 if btn_x_A[j][i] else 0.0)
    for j in range(ht_lgt_A):
        for i in range(wt_lgt_A):
            A_to["lgt"][j][i] = bool(lgt_x_A[j][i])
            A_to["lgt_sp"][j][i].set_opacity(1.0 if lgt_x_A[j][i] else 0.0)

def swap_grid(scene, A_from, A_to, B_from=None, B_to=None, rt=0.8):
    gA, gB = A_from["groups"], A_to["groups"]
    dA_l = gB["lgt_sp"].get_center() - gA["lgt_sp"].get_center()
    dA_b = gB["btn_sp"].get_center() - gA["btn_sp"].get_center()
    dB_l = -dA_l
    dB_b = -dA_b
    lgt_sp_A = gA["lgt_sp"]
    lgt_sp_B = gB["lgt_sp"]
    btn_sp_A = gA["btn_sp"]
    btn_sp_B = gB["btn_sp"]
    lgt_color_A = lgt_sp_A[0].get_fill_color() if len(lgt_sp_A) > 0 else None
    lgt_color_B = lgt_sp_B[0].get_fill_color() if len(lgt_sp_B) > 0 else None
    btn_color_A = btn_sp_A[0].get_fill_color() if len(btn_sp_A) > 0 else None
    btn_color_B = btn_sp_B[0].get_fill_color() if len(btn_sp_B) > 0 else None
    anims = []
    a_lgt_anim = lgt_sp_A.animate.shift(dA_l)
    b_lgt_anim = lgt_sp_B.animate.shift(dB_l)
    a_btn_anim = btn_sp_A.animate.shift(dA_b)
    b_btn_anim = btn_sp_B.animate.shift(dB_b)
    if lgt_color_B is not None: a_lgt_anim = a_lgt_anim.set_fill(lgt_color_B)
    if lgt_color_A is not None: b_lgt_anim = b_lgt_anim.set_fill(lgt_color_A)
    if btn_color_B is not None: a_btn_anim = a_btn_anim.set_fill(btn_color_B)
    if btn_color_A is not None: b_btn_anim = b_btn_anim.set_fill(btn_color_A)
    anims.extend([
        a_lgt_anim,
        gA["lgt_bd_base"].animate.shift(dA_l),
        gA["lgt_bd_hl"].animate.shift(dA_l),
        a_btn_anim,
        gA["btn_bd_base"].animate.shift(dA_b),
        gA["btn_bd_hl"].animate.shift(dA_b),
        b_lgt_anim,
        gB["lgt_bd_base"].animate.shift(dB_l),
        gB["lgt_bd_hl"].animate.shift(dB_l),
        b_btn_anim,
        gB["btn_bd_base"].animate.shift(dB_b),
        gB["btn_bd_hl"].animate.shift(dB_b),
    ])
    frA = A_from.get("extras", {}).get("outer_frames", [])
    frB = A_to.get("extras", {}).get("outer_frames", [])
    if frA:
        if len(frA) >= 1: anims.append(frA[0].animate.shift(dA_l))
        if len(frA) >= 2: anims.append(frA[1].animate.shift(dA_b))
    if frB:
        if len(frB) >= 1: anims.append(frB[0].animate.shift(dB_l))
        if len(frB) >= 2: anims.append(frB[1].animate.shift(dB_b))
    if B_from is not None and B_to is not None:
        gC, gD = B_from["groups"], B_to["groups"]
        dC_l = gD["lgt_sp"].get_center() - gC["lgt_sp"].get_center()
        dC_b = gD["btn_sp"].get_center() - gC["btn_sp"].get_center()
        dD_l = -dC_l
        dD_b = -dC_b
        lgt_sp_C = gC["lgt_sp"]
        lgt_sp_D = gD["lgt_sp"]
        btn_sp_C = gC["btn_sp"]
        btn_sp_D = gD["btn_sp"]
        lgt_color_C = lgt_sp_C[0].get_fill_color() if len(lgt_sp_C) > 0 else None
        lgt_color_D = lgt_sp_D[0].get_fill_color() if len(lgt_sp_D) > 0 else None
        btn_color_C = btn_sp_C[0].get_fill_color() if len(btn_sp_C) > 0 else None
        btn_color_D = btn_sp_D[0].get_fill_color() if len(btn_sp_D) > 0 else None
        c_lgt_anim = lgt_sp_C.animate.shift(dC_l)
        d_lgt_anim = lgt_sp_D.animate.shift(dD_l)
        c_btn_anim = btn_sp_C.animate.shift(dC_b)
        d_btn_anim = btn_sp_D.animate.shift(dD_b)
        if lgt_color_D is not None: c_lgt_anim = c_lgt_anim.set_fill(lgt_color_D)
        if lgt_color_C is not None: d_lgt_anim = d_lgt_anim.set_fill(lgt_color_C)
        if btn_color_D is not None: c_btn_anim = c_btn_anim.set_fill(btn_color_D)
        if btn_color_C is not None: d_btn_anim = d_btn_anim.set_fill(btn_color_C)
        anims.extend([
            c_lgt_anim,
            gC["lgt_bd_base"].animate.shift(dC_l),
            gC["lgt_bd_hl"].animate.shift(dC_l),
            c_btn_anim,
            gC["btn_bd_base"].animate.shift(dC_b),
            gC["btn_bd_hl"].animate.shift(dC_b),
            d_lgt_anim,
            gD["lgt_bd_base"].animate.shift(dD_l),
            gD["lgt_bd_hl"].animate.shift(dD_l),
            d_btn_anim,
            gD["btn_bd_base"].animate.shift(dD_b),
            gD["btn_bd_hl"].animate.shift(dD_b),
        ])
        frC = B_from.get("extras", {}).get("outer_frames", [])
        frD = B_to.get("extras", {}).get("outer_frames", [])
        if frC:
            if len(frC) >= 1: anims.append(frC[0].animate.shift(dC_l))
            if len(frC) >= 2: anims.append(frC[1].animate.shift(dC_b))
        if frD:
            if len(frD) >= 1: anims.append(frD[0].animate.shift(dD_l))
            if len(frD) >= 2: anims.append(frD[1].animate.shift(dD_b))
    if anims: scene.play(*anims, run_time=rt)
    tmp = A_from.copy()
    A_from.clear()
    A_from.update(A_to)
    A_to.clear()
    A_to.update(tmp)
    if B_from is not None and B_to is not None:
        tmp2 = B_from.copy()
        B_from.clear()
        B_from.update(B_to)
        B_to.clear()
        B_to.update(tmp2)
    try:
        objs = [
            A_from["groups"]["lgt_bd_hl"],
            A_from["groups"]["btn_bd_hl"],
            A_to["groups"]["lgt_bd_hl"],
            A_to["groups"]["btn_bd_hl"],
        ]
        if B_from is not None and B_to is not None:
            objs.extend([
                B_from["groups"]["lgt_bd_hl"],
                B_from["groups"]["btn_bd_hl"],
                B_to["groups"]["lgt_bd_hl"],
                B_to["groups"]["btn_bd_hl"],
            ])
        scene.bring_to_front(*objs)
    except Exception:
        pass

def addshift_grid(scene, A_from, A_to, B_from=None, B_to=None, k=1, rt=0.8):
    if k < 0: return
    ht_lgt_A = A_to["params"].get("h_l", A_to["params"]["h"])
    wt_lgt_A = A_to["params"].get("w_l", A_to["params"]["w"])
    hf_lgt_A = A_from["params"].get("h_l", A_from["params"]["h"])
    wf_lgt_A = A_from["params"].get("w_l", A_from["params"]["w"])
    new_lgt_A = [[False]*wt_lgt_A for _ in range(ht_lgt_A)]
    for j in range(ht_lgt_A):
        for i in range(wt_lgt_A):
            v = bool(A_to["lgt"][j][i])
            src = i - k
            if 0 <= src < wf_lgt_A and j < hf_lgt_A and A_from["lgt"][j][src]:
                v = not v
            new_lgt_A[j][i] = v
    new_lgt_B = None
    if B_from is not None and B_to is not None:
        ht_lgt_B = B_to["params"].get("h_l", B_to["params"]["h"])
        wt_lgt_B = B_to["params"].get("w_l", B_to["params"]["w"])
        hf_lgt_B = B_from["params"].get("h_l", B_from["params"]["h"])
        wf_lgt_B = B_from["params"].get("w_l", B_from["params"]["w"])
        new_lgt_B = [[False]*wt_lgt_B for _ in range(ht_lgt_B)]
        for j in range(ht_lgt_B):
            for i in range(wt_lgt_B):
                v = bool(B_to["lgt"][j][i])
                src = i - k
                if 0 <= src < wf_lgt_B and j < hf_lgt_B and B_from["lgt"][j][src]:
                    v = not v
                new_lgt_B[j][i] = v
    anims = []
    movers = []
    for j in range(min(hf_lgt_A, ht_lgt_A)):
        for src in range(wf_lgt_A):
            if not A_from["lgt"][j][src]: continue
            dest = src + k
            if 0 <= dest < wt_lgt_A and j < ht_lgt_A:
                bd = A_from["lgt_bd_base"][j][src].copy()
                sp = A_from["lgt_sp"][j][src].copy()
                m = VGroup(bd, sp)
                m.set_opacity(1.0)
                scene.add(m)
                movers.append(m)
                a = m.animate.move_to(A_to["lgt_sp"][j][dest].get_center()).set_opacity(0.0)
                anims.append(a)
    if B_from is not None and B_to is not None and new_lgt_B is not None:
        for j in range(min(hf_lgt_B, ht_lgt_B)):
            for src in range(wf_lgt_B):
                if not B_from["lgt"][j][src]: continue
                dest = src + k
                if 0 <= dest < wt_lgt_B and j < ht_lgt_B:
                    bd = B_from["lgt_bd_base"][j][src].copy()
                    sp = B_from["lgt_sp"][j][src].copy()
                    m = VGroup(bd, sp)
                    m.set_opacity(1.0)
                    scene.add(m)
                    movers.append(m)
                    a = m.animate.move_to(B_to["lgt_sp"][j][dest].get_center()).set_opacity(0.0)
                    anims.append(a)
    for j in range(ht_lgt_A):
        for i in range(wt_lgt_A):
            target = 1.0 if new_lgt_A[j][i] else 0.0
            _queue_opacity_anim(A_to["lgt_sp"][j][i], target, anims)
    if B_from is not None and B_to is not None and new_lgt_B is not None:
        for j in range(ht_lgt_B):
            for i in range(wt_lgt_B):
                target = 1.0 if new_lgt_B[j][i] else 0.0
                _queue_opacity_anim(B_to["lgt_sp"][j][i], target, anims)
    if anims:
        scene.play(*anims, run_time=rt)
    for m in movers:
        try:
            scene.remove(m)
        except Exception:
            pass
    for j in range(ht_lgt_A):
        for i in range(wt_lgt_A):
            A_to["lgt"][j][i] = bool(new_lgt_A[j][i])
            A_to["lgt_sp"][j][i].set_opacity(1.0 if new_lgt_A[j][i] else 0.0)
    if B_from is not None and B_to is not None and new_lgt_B is not None:
        for j in range(ht_lgt_B):
            for i in range(wt_lgt_B):
                B_to["lgt"][j][i] = bool(new_lgt_B[j][i])
                B_to["lgt_sp"][j][i].set_opacity(1.0 if new_lgt_B[j][i] else 0.0)

def shift_grid(scene, A_from, B_from=None, k=1, rt=0.3):
    if k <= 0: return
    ht_lgt_A = A_from["params"].get("h_l", A_from["params"]["h"])
    wt_lgt_A = A_from["params"].get("w_l", A_from["params"]["w"])
    new_lgt_A = [[False]*wt_lgt_A for _ in range(ht_lgt_A)]
    for j in range(ht_lgt_A):
        for i in range(wt_lgt_A):
            src = i - k
            v = False
            if 0 <= src < wt_lgt_A:
                v = bool(A_from["lgt"][j][src])
            new_lgt_A[j][i] = v
    if B_from is not None:
        ht_lgt_B = B_from["params"].get("h_l", B_from["params"]["h"])
        wt_lgt_B = B_from["params"].get("w_l", B_from["params"]["w"])
        new_lgt_B = [[False]*wt_lgt_B for _ in range(ht_lgt_B)]
        for j in range(ht_lgt_B):
            for i in range(wt_lgt_B):
                src = i - k
                v = False
                if 0 <= src < wt_lgt_B:
                    v = bool(B_from["lgt"][j][src])
                new_lgt_B[j][i] = v
    anims = []
    for j in range(ht_lgt_A):
        for i in range(wt_lgt_A):
            target = 1.0 if new_lgt_A[j][i] else 0.0
            _queue_opacity_anim(A_from["lgt_sp"][j][i], target, anims)
    if B_from is not None:
        for j in range(ht_lgt_B):
            for i in range(wt_lgt_B):
                target = 1.0 if new_lgt_B[j][i] else 0.0
                _queue_opacity_anim(B_from["lgt_sp"][j][i], target, anims)
    if anims:
        scene.play(*anims, run_time=rt)
    for j in range(ht_lgt_A):
        for i in range(wt_lgt_A):
            A_from["lgt"][j][i] = bool(new_lgt_A[j][i])
            A_from["lgt_sp"][j][i].set_opacity(1.0 if new_lgt_A[j][i] else 0.0)
    if B_from is not None:
        for j in range(ht_lgt_B):
            for i in range(wt_lgt_B):
                B_from["lgt"][j][i] = bool(new_lgt_B[j][i])
                B_from["lgt_sp"][j][i].set_opacity(1.0 if new_lgt_B[j][i] else 0.0)

def move_grid(scene, G, lgt_x=0.0, btn_x=0.0, lgt_y=0.0, btn_y=0.0, rt=0.8, sz=None):
    px = G["params"].get("lgt_x", 0.0)
    py = G["params"].get("lgt_y", 0.0)
    qx = G["params"].get("btn_x", 0.0)
    qy = G["params"].get("btn_y", 0.0)
    dlgt = np.array([lgt_x - px, lgt_y - py, 0.0])
    dbtn = np.array([btn_x - qx, btn_y - qy, 0.0])
    lg=G["groups"]
    lgt_targets=[lg["lgt_bd_base"],lg["lgt_bd_hl"],lg["lgt_sp"]]
    btn_targets=[lg["btn_bd_base"],lg["btn_bd_hl"],lg["btn_sp"]]
    if "lgt_group" not in lg: lg["lgt_group"]=VGroup(*lgt_targets)
    if "btn_group" not in lg: lg["btn_group"]=VGroup(*btn_targets)
    lgt_group=lg["lgt_group"]
    btn_group=lg["btn_group"]
    k=1.0
    if sz is not None:
        cols=max(1,G["params"].get("cols",1))
        cur_unit=max(lgt_group.get_width()/cols,1e-12)
        k=sz/max(cur_unit,1e-12)
    need_scale=abs(k-1.0)>1e-9
    need_move=(np.linalg.norm(dlgt)>1e-9) or (np.linalg.norm(dbtn)>1e-9)
    if rt>0 and (need_scale or need_move):
        tl=lgt_group.copy()
        tb=btn_group.copy()
        if need_scale:
            tl.scale(k)
            tb.scale(k)
        if np.linalg.norm(dlgt)>1e-9: tl.shift(dlgt)
        if np.linalg.norm(dbtn)>1e-9: tb.shift(dbtn)
        scene.play(Transform(lgt_group,tl),Transform(btn_group,tb),run_time=rt)
    else:
        if need_scale:
            lgt_group.scale(k)
            btn_group.scale(k)
        if np.linalg.norm(dlgt)>1e-9: lgt_group.shift(dlgt)
        if np.linalg.norm(dbtn)>1e-9: btn_group.shift(dbtn)
    G["params"]["lgt_x"] = lgt_x
    G["params"]["lgt_y"] = lgt_y
    G["params"]["btn_x"] = btn_x
    G["params"]["btn_y"] = btn_y
    if sz is not None: G["params"]["size"]=sz

def toggle_grid(scene, G, i, j, which="both", to=None, anim=0.3):
    anims=[]
    def _apply_one(kind, i, j, vis_to):
        if kind=="lgt":
            if not (0<=j<len(G["grid_vis_lgt"]) and 0<=i<len(G["grid_vis_lgt"][0])): return
            cur=G["grid_vis_lgt"][j][i]
            new= (not cur) if to is None else bool(to)
            G["grid_vis_lgt"][j][i]=new
            bd=G["lgt_bd_base"][j][i]
            hl=G["lgt_bd_hl"][j][i]
            sp=G["lgt_sp"][j][i]
            sp.set_stroke(width=0, opacity=0)
            if new:
                bd.set_fill(opacity=0)
                sp.set_fill(L_COLOR, 1)
                t_bd = 1.0
                t_hl = 1.0 if G["lgt_sel"][j][i] else 0.0
                if G["lgt"][j][i]:
                    if anim > 0 and scene is not None:
                        anims.append(sp.animate.set_opacity(1.0))
                    else:
                        sp.set_opacity(1.0)
                else:
                    sp.set_opacity(0.0)
            else:
                t_bd = 0.0
                t_hl = 0.0
                sp.set_opacity(0.0)
            if anim > 0 and scene is not None:
                anims.append(bd.animate.set_stroke(opacity=t_bd))
                anims.append(hl.animate.set_stroke(opacity=t_hl))
            else:
                bd.set_stroke(opacity=t_bd)
                hl.set_stroke(opacity=t_hl)
        else:
            if not (0<=j<len(G["grid_vis_btn"]) and 0<=i<len(G["grid_vis_btn"][0])): return
            cur=G["grid_vis_btn"][j][i]
            new= (not cur) if to is None else bool(to)
            G["grid_vis_btn"][j][i]=new
            bd=G["btn_bd_base"][j][i]
            hl=G["btn_bd_hl"][j][i]
            sp=G["btn_sp"][j][i]
            sp.set_stroke(width=0, opacity=0)
            if new:
                bd.set_fill(opacity=0)
                sp.set_fill(B_COLOR, 1)
                t_bd = 1.0
                t_hl = 1.0 if G["btn_sel"][j][i] else 0.0
                if G["btn"][j][i]:
                    if anim > 0 and scene is not None:
                        anims.append(sp.animate.set_opacity(1.0))
                    else:
                        sp.set_opacity(1.0)
                else:
                    sp.set_opacity(0.0)
            else:
                t_bd = 0.0
                t_hl = 0.0
                sp.set_opacity(0.0)
            if anim > 0 and scene is not None:
                anims.append(bd.animate.set_stroke(opacity=t_bd))
                anims.append(hl.animate.set_stroke(opacity=t_hl))
            else:
                bd.set_stroke(opacity=t_bd)
                hl.set_stroke(opacity=t_hl)
    if which in ("lgt","both"): _apply_one("lgt",i,j,to)
    if which in ("btn","both"): _apply_one("btn",i,j,to)
    if anim>0 and anims: scene.play(*anims, run_time=anim)

def toggle_lgt(scene, G, i, j, anim=0.3):
    G["lgt"][j][i] = not G["lgt"][j][i]
    m = G["lgt_sp"][j][i]
    m.set_stroke(width=0, opacity=0)
    vis = True
    if "grid_vis_lgt" in G and 0<=j<len(G["grid_vis_lgt"]) and 0<=i<len(G["grid_vis_lgt"][0]):
        vis = G["grid_vis_lgt"][j][i]
    target = 1 if (G["lgt"][j][i] and vis) else 0
    if scene is not None and anim>0:
        scene.play(m.animate.set_opacity(target), run_time=anim)
    else:
        m.set_opacity(target)

def toggle_btn(scene, G, i, j, anim=0.3):
    G["btn"][j][i] = not G["btn"][j][i]
    m = G["btn_sp"][j][i]
    m.set_stroke(width=0, opacity=0)
    vis = True
    if "grid_vis_btn" in G and 0<=j<len(G["grid_vis_btn"]) and 0<=i<len(G["grid_vis_btn"][0]):
        vis = G["grid_vis_btn"][j][i]
    target = 1 if (G["btn"][j][i] and vis) else 0
    if scene is not None and anim>0:
        scene.play(m.animate.set_opacity(target), run_time=anim)
    else:
        m.set_opacity(target)

def set_bd(G, kind, i, j, selected):
    if kind == "lgt":
        G["lgt_sel"][j][i] = selected
        vis=True
        if "grid_vis_lgt" in G and 0<=j<len(G["grid_vis_lgt"]) and 0<=i<len(G["grid_vis_lgt"][0]):
            vis=G["grid_vis_lgt"][j][i]
        G["lgt_bd_hl"][j][i].set_stroke(opacity=1 if (selected and vis) else 0)
        return
    G["btn_sel"][j][i] = selected
    vis=True
    if "grid_vis_btn" in G and 0<=j<len(G["grid_vis_btn"]) and 0<=i<len(G["grid_vis_btn"][0]):
        vis=G["grid_vis_btn"][j][i]
    G["btn_bd_hl"][j][i].set_stroke(opacity=1 if (selected and vis) else 0)

def clear_all_bd(G):
    w = G["params"]["w"]
    h = G["params"]["h"]
    for j in range(h):
        for i in range(w):
            if G["lgt_sel"][j][i]:
                G["lgt_sel"][j][i] = False
                G["lgt_bd_hl"][j][i].set_stroke(opacity=0)
            if G["btn_sel"][j][i]:
                G["btn_sel"][j][i] = False
                G["btn_bd_hl"][j][i].set_stroke(opacity=0)

def hl_bd(scene, grids, color=HL_COLOR_1, width=BD_W_SEL, buff=0.06, rt=0.3):
    if isinstance(grids, dict):
        gs = [[grids]]
    else:
        gs = grids if isinstance(grids[0], list) else [grids]
    root_group = VGroup()
    for y in range(len(gs)):
        for x in range(len(gs[y])):
            G = gs[y][x]
            root_group.add(G["groups"]["lgt_bd_base"], G["groups"]["btn_bd_base"])
    bd = (
        SurroundingRectangle(root_group, buff=buff)
        .set_fill(opacity=0)
        .set_stroke(color, width, 1)
    )
    scene.add(bd)
    scene.play(FadeIn(bd), run_time=rt)
    return bd

def del_bd(scene, bd, rt=0.3):
    if bd is None:
        return
    scene.play(FadeOut(bd), run_time=rt)
    try:
        scene.remove(bd)
    except Exception:
        pass

def hl_cells(scene, grids, which="lgt", indices=[(0,0)], color=HL_COLOR_1, width=BD_W_SEL, rt=0.3):
    gs = grids if isinstance(grids[0], list) else [grids]
    anims = []
    for y in range(len(gs)):
        for x in range(len(gs[y])):
            G = gs[y][x]
            for (i, j) in indices:
                m = G[f"{which}_bd_hl"][j][i]
                G[f"{which}_sel"][j][i] = True
                anims.append(ApplyMethod(m.set_stroke, color, width, 1))
    if anims:
        scene.play(*anims, run_time=rt)

def del_cells(scene, grids, which="lgt", indices=None, rt=0.3):
    gs = grids if isinstance(grids[0], list) else [grids]
    anims = []
    for y in range(len(gs)):
        for x in range(len(gs[y])):
            G = gs[y][x]
            h, w = G["params"]["h"], G["params"]["w"]
            idxs = indices if indices is not None else [(i, j) for j in range(h) for i in range(w)]
            for (i, j) in idxs:
                m = G[f"{which}_bd_hl"][j][i]
                anims.append(m.animate.set_stroke(opacity=0))
                G[f"{which}_sel"][j][i] = False
    if anims:
        scene.play(*anims, run_time=rt)

def add_cell(scene, G_from, G_to, sx, sy, tx, ty, rt=0.3, color_from=None, color_to=None):
    ht_lgt_to = G_to["params"].get("h_l", G_to["params"]["h"])
    wt_lgt_to = G_to["params"].get("w_l", G_to["params"]["w"])
    hf_btn_from = G_from["params"]["h"]
    wf_btn_from = G_from["params"]["w"]
    if not (0 <= sx < wf_btn_from and 0 <= sy < hf_btn_from):
        return
    if not (0 <= tx < wt_lgt_to and 0 <= ty < ht_lgt_to):
        return
    do_hl = scene is not None and (color_from is not None or color_to is not None)
    h_btn_to = G_to["params"]["h"]
    w_btn_to = G_to["params"]["w"]
    if do_hl:
        if color_from is not None:
            hl_cells(scene, [G_from], which="btn", indices=[(sx, sy)], color=color_from, rt=rt)
        if color_to is not None and 0 <= tx < w_btn_to and 0 <= ty < h_btn_to:
            hl_cells(scene, [G_to], which="btn", indices=[(tx, ty)], color=color_to, rt=rt)
    G_to["lgt"][ty][tx] = not G_to["lgt"][ty][tx]
    m_target = G_to["lgt_sp"][ty][tx]
    m_target.set_stroke(width=0, opacity=0)
    vis_to = True
    if "grid_vis_lgt" in G_to and 0 <= ty < len(G_to["grid_vis_lgt"]) and 0 <= tx < len(G_to["grid_vis_lgt"][0]):
        vis_to = G_to["grid_vis_lgt"][ty][tx]
    target_op = 1.0 if (G_to["lgt"][ty][tx] and vis_to) else 0.0
    if scene is not None and rt > 0:
        m_btn_src = G_from["btn_sp"][sy][sx].copy()
        m_lgt_src = G_from["lgt_sp"][sy][sx].copy()
        moving = VGroup(m_lgt_src, m_btn_src)
        vis_btn_from = True
        if "grid_vis_btn" in G_from and 0 <= sy < len(G_from["grid_vis_btn"]) and 0 <= sx < len(G_from["grid_vis_btn"][0]):
            vis_btn_from = G_from["grid_vis_btn"][sy][sx]
        op_btn_from = 1.0 if vis_btn_from else 0.0
        vis_lgt_from = True
        if "grid_vis_lgt" in G_from and 0 <= sy < len(G_from["grid_vis_lgt"]) and 0 <= sx < len(G_from["grid_vis_lgt"][0]):
            vis_lgt_from = G_from["grid_vis_lgt"][sy][sx]
        op_lgt_from = 1.0 if (G_from["lgt"][sy][sx] and vis_lgt_from) else 0.0
        m_btn_src.set_opacity(op_btn_from)
        m_lgt_src.set_opacity(op_lgt_from)
        scene.add(moving)
        try:
            frames_to = G_to.get("extras", {}).get("outer_frames", [])
        except Exception:
            frames_to = []
        try:
            frames_from = G_from.get("extras", {}).get("outer_frames", [])
        except Exception:
            frames_from = []
        try:
            if frames_from:
                scene.bring_to_front(*frames_from)
            if frames_to:
                scene.bring_to_front(*frames_to)
        except Exception:
            pass
        try:
            scene.bring_to_front(
                G_to["groups"]["lgt_bd_hl"],
                G_to["groups"]["btn_bd_hl"],
                G_from["groups"]["lgt_bd_hl"],
                G_from["groups"]["btn_bd_hl"],
            )
        except Exception:
            pass
        scene.play(
            moving.animate.move_to(m_target.get_center()).set_opacity(0.0),
            m_target.animate.set_opacity(target_op),
            run_time=rt,
        )
        try:
            scene.remove(moving)
        except Exception:
            pass
    else:
        m_target.set_opacity(target_op)

    if do_hl:
        if color_from is not None:
            del_cells(scene, [G_from], which="btn", indices=[(sx, sy)], rt=rt)
        if color_to is not None and 0 <= tx < w_btn_to and 0 <= ty < h_btn_to:
            del_cells(scene, [G_to], which="btn", indices=[(tx, ty)], rt=rt)

def hl_objs(scene, objs, color=HL_COLOR_1, width=BD_W_SEL, buff=0.06, rt=0.3):
    stack = [objs]
    targets, seen = [], set()
    while stack:
        cur = stack.pop()
        if cur is None:
            continue
        if isinstance(cur, (list, tuple)):
            stack.extend(cur)
        elif isinstance(cur, Mobject):
            i = id(cur)
            if i not in seen:
                seen.add(i)
                targets.append(cur)
    if not targets:
        return []
    targets.reverse()
    frames = []
    for m in targets:
        fr = SurroundingRectangle(m, buff=buff)
        fr.set_fill(opacity=0)
        fr.set_stroke(color, width, 1)
        frames.append(fr)
    grp = VGroup(*frames)
    scene.add(grp)
    if rt and rt > 0:
        scene.play(ShowCreation(grp), run_time=rt)
    return frames

def del_hl_objs(scene, frames, rt=0.3):
    stack = [frames]
    flat, seen = [], set()
    while stack:
        cur = stack.pop()
        if cur is None:
            continue
        if isinstance(cur, (list, tuple)):
            stack.extend(cur)
        elif isinstance(cur, Mobject):
            i = id(cur)
            if i not in seen:
                seen.add(i)
                flat.append(cur)
    if not flat:
        return
    if rt and rt > 0:
        scene.play(*[FadeOut(f) for f in flat], run_time=rt)
    try:
        scene.remove(*flat)
    except Exception:
        pass

def _queue_opacity_anim(mobj, target, anims):
    cur = mobj.get_opacity()
    if abs(cur - target) > 1e-6:
        anims.append(ApplyMethod(mobj.set_opacity, float(target)))

def press(scene, G, i, j, wait=0.0, anim=0.3, include_center=True):
    clear_all_bd(G)
    anims = []
    G["btn"][j][i] = not G["btn"][j][i]
    vis_btn=True
    if "grid_vis_btn" in G and 0<=j<len(G["grid_vis_btn"]) and 0<=i<len(G["grid_vis_btn"][0]):
        vis_btn=G["grid_vis_btn"][j][i]
    set_bd(G, "btn", i, j, True if vis_btn else False)
    if anim == 0:
        if vis_btn: G["btn_sp"][j][i].set_opacity(1.0 if G["btn"][j][i] else 0.0)
    else:
        if vis_btn: _queue_opacity_anim(G["btn_sp"][j][i], 1.0 if G["btn"][j][i] else 0.0, anims)
    w = G["params"]["w"]
    h = G["params"]["h"]
    cells = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    if include_center:
        cells.insert(0, (i, j))
    for x, y in cells:
        if 0 <= x < w and 0 <= y < h:
            G["lgt"][y][x] = not G["lgt"][y][x]
            vis_lgt=True
            if "grid_vis_lgt" in G and 0<=y<len(G["grid_vis_lgt"]) and 0<=x<len(G["grid_vis_lgt"][0]):
                vis_lgt=G["grid_vis_lgt"][y][x]
            set_bd(G, "lgt", x, y, True if vis_lgt else False)
            if anim == 0:
                if vis_lgt: G["lgt_sp"][y][x].set_opacity(1.0 if G["lgt"][y][x] else 0.0)
            else:
                if vis_lgt: _queue_opacity_anim(G["lgt_sp"][y][x], 1.0 if G["lgt"][y][x] else 0.0, anims)
    if anim != 0 and anims:
        scene.play(*anims, run_time=anim)
    if wait > 0:
        scene.wait(wait)

def press_rev(scene, G, i, j, wait=0.0, anim=0.3, include_center=True):
    clear_all_bd(G)
    anims=[]
    G["lgt"][j][i]=not G["lgt"][j][i]
    vis_lgt=True
    if "grid_vis_lgt" in G and 0<=j<len(G["grid_vis_lgt"]) and 0<=i<len(G["grid_vis_lgt"][0]):
        vis_lgt=G["grid_vis_lgt"][j][i]
    set_bd(G,"lgt",i,j,True if vis_lgt else False)
    if anim==0:
        if vis_lgt: G["lgt_sp"][j][i].set_opacity(1.0 if G["lgt"][j][i] else 0.0)
    else:
        if vis_lgt: _queue_opacity_anim(G["lgt_sp"][j][i],1.0 if G["lgt"][j][i] else 0.0,anims)
    w=G["params"]["w"]
    h=G["params"]["h"]
    cells=[(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
    if include_center:
        cells.insert(0,(i,j))
    for x,y in cells:
        if 0<=x<w and 0<=y<h:
            G["btn"][y][x]=not G["btn"][y][x]
            vis_btn=True
            if "grid_vis_btn" in G and 0<=y<len(G["grid_vis_btn"]) and 0<=x<len(G["grid_vis_btn"][0]):
                vis_btn=G["grid_vis_btn"][y][x]
            set_bd(G,"btn",x,y,True if vis_btn else False)
            if anim==0:
                if vis_btn: G["btn_sp"][y][x].set_opacity(1.0 if G["btn"][y][x] else 0.0)
            else:
                if vis_btn: _queue_opacity_anim(G["btn_sp"][y][x],1.0 if G["btn"][y][x] else 0.0,anims)
    if anim!=0 and anims:
        scene.play(*anims,run_time=anim)
    if wait>0:
        scene.wait(wait)

def press_lgt(lgt, x, y):
    H = len(lgt)
    W = len(lgt[0])
    for (xx, yy) in [(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
        if 0 <= xx < W and 0 <= yy < H:
            lgt[yy][xx] ^= 1

def apply_mat(scene, G, MAT, anim=0.1, clear_end=True):
    h = len(MAT)
    w = len(MAT[0]) if h > 0 else 0
    for j in range(h):
        for i in range(w):
            if MAT[j][i] == 1:
                press(scene, G, i, j, wait=0, anim=anim)
    if clear_end:
        clear_all_bd(G)

def set_grid_mats(scene, grids, mat=None, mat_l=None, rt=0.3, clear_first=True, keep_border=True, reset_state=True):
    if isinstance(grids, dict):
        gs = [[grids]]
    elif isinstance(grids, (list, tuple)):
        gs = grids if isinstance(grids[0], (list, tuple)) else [grids]
    else:
        gs = [[grids]]
    def _norm_mats(m):
        if m is None:
            return None
        if isinstance(m[0][0], (list, tuple)):
            return m
        out = []
        for row in gs:
            out.append([m for _ in row])
        return out
    mats_btn = _norm_mats(mat)
    mats_lgt = _norm_mats(mat_l)
    if clear_first:
        del_grids(scene, gs, kp_bd=keep_border, reset_state=reset_state)
    anims = []
    for y in range(len(gs)):
        for x in range(len(gs[y])):
            G = gs[y][x]
            p = G["params"]
            h_b, w_b = p["h"], p["w"]
            h_l, w_l = p.get("h_l", h_b), p.get("w_l", w_b)
            btn_mat = mats_btn[y][x] if mats_btn is not None else None
            lgt_mat = mats_lgt[y][x] if mats_lgt is not None else None
            if lgt_mat is not None:
                lh = len(lgt_mat)
                lw = len(lgt_mat[0]) if lh > 0 else 0
                H2 = min(h_l, lh)
                W2 = min(w_l, lw)
                for j in range(h_l):
                    for i in range(w_l):
                        new_v = G["lgt"][j][i]
                        if j < H2 and i < W2:
                            raw = lgt_mat[j][i]
                            try:
                                v = int(raw)
                            except Exception:
                                v = 1 if raw else 0
                            if v <= -1:
                                pass
                            else:
                                new_v = bool(v)
                        if new_v != G["lgt"][j][i]:
                            G["lgt"][j][i] = new_v
                            vis = True
                            if "grid_vis_lgt" in G and 0 <= j < len(G["grid_vis_lgt"]) and 0 <= i < len(G["grid_vis_lgt"][0]):
                                vis = G["grid_vis_lgt"][j][i]
                            target = 1.0 if (new_v and vis) else 0.0
                            _queue_opacity_anim(G["lgt_sp"][j][i], target, anims)
            if btn_mat is not None:
                mh = len(btn_mat)
                mw = len(btn_mat[0]) if mh > 0 else 0
                H = min(h_b, mh)
                W = min(w_b, mw)
                for j in range(h_b):
                    for i in range(w_b):
                        new_v = G["btn"][j][i]
                        if j < H and i < W:
                            raw = btn_mat[j][i]
                            try:
                                v = int(raw)
                            except Exception:
                                v = 1 if raw else 0
                            if v <= -1:
                                pass
                            else:
                                new_v = bool(v)
                        if new_v != G["btn"][j][i]:
                            G["btn"][j][i] = new_v
                            vis = True
                            if "grid_vis_btn" in G and 0 <= j < len(G["grid_vis_btn"]) and 0 <= i < len(G["grid_vis_btn"][0]):
                                vis = G["grid_vis_btn"][j][i]
                            target = 1.0 if (new_v and vis) else 0.0
                            _queue_opacity_anim(G["btn_sp"][j][i], target, anims)
    if anims:
        scene.play(*anims, run_time=rt)

def del_grids(scene, grids, rt=0.3, kp_bd=False, reset_state=True):
    def _flatten(x):
        out, st = [], [x]
        while st:
            it = st.pop()
            if it is None:
                continue
            if isinstance(it, dict) and "groups" in it:
                out.append(it)
            elif isinstance(it, (list, tuple)):
                st.extend(it)
        return out
    def _present_set():
        s = set()
        for top in scene.mobjects:
            for m in top.get_family():
                s.add(m)
        return s
    gs = _flatten(grids)
    if not gs:
        return
    pres = _present_set()
    if kp_bd:
        fades = []
        for G in gs:
            p = G["params"]
            h_b, w_b = p["h"], p["w"]
            h_l, w_l = p.get("h_l", h_b), p.get("w_l", w_b)
            for j in range(h_l):
                for i in range(w_l):
                    G["lgt_bd_hl"][j][i].set_stroke(opacity=0)
            for j in range(h_b):
                for i in range(w_b):
                    G["btn_bd_hl"][j][i].set_stroke(opacity=0)
            for k in ("lgt_sp", "btn_sp"):
                m = G["groups"][k]
                if m in pres:
                    fades.append(ApplyMethod(m.set_opacity, 0.0))
        if rt > 0 and fades:
            scene.play(*fades, run_time=rt)
        if reset_state:
            for G in gs:
                p = G["params"]
                h_b, w_b = p["h"], p["w"]
                h_l, w_l = p.get("h_l", h_b), p.get("w_l", w_b)
                for j in range(h_l):
                    for i in range(w_l):
                        G["lgt"][j][i] = False
                        G["lgt_sel"][j][i] = False
                for j in range(h_b):
                    for i in range(w_b):
                        G["btn"][j][i] = False
                        G["btn_sel"][j][i] = False
        return
    targets = []
    for G in gs:
        gr = G["groups"]
        cands = [gr["lgt_sp"], gr["btn_sp"], gr["lgt_bd_hl"], gr["lgt_bd_base"], gr["btn_bd_hl"], gr["btn_bd_base"]]
        cands += G.get("extras", {}).get("outer_frames", [])
        for c in cands:
            if c is None:
                continue
            for m in c.get_family():
                if m in pres:
                    targets.append(m)
    if not targets:
        return
    kill = VGroup(*dict.fromkeys(targets))
    if rt > 0:
        scene.play(FadeOut(kill, run_time=rt))
    try:
        scene.remove(kill)
    except Exception:
        pass
    if reset_state:
        for G in gs:
            p = G["params"]
            h_b, w_b = p["h"], p["w"]
            h_l, w_l = p.get("h_l", h_b), p.get("w_l", w_b)
            for j in range(h_l):
                for i in range(w_l):
                    G["lgt"][j][i] = False
                    G["lgt_sel"][j][i] = False
            for j in range(h_b):
                for i in range(w_b):
                    G["btn"][j][i] = False
                    G["btn_sel"][j][i] = False
            G["groups"]["lgt_bd_base"].set_stroke(opacity=0)
            G["groups"]["btn_bd_base"].set_stroke(opacity=0)

def del_labels(scene, *labels, rt=0.3):
    grp = VGroup(*labels)
    scene.play(FadeOut(grp, run_time=rt))
    try:
        scene.remove(grp)
    except Exception:
        pass

def _iter_grids(grids):
    if isinstance(grids, dict):
        yield grids
    elif isinstance(grids, (list, tuple)):
        for g in grids:
            yield from _iter_grids(g)

def set_all_lights(scene, grids, on=True, rt=0.3, clear_highlight=True):
    anims = []
    for G in _iter_grids(grids):
        if clear_highlight:
            clear_all_bd(G)
        h = G["params"]["h"]
        w = G["params"]["w"]
        for j in range(h):
            for i in range(w):
                if on:
                    if not G["lgt"][j][i]:
                        G["lgt"][j][i] = True
                        _queue_opacity_anim(G["lgt_sp"][j][i], 1.0, anims)
                else:
                    if G["lgt"][j][i]:
                        G["lgt"][j][i] = False
                        _queue_opacity_anim(G["lgt_sp"][j][i], 0.0, anims)
    if anims:
        scene.play(*anims, run_time=rt)

def mul_vec_mat_begin(scene, mat, vec, mat_color=I_COLOR, vec_color=Y_COLOR, res_color=X_COLOR, sz=0.4, w=None, h=None, mat_label=None, vec_label=None, res_label=None):
    if h is None: h = len(vec)
    if w is None: w = len(vec) if h>0 else 0
    grid_M = make_grid(scene, w, h, mat_l=mat, btn_c=mat_color, lgt_c=mat_color, sz=sz)
    mat_label_obj = None
    if mat_label is not None:
        if isinstance(mat_label, (list, tuple)):
            labels = mat_label
        else:
            labels = [""] * w
            labels[w // 2] = mat_label
        mat_label_obj = add_top_labels(scene, grid_M, labels, which="btn", dy=0.4)
    left_obj = add_left_labels(scene, grid_M, list(range(h)), which="btn", dx=0.4)
    ctx = {
        "mat":mat,
        "vec":vec,
        "mat_color":mat_color,
        "vec_color":vec_color,
        "res_color":res_color,
        "sz":sz,
        "h":h,
        "w":w,
        "grid_M":grid_M,
        "left_obj":left_obj,
        "mat_label":mat_label,
        "vec_label":vec_label,
        "res_label":res_label,
        "mat_label_obj":mat_label_obj,
    }
    return ctx

def mul_vec_mat_vec_and_rows(scene, ctx):
    h = ctx["h"]
    w = ctx["w"]
    mat = ctx["mat"]
    vec = ctx["vec"]
    sz = ctx["sz"]
    vec_color = ctx["vec_color"]
    grid_V1 = make_grid(scene, h, 1, mat_l=[vec], btn_y=-2, lgt_y=-2, btn_c=vec_color, lgt_c=vec_color, sz=sz)
    grid_V2 = make_grid(scene, 1, h, mat_l=[[v] for v in vec], btn_x=-2, lgt_x=-2, btn_c=vec_color, lgt_c=vec_color, sz=sz, show=False)
    trans_grid(scene, grid_V1, grid_V2)
    vec_label_obj = None
    if ctx.get("vec_label") is not None:
        labels = ctx["vec_label"] if isinstance(ctx["vec_label"], (list, tuple)) else [ctx["vec_label"]]
        vec_label_obj = add_top_labels(scene, grid_V2, labels, which="btn", dy=0.4)
    vh_grids = []
    bd_list = []
    for i in range(h):
        if not vec[i]:
            continue
        y = sz * ((h - 1) / 2 - i)
        g = make_grid(scene, w, 1, mat_l=[mat[i]], btn_y=y, lgt_y=y, btn_c=vec_color, lgt_c=vec_color, sz=sz, rt=0.15)
        vh_grids.append(g)
    ctx["grid_V2"] = grid_V2
    ctx["vh_grids"] = vh_grids
    ctx["bd_list"] = bd_list
    ctx["vec_label_obj"] = vec_label_obj
    return ctx

def mul_vec_mat_accumulate(scene, ctx):
    w = ctx["w"]
    sz = ctx["sz"]
    res_color = ctx["res_color"]
    grid_res = make_grid(scene, w, 1, mat_l=[[0] * w], btn_y=-2, lgt_y=-2, btn_c=res_color, lgt_c=res_color, sz=sz)
    res_label_obj = None
    if ctx.get("res_label") is not None:
        labels = ctx["res_label"] if isinstance(ctx["res_label"], (list, tuple)) else [ctx["res_label"]]
        res_label_obj = add_left_labels(scene, grid_res, labels, which="btn", dx=0.4)
    ctx["grid_res"] = grid_res
    ctx["res_label_obj"] = res_label_obj
    vh_grids = ctx["vh_grids"]
    bd_list = ctx["bd_list"]
    grid_res = ctx["grid_res"]
    for i in range(len(vh_grids)):
        add_grid(scene, vh_grids[i], grid_res, keep_from=False, rt=0.3)
    return grid_res

def mul_vec_mat_cleanup(scene, ctx, clear_res=True):
    grids = [ctx["grid_M"], ctx["grid_V2"]] + ctx["vh_grids"]
    if clear_res:
        grids.append(ctx["grid_res"])
    del_left_labels(scene, ctx["left_obj"])
    if ctx.get("mat_label_obj"):
        del_top_labels(scene, ctx["mat_label_obj"])
    if ctx.get("vec_label_obj"):
        del_top_labels(scene, ctx["vec_label_obj"])
    if ctx.get("res_label_obj"):
        del_left_labels(scene, ctx["res_label_obj"])
    del_grids(scene, grids)

def mul_vec_mat(scene, mat, vec, mat_color=I_COLOR, vec_color=Y_COLOR, res_color=X_COLOR, sz=0.4, w=None, h=None, mat_label=None, vec_label=None, res_label=None, wait=1.0):
    ctx = mul_vec_mat_begin(scene, mat, vec, mat_color, vec_color, res_color, sz, w=w, h=h, mat_label=mat_label, vec_label=vec_label, res_label=res_label)
    mul_vec_mat_vec_and_rows(scene, ctx)
    mul_vec_mat_accumulate(scene, ctx)
    scene.wait(wait)
    mul_vec_mat_cleanup(scene, ctx, clear_res=True)
    return ctx

def _split_inline_math(s):
    parts = []
    buf = ""
    m = False
    esc = False
    for ch in s:
        if esc:
            if ch == "$":
                buf += "$"
            else:
                buf += "\\" + ch
            esc = False
            continue
        if ch == "\\":
            esc = True
            continue
        if ch == "$":
            if m:
                parts.append(("tex", buf))
                buf = ""
                m = False
            else:
                if buf:
                    parts.append(("text", buf))
                buf = ""
                m = True
        else:
            buf += ch
    if buf:
        parts.append(("tex" if m else "text", buf))
    return parts

def _parse_color_segments(line, color_map, default_color):
    if not color_map:
        return [(line, default_color)]
    segs = []
    buf = ""
    cur_color = default_color
    i = 0
    n = len(line)
    changed = False
    while i < n:
        ch = line[i]
        if ch == "<":
            j = line.find(">", i + 1)
            if j != -1:
                tag = line[i + 1:j].strip()
                if tag in color_map:
                    if buf:
                        segs.append((buf, cur_color))
                        buf = ""
                    cur_color = color_map[tag]
                    changed = True
                    i = j + 1
                    continue
            buf += ch
            i += 1
        else:
            buf += ch
            i += 1
    if buf:
        segs.append((buf, cur_color))
    if not changed:
        return [(line, default_color)]
    return segs

def normalize_by_ref(objs, factor, ref_tex=REF_TEX, scene=None, text_desc=None):
    try:
        ref = Tex(ref_tex)
        ref.scale(1)
        h_ref = float(ref.get_height())
    except Exception:
        h_ref = 0.0
    if h_ref <= 1e-6:
        return
    target = h_ref * factor
    for o in objs:
        try:
            h = float(o.get_height())
        except Exception:
            h = 0.0
        if h > 1e-6:
            before = h
            s = target / h
            if abs(s - 1.0) > 1e-3:
                o.scale(s)
                try:
                    after = float(o.get_height())
                except Exception:
                    after = before * s
            else:
                after = before
            try:
                ts = _fmt_scene_time_ms(scene) if scene is not None else "00:00:00.000"
                txt = "" if text_desc is None else str(text_desc).replace("\n", " ")
                with open("normal.txt", "a", encoding="utf-8") as f:
                    f.write(f"{ts} {before:.6f} {after:.6f} {txt}\n")
            except Exception:
                pass

def _mk_line_group_color(line, font, size, default_color, baseline, auto_k, ref_tex, color_map):
    segs = _parse_color_segments(line, color_map, default_color)
    if len(segs) == 1 and segs[0][1] == default_color and "<" not in line:
        return _mk_line_group(line, font, size, default_color, baseline, auto_k, ref_tex)
    if "$" not in line:
        scale = size / FONT_SIZE_DEFAULT
        text = "".join(t for t, c in segs)
        m = Text(text, font=font)
        m.scale(scale)
        m.set_color(default_color)
        char_count = len(text)
        glyph_count = len(m)
        if glyph_count == char_count:
            idx = 0
            for t, c in segs:
                if not t:
                    continue
                if c != default_color:
                    for k in range(len(t)):
                        m[idx + k].set_color(c)
                idx += len(t)
        else:
            for t, c in segs:
                if c != default_color and t:
                    m.set_color_by_text(t, c)
        return m
    parts = []
    for txt, col in segs:
        if not txt:
            continue
        g = _mk_line_group(txt, font, size, col, baseline, auto_k, ref_tex)
        parts.append(g)
    if not parts:
        return _mk_line_group("", font, size, default_color, baseline, auto_k, ref_tex)
    return VGroup(*parts).arrange(RIGHT, buff=0.0, aligned_edge=DOWN)

def _mk_line_group(s, font, size, color, baseline=0.0, auto_k=0.5, ref_tex=REF_TEX):
    segs = _split_inline_math(s)
    scale = size / FONT_SIZE_DEFAULT
    if not segs:
        m = Text("", font=font)
        m.set_color(color)
        m.scale(scale)
        return m
    objs, tags = [], []
    for k, v in segs:
        if k == "tex":
            m = Tex(v)
            m.set_color(color)
            m.scale(scale)
            objs.append(m)
            tags.append("tex")
        else:
            m = Text(v, font=font)
            m.set_color(color)
            m.scale(scale)
            objs.append(m)
            tags.append("text")
    grp = VGroup(*objs).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
    text_bottoms = [o.get_bottom()[1] for o, t in zip(objs, tags) if t == "text"]
    if text_bottoms:
        ref = min(text_bottoms)
        h_ref = Tex(ref_tex).scale(scale).get_height() if auto_k else 0.0
        for o, t in zip(objs, tags):
            if t == "tex":
                dy = (ref - o.get_bottom()[1]) + baseline * scale
                if auto_k:
                    dy -= auto_k * (o.get_height() - h_ref)
                if abs(dy) > 1e-6:
                    o.shift(UP * dy)
    return grp

def _fmt_scene_time_ms(scene):
    t = 0.0
    try:
        if hasattr(scene, "time"):
            t = float(scene.time)
        elif hasattr(scene, "renderer") and hasattr(scene.renderer, "time"):
            t = float(scene.renderer.time)
        elif hasattr(scene, "renderer") and hasattr(scene.renderer, "get_time"):
            t = float(scene.renderer.get_time())
    except Exception:
        t = 0.0
    ms = int(round(t * 1000))
    s = ms // 1000
    ms = ms % 1000
    h = s // 3600
    m = (s % 3600) // 60
    s = s % 60
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

def show_subtitle(scene, text, text2=None, run_in=0.3, run_out=0.3, font=DEFAULT_FONT, font_size=FONT_SIZE_DEFAULT, line_gap=0.2, buff=0.5, baseline=0.05, auto_k=0.5, ref_tex=REF_TEX):
    old=getattr(scene,"_subtitle_mobj", getattr(scene,"_subtitle_", None))
    if old is not None:
        scene.play(FadeOut(old, run_time=run_out))
        try:
            scene.remove(old)
        except Exception:
            pass
        scene._subtitle_mobj = None
    parts = []
    if isinstance(text, (list, tuple)):
        parts = [str(x) for x in text]
    else:
        if text is not None:
            parts.append(str(text))
        if text2 is not None:
            parts.append(str(text2))
    parts = [p for p in parts if p is not None]
    if len(parts) == 0 or all(p == "" for p in parts):
        return None
    out_text = "".join(parts)
    try:
        with open("subtitle.txt", "a", encoding="utf-8") as f:
            f.write(f"{_fmt_scene_time_ms(scene)} {out_text}\n")
    except Exception:
        pass
    lines = VGroup(*[_mk_line_group(p, font, font_size, WHITE, baseline, auto_k, ref_tex) for p in parts])
    normalize_by_ref(lines.submobjects, SCALE_SUBTITLE * font_size / FONT_SIZE_DEFAULT, ref_tex, scene=scene, text_desc=out_text)
    lines.arrange(DOWN, buff=line_gap).to_edge(DOWN, buff=buff)
    scene.add(lines)
    scene.play(FadeIn(lines, run_time=run_in))
    scene._subtitle_mobj = lines
    scene._subtitle_ = lines
    return lines

def show_title(scene, line1=None, line2=None, run_in=0.3, run_out=0.3, font=DEFAULT_FONT, size1=FONT_SIZE_LARGE, size2=FONT_SIZE_DEFAULT, line_gap=0.15, buff=0.5, pause=0.8, rt=0.3, ref_tex=REF_TEX):
    show_subtitle(scene, "")
    old = getattr(scene, "_title_mobj", None)
    if old is not None:
        scene.play(FadeOut(old, run_time=run_out))
        try:
            scene.remove(old)
        except Exception:
            pass
        scene._title_mobj = None
    parts = []
    if isinstance(line1, (list, tuple)):
        parts = [str(x) for x in line1][:2]
    else:
        if line1 is not None:
            parts.append(str(line1))
        if line2 is not None:
            parts.append(str(line2))
    parts = [p for p in parts if p is not None]
    if len(parts) == 0 or all(p == "" for p in parts):
        return None
    out_text = "".join(parts)
    try:
        with open("title.txt", "a", encoding="utf-8") as f:
            f.write(f"{_fmt_scene_time_ms(scene)} {out_text}\n")
    except Exception:
        pass
    objs = []
    if len(parts) >= 1 and parts[0] != "":
        t1 = _mk_line_group(parts[0], font, size1, WHITE)
        normalize_by_ref([t1], SCALE_TITLE * size1 / FONT_SIZE_LARGE, ref_tex, scene=scene, text_desc=parts[0])
        objs.append(t1)
    if len(parts) >= 2 and parts[1] != "":
        t2 = _mk_line_group(parts[1], font, size2, WHITE)
        normalize_by_ref([t2], SCALE_TITLE * size2 / FONT_SIZE_DEFAULT, ref_tex, scene=scene, text_desc=parts[1])
        objs.append(t2)
    if not objs:
        return None
    grp = VGroup(*objs).arrange(DOWN, buff=line_gap)
    grp.move_to(ORIGIN)
    scene.add(grp)
    scene.play(FadeIn(grp, run_time=run_in))
    scene.wait(pause)
    scene.play(ApplyMethod(grp.to_edge, UP, buff), run_time=rt)
    scene._title_mobj = grp
    return grp

def show_latex(scene, text, x=0.0, y=0.0, run_in=0.3, run_out=0.3, font=DEFAULT_FONT, font_size=32, buff=0.5, line_gap=0.1, baseline=0.0, auto_k=0.5, ref_tex=REF_TEX, show=True, color_map=COLOR_MAP, default_color=WHITE, add_tex=ADD_TEX):
    parts = []
    if isinstance(text, (list, tuple)):
        parts = [str(p) for p in text if p is not None]
    else:
        if text is None:
            return None
        s = str(text)
        if "<br" in s:
            s = s.replace("<br/>", "<br>").replace("<br />", "<br>")
            s = s.replace("\n", "<br>")
            parts = s.split("<br>")
        else:
            parts = s.split("\n")
    parts = [p for p in parts if p is not None]
    if len(parts) == 0 or all(p == "" for p in parts):
        return None
    if isinstance(text, (list, tuple)):
        text_desc = "".join(str(p) for p in text if p is not None)
    else:
        text_desc = "" if text is None else str(text)
    wrapped_parts = []
    for p in parts:
        wrapped_parts.append(f"{add_tex}{p}{add_tex}")
    parts = wrapped_parts
    lines = VGroup(*[_mk_line_group_color(p, font, font_size, default_color, baseline, auto_k, ref_tex, color_map) for p in parts])
    h0 = 0.0
    for line in lines.submobjects:
        try:
            h_line = float(line.get_height())
        except Exception:
            h_line = 0.0
        if h_line > h0:
            h0 = h_line
    normalize_by_ref(lines.submobjects, SCALE_LATEX * font_size / 32, ref_tex, scene=scene, text_desc=text_desc)
    h1 = 0.0
    for line in lines.submobjects:
        try:
            h_line = float(line.get_height())
        except Exception:
            h_line = 0.0
        if h_line > h1:
            h1 = h_line
    lines.arrange(DOWN, buff=line_gap, aligned_edge=LEFT)
    lines.move_to(ORIGIN)
    lines.shift(RIGHT * x + UP * y)
    try:
        if isinstance(text, (list, tuple)):
            raw_text = "".join(str(p) for p in text if p is not None)
        else:
            raw_text = "" if text is None else str(text)
        raw_text = raw_text.replace("<br/>", "")
        raw_text = raw_text.replace("<br />", "")
        raw_text = raw_text.replace("<br>", "")
        s = raw_text
        res = []
        i = 0
        n = len(s)
        while i < n:
            ch = s[i]
            if ch == "<" and i + 2 < n and s[i + 1] == "c":
                j = i + 2
                while j < n and s[j] != ">":
                    j += 1
                if j < n:
                    i = j + 1
                    continue
            res.append(ch)
            i += 1
        raw_clean = "".join(res)
        if raw_clean.strip():
            with open("latex.txt", "a", encoding="utf-8") as f:
                f.write(f"{_fmt_scene_time_ms(scene)} {h0:.6f} {h1:.6f} {raw_clean}\n")
    except Exception:
        pass
    if not show or scene is None:
        return lines
    scene.add(lines)
    if run_in > 0:
        scene.play(FadeIn(lines, run_time=run_in))
    scene._latex_mobj = lines
    stack = getattr(scene, "_latex_stack", None)
    if stack is None:
        stack = []
        setattr(scene, "_latex_stack", stack)
    stack.append(lines)
    return lines

def trans_latex(scene, latex_from, latex_to, rt=0.8):
    if latex_from is None or latex_to is None:
        return None
    scene.play(ReplacementTransform(latex_from, latex_to), run_time=rt)
    stack = getattr(scene, "_latex_stack", None)
    if stack is None:
        stack = []
        setattr(scene, "_latex_stack", stack)
    if latex_from in stack:
        stack.remove(latex_from)
    if latex_to not in stack:
        stack.append(latex_to)
    if getattr(scene, "_latex_mobj", None) is latex_from:
        scene._latex_mobj = latex_to
    return latex_to

def del_latex(scene, *objs, run_out=0.3):
    if not objs:
        m = getattr(scene, "_latex_mobj", None)
        if m is None:
            return
        objs = (m,)
    flat, seen = [], set()
    for o in objs:
        if o is None:
            continue
        if isinstance(o, (list, tuple)):
            for t in o:
                if t is None:
                    continue
                if id(t) in seen:
                    continue
                flat.append(t)
                seen.add(id(t))
        else:
            if id(o) in seen:
                continue
            flat.append(o)
            seen.add(id(o))
    stack = getattr(scene, "_latex_stack", [])
    for m in flat:
        if run_out > 0:
            scene.play(FadeOut(m, run_time=run_out))
        try:
            scene.remove(m)
        except Exception:
            pass
        if m in stack:
            stack.remove(m)
        if getattr(scene, "_latex_mobj", None) is m:
            setattr(scene, "_latex_mobj", stack[-1] if stack else None)

def add_grid_labels(scene, G, labels2d, which="lgt", font=DEFAULT_FONT, scale=0.6, rt=0.3, ref_tex=REF_TEX):
    grp = "lgt_bd_base" if which == "lgt" else "btn_bd_base"
    cells = G.get(grp, None)
    if not cells:
        return []
    H, W = len(cells), len(cells[0])
    R = min(H, len(labels2d))
    objs2d = [[None for _ in range(W)] for _ in range(H)]
    created = []

    for r in range(R):
        row_labels = labels2d[r] or []
        C = min(W, len(row_labels))
        for c in range(C):
            s = row_labels[c]
            if s is None or s == "":
                continue
            m = Text(str(s), font=font).scale(scale)
            m.move_to(cells[r][c].get_center())
            objs2d[r][c] = m
            created.append(m)
    if created:
        scene.add(*created)
        if rt and rt > 0:
            scene.play(*[FadeIn(o) for o in created], run_time=rt)
    return objs2d

def add_top_labels(scene, G, labels, which="lgt", font=DEFAULT_FONT, scale=0.6, dy=None, rt=0.3, ref_tex=REF_TEX):
    grp = "lgt_bd_base" if which == "lgt" else "btn_bd_base"
    cells = G[grp]
    if not cells:
        return []
    W = len(cells[0])
    sz = G["params"]["sz"]
    shift = dy if dy is not None else sz
    n = min(W, len(labels))
    objs = []
    for i in range(n):
        s = str(labels[i])
        m = Text(s, font=font)
        pos = cells[0][i].get_center() + UP * shift
        m.move_to(pos)
        objs.append(m)
    text_desc = " ".join(str(labels[i]) for i in range(n))
    normalize_by_ref(objs, scale, ref_tex, scene=scene, text_desc=text_desc)
    if objs:
        scene.add(*objs)
        if rt and rt > 0:
            scene.play(*[FadeIn(o) for o in objs], run_time=rt)
    return objs

def add_left_labels(scene, G, labels, which="lgt", font=DEFAULT_FONT, scale=0.6, dx=None, rt=0.3, ref_tex=REF_TEX):
    grp = "lgt_bd_base" if which == "lgt" else "btn_bd_base"
    cells = G[grp]
    if not cells:
        return []
    H = len(cells)
    sz = G["params"]["sz"]
    shift = dx if dx is not None else sz
    n = min(H, len(labels))
    objs = []
    for j in range(n):
        s = str(labels[j])
        m = Text(s, font=font)
        pos = cells[j][0].get_center() + LEFT * shift
        m.move_to(pos)
        objs.append(m)
    text_desc = " ".join(str(labels[j]) for j in range(n))
    normalize_by_ref(objs, scale, ref_tex, scene=scene, text_desc=text_desc)
    if objs:
        scene.add(*objs)
        if rt and rt > 0:
            scene.play(*[FadeIn(o) for o in objs], run_time=rt)
    return objs

def add_bottom_label(scene, G, label, which="lgt", font=DEFAULT_FONT, scale=0.6, dy=None, rt=0.3, ref_tex=REF_TEX, color=WHITE):
    grp = "lgt_bd_base" if which == "lgt" else "btn_bd_base"
    cells = G[grp]
    if not cells:
        return []
    W = len(cells[0])
    sz = G["params"]["sz"]
    shift = dy if dy is not None else sz
    idx = W // 2
    s = str(label)
    m = Text(s, font=font)
    m.set_color(color)
    pos = cells[-1][idx].get_center() + DOWN * shift + LEFT * (sz / 2.0)
    m.move_to(pos)
    objs = [m]
    normalize_by_ref(objs, scale, ref_tex, scene=scene, text_desc=s)
    scene.add(*objs)
    if rt and rt > 0:
        scene.play(*[FadeIn(o) for o in objs], run_time=rt)
    return objs

def del_grid_labels(scene, objs2d, rt=0.3):
    try:
        del_top_labels(scene, objs2d, rt=rt)
        return
    except NameError:
        pass
    stack, flat, seen = [objs2d], [], set()
    while stack:
        cur = stack.pop()
        if cur is None:
            continue
        if isinstance(cur, (list, tuple)):
            stack.extend(cur)
        elif isinstance(cur, Mobject):
            i = id(cur)
            if i not in seen:
                seen.add(i)
                flat.append(cur)
    if not flat:
        return
    try:
        scene.play(*[FadeOut(o) for o in flat], run_time=rt)
    except Exception:
        pass
    try:
        scene.remove(*flat)
    except Exception:
        pass

def del_top_labels(scene, objs, rt=0.3):
    stack = [objs]
    flat, seen = [], set()
    while stack:
        cur = stack.pop()
        if cur is None:
            continue
        if isinstance(cur, (list, tuple)):
            stack.extend(cur)
        elif isinstance(cur, Mobject):
            i = id(cur)
            if i not in seen:
                seen.add(i)
                flat.append(cur)
    if not flat:
        return
    try:
        scene.play(*[FadeOut(o) for o in flat], run_time=rt)
    except Exception:
        pass
    try:
        scene.remove(*flat)
    except Exception:
        pass

def del_left_labels(scene, objs, rt=0.3):
    stack = [objs]
    flat, seen = [], set()
    while stack:
        cur = stack.pop()
        if cur is None:
            continue
        if isinstance(cur, (list, tuple)):
            stack.extend(cur)
        elif isinstance(cur, Mobject):
            i = id(cur)
            if i not in seen:
                seen.add(i)
                flat.append(cur)
    if not flat:
        return
    try:
        scene.play(*[FadeOut(o) for o in flat], run_time=rt)
    except Exception:
        pass
    try:
        scene.remove(*flat)
    except Exception:
        pass

def del_bottom_label(scene, objs, rt=0.3):
    stack = [objs]
    flat, seen = [], set()
    while stack:
        cur = stack.pop()
        if cur is None:
            continue
        if isinstance(cur, (list, tuple)):
            stack.extend(cur)
        elif isinstance(cur, Mobject):
            i = id(cur)
            if i not in seen:
                seen.add(i)
                flat.append(cur)
    if not flat:
        return
    try:
        scene.play(*[FadeOut(o) for o in flat], run_time=rt)
    except Exception:
        pass
    try:
        scene.remove(*flat)
    except Exception:
        pass

def show_center_latex(
    scene,
    latex_blocks,
    run_in=0.8,
    line_buff=0.20,
    inner_line_buff=0.10,
    hbuff=0.18,
    group_scale=0.82,
    align_left=True,
    default_indent=1.0,
    font=DEFAULT_FONT,
    shift_x=0.0,
    shift_y=0.0,
    replace_old=True
):
    def _sanitize_tex(s: str) -> str:
        s = s.replace(r"\left(", "(").replace(r"\right)", ")")
        s = s.replace(r"\left[", "[").replace(r"\right]", "]")
        s = s.replace(r"\left\{", "{").replace(r"\right\}", "}")
        s = s.replace("\u00A0", " ").replace("\u202F", " ")
        return s
    rows = []
    for blk in latex_blocks:
        btype = blk.get("type", "text")
        s = float(blk.get("scale", 1.0))
        cn_s = float(blk.get("cn_scale", s*0.77))
        if btype == "tex":
            m = Tex(_sanitize_tex(blk["content"])).scale(s)
        elif btype == "tex_lines":
            lines = [Tex(_sanitize_tex(x)).scale(s) for x in blk["content"]]
            m = VGroup(*lines).arrange(DOWN, buff=inner_line_buff, aligned_edge=LEFT)
        elif btype == "tex_cn_lines":
            row_items = []
            for item in blk["content"]:
                t = Tex(_sanitize_tex(item["tex"])).scale(s)
                cn = Text(item.get("cn", ""), font=font).scale(cn_s)
                row_items.append(VGroup(t, cn).arrange(RIGHT, buff=hbuff, aligned_edge=DOWN))
            m = VGroup(*row_items).arrange(DOWN, buff=inner_line_buff, aligned_edge=LEFT)
        else:
            m = Text(blk["content"], font=font).scale(s)
        indent = float(blk.get("indent", default_indent))
        if indent != 0:
            pad = Rectangle(width=indent, height=0.001, stroke_width=0, fill_opacity=0)
            m = VGroup(pad, m).arrange(RIGHT, buff=0, aligned_edge=DOWN)
        rows.append(m)
    group = VGroup(*rows).arrange(DOWN, buff=line_buff, aligned_edge=(LEFT if align_left else ORIGIN))
    group.scale(group_scale)
    group.move_to(ORIGIN)
    group.shift(RIGHT*shift_x+UP*shift_y)
    old = getattr(scene, "_center_latex_group", None)
    if replace_old and old is not None:
        try:
            scene.play(FadeOut(old, lag_ratio=0.06, run_time=0.25))
            scene.remove(old)
        except Exception:
            pass
        lst = getattr(scene, "_center_latex_groups", None)
        if isinstance(lst, list):
            try:
                lst.remove(old)
            except Exception:
                pass
    lst = getattr(scene, "_center_latex_groups", None)
    if not isinstance(lst, list):
        lst = []
        setattr(scene, "_center_latex_groups", lst)
    lst.append(group)
    scene._center_latex_group = group
    scene.play(FadeIn(group, lag_ratio=0.08, run_time=run_in))
    return group

def remove_center_latex(scene, group=None, run_out=0.8):
    if group is None:
        lst = getattr(scene, "_center_latex_groups", None)
        if isinstance(lst, list) and lst:
            for g in list(lst):
                try:
                    scene.play(FadeOut(g, lag_ratio=0.08, run_time=run_out))
                    scene.remove(g)
                except Exception:
                    pass
            lst.clear()
        else:
            g = getattr(scene, "_center_latex_group", None)
            if g is not None:
                try:
                    scene.play(FadeOut(g, lag_ratio=0.08, run_time=run_out))
                    scene.remove(g)
                except Exception:
                    pass
        scene._center_latex_group = None
    else:
        try:
            scene.play(FadeOut(group, lag_ratio=0.08, run_time=run_out))
            scene.remove(group)
        except Exception:
            pass
        lst = getattr(scene, "_center_latex_groups", None)
        if isinstance(lst, list):
            try:
                lst.remove(group)
            except Exception:
                pass
        if getattr(scene, "_center_latex_group", None) is group:
            scene._center_latex_group = None if not getattr(scene, "_center_latex_groups", None) else (scene._center_latex_groups[-1] if scene._center_latex_groups else None)

def show_algo_table(
    scene,
    x=0.0,
    y=3.0,
    run_in=0.3,
    run_out=0.3,
    font=DEFAULT_FONT,
    font_size=FONT_SIZE_DEFAULT,
    row_gap=0.4,
    col_gap=0.6,
    baseline=0.0,
    auto_k=0.5,
    ref_tex=REF_TEX,
    show=True,
    color_map=COLOR_MAP,
    default_color=WHITE,
    header_color=WHITE,
):
    headers = ("输出", "输入", "说明", "算法", "公式")
    def make_cell(text, color, tag, is_header=False):
        if isinstance(text, str) and text.strip() == "-":
            text = ""
        if not is_header and isinstance(text, str) and text:
            text = f"{tag}{text}"
        c = header_color if is_header else color
        m = show_latex(
            scene,
            text,
            x=0,
            y=0,
            run_in=0.0,
            run_out=0.0,
            font=font,
            font_size=font_size,
            buff=0.5,
            line_gap=0.0,
            baseline=baseline,
            auto_k=auto_k,
            ref_tex=ref_tex,
            show=False,
            color_map=color_map,
            default_color=c,
            add_tex="",
        )
        if m is None:
            return VGroup()
        if isinstance(m, VGroup) and len(m.submobjects) == 1:
            m = m.submobjects[0]
        m.move_to(ORIGIN)
        return m
    header_row = [make_cell(h, default_color, "", True) for h in headers]
    data_rows = []
    for color, color_tag, out_sym, in_sym, desc, algo, formula in LATEX_MAT:
        row = [
            make_cell(out_sym,   color, color_tag),
            make_cell(in_sym,    color, color_tag),
            make_cell(desc,      color, color_tag),
            make_cell(algo,      color, color_tag),
            make_cell(formula,   color, color_tag),
        ]
        data_rows.append(row)
    all_rows = [header_row] + data_rows
    n_cols = len(headers)
    col_widths = [0.0] * n_cols
    for row in all_rows:
        for j, cell in enumerate(row):
            w = float(cell.get_width())
            if w > col_widths[j]:
                col_widths[j] = w
    table_rows = []
    for row in all_rows:
        for j, cell in enumerate(row):
            x_left = sum(col_widths[:j]) + j * col_gap
            cur_left = float(cell.get_left()[0])
            dx = x_left - cur_left
            cell.shift(RIGHT * dx)
        row_group = VGroup(*row)
        table_rows.append(row_group)
    table = VGroup(*table_rows).arrange(DOWN, buff=row_gap, aligned_edge=LEFT)
    table.move_to(ORIGIN)
    table.shift(RIGHT * x + UP * y)
    if not show or scene is None:
        return table
    scene.add(table)
    if run_in > 0:
        scene.play(FadeIn(table, run_time=run_in))
    scene._algo_table = table
    return table

def hide_algo_table(scene, table=None, run_out=0.3, remove=True):
    if table is None:
        table = getattr(scene, "_algo_table", None)
    if table is None:
        return None
    if run_out > 0:
        scene.play(FadeOut(table, run_time=run_out))
    if remove:
        scene.remove(table)
    if getattr(scene, "_algo_table", None) is table:
        scene._algo_table = None
    return table

def show_poly_mul(scene, vec_p, vec_q, vec_f, vec_g, sz):
    n_p = len(vec_p)
    n_q = len(vec_q)
    n_f = len(vec_f)
    n_g = len(vec_g)
    prod_len = n_p + n_q - 1
    grid_p = make_grid(scene, n_p, 1, mat_l=[vec_p], btn_x=-(prod_len-n_p)*sz/2.0, lgt_x=-(prod_len-n_p)*sz/2.0, btn_y=(n_q+3)*sz/2.0, lgt_y=(n_q+3)*sz/2.0, btn_c=P_COLOR, lgt_c=P_COLOR, sz=sz)
    label_p = add_left_labels(scene, grid_p, ["p"], which="btn", dx=0.4)
    grid_q = make_grid(scene, 1, n_q, mat_l=[[v] for v in vec_q], btn_x=-(prod_len/2.0+2.0)*sz, lgt_x=-(prod_len/2.0+2.0)*sz, btn_c=Q_COLOR, lgt_c=Q_COLOR, sz=sz)
    label_q = add_top_labels(scene, grid_q, ["q"], which="btn", dy=0.4)
    grid_g = make_grid(scene, prod_len, 1, mat_l=[[0]*prod_len], btn_y=-(n_q+3)*sz/2, lgt_y=-(n_q+3)*sz/2, btn_c=G_COLOR, lgt_c=G_COLOR, sz=sz)
    label_g = add_left_labels(scene, grid_g, ["g"], which="btn", dx=0.4)
    grid_f = make_grid(scene, n_f, 1, mat_l=[vec_f], btn_y=-(n_q+5)*sz/2, lgt_y=-(n_q+5)*sz/2, btn_x=-(prod_len-n_f)*sz/2.0, lgt_x=-(prod_len-n_f)*sz/2.0, btn_c=F_COLOR, lgt_c=F_COLOR, sz=sz)
    label_f = add_left_labels(scene, grid_f, ["f"], which="btn", dx=0.4)
    grid_f2 = make_grid(scene, prod_len, 1, mat_l=[vec_f], btn_y=-(n_q+5)*sz/2, lgt_y=-(n_q+5)*sz/2, btn_x=0, lgt_x=0, btn_c=F_COLOR, lgt_c=F_COLOR, sz=sz, show=False)
    mid_rows = []
    for r in range(n_q):
        grid_row = make_grid(scene, n_p, 1, mat_l=[[0]*n_p], lgt_x=(r-(n_q-1)/2.0)*sz, btn_x=(r-(n_q-1)/2.0)*sz, btn_y=(n_q-1)*sz/2.0-r*sz, lgt_y=(n_q-1)*sz/2.0-r*sz, btn_c=X_COLOR, lgt_c=X_COLOR, sz=sz, rt=0.1)
        mid_rows.append(grid_row)
    mid_rows_cp = []
    mid_rows_p = []
    for r in range(n_q):
        if not vec_q[r]:
            continue
        grid_copy_p = make_grid(scene, n_p, 1, mat_l=[vec_p], btn_x=-(prod_len-n_p)*sz/2.0, lgt_x=-(prod_len-n_p)*sz/2.0, btn_y=(n_q+3)*sz/2.0, lgt_y=(n_q+3)*sz/2.0, btn_c=P_COLOR, lgt_c=P_COLOR, sz=sz, show=False)
        move_grid(scene, grid_copy_p, lgt_x=(r-(n_q-1)/2.0)*sz, btn_x=(r-(n_q-1)/2.0)*sz, lgt_y=(n_q-1)*sz/2.0-r*sz, btn_y=(n_q-1)*sz/2.0-r*sz, sz=None)
        mid_rows_cp.append(grid_copy_p)
        pad_left = r
        pad_right = prod_len - n_p - r
        grid_mid_p = make_grid(scene, prod_len, 1, mat_l=[[0]*pad_left + list(vec_p) + [0]*pad_right], mat_g=[[1 if (i>=pad_left and i<pad_left+n_p) else 0 for i in range(prod_len)]], btn_y=(n_q-1)*sz/2.0-r*sz, lgt_y=(n_q-1)*sz/2.0-r*sz, btn_c=P_COLOR, lgt_c=P_COLOR, sz=sz, show=False)
        mid_rows_p.append(grid_mid_p)
    for grid_mid_p in mid_rows_p:
        add_grid(scene, grid_mid_p, grid_g)
    add_grid(scene, grid_f2, grid_g)
    grid_g2 = make_grid(scene, (n_g-1), 1, mat_l=[vec_g], btn_y=-(n_q+3)*sz/2, lgt_y=-(n_q+3)*sz/2, btn_x=-(prod_len-(n_g-1))*sz/2.0, lgt_x=-(prod_len-(n_g-1))*sz/2.0, btn_c=G_COLOR, lgt_c=G_COLOR, sz=sz)
    del_grids(scene, [grid_g])
    return label_q, label_p, label_g, label_f, grid_p, grid_q, mid_rows, mid_rows_cp, mid_rows_p, grid_g2, grid_f

def clear_poly_mul(scene, ret):
    label_q, label_p, label_g, label_f, grid_p, grid_q, mid_rows, mid_rows_cp, mid_rows_p, grid_g2, grid_f = ret
    del_top_labels(scene, label_q)
    del_left_labels(scene, [label_p, label_g, label_f])
    del_grids(scene, [grid_p, grid_q, mid_rows, mid_rows_cp, mid_rows_p, grid_g2, grid_f])

def make_ops_euclid(mat_f, mat_p):
    def vec_to_int(v):
        x = 0
        for i, b in enumerate(v):
            if b: x |= (1 << i)
        return x
    def poly_deg(x):
        if x == 0: return -1
        return x.bit_length() - 1
    n = max(len(mat_f), len(mat_p))
    F = vec_to_int(mat_f + [0]*(n-len(mat_f)))
    P = vec_to_int(mat_p + [0]*(n-len(mat_p)))
    mask = (1 << n) - 1
    ops = []
    steps = 0
    while F != 0 and P != 0 and steps < 512:
        df = poly_deg(F)
        dp = poly_deg(P)
        if df < dp:
            ops.append(["swap", 0])
            F, P = P, F
            steps += 1
            continue
        shift = df - dp
        if shift > 0:
            ops.append(["addshift", shift])
            F ^= (P << shift) & mask
            steps += 1
        else:
            ops.append(["addshift", 0])
            F ^= P
            steps += 1
    if P == 0 and F != 0:
        ops.append(["swap", 0])
    return ops

def euclid_grids(scene, grids, ops, start=0, end=None, rt=None):
    if not ops: return
    if end is None: end = len(ops) - 1
    if start < 0: start = 0
    if end >= len(ops): end = len(ops) - 1
    f_grid, p_grid, e_grid, o_grid = grids
    for k in range(start, end + 1):
        op, arg = ops[k]
        if op in (0, "add", "ADD", "a", "A"):
            add_grid(scene, A_from=p_grid, A_to=f_grid, B_from=o_grid, B_to=e_grid, rt=rt)
        elif op in (1, "swap", "SWAP", "s", "S"):
            swap_grid(scene, A_from=f_grid, A_to=p_grid, B_from=e_grid, B_to=o_grid, rt=rt)
        elif op in (2, "shift", "SHIFT", "sh", "SH"):
            if arg and arg > 0:
                shift_grid(scene, A_from=p_grid, B_from=o_grid, k=arg, rt=rt)
        elif op in ("addshift", "AS", "as"):
            if arg and arg > 0:
                addshift_grid(scene, A_from=p_grid, A_to=f_grid, B_from=o_grid, B_to=e_grid, k=arg, rt=rt)
            else:
                addshift_grid(scene, A_from=p_grid, A_to=f_grid, B_from=o_grid, B_to=e_grid, k=0, rt=rt)

def euclid_create(scene, vec_f, vec_p, vec_o, vec_e, color_f, color_p, color_o, color_e, dx, dy, sz, w=None):
    if w is None: w = len(vec_f)
    grid_f = make_grid(scene, w=w, h=1, lgt_x=-dx, btn_x=-dx, lgt_y=dy, btn_y=dy, sz=sz, mat_l=[vec_f], btn_c=color_f, lgt_c=color_f)
    grid_p = make_grid(scene, w=w, h=1, lgt_x=-dx, btn_x=-dx, lgt_y=-dy, btn_y=-dy, sz=sz, mat_l=[vec_p], btn_c=color_p, lgt_c=color_p)
    label_f = add_left_labels(scene, grid_f, ["f"], which="lgt", dx=sz)
    label_p = add_left_labels(scene, grid_p, ["p"], which="lgt", dx=sz)
    grid_o = make_grid(scene, w=w, h=1, lgt_x=dx, btn_x=dx, lgt_y=dy, btn_y=dy, sz=sz, mat_l=[vec_o], btn_c=color_o, lgt_c=color_o)
    grid_e = make_grid(scene, w=w, h=1, lgt_x=dx, btn_x=dx, lgt_y=-dy, btn_y=-dy, sz=sz, mat_l=[vec_e], btn_c=color_e, lgt_c=color_e)
    label_o = add_left_labels(scene, grid_o, ["o"], which="lgt", dx=sz)
    label_e = add_left_labels(scene, grid_e, ["e"], which="lgt", dx=sz)
    return grid_f, grid_p, grid_o, grid_e, label_f, label_p, label_o, label_e

def euclid_ops(scene, euc, ops, start=0, end=None, rt=None):
    grid_f, grid_p, grid_o, grid_e, label_f, label_p, label_o, label_e = euc
    euclid_grids(scene, [grid_f, grid_p, grid_o, grid_e], ops, start=start, end=end, rt=rt)

def euclid_done(scene, euc, vec_g, color_g, dx, dy, sz, w=None):
    grid_f, grid_p, grid_o, grid_e, label_f, label_p, label_o, label_e = euc
    if w is None: w = len(vec_g)
    grid_g = make_grid(scene, w=w, h=1, lgt_x=-dx, btn_x=-dx, lgt_y=-dy, btn_y=-dy, sz=sz, mat_l=[vec_g], btn_c=color_g, lgt_c=color_g, show=False)
    trans_grid(scene, grid_p, grid_g)
    del_left_labels(scene, [label_f, label_o])
    del_grids(scene, [grid_f, grid_o])
    del_left_labels(scene, [label_p, label_e])
    label_g = add_left_labels(scene, grid_p, ["g"], which="lgt", dx=sz)
    label_q = add_left_labels(scene, grid_e, ["q"], which="lgt", dx=sz)
    return label_g, label_q, grid_g, grid_e

def euclid_clear(scene, euc2):
    label_g, label_q, grid_g, grid_e = euc2
    del_left_labels(scene, [label_g, label_q])
    del_grids(scene, [grid_g, grid_e])

def build_case(i, w, h, l=1):
    btn = [[0] * w for _ in range(h)]
    lgt = [[0] * w for _ in range(h)]
    for c in range(w):
        if (i >> c) & 1:
            btn[0][c] = 1
            press_lgt(lgt, c, 0)
    for r in range(h - 1):
        for c in range(w):
            if lgt[r][c] != l:
                btn[r + 1][c] = 1
                press_lgt(lgt, c, r + 1)
    return btn, lgt

def slice_mat(mat, a, b, fill=0):
    H = len(mat)
    W = len(mat[0]) if H > 0 else 0
    a = max(0, a)
    b = min(H - 1, b)
    out = [[fill] * W for _ in range(H)]
    if H == 0 or a > b:
        return out
    for j in range(a, b + 1):
        row = mat[j]
        for i in range(min(W, len(row))):
            out[j][i] = int(row[i])
    return out

def rotate_mat(mat, k):
    k %= 4
    if k == 0: return [row[:] for row in mat]
    if k == 1: return [list(r) for r in zip(*mat[::-1])]
    if k == 2: return [row[::-1] for row in mat[::-1]]
    if k == 3: return [list(r) for r in zip(*mat)][::-1]

def make_mat_l(n):
    N=n*n
    A=[[0]*n for _ in range(n)]
    for i in range(n):
        A[i][i]=1
        if i>0:A[i][i-1]=1
        if i<n-1:A[i][i+1]=1
    E=[[1 if i==j else 0 for j in range(n)] for i in range(n)]
    mat=[[0]*N for _ in range(N)]
    for bi in range(n):
        for bj in range(n):
            B=A if bi==bj else E if abs(bi-bj)==1 else None
            if B:
                r=bi*n
                c=bj*n
                for i in range(n):
                    mat[r+i][c:c+n]=B[i][:]
    return mat

def make_mat_k(n):
    I = [[1 if i == j else 0 for i in range(n)] for j in range(n)]
    Z = [[0]*n for _ in range(n)]
    M = [[[0]*n for _ in range(n)] for _ in range(n+1)]
    def v(A, y, x):
        return A[y][x] if 0 <= x < n else 0
    for y in range(n):
        for x in range(n):
            M[0][y][x] = I[y][x]
    for k in range(1, n+1):
        A = M[k-1]
        B = M[k-2] if k-2 >= 0 else Z
        for y in range(n):
            for x in range(n):
                M[k][y][x] = v(A, y, x-1) ^ v(A, y, x) ^ v(A, y, x+1) ^ B[y][x]
    return M

def make_mat_kn(n):
    M = make_mat_k(n)
    return [row[:] for row in M[n-1]]

def make_mat_ky(n):
    def shl(v):
        return [0] + v[:-1]
    def shr(v):
        return v[1:] + [0]
    prev2 = [0]*n
    prev = [0]*n
    rows = []
    rows.append([0]*n)
    for _ in range(n):
        cur = [(prev[j] ^ shl(prev)[j] ^ shr(prev)[j] ^ prev2[j]) ^ 1 for j in range(n)]
        rows.append(cur)
        prev2, prev = prev, cur
    return rows

MAT5K = make_mat_k(5)
MAT5KY = make_mat_ky(5)
MAT7K = make_mat_k(7)
MAT7KY = make_mat_ky(7)

MAT8_0 = [[0]*8 for _ in range(8)]
MAT_MK1 = [[1 if j <= i else 0 for j in range(8)] for i in range(8)]
MAT_MK2 = [[1 if j < i else 0 for j in range(8)] for i in range(8)]

MAT_B = [
    [1,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0],
    [1,0,1,0,0,0,0,0],
    [0,1,1,1,0,0,0,0],
    [0,0,0,0,1,0,0,0],
    [0,1,1,0,1,1,0,0],
    [1,0,0,0,1,0,1,0],
    [1,0,1,1,0,1,1,1],
]

MAT_Y = [
    [0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0],
    [1,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [1,0,0,0,1,0,0,0],
    [1,0,0,0,0,1,0,0],
    [0,1,0,1,0,1,0,0],
]

MAT_YK = [
    [0,1,0,1,0,1,0],
    [1,0,0,0,0,0,1],
    [0,1,0,0,0,1,0],
    [1,0,1,0,1,0,1],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
]

MAT_H = [
    [0,1,0,0,0,0,0],
    [1,0,1,0,0,0,0],
    [0,1,0,1,0,0,0],
    [0,0,1,0,1,0,0],
    [0,0,0,1,0,1,0],
    [0,0,0,0,1,0,1],
    [0,0,0,0,0,1,0],
]

MAT_K = [
    [1,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0],
    [1,0,1,0,0,0,0,0],
    [0,0,0,1,0,0,0,0],
    [0,0,1,0,1,0,0,0],
    [0,1,0,0,0,1,0,0],
    [1,0,1,0,1,0,1,0],
    [0,0,0,0,0,0,0,1],
]

MAT_C = [
    [1,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0],
    [1,1,1,1,0,0,0,0],
    [1,0,1,0,1,0,0,0],
    [0,0,0,0,1,1,0,0],
    [1,0,1,0,0,0,1,0],
    [1,1,1,1,1,1,1,1],
]

MAT_F = [
    [1,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0],
    [1,0,1,0,0,0,0,0],
    [0,0,0,1,0,0,0,0],
    [1,0,1,0,1,0,0,0],
    [0,1,0,0,0,1,0,0],
    [1,0,0,0,1,0,1,0],
    [0,0,0,0,0,0,0,1],
]

MAT_P = [
    [0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0],
    [1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,1,0,0,1,0,0,0],
    [0,0,1,0,1,0,0,0],
    [1,1,1,1,1,1,1,0],
]

MAT_G = [
    [1,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0],
    [1,0,1,0,1,0,0,0],
    [0,1,1,0,0,0,0,0],
    [1,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0],
]

MAT_Q = [
    [0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0],
    [1,1,0,0,0,0,0,0],
]

MAT_QH = [
    [1,1,0,0,0,0,0],
    [1,1,1,0,0,0,0],
    [0,1,1,1,0,0,0],
    [0,0,1,1,1,0,0],
    [0,0,0,1,1,1,0],
    [0,0,0,0,1,1,1],
    [0,0,0,0,0,1,1],
]

MAT_QH5 = [
    [0,1,0,0,0],
    [1,0,1,0,0],
    [0,1,0,1,0],
    [0,0,1,0,1],
    [0,0,0,1,0],
]

MAT_QH5_2 = [
    [1,1,0,0,0],
    [1,1,1,0,0],
    [0,1,1,1,0],
    [0,0,1,1,1],
    [0,0,0,1,1],
]

MAT_B5 = [
    [0,1,1,0,1],
    [1,1,1,0,0],
    [1,1,0,1,1],
    [0,0,1,1,1],
    [1,0,1,1,0],
]

MAT_Q5 = [
    [1,1,0,0,0],
    [1,1,1,0,0],
    [0,1,1,0,0],
    [0,1,1,1,0],
    [1,0,1,0,1],
]

MAT_E5 = [
    [1,0,0,0,1],
    [0,1,0,1,0],
    [0,0,1,1,1],
    [0,0,0,0,0],
    [0,0,0,0,0],
]

VEC_V = [0,1,0,0,0,1,0]

VEC_B5 = [0,1,1,0,1]
VEC_Y5 = [1,0,0,0,1]
VEC_K5 = [0,1,0,0,0]
VEC_F5 = [0,1,0,0,0,1]
VEC_C5 = [0,0,0,0,1]
VEC_P5 = [0,1,0,0,1]
VEC_Q5 = [0,1,0,0,0]
VEC_Q5_2 = [1,1,0,0,0]
VEC_G5 = [0,1,1,0,0,0]
VEC_G5_2 = [0,0,1,0,1,0]
VEC_E5 = [1,0,0,0,0]
VEC_O5 = [0,0,0,0,0]
VEC_Z5 = [0,1,0,1,0]
VEC_X5 = [0,0,0,1,1]
VEC_R5 = [0,0,0,1,2]

VEC_B7 = [1,0,1,1,0,1,1]
VEC_Y7 = [0,1,0,1,0,1,0]
VEC_K7 = [0,0,0,0,0,0,0]
VEC_F7 = [0,0,0,0,0,0,0,1]
VEC_C7 = [1,1,1,1,1,1,1]
VEC_P7 = [1,1,1,1,1,1,1]
VEC_Q7 = [1,1,0,0,0,0,0]
VEC_G7 = [1,0,0,0,0,0,0,0]
VEC_E7 = [1,0,0,0,0,0,0]
VEC_O7 = [0,0,0,0,0,0,0]
VEC_X7 = [1,1,0,1,0,1,1]

OPS_5 = make_ops_euclid(VEC_F5, VEC_P5)
OPS_7 = make_ops_euclid(VEC_F7, VEC_P7)

LATEX1 = [
    {"type": "text", "content": "递推公式（Fibonacci 多项式的 GF(2) 版本）：", "scale": 1.0, "indent": 0.0},
    {"type": "tex_lines", "scale": 0.6, "content": [
        r"f(0,x)=1",
        r"f(1,x)=x",
        r"f(2,x)=(1+x)^2",
        r"f(n+1,x)=x\cdot f(n,x)+f(n-1,x)",
        r"r(n)=\operatorname{deg}(\gcd(f(n,x),\,f(n,1+x)))"
    ]},
    {"type": "text", "content": "其中：", "scale": 1.0, "indent": 0.0},
    {"type": "tex_cn_lines", "scale": 0.6, "cn_scale": 0.6, "content": [
        {"tex": r"f(n,x)\in \mathbb{F}_2[x]", "cn": "（系数域为 GF(2)）"},
        {"tex": r"\operatorname{deg}:\ \mathbb{F}_2[x]\setminus\{0\}\to \mathbb{N}", "cn": "（多项式次数）"},
        {"tex": r"\gcd:\ \mathbb{F}_2[x]\times \mathbb{F}_2[x]\to \mathbb{F}_2[x]", "cn": "（多项式最大公因子）"}
    ]},
    {"type": "text", "content": "性质：", "scale": 1.0, "indent": 0.0},
    {"type": "tex_cn_lines", "scale": 0.6, "cn_scale": 0.6, "content": [
        {"tex": r"r(n)\equiv 0\pmod{2}", "cn": "（偶数）"},
        {"tex": r"r(n)\le n", "cn": "（上界）"},
        {"tex": r"r(n)\le r((n+1)k-1)\quad (n,k\in\mathbb{N})", "cn": "（按倍数拉长的单调性）"}
    ]}
]

LATEX_LEFT = [
    {"type": "text", "content": "[1] Jaap Scherphuis，《点灯问题游戏的数学原理》", "scale": 0.5, "indent": 0.0},
    {"type": "text", "content": "https://www.jaapsch.net/puzzles/lomath.htm",           "scale": 0.5, "indent": 0.5},
    {"type": "text", "content": "[2] Granvallen，《点灯游戏与数学之美》",               "scale": 0.5, "indent": 0.0},
    {"type": "text", "content": "https://granvallen.github.io/lightoutgame/",            "scale": 0.5, "indent": 0.5},
    {"type": "text", "content": "[3] axpokl，《点灯游戏 Flip Game 的 O(n^3) 求解算法》", "scale": 0.5, "indent": 0.0},
    {"type": "text", "content": "https://zhuanlan.zhihu.com/p/53646257",                 "scale": 0.5, "indent": 0.5},
    {"type": "text", "content": "[4] Chao Xu，《逼零集、点灯游戏与线性方程组》",          "scale": 0.5, "indent": 0.0},
    {"type": "text", "content": "https://zhuanlan.zhihu.com/p/553780037",                "scale": 0.5, "indent": 0.5},
    {"type": "text", "content": "[5] GitHub — axpokl，《Pascal点灯问题O(n^3)求解程序》", "scale": 0.5, "indent": 0.0},
    {"type": "text", "content": "https://github.com/axpokl/LightOut",                    "scale": 0.5, "indent": 0.5},
    {"type": "text", "content": "[6] GitHub — njpipeorgan，《大规模点灯问题求解器》",         "scale": 0.5, "indent": 0.0},
    {"type": "text", "content": "https://github.com/njpipeorgan/LightsOut",              "scale": 0.5, "indent": 0.5},
    {"type": "text", "content": "[7] OEIS，《n×n 全亮点灯问题的解数》",                   "scale": 0.5, "indent": 0.0},
    {"type": "text", "content": "https://oeis.org/A075462",                              "scale": 0.5, "indent": 0.5},
    {"type": "text", "content": "[8] OEIS，《n×n 全亮点灯问题的秩缺陷》",                 "scale": 0.5, "indent": 0.0},
    {"type": "text", "content": "https://oeis.org/A159257",                              "scale": 0.5, "indent": 0.5}
]

LATEX_RIGHT = [
    {"type": "text", "content": "本视频由 ManimGL 制作：",                                 "scale": 0.5, "indent": 0.0},
    {"type": "text", "content": "https://github.com/3b1b/manim",                          "scale": 0.5, "indent": 0.5},
    {"type": "text", "content": "视频脚本：",                                             "scale": 0.5, "indent": 0.0},
    {"type": "text", "content": "https://github.com/axpokl/LightOut/blob/master/lights_out_manim2.py", "scale": 0.5, "indent": 0.5},
    {"type": "text", "content": "Pascal语言算法实现：",                                             "scale": 0.5, "indent": 0.0},
    {"type": "text", "content": "https://github.com/axpokl/LightOut/blob/master/diandeng10_a_faster2_png_H11.pas", "scale": 0.5, "indent": 0.5},
    {"type": "text", "content": "点灯游戏安卓 APK（含 O(n^3) 求解）：",                    "scale": 0.5, "indent": 0.0},
    {"type": "text", "content": "https://axpokl.com/cx/axdiandeng2.apk",                  "scale": 0.5, "indent": 0.5}
]

LATEX_MAT = [
    (L_COLOR,  "<cL>",  "L",   "-",   "灯矩阵第一行",                 "公式递推",     "<cL>L(n,x)=L(n-1,x-1)⊕L(n-1,x)⊕L(n-1,x+1)⊕L(n-2,x)"),
    (B_COLOR,  "<cB>",  "B",   "-",   "按钮矩阵第一行",               "公式递推",     "<cB>B(n,x)=B(n-1,x-1)⊕B(n-1,x)⊕B(n-1,x+1)⊕B(n-2,x)"),
    (Y_COLOR,  "<cY>",  "Y",   "-",   "灯矩阵最后一行",               "公式递推...", "<cY>Y(n,y)=~(Y(n-1,y-1)⊕Y(n-1,y)⊕Y(n-1,y+1)⊕Y(n-2,y))"),
    (H_COLOR,  "<cH>",  "H",   "-",   "邻接矩阵",                     "公式递推",     "<cH>H(y,x)=(∣x-y∣=1)"),
    (K_COLOR,  "<cK>",  "K",   "<cH>H",   "H^n第一行（Krylov扩散基矩阵）", "公式递推",     "<cK>K(n,x)=K(n-1,x-1)⊕K(n-1,x+1)"),
    (F_COLOR,  "<cF>",  "F",   "<cK>K",   "K的逆矩阵（Krylov解耦矩阵）",   "公式递推",     "<cF>F(n,x)=F(n-1,x-1)⊕F(n-2,x)"),
    (C_COLOR,  "<cC>",  "C",   "<cB>B",   "B关于H的系数矩阵",             "公式递推",     "<cC>C(n,x)=C(n-1,x-1)⊕C(n-1,x)⊕C(n-2,x)"),
    (P_COLOR,  "<cP>",  "P",   "<cF>F<cP>,<cB>b", "多项式p(H)的系数",             "矩阵向量乘法", "<cP>p=<cF>F<cB>b"),
    (Q_COLOR,  "<cQ>",  "Q",   "<cF>F<cQ>,<cP>p", "多项式p(x)的在f(x)下的逆",     "扩展欧几里得", "<cQ>q=<cP>p^-1<cQ> mod <cF>F"),
    (G_COLOR,  "<cG>",  "G",   "<cF>F<cG>,<cP>P", "多项式p(x)和q(x)最大共因子",   "扩展欧几里得", "<cG>g=gcd(<cF>f<cG>,<cC>c<cG>)=gcd(<cF>f<cG>,<cP>p<cG>)"),
    (Z_COLOR,  "<cZ>",  "Z",   "<cQ>Q<cZ>,<cY>y", "部分逆按钮解",                 "矩阵向量乘法", "<cZ>z=<cQ>Q<cY>y"),
    (D_COLOR,  "<cD>",  "D",   "<cK>K<cD>,<cG>g", "多项式g(x)的矩阵",             "矩阵向量乘法", "<cD>d=<cK>K<cG>g"),
    (X_COLOR,  "<cX>",  "X",   "<cD>D<cX>,<cZ>z", "最终首行按钮解",               "前向异或消元", "<cZ>z=<cD>D<cX>x"),
    (T_COLOR,  "<cT>",  "T",   "<cX>x",   "最终按钮解矩阵",               "公式递推",     "<cT>T(n,x)=T(n-1,x-1)⊕T(n-1,x)⊕T(n-1,x+1)⊕T(n-2,x)"),
]

(
 LATEX_L,
 LATEX_B,
 LATEX_Y,
 LATEX_H,
 LATEX_K,
 LATEX_F,
 LATEX_C,
 LATEX_P,
 LATEX_Q,
 LATEX_G,
 LATEX_Z,
 LATEX_D,
 LATEX_M,
 LATEX_X,
 LATEX_T
) = [
    f"{row[6]}"
    for row in LATEX_MAT
]

class LightsOut(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        show_title(self, "点灯游戏的$O(n^2)$解法")
#演示n=5,7,11
        show_title(self, "首行叠加法（续上集）")

        show_subtitle(self, "在上集视频的《首行叠加法》中，有观众对按钮和灯的递推仍有疑问。", "这次我们来讲清楚，这个递推公式是怎么来的。")
        LAT1 = show_latex(self, "<cB>B(n,x)=B(n-1,x-1)⊕B(n-1,x)⊕B(n-1,x+1)⊕B(n-2,x)", 0, 2.0)
        LAT2 = show_latex(self, "<cB>B按钮    <cL>L灯    <cH1>⊕叠加    <cH2>~翻转", 0, 1.5)
        self.wait(4)

        show_subtitle(self, "我们用B代表按钮，L代表灯，⊕（加）代表叠加，~（非）代表翻转。")
        cols, rows = 5, 5
        sz = 0.25
        G5_ = [[None] * cols for _ in range(rows)]
        G5Y_ = [[None] * cols for _ in range(rows)]
        top_objs = [[None] * cols for _ in range(rows)]
        topy_objs = [[None] * cols for _ in range(rows)]
        left_objs = [[None] * cols for _ in range(rows)]
        for k in range(rows):
            for y in range(cols):
                mx = (y*2-cols)*(1+sz)+1
                my = -k*sz
                G5_[k][y] = make_grid(self, w=cols, h=1, lgt_x=mx, btn_x=mx, lgt_y=my, btn_y=my, sz=sz, mat=[MAT5K[k][y][:]], mat_l=[MAT5K[k+1][y][:]], show=True, rt=0.05)
                mx = (y*2-cols)*(1+sz)+1+sz*(cols+3)/2
                G5Y_[k][y] = make_grid(self, w=1, h=1, lgt_x=mx, btn_x=mx, lgt_y=my, btn_y=my, sz=sz, mat=[[MAT5KY[k][y]]], mat_l=[[MAT5KY[k+1][y]]],show=True, rt=0.05)
                if k == 0: top_objs[k][y] = add_top_labels(self, G5_[k][y], ["x1","x2","x3","x4","x5"], which="lgt", scale=0.4, rt=0.01)
                if k == 0: topy_objs[k][y] = add_top_labels(self, G5Y_[k][y], [f"y{y+1}"], which="lgt", scale=0.4, rt=0.01)
                left_objs[k][y] = add_left_labels(self, G5_[k][y], [f"n{k+1}"], which="lgt", scale=0.4, rt=0.01)

        show_subtitle(self, "n代表从上到下第n行灯或按钮。", "因为我们是一行行进行推导的，n也代表第n次推导。")
        n_frames = hl_objs(self, [left_objs], width=BD_W)
        self.wait(4)
        del_hl_objs(self, n_frames)
        show_subtitle(self, "x代表从左到右第x列按钮。将灯表示为第一行的某几个列的按钮的叠加。", "这里的x不局限于第一行。")
        x_frames = hl_objs(self, [top_objs], width=BD_W)
        self.wait(4)
        del_hl_objs(self, x_frames)
        show_subtitle(self, "y代表从左到右第y列灯。", "这里的公式对任意第y个灯都满足，所以省去了y。")
        y_frames = hl_objs(self, [LAT1])
        self.wait(4)
        del_hl_objs(self, y_frames)

        show_subtitle(self, "在这里，粉色原点是用按钮表示按钮，淡蓝色方块是用按钮表示灯。")
        mat_0 = [[0] * cols]
        mat_lgt = []
        mat_btn = []
        mat_lgt_y = []
        mat_btn_y = []
        for k in range(rows):
            row_lgt = []
            row_btn = []
            row_lgt_y = []
            row_btn_y = []
            for y in range(cols):
                row_lgt.append([MAT5K[k+1][y][:]])
                row_btn.append([MAT5K[k][y][:]])
                row_lgt_y.append([[MAT5KY[k+1][y]]])
                row_btn_y.append([[MAT5KY[k][y]]])
            mat_lgt.append(row_lgt)
            mat_btn.append(row_btn)
            mat_lgt_y.append(row_lgt_y)
            mat_btn_y.append(row_btn_y)
        set_grid_mats(self, grids=G5_, mat=mat_btn, mat_l=mat_0, clear_first=False)
        set_grid_mats(self, grids=G5Y_, mat=mat_btn_y, mat_l=mat_0, clear_first=False)
        self.wait(2)
        set_grid_mats(self, grids=G5_, mat=mat_0, mat_l=mat_lgt, clear_first=False)
        set_grid_mats(self, grids=G5Y_, mat=mat_0, mat_l=mat_lgt_y, clear_first=False)
        self.wait(4)

        show_subtitle(self, "而在上集视频中，因为最终目标是将灯用按钮表示，", "因此省去了按钮表示按钮，粉色原点直接为按钮表示灯。")
        set_grid_mats(self, grids=G5_, mat=mat_lgt, mat_l=mat_0, clear_first=False)
        set_grid_mats(self, grids=G5Y_, mat=mat_lgt_y, mat_l=mat_0, clear_first=False)
        self.wait(4)

        del_latex(self, [LAT1, LAT2]);
        del_top_labels(self, top_objs)
        del_top_labels(self, topy_objs)
        del_left_labels(self, left_objs)
        del_grids(self, G5_);
        del_grids(self, G5Y_);

        show_subtitle(self, "让我们举一个具体的例子。", "在5x5的格子中，我们将灯和按钮编号为1-25。")
        cols, rows = 5, 5
        G5 = make_grid(self, w=cols, h=rows, lgt_x=-4, btn_x=-4, sz=0.5)
        objs = add_grid_labels(self, G5, [[f"B{c*rows + r + 1}" for c in range(cols)] for r in range(rows)], which="btn", scale=0.5)
        self.wait(2)
        show_subtitle(self, "在《叠加法》中，我们将灯表示为所有按钮的叠加。", "例如：L1=B1⊕B2⊕B6，L6=B1⊕B6⊕B7⊕B11。")
        sz = 0.15
        G5_ = [[None] * cols for _ in range(rows)]
        mat_l = make_mat_l(rows)
        btn_objs = [[None] * cols for _ in range(rows)]
        lgt_objs = [[None] * cols for _ in range(rows)]
        for y in range(rows):
            for x in range(cols):
                idx = y * cols + x
                my = ((rows * cols) - 1) * sz / 2 - idx * sz
                G5_[y][x] = make_grid(self, w=cols * rows, h=1, w_l=1, h_l=1, lgt_x=3, btn_x=0, lgt_y=my, btn_y=my, sz=sz, rt=0.01, mat=[mat_l[idx][:]], mat_l=[[1]], show=False)
                rt = 0.2
                if y==0 and x<=1 : rt = 1.0
                press_rev(self, G5, x,y, anim=rt / 5)
                trans_grid(self,G5,G5_[y][x], keep_from=True, rt=rt);
                btn_objs[y][x] = add_grid_labels(self, G5_[y][x], [[f"B{j+1}" for j in range(cols*rows)]], which="btn", scale=0.2, rt=0.01)
                lgt_objs[y][x] = add_grid_labels(self, G5_[y][x], [[f"L{idx+1}"]], which="lgt", scale=0.2, rt=0.01)
                del_grids(self, [G5], kp_bd=True , rt=rt /5) 

        show_subtitle(self, "通过这种方式我们得到了25元一次方程组。", "写成增广矩阵，也就是按钮矩阵加灯向量的形式。")
        del_grid_labels(self, objs)
        del_grids(self, [G5]) 
        self.wait(6)
        del_grid_labels(self, btn_objs)
        del_grid_labels(self, lgt_objs)
        del_grids(self, [G5_]) 

        show_subtitle(self, "而在《首行叠加法》中，我们需要把灯表示为第一行按钮的叠加。")
        cols, rows = 5, 5
        sz = 0.25
        G5_ = [[None] * cols for _ in range(rows)]
        G5Y_ = [[None] * cols for _ in range(rows)]
        top_objs = [[None] * cols for _ in range(rows)]
        topy_objs = [[None] * cols for _ in range(rows)]
        left_objs = [[None] * cols for _ in range(rows)]
        for k in range(rows):
            for y in range(cols):
                mx = (y*2-cols)*(1+sz)+1
                my = -k*sz
                G5_[k][y] = make_grid(self, w=cols, h=1, lgt_x=mx, btn_x=mx, lgt_y=my, btn_y=my, sz=sz, mat=[[0]*cols], mat_l=[[0]*cols], show=True, rt=0.01)
                mx = (y*2-cols)*(1+sz)+1+sz*(cols+3)/2
                G5Y_[k][y] = make_grid(self, w=1, h=1, lgt_x=mx, btn_x=mx, lgt_y=my, btn_y=my, sz=sz, mat=[[0]*cols for _ in range(rows)], mat_l=[[0]], show=True, rt=0.01)
                if k == 0: top_objs[k][y] = add_top_labels(self, G5_[k][y], ["B1","B2","B3","B4","B5"], which="lgt", scale=0.4, rt=0.01)
                if k == 0: topy_objs[k][y] = add_top_labels(self, G5Y_[k][y], [f"L{y+1}"], which="lgt", scale=0.4, rt=0.01)
                left_objs[k][y] = add_left_labels(self, G5_[k][y], [f"{ k*cols + y + 1 }"], which="lgt", scale=0.4, rt=0.01)

        show_subtitle(self, "这里的五个矩阵，", "分别代表第y列是由第一行的哪几个按钮叠加的。")
        self.wait(4)
        show_subtitle(self, "由于按法是动态的，当第二行按钮还未被按下时，", "L1=B1⊕B2，即第一个灯L1由第一行的一、二个按钮，即B1,B2叠加的。")
        toggle_lgt(self, G5_[0][0], 0, 0)
        toggle_lgt(self, G5_[0][0], 1, 0)
        self.wait(4)

        show_subtitle(self, "然后，B6=~L1=~(B1⊕B2)，即第六个按钮B6是第一个灯L1的翻转。", "因此，第二行按钮B6和第一行灯L1的叠加状态是相同的。")
        toggle_btn(self, G5_[1][0], 0, 0)
        toggle_btn(self, G5_[1][0], 1, 0)
        self.wait(4)
        
        show_subtitle(self, "旁边的向量，代表的是按钮或灯有没有翻转。")
        toggle_lgt(self, G5Y_[0][0], 0, 0)
        self.wait(4)
        show_subtitle(self, "例如，当第一个向量的第一个灯亮起时，", "表示第一个灯除了由刚才说的按钮叠加外，还需要再翻转才是正确的状态。")
        self.wait(4)

        show_subtitle(self, "同理，B7=~L2=~(B1⊕B2⊕B3)，即第七个按钮B6是第二个灯L2的翻转。", "同样，第二行的按钮B7和第一行灯L2的叠加状态是相同的。")
        toggle_lgt(self, G5_[0][1], 0, 0)
        toggle_lgt(self, G5_[0][1], 1, 0)
        toggle_lgt(self, G5_[0][1], 2, 0)
        toggle_btn(self, G5_[1][1], 0, 0)
        toggle_btn(self, G5_[1][1], 1, 0)
        toggle_btn(self, G5_[1][1], 2, 0)
        toggle_lgt(self, G5Y_[0][1], 0, 0)
        self.wait(4)

        show_subtitle(self, "这里，我们将第一个按钮B1的状态补全，", "将B1用第一行的按钮叠加时，有B1=B1。")
        toggle_btn(self, G5_[0][0], 0, 0)
        self.wait(4)

        show_subtitle(self, "接下来我们来看第六个灯。", "L6=B1⊕B6⊕B7=B1⊕~(B1⊕B2)⊕~(B1⊕B2⊕B3)=B1⊕B3。")
        hl_cells(self, [G5_[0][0]], which="btn", indices=[(0, 0)])
        hl_cells(self, [G5_[1][0]], which="btn", indices=[(0, 0)])
        hl_cells(self, [G5_[1][0]], which="btn", indices=[(1, 0)])
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(0, 0)])
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(1, 0)])
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(2, 0)])
        add_cell(self, G5_[0][0], G5_[1][0], 0, 0, 0, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2)
        add_cell(self, G5_[1][0], G5_[1][0], 0, 0, 0, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2)
        add_cell(self, G5_[1][0], G5_[1][0], 1, 0, 1, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2)
        add_cell(self, G5_[1][1], G5_[1][0], 0, 0, 0, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2)
        add_cell(self, G5_[1][1], G5_[1][0], 1, 0, 1, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2)
        add_cell(self, G5_[1][1], G5_[1][0], 2, 0, 2, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2)

        show_subtitle(self, "又比如，L7=B2⊕B6⊕B7⊕B8", "=B2⊕~(B1⊕B2)⊕~(B1⊕B2⊕B3)⊕~(B2⊕B3⊕B4)=~B4")
        toggle_btn(self, G5_[0][1], 1, 0)
        toggle_btn(self, G5_[1][2], 1, 0)
        toggle_btn(self, G5_[1][2], 2, 0)
        toggle_btn(self, G5_[1][2], 3, 0)
        hl_cells(self, [G5_[0][1]], which="btn", indices=[(1, 0)])
        hl_cells(self, [G5_[1][0]], which="btn", indices=[(0, 0)])
        hl_cells(self, [G5_[1][0]], which="btn", indices=[(1, 0)])
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(0, 0)])
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(1, 0)])
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(2, 0)])
        hl_cells(self, [G5_[1][2]], which="btn", indices=[(1, 0)])
        hl_cells(self, [G5_[1][2]], which="btn", indices=[(2, 0)])
        hl_cells(self, [G5_[1][2]], which="btn", indices=[(3, 0)])
        add_cell(self, G5_[0][1], G5_[1][1], 1, 0, 1, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2)
        add_cell(self, G5_[1][0], G5_[1][1], 0, 0, 0, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2)
        add_cell(self, G5_[1][0], G5_[1][1], 1, 0, 1, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2)
        add_cell(self, G5_[1][1], G5_[1][1], 0, 0, 0, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2)
        add_cell(self, G5_[1][1], G5_[1][1], 1, 0, 1, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2)
        add_cell(self, G5_[1][1], G5_[1][1], 2, 0, 2, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2)
        add_cell(self, G5_[1][2], G5_[1][1], 1, 0, 1, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2)
        add_cell(self, G5_[1][2], G5_[1][1], 2, 0, 2, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2)
        add_cell(self, G5_[1][2], G5_[1][1], 3, 0, 3, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2)

        show_subtitle(self, "这样不断递推，我们可以将任意L表示为某些B1到B5的叠加，再加上翻转。")
        for k in range(rows):
            for y in range(cols):
                grid = G5_[k][y]
                row_l = MAT5K[k+1][y]
                row_b = MAT5K[k][y] if k + 1 < len(MAT5K) else []
                w = min(cols, len(row_l), len(grid["lgt"][0]))
                for x in range(w):
                    if row_l[x] and not grid["lgt"][0][x]:
                        toggle_lgt(self, grid, x, 0, anim=0.01)
                    if x < len(row_b) and row_b[x] and not grid["btn"][0][x]:
                        toggle_btn(self, grid, x, 0, anim=0.01)
                gridY = G5Y_[k][y]
                val_btn = MAT5KY[k][y] if k < len(MAT5KY) else 0
                val_lgt = MAT5KY[k+1][y] if k+1 < len(MAT5KY) else 0
                if bool(val_btn) != gridY["btn"][0][0]:
                    toggle_btn(self, gridY, 0, 0, anim=0.01)
                if bool(val_lgt) != gridY["lgt"][0][0]:
                    toggle_lgt(self, gridY, 0, 0, anim=0.01)
        self.wait(4)
        del_top_labels(self, top_objs)
        del_top_labels(self, topy_objs)
        del_left_labels(self, left_objs)

        show_subtitle(self, "现在，如果我们把序号1-25用坐标x,y表示，", "则灯和按钮矩阵可写为上述公式。让我们以L7(2)=L(2,2,2)为例。")
        LAT1_1 = show_latex(self, "<cL>L(n,x,y)=<cB>B(n,x,y-1)⊕B(n,x,y)⊕B(n,x,y+1)⊕B(n-1,x,y)", 0, 2.0)
        top_objs = [[None] * cols for _ in range(rows)]
        topy_objs = [[None] * cols for _ in range(rows)]
        left_objs = [[None] * cols for _ in range(rows)]
        for k in range(rows):
            for y in range(cols):
                mx = (y*2-cols)*(1+sz)+1
                my = -k*sz
                mx = (y*2-cols)*(1+sz)+1+sz*(cols+3)/2
                if k == 0: top_objs[k][y] = add_top_labels(self, G5_[k][y], ["x1","x2","x3","x4","x5"], which="lgt", scale=0.4, rt=0.01)
                if k == 0: topy_objs[k][y] = add_top_labels(self, G5Y_[k][y], [f"y{y+1}"], which="lgt", scale=0.4, rt=0.01)
                left_objs[k][y] = add_left_labels(self, G5_[k][y], [f"n{k+1}"], which="lgt", scale=0.4, rt=0.01)
        hl_cells(self, [G5_[1][0]], which="btn", indices=[(1, 0)])
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(1, 0)])
        hl_cells(self, [G5_[1][2]], which="btn", indices=[(1, 0)])
        hl_cells(self, [G5_[0][1]], which="btn", indices=[(1, 0)])
        self.wait(2)
        del_cells(self, [G5_[1][0]], which="btn", indices=[(1, 0)])
        del_cells(self, [G5_[1][1]], which="btn", indices=[(1, 0)])
        del_cells(self, [G5_[1][2]], which="btn", indices=[(1, 0)])
        del_cells(self, [G5_[0][1]], which="btn", indices=[(1, 0)])

        show_subtitle(self, "这里，我们的矩阵同时满足另一个性质，", "称之为十字偶校验约束。")
        LAT0_1 = show_latex(self, "<cH2>B(n,x-1,y)⊕B(n,x+1,y)⊕B(n,x,y-1)⊕B(n,x,y+1)=0", 0, 2.5)
        hl_cells(self, [G5_[1][0]], which="btn", indices=[(1, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][2]], which="btn", indices=[(1, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(0, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(2, 0)], color=HL_COLOR_2)
        self.wait(2)

        show_subtitle(self, "某个元素的左右两个矩阵的对应位置的元素，", "和元素所在矩阵左右两个元素的叠加后为零。")
        LAT0_2 = show_latex(self, "<cH2>B(n,x-1,y)⊕B(n,x+1,y)=B(n,x,y-1)⊕B(n,x,y+1)", 0, 2.5, show=False)
        trans_latex(self, LAT0_1, LAT0_2)
        self.wait(2)
        show_subtitle(self, "这就是之前视频中，《优化生成矩阵》章节中的性质，", "后面我会给予证明。")
        self.wait(2)
        del_cells(self, [G5_[1][0]], which="btn", indices=[(1, 0)])
        del_cells(self, [G5_[1][2]], which="btn", indices=[(1, 0)])
        del_cells(self, [G5_[1][1]], which="btn", indices=[(0, 0)])
        del_cells(self, [G5_[1][1]], which="btn", indices=[(2, 0)])

        show_subtitle(self, "通过这个性质，递推公式可化为只根据当前矩阵的元素来叠加，", "无需依赖于左右矩阵。")
        hl_cells(self, [G5_[1][0]], which="btn", indices=[(1, 0)])
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(1, 0)])
        hl_cells(self, [G5_[1][2]], which="btn", indices=[(1, 0)])
        hl_cells(self, [G5_[0][1]], which="btn", indices=[(1, 0)])
        LAT1_2 = show_latex(self, "<cL>L(n,x,y)=<cB>B(n,x-1,y)⊕B(n,x,y)⊕B(n,x+1,y)⊕B(n-1,x,y)", 0, 2.0, show=False)
        trans_latex(self, LAT1_1, LAT1_2)
        self.wait(2)
        hl_cells(self, [G5_[1][0]], which="btn", indices=[(1, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][2]], which="btn", indices=[(1, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(0, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(2, 0)], color=HL_COLOR_2)
        self.wait(2)
        del_cells(self, [G5_[1][0]], which="btn", indices=[(1, 0)])
        del_cells(self, [G5_[1][2]], which="btn", indices=[(1, 0)])
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(0, 0)])
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(2, 0)])
        self.wait(2)

        show_subtitle(self, "因此，我们可以在公式中去除y。", "去除y后，灯可以表示为当前矩阵的上左中右的按钮的叠加。")
        LAT1_3 = show_latex(self, "<cL>L(n,x)=<cB>B(n,x-1)⊕B(n,x)⊕B(n,x+1)⊕B(n-1,x)", 0, 2.0, show=False)
        trans_latex(self, LAT1_2, LAT1_3)
        self.wait(4)

        show_subtitle(self, "又因为，下一行的按钮是当前灯的翻转。")
        LAT1_4 = show_latex(self, "<cB>B(n+1,x)=<cL>~L(n,x)=<cB>~(B(n,x-1)⊕B(n,x)⊕B(n,x+1)⊕B(n-1,x))", 0, 2.0, show=False)
        trans_latex(self, LAT1_3, LAT1_4)
        self.wait(2)
        show_subtitle(self, "以及，下一行的灯是上左中右的灯的翻转的叠加。")
        LAT2_1 = show_latex(self, "<cL>L(n+1,x)=<cL>~L(n,x-1)⊕~L(n,x)⊕~L(n,x+1)⊕~L(n-1,x)", 0, 1.5)
        self.wait(2)

        show_subtitle(self, "如果把翻转~提取出来，便有了一开始的推导公式。")
        self.wait(2)
        show_subtitle(self, "也就是，按钮是上一行的左中右按钮和上上行的按钮的叠加。")
        LAT1_5 = show_latex(self, "<cB>B(n,x)=<cB>B(n-1,x-1)⊕B(n-1,x)⊕B(n-1,x+1)⊕B(n-2,x)", 0, 2.0, show=False)
        trans_latex(self, LAT1_4, LAT1_5)
        self.wait(2)

        show_subtitle(self, "以及，灯是上一行的左中右按钮和上上行的灯的叠加。")
        LAT2_2 = show_latex(self, "<cL>L(n,x)=<cL>L(n-1,x-1)⊕L(n-1,x)⊕L(n-1,x+1)⊕L(n-2,x)", 0, 1.5, show=False)
        trans_latex(self, LAT2_1, LAT2_2)
        self.wait(4)
        del_cells(self, [G5_[1][1]], which="btn", indices=[(0, 0)])
        del_cells(self, [G5_[1][1]], which="btn", indices=[(1, 0)])
        del_cells(self, [G5_[1][1]], which="btn", indices=[(2, 0)])
        del_cells(self, [G5_[0][1]], which="btn", indices=[(1, 0)])

        show_subtitle(self, "可以注意到，按钮和灯的递推公式具有相同的形式，", "这是因为上一行灯就是下一行按钮。")
        self.wait(2)
        show_subtitle(self, "因为最终需要推导的是灯矩阵，因此灯矩阵是从按钮的第一行推导5行。", "因为最后一次推导的是灯，因此按钮矩阵也是5行。")
        self.wait(4)

        del_latex(self, [LAT0_2, LAT2_2]);

        show_subtitle(self, "对于翻转的情况，则可以单独列出来，以类似的方法推导，写成公式Y。")
        LAT3 = show_latex(self, "<cH2>Y(n,y)=<cH2>~(Y(n-1,y-1)⊕Y(n-1,y)⊕Y(n-1,y+1)⊕Y(n-2,y))", 0, 1.5)
        self.wait(2)
        show_subtitle(self, "下一行的翻转是上一行左中右和上上行叠加后的翻转。")
        self.wait(2)

        hl_cells(self, [G5Y_[0][1]], which="btn", indices=[(0, 0)])
        hl_cells(self, [G5Y_[1][0]], which="btn", indices=[(0, 0)])
        hl_cells(self, [G5Y_[1][1]], which="btn", indices=[(0, 0)])
        hl_cells(self, [G5Y_[1][2]], which="btn", indices=[(0, 0)])

        show_subtitle(self, "可以注意到，这里的公式Y和公式B的推导公式是类似的的。", "只不过，Y是从零向量开始推导的，并且不能省略翻转符号~。")
        self.wait(2)
        show_subtitle(self, "1. 使用零向量：第一次翻转发生在从一到二行的推导过程中，", "在此之前没有发生过翻转，因此Y的第一行是全零。")
        hl_cells(self, [G5Y_[0][0]], which="btn", indices=[(0, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5Y_[0][1]], which="btn", indices=[(0, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5Y_[0][2]], which="btn", indices=[(0, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5Y_[0][3]], which="btn", indices=[(0, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5Y_[0][4]], which="btn", indices=[(0, 0)], color=HL_COLOR_2)
        self.wait(2)
        show_subtitle(self, "2. 翻转符号~必须存在：每次推导都需要翻转，因此不可省略。", "而前者将这个翻转取出来了，因此不用翻转符号~。")
        self.wait(2)
        show_subtitle(self, "3. 不使用x而使用y：翻转是前面所有按钮的翻转叠加后提取出来的，", "代表的是灯的翻转，而不是某个按钮的翻转。")
        self.wait(4)
        del_cells(self, [G5Y_[0][0]], which="btn", indices=[(0, 0)])
        del_cells(self, [G5Y_[0][1]], which="btn", indices=[(0, 0)])
        del_cells(self, [G5Y_[0][2]], which="btn", indices=[(0, 0)])
        del_cells(self, [G5Y_[0][3]], which="btn", indices=[(0, 0)])
        del_cells(self, [G5Y_[0][4]], which="btn", indices=[(0, 0)])
        del_cells(self, [G5Y_[0][1]], which="btn", indices=[(0, 0)])
        del_cells(self, [G5Y_[1][0]], which="btn", indices=[(0, 0)])
        del_cells(self, [G5Y_[1][1]], which="btn", indices=[(0, 0)])
        del_cells(self, [G5Y_[1][2]], which="btn", indices=[(0, 0)])
        del_latex(self, [LAT1_5, LAT3]);
        del_top_labels(self, top_objs)
        del_top_labels(self, topy_objs)
        del_left_labels(self, left_objs)
        del_grids(self, [G5_, G5Y_]) 

        show_title(self, "优化生成矩阵（续上集）")
        show_subtitle(self, "在《生成优化矩阵》章节中，我将矩阵的行重排。", "其实是调换了n和y的位置，使原来从左到右的第y个矩阵变为了第n个矩阵。")
        cols, rows = 5, 5
        sz = 0.25
        G5_ = [[None] * cols for _ in range(rows)]
        G5Y_ = [[None] * cols for _ in range(rows)]
        for k in range(rows):
            for y in range(cols):
                mx = (y*2-cols)*(1+sz)+1
                my = -k*sz
                G5_[k][y] = make_grid(self, w=cols, h=1, lgt_x=mx, btn_x=mx, lgt_y=my, btn_y=my, sz=sz, mat=[MAT5K[k][y][:]], mat_l=[MAT5K[k+1][y][:]], show=True, rt=0.01)
                mx = (y*2-cols)*(1+sz)+1+sz*(cols+3)/2
                G5Y_[k][y] = make_grid(self, w=1, h=1, lgt_x=mx, btn_x=mx, lgt_y=my, btn_y=my, sz=sz, mat=[[MAT5KY[k][y]]], mat_l=[[MAT5KY[k+1][y]]],show=True, rt=0.01)
        for k in range(rows):
            for y in range(cols):
                if (k > y):
                    swap_grid(self, G5_[k][y], G5_[y][k], G5Y_[k][y], G5Y_[y][k])
        top_objs = [[None] * cols for _ in range(rows)]
        topy_objs = [[None] * cols for _ in range(rows)]
        left_objs = [[None] * cols for _ in range(rows)]
        for k in range(rows):
            for y in range(cols):
                if k == 0: top_objs[k][y] = add_top_labels(self, G5_[k][y], ["x1","x2","x3","x4","x5"], which="lgt", scale=0.4, rt=0.01)
                if k == 0: topy_objs[k][y] = add_top_labels(self, G5Y_[k][y], [f"n{y+1}"], which="lgt", scale=0.4, rt=0.01)
                left_objs[k][y] = add_left_labels(self, G5_[k][y], [f"y{k+1}"], which="lgt", scale=0.4, rt=0.01)

        show_subtitle(self, "这n个矩阵都满足十字偶校验约束，即上下左右四个格子叠加为零，", "因此这里的公式省去了n。")
        LAT1_1 = show_latex(self, "<cH2>B(x-1,y)⊕B(x+1,y)⊕B(x,y-1)⊕B(x,y+1)=0", 0, 1.5)
        self.wait(2)

        show_subtitle(self, "这里和之前的情况是一样的，", "只不过n和y调换了，因此位置发生了变化。")
        hl_cells(self, [G5_[0][2]], which="btn", indices=[(1, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[2][2]], which="btn", indices=[(1, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][2]], which="btn", indices=[(0, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][2]], which="btn", indices=[(2, 0)], color=HL_COLOR_2)
        self.wait(2)

        show_subtitle(self, "这是一个十分重要的性质。", "通过这个性质，可以由第一个灯直接推导后面的灯。")
        self.wait(2)
        show_subtitle(self, "在后面会说的O(n^2)算法中，", "其本质也是利用这个性质进行的优化。")
        self.wait(2)
        show_subtitle(self, "下面让我用数学归纳法，证明这个性质。")
        self.wait(2)

        show_subtitle(self, "由于右边的按钮矩阵就是左边的灯矩阵，", "为了方便，我们就只看按钮矩阵。")
        set_all_lights(self, G5_, on=False)
        set_all_lights(self, G5Y_, on=False)
        self.wait(2)

        show_subtitle(self, "首先，我们假定前两个矩阵B(n-1)和B(n-2)满足这个性质，", "现在来证明则B(n)也满足这个性质。")
        LAT1_2 = show_latex(self, "<cH2>B(n,x-1,y)⊕B(n,x+1,y)⊕B(n,x,y-1)⊕B(n,x,y+1)", 0, 1.5, show=False)
        trans_latex(self, LAT1_1, LAT1_2)
        bd = hl_bd(self, [row[2] for row in G5_])
        self.wait(2)

        show_subtitle(self, "将刚才的矩阵递推关系加上参数y并重写。")
        LAT2_1 = show_latex(self, "<cB>B(n,x,y)=B(n-1,x-1,y)⊕B(n-1,x,y)⊕B(n-1,x+1,y)⊕B(n-2,x,y)", 0, 1.0)
        hl_cells(self, [G5_[0][2]], which="btn", indices=[(1, 0)], color=HL_COLOR_1)
        hl_cells(self, [G5_[0][0]], which="btn", indices=[(1, 0)], color=HL_COLOR_1)
        hl_cells(self, [G5_[0][1]], which="btn", indices=[(0, 0)], color=HL_COLOR_1)
        hl_cells(self, [G5_[0][1]], which="btn", indices=[(1, 0)], color=HL_COLOR_1)
        hl_cells(self, [G5_[0][1]], which="btn", indices=[(2, 0)], color=HL_COLOR_1)
        self.wait(2)

        show_subtitle(self, "对于B(n)，我们将式子竖着写成四项，", "然后将递推关系代入这个式子。")
        LAT1_3 = show_latex(self, "<cH2>B(n,x-1,y)⊕<br><cH2>B(n,x+1,y)⊕<br><cH2>B(n,x,y-1)⊕<br><cH2>B(n,x,y+1)", 0, 2.0, show=False, font_size=FONT_SIZE_SMALL)
        trans_latex(self, LAT1_2, LAT1_3)
        self.wait(2)

        LAT1_4 = show_latex(self,
            "<cH2>(B(n-1,x-1-1,y)⊕B(n-1,x-1+1,y)⊕B(n-1,x-1,y-1)⊕B(n-1,x-1,y+1))⊕<br>"
            "<cH2>(B(n-1,x-1,y)⊕B(n-1,x+1,y)⊕B(n-1,x,y-1)⊕B(n-1,x,y+1))⊕<br>"
            "<cH2>(B(n-1,x+1-1,y)⊕B(n-1,x+1+1,y)⊕B(n-1,x+1,y-1)⊕B(n-1,x+1,y+1))⊕<br>"
            "<cH2>(B(n-2,x-1,y)⊕B(n-2,x+1,y)⊕B(n-2,x,y-1)⊕B(n-2,x,y+1))",
            0, 2.0, show=False, font_size=FONT_SIZE_SMALL)
        trans_latex(self, LAT1_3, LAT1_4)
        self.wait(2)

        show_subtitle(self, "代入后的式子包含16个项目。现在重新排列项目顺序，将y和n调换，类似《优化生成矩阵》章节中的调换操作。")
        LAT1_5 = show_latex(self,
            "<cH2>(B(n-1,x-1-1,y)⊕B(n-1,x-1,y)⊕B(n-1,x+1-1,y)⊕B(n-2,x-1,y))⊕<br>"
            "<cH2>(B(n-1,x-1+1,y)⊕B(n-1,x+1,y)⊕B(n-1,x+1+1,y)⊕B(n-2,x+1,y))⊕<br>"
            "<cH2>(B(n-1,x-1,y-1)⊕B(n-1,x,y-1)⊕B(n-1,x+1,y-1)⊕B(n-2,x,y-1))⊕<br>"
            "<cH2>(B(n-1,x-1,y+1)⊕B(n-1,x,y+1)⊕B(n-1,x+1,y+1)⊕B(n-2,x,y+1))",
            0, 2.0, show=False, font_size=FONT_SIZE_SMALL)
        trans_latex(self, LAT1_4, LAT1_5)

        hl_cells(self, [G5_[0][0]], which="btn", indices=[(1, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[2][0]], which="btn", indices=[(1, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][0]], which="btn", indices=[(0, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][0]], which="btn", indices=[(2, 0)], color=HL_COLOR_2)
        del_cells(self, [G5_[0][0]], which="btn", indices=[(1, 0)])
        del_cells(self, [G5_[2][0]], which="btn", indices=[(1, 0)])
        del_cells(self, [G5_[1][0]], which="btn", indices=[(0, 0)])
        del_cells(self, [G5_[1][0]], which="btn", indices=[(2, 0)])
        hl_cells(self, [G5_[0][1]], which="btn", indices=[(0, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[2][1]], which="btn", indices=[(0, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(1, 0)], color=HL_COLOR_2)
        del_cells(self, [G5_[0][1]], which="btn", indices=[(0, 0)])
        del_cells(self, [G5_[2][1]], which="btn", indices=[(0, 0)])
        del_cells(self, [G5_[1][1]], which="btn", indices=[(1, 0)])
        hl_cells(self, [G5_[0][1]], which="btn", indices=[(1, 0)])
        hl_cells(self, [G5_[2][1]], which="btn", indices=[(1, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(0, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(2, 0)], color=HL_COLOR_2)
        del_cells(self, [G5_[0][1]], which="btn", indices=[(1, 0)])
        del_cells(self, [G5_[2][1]], which="btn", indices=[(1, 0)])
        del_cells(self, [G5_[1][1]], which="btn", indices=[(0, 0)])
        del_cells(self, [G5_[1][1]], which="btn", indices=[(2, 0)])
        hl_cells(self, [G5_[0][1]], which="btn", indices=[(2, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[2][1]], which="btn", indices=[(2, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(1, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(3, 0)], color=HL_COLOR_2)
        del_cells(self, [G5_[0][1]], which="btn", indices=[(2, 0)])
        del_cells(self, [G5_[2][1]], which="btn", indices=[(2, 0)])
        del_cells(self, [G5_[1][1]], which="btn", indices=[(1, 0)])
        del_cells(self, [G5_[1][1]], which="btn", indices=[(3, 0)])
        hl_cells(self, [G5_[0][2]], which="btn", indices=[(1, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[2][2]], which="btn", indices=[(1, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][2]], which="btn", indices=[(0, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][2]], which="btn", indices=[(2, 0)], color=HL_COLOR_2)

        show_subtitle(self, "不难发现，这四项属于B(n-1)或B(n-2)，", "并且元素之间的关系满足十字偶校验约束，因此整个式子化为了零。")
        LAT1_6 = show_latex(self, "<cH2>0⊕<br><cH2>0⊕<br><cH2>0⊕<br><cH2>0", 0, 2.0, show=False, font_size=FONT_SIZE_SMALL)
        trans_latex(self, LAT1_5, LAT1_6)
        self.wait(1)
        LAT1_7 = show_latex(self, "<cH2>0⊕0⊕0⊕0", 0, 1.5, show=False)
        trans_latex(self, LAT1_6, LAT1_7)
        self.wait(2)
        LAT1_8 = show_latex(self, "<cH2>B(n,x-1,y)⊕B(n,x+1,y)⊕B(n,x,y-1)⊕B(n,x,y+1)=0", 0, 1.5, show=False)
        trans_latex(self, LAT1_7, LAT1_8)
        self.wait(2)

        del_cells(self, [G5_[0][2]], which="btn", indices=[(1, 0)])
        del_cells(self, [G5_[2][2]], which="btn", indices=[(1, 0)])
        del_cells(self, [G5_[1][2]], which="btn", indices=[(0, 0)])
        del_cells(self, [G5_[1][2]], which="btn", indices=[(2, 0)])
        del_bd(self, bd)

        show_subtitle(self, "现在，我们只需要证明最左边两个矩阵也满足这个性质即可。", "第一个矩阵是单位矩阵，显然满足这个性质。")
        bd = hl_bd(self, [row[0] for row in G5_])
        hl_cells(self, [G5_[0][0]], which="btn", indices=[(1, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[2][0]], which="btn", indices=[(1, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][0]], which="btn", indices=[(0, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][0]], which="btn", indices=[(2, 0)], color=HL_COLOR_2)
        self.wait(4)
        del_cells(self, [G5_[0][0]], which="btn", indices=[(1, 0)])
        del_cells(self, [G5_[2][0]], which="btn", indices=[(1, 0)])
        del_cells(self, [G5_[1][0]], which="btn", indices=[(0, 0)])
        del_cells(self, [G5_[1][0]], which="btn", indices=[(2, 0)])
        del_bd(self, bd)

        show_subtitle(self, "第二个矩阵可以表示为左边两个矩阵的叠加。", "由于单位矩阵左边没有矩阵，因此相当于叠加了一个零矩阵。")
        bd = hl_bd(self, [row[1] for row in G5_])
        hl_cells(self, [G5_[0][1]], which="btn", indices=[(1, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[2][1]], which="btn", indices=[(1, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(0, 0)], color=HL_COLOR_2)
        hl_cells(self, [G5_[1][1]], which="btn", indices=[(2, 0)], color=HL_COLOR_2)
        self.wait(2)
        show_subtitle(self, "由于零矩阵显然满足这个性质，因此第二个矩阵也满足这个性质。")
        self.wait(2)
        del_cells(self, [G5_[0][1]], which="btn", indices=[(1, 0)])
        del_cells(self, [G5_[2][1]], which="btn", indices=[(1, 0)])
        del_cells(self, [G5_[1][1]], which="btn", indices=[(0, 0)])
        del_cells(self, [G5_[1][1]], which="btn", indices=[(2, 0)])
        del_bd(self, bd)

        show_subtitle(self, "因为B(n)有了这个性质，我们只需要知道B(n)的第一行，", "就能通过公式推导出下面的行，求得完整的矩阵B(n)。")
        mat_0 = [[0] * cols]
        mat_lgt = []
        mat_btn = []
        mat_lgt_y = []
        mat_btn_y = []
        for y in range(cols):
            col_lgt = []
            col_btn = []
            col_lgt_y = []
            col_btn_y = []
            for k in range(rows):
                col_lgt.append([MAT5K[k+1][y][:]])
                col_btn.append([MAT5K[k][y][:]])
                col_lgt_y.append([[MAT5KY[k+1][y]]])
                col_btn_y.append([[MAT5KY[k][y]]])
            mat_lgt.append(col_lgt)
            mat_btn.append(col_btn)
            mat_lgt_y.append(col_lgt_y)
            mat_btn_y.append(col_btn_y)
        set_grid_mats(self, grids=G5_, mat=mat_btn, mat_l=mat_lgt, clear_first=False)
        set_grid_mats(self, grids=G5Y_, mat=mat_btn_y, mat_l=mat_lgt_y, clear_first=False)
        bd = hl_bd(self, [G5_[0][4]])
        self.wait(2)
        del_bd(self, bd)
        bd = hl_bd(self, [row[4] for row in G5_])
        self.wait(2)
        del_latex(self, [LAT1_8, LAT2_1])
        del_bd(self, bd)
        del_top_labels(self, top_objs)
        del_top_labels(self, topy_objs)
        del_left_labels(self, left_objs)
        del_grids(self, [G5_, G5Y_]) 

#——————————————————————

        show_title(self, "首行求逆法")

        show_subtitle(self, "对于O(n^2)的算法，我们也是使用类似的方法，", "尽可能的不去对完整矩阵进行操作，而是通过第一行来求逆或求解。")
        grid_B1 = make_grid(self, 7, 1, mat_l=[MAT7K[7][0]], btn_c=B_COLOR, lgt_c=B_COLOR, sz=0.4, btn_y=1.2, lgt_y=1.2)
        topy_obj_B = add_top_labels(self, grid_B1, ["", "", "", "B", "", "", ""], which="btn")
        self.wait(2)
        show_subtitle(self, "这里，让我以我们以n=7为例。", "这里的B就是前面提到的按钮矩阵B，而y就是翻转矩阵Y的最后一行。")
        grid_B = make_grid(self, 7, 7, mat_l=MAT7K[7], btn_c=B_COLOR, lgt_c=B_COLOR, sz=0.4)
        grid_Y = make_grid(self, 1, 7, mat_l=[[v] for v in MAT7KY[7]], btn_c=Y_COLOR, lgt_c=Y_COLOR, btn_x=2, lgt_x=2, sz=0.4)
        topy_obj_Y = add_top_labels(self, grid_Y, ["y"], which="btn")
        self.wait(2)

        show_subtitle(self, "我们的目标是，对于Bx=y，在已知B的第一行和y的情况下求x。")
        LAT_B = show_latex(self, "<cB>B<cX>x<cY>=y", 0, 2.0)
        pB   = grid_B["params"]
        sz   = pB["sz"]
        h_l  = pB["h_l"]
        lgt_x = pB["lgt_x"]
        btn_x = pB["btn_x"]
        lgt_y0 = pB["lgt_y"]
        btn_y0 = pB["btn_y"]
        row0_y = lgt_y0 + (h_l - 1) * sz / 2.0
        grid_B_row = make_grid(self, 7, 1, lgt_x=lgt_x, btn_x=btn_x, lgt_y=row0_y, btn_y=row0_y, sz=sz, show=False)
        bd_B_row = hl_bd(self, grid_B_row)
        grid_X = make_grid(self, 1, 7, mat_l=[[1],[1],[0],[1],[0],[1],[1]], btn_c=X_COLOR, lgt_c=X_COLOR, btn_x=2.8, lgt_x=2.8, sz=0.4)
        topy_obj_X = add_top_labels(self, grid_X, ["x"], which="btn")

        mul_vec_mat(self, w=7, h=7, mat=MAT7K[7], vec=VEC_X7, mat_color=B_COLOR, vec_color=X_COLOR, res_color=Y_COLOR, mat_label="", vec_label="x", res_label="y", sz=0.4)
        del_latex(self, [LAT_B])
        del_bd(self, bd_B_row)
        del_top_labels(self, [topy_obj_B, topy_obj_Y, topy_obj_X])
        del_grids(self, [grid_B, grid_Y, grid_X])

        show_subtitle(self, "如果将n在不同情况下B的第一行写在一起，这样的矩阵长这样，我们记为B'。")
        move_grid(self, grid_B1, btn_y=-1.4, lgt_y=-1.4, btn_x=-0.2, lgt_x=-0.2)
        bd_b_row7 = hl_bd(self, grid_B1)
        LAT_B = show_latex(self, LATEX_B, 0, 2.0)
        grid_B = make_grid(self, 8, 8, mat_l=MAT_B, mat_g={"lgt": MAT_MK1, "btn": MAT8_0}, btn_c=B_COLOR, lgt_c=B_COLOR, sz=0.4)
        left_obj = add_left_labels(self, grid_B, list(range(8)), which="btn", dx=0.4)
        bottom_obj = add_bottom_label(self, grid_B, "B'", which="btn", dy=0.6, color=B_COLOR)
        hl_cells(self, [grid_B], which="btn", indices=[(1,1),(0,2),(1,2),(2,2)])
        hl_cells(self, [grid_B], which="btn", indices=[(1,3)], color=HL_COLOR_2)
        self.wait(2)
        show_subtitle(self, "注意，这里的B'矩阵不是刚才说的当n确定时的完整的B矩阵，", "而是B(n)的第一行拼接起来。")
        self.wait(2)
        del_cells(self, [grid_B], which="btn", indices=[(1,1),(0,2),(1,2),(2,2)])
        del_cells(self, [grid_B], which="btn", indices=[(1,3)])
        show_subtitle(self, "另外，这里从n=0开始一共递推n次，最后一个1不包含在B矩阵的第一行内。", "例如n=7时，第一行为1011011，最后一个1省去。")
        del_bottom_label(self, bottom_obj)
        grid_B0 = make_grid(self, 8, 8, mat_l=MAT_B, mat_g={"lgt": MAT_MK2, "btn": MAT8_0}, btn_c=B_COLOR, lgt_c=B_COLOR, sz=0.4, show=False)
        bottom_obj = add_bottom_label(self, grid_B0, "B''", which="btn", dy=0.6, color=B_COLOR)
        trans_grid(self,grid_B,grid_B0, keep_from=False);
        show_subtitle(self, "改写后的矩阵记为B''=B'⊕I")

        self.wait(2)
        del_bd(self, bd_b_row7)
        del_latex(self, [LAT_B])
        del_left_labels(self, left_obj)
        del_bottom_label(self, bottom_obj)
        del_grids(self, [grid_B0, grid_B1])

        show_subtitle(self, "把Y的第一行写在一起是这样的，记作Y'。")
        LAT_Y = show_latex(self, LATEX_Y, 0, 2.0)
        grid_Y = make_grid(self, 8, 8, mat_l=MAT_Y, mat_g={"lgt": MAT_MK2, "btn": MAT8_0}, btn_c=Y_COLOR, lgt_c=Y_COLOR, sz=0.4)
        left_obj = add_left_labels(self, grid_Y, list(range(8)), which="btn", dx=0.4)
        bottom_obj = add_bottom_label(self, grid_Y, "Y'", which="btn", dy=0.6, color=Y_COLOR)
        self.wait(2)
        del_left_labels(self, left_obj)
        del_bottom_label(self, bottom_obj)
        del_grids(self, [grid_Y])

        show_subtitle(self, "合并在一起后的Y'有上述递推公式。")
        LAT_Y1 = show_latex(self,
            "<cY>Y0(n,y)=Y0(n-1,y-1)⊕Y0(n-1,y)⊕Y0(n-1,y+1)⊕Y0(n-2,y),y>y;Y'(y,n),y=1<br>"
            "<cY>Y1(n,y)=Y'(n-1,y-1)⊕Y0(n-1,y)<br>"
            "<cY>Y2(n,y)=Y1(n-1,y-1)⊕Y0(n-2,y)<br>"
            "<cY>Y'(n,y)=~(Y1(n,y-1)⊕Y1(n,y)⊕Y1(n,y+1)⊕Y2(n,y)),y<=n;0,y>n",
            0, 0.5, font_size=FONT_SIZE_SMALL)
        LAT_Y2 = show_latex(self,
            "<cY>Y0(n,y)=Y0(n-1,y-1)⊕Y0(n-1,y)⊕Y0(n-1,y+1)⊕Y0(n-2,y),y>1;Y'(n,y),y=1<br>"
            "<cY>Y'(n,y)=~(Y'(n-1,y-2)⊕Y'(n-1,y-1)⊕Y'(n-1,y)⊕Y'(n-2,y-2)<br>"
            "<cY>⊕Y0(n-1,y-1)⊕Y0(n-1,y)⊕Y0(n-1,y+1)⊕Y0(n-2,y-1)⊕Y0(n-2,y)),y<=n;0,y>n",
            0, -1.25, font_size=FONT_SIZE_SMALL)
        self.wait(2)
        del_latex(self, [LAT_Y, LAT_Y1, LAT_Y2])

        show_subtitle(self, "为了实现这个目标，我们需要首先将B进行分解。", "这里，让我首先介绍一个非常重要的矩阵H，称为邻接矩阵。")
        LAT_H = show_latex(self, LATEX_H, 0, 2.0)
        ctx = mul_vec_mat_begin(self, mat=MAT_H, vec=VEC_V, mat_color=H_COLOR, vec_color=V_COLOR, res_color=V_COLOR, mat_label="H", vec_label="v", res_label="v'", sz=0.4)
        show_subtitle(self, "对于H的每一个元素，如果x和y的差为一则为一，否则为零。")
        self.wait(2)
        show_subtitle(self, "如果将向量v乘以该矩阵，等同于将向量v的每个元素向左右扩散后叠加。")
        LAT_V = show_latex(self, "<cV>v'(x)=v(x)*<cH>H<cV>=v(x-1)⊕v(x+1)", 0, 2.5)
        mul_vec_mat_vec_and_rows(self, ctx)
        mul_vec_mat_accumulate(self, ctx)
        self.wait(2)
        show_subtitle(self, "这是因为矩阵的对应行就是向量每个元素左右扩散的结果。")
        self.wait(2)
        del_latex(self, [LAT_H, LAT_V])
        mul_vec_mat_cleanup(self, ctx, clear_res=True)

        show_subtitle(self, "不难发现，《首行叠加法》中的各个B矩阵，可以使用H表示为以上公式。")

        LAT_BH = show_latex(self, "<cB>B(n)=B(n-1)*<cH>H<cB>⊕B(n-1)⊕B(n-2)", 0, 2.5)
        LAT_BH0 = show_latex(self, "<cB>B(0)=<cI>I<cH>=H^0", 0, 2.0)
        LAT_BH1 = show_latex(self, "<cB>B(1)=<cH>H=<cH>H^0+H^1", 0, 1.5)
        LAT_BH2 = show_latex(self, "<cB>B(2)=B(1)*<cH>H<cB>+B(1)+B(0)=<cH>(H^2+H^1)+(H^1+H^0)+H^0=H^2", 0, 1.0)

        show_subtitle(self, "例如，B(0)=H^0，B(1)=H^0+H^1，B(2)=H^2")
        self.wait(2)
        del_latex(self, [LAT_BH0, LAT_BH1, LAT_BH2])

        show_subtitle(self, "将其系数用多项式c(n,x)表达，则有和B矩阵类似的表达式。","同时，将系数c写成矩阵的形式，记为C。")
        grid_C = make_grid(self, 8, 8, mat_l=MAT_C, mat_g={"lgt": MAT_MK1, "btn": MAT8_0}, btn_c=C_COLOR, lgt_c=C_COLOR, sz=0.4)
        left_obj = add_left_labels(self, grid_C, list(range(8)), which="btn", dx=0.4)
        bottom_obj = add_bottom_label(self, grid_C, "C", which="btn", dy=0.6, color=C_COLOR)
        LAT_C = show_latex(self, LATEX_C, 0, 2.0)
        hl_cells(self, [grid_C], which="btn", indices=[(1,1),(0,2),(1,2)])
        hl_cells(self, [grid_C], which="btn", indices=[(1,3)], color=HL_COLOR_2)
        self.wait(2)
        show_subtitle(self, "注意，这里的乘以H的操作在系数上代表右移而不是左右扩散，", "因此表达式中只有x-1而没有x+1。")
        self.wait(2)
        show_subtitle(self, "这个C矩阵和后面提到的F矩阵息息相关。")
        self.wait(2)
        del_cells(self, [grid_C], which="btn", indices=[(1,1),(0,2),(1,2)])
        del_cells(self, [grid_C], which="btn", indices=[(1,3)])
        del_latex(self, [LAT_BH, LAT_C])
        del_left_labels(self, left_obj)
        del_bottom_label(self, bottom_obj)
        del_grids(self, [grid_C])

        show_subtitle(self, "现在，如果我们将多个H相乘，也就是H^n，", "则其首行H^n(0)从单位矩阵n=0开始，看起来像是这样的。")
        grid_K = make_grid(self, 8, 8, mat_l=MAT_K, mat_g={"lgt": MAT_MK1, "btn": MAT8_0}, btn_c=K_COLOR, lgt_c=K_COLOR, sz=0.4)
        left_obj = add_left_labels(self, grid_K, list(range(8)), which="btn", dx=0.4)
        bottom_obj = add_bottom_label(self, grid_K, "K", which="btn", dy=0.6, color=K_COLOR)
        self.wait(2)
        show_subtitle(self, "我们把这个下三角矩阵记为K，即Krylov矩阵或扩散基矩阵。", "也就是说，对于K的第n行，有K(n)=H^n(0)。")
        LAT_K1 = show_latex(self, "<cK>K(n)=k(n-1)*<cH>H=H^n(0)", 0, 2.5)
        self.wait(2)
        show_subtitle(self, "这里下一行是上一行乘以H，也就是上一行左右扩散的叠加。", "因此对于K的每个元素，有上述递推公式。")
        LAT_K2 = show_latex(self, LATEX_K, 0, 2.0)
        hl_cells(self, [grid_K], which="btn", indices=[(0,2),(2,2)])
        hl_cells(self, [grid_K], which="btn", indices=[(1,3)], color=HL_COLOR_2)
        self.wait(2)
        del_cells(self, [grid_K], which="btn", indices=[(0,2),(2,2)])
        del_cells(self, [grid_K], which="btn", indices=[(1,3)])
        del_latex(self, [LAT_K1, LAT_K2])
        del_left_labels(self, left_obj)
        del_bottom_label(self, bottom_obj)
        del_grids(self, [grid_K])

        show_subtitle(self, "现在，定义多项式p(x)。", "我们的目标是把B拆分成H^n。")
        LAT_P1 = show_latex(self, "<cP>p(x)=p0*x^0+p1*x^1+p2*x^2...=SUM+(pi*x^i)", 0, 2.5)
        self.wait(2)
        show_subtitle(self, "将矩阵H代入多项式p(x)，得到p(H)，并用其表示矩阵B。")
        LAT_P2 = show_latex(self, "<cB>B<cP>=p(<cH>H<cP>)=p0*<cH>H^0<cP>⊕p1*<cH>H^1<cP>⊕p2*<cH>H^2<cP>⊕...=SUM⊕(pi*<cH>H^i<cP>)", 0, 2.0)
        self.wait(2)
        show_subtitle(self, "这样，原始求x的问题就变为了p(H)x=y。")
        LAT_P3 = show_latex(self, "<cB>B<cX>x<cP>=p(<cH>H<cP>)<cX>x<cP>=<cY>y", 0, 1.5)
        self.wait(2)
        show_subtitle(self, "现在，我们需要把多项式p(H)的系数计算出来。", "这个系数构成的向量我们记为p。")
        LAT_P4 = show_latex(self, "<cP>p=(p0,p1,p2...)", 0, 1.0)
        self.wait(2)
        show_subtitle(self, "为了简化运算，我们只关心矩阵第一行B(0)，记为b。", "根据刚才的定义，我们可以得到b=K*p。")
        LAT_P5 = show_latex(self,
            "<cB>b<br>"
            "<cB>=B(0)<br>"
            "<cP>=p(<cH>H(0)<cP>)<br>"
            "<cP>=p0*<cH>H^0(0)<cP>⊕p1*<cH>H^1(0)<cP>⊕p2*<cH>H^2(0)<cP>⊕...<br>"
            "<cP>=p0*<cK>K(0)<cP>⊕p1*<cK>K(1)<cP>⊕p2*<cK>K(2)<cP>⊕...<br>"
            "<cP>=<cK>K<cP>p",
            0, -0.5)
        self.wait(2)
        del_latex(self, [LAT_P1, LAT_P2, LAT_P3, LAT_P4])
        LAT_B = show_latex(self, "<cB>b=<cK>K<cP>p", 0, 2.0, show=False)
        trans_latex(self, LAT_P5, LAT_B)

        mul_vec_mat(self, w=7, h=7, mat=MAT_K, vec=VEC_P7, mat_color=K_COLOR, vec_color=P_COLOR, res_color=B_COLOR, mat_label="K", vec_label="p", res_label="b", sz=0.4)
        del_latex(self, [LAT_B])

        show_subtitle(self, "为了求得p，我们可以将两边同时乘以K的逆矩阵K^-1。", "为了方便我们记为F，又称反Krylov矩阵或解耦矩阵。")
        grid_F = make_grid(self, 8, 8, mat_l=MAT_F, mat_g={"lgt": MAT_MK1, "btn": MAT8_0}, btn_c=F_COLOR, lgt_c=F_COLOR, sz=0.4)
        left_obj = add_left_labels(self, grid_F, list(range(8)), which="btn", dx=0.4)
        bottom_obj = add_bottom_label(self, grid_F, "F", which="btn", dy=0.6, color=F_COLOR)
        hl_cells(self, [grid_F], which="btn", indices=[(1,1),(0,2)])
        hl_cells(self, [grid_F], which="btn", indices=[(1,3)], color=HL_COLOR_2)
        self.wait(2)
        show_subtitle(self, "这个矩阵F也是下三角矩阵，并且和矩阵K看上去差不多，不过并不相同。", "事实上，这个矩阵F也满足类似的性质。")
        LAT_K = show_latex(self, LATEX_K, 0, 2.5)
        LAT_F = show_latex(self, LATEX_F, 0, 2.0)
        del_bottom_label(self, bottom_obj)
        del_grids(self, [grid_F], kp_bd=True)
        grid_K = make_grid(self, 8, 8, mat_l=MAT_K, mat_g={"lgt": MAT_MK1, "btn": MAT8_0}, btn_c=K_COLOR, lgt_c=K_COLOR, sz=0.4)
        bottom_obj = add_bottom_label(self, grid_K, "K", which="btn", dy=0.6, color=K_COLOR)
        hl_cells(self, [grid_K], which="btn", indices=[(0,2),(2,2)])
        hl_cells(self, [grid_K], which="btn", indices=[(1,3)], color=HL_COLOR_2)
        self.wait(1)
        del_bottom_label(self, bottom_obj)
        del_grids(self, [grid_K], kp_bd=True)
        grid_F0 = make_grid(self, 8, 8, mat_l=MAT_F, mat_g={"lgt": MAT_MK1, "btn": MAT8_0}, btn_c=F_COLOR, lgt_c=F_COLOR, sz=0.4)
        bottom_obj = add_bottom_label(self, grid_F0, "F", which="btn", dy=0.6, color=F_COLOR)
        hl_cells(self, [grid_F0], which="btn", indices=[(1,1),(0,2)])
        hl_cells(self, [grid_F0], which="btn", indices=[(1,3)], color=HL_COLOR_2)
        del_grids(self, [grid_K, grid_F])
        self.wait(2)
        show_subtitle(self, "有兴趣的小伙伴可以试着证明一下，", "使用这两个性质构造的矩阵K和F，证明S=K*F为单位矩阵I。")
        self.wait(2)
        show_subtitle(self, "提示：矩阵S=K*F满足十字偶校验约束，因此有以上递推公式。")
        LAT_S = show_latex(self, "<cI>S(n,x)=S(n-1,x-1)⊕S(n-1,x+1)⊕S(n-2,x)", 0, -2.5)

        self.wait(2)
        del_cells(self, [grid_F0], which="btn", indices=[(1,1),(0,2)])
        del_cells(self, [grid_F0], which="btn", indices=[(1,3)])
        del_latex(self, [LAT_K, LAT_F, LAT_S])
        del_left_labels(self, left_obj)

        show_subtitle(self, "这里说明一下，矩阵F的每行对应多项式f(n,x)，", "也就是上一集视频《解的数量》章节中提到的OEIS中的Fibonacci多项式。")
        LAT_F = show_latex(self, "<cF>f(n,x)=x*f(n-1,x)⊕f(n-2,x)", 0, 2.5)
        LAT_F2 = show_latex(self, "<cF>F(n,x)=F(n-1,x-1)⊕F(n-2,x)", 0, 2.0)
        self.wait(2)
        del_bottom_label(self, bottom_obj)
        del_grids(self, [grid_F0])
        show_subtitle(self, "此外，刚才递推得到的C矩阵对应多项式c(n,x)，", "其实也就是这里提到的f(n,x+1)。")
        LAT_C = show_latex(self, "<cC>c(n,x)=x*c(n-1,x)⊕c(n-1,x)⊕c(n-2,x)", 0, 1.0)
        LAT_C2 = show_latex(self, "<cC>C(n,x)=C(n-1,x-1)⊕C(n-1,x)⊕C(n-2,x)", 0, 0.5)
        LAT_CF = show_latex(self, "<cC>c(n,x)<cF>=f(n,x+1)", 0, -0.5)
        show_subtitle(self, "这个证明也不难，大家可以使用公式求出F和C的递推公式，", "或者由递推公式反推。")
        self.wait(2)
        show_subtitle(self, "同时，B(n)矩阵也可以表示为以上形式。", "这里的H⊕I等价于x+1。")
        LAT_B1 = show_latex(self, "<cB>B(n)=B(n-1)*(<cH>H<cB>⊕<cI>I<cB>)⊕B(n-2)", 0, -1.5)
        LAT_B2 = show_latex(self, LATEX_B, 0, -2.0)
        self.wait(2)
        del_latex(self, [LAT_F, LAT_F2, LAT_C, LAT_C2, LAT_CF, LAT_B1 , LAT_B2])

        show_subtitle(self, "让我们继续求p。由于F和K互逆，我们有：F*b=F*K*p=p。", "这样我们便求出了p。")
        LAT_P = show_latex(self, LATEX_P, 0, 2.0)
        grid_F0 = make_grid(self, 8, 8, mat_l=MAT_F, mat_g={"lgt": MAT_MK1, "btn": MAT8_0}, btn_c=F_COLOR, lgt_c=F_COLOR, sz=0.4)
        move_grid(self, grid_F0, btn_y=-0.2, lgt_y=-0.2, btn_x=0.2, lgt_x=0.2)
        grid_F2 = make_grid(self, 7, 7, mat_l=MAT_F, mat_g={"lgt": MAT_MK1, "btn": MAT8_0}, btn_c=F_COLOR, lgt_c=F_COLOR, sz=0.4)
        self.wait(2)
        del_grids(self, [grid_F0])

        show_subtitle(self, "这里，为了和视频演示一致，由于b是竖着的，写为p=F*b，省去了转置符号。", "对于矩阵乘法运算来说，则有P=B''*F。")
        ctx = mul_vec_mat_begin(self, w=7, h=7, mat=MAT_F, vec=VEC_B7, mat_color=F_COLOR, vec_color=B_COLOR, res_color=P_COLOR, mat_label="F", vec_label="b", res_label="p", sz=0.4)
        mul_vec_mat_vec_and_rows(self, ctx)
        mul_vec_mat_accumulate(self, ctx)
        del_grids(self, [grid_F2])
        grid_P0 = make_grid(self, 7, 1, mat_l=[VEC_P7], btn_y=-2, lgt_y=-2, btn_c=P_COLOR, lgt_c=P_COLOR, sz=0.4)
        mul_vec_mat_cleanup(self, ctx, clear_res=True)
        move_grid(self, grid_P0, btn_y=-1.4, lgt_y=-1.4, btn_x=-0.2, lgt_x=-0.2)

        show_subtitle(self, "将多项式p(x)写成矩阵的形式，记为P。")
        grid_P = make_grid(self, 8, 8, mat_l=MAT_P, mat_g={"lgt": MAT_MK2, "btn": MAT8_0}, btn_c=P_COLOR, lgt_c=P_COLOR, sz=0.4)
        del_grids(self, [grid_P0])
        left_obj = add_left_labels(self, grid_P, list(range(8)), which="btn", dx=0.4)
        bottom_obj = add_bottom_label(self, grid_P, "P", which="btn", dy=0.6, color=P_COLOR)
        self.wait(2)
        del_left_labels(self, left_obj)
        del_bottom_label(self, bottom_obj)
        del_grids(self, [grid_P])

        show_subtitle(self, "有了F*b=p之后，后续的计算我们都不需要用到完整的B，", "而只需要这个第一行b。")
        mul_vec_mat(self, w=7, h=7, mat=MAT_F, vec=VEC_B7, mat_color=F_COLOR, vec_color=B_COLOR, res_color=P_COLOR, mat_label="F", vec_label="b", res_label="p", sz=0.4)
        del_latex(self, [LAT_P])
        show_subtitle(self, "这是因为我们已经将问题从Bx=y转为了p(H)=y。", "由此，在前面说到的生成矩阵也只需要计算第一行b。")
        cols, n = 7, 7
        sz = 0.4
        rows = n + 1
        G5_ = [[None] for _ in range(rows)]
        top_objs = [[None] for _ in range(rows)]
        left_objs = [[None] for _ in range(rows)]
        start_y = (rows - 1) * sz / 2
        for k in range(rows):
            mx = -sz / 2
            my = start_y - k * sz
            G5_[k][0] = make_grid(self, w=cols, h=1, lgt_x=mx, btn_x=mx, lgt_y=my, btn_y=my, sz=sz, mat=[[0]*cols], mat_l=[MAT7K[k][0][:]], show=True, lgt_c=B_COLOR)
            if k == 0: top_objs[k][0] = add_top_labels(self, G5_[k][0], ["B1","B2","B3","B4","B5","B6","B7"], which="btn", scale=0.4, rt=0.01)
            left_objs[k][0] = add_left_labels(self, G5_[k][0], [f"n{k}"], which="btn", scale=0.4, rt=0.01)
        self.wait(2)
        del_left_labels(self, left_objs)
        del_top_labels(self, top_objs)

        show_subtitle(self, "由于在不同n的情况下计算b的方式是一样的，", "我们可以把n-1情况下算出的b，直接用于计算n的情况。")
        LAT_B1 = show_latex(self, "<cB>b(n,x)=b(n-1,x-1)⊕b(n-1,x)⊕b(n-1,x+1)⊕b(n-2,x)", 0, 2.5)
        LAT_B2 = show_latex(self, LATEX_B, 0, 2.0)
        grid_B = make_grid(self, 8, 8, mat_l=MAT_B, mat_g={"lgt": MAT_MK1, "btn": MAT8_0}, btn_c=B_COLOR, lgt_c=B_COLOR, sz=0.4)
        del_grids(self, G5_, rt=0.01)
        left_obj = add_left_labels(self, grid_B, list(range(8)), which="btn", dx=0.4)
        bottom_obj = add_bottom_label(self, grid_B, "B'", which="btn", dy=0.6, color=B_COLOR)
        hl_cells(self, [grid_B], which="btn", indices=[(1,1),(0,2),(1,2),(2,2)])
        hl_cells(self, [grid_B], which="btn", indices=[(1,3)], color=HL_COLOR_2)
        self.wait(1)
        show_subtitle(self, "这样，如果我们是从n=0开始计算的，", "我们只需要O(n)的时间复杂度便可求出b。")
        self.wait(2)
        del_latex(self, [LAT_B1, LAT_B2])
        del_cells(self, [grid_B], which="btn", indices=[(1,1),(0,2),(1,2),(2,2)])
        del_cells(self, [grid_B], which="btn", indices=[(1,3)])
        del_left_labels(self, left_obj)
        del_bottom_label(self, bottom_obj)
        del_grids(self, [grid_B])

        show_subtitle(self, "同样，计算K和F也是如此。因为每行之间有递推公式，", "如果从n=0开始计算，也可以在O(n)时间内求出。")
        LAT_K = show_latex(self, LATEX_K, 0, 2.0)
        grid_K = make_grid(self, 8, 8, mat_l=MAT_K, mat_g={"lgt": MAT_MK1, "btn": MAT8_0}, btn_c=K_COLOR, lgt_c=K_COLOR, sz=0.4)
        left_obj = add_left_labels(self, grid_K, list(range(8)), which="btn", dx=0.4)
        bottom_obj = add_bottom_label(self, grid_K, "K", which="btn", dy=0.6, color=K_COLOR)
        hl_cells(self, [grid_K], which="btn", indices=[(0,2),(2,2)])
        hl_cells(self, [grid_K], which="btn", indices=[(1,3)], color=HL_COLOR_2)
        self.wait(1)
        del_latex(self, [LAT_K])
        del_cells(self, [grid_K], which="btn", indices=[(0,2),(2,2)])
        del_cells(self, [grid_K], which="btn", indices=[(1,3)])
        del_left_labels(self, left_obj)
        del_bottom_label(self, bottom_obj)
        del_grids(self, [grid_K])
        LAT_F = show_latex(self, LATEX_F, 0, 2.0)
        grid_F = make_grid(self, 8, 8, mat_l=MAT_F, mat_g={"lgt": MAT_MK1, "btn": MAT8_0}, btn_c=F_COLOR, lgt_c=F_COLOR, sz=0.4)
        left_obj = add_left_labels(self, grid_F, list(range(8)), which="btn", dx=0.4)
        bottom_obj = add_bottom_label(self, grid_F, "F", which="btn", dy=0.6, color=F_COLOR)
        hl_cells(self, [grid_F], which="btn", indices=[(1,1),(0,2)])
        hl_cells(self, [grid_F], which="btn", indices=[(1,3)], color=HL_COLOR_2)
        show_subtitle(self, "如果需要直接计算特定n，可以用别的方式优化到O(n*log(n))。", "因为这里的算法不涉及这个优化，因此不再赘述。")
        self.wait(2)
        del_latex(self, [LAT_F])
        del_cells(self, [grid_F], which="btn", indices=[(1,1),(0,2)])
        del_cells(self, [grid_F], which="btn", indices=[(1,3)])
        del_left_labels(self, left_obj)
        del_bottom_label(self, bottom_obj)

        show_subtitle(self, "为了求出p=F*b，我们需要将向量和矩阵相乘，", "一般情况下时间复杂度是O(n^2)。")
        move_grid(self, grid_F, btn_y=-0.2, lgt_y=-0.2, btn_x=0.2, lgt_x=0.2)
        grid_F2 = make_grid(self, 7, 7, mat_l=MAT_F, mat_g={"lgt": MAT_MK1, "btn": MAT8_0}, btn_c=F_COLOR, lgt_c=F_COLOR, sz=0.4)
        del_grids(self, [grid_F])
        LAT_P = show_latex(self, LATEX_P, 0, 2.0)
        ctx = mul_vec_mat_begin(self, w=7, h=7, mat=MAT_F, vec=VEC_B7, mat_color=F_COLOR, vec_color=B_COLOR, res_color=P_COLOR, mat_label="F", vec_label="b", res_label="p", sz=0.4)
        mul_vec_mat_vec_and_rows(self, ctx)
        mul_vec_mat_accumulate(self, ctx)
        show_subtitle(self, "因为矩阵F是有递推规律的，理论上使用FFT等算法，", "可以把乘法优化到O(n*log(n))。")
        del_latex(self, [LAT_P])
        del_grids(self, [grid_F2])
        mul_vec_mat_cleanup(self, ctx, clear_res=True)

        show_subtitle(self, "事实上，这里计算p的时候，我们将B''的对角线去除了，有P=B''*F。", "假如我们保留B''的对角线，则有C=B'*F。")
        LAT_P = show_latex(self, "<cP>P=<cB>B''<cF>F", 0, 2.0)
        grid_B = make_grid(self, 8, 8, mat_l=MAT_B, mat_g={"lgt": MAT_MK2, "btn": MAT8_0}, btn_c=B_COLOR, lgt_c=B_COLOR, sz=0.4)
        left_obj = add_left_labels(self, grid_B, list(range(8)), which="btn", dx=0.4)
        bottom_obj = add_bottom_label(self, grid_B, "B''", which="btn", dy=0.6, color=B_COLOR)
        self.wait(2)
        del_latex(self, [LAT_P])
        LAT_C = show_latex(self, "<cC>C=<cB>B'<cF>F", 0, 2.0)
        del_bottom_label(self, bottom_obj)
        grid_B0 = make_grid(self, 8, 8, mat_l=MAT_B, mat_g={"lgt": MAT_MK1, "btn": MAT8_0}, btn_c=B_COLOR, lgt_c=B_COLOR, sz=0.4, show=False)
        bottom_obj = add_bottom_label(self, grid_B0, "B'", which="btn", dy=0.6, color=B_COLOR)
        trans_grid(self,grid_B,grid_B0, keep_from=False);
        self.wait(2)
        del_latex(self, [LAT_C])
        del_left_labels(self, left_obj)
        del_bottom_label(self, bottom_obj)
        del_grids(self, [grid_B0])

        show_subtitle(self, "为了证明这一点，我们假定B'*F=C'，得出以上递推公式。", "由于C'的递推公式和C是相同的，因此这里的C'就是C，即C'=C=B'*F。")
        LAT_C0 = show_latex(self, 
            "<cC>C'(n,x)<br>"
            "<cC>=(<cB>B'<cC>*<cF>F<cC>)(n,x)<br>"
            "<cC>=Sum_j:[<cB>B'(n,j)<cC>*<cF>F(j,x)<cC>]<br>"
            "<cC>=Sum_j:[(<cB>B'(n-1,j-1)<cC>⊕<cB>B'(n-1,j)<cC>⊕<cB>B'(n-1,j+1)<cC>⊕<cB>B'(n-2,j))<cC>*<cF>F(j,x)<cC>]<br>"
            "<cC>=Sum_j:[<cB>B'(n-1,j-1)<cC>*<cF>F(j,x)<cC>⊕<cB>B'(n-1,j)<cC>*<cF>F(j,x)<cC>⊕<cB>B'(n-1,j+1)<cC>*<cF>F(j,x)<cC>⊕<cB>B'(n-2,j)<cC>*<cF>F(j,x)<cC>]<br>"
            "<cC>=Sum_j:[<cB>B'(n-1,j)<cC>*<cF>F(j+1,x)<cC>⊕<cB>B'(n-1,j)<cC>*<cF>F(j,x)<cC>⊕<cB>B'(n-1,j)<cC>*<cF>F(j-1,x)<cC>⊕<cB>B'(n-2,j)<cC>*<cF>F(j,x)<cC>]<br>"
            "<cC>=Sum_j:[<cB>B'(n-1,j)<cC>*<cF>F(j,x-1)<cC>⊕<cB>B'(n-1,j)<cC>*<cF>F(j-1,x-1)<cC>⊕<cB>B'(n-1,j)<cC>*<cF>F(j-2,x)<cC>⊕<cB>B'(n-2,j)<cC>*<cF>F(j,x)<cC>]<br>"
            "<cC>=Sum_j:[<cB>B'(n-1,j)<cC>*<cF>F(j,x-1)<cC>⊕<cB>B'(n-1,j)<cC>*(<cF>F(j-1,x-1)<cC>⊕<cF>F(j-2,x))<cC>⊕<cB>B'(n-2,j)<cC>*<cF>F(j,x)<cC>]<br>"
            "<cC>=Sum_j:[<cB>B'(n-1,j)<cC>*<cF>F(j,x-1)<cC>⊕<cB>B'(n-1,j)<cC>*<cF>F(j,x)<cC>⊕<cB>B'(n-2,j)<cC>*<cF>F(j,x)<cC>]<br>"
            "<cC>=C'(n-1,x-1)<cC>⊕C'(n-1,x)<cC>⊕C'(n-2,x)",
             0, 1.0, font_size=FONT_SIZE_SMALL)
        self.wait(2)
        LAT_C = show_latex(self, "<cC>C'(n,x)=C'(n-1,x-1)<cC>⊕C'(n-1,x)<cC>⊕C'(n-2,x)", 0, 1.0, show=False)
        trans_latex(self, LAT_C0, LAT_C)
        self.wait(2)

        show_subtitle(self, "由于C=B'*F，因此P=C⊕F。", "我们可以用递推公式计算出C，和F叠加直接求得P，无需使用矩阵乘法。")
        LAT_CF = show_latex(self, "<cP>P=<cB>B''<cP>*<cF>F<cP>=(<cB>B'<cP>⊕<cI>I<cP>)*<cF>F=<cB>B'<cP>*<cF>F<cP>⊕<cI>I<cP>*<cF>F<cP>=<cC>C<cP>⊕<cF>F", 0, 0.0)
        self.wait(2)

        show_subtitle(self, "同时，由于P=C⊕F，因此P也可以写成这个递推公式，", "从而无需B，C或F，直接在O(n)的时间内，由P自己推得。")
        LAT_P = show_latex(self, "<cP>P(n,x)=P(n-1,x)⊕P(n-2,x-1)⊕P(n-2,x-2)⊕P(n-3,x)⊕P(n-4,x)", 0, -0.5)
        self.wait(2)
        show_subtitle(self, "这个证明较长，因此这里就不展示出来了。", "有兴趣的观众可以从C和F的递推公式进行证明。")
        self.wait(2)
        del_latex(self, [LAT_C, LAT_CF, LAT_P])

        show_subtitle(self, "现在，我们已求得了p，并将原始问题转换为了p(H)x=y。", "那这又有什么用呢？")
        LAT_Y = show_latex(self, "<cB>B<cX>x<cP>=p(<cH>H<cP>)<cX>x<cP>=<cY>y", 0, 0.0, font_size=FONT_SIZE_LARGE)
        self.wait(2)
        del_latex(self, [LAT_Y])

        show_subtitle(self, "试想一下，如果有一个多项式q(x)，", "满足q(x)*p(x)=1 mod f(x)。")
        LAT_Q1 = show_latex(self, "<cQ>q(x)<cP>p(x)<cI>=1 mod <cF>f(x)", 0, 2.5)

        sz=0.35
        poly_7 = show_poly_mul(self, VEC_P7, VEC_Q7, VEC_F7, VEC_G7, sz=sz)
        self.wait(2)
        grid_q1 = make_grid(self, 1, 7, mat_l=[[v] for v in VEC_Q7], btn_x=-(13/2.0+2.0)*sz, lgt_x=-(13/2.0+2.0)*sz, btn_c=Q_COLOR, lgt_c=Q_COLOR, sz=sz)
        clear_poly_mul(self, poly_7)

        show_subtitle(self, "这里的f(x)就是前面提到的多项式f(n,x)。", "那么，将原始两边同时乘以q(H)，便有：x=q(H)*y。")
        LAT_Q2 = show_latex(self, "<cX>x=<cQ>q(<cH>H<cQ>)<cP>p(<cH>H<cP>)<cX>x=<cQ>q(<cH>H<cQ>)<cY>y", 0, 2.0)
        sz=0.4
        grid_q0 = make_grid(self, 7, 1, mat_l=[VEC_Q7], btn_y=(7-1)*sz/2, lgt_y=(7-1)*sz/2, btn_c=P_COLOR, lgt_c=Q_COLOR, sz=sz, show=False)
        trans_grid(self, grid_q1, grid_q0)
        self.wait(2)

        show_subtitle(self, "这样，我们就能立刻求出x。")
        mul_vec_mat(self, w=7, h=7, mat=MAT_QH, vec=VEC_Y7, mat_color=Q_COLOR, vec_color=Y_COLOR, res_color=X_COLOR, mat_label="Q'", vec_label="y", res_label="x", sz=0.4)

        show_subtitle(self, "让我把这样的多项式q(x)我们称之为p(x)的逆多项式。", "那么，如何求出逆多项式q(x)呢？")
        label_q = add_left_labels(self, grid_q0, ["q"], which="btn", dx=0.4)
        self.wait(2)
        del_left_labels(self, [label_q])
        del_grids(self, [grid_q0])

        dx, dy, sz = 2.5, 0.5, 0.4
        show_subtitle(self, "我们可以使用扩展欧几里得算法，利用f(x)和p(x)来求取q(x)。")
        euc = euclid_create(self, VEC_F7, VEC_P7, VEC_O7, VEC_E7, F_COLOR, P_COLOR, I_COLOR, Q_COLOR, dx, dy, sz)
        self.wait(2)
        show_subtitle(self, "这里，我们同时定义一个零多项式o(x)和单位多项式e(x)，", "在对f(x)和p(x)操作的同时，对o(x)和e(x)做相同的操作。")
        self.wait(2)

        show_subtitle(self, "我们使用辗转相减法，将p(x)右移，", "使其最高系数和f(x)对齐，然后叠加到f(x)上。")
        euclid_ops(self, euc, OPS_7, start=0, end=0)
        self.wait(2)

        show_subtitle(self, "叠加后，如果f(x)的最高系数仍旧大于等于p(x)，", "则继续右移p(x)并叠加到f(x)上。")
        euclid_ops(self, euc, OPS_7, start=1, end=1)
        self.wait(2)

        show_subtitle(self, "否则，当f(x)的最高系数小于p(x)时，将p(x)和f(x)互换。")
        euclid_ops(self, euc, OPS_7, start=2, end=2)
        self.wait(2)

        show_subtitle(self, "重复这样操作，直到f(x)最终被叠加为零。")
        euclid_ops(self, euc, OPS_7, start=3)
        self.wait(2)

        show_subtitle(self, "最后剩下的p(x)则为两个多项式的最大公因子，记为g(x)，", "同时，最后剩下的e(x)则为p(x)的逆，也就是q(x)。")
        euc2 = euclid_done(self, euc, VEC_G7, G_COLOR, dx, dy, sz)
        self.wait(2)
        grid_e0 = make_grid(self, w=8, h=1, lgt_x= dx, btn_x= dx, lgt_y=-dy, btn_y=-dy, sz=sz, mat_l=[VEC_Q7], btn_c=Q_COLOR, lgt_c=Q_COLOR, rt=0.01)
        euclid_clear(self, euc2)

        show_subtitle(self, "将q(x)写成矩阵Q。注意，这里的矩阵不是后面提到的完整的逆矩阵Q'，", "而是多个q(x)拼接起来。")
        move_grid(self, grid_e0, btn_y=-1.4, lgt_y=-1.4)
        grid_Q = make_grid(self, 8, 8, mat_l=MAT_Q, mat_g={"lgt": MAT_MK2, "btn": MAT8_0}, btn_c=Q_COLOR, lgt_c=Q_COLOR, sz=0.4)
        left_obj = add_left_labels(self, grid_Q, list(range(8)), which="btn", dx=0.4)
        bottom_obj = add_bottom_label(self, grid_Q, "Q", which="btn", dy=0.6, color=G_COLOR)
        del_grids(self, [grid_e0])
        self.wait(2)
        del_latex(self, [LAT_Q1, LAT_Q2])
        del_left_labels(self, left_obj)
        del_bottom_label(self, bottom_obj)
        del_grids(self, [grid_Q])

        show_subtitle(self, "这里，由于我们已求得q(x)。我们也可以利用这个式子来求x。")
        LAT_Q3 = show_latex(self, 
            "<cX>x<br><cQ>=q(<cH>H<cQ>)<cY>y<br>"
            "<cQ>=(q0*<cH>H^0<cQ>⊕q1*<cH>H^1<cQ>⊕q2*<cH>H^2<cQ>⊕...)*<cY>y<br>"
            "<cQ>=q0*<cH>H^0*<cY>y<cQ>⊕q1*<cH>H^1*<cY>y<cQ>⊕q2*<cH>H^2*<cY>y<cQ>⊕...<br>"
            "<cQ>=SUM:qi*<cH>H^i<cQ>*<cY>y",
             0, 1.0)
        self.wait(2)
        show_subtitle(self, "这里，我们可以从Y开始，不断将其和H相乘，", "使用左右扩散的办法计算下一个H^n*y，然后和qn叠加，得到x。")
        LAT_Q4 = show_latex(self, "<cX>x<cQ>=q(<cH>H<cQ>)<cY>y<cQ>=SUM:qi*<cH>H^i<cQ>*<cY>y", 0, 2.5, show=False)
        trans_latex(self, LAT_Q3, LAT_Q4)
        LAT_Y3 = show_latex(self, "<cY>Y'(n,x)=Y'(n-1,x-1)+Y'(n-1,x+1)", 0, 2.0)
        mul_vec_mat(self, w=7, h=7, mat=MAT_YK, vec=VEC_Q7, mat_color=Y_COLOR, vec_color=Q_COLOR, res_color=X_COLOR, mat_label="Y'", vec_label="q", res_label="x", sz=0.4)
        del_latex(self, LAT_Q4, LAT_Y3)

        show_subtitle(self, "另一方面，q(x)的系数也就是B的逆矩阵Q'的第一行，", "并且可以证明B的逆矩阵Q'也满足十字偶校验约束。")
        LAT_Q5 = show_latex(self, "<cX>x<cQ>=Q'<cY>y<cQ>", 0, 2.5)
        ctx = mul_vec_mat_begin(self, w=7, h=7, mat=MAT_QH, vec=VEC_Y7, mat_color=Q_COLOR, vec_color=Y_COLOR, res_color=X_COLOR, mat_label="Q'", vec_label="y", res_label="x", sz=0.4)
        self.wait(2)

        show_subtitle(self, "因此，也可以通过递推公式，", "利用q(x)直接求出整个逆矩阵Q'，然后再和y相乘获得x。")
        mul_vec_mat_vec_and_rows(self, ctx)
        mul_vec_mat_accumulate(self, ctx)
        self.wait(1)

        show_subtitle(self, "不过，这整个求解的过程有一个问题，", "那就是我们假设满足q(x)p(x)=1 mod f(x)的多项式q(x)存在。")
        self.wait(2)

        show_subtitle(self, "如果这样的多项式q(x)不存在，我们又当如何呢？")
        self.wait(2)
        mul_vec_mat_cleanup(self, ctx, clear_res=True)
        del_latex(self, LAT_Q5)

#——————————————————————

        show_title(self, "不可逆矩阵")

        show_subtitle(self, "在上一集视频《解的数量》章节中，我们提到公式r'(n)。")
        LAT_R = show_latex(self, "<cR>r'(n)=deg(<cG>gcd(<cF>f(n,x)<cG>,<cC>c(n,x)<cG>)<cR>)", 0, 1.0)
        self.wait(2)
        show_subtitle(self, "这里，gcd表示最大公因子。", "不难发现，这里的gcd(f,c)就是前面扩展欧几里得算法中的g(x)。")
        LAT_G = show_latex(self, "<cG>g(n,x)=gcd(<cF>f(n,x)<cG>,<cC>c(n,x)<cG>)", 0, 0.5)
        self.wait(2)
        show_subtitle(self, "同时，由于F=C+P，因此gcd(f,c)和gcd(f,p)是相等的。")
        LAT_GP = show_latex(self, "<cG>g(n,x)=gcd(<cF>f(n,x)<cG>,<cC>c(n,x)<cG>)=gcd(<cF>f(n,x)<cG>,<cP>p(n,x)<cG>)", 0, 0.0)
        self.wait(2)
        show_subtitle(self, "deg则表示最高次幂。r'代表矩阵B丢失的秩，也就是n-r。", "r'的值决定了解的数量，即2^r'。")
        self.wait(2)
        show_subtitle(self, "可以发现，如果B是可逆的，则g(x)=1，r'=0，n=r-r'=r。")
        self.wait(2)
        del_latex(self, [LAT_R, LAT_G, LAT_GP])

        show_subtitle(self, "将g(x)写成矩阵的形式，记为G。")
        grid_G = make_grid(self, 8, 8, mat_l=MAT_G, mat_g={"lgt": MAT_MK1, "btn": MAT8_0}, btn_c=G_COLOR, lgt_c=G_COLOR, sz=0.4)
        left_obj = add_left_labels(self, grid_G, list(range(8)), which="btn", dx=0.4)
        bottom_obj = add_bottom_label(self, grid_G, "G", which="btn", dy=0.6, color=G_COLOR)
        LAT_G = show_latex(self, LATEX_G, 0, 2.0)
        hl_cells(self, [grid_G], which="btn", indices=[(0,0),(0,1),(0,2),(0,3),(4,4),(2,5),(0,6),(0,7)], color=HL_COLOR_1)
        self.wait(2)

        show_subtitle(self, "不难注意到，只有当矩阵B为可逆矩阵时，g(x)=1，", "并且g(x)的最高次幂为n-r=r'。")
        self.wait(2)
        del_cells(self, [grid_G], which="btn", indices=[(0,0),(0,1),(0,2),(0,3),(4,4),(2,5),(0,6),(0,7)])
        del_latex(self, [LAT_G])
        del_left_labels(self, left_obj)
        del_bottom_label(self, bottom_obj)
        del_grids(self, [grid_G])

        sz = 0.4
        show_subtitle(self, "例如，当n=5时的时候，", "高斯消元后的B的伪逆矩阵Q'和单元矩阵E'矩阵是这样的。")
        LAT_G = show_latex(self, "<cB>B<cQ>Q'<cE>=E'", 0, 2.0)
        grid_B5 = make_grid(self, 5, 5, lgt_x=-3, btn_x=-3, mat_l=MAT_B5, btn_c=B_COLOR, lgt_c=B_COLOR, sz=sz)
        grid_Q5 = make_grid(self, 5, 5, lgt_x=-0, btn_x=-0, mat_l=MAT_Q5, btn_c=Q_COLOR, lgt_c=Q_COLOR, sz=sz)
        grid_E5 = make_grid(self, 5, 5, lgt_x=+3, btn_x=+3, mat_l=MAT_E5, btn_c=E_COLOR, lgt_c=E_COLOR, sz=sz)
        topy_obj_B5 = add_top_labels(self, grid_B5, ["", "", "B", "", ""], which="btn")
        topy_obj_Q5 = add_top_labels(self, grid_Q5, ["", "", "Q'", "", ""], which="btn")
        topy_obj_E5 = add_top_labels(self, grid_E5, ["", "", "E'", "", ""], which="btn")
        self.wait(2)

        show_subtitle(self, "这里，矩阵B不可逆，其秩为r=3。", "我们以rxr为界将矩阵分为四块，则有这些结论。")
        grid_B5_Br = make_grid(self, 3, 3, lgt_x=-3.4, btn_x=-3.4, lgt_y=0.4, btn_y=0.4, mat_l=[[0]*3 for _ in range(3)], btn_c=B_COLOR, lgt_c=B_COLOR, sz=sz, rt=0.01)
        grid_Q5_Qr = make_grid(self, 3, 3, lgt_x=-0.4, btn_x=-0.4, lgt_y=0.4, btn_y=0.4, mat_l=[[0]*3 for _ in range(3)], btn_c=Q_COLOR, lgt_c=Q_COLOR, sz=sz, rt=0.01)
        grid_E5_Ir = make_grid(self, 3, 3, lgt_x=2.6, btn_x=2.6, lgt_y=0.4, btn_y=0.4, mat_l=[[0]*3 for _ in range(3)], btn_c=E_COLOR, lgt_c=E_COLOR, sz=sz, rt=0.01)
        bd_B5_Br = hl_bd(self, grid_B5_Br)
        bd_Q5_Qr = hl_bd(self, grid_Q5_Qr)
        bd_E5_Ir = hl_bd(self, grid_E5_Ir, color=HL_COLOR_2)
        self.wait(2)

        show_subtitle(self, "1. B矩阵左上角rxr的子矩阵满秩，", "并且为和Q'左上角rxr子矩阵互为逆矩阵。")
        self.wait(2)
        del_grids(self, [grid_B5_Br, grid_Q5_Qr, grid_E5_Ir])
        del_bd(self, bd_B5_Br)
        del_bd(self, bd_Q5_Qr)
        del_bd(self, bd_E5_Ir)

        show_subtitle(self, "2. Q'右下角和E'左上角为单位矩阵，", "Q'右上角和E'下方为零。")
        grid_Q5_I22 = make_grid(self, 2, 2, lgt_x=0.6, btn_x=0.6, lgt_y=-0.6, btn_y=-0.6, mat_l=[[0]*2 for _ in range(2)], btn_c=Q_COLOR, lgt_c=Q_COLOR, sz=sz, rt=0.01)
        grid_E5_I33 = make_grid(self, 3, 3, lgt_x=2.6, btn_x=2.6, lgt_y=0.4, btn_y=0.4, mat_l=[[0]*3 for _ in range(3)], btn_c=E_COLOR, lgt_c=E_COLOR, sz=sz, rt=0.01)
        grid_Q5_Z32 = make_grid(self, 2, 3, lgt_x=0.6, btn_x=0.6, lgt_y=0.4, btn_y=0.4, mat_l=[[0]*2 for _ in range(3)], btn_c=Q_COLOR, lgt_c=Q_COLOR, sz=sz, rt=0.01)
        grid_E5_Z25 = make_grid(self, 5, 2, lgt_x=3.0, btn_x=3.0, lgt_y=-0.6, btn_y=-0.6, mat_l=[[0]*5 for _ in range(2)], btn_c=E_COLOR, lgt_c=E_COLOR, sz=sz, rt=0.01)
        bd_Q5_I22 = hl_bd(self, grid_Q5_I22)
        bd_E5_I33 = hl_bd(self, grid_E5_I33)
        bd_Q5_Z32 = hl_bd(self, grid_Q5_Z32, color=HL_COLOR_2)
        bd_E5_Z25 = hl_bd(self, grid_E5_Z25, color=HL_COLOR_2)
        self.wait(2)
        del_grids(self, [grid_Q5_I22, grid_E5_I33, grid_Q5_Z32, grid_E5_Z25])
        del_bd(self, bd_Q5_Z32)
        del_bd(self, bd_E5_Z25)
        del_bd(self, bd_Q5_I22)
        del_bd(self, bd_E5_I33)

        show_subtitle(self, "3. Q'左下角Wr和E'右上角的静默操作相同，", "并且其值等于Q'左上角乘B右上角，或者B左下角乘以Q'左上角。")
        grid_B5_U1 = make_grid(self, 3, 2, lgt_x=-3.4, btn_x=-3.4, lgt_y=-0.6, btn_y=-0.6, mat_l=[[0]*3 for _ in range(2)], btn_c=B_COLOR, lgt_c=B_COLOR, sz=sz, rt=0.01)
        grid_B5_U2 = make_grid(self, 2, 3, lgt_x=-2.4, btn_x=-2.4, lgt_y=0.4, btn_y=0.4, mat_l=[[0]*2 for _ in range(3)], btn_c=B_COLOR, lgt_c=B_COLOR, sz=sz, rt=0.01)
        grid_Q5_Qr = make_grid(self, 3, 3, lgt_x=-0.4, btn_x=-0.4, lgt_y=0.4, btn_y=0.4, mat_l=[[0]*3 for _ in range(3)], btn_c=Q_COLOR, lgt_c=Q_COLOR, sz=sz, rt=0.01)
        grid_Q5_Wr = make_grid(self, 3, 2, lgt_x=-0.4, btn_x=-0.4, lgt_y=-0.6, btn_y=-0.6, mat_l=[[0]*3 for _ in range(2)], btn_c=Q_COLOR, lgt_c=Q_COLOR, sz=sz, rt=0.01)
        grid_E5_Wr = make_grid(self, 2, 3, lgt_x=3.6, btn_x=3.6, lgt_y=0.4, btn_y=0.4, mat_l=[[0]*2 for _ in range(3)], btn_c=E_COLOR, lgt_c=E_COLOR, sz=sz, rt=0.01)
        bd_Q5_Wr = hl_bd(self, grid_Q5_Wr)
        bd_E5_Wr = hl_bd(self, grid_E5_Wr)
        bd_B5_U1 = hl_bd(self, grid_B5_U1, color=HL_COLOR_2)
        bd_B5_U2 = hl_bd(self, grid_B5_U2, color=HL_COLOR_2)
        bd_Q5_Qr = hl_bd(self, grid_Q5_Qr, color=HL_COLOR_2)
        self.wait(2)
        del_grids(self, [grid_B5_U1, grid_B5_U2, grid_Q5_Qr, grid_Q5_Wr, grid_E5_Wr])
        del_bd(self, bd_B5_U1)
        del_bd(self, bd_B5_U2)
        del_bd(self, bd_Q5_Qr)
        del_bd(self, bd_Q5_Wr)
        del_bd(self, bd_E5_Wr)

        show_subtitle(self, "这些性质可以通过分块矩阵乘法，结合高斯消元和矩阵B的对称性得出，", "有兴趣的观众可以自行证明。")
        self.wait(2)
        grid_q4 = make_grid(self, 5, 1, lgt_y=sz*2, btn_y=sz*2, mat_l=[VEC_Q5_2], btn_c=Q_COLOR, lgt_c=Q_COLOR, sz=sz)
        del_latex(self, LAT_G)
        del_top_labels(self, [topy_obj_B5, topy_obj_Q5, topy_obj_E5])
        del_grids(self, [grid_B5, grid_Q5, grid_E5])

        show_subtitle(self, "可以发现，Q'不满足十字偶校验约束，因而无法通过公式递推求得。", "并且使用Q'第一行求得的x也不是原方程的解。")
        grid_q5 = make_grid(scene, 5, 1, lgt_y=sz*2, btn_y=sz*2, mat_l=[VEC_Q5_2], btn_c=Q_COLOR, lgt_c=Q_COLOR, sz=sz, show=False)
        trans_grid(self, grid_q4, grid_q5)
        mul_vec_mat(self, w=5, h=5, mat=MAT_QH5_2, vec=VEC_Y5, mat_color=Q_COLOR, vec_color=Y_COLOR, res_color=X_COLOR, mat_label="Q'", vec_label="y", res_label="x", sz=sz, wait=2.0)

        show_subtitle(self, "如果我们令Q'第一行为q(x)，并且和p(x)相乘，", "得到的g(x)不为1，最高次幂为4。")
        grid_q6 = make_grid(self, 1, 5, mat_l=[[v] for v in VEC_Q5_2], btn_x=-(9/2.0+2.0)*sz, lgt_x=-(9/2.0+2.0)*sz, btn_c=Q_COLOR, lgt_c=Q_COLOR, sz=sz, show=False)
        trans_grid(self, grid_q5, grid_q6)
        poly_5 = show_poly_mul(self, VEC_P5, VEC_Q5_2, VEC_F5, VEC_G5_2, sz=sz)
        self.wait(2)
        del_grids(self, [grid_q6])
        clear_poly_mul(self, poly_5)

        show_subtitle(self, "另一方面，如果我们直接使用扩展欧几里得法，", "通过p(x)和f(x)进行求解，得到的g(x)也不为1。")
        dx, dy, sz = 2.5, 0.5, 0.4
        euc = euclid_create(self, VEC_F5, VEC_P5, VEC_O5, VEC_E5, F_COLOR, P_COLOR, I_COLOR, Q_COLOR, dx, dy, sz)
        euclid_ops(self, euc, OPS_5, rt=0.3)
        euc2 = euclid_done(self, euc, VEC_G5, G_COLOR, dx, dy, sz)
        grid_q1 = make_grid(self, w=6, h=1, lgt_x=dx, btn_x=dx, lgt_y=-dy, btn_y=-dy, sz=sz, mat_l=[VEC_Q5], btn_c=Q_COLOR, lgt_c=Q_COLOR)
        self.wait(2)
        euclid_clear(self, euc2)

        show_subtitle(self, "将求得的q(x)和p(x)相乘，", "得到刚才求得的g(x)，其最高次幂为2。")
        grid_q2 = make_grid(self, 1, 5, mat_l=[[v] for v in VEC_Q5], btn_x=-(9/2.0+2.0)*sz, lgt_x=-(9/2.0+2.0)*sz, btn_c=Q_COLOR, lgt_c=Q_COLOR, sz=sz, show=False)
        trans_grid(self, grid_q1, grid_q2)
        poly_5 = show_poly_mul(self, VEC_P5, VEC_Q5, VEC_F5, VEC_G5, sz=sz)
        self.wait(2)
        clear_poly_mul(self, poly_5)

        show_subtitle(self, "这里，我们计算q(H)*y，发现求得的x也不是解。")
        grid_q3 = make_grid(scene, 5, 1, lgt_y=sz*2, btn_y=sz*2, mat_l=[VEC_Q5], btn_c=Q_COLOR, lgt_c=Q_COLOR, sz=sz, show=False)
        trans_grid(self, grid_q2, grid_q3)
        mul_vec_mat(self, w=5, h=5, mat=MAT_QH5, vec=VEC_Y5, mat_color=Q_COLOR, vec_color=Y_COLOR, res_color=X_COLOR, mat_label="q(H)", vec_label="y", res_label="x", sz=sz, wait=2.0)
        del_grids(self, [grid_q3])

        show_subtitle(self, "两种方法求得的q(x)和g(x)都不相同，", "g(x)都不为1，并且q(H)*y=x也都不是解。")
        grid_p = make_grid(self, w=5, h=1, lgt_x=-dx, btn_x=-dx, lgt_y=dy, btn_y=dy, sz=sz, mat_l=[VEC_P5], btn_c=P_COLOR, lgt_c=P_COLOR)
        grid_q1 = make_grid(self, w=5, h=1, lgt_x=-dx, btn_x=-dx, lgt_y=-dy, btn_y=-dy, sz=sz, mat_l=[VEC_Q5_2], btn_c=Q_COLOR, lgt_c=Q_COLOR)
        grid_q2 = make_grid(self, w=5, h=1, lgt_x=-dx, btn_x=-dx, lgt_y=-dy-sz, btn_y=-dy-sz, sz=sz, mat_l=[VEC_Q5], btn_c=Q_COLOR, lgt_c=Q_COLOR)
        label_p = add_left_labels(self, grid_p, ["p"], which="lgt", dx=sz)
        label_q1 = add_left_labels(self, grid_q1, ["q"], which="lgt", dx=sz)
        label_q2 = add_left_labels(self, grid_q2, ["q"], which="lgt", dx=sz)
        grid_f = make_grid(self, w=5, h=1, lgt_x=dx, btn_x=dx, lgt_y=dy, btn_y=dy, sz=sz, mat_l=[VEC_F5], btn_c=F_COLOR, lgt_c=F_COLOR)
        grid_g1 = make_grid(self, w=5, h=1, lgt_x=dx, btn_x=dx, lgt_y=-dy, btn_y=-dy, sz=sz, mat_l=[VEC_G5_2], btn_c=G_COLOR, lgt_c=G_COLOR)
        grid_g2 = make_grid(self, w=5, h=1, lgt_x=dx, btn_x=dx, lgt_y=-dy-sz, btn_y=-dy-sz, sz=sz, mat_l=[VEC_G5], btn_c=G_COLOR, lgt_c=G_COLOR)
        label_f = add_left_labels(self, grid_f, ["f"], which="lgt", dx=sz)
        label_g1 = add_left_labels(self, grid_g1, ["g"], which="lgt", dx=sz)
        label_g2 = add_left_labels(self, grid_g2, ["g"], which="lgt", dx=sz)
        self.wait(2)
        show_subtitle(self, "因此，如果g(x)不为1，则q(x)不满足q(x)p(x)=1 mod f(x)。", "或者说，满足q(x)p(x)=1 mod f(x)的q(x)不存在。")
        self.wait(2)
        del_left_labels(self, [label_p, label_q1, label_q2, label_f, label_g1, label_g2])
        del_grids(self, [grid_p, grid_q1, grid_q2, grid_f, grid_g1, grid_g2])

        show_subtitle(self, "那么对于不可逆的矩阵B，我们又有什么解决办法呢？")
        LAT_G = show_latex(self, "<cB>B<cQ>Q'<cE>=E'", 0, 2.0)
        grid_B5 = make_grid(self, 5, 5, lgt_x=-3, btn_x=-3, mat_l=MAT_B5, btn_c=B_COLOR, lgt_c=B_COLOR, sz=sz)
        grid_Q5 = make_grid(self, 5, 5, lgt_x=-0, btn_x=-0, mat_l=MAT_Q5, btn_c=Q_COLOR, lgt_c=Q_COLOR, sz=sz)
        grid_E5 = make_grid(self, 5, 5, lgt_x=+3, btn_x=+3, mat_l=MAT_E5, btn_c=E_COLOR, lgt_c=E_COLOR, sz=sz)
        topy_obj_B5 = add_top_labels(self, grid_B5, ["", "", "B", "", ""], which="btn")
        topy_obj_Q5 = add_top_labels(self, grid_Q5, ["", "", "Q'", "", ""], which="btn")
        topy_obj_E5 = add_top_labels(self, grid_E5, ["", "", "E'", "", ""], which="btn")
        self.wait(2)
        del_latex(self, LAT_G)
        del_top_labels(self, [topy_obj_B5, topy_obj_Q5, topy_obj_E5])
        del_grids(self, [grid_B5, grid_Q5, grid_E5])

#——————————————————————

        show_title(self, "首行方程法")

#——————————————————————

        show_title(self, "算法总结")

        table = show_algo_table(self, x=0.0, y=0.0, font_size=18, row_gap=0.075, col_gap=0.5)
        self.wait(2)
        hide_algo_table(self, table)

        show_title(self, "更快的算法")

        show_subtitle(self, "向量和矩阵的乘法，欧几里得算法，以及K矩阵的生成，", "理论上通过卷积，FFT或牛顿迭代法是有可能优化到O(n*log(n))的。")
        self.wait(2)
        show_subtitle(self, "考虑到UP主《信号与系统》、《数字信号处理》、《数值分析》等课程较差，", "暂时就不研究了。有兴趣的小伙伴可自行研究并留言。")
        self.wait(2)
        show_subtitle(self, "如果对视频中的内容有疑问，觉得视频内容表述不清，", "或者发现视频中的任何错误，也请大家多多留言和指证。谢谢大家观看！")
        self.wait(2)
        show_subtitle(self, "")
