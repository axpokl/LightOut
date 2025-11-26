from manimlib import *
import numpy as np

HL_COLOR_1 = RED
HL_COLOR_2 = YELLOW

L_COLOR  = "#55aaff"
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
Z_COLOR  = "#ffdd55"
D_COLOR  = "#aaffff"
ID_COLOR = "#ffffff"
X_COLOR  = "#ffaa55"
T_COLOR  = "#ffffaa"

COLOR_MAP = {
    "cH1": HL_COLOR_1,
    "cH2": HL_COLOR_2,
    "cL":  L_COLOR,
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
    "cZ":  Z_COLOR,
    "cD":  D_COLOR,
    "cID": ID_COLOR,
    "cX":  X_COLOR,
    "cT":  T_COLOR,
}

BD_W = 2
BD_W_SEL = 8

DEFAULT_FONT = "SimHei"

SCALE_LATEX = 1.0
SCALE_SUBTITLE = 1.25
SCALE_TITLE = 1.65

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

def trans_grid(scene, G_from, G_to, rt=0.8, keep_from=False, target_override=None, extra_anims=None,):
    if G_to["groups"]["lgt_bd_base"].get_stroke_opacity() == 0:
        G_to["groups"]["lgt_bd_base"].set_stroke(opacity=1)
    if G_to["groups"]["btn_bd_base"].get_stroke_opacity() == 0:
        G_to["groups"]["btn_bd_base"].set_stroke(opacity=1)
    def composite(G):
        return VGroup(
            G["groups"]["lgt_sp"],
            G["groups"]["lgt_bd_base"],
            G["groups"]["btn_sp"],
            G["groups"]["btn_bd_base"],
        )
    grp_from = composite(G_from).copy() if keep_from else composite(G_from)
    grp_to = target_override if target_override is not None else composite(G_to)
    if keep_from:
        scene.add(grp_from)
    if extra_anims:
        scene.play(ReplacementTransform(grp_from, grp_to), *extra_anims, run_time=rt)
    else:
        scene.play(ReplacementTransform(grp_from, grp_to), run_time=rt)
    if target_override is not None:
        try:
            scene.remove(grp_to)
        except Exception:
            pass
    scene.add(G_to["groups"]["lgt_bd_hl"])
    scene.add(G_to["groups"]["btn_bd_hl"])
    try:
        scene.bring_to_front(G_to["groups"]["lgt_bd_hl"])
        scene.bring_to_front(G_to["groups"]["btn_bd_hl"])
    except Exception:
        pass
    if not keep_from:
        del_grids(scene, G_from, rt=0.0)

def add_grid(scene, G_from, G_to, rt=0.8):
    ht_btn, wt_btn = G_to["params"]["h"], G_to["params"]["w"]
    hf_btn, wf_btn = G_from["params"]["h"], G_from["params"]["w"]
    ht_lgt = G_to["params"].get("h_l", ht_btn)
    wt_lgt = G_to["params"].get("w_l", wt_btn)
    hf_lgt = G_from["params"].get("h_l", hf_btn)
    wf_lgt = G_from["params"].get("w_l", wf_btn)
    btn_x = [[0] * wt_btn for _ in range(ht_btn)]
    for j in range(ht_btn):
        for i in range(wt_btn):
            b0 = 1 if G_to["btn"][j][i] else 0
            b1 = 1 if (j < hf_btn and i < wf_btn and G_from["btn"][j][i]) else 0
            btn_x[j][i] = b0 ^ b1
    lgt_x = [[0] * wt_lgt for _ in range(ht_lgt)]
    for j in range(ht_lgt):
        for i in range(wt_lgt):
            l0 = 1 if G_to["lgt"][j][i] else 0
            l1 = 1 if (j < hf_lgt and i < wf_lgt and G_from["lgt"][j][i]) else 0
            lgt_x[j][i] = l0 ^ l1
    lgt_sp_final = []
    for j in range(ht_lgt):
        for i in range(wt_lgt):
            m1 = G_to["lgt_sp"][j][i].copy()
            m1.set_opacity(1.0 if lgt_x[j][i] else 0.0)
            lgt_sp_final.append(m1)
    btn_sp_final = []
    for j in range(ht_btn):
        for i in range(wt_btn):
            m2 = G_to["btn_sp"][j][i].copy()
            m2.set_opacity(1.0 if btn_x[j][i] else 0.0)
            btn_sp_final.append(m2)
    grp_final = VGroup(
        VGroup(*lgt_sp_final),
        G_to["groups"]["lgt_bd_base"].copy(),
        VGroup(*btn_sp_final),
        G_to["groups"]["btn_bd_base"].copy(),
    )
    anims = []
    for j in range(ht_lgt):
        for i in range(wt_lgt):
            _queue_opacity_anim(G_to["lgt_sp"][j][i], 1.0 if lgt_x[j][i] else 0.0, anims)
    for j in range(ht_btn):
        for i in range(wt_btn):
            _queue_opacity_anim(G_to["btn_sp"][j][i], 1.0 if btn_x[j][i] else 0.0, anims)
    trans_grid(
        scene,
        G_from,
        G_to,
        rt=rt,
        keep_from=True,
        target_override=grp_final,
        extra_anims=anims,
    )
    for j in range(ht_btn):
        for i in range(wt_btn):
            G_to["btn"][j][i] = bool(btn_x[j][i])
            G_to["btn_sp"][j][i].set_opacity(1.0 if btn_x[j][i] else 0.0)
    for j in range(ht_lgt):
        for i in range(wt_lgt):
            G_to["lgt"][j][i] = bool(lgt_x[j][i])
            G_to["lgt_sp"][j][i].set_opacity(1.0 if lgt_x[j][i] else 0.0)

