from manimlib import *
import numpy as np

LIGHT_BLUE = "#55aaff"
PINK = "#ff55aa"

BD_W = 2
BD_W_SEL = 8
HL_COLOR = RED
DEFAULT_FONT = "SimHei"

def make_grid(scene, w, h, lgt_x=0.0, btn_x=0.0, lgt_y=0.0, btn_y=0.0, sz=1.0, rt=0.3, mat=None, mat_l=None, w_l=None, h_l=None, show=True, mat_g=None,):
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
            lbd_hl = lbd.copy().set_stroke(HL_COLOR, BD_W_SEL, 0).set_fill(opacity=0)
            if not grid_vis_lgt[j][i]: lbd_hl.set_stroke(opacity=0)
            lgt_bd_hl[j][i]=lbd_hl
            lgt_bd_hl_grp.add(lbd_hl)
            lsp = Square(side_length=lgt_sz).set_stroke(width=0, opacity=0).set_fill(LIGHT_BLUE,1)
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
            bbd_hl = bbd.copy().set_stroke(HL_COLOR, BD_W_SEL, 0).set_fill(opacity=0)
            if not grid_vis_btn[j][i]: bbd_hl.set_stroke(opacity=0)
            btn_bd_hl[j][i]=bbd_hl
            btn_bd_hl_grp.add(bbd_hl)
            bsp = Circle(radius=btn_sz).set_stroke(width=0, opacity=0).set_fill(PINK,1)
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
                sp.set_fill(LIGHT_BLUE, 1)
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
                sp.set_fill(PINK, 1)
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

def hl_bd(scene, G, color=RED, width=BD_W_SEL, buff=0.06, rt=0.3):
    if "extras" not in G:
        G["extras"] = {}
    frames = []
    lgt_frame = (
        SurroundingRectangle(G["groups"]["lgt_bd_base"], buff=buff)
        .set_fill(opacity=0)
        .set_stroke(color, width, 1)
    )
    scene.add(lgt_frame)
    frames.append(lgt_frame)
    btn_frame = (
        SurroundingRectangle(G["groups"]["btn_bd_base"], buff=buff)
        .set_fill(opacity=0)
        .set_stroke(color, width, 1)
    )
    scene.add(btn_frame)
    frames.append(btn_frame)
    scene.play(*[FadeIn(f) for f in frames], run_time=rt)
    G["extras"]["outer_frames"] = frames

def del_bd(scene, G, rt=0.3):
    frames = G.get("extras", {}).get("outer_frames", [])
    if not frames:
        return
    scene.play(*[FadeOut(f) for f in frames], run_time=rt)
    try:
        scene.remove(*frames)
    except Exception:
        pass
    G["extras"]["outer_frames"] = []

def hl_cells(scene, grids, which="lgt", indices=[(0,0)], color=RED, width=BD_W_SEL, rt=0.3):
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

def show_all_lights(scene, G, rt=0.3, clear_highlight=True):
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

def _mk_line_group(s, font, size, color, baseline=0.0, auto_k=0.5, ref_tex="N\\times N"):
    segs = _split_inline_math(s)
    scale = size / 38
    if not segs:
        return Text("", color=color, font=font).scale(scale)
    objs, tags = [], []
    for k, v in segs:
        if k == "tex":
            m = Tex(v).set_color(color).scale(scale)
            objs.append(m)
            tags.append("tex")
        else:
            m = Text(v, color=color, font=font).scale(scale)
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
    if len(parts) >= 1 and parts[0] != "":
        t1 = _mk_line_group(parts[0], font, size1, WHITE)
        objs.append(t1)
    if len(parts) >= 2 and parts[1] != "":
        t2 = _mk_line_group(parts[1], font, size2, WHITE)
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

def show_latex(scene, text, x=0.0, y=0.0, run_in=0.3, run_out=0.3, font=DEFAULT_FONT, font_size=32, buff=0.5, baseline=0.05, auto_k=0.5, ref_tex="N\\times N"):
    parts = []
    if isinstance(text, (list, tuple)):
        parts = [str(p) for p in text if p is not None]
    else:
        if text is None:
            return None
        parts = str(text).split("\n")
    parts = [p for p in parts if p is not None]
    if len(parts) == 0 or all(p == "" for p in parts):
        return None
    lines = VGroup(*[_mk_line_group(p, font, font_size, WHITE, baseline, auto_k, ref_tex) for p in parts])
    lines.arrange(DOWN, buff=buff, aligned_edge=LEFT)
    lines.move_to(ORIGIN)
    lines.shift(RIGHT * x + UP * y)
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

