# 点灯游戏（Lights Out）求解器 · 算法说明
# Lights Out Solver · Algorithm Notes

> 语言 / Language: [中文](#中文版本) | [English](#english-version)

---

## 中文版本

> 以**线性代数视角**系统梳理点灯游戏的四类算法路线，重点介绍**首行方程法（O(n^3))**与可扩展性。

### 目录
- 问题与规则
- 术语与记号
- 算法总览（对比表）
- 四种算法的要点
  - 1) 完全穷举 · O(2^(n^2))
  - 2) 首行穷举 · O(2^n)
  - 3) 完全方程 · O(n^6)
  - 4) 首行方程（推荐）· O(n^3)
- 数学建模与可解性
- 非全暗初始态的处理
- 变体与扩展
- 验证与测试建议
- 性能与工程化建议（算法层面）
- 常见问答
- 参考资料
- 许可

---

### 问题与规则
- 棋盘：`n × n`。
- 操作：按下某格按钮会切换**自身 + 上下左右**五盏灯的亮灭（边界处按实际存在的邻居）。
- 目标：给定初始状态（默认**全暗**），通过一组按钮使**所有灯全亮**。
- 基本性质：
  1. 同一按钮按**偶数次 ≡ 未按**；
  2. 按键**顺序无关**；
  3. 因而每个按钮仅需考虑二元状态（按/不按）。

---

### 术语与记号
- 亮/暗：`1/0`；按/不按：`1/0`；所有运算在 **GF(2)** 上（即**异或**）。
- 记 `x ∈ {0,1}^{n^2}` 为按钮向量；`y ∈ {0,1}^{n^2}` 为“目标翻转”向量（全亮且初始全暗时 `y=1`）。
- 线性系统：`A · x = y (mod 2)`。其中 `A` 为 `n^2 × n^2` 的 0-1 矩阵，描述“按某处会翻转哪些灯”。

---

### 算法总览（对比表）

| 方法 | 核心思路 | 时间复杂度 | 空间复杂度 | 规模适配 | 备注 |
|---|---|---:|---:|---:|---|
| 完全穷举 | 穷举 `n^2` 个按钮的 0/1 组合 | `O(2^(n^2))` | `O(1)` | 极小 | 仅教学/验证 |
| 首行穷举 | 穷举**首行**按钮，逐行“压灯” | `O(2^n)` | `O(n^2)` | 小~中 | 经典直观 |
| 完全方程 | 在 `n^2×n^2` 上做 GF(2) 消元/求逆 | `O(n^6)` | `O(n^4)` | 中 | 数学严谨但过重 |
| **首行方程** | 仅建立**首行→全局**线性关系并解 `n×n` | **`O(n^3)`** | **`O(n^2)`** | **中~大** | **推荐**路线 |

> 解的**存在性/唯一性**由矩阵**秩**决定：解空间大小 `= 2^(n^2 - rank(A))`。

---

### 四种算法的要点

#### 1) 完全穷举 · O(2^(n^2))
- 核心：遍历全部按钮布尔向量 `x`，模拟得到灯状态，检查是否全亮。
- 优点：零门槛、实现最简单。
- 缺点：指数爆炸，`n≥6` 即不可用。
- 适用：教学、小盘面验证。

#### 2) 首行穷举 · O(2^n)
- 核心：
  1. 枚举**首行**按钮状态；
  2. 由“上一行灯灭则需按下一行对应按钮”的**行递推**，确定 2..n 行按钮；
  3. 检查末行灯是否全亮。
- 要点：首行唯一决定全局；行递推遵循本地邻接规则。
- 优缺点：比完全穷举小了数量级，但仍为指数级；实现直观，常用于 `n ≤ 20` 的搜索/打表。

#### 3) 完全方程 · O(n^6)
- 核心：
  1. 直接写出 `n^2` 个方程，构造 `n^2×n^2` 的系数矩阵 `A`；
  2. 在 GF(2) 上高斯消元/求逆，解 `x`。
- 优点：一次性得到**所有**按钮的线性解；可分析**秩**、**解个数**。
- 缺点：矩阵维度过大（`n^2`），计算/内存成本陡增。
- 适用：中等盘面、数学分析、离线计算。

#### 4) 首行方程（推荐） · O(n^3)
- 核心思想：  
  - 只建模“**首行按钮向量 f** → **末行（或约束行）灯状态**”的线性映射：`T · f = y' (mod 2)`，其中 `T` 为 `n×n`。  
  - 解得 `f` 后，按首行穷举的**行递推**原理，线性地生成 2..n 行按钮解。
- 高层步骤（不涉具体代码）：
  1. 构造 `n×n` 转移矩阵 `T`：对单位基 `e_i` 递推到约束行，得到列向量；
  2. 求解 `T · f = y'`（GF(2) 消元/回代）得到首行 `f`；
  3. 由 `f` 行递推生成整盘按钮。