def swap_grid(scene, A, B, rt=0.8):
    pA, pB = A["params"].copy(), B["params"].copy()
    dA_l = RIGHT*(pB["lgt_x"]-pA["lgt_x"]) + UP*(pB["lgt_y"]-pA["lgt_y"])
    dA_b = RIGHT*(pB["btn_x"]-pA["btn_x"]) + UP*(pB["btn_y"]-pA["btn_y"])
    dB_l = -dA_l
    dB_b = -dA_b
    gA, gB = A["groups"], B["groups"]
    anims = [
        gA["lgt_sp"].animate.shift(dA_l), gA["lgt_bd_base"].animate.shift(dA_l), gA["lgt_bd_hl"].animate.shift(dA_l),
        gA["btn_sp"].animate.shift(dA_b), gA["btn_bd_base"].animate.shift(dA_b), gA["btn_bd_hl"].animate.shift(dA_b),
        gB["lgt_sp"].animate.shift(dB_l), gB["lgt_bd_base"].animate.shift(dB_l), gB["lgt_bd_hl"].animate.shift(dB_l),
        gB["btn_sp"].animate.shift(dB_b), gB["btn_bd_base"].animate.shift(dB_b), gB["btn_bd_hl"].animate.shift(dB_b),
    ]
    frA = A.get("extras", {}).get("outer_frames", [])
    frB = B.get("extras", {}).get("outer_frames", [])
    if frA:
        if len(frA) >= 1: anims.append(frA[0].animate.shift(dA_l))
        if len(frA) >= 2: anims.append(frA[1].animate.shift(dA_b))
    if frB:
        if len(frB) >= 1: anims.append(frB[0].animate.shift(dB_l))
        if len(frB) >= 2: anims.append(frB[1].animate.shift(dB_b))
    if anims: scene.play(*anims, run_time=rt)
    tmp = A.copy()
    A.clear()
    A.update(B)
    B.clear()
    B.update(tmp)
    try:
        scene.bring_to_front(A["groups"]["lgt_bd_hl"], A["groups"]["btn_bd_hl"], B["groups"]["lgt_bd_hl"], B["groups"]["btn_bd_hl"])
    except Exception:
        pass

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

def add_cell(scene, G_from, G_to, sx, sy, tx, ty, rt=1.0, color_from=None, color_to=None):
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

def show_mats(scene, grids, mats, rt=0.8, clear_first=True, keep_border=True, reset_state=True):
    gs = grids if isinstance(grids[0], list) else [grids]
    ms = mats if isinstance(mats[0][0], list) else [mats]
    if clear_first:
        del_grids(scene, gs, kp_bd=keep_border, reset_state=reset_state)
    anims = []
    for y in range(len(gs)):
        for x in range(len(gs[y])):
            p = gs[y][x]["params"]
            T = make_grid(scene, w=p["w"], h=p["h"], lgt_x=p["lgt_x"], btn_x=p["btn_x"], lgt_y=p["lgt_y"], btn_y=p["btn_y"], sz=p["sz"], rt=0.0, mat=ms[y][x], show=False)
            h, w = p["h"], p["w"]
            for j in range(h):
                for i in range(w):
                    _queue_opacity_anim(gs[y][x]["lgt_sp"][j][i], 1.0 if T["lgt"][j][i] else 0.0, anims)
                    _queue_opacity_anim(gs[y][x]["btn_sp"][j][i], 1.0 if T["btn"][j][i] else 0.0, anims)
            gs[y][x]["lgt"] = [row[:] for row in T["lgt"]]
            gs[y][x]["btn"] = [row[:] for row in T["btn"]]
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

def _mk_line_group_color(line, font, size, default_color, baseline, auto_k, ref_tex, color_map):
    segs = _parse_color_segments(line, color_map, default_color)
    if len(segs) == 1 and segs[0][1] == default_color:
        return _mk_line_group(line, font, size, default_color, baseline, auto_k, ref_tex)
    if "$" not in line:
        scale = size / 38
        text = "".join(t for t, c in segs)
        m = Text(text, font=font)
        m.set_color(default_color)
        for t, c in segs:
            if c != default_color and t:
                m.set_color_by_text(t, c)
        m.scale(scale)
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

def _mk_line_group(s, font, size, color, baseline=0.0, auto_k=0.5, ref_tex="N\\times N"):
    segs = _split_inline_math(s)
    scale = size / 38
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

def show_subtitle(scene, text, text2=None, run_in=0.3, run_out=0.3, font=DEFAULT_FONT, font_size=32, line_gap=0.2, buff=0.5, baseline=0.05, auto_k=0.5, ref_tex="N\\times N"):
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
    try:
        ref = Tex(ref_tex)
        ref.scale(1)
        h_ref = float(ref.get_height())
    except Exception:
        h_ref = 0.0
    if h_ref > 1e-6:
        target = h_ref * (SCALE_SUBTITLE * font_size / 32)
        for line in lines.submobjects:
            try:
                h_line = float(line.get_height())
            except Exception:
                h_line = 0.0
            if h_line > 1e-6:
                s = target / h_line
                if abs(s - 1.0) > 1e-3:
                    line.scale(s)
    lines.arrange(DOWN, buff=line_gap).to_edge(DOWN, buff=buff)
    scene.add(lines)
    scene.play(FadeIn(lines, run_time=run_in))
    scene._subtitle_mobj = lines
    scene._subtitle_ = lines
    return lines

def show_title(scene, line1=None, line2=None, run_in=0.3, run_out=0.3, font=DEFAULT_FONT, size1=48, size2=32, line_gap=0.15, buff=0.5, pause=0.8, rt=0.3):
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
    try:
        ref = Tex("N\\times N")
        ref.scale(1)
        h_ref = float(ref.get_height())
    except Exception:
        h_ref = 0.0
    if len(parts) >= 1 and parts[0] != "":
        t1 = _mk_line_group(parts[0], font, size1, WHITE)
        if h_ref > 1e-6:
            try:
                h_line = float(t1.get_height())
            except Exception:
                h_line = 0.0
            if h_line > 1e-6:
                target = h_ref * (SCALE_TITLE * size1 / 48)
                s = target / h_line
                if abs(s - 1.0) > 1e-3:
                    t1.scale(s)
        objs.append(t1)
    if len(parts) >= 2 and parts[1] != "":
        t2 = _mk_line_group(parts[1], font, size2, WHITE)
        if h_ref > 1e-6:
            try:
                h_line2 = float(t2.get_height())
            except Exception:
                h_line2 = 0.0
            if h_line2 > 1e-6:
                target2 = h_ref * (SCALE_TITLE * size2 / 32)
                s2 = target2 / h_line2
                if abs(s2 - 1.0) > 1e-3:
                    t2.scale(s2)
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

