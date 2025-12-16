## 【Manim】《点灯游戏的数学解法》：www.bilibili.com/video/BV1XcxNz7EjF/

---

# 点灯游戏（Lights Out）求解器 · 算法说明

> Language: [English](#english-version)

---

## 中文版本

### 目录
- 问题与规则
- 关键观察（按两次抵消、顺序无关）
- 术语与记号（GF(2) 建模）
- 算法总览（对比表）
- 四类基础路线
  - 1) 完全穷举 · `O(2^(n^2))`
  - 2) 首行穷举 · `O(2^n)`
  - 3) 叠加法（全局高斯消元）· `O(n^6)`
  - 4) 首行叠加法 · `O(n^3)`
- 首行叠加法的关键递推（B/L/Y）
- 优化生成矩阵（十字偶校验约束）
- 解的数量（静默操作、最多 `2^n`）
- 首行求逆 + 反向消元（O(n^2)）
  - H：左右扩散矩阵
  - K/F：扩散基矩阵与解耦矩阵
  - p(H) 分解与系数求解
  - 可逆：逆多项式 q(x)
  - 不可逆：最大公因子 g(x)、D 矩阵与反向消元
- 可解性（自反 + 对称 ⇒ 必可解）
- 工程实现与验证建议
- 参考文献

---

### 问题与规则
- 棋盘：`n × n`。
- 操作：点击某格按钮，会翻转（亮↔暗）：
  - 自身
  - 上下左右四邻居（边界处只翻转存在的邻居）
- 目标（两种等价说法）：
  - 从**全暗**出发，使灯**全亮**
  - 或从**全亮**出发，使灯**全暗**
- 二值化与运算：
  - 按/不按：`1/0`
  - 亮/暗：`1/0`
  - 所有运算都在 **GF(2)**（即 XOR / 异或）上

---

### 关键观察（视频引言）
1. **同一按钮按两次等同于没按**  
   因为翻转两次回到原状态：`a ⊕ 1 ⊕ 1 = a`。
2. **按按钮的顺序无关**  
   因为 XOR 可交换且可结合：`(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)`。
3. 因而每个按钮只需考虑二元状态（按/不按），一组按钮状态唯一决定一组灯状态。

---

### 术语与记号（GF(2) 建模）
- 将棋盘拉直编号（仅用于矩阵表达）：
  - 按钮向量：`x ∈ {0,1}^{n^2}`
  - 灯向量：`l ∈ {0,1}^{n^2}`
- 存在 `n^2 × n^2` 的 0/1 矩阵 `A`，其第 `j` 列表示“只按第 `j` 个按钮”时会翻转哪些灯。
- 叠加性（视频“按多个按钮=操作叠加”）在 GF(2) 上对应线性系统：
  - `l = A · x (mod 2)`
- 目标全亮可写为：
  - `A · x = 1 (mod 2)`（`1` 为全 1 向量）

---

### 算法总览（对比表）

| 方法 | 核心思路（视频术语） | 规模 | 时间复杂度 | 空间复杂度 | 备注 |
|---|---|---:|---:|---:|---|
| 完全穷举 | 遍历所有 `n^2` 按钮的 0/1 组合 | `2^(n^2)` | `O(2^(n^2))` | `O(n^2)` | `n=6` 迅速爆炸 |
| 首行穷举 | 只穷举第 1 行，后续行按“压灯”唯一递推 | `2^n` | `O(2^n·n^2)` | `O(n^2)` | 从第 2 行起按法由上一行灯状态决定 |
| 叠加法（全局消元） | 对 `[E / A]` 做 GF(2) 高斯消元，求逆/伪逆/零空间 | `n^2×n^2` | `O(n^6)` | `O(n^4)` | 解释“静默操作=多解”最直观 |
| **首行叠加法** | 把末行灯表示成首行按钮线性组合 + 翻转向量，只解 `n×n` | `n×n` | **`O(n^3)`** | **`O(n^2)`** | 规模从 `n^2` 降为 `n` |
| **首行求逆+反向消元** | 多项式/扩散基/欧几里得 + 结构化回代 | n | **`O(n^2)`** | **`O(n)`** | 可逆直接求逆，不可逆用 `g` 与 `D` 反向消元 |

