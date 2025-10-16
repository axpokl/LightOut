from manimlib import *

LIGHT_BLUE = "#55aaff"
PINK = "#ff55aa"

MAT5 = [
    [1,1,0,0,0],
    [1,1,0,1,1],
    [0,0,1,1,1],
    [0,1,1,1,0],
    [0,1,1,0,1],
]

MAT7 = [
    [1,1,0,1,0,1,1],
    [1,1,1,0,1,1,1],
    [0,1,1,0,1,1,0],
    [1,0,0,1,0,0,1],
    [0,1,1,0,1,1,0],
    [1,1,1,0,1,1,1],
    [1,1,0,1,0,1,1],
]

MAT11 = [
    [1,0,0,0,1,0,0,0,0,0,0],
    [0,0,1,0,0,0,1,1,1,1,1],
    [0,0,0,0,0,0,1,0,0,0,1],
    [1,1,0,1,1,0,1,1,0,1,1],
    [1,1,1,1,1,1,0,1,1,1,0],
    [0,1,0,1,1,1,0,0,0,0,1],
    [1,1,0,0,1,0,0,0,0,1,0],
    [1,0,0,1,1,1,1,1,0,0,1],
    [1,1,0,1,1,0,0,1,0,1,0],
    [0,1,1,0,0,1,1,1,1,0,1],
    [1,0,1,1,1,1,0,1,1,0,0],
]

def mat_to_seq(mat):
    n = len(mat)
    seq = []
    for j in range(n):
        for i in range(n):
            if mat[j][i] == 1:
                seq.append((i, j))
    return seq

class LightsOutGrid(VGroup):
    def __init__(self, n=5, cell_size=0.6, **kwargs):
        super().__init__(**kwargs)
        self.n = n
        self.cell_size = cell_size
        self.squares = [[None]*n for _ in range(n)]
        self.circles = [[None]*n for _ in range(n)]
        g = VGroup()
        for j in range(n):
            row = VGroup()
            for i in range(n):
                sq = Square(side_length=cell_size)
                sq.set_stroke(WHITE, 2).set_fill(BLACK, opacity=1)
                row.add(sq)
                self.squares[j][i] = sq
            row.arrange(RIGHT, buff=0)
            g.add(row)
        g.arrange(DOWN, buff=0)
        self.add(g)
        self.state = [[0]*n for _ in range(n)]
        self.pressed = [[0]*n for _ in range(n)]

    def neighbors(self, i, j):
        yield (i, j)
        if i > 0: yield (i-1, j)
        if i < self.n-1: yield (i+1, j)
        if j > 0: yield (i, j-1)
        if j < self.n-1: yield (i, j+1)

    def press_anims(self, i, j, rt=0.25):
        anims = []
        for x, y in self.neighbors(i, j):
            self.state[y][x] ^= 1
            color = LIGHT_BLUE if self.state[y][x] else BLACK
            anims.append(ApplyMethod(self.squares[y][x].set_fill, color, 1, False))
            circ = self.circles[y][x]
            if circ is not None:
                circ.move_to(self.squares[y][x].get_center())
                def _restack(mobj, alpha):
                    if mobj in self.submobjects:
                        self.remove(mobj)
                    self.add(mobj)
                anims.append(UpdateFromAlphaFunc(circ, _restack))
        if not self.pressed[j][i]:
            c = Circle(radius=self.cell_size*0.22).set_fill(PINK, 1).set_stroke(PINK, 0)
            c.move_to(self.squares[j][i].get_center())
            self.circles[j][i] = c
            self.pressed[j][i] = 1
            anims.append(FadeIn(c, scale=0.5))
        else:
            self.pressed[j][i] = 0
            anims.append(FadeOut(self.circles[j][i], scale=0.5))
            self.circles[j][i] = None
        return AnimationGroup(*anims, lag_ratio=0, run_time=rt)

    def reset_anims(self, rt=0.25):
        anims = []
        for j in range(self.n):
            for i in range(self.n):
                self.state[j][i] = 0
                if self.circles[j][i]:
                    anims.append(FadeOut(self.circles[j][i], run_time=rt))
                    self.circles[j][i] = None
                self.pressed[j][i] = 0
                anims.append(ApplyMethod(self.squares[j][i].set_fill, BLACK, 1))
        return AnimationGroup(*anims, lag_ratio=0.01, run_time=rt)

class LightsOutThreeGridsGL(Scene):
    def construct(self):

        g5  = LightsOutGrid(n=5,  cell_size=0.6).shift(4.1*LEFT)
        g7  = LightsOutGrid(n=7,  cell_size=0.5)
        g11 = LightsOutGrid(n=11, cell_size=0.33).shift(4.1*RIGHT)

        t5  = Text("N=5", color=WHITE).next_to(g5,  UP, buff=0.3)
        t7  = Text("N=7", color=WHITE).next_to(g7,  UP, buff=0.3)
        t11 = Text("N=11", color=WHITE).next_to(g11, UP, buff=0.3)

        self.play(FadeIn(g5), FadeIn(g7), FadeIn(g11), FadeIn(t5), FadeIn(t7), FadeIn(t11))
        self.wait(0.2)

        seq5  = mat_to_seq(MAT5)
        seq7  = mat_to_seq(MAT7)
        seq11 = mat_to_seq(MAT11)

        for (i,j) in seq5:  self.play(g5.press_anims(i,j,0.3))
        for (i,j) in seq7:  self.play(g7.press_anims(i,j,0.2))
        for (i,j) in seq11: self.play(g11.press_anims(i,j,0.1))

        self.play(g5.reset_anims(0.3), g7.reset_anims(0.3), g11.reset_anims(0.3))
        self.wait(0.2)