def show_latex(scene, text, x=0.0, y=0.0, run_in=0.3, run_out=0.3, font=DEFAULT_FONT, font_size=32, buff=0.5, line_gap=0.1, baseline=0.0, auto_k=0.5, ref_tex="N\\times N", show=True, color_map=COLOR_MAP, default_color=WHITE):
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

    lines = VGroup(*[_mk_line_group_color(p, font, font_size, default_color, baseline, auto_k, ref_tex, color_map) for p in parts])
    try:
        ref = Tex(ref_tex)
        ref.scale(1)
        h_ref = float(ref.get_height())
    except Exception:
        h_ref = 0.0
    if h_ref > 1e-6:
        target = h_ref * (SCALE_LATEX * font_size / 32)
        for line in lines.submobjects:
            try:
                h_line = float(line.get_height())
            except Exception:
                h_line = 0.0
            if h_line > 1e-6:
                s = target / h_line
                if abs(s - 1.0) > 1e-3:
                    line.scale(s)
    lines.arrange(DOWN, buff=line_gap, aligned_edge=LEFT)
    lines.move_to(ORIGIN)
    lines.shift(RIGHT * x + UP * y)
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

def trans_latex(scene, latex_from, latex_to, rt=1.0):
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

def add_grid_labels(scene, G, labels2d, which="lgt", font=DEFAULT_FONT, scale=0.5, rt=0.3):
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

def add_top_labels(scene, G, labels, which="lgt", font=DEFAULT_FONT, scale=0.55, dy=None, rt=0.3):
    grp = "lgt_bd_base" if which == "lgt" else "btn_bd_base"
    cells = G[grp]
    if not cells:
        return []
    W = len(cells[0])
    sz = G["params"]["sz"]
    shift = dy if dy is not None else sz
    n = min(W, len(labels))
    try:
        ref = Text("1", font=font)
        ref.scale(1)
        h_ref = float(ref.get_height())
    except Exception:
        h_ref = 0.0
    target = h_ref * scale if h_ref > 1e-6 else 0.0
    objs = []
    for i in range(n):
        s = str(labels[i])
        m = Text(s, font=font)
        if target > 0.0:
            try:
                h_line = float(m.get_height())
            except Exception:
                h_line = 0.0
            if h_line > 1e-6:
                s_factor = target / h_line
                if abs(s_factor - 1.0) > 1e-3:
                    m.scale(s_factor)
        else:
            m.scale(scale)
        pos = cells[0][i].get_center() + UP * shift
        m.move_to(pos)
        objs.append(m)
    if objs:
        scene.add(*objs)
        if rt and rt > 0:
            scene.play(*[FadeIn(o) for o in objs], run_time=rt)
    return objs

def add_left_labels(scene, G, labels, which="lgt", font=DEFAULT_FONT, scale=0.55, dx=None, rt=0.3):
    grp = "lgt_bd_base" if which == "lgt" else "btn_bd_base"
    cells = G[grp]
    if not cells:
        return []
    H = len(cells)
    sz = G["params"]["sz"]
    shift = dx if dx is not None else sz
    n = min(H, len(labels))
    try:
        ref = Text("1", font=font)
        ref.scale(1)
        h_ref = float(ref.get_height())
    except Exception:
        h_ref = 0.0
    target = h_ref * scale if h_ref > 1e-6 else 0.0
    objs = []
    for j in range(n):
        s = str(labels[j])
        m = Text(s, font=font)
        if target > 0.0:
            try:
                h_line = float(m.get_height())
            except Exception:
                h_line = 0.0
            if h_line > 1e-6:
                s_factor = target / h_line
                if abs(s_factor - 1.0) > 1e-3:
                    m.scale(s_factor)
        else:
            m.scale(scale)
        pos = cells[j][0].get_center() + LEFT * shift
        m.move_to(pos)
        objs.append(m)
    if objs:
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
    from manimlib.mobject.mobject import Mobject
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
    font_size=32,
    row_gap=0.4,
    col_gap=0.6,
    baseline=0.0,
    auto_k=0.5,
    ref_tex="N\\times N",
    show=True,
    color_map=COLOR_MAP,
    default_color=WHITE,
    header_color=WHITE,
):
    headers = ("输出", "输入", "说明", "算法", "公式")
    def make_cell(text, color, is_header=False):
        if isinstance(text, str) and text.strip() == "-":
            text = ""
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
        )
        if m is None:
            return VGroup()
        if isinstance(m, VGroup) and len(m.submobjects) == 1:
            m = m.submobjects[0]
        m.move_to(ORIGIN)
        return m
    header_row = [make_cell(h, default_color, True) for h in headers]
    data_rows = []
    for color, out_sym, in_sym, desc, algo, formula in LATEX_MAT:
        row = [
            make_cell(out_sym, color),
            make_cell(in_sym, color),
            make_cell(desc, color),
            make_cell(algo, color),
            make_cell(formula, color),
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
    {"type": "text", "content": "点灯游戏安卓 APK（含 O(n^3) 求解）：",                    "scale": 0.5, "indent": 0.0},
    {"type": "text", "content": "https://axpokl.com/cx/axdiandeng2.apk",                  "scale": 0.5, "indent": 0.5}
]