---

## 四类基础路线

### 1) 完全穷举 · `O(2^(n^2))`
- 枚举所有按钮向量 `x`（长度 `n^2`），计算 `l = A·x`，检查是否全亮。
- 视频示例：
  - `n=2`：`2^4=16`
  - `n=3`：`2^9=512`
  - `n=5`：`2^25=33,554,432`（需要计算机）
  - `n=6`：`2^36` 过大

---

### 2) 首行穷举 · `O(2^n)`
- 关键现象（视频“从上到下一行一行按”）：
  - 随机选择第 1 行按钮后，第 1 行灯状态确定；
  - 若第 1 行某灯为暗，为避免破坏已处理结果，只能按第 2 行对应列按钮去修正；
  - 从第 2 行开始，每行按钮状态都被上一行灯状态**唯一决定**；
  - 最后检查末行是否全亮，若是即得到一种解。
- 复杂度：
  - 首行有 `2^n` 种；
  - 每种首行递推整盘 `O(n^2)`；
  - 总体 `O(2^n·n^2)`。

---

### 3) 叠加法（全局高斯消元）· `O(n^6)`
- 视频中的“把每个按钮单按一次得到一组灯状态，再通过叠加消去，构造单开灯操作”本质是：
  - 将操作写成增广矩阵 `[E | A]`（左边记录按钮组合，右边记录灯翻转效果）
  - 用 GF(2) 高斯消元（行交换、行异或）把 `A` 消成单位矩阵（可逆时）
  - 左边同步变换得到 `A^{-1}`，从而可把任意目标灯向量映射回按钮向量
- 静默操作（视频重点）：
  - 消元过程中可能出现某些操作“没有翻转任何灯”，即 `A·x = 0`；
  - 这些 `x` 构成零空间（静默空间），其维度决定解的数量：
    - 有 `r'` 个独立静默操作 ⇒ 解有 `2^{r'}` 个
- 复杂度为何是 `O(n^6)`：
  - 矩阵维度是 `n^2`，消元为立方：`(n^2)^3 = n^6`。

---

### 4) 首行叠加法（O(n³)）
> 将“首行穷举的递推”与“叠加消元”结合：把最后一行灯写成“首行按钮的线性组合 + 翻转向量”，于是只需求解 `n×n` 系统。

---

## 首行叠加法的关键递推（B/L/Y）

### 记号（按视频）
- `B(n,x)`：第 `n` 行、第 `x` 列按钮（0/1）
- `L(n,x)`：第 `n` 行、第 `x` 列灯（0/1）
- `⊕`：叠加（XOR）
- `~`：翻转（NOT），在 GF(2) 中 `~a = a ⊕ 1`

### 基本关系（视频推导）
1. 灯可由“上左中右按钮”叠加表示（将“下按钮”留到下一步）：
   - `L(n,x)=B(n-1,x-1)⊕B(n,x-1)⊕B(n,x)⊕B(n,x+1)`
2. 为点亮（或消暗）当前灯，下一行按钮取为当前灯翻转：
   - `B(n+1,x)=~L(n,x)`
3. 使用 `~(a⊕b)=a⊕~(b)`（本质是 `~t=t⊕1`）把“每步必然翻转”抽成翻转向量 `Y`。

### 二阶递推（视频最终公式）
- 按钮递推：
  - `B(n,x)=B(n-1,x-1)⊕B(n-1,x)⊕B(n-1,x+1)⊕B(n-2,x)`
- 灯递推（形式相同）：
  - `L(n,x)=L(n-1,x-1)⊕L(n-1,x)⊕L(n-1,x+1)⊕L(n-2,x)`
- 翻转向量递推（必须保留 `~`）：
  - `Y(n,y)=~(Y(n-1,y-1)⊕Y(n-1,y)⊕Y(n-1,y+1)⊕Y(n-2,y))`

---