- 复杂度：构造 `T` `O(n^2~n^3)`；解 `T` `O(n^3)`；生成整盘 `O(n^2)`；总体约 `O(n^3)`。
- 优势：`n×n` 规模，兼具可扩展性与可解释性。

---

### 数学建模与可解性
- 线性系统：`A · x = y (mod 2)`；`A` 由邻接关系决定（自身+上下左右）。
- 秩与解数：若 `rank(A)=r`，解空间大小 `= 2^(n^2 - r)`；`r=n^2` 唯一解，`r<n^2` 多解。
- 对称性与可解性：标准点灯（对称邻接）下，系统**总可解**。
- 秩的规律：不同 `n` 的秩见 OEIS **A159257**。

---

### 非全暗初始态的处理
- 思想：把“已点亮”视作已被翻转一次。  
- 做法：将目标向量设为**目标 XOR 初始**：全亮目标 `1`、初始 `s`，则 `y = 1 XOR s`。四种算法均适用。

---

### 变体与扩展
- 矩形 `n×m`：结构与递推保持一致；完全方程为 `nm × nm`；首行方程可用“首行/首列方程”，维度降为 `n` 或 `m`。
- 不同邻接：含对角（Moore 邻域）、环面（torus）、加权翻转（GF(2) 仍为 0/1 权重）。满足对称性即可套用线性框架。
- 部分目标/约束：在 `y` 的对应位置设为 0/1（表示是否需要翻转）。

---

### 验证与测试建议
1. 线性性：任取两组解 `x₁, x₂`，验证 `x₁ XOR x₂` 的封闭性（同右端项或零空间平移）。  
2. 小盘面对拍：`n≤4` 完全穷举校验首行方程结果。  
3. 秩与解数：消元时统计秩，验证 `2^(n^2-rank)` 与实测解数一致。  
4. 末行约束：用单位基构造 `T` 时复测“单按影响”的正确性。  

---

### 性能与工程化建议（算法层面）
- GF(2) 专用技巧：位集（bitset）/机器字存储行，按位异或；行/块重排与部分选主元；块化 XOR 策略。  
- 并行化：行块化消元、前向/回代流水线；`T` 的列（或行）构造可并行。  
- 结构利用：`T` 近似带状/卷积式递推，探索多项式/卷积加速（快速异或卷积思想）。

---

### 常见问答
- 为什么“首行决定全局”？——每行灯仅受本行与相邻行按钮影响，递推把首行选择传导至整盘。  
- 解为何可能不唯一？——`rank(A)<n^2` 时存在零空间，特解与零空间任意向量异或仍为解。  
- 环面/对角邻接还能用吗？——能。按新邻接重建 `A`/`T` 即可。  
- 有“解个数”的闭式吗？——一般依赖具体 `n` 与边界条件的秩，参见文献与 OEIS 数据。

---

### 参考资料
- Lights Out Mathematics — 秩、解个数、边界/邻接规则  
  https://www.jaapsch.net/puzzles/lomath.htm  
- OEIS A159257 — Rank of the Lights Out matrix on an n×n board  
  https://oeis.org/A159257

---

## English Version

> A linear-algebra oriented overview of four algorithmic routes to solve **Lights Out**, with a focus on the **First-Row Linear System (O(n^3))** and its extensibility.

### Table of Contents
- Problem & Rules
- Notation
- Algorithm Overview (Comparison)
- The Four Methods
  - 1) Full Enumeration · O(2^(n^2))
  - 2) First-Row Enumeration · O(2^n)
  - 3) Full Linear System · O(n^6)
  - 4) First-Row Linear System (Recommended) · O(n^3)
- Modeling & Solvability
- Nonzero Initial States
- Variants & Extensions
- Verification & Testing
- Performance Notes (Algorithmic)
- FAQ
- References
- License

---

### Problem & Rules
- Board: `n × n`.
- Operation: pressing a cell toggles **itself + its four orthogonal neighbors** (existing neighbors only).
- Goal: given an initial state (default **all off**), find a set of presses to make **all lights on**.
- Invariants:
  1. Pressing the same button an **even** number of times ≡ **not pressed**;
  2. **Order** of presses does **not** matter;
  3. Each button is binary (press / not press).

---

### Notation
- On/Off as `1/0`; Press/No-press as `1/0`; all arithmetic over **GF(2)** (XOR).
- Let `x ∈ {0,1}^{n^2}` be the press vector; `y ∈ {0,1}^{n^2}` the target “to-flip” vector (`y=1` for all-on from all-off).
- Linear system: `A · x = y (mod 2)`, where `A` (`n^2 × n^2`) encodes toggle adjacency.

---

### Algorithm Overview (Comparison)