LATEX_MAT = [
    (L_COLOR,  "L",   "-",   "灯矩阵第一行",                 "公式递推",     "L(n,x)=L(n-1,x-1)⊕L(n-1,x)⊕L(n-1,x+1)⊕L(n-2,x)"),
    (B_COLOR,  "B",   "-",   "按钮矩阵第一行",               "公式递推",     "B(n,x)=B(n-1,x-1)⊕B(n-1,x)⊕B(n-1,x+1)⊕B(n-2,x)"),
    (Y_COLOR,  "Y",   "-",   "灯矩阵最后一行",               "公式递推",     "Y(n,y)=~(Y(n-1,y-1)⊕Y(n-1,y)⊕Y(n-1,y+1)⊕Y(n-2,y))"),
    (H_COLOR,  "H",   "-",   "H^n第一行（Krylov扩散基矩阵）", "公式递推", "H(y,x)​=(​∣x-y∣=1)"),
    (K_COLOR,  "K",   "-",   "H^n第一行（Krylov扩散基矩阵）", "公式递推", "K(n,x)=K(n-1,x-1)⊕K(n-1,x+1)"),
    (F_COLOR,  "F",   "-",   "K的逆矩阵（Krylov解耦矩阵）",       "公式递推", "F(n,x)=F(n-1,x-1)⊕F(n-2,x)"),
    (C_COLOR,  "C",   "-",   "B关于H的系数矩阵",             "公式递推",     "C(n,x)=C(n-1,x-1)⊕C(n-1,x)⊕C(n-2,x)"),
    (P_COLOR,  "P",   "B,F", "多项式p(H)的系数",            "矩阵向量乘法", "P=B*F"),
    (Q_COLOR,  "Q",   "F,P", "多项式p(x)的在f(x)下的逆",    "扩展欧几里得", "Q=P^-1 mod F"),
    (G_COLOR,  "G",   "F,P", "多项式p(x)和q(x)最大共因子", "扩展欧几里得", "G=gcd(F,P)=gcd(F,C)"),
    (Z_COLOR,  "Z",   "Q,Y", "部分逆按钮解",               "矩阵向量乘法", "Z=Q*Y"),
    (D_COLOR,  "D",   "G",   "多项式g(x)的矩阵",           "矩阵向量乘法", "D=G*K"),
    (ID_COLOR, "ID",  "D",   "H每一行的主元索引",          "求最大值",     "ID=max(D(n))"),
    (X_COLOR,  "X",   "D,Z", "最终首行按钮解",             "前向异或消元", "Z=G*X"),
    (T_COLOR,  "T",   "X",   "最终按钮解矩阵",             "公式递推",     "T(n,x)=T(n-1,x-1)⊕T(n-1,x)⊕T(n-1,x+1)⊕T(n-2,x)"),
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
 LATEX_ID,
 LATEX_X,
 LATEX_T
) = [
    f"<c{row[1]}>{row[5]}"
    for row in LATEX_MAT
]

class LightsOut(Scene):
    def construct(self):
        self.camera.background_color = BLACK

#        """
        show_title(self, "点灯游戏的$O(n^2)$解法")