## 将末行灯表示为首行按钮的线性系统（O(n³) 的核心）

1. 令首行按钮向量为 `X`（长度 `n`）。
2. 通过上面的递推，把“末行灯”写成：
   - `L_last = M·X ⊕ Y_last`
   - 其中 `M` 为 `n×n` 矩阵，表示“首行按钮 → 末行灯”的线性映射；
   - `Y_last` 为递推抽出的翻转向量（长度 `n`）。
3. 目标全亮（或给定目标向量 `T`）：
   - `M·X = T ⊕ Y_last`
4. 在 GF(2) 上对 `n×n` 系统消元求 `X`，再用“压灯递推”生成整盘按钮。

---

## 优化生成矩阵（十字偶校验约束）

### 十字偶校验约束（视频定义）
对任意相关矩阵（按钮/灯映射矩阵）均满足：
- `B(x-1,y)⊕B(x+1,y)⊕B(x,y-1)⊕B(x,y+1)=0`

### 直接收益（视频结论）
- 只要知道矩阵的**第一行**，就能递推出其余各行：
  - `B(x,y)=B(x-1,y-1)⊕B(x-1,y+1)⊕B(x-2,y)`
- 因此生成 `M` 时不必为每个列/每个灯生成完整矩阵：
  - 先求关键的第一行
  - 再用递推补全
- 这也是后续 `O(n^2)` 算法里“尽量只操作第一行”的同源优化思想。

---

## 解的数量（静默操作、最多 `2^n`）

- 静默操作：满足 `A·x=0` 的按钮图案（翻转 0 盏灯）。
- 静默空间维度为 `r'` 时：
  - 解的数量 `=2^{r'}`
- 视频示例：
  - `3×3`：无静默 ⇒ 唯一解
  - `5×5`：`r'=2` ⇒ `4` 种解
  - `4×4`：首行空间全静默 ⇒ `2^4=16` 种解
- 上界（视频结论）：
  - `n×n` 解最多为 `2^n`（静默自由度最多 n）
  - 对应 OEIS：A075462

---

## 首行求逆 + 反向消元（O(n²)）

> 目标：求解首行系统 `B X = Y`（GF(2)），其中只需要 `B` 的第一行 `b` 与 `Y`。

---

### 1) H：左右扩散矩阵
- 定义：
  - `H(y,x)=1` 当且仅当 `|x-y|=1`
- 作用（视频解释）：
  - 向量乘 `H` 等价于左右扩散叠加：
  - `v*H` 的第 `x` 位为 `v(x-1)⊕v(x+1)`

---

### 2) K：扩散基矩阵（Krylov）
- 定义：
  - `K(n)=H^n(0)`
- 递推：
  - `K(n,x)=K(n-1,x-1)⊕K(n-1,x+1)`

---

### 3) F：K 的逆（解耦矩阵）
- 定义：
  - `F=K^{-1}`
- 递推性质（视频给出）：
  - `F(y,x)=F(y-1,x-1)⊕F(y-2,x)`

---

### 4) 把 B 表示为多项式 `p(H)` 并求系数 `p`
- 视频给出的 B 递推：
  - `B(n)=B(n-1)*H⊕B(n-1)⊕B(n-2)`
- 用多项式表达：
  - `B = p(H) = p0*H^0 ⊕ p1*H^1 ⊕ p2*H^2 ⊕ ...`
- 只关心第一行 `b`，并用 `K` 表示 `H^k(0)`：
  - `b = p*K`
- 两边乘 `F=K^{-1}`：
  - `p = b*F`

---

### 5) 可逆情况：求逆多项式 `q(x)`，直接 `X=q(H)*Y`
- 若存在 `q(x)` 使得：
  - `q(x)p(x)=1 mod f(x)`（视频里的 `f(n,x)`）
- 则：
  - `X = q(H)*Y`
- 计算 `q(H)*Y`（视频方式）：
  - 从 `Y` 开始不断做 `*H`（左右扩散）得到 `H^k*Y`
  - 若 `qk=1` 则叠加进结果
  - 共 `n` 次扩散、每次 `O(n)` ⇒ `O(n^2)`

