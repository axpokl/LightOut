from manimlib import *
import numpy as np

LIGHT_BLUE = "#55aaff"
PINK = "#ff55aa"

BD_W = 2
BD_W_SEL = 8
HL_COLOR = RED
DEFAULT_FONT = "SimHei"

def make_grid(scene, w, h, lgt_x=0.0, btn_x=0.0, lgt_y=0.0, btn_y=0.0, sz=1.0, rt=0.3, mat=None, mat_l=None, w_l=None, h_l=None, show=True,):
    w_l = w if w_l is None else int(w_l)
    h_l = h if h_l is None else int(h_l)

    lgt = [[False for _ in range(w_l)] for _ in range(h_l)]
    btn = [[False for _ in range(w)] for _ in range(h)]
    lgt_sel = [[False for _ in range(w_l)] for _ in range(h_l)]
    btn_sel = [[False for _ in range(w)] for _ in range(h)]

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
            lgt_bd_base[j][i] = lbd
            lgt_bd_base_grp.add(lbd)
            lbd_hl = lbd.copy().set_stroke(HL_COLOR, BD_W_SEL, 0).set_fill(opacity=0)
            lgt_bd_hl[j][i] = lbd_hl
            lgt_bd_hl_grp.add(lbd_hl)
            lsp = Square(side_length=lgt_sz).set_stroke(width=0, opacity=0).set_fill(LIGHT_BLUE, 1)
            lsp.move_to(center + lgt_shift)
            lgt_sp[j][i] = lsp
            lgt_sp_grp.add(lsp)

    for j in range(h):
        for i in range(w):
            center = np.array([btn_start_x + i * sz, btn_start_y - j * sz, 0.0])
            bbd = Square(side_length=sz).set_fill(opacity=0).set_stroke(WHITE, BD_W, 0)
            bbd.move_to(center + btn_shift)
            btn_bd_base[j][i] = bbd
            btn_bd_base_grp.add(bbd)
            bbd_hl = bbd.copy().set_stroke(HL_COLOR, BD_W_SEL, 0).set_fill(opacity=0)
            btn_bd_hl[j][i] = bbd_hl
            btn_bd_hl_grp.add(bbd_hl)
            bsp = Circle(radius=btn_sz).set_stroke(width=0, opacity=0).set_fill(PINK, 1)
            bsp.move_to(center + btn_shift)
            btn_sp[j][i] = bsp
            btn_sp_grp.add(bsp)

    if mat is not None:
        mh = len(mat)
        mw = len(mat[0]) if mh > 0 else 0
        H = min(h, mh)
        W = min(w, mw)
        for j in range(H):
            for i in range(W):
                if int(mat[j][i]) == 1:
                    btn[j][i] = True
                    for (x, y) in ((i, j), (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                        if 0 <= x < w_l and 0 <= y < h_l:
                            lgt[y][x] = not lgt[y][x]

    if mat_l is not None:
        lh = len(mat_l)
        lw = len(mat_l[0]) if lh > 0 else 0
        H2 = min(h_l, lh)
        W2 = min(w_l, lw)
        for j in range(H2):
            for i in range(W2):
                lgt[j][i] = bool(int(mat_l[j][i]))

    for j in range(h_l):
        for i in range(w_l):
            lgt_sp[j][i].set_opacity(1 if lgt[j][i] else 0)
    for j in range(h):
        for i in range(w):
            btn_sp[j][i].set_opacity(1 if btn[j][i] else 0)

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
            scene.play(
                lgt_bd_base_grp.animate.set_stroke(opacity=1),
                btn_bd_base_grp.animate.set_stroke(opacity=1),
                run_time=rt,
            )
        else:
            lgt_bd_base_grp.set_stroke(opacity=1)
            btn_bd_base_grp.set_stroke(opacity=1)
    else:
        lgt_bd_base_grp.set_stroke(opacity=1)
        btn_bd_base_grp.set_stroke(opacity=1)
        lgt_bd_hl_grp.set_stroke(opacity=0)
        btn_bd_hl_grp.set_stroke(opacity=0)

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

def gauss_grids(scene, grids, ops, start=0, end=None, rt=0.8):
    if not ops: return
    if end is None: end=len(ops)-1
    if start<0: start=0
    if end>=len(ops): end=len(ops)-1
    for k in range(start, end+1):
        op, sy, sx, ty, tx = ops[k]
        a=grids[sy][sx]
        b=grids[ty][tx]
        if op in (0, "add", "ADD", "a", "A"):
            add_grid(scene, a, b, rt)
        else:
            swap_grid(scene, a, b, rt)

def make_ops_n2(mat, n):
    A=[row[:] for row in mat]
    N=len(A)
    fwd=[]
    piv=[]
    r=0
    for c in range(N):
        p=None
        for i in range(r,N):
            if A[i][c]&1:
                p=i
                break
        if p is None: 
            continue
        if p!=r:
            A[p],A[r]=A[r],A[p]
            fwd.append([1,p//n,p%n,r//n,r%n])
        for i in range(r+1,N):
            if A[i][c]&1:
                A[i]=[x^y for x,y in zip(A[i],A[r])]
                fwd.append([0,r//n,r%n,i//n,i%n])
        piv.append((r,c))
        r+=1
        if r==N: break
    bwd=[]
    for r,c in reversed(piv):
        for i in range(r):
            if A[i][c]&1:
                A[i]=[x^y for x,y in zip(A[i],A[r])]
                bwd.append([0,r//n,r%n,i//n,i%n])
    return fwd,bwd

def make_ops_n(mat, n):
    row_y = n-1
    A=[row[:] for row in mat]
    N=len(A)
    fwd=[]
    piv=[]
    r=0
    for c in range(N):
        p=None
        for i in range(r,N):
            if A[i][c]&1:
                p=i
                break
        if p is None: 
            continue
        if p!=r:
            A[p],A[r]=A[r],A[p]
            fwd.append([1,row_y,p,row_y,r])
        for i in range(r+1,N):
            if A[i][c]&1:
                A[i]=[x^y for x,y in zip(A[i],A[r])]
                fwd.append([0,row_y,r,row_y,i])
        piv.append((r,c))
        r+=1
        if r==N: break
    bwd=[]
    for r,c in reversed(piv):
        for i in range(r):
            if A[i][c]&1:
                A[i]=[x^y for x,y in zip(A[i],A[r])]
                bwd.append([0,row_y,r,row_y,i])
    return fwd,bwd

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
    G["btn_sel"][j][i] = selected
    G["btn_bd_hl"][j][i].set_stroke(opacity=1 if selected else 0)

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
    set_bd(G, "btn", i, j, True)
    if anim == 0:
        G["btn_sp"][j][i].set_opacity(1.0 if G["btn"][j][i] else 0.0)
    else:
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
            if anim == 0:
                G["lgt_sp"][y][x].set_opacity(1.0 if G["lgt"][y][x] else 0.0)
            else:
                _queue_opacity_anim(G["lgt_sp"][y][x], 1.0 if G["lgt"][y][x] else 0.0, anims)
    if anim != 0 and anims:
        scene.play(*anims, run_time=anim)
    if wait > 0:
        scene.wait(wait)

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

def show_subtitle(scene, text, text2=None, run_in=0.3, run_out=0.3, font=DEFAULT_FONT, font_size=32, line_gap=0.2, buff=0.5, baseline=0.05, auto_k=0.5, ref_tex="N\\times N",):
    old = getattr(scene, "_subtitle_mobj", None)
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
    lines = VGroup(*[_mk_line_group(p, font, font_size, WHITE, baseline, auto_k, ref_tex) for p in parts])
    lines.arrange(DOWN, buff=line_gap).to_edge(DOWN, buff=buff)
    scene.add(lines)
    scene.play(FadeIn(lines, run_time=run_in))
    scene._subtitle_mobj = lines
    return lines

def show_title(scene, line1=None, line2=None, run_in=0.3, run_out=0.3, font=DEFAULT_FONT, size1=48, size2=32, line_gap=0.15, buff=0.5, pause=0.8, rt=0.3,):
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
    run_in=0.6,
    line_buff=0.20,
    inner_line_buff=0.10,
    hbuff=0.18,
    group_scale=0.82,
    align_left=True,
    default_indent=1.0, 
    font=DEFAULT_FONT
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
                t  = Tex(_sanitize_tex(item["tex"])).scale(s)
                cn = Text(item.get("cn",""), font=font).scale(cn_s)
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
    old = getattr(scene, "_center_latex_group", None)
    if old is not None:
        try:
            scene.play(FadeOut(old, lag_ratio=0.06, run_time=0.25))
            scene.remove(old)
        except Exception:
            pass
    scene._center_latex_group = group
    scene.play(FadeIn(group, lag_ratio=0.08, run_time=run_in))
    return group

def remove_center_latex(scene, run_out=0.8):
    g = getattr(scene, "_center_latex_group", None)
    if g is not None:
        try:
            scene.play(FadeOut(g, lag_ratio=0.08, run_time=run_out))
            scene.remove(g)
        except Exception:
            pass
        scene._center_latex_group = None

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

def press_lgt(lgt, x, y):
    H = len(lgt)
    W = len(lgt[0])
    for (xx, yy) in [(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
        if 0 <= xx < W and 0 <= yy < H:
            lgt[yy][xx] ^= 1

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

def rotate_mat(mat, k):
    k %= 4
    if k == 0: return [row[:] for row in mat]
    if k == 1: return [list(r) for r in zip(*mat[::-1])]
    if k == 2: return [row[::-1] for row in mat[::-1]]
    if k == 3: return [list(r) for r in zip(*mat)][::-1]

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
MAT3 = [
    [MAT300, MAT301, MAT302],
    [MAT310, MAT311, MAT312],
    [MAT320, MAT321, MAT322],
]

MAT3K = make_mat_k(3)
MAT4K = make_mat_k(4)
MAT5K = make_mat_k(5)
MAT3KN = [[0, 1, 1], [1, 1, 1], [1, 1, 0]]
MAT4KN = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
MAT5KN = [[0, 1, 1, 0, 1], [1, 1, 1, 0, 0], [1, 1, 0, 1, 1], [0, 0, 1, 1, 1], [1, 0, 1, 1, 0]]
MAT3KL = [[1, 1, 1], [1, 0, 1], [1, 0, 1]]
MAT4KL = [[1, 1, 1, 1], [1, 0, 0, 1], [1, 1, 1, 1], [0, 0, 0, 0]]
MAT5KL = [[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 1, 0, 1, 1], [0, 1, 1, 1, 0], [1, 0, 0, 0, 1]]


MAB = [[0, 0], [0, 1], [1, 0], [1, 1]]
MAB2 = [[0, 1], [0, 0], [1, 1], [1, 0]]
MXOR = [[0], [1], [1], [0]]
MNOT = [[1], [0], [0], [1]]
ML2 = [[0, 0], [0, 0], [0, 0], [0, 0]]
ML1 = [[0], [0], [0], [0]]

OPS3 = make_ops_n2(make_mat_l(3), 3)
OPS4 = make_ops_n2(make_mat_l(4), 4)
OPS5 = make_ops_n2(make_mat_l(5), 5)
OPS3K = make_ops_n(MAT3KN, 3)
OPS4K = make_ops_n(MAT4KN, 4)
OPS5K = make_ops_n(MAT5KN, 5)


LATEX1 = [
    {"type": "text", "content": "递推公式（Fibonacci 多项式的 GF(2) 版本）：", "scale": 0.8, "indent": 0.0},
    {"type": "tex_lines", "scale": 0.7, "content": [
        r"f(0,x)=1",
        r"f(1,x)=x",
        r"f(2,x)=(1+x)^2",
        r"f(n+1,x)=x\cdot f(n,x)+f(n-1,x)",
        r"r(n)=\operatorname{deg}(\gcd(f(n,x),\,f(n,1+x)))"
    ]},
    {"type": "text", "content": "其中：", "scale": 0.8, "indent": 0.0},
    {"type": "tex_cn_lines", "scale": 0.7, "cn_scale": 0.7, "content": [
        {"tex": r"f(n,x)\in \mathbb{F}_2[x]", "cn": "（系数域为 GF(2)）"},
        {"tex": r"\operatorname{deg}:\ \mathbb{F}_2[x]\setminus\{0\}\to \mathbb{N}", "cn": "（多项式次数）"},
        {"tex": r"\gcd:\ \mathbb{F}_2[x]\times \mathbb{F}_2[x]\to \mathbb{F}_2[x]", "cn": "（多项式最大公因子）"}
    ]},
    {"type": "text", "content": "性质：", "scale": 0.8, "indent": 0.0},
    {"type": "tex_cn_lines", "scale": 0.7, "cn_scale": 0.7, "content": [
        {"tex": r"r(n)\equiv 0\pmod{2}", "cn": "（偶数）"},
        {"tex": r"r(n)\le n", "cn": "（上界）"},
        {"tex": r"r(n)\le r((n+1)k-1)\quad (n,k\in\mathbb{N})", "cn": "（按倍数拉长的单调性）"}
    ]}
]

class LightsOut(Scene):
    def construct(self):
        self.camera.background_color = BLACK
#硬核科普
#        """
        show_title(self, "点灯游戏的$O(n^3)$解法","又名：灭灯游戏（Lights Out）")

        self.wait(1)
        G5  = make_grid(self, w=5,  h=5,  lgt_x=-4.5, btn_x=-4.5, lgt_y=-1.0, btn_y=-1.0, sz=0.6)
        G7  = make_grid(self, w=7,  h=7,  lgt_x= 0.0, btn_x= 0.0, lgt_y=-1.0, btn_y=-1.0, sz=0.5)
        G11 = make_grid(self, w=11, h=11, lgt_x= 4.5, btn_x= 4.5, lgt_y=-1.0, btn_y=-1.0, sz=0.35)
        t5  = Text("N=5",  color=WHITE).next_to(G5["groups"]["lgt_bd_base"],  UP*0.5, buff=0.3)
        t7  = Text("N=7",  color=WHITE).next_to(G7["groups"]["lgt_bd_base"],  UP*0.5, buff=0.3)
        t11 = Text("N=11", color=WHITE).next_to(G11["groups"]["lgt_bd_base"], UP*0.5, buff=0.3)
        self.play(FadeIn(t5), FadeIn(t7), FadeIn(t11), run_time=0.4)
        self.wait(1)
        apply_mat(self, G5,  MAT5,  anim=0.15)
        apply_mat(self, G7,  MAT7,  anim=0.10)
        apply_mat(self, G11, MAT11, anim=0.05)
        self.wait(2)
        del_labels(self, t5, t7, t11)
        del_grids(self, [G5, G7, G11]) 

        show_title(self, "游戏规则")

        show_subtitle(self, "规则：在 $N\\times N$ 的格子内，点击一个按钮，", "该格及周围的灯会被同时翻转。")
        self.wait(0.5)
        G5 = make_grid(self, w=5, h=5, lgt_x=0, btn_x=0, sz=0.6)
        self.wait(1)
        press(self, G5, 1, 1, wait=2)
        press(self, G5, 1, 4, wait=2)
        press(self, G5, 4, 0, wait=2)
        press(self, G5, 4, 1, wait=2)
        press(self, G5, 4, 2, wait=2)
        self.wait(2)
        del_grids(self, [G5], kp_bd=True )

        show_subtitle(self, "目标：从全暗状态打开所有灯（或者全亮状态关闭所有灯）。")
        self.wait(1)
        show_all_lights(self, G5)
        self.wait(2)
        del_grids(self, [G5], kp_bd=True ) 
        self.wait(1)
        del_grids(self, [G5]) 

        show_title(self, "基本原理")

        show_subtitle(self, "连续按两次按钮，等同于没有按。")
        self.wait(0.5)
        G5 = make_grid(self, w=5, h=5, lgt_x=0, btn_x=0, sz=0.6)
        self.wait(1)
        press(self, G5, 1, 1, wait=1.5)
        press(self, G5, 1, 1, wait=1.5)
        press(self, G5, 4, 4, wait=1.5)
        press(self, G5, 4, 4, wait=1.5)
        self.wait(1)
        del_grids(self, [G5]) 

        show_subtitle(self, "用不同顺序按按钮，灯的最终状态是一样的。")
        self.wait(0.5)
        G51 = make_grid(self, w=5, h=5, lgt_x=-2, btn_x=-2, sz=0.6)
        G52 = make_grid(self, w=5, h=5, lgt_x=+2, btn_x=+2, sz=0.6)
        self.wait(1)
        press(self, G51, 2, 1, wait=0.3)
        press(self, G51, 2, 2, wait=0.3)
        press(self, G51, 2, 3, wait=0.3)
        press(self, G51, 3, 3, wait=0.3)
        clear_all_bd(G51)
        self.wait(1)
        press(self, G52, 3, 3, wait=0.3)
        press(self, G52, 2, 3, wait=0.3)
        press(self, G52, 2, 2, wait=0.3)
        press(self, G52, 2, 1, wait=0.3)
        clear_all_bd(G52)
        self.wait(3)
        del_grids(self, [G51, G52]) 

        show_subtitle(self, "因此，格子内的按钮，我们只需考虑按或不按，并且不用关心顺序。")
        self.wait(0.5)
        G51 = make_grid(self, w=5, h=5, lgt_x=-3.0, btn_x=-3.0, sz=0.4, mat=MAT51)
        G52 = make_grid(self, w=5, h=5, lgt_x= 0.0, btn_x= 0.0, sz=0.4, mat=MAT52)
        G53 = make_grid(self, w=5, h=5, lgt_x= 3.0, btn_x= 3.0, sz=0.4, mat=MAT53)
        self.wait(3)

        show_subtitle(self, "我们可以将按钮和灯分开表示，", "所有按钮的状态为一组，对应灯的状态为一组。")
        self.wait(0.5)
        move_grid(self, G51, lgt_x=-3.0, btn_x=-3.0, lgt_y=-1.2, btn_y=1.2)
        move_grid(self, G52, lgt_x= 0.0, btn_x= 0.0, lgt_y=-1.2, btn_y=1.2)
        move_grid(self, G53, lgt_x= 3.0, btn_x= 3.0, lgt_y=-1.2, btn_y=1.2)
        self.wait(3)

        show_subtitle(self, "我们的目标是：找到一个按钮组，其对应灯的状态为全亮。", "那么，我们如何找到这样一个组按钮呢？")
        self.wait(0.5)
        hl_bd(self, G53)
        self.wait(6)
        del_bd(self, G53)
        del_grids(self, [G51, G52, G53]) 

        show_title(self, "穷举法")

        show_subtitle(self, "$N\\times N$ 个按钮共有 $2^{N\\times N}$ 种组合，每种组合对应唯一的灯状态。", "只要所有情况都试一遍，看看灯的状态如何即可。")
        self.wait(0.5)
        cols, rows = 4, 4
        sz, gap = 0.4, 0.25
        G = [[None] * cols for _ in range(rows)]
        idx = 0
        for y in range(rows):
            for x in range(cols):
                mx = -(cols - 1) * (2 * sz + gap) / 2 + x * (2 * sz + gap)
                my =  (rows - 1) * (2 * sz + gap) / 2 - y * (2 * sz + gap)
                mat = [[(idx>>0)&1, (idx>>1)&1], [(idx>>2)&1, (idx>>3)&1]]
                G[y][x] = make_grid(self, w=2, h=2, lgt_x=mx+2.5, btn_x=mx-2.5, lgt_y=my, btn_y=my, sz=sz, rt=0.1, mat=mat)
                idx += 1
        self.wait(2)

        show_subtitle(self, "例如，当 $N=2$ 时，对应的状态为 $2^{2\\times 2}=2^4=16$。", "很快我们就能列举出所有的情况并得出结论。")
        self.wait(0.5)
        hl_bd(self, G[3][3])
        self.wait(4)
        del_bd(self, G[3][3])
        del_grids(self, G)
        self.wait(1)

        show_subtitle(self, "又例如，当 $N=3$ 时，对应的状态为 $2^{3\\times 3}=2^9=512$。", "我们也可以穷举所有情况得出结论。")
        self.wait(0.5)
        G3 = make_grid(self, w=3, h=3, lgt_x=2, btn_x=-2, sz=1)
        label_fix = Text("N=", color=WHITE).scale(0.8)
        label_num = Integer(0, color=WHITE).scale(0.8)
        label_grp = VGroup(label_fix, label_num).arrange(RIGHT, buff=0.1)
        label_grp.move_to(ORIGIN).shift(DOWN * 2).shift(LEFT * 0.2)
        self.add(label_grp)
        p = 0
        for i in range(1, 512):
            g = i ^ (i >> 1)
            k = (p ^ g).bit_length() - 1
            hit = (i % 3 == 0)
            press(self, G3, k % 3, k // 3, wait=0.01 if hit else 0.0, anim=0.0)
            if hit:
                label_num.set_value(i)
            if g == int("101010101", 2):
                break
            p = g
        self.wait(3)
        self.play(FadeOut(label_grp, run_time=0.3))
        self.remove(label_grp)
        del_grids(self, [G3])

        show_subtitle(self, "对于 $N=5$，也就是一开始的经典问题，", "其状态数为 $2^{5\\times 5}=2^{25}=33\\,554\\,432$，需要计算机来求解。")
        self.wait(0.5)
        G500 = make_grid(self, w=5, h=5, lgt_x=-1.2, btn_x=-1.2, lgt_y= 1.2, btn_y= 1.2, sz=0.35, mat=MAT500)
        G501 = make_grid(self, w=5, h=5, lgt_x= 1.2, btn_x= 1.2, lgt_y= 1.2, btn_y= 1.2, sz=0.35, mat=MAT501)
        G510 = make_grid(self, w=5, h=5, lgt_x=-1.2, btn_x=-1.2, lgt_y=-1.2, btn_y=-1.2, sz=0.35, mat=MAT510)
        G511 = make_grid(self, w=5, h=5, lgt_x= 1.2, btn_x= 1.2, lgt_y=-1.2, btn_y=-1.2, sz=0.35, mat=MAT511)
        self.wait(4)
        del_grids(self, [G500, G501, G510, G511])

        show_subtitle(self, "当 $N=6$ 时，状态数为 $2^{36}=68\\,719\\,476\\,736$。", "复杂度增长得太快，计算机也难以求解。")
        self.wait(0.5)
        G6 = make_grid(self, w=6, h=6, sz=0.5)
        self.wait(4)

        show_subtitle(self, "那我们该怎么办呢？", "有没有更快更巧妙的解法呢？")
        self.wait(0.5)
        show_all_lights(self, G6)
        self.wait(6)
        del_grids(self, [G6])

        show_title(self, "首行穷举法")

        show_subtitle(self, "细心的小伙伴会发现，无论什么局面，", "我们都能一行一行按按钮，点亮尽可能多的灯。")
        self.wait(0.5)
        G51 = make_grid(self, w=5, h=5, lgt_x=-4.0, btn_x=-4.0, sz=0.6)
        G52 = make_grid(self, w=5, h=5, lgt_x= 0.0, btn_x= 0.0, sz=0.6)
        G53 = make_grid(self, w=5, h=5, lgt_x= 4.0, btn_x= 4.0, sz=0.6)
        self.wait(1)
        for r in range(5):
            apply_mat(self, G51, slice_mat(MAT51_L, r, r), anim=0.2, clear_end=True)
            apply_mat(self, G52, slice_mat(MAT52_L, r, r), anim=0.2, clear_end=True)
            apply_mat(self, G53, slice_mat(MAT53_L, r, r), anim=0.2, clear_end=True)
            self.wait(1)
        self.wait(2)
        del_grids(self, [G51, G52, G53])

        show_subtitle(self, "例如，我们在第1行随机点击了几个按钮。", "此时，第1行的灯有些是亮的，有些是暗的。")
        self.wait(0.5)
        G5 = make_grid(self, w=5, h=5, lgt_x= 0.0, btn_x= 0.0, sz=0.6)
        apply_mat(self, G5, slice_mat(MAT51_L, 0, 0), anim=0.5, clear_end=True)
        self.wait(1)
        set_bd(G5, "lgt", 2, 0, True)
        set_bd(G5, "lgt", 3, 0, True)
        set_bd(G5, "lgt", 4, 0, True)
        self.wait(3)
        clear_all_bd(G5)

        show_subtitle(self, "为了让第1行的灯全亮，", "我们可以去按暗的灯下方的第2行的对应按钮。")
        self.wait(0.5)
        set_bd(G5, "btn", 2, 1, True)
        set_bd(G5, "btn", 3, 1, True)
        set_bd(G5, "btn", 4, 1, True)
        self.wait(2)
        apply_mat(self, G5, slice_mat(MAT51_L, 1, 1), anim=0.5, clear_end=True)
        self.wait(3)

        show_subtitle(self, "这时候，第2行的某些灯是暗的。", "因为按第2行的按钮会熄灭第1行的灯，我们要按第3行的按钮。")
        self.wait(0.5)
        set_bd(G5, "lgt", 2, 1, True)
        set_bd(G5, "lgt", 4, 1, True)
        self.wait(3)
        apply_mat(self, G5, slice_mat(MAT51_L, 2, 2), anim=0.5, clear_end=True)
        self.wait(4)

        show_subtitle(self, "重复这一步骤，直到按完最后一行的按钮。", "如果最后一行的灯恰好全亮了，那我们就找到了一种解法。")
        self.wait(0.5)
        apply_mat(self, G5, slice_mat(MAT51_L, 3, 5), anim=0.5, clear_end=True)
        self.wait(1)
        set_bd(G5, "lgt", 0, 4, True)
        set_bd(G5, "lgt", 1, 4, True)
        set_bd(G5, "lgt", 2, 4, True)
        self.wait(1)
        show_subtitle(self, "这里有灯还是暗的，因此不是正确解法。", "让我们换一种解法。")
        self.wait(5)
        del_grids(self, [G5], kp_bd=True )

        show_subtitle(self, "这次，让我们点击第1行的前两个按钮。")
        self.wait(0.5)
        apply_mat(self, G5, slice_mat(MAT53_L, 0, 0), anim=0.5, clear_end=True)
        self.wait(3)

        show_subtitle(self, "经过递推，最后一行灯都被点亮了，因此这就是一种正确解法。")
        self.wait(0.5)
        apply_mat(self, G5, slice_mat(MAT53_L, 1, 4), anim=0.2, clear_end=True)
        self.wait(4)
        del_grids(self, [G5])

        show_subtitle(self, "由于从第2行开始，每一行的按法都由上一行的灯确定，", "因此，我们只需遍历第1行的所有按法，递推最后一行灯即可。")
        self.wait(0.5)
        cols, rows = 8, 4
        sz, gap = 0.2, 0.8
        MAT_btn = []
        MAT_lgt = []
        sol_idx = []
        for i in range(32):
            mb, ml = build_case(i, w=5, h=5)
            MAT_btn.append(mb)
            MAT_lgt.append(ml)
            if all(ml[4][c] == 1 for c in range(5)):
                sol_idx.append(i)
        G = [[None] * cols for _ in range(rows)]
        for idx in range(32):
            x = idx % cols
            y = idx // cols
            mx = -(cols - 1) * (2 * sz + gap) / 2 + x * (2 * sz + gap)
            my = (rows - 1) * (2 * sz + gap) / 2 - y * (2 * sz + gap)
            G[y][x] = make_grid(self, w=5, h=5, lgt_x=mx, btn_x=mx,lgt_y=my,btn_y=my,sz=sz,rt=0.01,mat=slice_mat(MAT_btn[idx],0,0))
        self.wait(1)

        show_subtitle(self, "通过这种行之间的关系，我们把随机性限制在第1行，使穷举量降到了 $2^N$。", "这里，我们在 32 种按法中找到了四种解法。")
        self.wait(0.5)
        for idx in range(32):
            x = idx % cols
            y = idx // cols
            apply_mat(self, G[y][x], slice_mat(MAT_btn[idx], 1, rows-1), anim=0.1, clear_end=True)
            if idx in sol_idx:
                hl_bd(self, G[y][x], rt=0.1)
        self.wait(4)

        show_subtitle(self, "这个方法的复杂度仍是指数级别的。", "那么，有没有更快更精妙的解法呢？")
        self.wait(6)
        for idx in range(32):
            x = idx % cols
            y = idx // cols
            del_bd(self, G[y][x], rt=0.01)
        del_grids(self, G)

        show_title(self, "叠加法")

        show_subtitle(self, "对于 $N\\times N$ 的格子来说，", "我们的基本操作只有 $N\\times N$ 种，也就是按或者不按某个按钮。")
        self.wait(0.5)
        cols, rows = 3, 3
        sz, gap = 0.4, 0.7
        G3 = [[None] * cols for _ in range(rows)]
        MAT3_0 = [[None] * cols for _ in range(rows)]
        for y in range(rows):
            for x in range(cols):
                mx = -(cols - 1) * (2 * sz + gap) / 2 + x * (2 * sz + gap)
                my =  (rows - 1) * (2 * sz + gap) / 2 - y * (2 * sz + gap)
                mat= [[1 if (j == y and i == x) else 0 for i in range(cols)] for j in range(rows)]
                MAT3_0[y][x] = [row[:] for row in mat]
                G3[y][x] = make_grid(self, w=cols, h=rows, lgt_x=mx + 2.5, btn_x=mx - 2.5, lgt_y=my, btn_y=my, sz=sz, rt=0.1, mat=mat)
        self.wait(4)

        show_subtitle(self, "对于某一特定的灯，只有周围几个按钮可以改变其状态。", "比如这里的第1个灯，只会被左上角的三个按钮影响。")
        self.wait(0.5)
        hl_cells(self, [G3[0][1], G3[1][0], G3[0][0]], which="lgt", indices=[(0,0)])
        self.wait(4)

        show_subtitle(self, "按多个按钮相当于把多种操作叠加起来。", "我们把这三个操作叠加起来得到第1个灯的状态。")
        self.wait(0.5)
        add_grid(self, G3[0][1], G3[0][0], rt=1)
        add_grid(self, G3[1][0], G3[0][0], rt=1)
        self.wait(4)
        del_cells(self, [G3[0][1], G3[1][0], G3[0][0]], which="lgt", indices=[(0,0)])

        show_subtitle(self, "有没有办法叠加多种操作后，只亮一个灯呢？")
        self.wait(0.5)
        show_mats(self, G3, MAT3)
        self.wait(4)

        show_subtitle(self, "如果每一个灯都可以单独点亮，", "那我们就能把这些操作都叠加起来，让所有灯全亮。")
        self.wait(0.5)
        for y in range(rows):
            for x in range(cols):
                if not(x == 1 and y == 1): 
                    add_grid(self, G3[y][x], G3[1][1], rt=0.5)
        hl_bd(self, G3[1][1])
        self.wait(5)
        del_bd(self, G3[1][1])
        del_grids(self, G3, kp_bd=True )

        show_subtitle(self, "现在，让我们重新观察 $3 \\times 3$ 的格子，共有九种操作，标记为操作1到9。")
        self.wait(0.5)
        show_mats(self, G3, MAT3_0)
        self.wait(4)

        show_subtitle(self, "让我们观察第1个灯。", "这里，操作1、操作2都翻转了第1个灯。")
        self.wait(0.5)
        hl_cells(self, [G3[0][0], G3[0][1]], which="lgt", indices=[(0,0)])
        self.wait(4)

        show_subtitle(self, "现在，我们把操作1叠加到操作2上，", "操作2就不会翻转第1个灯了。")
        self.wait(0.5)
        gauss_grids(self, G3, OPS3[0], start=0, end=0)
        self.wait(4)
        del_cells(self, [G3[0][0], G3[0][1]], which="lgt", indices=[(0,0)])

        show_subtitle(self, "同样，操作4也会翻转第1个灯，", "我们也把操作1叠加到操作4上。")
        self.wait(0.5)
        hl_cells(self, [G3[0][0], G3[1][0]], which="lgt", indices=[(0,0)])
        self.wait(2)
        gauss_grids(self, G3, OPS3[0], start=1, end=1)
        self.wait(4)
        del_cells(self, [G3[0][0], G3[1][0]], which="lgt", indices=[(0,0)])

        show_subtitle(self, "如此一来，只有操作1能够翻转第1个灯。")
        self.wait(0.5)
        hl_cells(self, G3, which="lgt", indices=[(0,0)])
        self.wait(4)
        del_cells(self, G3, which="lgt", indices=[(0,0)])

        show_subtitle(self, "接着我们看第2个灯。")
        self.wait(0.5)
        hl_cells(self, [G3[0][1], G3[0][2], G3[1][0], G3[1][1]], which="lgt", indices=[(1,0)])
        self.wait(2)
        show_subtitle(self, "同样的，在操作2到9中，", "我们找到会翻转第2个灯的操作，把操作2叠加上去。")
        self.wait(4)

        show_subtitle(self, "这里，由于操作2没有翻转第2个灯，", "我们就交换操作2和操作3的位置。")
        self.wait(0.5)
        gauss_grids(self, G3, OPS3[0], start=2, end=2)
        self.wait(4)

        show_subtitle(self, "然后我们把操作2叠加到操作4和操作5上。")
        self.wait(0.5)
        gauss_grids(self, G3, OPS3[0], start=3, end=4)
        self.wait(4)
        del_cells(self, G3, which="lgt", indices=[(1,0)])

        show_subtitle(self, "重复以上步骤，就能确保操作n只能翻转第n到9个灯。")
        self.wait(0.5)
        gauss_grids(self, G3, OPS3[0], start=5)
        self.wait(2)

        show_subtitle(self, "由于操作9不能翻转第1到8个灯，只能翻转第9个灯，", "于是我们便发现了单独翻转第9个灯的操作。")
        self.wait(0.5)
        hl_cells(self, [G3[2][2]], which="lgt", indices=[(2,2)])
        self.wait(4)
        del_cells(self, G3, which="lgt", indices=[(2,2)])

        show_subtitle(self, "然后，我们再回过来考察操作8，", "幸运的是，操作8可以单独翻转第8个灯。")
        self.wait(0.5)
        hl_cells(self, [G3[2][1]], which="lgt", indices=[(1,2)])
        self.wait(4)
        del_cells(self, G3, which="lgt", indices=[(1,2)])

        show_subtitle(self, "我们再观察操作7。", "操作7会同时翻转第7个灯和第9个灯。")
        self.wait(0.5)
        hl_cells(self, [G3[2][0]], which="lgt", indices=[(0,2)])
        hl_cells(self, [G3[2][2], G3[2][0]], which="lgt", indices=[(2,2)])
        self.wait(4)
        show_subtitle(self, "我们可以把操作9叠加上去，", "使操作7可以单独翻转第7个灯。")
        gauss_grids(self, G3, OPS3[1], start=1, end=1)
        self.wait(4)
        del_cells(self, G3, which="lgt", indices=[(0,2)])
        del_cells(self, G3, which="lgt", indices=[(2,2)])

        show_subtitle(self, "让我们继续去叠加剩余的操作。")
        self.wait(0.5)
        gauss_grids(self, G3, OPS3[1], start=0, end=0)
        gauss_grids(self, G3, OPS3[1], start=2)
        show_subtitle(self, "最终，我们得到了全部单独翻转第1到第9个灯的操作。")
        self.wait(4)

        show_subtitle(self, "现在，我们把这9个操作叠加起来，就得到了游戏的解法。")
        self.wait(0.5)
        for y in range(rows):
            for x in range(cols):
                if not(x == 1 and y == 1): 
                    add_grid(self, G3[y][x], G3[1][1], rt=0.5)
        hl_bd(self, G3[1][1])
        self.wait(6)
        del_bd(self, G3[1][1])

        show_subtitle(self, "让我们再次重新观察这些 $3 \\times 3$ 的格子。")
        self.wait(0.5)
        show_mats(self, G3, MAT3_0)
        self.wait(4)

        show_subtitle(self, "事实上，我们可以将所有按钮和灯排列成一行。", "现在，所有按钮和灯排列成9x9的大矩阵。")
        self.wait(0.5)
        cols, rows = 3, 3
        sz = 0.4
        G3_ = [[None] * cols for _ in range(rows)]
        mat_l = make_mat_l(rows)
        for y in range(rows):
            for x in range(cols):
                idx = y * cols + x
                my = ((rows * cols) - 1) * sz / 2 - idx * sz
                mat = [[1 if k == idx else 0 for k in range(rows*cols)]]
                G3_[y][x] = make_grid(self, w=cols * rows, h=1, lgt_x=+2.5, btn_x=-2.5, lgt_y=my, btn_y=my, sz=sz, rt=0.1, mat=mat, mat_l=[mat_l[idx][:]], show=False)
                trans_grid(self, G3[y][x], G3_[y][x])
        self.wait(4)
        
        show_subtitle(self, "不难发现，我们刚才的操作，就是对这个矩阵进行高斯消元。", "通过把一行加到另一行，或者交换两行，让矩阵变为上三角矩阵。")
        self.wait(0.5)
        gauss_grids(self, G3_, OPS3[0])
        self.wait(2)
        show_subtitle(self, "然后，再把行逆推回去，变为单位矩阵。")
        self.wait(0.5)
        gauss_grids(self, G3_, OPS3[1])

        show_subtitle(self, "最后，再把所有行加起来，就得到一组完整的解法。")
        self.wait(0.5)
        my = ((rows * cols) - 1) * sz / 2 - (rows * cols + 1) * sz
        G3_sum = make_grid(self, w=(rows * cols), h=1, lgt_x=2.5, btn_x=-2.5, lgt_y=my, btn_y=my, sz=sz, rt=0.1, show=True)
        for y in range(rows):
            for x in range(cols):
                add_grid(self, G3_[y][x], G3_sum)
        del_grids(self, G3_)
        G3sum = make_grid(self, w=3, h=3, lgt_x=2.5, btn_x=-2.5, sz=sz*2, rt=0.1, mat=MAT3sum, show=False)
        trans_grid(self, G3_sum, G3sum)
        self.wait(6)
        del_grids(self, [G3sum])

        show_subtitle(self, "对于 $5 \\times 5$ 的格子，我们也可以这样操作。", "我们生成按钮和灯矩阵，然后对其进行消元。")
        self.wait(0.5)
        cols, rows = 5, 5
        sz = 0.15
        G5_ = [[None] * cols for _ in range(rows)]
        mat_l = make_mat_l(rows)
        for y in range(rows):
            for x in range(cols):
                idx = y * cols + x
                my = ((rows * cols) - 1) * sz / 2 - idx * sz
                mat = [[1 if k == idx else 0 for k in range(rows*cols)]]
                G5_[y][x] = make_grid(self, w=cols * rows, h=1, lgt_x=+2.5, btn_x=-2.5, lgt_y=my, btn_y=my, sz=sz, rt=0.01, mat=mat, mat_l=[mat_l[idx][:]], show=True)
        self.wait(2)
        gauss_grids(self, G5_, OPS5[0], rt=0.01)
        self.wait(1)
        gauss_grids(self, G5_, OPS5[1], rt=0.01)
        self.wait(4)

        show_subtitle(self, "我们把25种操作叠加起来，这就是 $5 \\times 5$ 的一种解法。")
        self.wait(0.5)
        my = ((rows * cols) - 1) * sz / 2 - (rows * cols + 1) * sz
        G5_sum = make_grid(self, w=(rows * cols), h=1, lgt_x=2.5, btn_x=-2.5, lgt_y=my, btn_y=my, sz=sz, rt=0.1, show=True)
        for y in range(rows):
            for x in range(cols):
                add_grid(self, G5_[y][x], G5_sum, rt=0.01)
        self.wait(4)

        show_subtitle(self, "可以注意到，消元后的矩阵最后两行，灯矩阵的部分为空白。", "也就是说，这两组操作没有翻动任何灯，我们称之为静默操作。")
        self.wait(0.5)
        hl_bd(self, G5_[4][3], width=BD_W_SEL/2, buff=0.03)
        hl_bd(self, G5_[4][4], width=BD_W_SEL/2, buff=0.03)
        self.wait(4)
        del_grids(self, [G5_[r][c] for r in range(rows) for c in range(cols) if not (r == 4 and c in (3, 4))])
        G5qut = [[None] * 2 for _ in range(2)]
        G5qut[1][0] = make_grid(self, w=rows, h=cols, lgt_x=2.5-1, btn_x=-2.5-1, lgt_y=-0.0, btn_y=-0.0, sz=sz*2, rt=0.0, mat=MAT5qut1, show=False)
        G5qut[1][1] = make_grid(self, w=rows, h=cols, lgt_x=2.5+1, btn_x=-2.5+1, lgt_y=-0.0, btn_y=-0.0, sz=sz*2, rt=0.0, mat=MAT5qut0, show=False)
        trans_grid(self, G5_[4][3], G5qut[1][1])
        trans_grid(self, G5_[4][4], G5qut[1][0])
        G5sum = make_grid(self, w=rows, h=cols, lgt_x=2.5, btn_x=-2.5, lgt_y=my+0.5, btn_y=my+0.5, sz=sz, rt=0.0, mat=rotate_mat(MAT5, 2), show=False)
        trans_grid(self, G5_sum, G5sum)
        self.wait(4)

        show_subtitle(self, "我们将其两两组合，形成四种静默操作。")
        self.wait(0.5)
        G5qut[0][0] = make_grid(self, w=rows, h=cols, lgt_x=2.5-1, btn_x=-2.5-1, lgt_y=-my-0.25, btn_y=-my-0.25, sz=sz*2, show=True)
        G5qut[0][1] = make_grid(self, w=rows, h=cols, lgt_x=2.5+1, btn_x=-2.5+1, lgt_y=-my-0.25, btn_y=-my-0.25, sz=sz*2, show=True)
        self.wait(1)
        add_grid(self, G5qut[1][0], G5qut[0][1])
        add_grid(self, G5qut[1][1], G5qut[0][1])
        self.wait(4)

        show_subtitle(self, "由于静默操作不会改变灯，我们也可以把它们分别和刚才的解法叠加。", "这也是刚才首行穷举法得到的四种解法。")
        self.wait(0.5)
        add_grid(self, G5sum, G5qut[0][0])
        add_grid(self, G5sum, G5qut[0][1])
        add_grid(self, G5sum, G5qut[1][0])
        add_grid(self, G5sum, G5qut[1][1])
        self.wait(6)
        del_grids(self, [G5sum])
        del_grids(self, G5qut)

        show_subtitle(self, "由于静默操作的存在，至少有两种按法对应同一种灯的状态。", "因此，总会有一种灯的状态没法按出来。例如仅翻转第一个灯。")
        self.wait(0.5)
        mat = [[1 if (j==0 and i==0) else 0 for i in range(5)] for j in range(5)]
        G5 = make_grid(self, w=5, h=5, lgt_x= 0.0, btn_x= 0.0, sz=0.6, mat_l=mat)
        self.wait(6)
        del_grids(self, [G5])

        show_title(self, "增广矩阵法")

        show_subtitle(self, "按钮会影响周围的灯，同样，灯也只会被附近的按钮翻转。", "因此，灯的最终状态可以表示为若干个按钮的叠加，也就是全亮。")
        self.wait(0.5)
        cols, rows = 5, 5
        sz = 0.15
        G5_ = [[None] * cols for _ in range(rows)]
        mat_l = make_mat_l(rows)
        for y in range(rows):
            for x in range(cols):
                idx = y * cols + x
                my = ((rows * cols) - 1) * sz / 2 - idx * sz
                G5_[y][x] = make_grid(self, w=cols * rows, h=1, w_l=1, h_l=1, lgt_x=1.25, btn_x=-1.25, lgt_y=my, btn_y=my, sz=sz, rt=0.01, mat=[mat_l[idx][:]], mat_l=[[1]], show=True)
        self.wait(5)

        show_subtitle(self, "前者，我们对按钮和灯矩阵进行消元，相当于同时乘以逆矩阵。", "现在，我们对灯向量做相同的操作，便获得了按钮的状态，也就是解法。")
        self.wait(0.5)
        gauss_grids(self, G5_, OPS5[0], rt=0.01)
        self.wait(1)
        gauss_grids(self, G5_, OPS5[1], rt=0.01)
        self.wait(5)

        show_subtitle(self, "由于灯向量是全亮，矩阵和向量相乘，等同于把所有按法叠加。", "通过这个方法，我们无需求出逆矩阵，直接通过消元获得了解法。")
        self.wait(0.5)
        G5_l_ = make_grid(self, w=1, h=cols * rows, w_l=1, h_l=cols * rows, lgt_x=1.25, btn_x=1.25, lgt_y=0.0, btn_y=0.0, sz=sz, rt=0.0, mat_l=MAT5_L, show=True)
        G5_l = make_grid(self, w=cols, h=rows, lgt_x=3.0, btn_x=3.0, sz=sz*2, rt=0.0, mat_l=MAT510, show=False)
        trans_grid(self, G5_l_, G5_l)
        self.wait(5)

        show_subtitle(self, "因为灯和按钮各有 $N \\times N$ 个，每一行都有 $N \\times N$ 个按钮叠加，", "因此该方法的复杂度为 $(N \\times N)^3 = N^6$ 。")
        self.wait(5)
        show_subtitle(self, "这个方法的复杂度是多项式级别的，但 $N \\times N$ 的矩阵仍然很大。", "那么，我们是否还能找到更快、更巧妙的解法呢？")
        self.wait(6)
        del_grids(self, G5_)
        del_grids(self, [G5_l])

        show_title(self, "首行叠加法")

        show_subtitle(self, "刚才，我们把按钮和灯当作整体叠加，并未分行。", "然而，从首行穷举法可知，只要确定第一行按钮，就能推得最后一行灯。")
        self.wait(0.5)
        G51 = make_grid(self, w=5, h=5, lgt_x=-4.0, btn_x=-4.0, sz=0.6)
        G52 = make_grid(self, w=5, h=5, lgt_x= 0.0, btn_x= 0.0, sz=0.6)
        G53 = make_grid(self, w=5, h=5, lgt_x= 4.0, btn_x= 4.0, sz=0.6)
        self.wait(1)
        for r in range(5):
            apply_mat(self, G51, slice_mat(MAT51_L, r, r), anim=0.2, clear_end=True)
            apply_mat(self, G52, slice_mat(MAT52_L, r, r), anim=0.2, clear_end=True)
            apply_mat(self, G53, slice_mat(MAT53_L, r, r), anim=0.2, clear_end=True)
        self.wait(2)
        show_subtitle(self, "是否可以将叠加法和首行穷举法结合，", "用第一行按钮直接表示最后一行的灯呢？")
        for r in range(5):
            hl_cells(self, [G51, G52, G53], which="btn", indices=[(r,0)], rt=0.01)
            hl_cells(self, [G51, G52, G53], which="lgt", indices=[(r,4)], rt=0.01)
        self.wait(4)
        del_grids(self, [G51, G52, G53])

        show_subtitle(self, "从首行穷举法我们知道，灯由周围的按钮确定，下一行的按钮则是灯的翻转。", "我们把一行的灯单独列出来，用按钮表示状态。")
        self.wait(0.5)
        cols, rows = 5, 5
        sz = 0.25
        G5_ = [[None] * cols for _ in range(rows)]
        for k in range(1):
            for y in range(cols):
                mx = (y*2-cols)*(1+sz)+1
                my = -k*sz-0.5
                G5_[k][y] = make_grid(self, w=cols, h=1, w_l=1, h_l=1, lgt_x=mx+sz*(cols+3)/2, btn_x=mx, lgt_y=my, btn_y=my, sz=sz, mat=[MAT5K[k][y][:]], mat_l=[[MAT5KL[k][y]]], show=True, rt=0.1)
        self.wait(5)

        show_subtitle(self, "例如这里，左边第一行代表第一个灯由第1、2个按钮决定，", "旁边的蓝色方格代表按钮是灯的翻转。")
        self.wait(0.5)
        hl_cells(self, [G5_[0][0]], which="btn", indices=[(0,0)])
        hl_cells(self, [G5_[0][0]], which="btn", indices=[(1,0)])
        hl_cells(self, [G5_[0][0]], which="lgt", indices=[(0,0)])
        self.wait(5)
        del_cells(self, [G5_[0][0]], which="btn", indices=[(0,0)])
        del_cells(self, [G5_[0][0]], which="btn", indices=[(1,0)])
        del_cells(self, [G5_[0][0]], which="lgt", indices=[(0,0)])

        show_subtitle(self, "需要注意，两个状态先叠加再翻转，等价于先翻转其中一个再叠加另一个。", "因此，我们可以将翻转的情况单独列出来。")
        self.wait(0.5)
        szab = 0.35
        my = 1.0
        gap = 1.4
        dy=0.25
        scale=0.6
        Bab  = make_grid(self, w=2, h=4, w_l=2, h_l=4, lgt_x=-4 + gap*0, btn_x=-4 + gap*0, lgt_y=my, btn_y=my, sz=szab, mat=MAB,  mat_l=ML2)
        L1=make_grid_label(self,Bab,r"a, b",dy,scale)
        Bxor = make_grid(self, w=1, h=4, w_l=1, h_l=4, lgt_x=-4 + gap*1, btn_x=-4 + gap*1, lgt_y=my, btn_y=my, sz=szab, mat=MXOR, mat_l=ML1)
        L2=make_grid_label(self,Bxor,r"a \oplus b",dy,scale)
        Bnot = make_grid(self, w=1, h=4, w_l=1, h_l=4, lgt_x=-4 + gap*2, btn_x=-4 + gap*2, lgt_y=my, btn_y=my, sz=szab, mat=MNOT, mat_l=ML1)
        L3=make_grid_label(self,Bnot,r"\lnot(a \oplus b)",dy,scale)
        Bab2  = make_grid(self, w=2, h=4, w_l=2, h_l=4, lgt_x=4 - gap*2, btn_x=4 - gap*2, lgt_y=my, btn_y=my, sz=szab, mat=MAB,  mat_l=ML2)
        L4=make_grid_label(self,Bab2,r"a, b",dy,scale)
        Bnot2 = make_grid(self, w=2, h=4, w_l=2, h_l=4, lgt_x=4 - gap*1, btn_x=4 - gap*1, lgt_y=my, btn_y=my, sz=szab, mat=MAB2, mat_l=ML2)
        L5=make_grid_label(self,Bnot2,r"a,\lnot b",dy,scale)
        Bxor2 = make_grid(self, w=1, h=4, w_l=1, h_l=4, lgt_x=4 - gap*0, btn_x=4 - gap*0, lgt_y=my, btn_y=my, sz=szab, mat=MNOT, mat_l=ML1)
        L6=make_grid_label(self,Bxor2,r"a \oplus \lnot b",dy,scale)
        self.wait(4)
        show_subtitle(self, "另外，如果某个按钮被叠加了两次，那就等同于没有叠加。", "同样，如果灯被翻转两次，也等同于没有翻转。")
        self.wait(4)

        show_subtitle(self, "接着推导第二行，可由上一行按钮状态（左中右）叠加确定，", "因为灯的翻转可以单独列出，也由灯的翻转状态（左中右）叠加确定。")
        self.wait(0.5)
        for k in range(1, 2):
            for y in range(cols):
                mx = (y*2-cols)*(1+sz)+1
                my = -k*sz-0.5
                G5_[k][y] = make_grid(self, w=cols, h=1, w_l=1, h_l=1, lgt_x=mx+sz*(cols+3)/2, btn_x=mx, lgt_y=my, btn_y=my, sz=sz, mat=[MAT5K[k][y][:]], mat_l=[[MAT5KL[k][y]]], show=True, rt=0.1)
        self.wait(2)
        hl_cells(self, [G5_[0][0], G5_[1][0]], which="btn", indices=[(0,0)])
        hl_cells(self, [G5_[0][0]], which="btn", indices=[(1,0)])
        hl_cells(self, [G5_[0][0], G5_[1][0], G5_[0][1]], which="lgt", indices=[(0,0)])
        show_subtitle(self, "这里分别表示第二行第一个按钮和灯，", "分别为上一行的按钮或灯的叠加或翻转。")
        self.wait(5)
        del_cells(self, [G5_[0][0], G5_[1][0]], which="btn", indices=[(0,0)])
        del_cells(self, [G5_[0][0]], which="btn", indices=[(1,0)])
        del_cells(self, [G5_[0][0], G5_[1][0], G5_[0][1]], which="lgt", indices=[(0,0)])

        show_subtitle(self, "接着推导剩余的部分。")
        self.wait(0.5)
        for k in range(2, rows):
            for y in range(cols):
                mx = (y*2-cols)*(1+sz)+1
                my = -k*sz-0.5
                G5_[k][y] = make_grid(self, w=cols, h=1, w_l=1, h_l=1, lgt_x=mx+sz*(cols+3)/2, btn_x=mx, lgt_y=my, btn_y=my, sz=sz, mat=[MAT5K[k][y][:]], mat_l=[[MAT5KL[k][y]]], show=True, rt=0.1)
        self.wait(3)
        show_subtitle(self, "于是，我们可以由第一行按钮的状态开始，", "不断推导，得到最后一行灯是由第一行哪几个按钮叠加的。")
        for y in range(cols):
            hl_bd(self, G5_[4][y], width=BD_W_SEL/2, buff=0.03)
        self.wait(5)

        show_subtitle(self, "最后，我们便得到了一种与叠加法类似的矩阵，用按钮表示灯的状态。", "只不过这一次，灯和按钮都只有 $N$ 个。")
        self.wait(0.5)
        del_grid_label(self, [L1,L2,L3,L4,L5,L6])
        del_grids(self, [Bab, Bxor, Bnot, Bab2, Bnot2, Bxor2])
        del_grids(self, G5_[:-1])
        for y in range(cols):
            mx = -sz*2
            my = -(y-(cols-1)/2)*sz*2
            del_bd(self, G5_[4][y])
            move_grid(self, G5_[rows-1][y], lgt_x=mx+sz*2*(cols+3)/2, btn_x=mx, lgt_y=my, btn_y=my, sz=sz*2)
        self.wait(4)

        show_subtitle(self, "由于在推导的过程中灯进行了翻转，", "因此最终灯向量也是翻转过的状态。")
        self.wait(0.5)
        hl_cells(self, G5_[4], which="lgt", indices=[(0,0)])
        self.wait(3)
        del_cells(self, G5_[4], which="lgt", indices=[(0,0)])

        show_subtitle(self, "现在，我们对矩阵消元，", "同时操作灯向量，最终得到第一行按钮的状态。")
        self.wait(0.5)
        gauss_grids(self, G5_, OPS5K[0])
        gauss_grids(self, G5_, OPS5K[1])
        self.wait(4)

        show_subtitle(self, "可以注意到，消元后的矩阵和之前25x25的情况一样，", "最后两行为静默操作，而右边的灯向量就是解法。")
        self.wait(0.5)
        for r in range(5):
            hl_cells(self, [G5_[4][3], G5_[4][4]], which="btn", indices=[(r,0)], rt = 0.1)
        hl_cells(self, G5_[4], which="lgt", indices=[(0,0)])
        self.wait(4)
        for r in range(5):
            del_cells(self, [G5_[4][3], G5_[4][4]], which="btn", indices=[(r,0)], rt = 0.1)
        del_cells(self, G5_[4], which="lgt", indices=[(0,0)])

        show_subtitle(self, "求出静默操作需要获得逆矩阵，有兴趣的小伙伴可以自己试一下。", "实际上，由于矩阵的高度对称性，这里的列向量和静默操作是相同的。")
        self.wait(0.5)
        hl_cells(self, [G5_[4][0], G5_[4][1], G5_[4][2]], which="btn", indices=[(3,0)])
        hl_cells(self, [G5_[4][0], G5_[4][1], G5_[4][2]], which="btn", indices=[(4,0)])
        self.wait(4)
        del_cells(self, [G5_[4][0], G5_[4][1], G5_[4][2]], which="btn", indices=[(3,0)])
        del_cells(self, [G5_[4][0], G5_[4][1], G5_[4][2]], which="btn", indices=[(4,0)])
        show_subtitle(self, "不难看出，和刚才的叠加法一样，", "这次矩阵规模从 $N \\times N$ 变为了 $N$，因此复杂度就是 $N^3$ 。")
        self.wait(6)
        del_grids(self, G5_)

        show_title(self, "优化生成矩阵")

        show_subtitle(self, "在首行叠加法中，我们首先要得到第一按钮和最后一行灯关系矩阵，", "这个矩阵是需要推导生成的，并且不难看出其复杂度是 $N^3$ 。")
        self.wait(0.5)
        cols, rows = 5, 5
        sz = 0.25
        G5_ = [[None] * cols for _ in range(rows)]
        for k in range(rows):
            for y in range(cols):
                mx = (y*2-cols)*(1+sz)+1
                my = -k*sz+0.5
                G5_[k][y] = make_grid(self, w=cols, h=1, w_l=1, h_l=1, lgt_x=mx+sz*(cols+3)/2, btn_x=mx, lgt_y=my, btn_y=my, sz=sz, mat=[MAT5K[k][y][:]], mat_l=[[MAT5KL[k][y]]], show=True, rt=0.1)
        self.wait(2)

        show_subtitle(self, "我们将每一个灯都分开来推导，但实际上这些灯之间是有关联的。", "将矩阵重排后可以观察到，这些矩阵有着高度的对称性。")
        self.wait(0.5)
        for k in range(rows):
            for y in range(cols):
                if (k > y):
                    swap_grid(self, G5_[k][y], G5_[y][k])
        self.wait(5)

        show_subtitle(self, "仔细观察这些矩阵可以发现，", "每个格子的上下左右四个格子的状态数量恰好是偶数个。")
        self.wait(0.5)
        hl_cells(self, G5_[0], which="btn", indices=[(2,0)])
        hl_cells(self, G5_[1], which="btn", indices=[(1,0)])
        hl_cells(self, G5_[1], which="btn", indices=[(3,0)])
        hl_cells(self, G5_[2], which="btn", indices=[(2,0)])
        self.wait(6)
        del_cells(self, G5_[0], which="btn", indices=[(2,0)])
        del_cells(self, G5_[1], which="btn", indices=[(1,0)])
        del_cells(self, G5_[1], which="btn", indices=[(3,0)])
        del_cells(self, G5_[2], which="btn", indices=[(2,0)])

        show_subtitle(self, "由于最后一个矩阵才是我们需要的，", "因此我们只需要知道最后一个矩阵的第一行，就可以推得余下的。")
        self.wait(0.5)
        for k in range(rows):
            hl_bd(self, G5_[k][4], width=BD_W_SEL/2, buff=0.03)
        self.wait(4)
        show_subtitle(self, "因此，我们只需要推导第一个灯的状态，", "就可以得到所有灯的状态，从而减少复杂度。")
        self.wait(5)
        for k in range(rows):
            del_bd(self, G5_[k][4])
        del_grids(self, G5_)

        show_title(self, "解的数量")

        show_subtitle(self, "刚才我们发现，对于 $5 \\times 5$ 的格子，", "因为有两组静默操作，和前面的解共同构成了四种解法。")
        self.wait(0.5)
        cols, rows = 5, 5
        sz = 0.25
        G5_ = [[None] * cols for _ in range(rows)]
        for k in range(rows):
            for y in range(cols):
                mx = (y*2-cols)*(1+sz)+1
                my = -k*sz+0.5
                G5_[k][y] = make_grid(self, w=cols, h=1, w_l=1, h_l=1, lgt_x=mx+sz*(cols+3)/2, btn_x=mx, lgt_y=my, btn_y=my, sz=sz, mat=[MAT5K[k][y][:]], mat_l=[[MAT5KL[k][y]]], show=True, rt=0.1)
        del_grids(self, G5_[:-1])
        for y in range(cols):
            mx = -sz*2
            my = -(y-(cols-1)/2)*sz*2
            move_grid(self, G5_[rows-1][y], lgt_x=mx+sz*2*(cols+3)/2, btn_x=mx, lgt_y=my, btn_y=my, sz=sz*2, rt=0.3)
        gauss_grids(self, G5_, OPS5K[0], rt=0.3)
        gauss_grids(self, G5_, OPS5K[1], rt=0.3)
        hl_bd(self, G5_[4][3])
        hl_bd(self, G5_[4][4])
        self.wait(3)
        del_bd(self, G5_[4][3])
        del_bd(self, G5_[4][4])
        del_grids(self, G5_)


        show_subtitle(self, "而对于 $3 \\times 3$ 的格子来说，", "由于没有静默操作，因此解法是唯一的。")
        self.wait(0.5)
        cols, rows = 3, 3
        sz = 0.45
        G3_ = [[None] * cols for _ in range(rows)]
        for k in range(rows):
            for y in range(cols):
                mx = (y*2-cols)*(1+sz)+1
                my = -k*sz+0.5
                G3_[k][y] = make_grid(self, w=cols, h=1, w_l=1, h_l=1, lgt_x=mx+sz*(cols+3)/2, btn_x=mx, lgt_y=my, btn_y=my, sz=sz, mat=[MAT3K[k][y][:]], mat_l=[[MAT3KL[k][y]]], show=True, rt=0.1)
        del_grids(self, G3_[:-1])
        for y in range(cols):
            mx = -sz*2
            my = -(y-(cols-1)/2)*sz*2
            move_grid(self, G3_[rows-1][y], lgt_x=mx+sz*2*(cols+3)/2, btn_x=mx, lgt_y=my, btn_y=my, sz=sz*2, rt=0.3)
        gauss_grids(self, G3_, OPS3K[0], rt=0.3)
        gauss_grids(self, G3_, OPS3K[1], rt=0.3)
        hl_bd(self, G3_[2][0])
        hl_bd(self, G3_[2][1])
        hl_bd(self, G3_[2][2])
        self.wait(3)
        del_bd(self, G3_[2][0])
        del_bd(self, G3_[2][1])
        del_bd(self, G3_[2][2])
        del_grids(self, G3_)

        show_subtitle(self, "那么，对于 $N \\times N$ 的格子来说，最多可能有多少组静默操作呢？", "现在，我们观察 $4 \\times 4$ 的格子，并用首行叠加法求解。")
        self.wait(0.5)
        cols, rows = 4, 4
        sz = 0.3
        G4_ = [[None] * cols for _ in range(rows)]
        for k in range(rows):
            for y in range(cols):
                mx = (y*2-cols)*(1+sz)+1
                my = -k*sz+0.5
                G4_[k][y] = make_grid(self, w=cols, h=1, w_l=1, h_l=1, lgt_x=mx+sz*(cols+3)/2, btn_x=mx, lgt_y=my, btn_y=my, sz=sz, mat=[MAT4K[k][y][:]], mat_l=[[MAT4KL[k][y]]], show=True, rt=0.1)
        del_grids(self, G4_[:-1])
        for y in range(cols):
            mx = -sz*2
            my = -(y-(cols-1)/2)*sz*2
            move_grid(self, G4_[rows-1][y], lgt_x=mx+sz*2*(cols+3)/2, btn_x=mx, lgt_y=my, btn_y=my, sz=sz*2, rt=0.3)
        gauss_grids(self, G4_, OPS4K[0])
        gauss_grids(self, G4_, OPS4K[1])
        self.wait(3)
        show_subtitle(self, "这次我们意外的发现，所有的按钮都被抵消了，我们得到了一个零矩阵", "也就是说， $4 \\times 4$ 的格子有四组独立的静默操作，叠加后就是16种。")
        hl_bd(self, G4_[3][0])
        hl_bd(self, G4_[3][1])
        hl_bd(self, G4_[3][2])
        hl_bd(self, G4_[3][3])
        self.wait(5)
        del_bd(self, G4_[3][0])
        del_bd(self, G4_[3][1])
        del_bd(self, G4_[3][2])
        del_bd(self, G4_[3][3])
        del_grids(self, G4_)

        show_subtitle(self, "由于第一行按钮的状态只有16种，因此所有16种都是静默操作。", "这里，任意一种第一行按钮的状态，都能通过后三行消除所有灯。")
        self.wait(0.5)
        cols, rows = 4, 4
        sz, gap = 0.2, 0.8
        MAT_btn = []
        MAT_lgt = []
        sol_idx = []
        for i in range(16):
            mb, ml = build_case(i, w=4, h=4, l=0)
            MAT_btn.append(mb)
            MAT_lgt.append(ml)
            if all(ml[3][c] == 1 for c in range(4)):
                sol_idx.append(i)
        G = [[None] * cols for _ in range(rows)]
        for idx in range(16):
            x = idx % cols
            y = idx // cols
            mx = -(cols - 1) * (2 * sz + gap) / 2 + x * (2 * sz + gap)
            my = (rows - 1) * (2 * sz + gap) / 2 - y * (2 * sz + gap)
            G[y][x] = make_grid(self, w=4, h=4, lgt_x=mx, btn_x=mx, lgt_y=my, btn_y=my, sz=sz, rt=0.01, mat=slice_mat(MAT_btn[idx],0,0))
        for idx in range(16):
            x = idx % cols
            y = idx // cols
            apply_mat(self, G[y][x], slice_mat(MAT_btn[idx], 1, rows-1), anim=0.1, clear_end=True)
        self.wait(4)
        for idx in range(16):
            x = idx % cols
            y = idx // cols
            del_bd(self, G[y][x], rt=0.01)
        del_grids(self, G)

        show_subtitle(self, "同时，16种静默操作也对应着16种解法。", "这里，同样从任意一种第一行的状态，我们也能通过后面三行点亮所有灯。")
        self.wait(0.5)
        cols, rows = 4, 4
        sz, gap = 0.2, 0.8
        MAT_btn = []
        MAT_lgt = []
        sol_idx = []
        for i in range(16):
            mb, ml = build_case(i, w=4, h=4, l=1)
            MAT_btn.append(mb)
            MAT_lgt.append(ml)
            if all(ml[3][c] == 1 for c in range(4)):
                sol_idx.append(i)
        G = [[None] * cols for _ in range(rows)]
        for idx in range(16):
            x = idx % cols
            y = idx // cols
            mx = -(cols - 1) * (2 * sz + gap) / 2 + x * (2 * sz + gap)
            my = (rows - 1) * (2 * sz + gap) / 2 - y * (2 * sz + gap)
            G[y][x] = make_grid(self, w=4, h=4, lgt_x=mx, btn_x=mx, lgt_y=my, btn_y=my, sz=sz, rt=0.01, mat=slice_mat(MAT_btn[idx],0,0))
        for idx in range(16):
            x = idx % cols
            y = idx // cols
            apply_mat(self, G[y][x], slice_mat(MAT_btn[idx], 1, rows-1), anim=0.1, clear_end=True)
        show_subtitle(self, "因为 $N \\times N$ 格子第一行最多有 $2^N$ 种状态，", "因此$N \\times N$ 格子的解法最多为 $2^N$ 种。")
        self.wait(4)
        for idx in range(16):
            x = idx % cols
            y = idx // cols
            del_bd(self, G[y][x], rt=0.01)
        del_grids(self, G)

        show_subtitle(self, "这里列出了 $N=1$ 到 $N=16$ 的情况。", "这个序列被OEIS收录到了：https://oeis.org/A075462。")
        self.wait(0.5)
#演示N=1-16的矩阵E'
        self.wait(4)

        show_subtitle(self, "关于这个矩阵的秩，可以使用上述公式进行计算。")
        self.wait(0.5)
        show_center_latex(self, latex_blocks=LATEX1)
        self.wait(10)
        remove_center_latex(self)

        """



        G_a = make_grid(self, w=5, h=5, lgt_x=-4, btn_x=-2, sz=0.4, mat=MAT51)
        G_b = make_grid(self, w=5, h=5, lgt_x=+2, btn_x=+4, sz=0.4, mat=MAT52)
        self.wait(2)
        add_grid(self, G_b, G_a, rt=3)
        apply_mat(self, G_b, MAT51, anim=0.1, clear_end=True)
        self.wait(2)
        press(self, G_a, 1, 2, wait=0)
        press(self, G_b, 1, 2, wait=0)
        self.wait(2)
        del_grids(self, G_a)
        del_grids(self, G_b)
        self.wait(2)

        G_a = make_grid(self, w=5, h=5, lgt_x=-4, btn_x=-2, sz=0.4, mat=MAT51, show=False)
        G_b = make_grid(self, w=5, h=5, lgt_x=+2, btn_x=+4, sz=0.4, mat=MAT52)
        self.wait(2)
        trans_grid(self, G_b, G_a, rt=3)
        press(self, G_a, 1, 2, wait=0)
        press(self, G_b, 1, 2, wait=0)
        self.wait(2)
        del_grids(self, G_a)
        del_grids(self, G_b)


        G_a = make_grid(self, w=5, h=5, lgt_x=-4, btn_x=-2, sz=0.4, mat=MAT51)
        G_b = make_grid(self, w=5, h=5, lgt_x=+2, btn_x=+4, sz=0.4, mat=MAT52)
        self.wait(2)
        swap_grid(self, G_a, G_b)
        self.wait(2)
        add_grid(self, G_a, G_b)
        self.wait(2)
        del_grids(self, G_a)
        del_grids(self, G_b)
        self.wait(2)
        

        """