#演示n=5,7,11
        show_title(self, "首行叠加法（续上集）")

        show_subtitle(self, "在上集视频的首行叠加法中，有观众对按钮和灯的递推仍有疑问。", "这次我们来讲清楚，这个递推公式是怎么来的。")
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
                my = -k*sz+0.5
                G5_[k][y] = make_grid(self, w=cols, h=1, lgt_x=mx, btn_x=mx, lgt_y=my, btn_y=my, sz=sz, mat=[MAT5K[k][y][:]], mat_l=[MAT5K[k+1][y][:]], show=True, rt=0.05)
                mx = (y*2-cols)*(1+sz)+1+sz*(cols+3)/2
                G5Y_[k][y] = make_grid(self, w=1, h=1, lgt_x=mx, btn_x=mx, lgt_y=my, btn_y=my, sz=sz, mat=[[MAT5KY[k][y]]], mat_l=[[MAT5KY[k+1][y]]],show=True, rt=0.05)
                if k == 0: top_objs[k][y] = add_top_labels(self, G5_[k][y], ["x1","x2","x3","x4","x5"], which="lgt", scale=0.4, rt=0.01)
                if k == 0: topy_objs[k][y] = add_top_labels(self, G5Y_[k][y], [f"y{y+1}"], which="lgt", scale=0.4, rt=0.01)
                left_objs[k][y] = add_left_labels(self, G5_[k][y], [f"n{k+1}"], which="lgt", scale=0.4, rt=0.01)

        show_subtitle(self, "n代表从上到下第n行灯或按钮。", "因为我们是一行行进行推导的，n也代表第n次推导。")
        self.wait(4)
        show_subtitle(self, "x代表从左到右第x列按钮。将灯表示为第一行的某几个列的按钮的叠加。", "这里的x不局限于第一行。")
        self.wait(4)
        show_subtitle(self, "y代表从左到右第y列灯。", "这里的公式对任意第y个灯都满足，所以省去了y。")
        self.wait(4)

        show_subtitle(self, "在上集视频中，因为最终目标是将灯用按钮表示，", "因此省去了按钮表示按钮，粉色原点直接为按钮表示灯。")
        self.wait(4)
        show_subtitle(self, "在这里，粉色原点是用按钮表示按钮，淡蓝色方块是用按钮表示灯。")
        self.wait(4)

        del_latex(self, [LAT1, LAT2]);
        del_top_labels(self, top_objs)
        del_top_labels(self, topy_objs)
        del_left_labels(self, left_objs)
        del_grids(self, G5_);
        del_grids(self, G5Y_);

        show_subtitle(self, "让我们举一个具体的例子。", "在5x5的格子中，我们将灯和按钮编号为1-25。")
        self.wait(2)
        show_subtitle(self, "在叠加法中，我们将灯表示为所有按钮的叠加。", "例如：L1=B1⊕B2⊕B6，L6=B1⊕B6⊕B7⊕B11。")
        cols, rows = 5, 5
        G5 = make_grid(self, w=cols, h=rows, lgt_x=-4, btn_x=-4, sz=0.5)
        objs = add_grid_labels(self, G5, [[f"B{c*rows + r + 1}" for c in range(cols)] for r in range(rows)], which="btn", scale=0.5)
        sz = 0.18
        G5_ = [[None] * cols for _ in range(rows)]
        mat_l = make_mat_l(rows)
        btn_objs = [[None] * cols for _ in range(rows)]
        lgt_objs = [[None] * cols for _ in range(rows)]
        for y in range(rows):
            for x in range(cols):
                idx = y * cols + x
                my = ((rows * cols) - 1) * sz / 2 - idx * sz
                G5_[y][x] = make_grid(self, w=cols * rows, h=1, w_l=1, h_l=1, lgt_x=3, btn_x=0, lgt_y=my, btn_y=my, sz=sz, rt=0.01, mat=[mat_l[idx][:]], mat_l=[[1]], show=False)
                rt = 0.1
                if y==0 and x<=1 : rt = 1.5
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

        show_subtitle(self, "而在首行叠加法中，我们需要把灯表示为第一行按钮的叠加。")
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
                my = -k*sz+0.5
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
        add_cell(self, G5_[0][0], G5_[1][0], 0, 0, 0, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2, rt=0.3)
        add_cell(self, G5_[1][0], G5_[1][0], 0, 0, 0, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2, rt=0.3)
        add_cell(self, G5_[1][0], G5_[1][0], 1, 0, 1, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2, rt=0.3)
        add_cell(self, G5_[1][1], G5_[1][0], 0, 0, 0, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2, rt=0.3)
        add_cell(self, G5_[1][1], G5_[1][0], 1, 0, 1, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2, rt=0.3)
        add_cell(self, G5_[1][1], G5_[1][0], 2, 0, 2, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2, rt=0.3)

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
        add_cell(self, G5_[0][1], G5_[1][1], 1, 0, 1, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2, rt=0.3)
        add_cell(self, G5_[1][0], G5_[1][1], 0, 0, 0, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2, rt=0.3)
        add_cell(self, G5_[1][0], G5_[1][1], 1, 0, 1, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2, rt=0.3)
        add_cell(self, G5_[1][1], G5_[1][1], 0, 0, 0, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2, rt=0.3)
        add_cell(self, G5_[1][1], G5_[1][1], 1, 0, 1, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2, rt=0.3)
        add_cell(self, G5_[1][1], G5_[1][1], 2, 0, 2, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2, rt=0.3)
        add_cell(self, G5_[1][2], G5_[1][1], 1, 0, 1, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2, rt=0.3)
        add_cell(self, G5_[1][2], G5_[1][1], 2, 0, 2, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2, rt=0.3)
        add_cell(self, G5_[1][2], G5_[1][1], 3, 0, 3, 0, color_from=HL_COLOR_1, color_to=HL_COLOR_2, rt=0.3)

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
                my = -k*sz+0.5
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
        show_subtitle(self, "这就是之前视频中，优化生成矩阵章节中的性质，", "后面我会给予证明。")
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
        show_subtitle(self, "在生成优化矩阵章节中，我将矩阵的行重排。", "其实是调换了n和y的位置，使原来从左到右的第y个矩阵变为了第n个矩阵。")
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
                    swap_grid(self, G5_[k][y], G5_[y][k], rt=0.3)
                    swap_grid(self, G5Y_[k][y], G5Y_[y][k], rt=0.3)
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
        LAT1_3 = show_latex(self, "<cH2>B(n,x-1,y)⊕<br><cH2>B(n,x+1,y)⊕<br><cH2>B(n,x,y-1)⊕<br><cH2>B(n,x,y+1)", 0, 2.0, show=False, font_size=24)
        trans_latex(self, LAT1_2, LAT1_3)
        self.wait(2)

        LAT1_4 = show_latex(self,
            "<cH2>(B(n-1,x-1-1,y)⊕B(n-1,x-1+1,y)⊕B(n-1,x-1,y-1)⊕B(n-1,x-1,y+1))⊕<br>"
            "<cH2>(B(n-1,x-1,y)⊕B(n-1,x+1,y)⊕B(n-1,x,y-1)⊕B(n-1,x,y+1))⊕<br>"
            "<cH2>(B(n-1,x+1-1,y)⊕B(n-1,x+1+1,y)⊕B(n-1,x+1,y-1)⊕B(n-1,x+1,y+1))⊕<br>"
            "<cH2>(B(n-2,x-1,y)⊕B(n-2,x+1,y)⊕B(n-2,x,y-1)⊕B(n-2,x,y+1))",
            0, 2.0, show=False, font_size=24)
        trans_latex(self, LAT1_3, LAT1_4)
        self.wait(2)

        show_subtitle(self, "代入后的式子包含16个项目。现在重新排列项目顺序，将y和n调换，类似刚才生成矩阵章节中的调换操作。")
        LAT1_5 = show_latex(self,
            "<cH2>(B(n-1,x-1-1,y)⊕B(n-1,x-1,y)⊕B(n-1,x+1-1,y)⊕B(n-2,x-1,y))⊕<br>"
            "<cH2>(B(n-1,x-1+1,y)⊕B(n-1,x+1,y)⊕B(n-1,x+1+1,y)⊕B(n-2,x+1,y))⊕<br>"
            "<cH2>(B(n-1,x-1,y-1)⊕B(n-1,x,y-1)⊕B(n-1,x+1,y-1)⊕B(n-2,x,y-1))⊕<br>"
            "<cH2>(B(n-1,x-1,y+1)⊕B(n-1,x,y+1)⊕B(n-1,x+1,y+1)⊕B(n-2,x,y+1))",
            0, 2.0, show=False, font_size=24)
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
        LAT1_6 = show_latex(self, "<cH2>0⊕<br><cH2>0⊕<br><cH2>0⊕<br><cH2>0", 0, 2.0, show=False, font_size=24)
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

        show_subtitle(self, "因为B(n)有了这个性质，我们只需要知道B(n)的第一行，", "就能通过公式推导出下面的行。")
        bd = hl_bd(self, [G5_[0][4]])
        self.wait(2)
        del_bd(self, bd)
        show_subtitle(self, "通过这种方法，我们无需对每个y都生成矩阵B，", "只需计算这些B矩阵的第一行，得到B(n)的第一行，即可求得完整的矩阵B(n)。")
        bd = hl_bd(self, [row[4] for row in G5_])
        self.wait(2)
        del_latex(self, [LAT1_8, LAT2_1])
        del_bd(self, bd)
        del_top_labels(self, top_objs)
        del_top_labels(self, topy_objs)
        del_left_labels(self, left_objs)
        del_grids(self, [G5_, G5Y_]) 


#        table = show_algo_table(self, x=0.0, y=0.0, font_size=18, row_gap=0.075, col_gap=0.5)
#        self.wait(2)
#        hide_algo_table(self, table)

#        """