---

### 6) 不可逆情况：`g(x)≠1` ⇒ 反向消元法
- 欧几里得法得到 `q'(x)` 满足：
  - `q'(x)p(x)=g(x) mod f(x)`
- 定义：
  - `r' = deg(g)`，且 `r'=n-r`
- 定义部分解：
  - `z = q'(H)*y`
- 得到关键方程：
  - `z = g(H)*x`

---

### 7) 构造 D 并用其解 `z = D*x`
- 令 `D = g(H)`（矩阵形式），则：
  - `z = D*x`
- 视频给出的构造要点：
  - 乘 `H` 的扩散过程对应 `K`
  - 可用 `d=K*g` 得到关键行，再用十字偶校验约束递推补全 `D`

#### D 的性质（视频列举，r'=deg(g)）
1. 后 `r=n-r'` 行呈带状上三角结构：左侧一段为 0。
2. 后 `r` 行在 `i=j-r'` 处存在主元 1。
3. 后 `r` 行线性无关。
4. 前 `r'` 行都可由后 `r` 行线性叠加得到。

#### 反向消元求特解（视频逻辑）
- 只用后 `r` 行消元。
- 从左到右依次消去 `z[i]`：
  - 若 `z[i]=1`，唯一需要叠加的行是 `j=i+r'`（因为只有该行在第 `i` 列有主元 1）
  - 叠加后 `z[i]` 被消去，同时在 `x[i]` 记 1
- 得到一个特解 `x`。

#### 得到全部 `2^{r'}` 个解
- 前 `r'` 行可由后 `r` 行叠加 ⇒ 在求解前可任意叠加前 `r'` 行改变 `z`
- 共有 `2^{r'}` 种组合 ⇒ 产生 `2^{r'}` 个解

#### 对称性补充（视频）
- `D` 满足高度对称：`D[j,i]=D[i,j]`
- 因而也可从右往左做等价消元（略）

---

## 可解性（自反 + 对称 ⇒ 必可解）

### 条件（视频结论）
点灯游戏只要满足：
1. 自反性：按钮 `a` 会翻转灯 `a`
2. 对称性：若 `a` 翻 `b`，则 `b` 也翻 `a`

则游戏**一定存在解**，并可推广到任意空间布局与形状，不局限于方阵。

### 视频提供的两类证明思路（摘要）
- 归纳构造：去掉一个按钮得到可解子游戏，叠加多组解构造原游戏解；不同奇偶情况下加上能翻奇数个灯的操作做修正。
- 图论反证：把游戏看作带自环无向图，使用“去点可解 ⇒ 得到 P_i ⇒ 全叠加”的矛盾链条，并结合握手引理推出不可解例不存在。

---

## 工程实现与验证建议

### 实现建议
1. 统一 GF(2) 运算：行操作只用交换、XOR。
2. 边界越界按 0 处理（无邻居视为不存在）。
3. 优先使用“只算第一行 + 十字偶校验补全”的生成方式。
4. 性能优先：bitset/机器字行存储，整行 XOR。

### 验证建议
1. 小规模对拍：`n≤4` 用完全穷举验证首行叠加/反向消元结果。
2. 静默维度检验：统计 `r'`，验证解数是否为 `2^{r'}`。
3. 线性性检验：任取两解 `x1,x2`，检查 `A·(x1⊕x2)=0`（差解应落在静默空间）。

---

## 参考文献

[1] Jaap Scherphuis，《点灯问题游戏的数学原理》  
https://www.jaapsch.net/puzzles/lomath.htm

[2] Granvallen，《点灯游戏与数学之美》  
https://granvallen.github.io/lightoutgame/

[3] axpokl，《点灯游戏 Flip Game 的 O(n³) 求解算法》  
https://zhuanlan.zhihu.com/p/53646257

[4] Chao Xu，《逼零集、点灯游戏与线性方程组》  
https://zhuanlan.zhihu.com/p/553780037