| Method | Core Idea | Time | Space | Scale | Note |
|---|---|---:|---:|---:|---|
| Full Enumeration | Enumerate all `n^2`-bit press vectors | `O(2^(n^2))` | `O(1)` | tiny | pedagogy only |
| First-Row Enumeration | Enumerate **first row**, then row-by-row propagation | `O(2^n)` | `O(n^2)` | small–mid | classic |
| Full Linear System | Solve on `n^2×n^2` matrix over GF(2) | `O(n^6)` | `O(n^4)` | mid | rigorous but heavy |
| **First-Row Linear System** | Build **first-row → constraint row** map (`n×n`) and solve | **`O(n^3)`** | **`O(n^2)`** | **mid–large** | **recommended** |

> Solvability & uniqueness depend on the **rank** of `A`: solution count `= 2^(n^2 - rank(A))`.

---

### The Four Methods

#### 1) Full Enumeration · O(2^(n^2))
- Traverse all `x`, simulate lights, check all-on.
- Pros: trivial to implement.
- Cons: exponential blow-up (`n≥6` impractical).
- Use: pedagogy / tiny boards.

#### 2) First-Row Enumeration · O(2^n)
- Enumerate the **first row**, then:
  1) if a light in row `r` is off, press the corresponding cell in row `r+1`;
  2) continue row-by-row; finally check the last row is all on.
- The first row determines the whole board.
- Still exponential in `n`, but practical for small `n` (e.g., `≤ 20`).

#### 3) Full Linear System · O(n^6)
- Write `n^2` equations (`n^2×n^2` matrix `A`), solve over GF(2) (Gaussian elimination / inverse).
- Pros: global linear view, rank & solution-space analysis.
- Cons: dimension `n^2` makes it heavy in time/space.

#### 4) First-Row Linear System (Recommended) · O(n^3)
- Idea: model the linear map from **first-row press vector `f`** to a **constraint row** (often the last row) of lights:  
  `T · f = y' (mod 2)`, with `T` being `n×n`.
- Steps (high-level):
  1. Build `T` by propagating each unit vector `e_i` down to the constraint row;
  2. Solve `T · f = y'` over GF(2) to obtain `f`;
  3. Generate the whole board by row propagation from `f`.
- Complexity: building `T` `O(n^2~n^3)`; solving `O(n^3)`; generation `O(n^2)`; overall ~ `O(n^3)`.
- Strength: scalable (`n×n`), mathematically interpretable (rank & nullspace).

---

### Modeling & Solvability
- System: `A · x = y (mod 2)`; `A` from adjacency (self + four neighbors).
- Rank & solution count: if `rank(A)=r`, then `#solutions = 2^(n^2 - r)`; unique iff `r=n^2`.
- Symmetry implies standard Lights Out is **always solvable**.
- Rank patterns across `n` are documented (see OEIS **A159257**).

---

### Nonzero Initial States
- Treat an already-on light as “already flipped once”.
- Set right-hand side to **target XOR initial**: for all-on target `1` and initial `s`, use `y = 1 XOR s`.
- All four methods remain applicable.

---

### Variants & Extensions
- Rectangular `n×m`: same structure; full system is `nm × nm`; first-row/first-column systems reduce to `n` or `m`.
- Alternative adjacencies: with diagonals (Moore), torus boundaries, or binary weights—still in GF(2).
- Partial targets/constraints: set corresponding entries in `y` to 0/1.

---

### Verification & Testing
1. Linearity: for two solutions `x₁, x₂` (same RHS), `x₁ XOR x₂` lies in the nullspace.  
2. Tiny-board cross-check: for `n≤4`, compare with full enumeration.  
3. Rank vs. solution count: verify `2^(n^2-rank)` against empirical counts.  
4. Constraint consistency: re-check single-press influence when building `T`.

---

### Performance Notes (Algorithmic)
- GF(2)-specific tricks: bitsets / word-wise XOR rows; partial pivoting (row swaps) in elimination; block-XOR strategies.  
- Parallelism: block elimination, pipelined forward/back substitution; parallel column/row construction of `T`.  
- Structural use: `T` is near-banded / convolutional—consider polynomial or (fast) XOR-convolution methods.

---

### FAQ
- Why does “the first row determine the whole board”?  
  Because each row only depends on itself and adjacent rows; propagation eliminates other degrees of freedom.
- Why can solutions be non-unique?  
  If `rank(A)<n^2`, the nullspace is nontrivial; any particular solution plus a nullspace vector is another solution.
- Do torus/diagonal adjacencies still fit?  
  Yes—rebuild `A`/`T` for the new adjacency; the GF(2) framework remains valid.
- Is there a closed form for the number of solutions?  
  Generally depends on `n` and boundary conditions (via rank); see literature/OEIS.

---

### References
- Lights Out Mathematics — ranks, solution counts, boundary/adjacency variants  
  https://www.jaapsch.net/puzzles/lomath.htm  
- OEIS A159257 — Rank of the Lights Out matrix on an n×n board  
  https://oeis.org/A159257