#——————————————————————
        show_title(self, "首行求逆法")

        show_subtitle(self, "对于O(n^2)的算法，我们也是使用类似的方法，", "尽可能的不去对完整矩阵进行操作，而是通过第一行来求逆或求解。")
        grid_B = make_grid(self, 7, 7, mat_l=MAT7K[7], btn_c=B_COLOR, lgt_c=B_COLOR, sz=0.4)
        grid_Y = make_grid(self, 1, 7, mat_l=[[v] for v in MAT7KY[7]], btn_c=Y_COLOR, lgt_c=Y_COLOR, btn_x=2, lgt_x=2, sz=0.4)
        self.wait(2)
        show_subtitle(self, "这里，让我以我们以n=7为例。", "这里的B就是前面提到的按钮矩阵B，而Y就是翻转矩阵Y的最后一行。")
        topy_obj_B = add_top_labels(self, grid_B, ["", "", "", "B", "", "", ""], which="btn", scale=0.7)
        topy_obj_Y = add_top_labels(self, grid_Y, ["Y"], which="btn", scale=0.7)
        self.wait(2)
        show_subtitle(self, "我们的目标是，对于BX=Y，在已知B的第一行和Y的情况下求X。")
        hl_cells(self, [grid_B], which="lgt", indices= [(i, 0) for i in range(grid_B["params"]["w_l"] )])
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
        topy_obj_X = add_top_labels(self, grid_X, ["X"], which="btn", scale=0.7)
        self.wait(2)
        del_bd(self, bd_B_row)
        del_top_labels(self, [topy_obj_B, topy_obj_Y, topy_obj_X])
        del_grids(self, [grid_B, grid_Y, grid_X])

        show_subtitle(self, "如果将n在不同情况下B的第一行写在一起，这样的B矩阵长这样。")
        LAT_B = show_latex(self, LATEX_B, 0, 2.0)
        grid_B = make_grid(self, 8, 8, mat_l=MAT_B, mat_g={"lgt": MAT_MK1, "btn": MAT8_0}, btn_c=B_COLOR, lgt_c=B_COLOR, sz=0.4)
        left_obj = add_left_labels(self, grid_B, list(range(8)), which="btn", dx=0.4)
        hl_cells(self, [grid_B], which="btn", indices=[(1,1),(0,2),(1,2),(2,2)])
        hl_cells(self, [grid_B], which="btn", indices=[(1,3)], color=HL_COLOR_2)
        self.wait(2)
        show_subtitle(self, "注意，这里的B矩阵不是刚才说的当n确定时的完整的B矩阵。")
        self.wait(2)
        del_cells(self, [grid_B], which="btn", indices=[(1,1),(0,2),(1,2),(2,2)])
        del_cells(self, [grid_B], which="btn", indices=[(1,3)])
        show_subtitle(self, "另外，这里从n=0开始一共递推n次，第n列的1不包含在B矩阵的第一行内。", "例如n=5时，第一行为01101，最后一个1省去。")
        grid_B_ = make_grid(self, 8, 8, mat_l=MAT_B, mat_g={"lgt": MAT_MK2, "btn": MAT8_0}, btn_c=B_COLOR, lgt_c=B_COLOR, sz=0.4, show=False)
        trans_grid(self,grid_B,grid_B_, keep_from=False);
        self.wait(2)
        del_latex(self, [LAT_B])
        del_left_labels(self, left_obj)
        del_grids(self, [grid_B_])

        show_subtitle(self, "把Y的第一行写在一起是这样的。")
        LAT_Y = show_latex(self, LATEX_Y, 0, 2.0)
        grid_Y = make_grid(self, 8, 8, mat_l=MAT_Y, mat_g={"lgt": MAT_MK2, "btn": MAT8_0}, btn_c=Y_COLOR, lgt_c=Y_COLOR, sz=0.4)
        left_obj = add_left_labels(self, grid_Y, list(range(8)), which="btn", dx=0.4)
        self.wait(2)
        del_latex(self, [LAT_Y])
        del_left_labels(self, left_obj)
        del_grids(self, [grid_Y])

        show_subtitle(self, "为了实现这个目标，我们需要首先将B进行分解。", "这里，让我首先介绍一个非常重要的矩阵H。")
        LAT_H = show_latex(self, LATEX_H, 0, 2.0)
        grid_H = make_grid(self, 7, 7, mat_l=MAT_H, btn_c=H_COLOR, lgt_c=H_COLOR, sz=0.4)
        left_obj = add_left_labels(self, grid_H, list(range(7)), which="btn", dx=0.4)
        show_subtitle(self, "对于H的每一个元素，如果x和y的差为一则为一，否则为零。")
        self.wait(2)
        show_subtitle(self, "如果将向量v乘以该矩阵，等同于将向量v的每个元素向左右扩散后叠加。")
        LAT_V = show_latex(self, "<cV>v(x)*<cH>H<cV>=v(x-1)⊕v(x+1)", 0, 2.5)
        grid_V1 = make_grid(self, 7, 1, mat_l=[[0,1,0,0,0,1,0]], btn_y=-2, lgt_y=-2, btn_c=V_COLOR, lgt_c=V_COLOR, sz=0.4)
        grid_V2 = make_grid(self, 1, 7, mat_l=[[0],[1],[0],[0],[0],[1],[0]], btn_x=-2, lgt_x=-2, btn_c=V_COLOR, lgt_c=V_COLOR, sz=0.4, show=False)
        trans_grid(self, grid_V1, grid_V2)
        grid_V3 = make_grid(self, 7, 1, mat_l=[[0,0,0,0,0,0,0]], btn_y=-2, lgt_y=-2, btn_c=V_COLOR, lgt_c=V_COLOR, sz=0.4)

        grid_VH1 = make_grid(self, 7, 1, mat_l=[MAT_H[1]], btn_y=0.8, lgt_y=0.8, btn_c=V_COLOR, lgt_c=V_COLOR, sz=0.4)
        grid_VH2 = make_grid(self, 7, 1, mat_l=[MAT_H[5]], btn_y=-0.8, lgt_y=-0.8, btn_c=V_COLOR, lgt_c=V_COLOR, sz=0.4)
        bd1 = hl_bd(self, grid_VH1)
        bd2 = hl_bd(self, grid_VH2)
        add_grid(self, grid_VH1, grid_V3)
        del_bd(self,bd1)
        add_grid(self, grid_VH2, grid_V3)
        del_bd(self,bd2)
        show_subtitle(self, "这是因为矩阵的对应行就是向量每个元素左右扩散的结果。")
        self.wait(2)
        del_latex(self, [LAT_H, LAT_V])
        del_left_labels(self, left_obj)
        del_grids(self, [grid_H, grid_V3, grid_V2, grid_VH1, grid_VH2])

        show_subtitle(self, "如果将多个H相乘，也就是H^n，", "则其首行H^n(0)从单位矩阵n=0开始，看起来像是这样的。")
        grid_K = make_grid(self, 8, 8, mat_l=MAT_K, mat_g={"lgt": MAT_MK1, "btn": MAT8_0}, btn_c=K_COLOR, lgt_c=K_COLOR, sz=0.4)
        left_obj = add_left_labels(self, grid_K, list(range(8)), which="btn", dx=0.4)
        self.wait(2)
        show_subtitle(self, "我们把这个下三角矩阵记为K，即Krylov矩阵或扩散基矩阵。", "也就是说，对于K的第n行，有K(n)=H^n(0)。")
        LAT_K1 = show_latex(self, "<cK>K(n)=k(n-1)*<cH>H=H^n(0)", 0, 2.5)
        self.wait(2)
        show_subtitle(self, "这里下一行是上一行乘以H，也就是上一行左右扩散的叠加。", "因此对于K的每个元素，有以上公式。")
        LAT_K2 = show_latex(self, LATEX_K, 0, 2.0)
        hl_cells(self, [grid_K], which="btn", indices=[(0,2),(2,2)])
        hl_cells(self, [grid_K], which="btn", indices=[(1,3)], color=HL_COLOR_2)
        self.wait(2)
        del_cells(self, [grid_K], which="btn", indices=[(0,2),(2,2)])
        del_cells(self, [grid_K], which="btn", indices=[(1,3)])
        del_latex(self, [LAT_K1, LAT_K2])
        del_left_labels(self, left_obj)
        del_grids(self, [grid_K])

        show_subtitle(self, "不难发现，首行叠加法中的各个B矩阵，可以使用H表示为以上公式。")

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
        del_grids(self, [grid_C])