[5] GitHub — axpokl，《Pascal 实现的标准点灯问题 O(n³) 求解程序》  
https://github.com/axpokl/LightOut

[6] GitHub — njpipeorgan，《大规模点灯问题求解器及解法说明》  
https://github.com/njpipeorgan/LightsOut

[7] OEIS，《n×n 全亮点灯问题的解数》  
https://oeis.org/A075462

[8] OEIS，《n×n 点灯问题的秩缺陷》  
https://oeis.org/A159257

---

# Lights Out Solver · Algorithm Notes

> Language: [中文](#中文版本)

---

## English version

### Table of contents
- Problem and rules
- Key observations (press twice cancels, order does not matter)
- Terms and notation (GF(2) model)
- Overview table (comparison)
- Four basic routes
  - 1) Full brute force · `O(2^(n^2))`
  - 2) First-row brute force · `O(2^n)`
  - 3) Superposition method (global Gaussian elimination) · `O(n^6)`
  - 4) First-row superposition · `O(n^3)`
- Key recurrences in first-row superposition (B/L/Y)
- Optimized matrix generation (cross even-parity constraint)
- Number of solutions (silent patterns, at most `2^n`)
- First-row inversion + reverse elimination (O(n²))
  - H: left-right diffusion matrix
  - K/F: diffusion basis matrix and decoupling matrix
  - Decompose B as `p(H)` and solve coefficients `p`
  - Invertible case: inverse polynomial `q(x)`
  - Non-invertible case: gcd `g(x)`, D matrix, reverse elimination
- Solvability (reflexive + symmetric ⇒ always solvable)
- Engineering tips and validation
- References

---

### Problem and rules
- Board: `n × n`.
- Operation: pressing a cell toggles (on↔off):
  - itself
  - its 4-neighbors (up/down/left/right, only those that exist on the boundary)
- Goal (two equivalent statements):
  - start from **all-off** and make **all-on**
  - or start from **all-on** and make **all-off**
- Binary states and operations:
  - press / not press: `1/0`
  - light on / off: `1/0`
  - all computations are in **GF(2)** (XOR)

---

### Key observations (video intro)
1. **Pressing the same button twice is the same as not pressing it**  
   because toggling twice returns to the original state: `a ⊕ 1 ⊕ 1 = a`.
2. **The order of presses does not matter**  
   because XOR is commutative and associative: `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)`.
3. Therefore each button only needs a binary choice (press or not), and one press pattern uniquely determines one final light state.

---

### Terms and notation (GF(2) model)
- Flatten the board into a 1D index (only for matrix expressions):
  - press vector: `x ∈ {0,1}^{n^2}`
  - light vector: `l ∈ {0,1}^{n^2}`
- There exists a `0/1` matrix `A` of size `n^2 × n^2`:
  - column `j` describes which lights are toggled when **only** button `j` is pressed
- The video’s “press multiple buttons = superpose operations” is exactly GF(2) linearity:
  - `l = A · x (mod 2)`
- The all-on target can be written as:
  - `A · x = 1 (mod 2)` where `1` is the all-ones vector

---

### Overview table (comparison)

| Method | Core idea (video phrasing) | Scale | Time complexity | Space | Notes |
|---|---|---:|---:|---:|---|
| Full brute force | Enumerate all `n^2` button 0/1 patterns | `2^(n^2)` | `O(2^(n^2))` | `O(n^2)` | explodes fast (`n=6` is huge) |
| First-row brute force | Enumerate only row 1; later rows are forced by “press-down” recursion | `2^n` | `O(2^n·n^2)` | `O(n^2)` | from row 2 onward the presses are uniquely determined |
| Superposition (global elimination) | Do GF(2) Gaussian elimination on `[E / A]`, get inverse / pseudoinverse / nullspace | `n^2×n^2` | `O(n^6)` | `O(n^4)` | makes “silent patterns = multiple solutions” very visible |
| **First-row superposition** | Express last-row lights as linear combo of first-row presses + flip vector; solve `n×n` | `n×n` | **`O(n^3)`** | **`O(n^2)`** | reduces size from `n^2` to `n` |
| **First-row inversion + reverse elimination** | Use polynomials/diffusion basis/Euclid + structured back-substitution | n | **`O(n^2)`** | **`O(n)`** | invertible: direct; non-invertible: use `g` and `D` |