def make_grid_label(scene, G, tex, dy=0.25, scale=0.6):
    lg=G["groups"]
    cont=VGroup(lg["lgt_bd_base"],lg["lgt_bd_hl"],lg["lgt_sp"],lg["btn_bd_base"],lg["btn_bd_hl"],lg["btn_sp"])
    m=Tex(tex)
    m.scale(scale)
    m.next_to(cont,UP,buff=dy)
    scene.add(m)
    return m

def del_grid_label(sc, labels, rt=0.3):
    if not labels: return
    if rt>0:
        sc.play(*[FadeOut(m) for m in labels], run_time=rt)
    for m in labels: sc.remove(m)

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
    M = [[[0]*n for _ in range(n)] for _ in range(n)]
    def v(A,y,x):
        return A[y][x] if 0 <= x < n else 0
    for y in range(n):
        for x in range(n):
            M[0][y][x] = v(I,y,x-1) ^ v(I,y,x) ^ v(I,y,x+1) ^ Z[y][x]
    if n >= 2:
        for y in range(n):
            for x in range(n):
                M[1][y][x] = v(M[0],y,x-1) ^ v(M[0],y,x) ^ v(M[0],y,x+1) ^ I[y][x]
    for k in range(2, n):
        A, B = M[k-1], M[k-2]
        for y in range(n):
            for x in range(n):
                M[k][y][x] = v(A,y,x-1) ^ v(A,y,x) ^ v(A,y,x+1) ^ B[y][x]
    return M

def make_mat_kn(n):
    M = make_mat_k(n)
    return [row[:] for row in M[n-1]]

def make_mat_kl(n):
    def shl(v):
        return [0] + v[:-1]
    def shr(v):
        return v[1:] + [0]
    prev2 = [0]*n
    prev  = [0]*n
    rows = []
    for _ in range(n):
        cur = [ (prev[j] ^ shl(prev)[j] ^ shr(prev)[j] ^ prev2[j]) ^ 1 for j in range(n) ]
        rows.append(cur)
        prev2, prev = prev, cur
    return rows

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

MAT51 = [[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 0], [1, 0, 0, 0, 1]]
MAT52 = [[0, 1, 0, 0, 0], [0, 1, 0, 1, 1], [0, 0, 1, 0, 0], [1, 1, 0, 1, 0], [0, 1, 0, 0, 0]]
MAT53 = MAT5

MAT500 = rotate_mat(MAT5, 0)
MAT501 = rotate_mat(MAT5, 1)
MAT511 = rotate_mat(MAT5, 2)
MAT510 = rotate_mat(MAT5, 3)

MAT51_L = [[1, 0, 0, 0, 0], [0, 0, 1, 1, 1], [0, 0, 1, 0, 1], [1, 0, 1, 0, 1], [0, 1, 1, 1, 1]]
MAT52_L = [[0, 0, 1, 0, 0], [1, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 0, 1, 0]]
MAT53_L = MAT5

MAT5_L = [[0], [1], [1], [0], [1], [0], [1], [1], [1], [0], [0], [0], [1], [1], [1], [1], [1], [0], [1], [1], [1], [1], [0], [0], [0]]

MAT5qut0 = [[0, 1, 1, 1, 0], [1, 0, 1, 0, 1], [1, 1, 0, 1, 1], [1, 0, 1, 0, 1], [0, 1, 1, 1, 0]]
MAT5qut1 = [[1, 0, 1, 0, 1], [1, 0, 1, 0, 1], [0, 0, 0, 0, 0], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1]]

MAT3sum = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
MAT300 = [[1, 0, 1], [0, 0, 1], [1, 1, 0]]
MAT302 = rotate_mat(MAT300, 1)
MAT322 = rotate_mat(MAT300, 2)
MAT320 = rotate_mat(MAT300, 3)
MAT301 = [[0, 0, 0], [0, 1, 0], [1, 1, 1]]
MAT312 = rotate_mat(MAT301, 1)
MAT321 = rotate_mat(MAT301, 2)
MAT310 = rotate_mat(MAT301, 3)
MAT311 = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
MAT3 = [[MAT300, MAT301, MAT302], [MAT310, MAT311, MAT312], [MAT320, MAT321, MAT322]]

MAT3K = make_mat_k(3)
MAT4K = make_mat_k(4)
MAT5K = make_mat_k(5)
MAT3KL = make_mat_kl(3)
MAT4KL = make_mat_kl(4)
MAT5KL = make_mat_kl(5)