#——————————————————————
        """

        show_subtitle(self, "现在，定义多项式p(x)。", "我们的目标是把B拆分成H^n，使用多项式p(H)表示B。")
p(x)=p0x^0+p1x^1+p2x^2...=SUM
B=p(H)=p0*​H^0⊕p1​*H^1⊕p2​*H2⊕⋯=SUM

#【演示】展示朗读公式
        show_subtitle(self, "这样，原始求X的问题就变为了p(H)X=Y。")
BX=Y⟺p(H)X=Y

#【演示】展示朗读公式

        show_subtitle(self, "现在，我们需要把多项式p(H)的系数计算出来。", "这个系数构成的向量我们记为p。")
p=(p0,p1,p2...)。
        show_subtitle(self, "为了简化运算，我们只关心矩阵第一行B(0)，记为b。", "根据刚才的定义，我们可以得到b=p*k。")
b=B(0)=p(H(0))=p0​*H^0(0)⊕p1*​H^1(0)⊕p2​*H^2(0)⊕⋯=p0​*K(0)⊕p1*K(1)⊕p2*K(2)⊕⋯=p*K
#【演示】展示朗读公式(b=B(0)=p(H(0))=p*K)，把0加上去或直接展示新的。
#——————————————————————

        show_subtitle(self, "为了求得p，我们可以将两边同时乘以K的逆矩阵K^-1。", "为了方便我们记为F，又称反Krylov矩阵或解耦矩阵。")

        grid_F = make_grid(self, 8, 8, mat_l=MAT_F, mat_g={"lgt": MAT_MK1, "btn": MAT8_0}, btn_c=F_COLOR, lgt_c=F_COLOR, sz=0.4)
        self.wait(2)
        del_grids(self, [grid_F])



#【演示】一行行显示F矩阵，圈出递推公式

        show_subtitle(self, "这个矩阵F也是下三角矩阵，并且和矩阵K看上去差不多，不过并不相同。", "事实上，这个矩阵F也满足类似的性质。")
F(y,x)=F(y-1,x-1)⊕F(y-2,x)
        show_subtitle(self, "有兴趣的小伙伴可以试着证明一下，", "使用这两个性质构造的矩阵K和F，然后证明互为逆矩阵。")

        show_subtitle(self, "于是，我们便有：b*F=p*K*F=p。这样我们便求出了p。")
#【演示】演示，计算P矩阵（b竖着，叠加）

        show_subtitle(self, "将多项式p(x)写成矩阵的形式，记为P。")

        grid_P = make_grid(self, 8, 8, mat_l=MAT_P, mat_g={"lgt": MAT_MK2, "btn": MAT8_0}, btn_c=P_COLOR, lgt_c=P_COLOR, sz=0.4)
        self.wait(2)
        del_grids(self, [grid_P])



#【演示】一行行显示P矩阵

#——————————————————————

        show_subtitle(self, "这里说明一下，矩阵F的每行对应多项式f(n,x)，", "也就是上一集视频《解的数量》章节中提到的OEIS中的Fibonacci多项式。")
f(n,x)=x·f(n-1,x)⊕f(n-2,x)
#【演示】LATEX1
        show_subtitle(self, "此外，刚才递推得到的C矩阵对应多项式c(n,x)，", "其实也就是这里提到的f(n,x+1)。")
c(n,x)=f(n,x+1)
#【演示】朗读公式
        show_subtitle(self, "这是因为B(n)矩阵也可以写为以上形式。", "这里的H⊕I等价于x+1。")
B(n)=B(n-1)*(H⊕I)⊕B(n-2)

#【演示】朗读公式


        show_subtitle(self, "同时，上一集视频提到的公式r'(n)，", "可以表示为多项式f和c的最大公因子的最高次幂。")
r'(n)=deg(gcd(f(n,x),c(n,x)))
        show_subtitle(self, "这里，gcd表示最大公因子，我们将其记为多项式g(x)。")
g(n,x)=gcd(f(n,x),c(n,x))
        show_subtitle(self, "deg表示最高次幂，其等价于矩阵B丢失的秩，也就是n-r。", "这个g(x)和n-r在后续算法中也会提到。")

        show_subtitle(self, "将g(x)写成矩阵的形式，记为G。")

        grid_G = make_grid(self, 8, 8, mat_l=MAT_G, mat_g={"lgt": MAT_MK1, "btn": MAT8_0}, btn_c=G_COLOR, lgt_c=G_COLOR, sz=0.4)
        self.wait(2)
        del_grids(self, [grid_G])


#【演示】一行行显示G矩阵

        show_subtitle(self, "可以发现，如果B是可逆的，则g(x)=1，n=r，r’=0。", "否则，r'的值决定了解的数量，即2^r'。")

#【演示】圈出每一行最高系数格

#——————————————————————



事实上，后续的计算我们都不需要用到完整的B，而只需要这个第一行b。
这是因为我们已经将问题从BX=Y转为了p(H)=Y。由此，在前面说到的生成矩阵也只需要计算第一行b。
由于在不同n的情况下b的计算方式是一样的，我们可以把n-1情况下算出的b，直接用于对n情况下b的计算，也就是：
b(n,x)=b(n-1,x-1)⊕b(n-1,x)⊕b(n-1,x+1)⊕b(n-2,x)
这样，如果我们是从n=0开始计算的，我们只需要O(n)的时间复杂度便可求出b。
同样，计算K和F也是如此。因为每行之间有递推公式，如果从n=0开始计算，也可以在O(n)时间内求出。
如果需要直接计算特定n，可以用别的方式优化到O(n*log(n))。因为这里的算法不涉及这个优化，因此不再赘述。
为了求出p=b*F，我们需要将向量和矩阵相乘，一般情况下时间复杂度是O(n^2)。
因为矩阵F是有递推规律的，理论上使用FFT等算法可以优化到O(n*log(n))。

现在我们已求得了p，并将原始问题转换为了p(H)X=Y。那这又有什么用呢？

——————————————————————

试想一下，如果有一个多项式q(x)，满足：
q(x)p(x)=1 mod f(x)
这里的f(x)就是前面提到的多项式f(n,x)。那么，将原始两边同时乘以q(H)，便有：
X=q(H)p(H)X=q(H)*Y
这样，我们就能立刻求出X。
让我把这样的多项式q(x)我们称之为p(x)的逆多项式。那么，如何求出逆多项式q(x)呢？

这里，我们同样将q(x)的系数写为向量q，然后扩展欧几里得算法来求取q：

我们使用辗转相减法，将p(x)右移，使最高系数对齐，然后叠加到f(x)上。
如果叠加后的f(x)的最高次数小于p(x)，则将f(x)和p(x)互换，然后再次进行操作。
同时，我们定义一个单位多项式e(x)和零多项式o(x)，在对f(x)和p(x)操作的时候对e(x)和o(x)做同样操作。
这样，最终f(x)会被叠加到零，而剩下的p(x)则为两个多项式的最大公因子，记为g(x)。
同时，最后剩下的o(x)则是p(x)的逆，也就是q(x)。

将q(x)写成矩阵Q的前6行，注意这里的矩阵不是后面提到的完整的逆矩阵Q，而是每个逆矩阵Q的第一行拼凑起来。

        grid_Q = make_grid(self, 8, 8, mat_l=MAT_Q, mat_g={"lgt": MAT_MK2, "btn": MAT8_0}, btn_c=Q_COLOR, lgt_c=Q_COLOR, sz=0.4)
        self.wait(2)
        del_grids(self, [grid_Q])
——————————————————————

这里，由于我们已求得q(x)。我们也可以利用这个式子来求X：
X=q(H)*Y=(q0*H^0⊕q1*H^1⊕q2*H^2⊕...)*Y=q0*H^0*Y⊕q1*H^1*Y⊕q2*H^2*Y⊕...
这里，我们可以从Y开始，不断将其和H相乘，使用左右扩散的办法计算下一个H^n*Y，然后和qn叠加，得到X。
通过这个办法，我们也可以在O(n^2)中求得X。

事实上，q(x)的系数也就是B的逆矩阵Q的第一行，并且可以证明B的逆矩阵Q也满足十字偶校验约束。
因此，可以通过递推公式，用逆矩阵第一行q(x)直接求出整个逆矩阵Q，然后再和Y相乘获得X。
不过，这整个求解的过程有一个问题，就是我们假设满足q(x)p(x)=1 mod f(x)的多项式q(x)存在。
如果矩阵B不可逆呢？例如当n=5的时候，这种情况下求得的g(x)不为1，因此q(x)不是p(x)的逆。或者说，满足该式子的q(x)不存在：
q(x)p(x)=1 mod f(x)
这种情况下，求得的q(x)和伪逆矩阵Q'不同，并且都不满足q(x)p(x)=1 mod f(x)。并且伪逆矩阵Q'也不满足十字偶校验约束，因此无法通过公式递推再相乘求解X。

例如，n=5时的伪逆矩阵Q'看起来像是这样：

B	Q'	E'
01101	11000	10001
11100	11100	01010
11011	01100	00111
00111	01110	00000
10110	10101	00000

        grid_B5 = make_grid(self, 5, 5, mat_l=MAT_B5, btn_c=B_COLOR, lgt_c=B_COLOR, sz=0.4)
        self.wait(2)
        del_grids(self, [grid_B5])

        grid_Q5 = make_grid(self, 5, 5, mat_l=MAT_Q5, btn_c=Q_COLOR, lgt_c=Q_COLOR, sz=0.4)
        self.wait(2)
        del_grids(self, [grid_Q5])

        grid_E5 = make_grid(self, 5, 5, mat_l=MAT_E5, btn_c=L_COLOR, lgt_c=L_COLOR, sz=0.4)
        self.wait(2)
        del_grids(self, [grid_E5])

可以证明，这里的伪逆矩阵Q'，以及高斯消元后的伪单位矩阵E'具有这样的形式（转置和矩阵大小下标省略）：
[Br	Ur]	[Qr	0]	[I	Wr]
[Ur	Vr]	[Wr	I]	[0	0]
这里，矩阵B的秩为r，例如n=5时r=3，并以rxr为界将矩阵分为四块，其中：
Qr=Br^-1：B矩阵左上角rxr的子矩阵Br满秩，并且B的伪逆矩阵Q'的左上角rxr子矩阵Qr伪Br的逆。
Wr=Ur*Qr：伪逆矩阵Q'左下角和伪单位矩阵E'右上角内容相同（静默操作），并且其值等于Ur乘以Qr。
矩阵Q'和E'一定具有这样的形式，并且可以用分块矩阵乘法很容易的证明这两个性质。有兴趣的观众可以自行证明。

可以发现，这里的q(x)并不是Q'的第一行，并且求得的X也不是原方程的解。

这里可以验证：
公式递推法：f(x)=x^2+x^5
欧几里得法：q(x)p(x)=x*(x+x^4)=x^2+x^5 ≠ 1 mod x^2+x^5
伪逆第一行：q​(x)p(x)=(1+x)*(x+x^4)=x+x^2+x^4+x^5 ≠ 1 mod x^2+x^5

不难注意到，只有当矩阵B为可逆矩阵时，g(x)=1，并且g(x)的最高次幂为n-r=r'。那么对于不可逆的矩阵B，我们又有什么解决办法呢？
【演示】这里可以圈出g(x)以及最高次幂=2

——————————————————————





        """