---

## Four basic routes

### 1) Full brute force · `O(2^(n^2))`
- Enumerate all press vectors `x` (length `n^2`), compute `l = A·x`, and check whether `l` is all-on.
- Video examples:
  - `n=2`: `2^4=16`
  - `n=3`: `2^9=512`
  - `n=5`: `2^25=33,554,432` (needs a computer)
  - `n=6`: `2^36` is too large

---

### 2) First-row brute force · `O(2^n)`
- Key phenomenon (video: “go row by row from top to bottom”):
  - Choose the first-row presses arbitrarily; then row 1 lights are determined.
  - If a light in row 1 is off, to fix it without disturbing completed work, you must press the button directly below it (in row 2).
  - From row 2 onward, each row’s presses are **uniquely determined** by the previous row’s light state.
  - Finally check if the last row is all-on; if yes you found a solution.
- Complexity:
  - `2^n` choices for the first row
  - per choice: propagate over the whole board `O(n^2)`
  - total: `O(2^n·n^2)`

---

### 3) Superposition method (global Gaussian elimination) · `O(n^6)`
> The video’s “turn 9 single-button operations into 9 single-light operations” is exactly eliminating a matrix to the identity.

- Matrix setup (video “button matrix + light matrix”):
  - Build the augmented matrix `[E | A]`:
    - left block `E`: tracks how operations (button combinations) are formed
    - right block `A`: the corresponding light toggles
  - Perform GF(2) Gaussian elimination (row swap, row XOR)
  - If `A` is invertible and you reduce `A` to `I`, then the left block becomes `A^{-1}`.
- Silent patterns (video highlight):
  - During elimination you can get operations that toggle **no** lights: `A·x = 0`.
  - These are “silent patterns” (nullspace vectors).
  - If there are `r'` independent silent patterns, then the solution count is `2^{r'}`.
- Why `O(n^6)`:
  - dimension is `n^2`, elimination is cubic: `(n^2)^3 = n^6`

---

### 4) First-row superposition · `O(n^3)`
> Combine first-row propagation with superposition: express the last-row lights as a linear function of only the first-row presses, then solve an `n×n` GF(2) system.

---

## Key recurrences in first-row superposition (B/L/Y)

### Notation (as in the video)
- `B(n,x)`: the button (press) at row `n`, column `x` (0/1)
- `L(n,x)`: the light at row `n`, column `x` (0/1)
- `⊕`: XOR (superposition)
- `~`: NOT; in GF(2), `~a = a ⊕ 1`

### Base relations (video derivation)
1. A light can be expressed using the “up-left / left / self / right” buttons (the “down” button is handled by the next step):
   - `L(n,x)=B(n-1,x-1)⊕B(n,x-1)⊕B(n,x)⊕B(n,x+1)`
2. To fix the current row, the next-row press equals the flip of the current light:
   - `B(n+1,x)=~L(n,x)`
3. Use `~(a⊕b)=a⊕~(b)` (equivalently `~t=t⊕1`) to separate the forced flips into a flip vector `Y`.

### Second-order recurrences (final video formulas)
- Button recurrence:
  - `B(n,x)=B(n-1,x-1)⊕B(n-1,x)⊕B(n-1,x+1)⊕B(n-2,x)`
- Light recurrence (same form):
  - `L(n,x)=L(n-1,x-1)⊕L(n-1,x)⊕L(n-1,x+1)⊕L(n-2,x)`
- Flip-vector recurrence (must keep `~`):
  - `Y(n,y)=~(Y(n-1,y-1)⊕Y(n-1,y)⊕Y(n-1,y+1)⊕Y(n-2,y))`

---

## Express the last row as a linear system in the first row