MAB = [[0, 0], [0, 1], [1, 0], [1, 1]]
MAB2 = [[0, 1], [0, 0], [1, 1], [1, 0]]
MXOR = [[0], [1], [1], [0]]
MNOT = [[1], [0], [0], [1]]
ML2 = [[0, 0], [0, 0], [0, 0], [0, 0]]
ML1 = [[0], [0], [0], [0]]

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

class LightsOut(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        show_title(self, "点灯游戏的$O(n^2)$解法")

        show_title(self, "首行叠加法（续上集）")

        show_subtitle(self, "在上集视频首行叠加法中，有观众对按钮和灯的递推仍有疑问。", "这次我们来讲清楚，这个递推公式是怎么来的。")

        LAT = show_latex(self, "B(n,x)=B(n-1,x-1)⊕B(n-1,x)⊕B(n-1,x+1)⊕B(n-2,x)", 0, 2)

        self.wait(0.5)
        cols, rows = 5, 5
        sz = 0.25
        G5_ = [[None] * cols for _ in range(rows)]
        for k in range(rows):
            for y in range(cols):
                mx = (y*2-cols)*(1+sz)+1
                my = -k*sz+0.5
                G5_[k][y] = make_grid(self, w=cols, h=1, w_l=1, h_l=1, lgt_x=mx+sz*(cols+3)/2, btn_x=mx, lgt_y=my, btn_y=my, sz=sz, mat=[MAT5K[k][y][:]], mat_l=[[MAT5KL[k][y]]], show=True, rt=0.05)

        show_subtitle(self, "这里，我们用B表示按钮，L表示灯，⊕（加）代表叠加，~（非）代表翻转。", "n,x,y则表示为：")

        show_subtitle(self, "n:从上到下第n行灯或按钮，也代表第y次迭代，", "因为我们是一行行进行推导的。")
        show_subtitle(self, "x:从左到右第x列按钮。将灯表示为第一行的某几个列的按钮的叠加。", "这里的x不局限于第一行。")
        show_subtitle(self, "y:从左到右第y列灯。", "这里的公式对任意第y个灯都满足，所以省去。")

        del_latex(self, [LAT]);
        del_grids(self, G5_);

#【演示】创建灯和按钮矩阵（5x5），标记n,x,y（1..5)
#【演示】高亮或圈出n,x,y

        show_subtitle(self, "让我们举一个具体的例子。", "在5x5的格子中，将灯和按钮编号1-25。")
#【演示】创建大矩阵(25x25)，以及灯向量，标记数字1-25

        show_subtitle(self, "在叠加法中，我们将灯表示为所有按钮的叠加。", "例如：L1=B1⊕B2⊕B6，L6=B1⊕B6⊕B7⊕B11。")
#【演示】将L1,B1,B2,B6点亮，然后转移到右边的大矩阵和向量种，L6同理
        show_subtitle(self, "通过这种方式我们得到了25元一次方程组，", "写成增广矩阵，也就是按钮矩阵加灯向量的形式。")
#【演示】填满所有25行（可以从左边第一列开始继续）

        show_subtitle(self, "而在首行叠加法中，我们需要把灯表示为第一行按钮的叠加。")
#【演示】画出五个矩阵和灯向量。
        show_subtitle(self, "这里的五个矩阵，", "分别代表第n列的按钮或灯是由第一行的哪几个按钮叠加的。")
        show_subtitle(self, "例如，当第一个矩阵的第一、二个灯亮起时，", "表示第一个灯由第一行的一、二个按钮叠加。")

        show_subtitle(self, "而旁边的向量，代表的是按钮或灯有没有翻转。")
        show_subtitle(self, "例如，当第一个向量的第一个灯亮起时，", "表示第一个灯除了由刚才说的按钮叠加外，还需要再翻转才是正确的状态。")
#【演示】亮起第一行两个灯，还有灯向量（第一个）
        show_subtitle(self, "由于按法是动态的，当B6还没有按下时，", "L1=B1⊕B2，即第一个灯由第一行的一、二个按钮叠加。")
        show_subtitle(self, "然后B6=~L1=~(B1⊕B2)，即第六个按钮是第一个灯的翻转。")
#【演示】亮起第一行两个灯，再亮起第二行两个按钮以及按钮向量
        show_subtitle(self, "同样道理，L6=B1⊕B6⊕B7=B1⊕~(B1⊕B2)⊕~(B1⊕B2⊕B3)=B1⊕B3。")
#【演示】画出B1,B6,B7的按钮状态，然后三个叠加再一起。
        show_subtitle(self, "又比如，L7=B2⊕B6⊕B7⊕B8=B2⊕~(B1⊕B2)⊕~(B1⊕B2⊕B3)⊕~(B2⊕B3⊕B4)=~B4")
#【演示】四个叠加在一起
        show_subtitle(self, "这样不断递推，我们可以将任意L表达为某些B1到B5的叠加，再加上翻转。")

#——————————————————————

        show_subtitle(self, "现在，我们把序号1-25用坐标x,y表示，则灯和按钮矩阵可写为以下公式：")
        LAT1 = show_latex(self, "L(n,x)=B(n-1,x-1)⊕B(n,x-1)⊕B(n,x)⊕B(n,x+1)", 0, 2)
        show_subtitle(self, "灯为上左中右按钮的叠加。")
        LAT2 = show_latex(self, "B(n+1,x)=~L(n,x)=~(B(n-1,x-1)⊕B(n,x-1)⊕B(n,x)⊕B(n,x+1))", 0, 1.5)
        show_subtitle(self, "下一行按钮是当前灯翻转。")
        LAT3 = show_latex(self, "L(n+1,x)=~L(n-1,x-1)⊕~L(n,x-1)⊕~L(n,x)⊕~L(n,x+1)", 0, 1)
        show_subtitle(self, "下一行灯是上左中右灯翻转的叠加。")

#【演示，显示并朗读这些公式】
        show_subtitle(self, "如果把翻转~提取出来，便有了一开始的推导公式：")
        LAT4 = show_latex(self, "B(n,x)=B(n-1,x-1)⊕B(n-1,x)⊕B(n-1,x+1)⊕B(n-2,x)", 0, 0.5)
        show_subtitle(self, "按钮是上一行左中右按钮和上上行按钮叠加。")
        LAT5 = show_latex(self, "L(n,x)=L(n-1,x-1)⊕L(n-1,x)⊕L(n-1,x+1)⊕L(n-2,x)", 0, 0)
        show_subtitle(self, "灯是上一行左中右按钮和上上行灯叠加。")
        del_latex(self, [LAT1, LAT2, LAT3, LAT4, LAT5]);

#【演示，显示并朗读这些公式】

        show_subtitle(self, "之前叠加时是将多个B行一起叠加。", "如果拆分为每个B元素，则相当于从上左中右的位置一个个叠加。")
#【演示】还是叠加L6，但是这次是一个一个元素
        show_subtitle(self, "这里用公式尽管是一个个元素叠加的，", "但是由于每个元素已经包含了之前叠加的结果，效果上和用行叠加是相同的。")
#【演示】还是叠加L6，这次是一起叠加

#——————————————————————

        show_subtitle(self, "这里按钮的第一行是10000，", "这是因为B1也需要表示为B1到B5的表达式，也就是B1=B1。")
#【演示】B1
        show_subtitle(self, "在上一个视频中，因为写的是L矩阵，", "因此写为L1=B1⊕B2，这里等同于B矩阵的第二行。")
#【演示】L1
        show_subtitle(self, "因为B(n+1,x)=~L(n,x)，", "因此上一行灯矩阵和下一行按钮矩阵是相同的。")
#【演示】L1到B6
        show_subtitle(self, "因为最终需要推导的是灯矩阵，因此灯矩阵是从按钮的第一行推导5行。", "因为最后一次推导的是灯，因此按钮矩阵也是5行。")
#【演示】继续推导L6。。。

#——————————————————————

        show_subtitle(self, "对于翻转的情况，则可以单独列出来，以类似的方法推导，写成Y公式：")
        LAT = show_latex(self, "Y(n,y)=~(Y(n-1,y-1)⊕Y(n-1,y)⊕Y(n-1,y+1)⊕Y(n-2,y))", 0, 2)
        show_subtitle(self, "下一行的翻转是上一行左中右和上上行叠加后的翻转。")
#【演示】翻转矩阵
        show_subtitle(self, "可以注意到，这里的公式Y和B的推导公式是类似的的。", "只不过，Y是从零向量开始推导的，并且不能省略翻转符号~。")

        show_subtitle(self, "1. 使用零向量：第一次翻转发生在从一到二行的迭代过程中，", "在此之前没有发生过翻转，因此Y的第一行就不是10000而是00000了。")
#【演示】圈出0向量
        show_subtitle(self, "2. 翻转符号~必须存在：每次迭代都需要翻转，因此不可省略。", "而前者将这个翻转取出来了，不用翻转符号~。")
#【演示】？
        show_subtitle(self, "3. 不使用x而使用y：翻转是前面所有按钮的翻转叠加后提取出来的，", "代表的是灯的翻转，而不是某个按钮的翻转。")
#【演示】将y=1..5写出来

        del_latex(self, [LAT]);

#——————————————————————


        show_title(self, "优化生成矩阵（续上集）")