1. Let the first-row press vector be `X` (length `n`).
2. Using the recurrences, express the last-row lights as:
   - `L_last = M·X ⊕ Y_last`
   - `M` is an `n×n` matrix mapping “first-row presses → last-row lights”
   - `Y_last` is the extracted flip vector (length `n`)
3. For the all-on target (or a target vector `T`):
   - `M·X = T ⊕ Y_last`
4. Solve this `n×n` GF(2) system by elimination to get `X`, then generate the full board using the standard row-by-row propagation.

---

## Optimized matrix generation (cross even-parity constraint)

### Cross even-parity constraint (video definition)
For every related matrix (button/light mapping matrices), the following holds:
- `B(x-1,y)⊕B(x+1,y)⊕B(x,y-1)⊕B(x,y+1)=0`

### Benefit (video conclusion)
- Knowing **only the first row** is enough to reconstruct the rest:
  - `B(x,y)=B(x-1,y-1)⊕B(x-1,y+1)⊕B(x-2,y)`
- So when building `M`, do not generate full matrices for every column:
  - compute the key first row
  - fill the remaining rows by recurrence
- This matches the later `O(n^2)` philosophy: “operate on first rows as much as possible”.

---

## Number of solutions (silent patterns, at most `2^n`)

- Silent pattern: any press pattern `x` such that `A·x=0` (toggles zero lights).
- If the silent-space dimension is `r'`, then:
  - number of solutions `=2^{r'}`
- Video examples:
  - `3×3`: no silent patterns ⇒ unique solution
  - `5×5`: `r'=2` ⇒ 4 solutions
  - `4×4`: the entire first-row space is silent ⇒ `2^4=16` solutions
- Upper bound (video claim):
  - at most `2^n` solutions on an `n×n` board
  - referenced as OEIS A075462

---

## First-row inversion + reverse elimination (O(n²))

> Goal: solve the first-row system `B X = Y` in GF(2), where only the first row `b` of `B` and the vector `Y` are needed.

---

### 1) H: left-right diffusion matrix
- Definition:
  - `H(y,x)=1` iff `|x-y|=1`
- Action (video meaning):
  - multiplying a vector by `H` diffuses it left and right and XORs:
  - the `x`-th entry of `v*H` is `v(x-1)⊕v(x+1)`

---

### 2) K: diffusion basis matrix (Krylov)
- Definition:
  - `K(n)=H^n(0)`
- Recurrence:
  - `K(n,x)=K(n-1,x-1)⊕K(n-1,x+1)`

---

### 3) F: inverse of K (decoupling matrix)
- Definition:
  - `F=K^{-1}`
- Recurrence property (video):
  - `F(y,x)=F(y-1,x-1)⊕F(y-2,x)`

---

### 4) Decompose B as a polynomial `p(H)` and solve coefficients `p`
- Video recurrence for `B`:
  - `B(n)=B(n-1)*H⊕B(n-1)⊕B(n-2)`
- Polynomial form:
  - `B = p(H) = p0*H^0 ⊕ p1*H^1 ⊕ p2*H^2 ⊕ ...`
- Only the first row `b` is needed, and `H^k(0)` equals `K(k)`:
  - `b = p*K`
- Multiply both sides by `F=K^{-1}`:
  - `p = b*F`

---

### 5) Invertible case: inverse polynomial `q(x)`, then `X=q(H)*Y`
- If there exists `q(x)` such that:
  - `q(x)p(x)=1 mod f(x)` (the video’s `f(n,x)`)
- Then:
  - `X = q(H)*Y`
- Computing `q(H)*Y` in `O(n^2)` (video method):
  - start from `Y`, repeatedly multiply by `H` (left-right diffusion) to get `H^k*Y`
  - if `qk=1`, XOR that term into the result
  - `n` diffusions × `O(n)` each ⇒ `O(n^2)`

---

### 6) Non-invertible case: `g(x)≠1` ⇒ reverse elimination
- The extended Euclid procedure produces `q'(x)` such that:
  - `q'(x)p(x)=g(x) mod f(x)`
- Define:
  - `r' = deg(g)`, and `r' = n - r`
- Define a partial result:
  - `z = q'(H)*y`
- Key equation:
  - `z = g(H)*x`

---

### 7) Build D and solve `z = D*x`
- Let `D = g(H)` in matrix form, so:
  - `z = D*x`
- Construction idea in the video:
  - multiplication by `H` corresponds to diffusion, and `K` already encodes repeated diffusion
  - use `d=K*g` to obtain the key row, then reconstruct `D` using the cross even-parity constraint

#### Properties of D (video list, with `r'=deg(g)`)
1. The last `r=n-r'` rows form a banded upper-triangular-like structure: a block of zeros on the left.
2. In those last `r` rows, a pivot `1` appears at `i=j-r'`.
3. Those last `r` rows are linearly independent.
4. The first `r'` rows are linear combinations of the last `r` rows.

#### Reverse elimination for a particular solution (video logic)
- Use only the last `r` rows to eliminate.
- Process `z[i]` left-to-right:
  - if `z[i]=1`, you must XOR row `j=i+r'` (it is the only row with pivot 1 in column `i`)
  - after XOR, `z[i]` is cleared; set `x[i]=1`
- This yields one particular solution `x`.

#### All `2^{r'}` solutions
- Since the first `r'` rows are combinations of the last `r` rows, you may XOR any combination of the first `r'` rows into `z` before elimination.
- There are `2^{r'}` combinations ⇒ `2^{r'}` distinct solutions.

#### Symmetry note (video)
- `D` is symmetric: `D[j,i]=D[i,j]`
- therefore an equivalent elimination can be done from right to left (omitted)

---

## Solvability (reflexive + symmetric ⇒ always solvable)

### Conditions (video claim)
A Lights Out game is always solvable if:
1. Reflexive: button `a` toggles light `a` (self-loop).
2. Symmetric: if `a` toggles `b`, then `b` toggles `a` (undirected edge).

This is stated to hold for any shape and layout, not only square grids.

### Proof styles in the video (summary)
- Inductive construction: remove one button to get a solvable subgame; combine multiple subgame solutions by XOR; handle odd/even cases by adding an operation that toggles an odd number of lights.
- Graph-theoretic contradiction: model as an undirected graph with self-loops; derive contradictions using “remove-a-vertex ⇒ solvable” patterns and the handshake lemma, concluding no minimal unsolvable instance exists.

---

## Engineering tips and validation

### Implementation tips
1. Use a consistent GF(2) model: only row swap and row XOR.
2. Treat out-of-bound neighbor references as 0 (non-existent).
3. Prefer “first-row-only + recurrence fill” (cross even-parity constraint) when generating matrices.
4. For speed: store rows as bitsets / machine words and XOR whole words at a time.

### Validation checklist
1. Small-n cross-check: for `n≤4`, brute force all patterns and compare with the solver outputs.
2. Silent-dimension check: compute/track `r'` and verify solution count equals `2^{r'}`.
3. Linearity check: for any two solutions `x1,x2`, verify `A·(x1⊕x2)=0` (their difference is silent).

---

## References

[1] Jaap Scherphuis, “Lights Out Mathematics”  
https://www.jaapsch.net/puzzles/lomath.htm

[2] Granvallen, “Lights Out Game and the Beauty of Mathematics”  
https://granvallen.github.io/lightoutgame/

[3] axpokl, “Flip Game O(n³) Solver”  
https://zhuanlan.zhihu.com/p/53646257

[4] Chao Xu, “Zero Forcing Sets, Lights Out, and Linear Systems”  
https://zhuanlan.zhihu.com/p/553780037

[5] GitHub — axpokl, “Pascal Implementation of Standard Lights Out O(n³) Solver”  
https://github.com/axpokl/LightOut

[6] GitHub — njpipeorgan, “Large-Scale Lights Out Solver and Notes”  
https://github.com/njpipeorgan/LightsOut

[7] OEIS — “Number of solutions for n×n all-on Lights Out” (A075462)  
https://oeis.org/A075462

[8] OEIS — “Rank deficiency of the n×n Lights Out matrix” (A159257)  
https://oeis.org/A159257
