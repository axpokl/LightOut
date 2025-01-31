import numpy as np

def gf2_gauss_jordan(A):
    """严格的GF(2)高斯-约当消元"""
    n = A.shape[0]
    E = np.eye(n, dtype=int)
    
    for col in range(n):
        # 寻找主元
        pivot = np.where(A[col:, col] == 1)[0]
        if not pivot.size:
            continue  # 跳过自由变量列
        
        pivot_row = pivot[0] + col
        
        # 交换行
        if pivot_row != col:
            A[[col, pivot_row]] = A[[pivot_row, col]]
            E[[col, pivot_row]] = E[[pivot_row, col]]
        
        # 消去其他行
        for row in range(n):
            if row != col and A[row, col]:
                A[row] ^= A[col]
                E[row] ^= E[col]
    
    # 标准化行
    for i in range(n):
        if A[i, i] == 1:
            continue
        for j in range(i+1, n):
            if A[j, i] == 1:
                A[i] ^= A[j]
                E[i] ^= E[j]
                break
    
    return E

def block_gf2_invert(A, block_size=5):
    """分块高斯消元 (不改变算法结构，仅优化实现)"""
    n = A.shape[0]
    E = np.eye(n, dtype=int)
    A = A.copy()
    
    # 记录自由变量位置
    free_vars = []
    
    for col in range(0, n, block_size):
        current_block = slice(col, min(col+block_size, n))
        
        # 处理当前块列
        for c in range(col, min(col+block_size, n)):
            # 寻找主元
            pivot_row = None
            for r in range(c, n):
                if A[r, c] == 1:
                    pivot_row = r
                    break
            
            if pivot_row is None:
                free_vars.append(c)
                continue
                
            # 交换行
            if pivot_row != c:
                A[[c, pivot_row]] ^= A[[pivot_row, c]]
                E[[c, pivot_row]] ^= E[[pivot_row, c]]
            
            # 消去当前列
            for r in range(n):
                if r != c and A[r, c]:
                    A[r] ^= A[c]
                    E[r] ^= E[c]
    
    # 处理自由变量 (保持结果与标准高斯一致)
    for c in free_vars:
        E[c] = 0
    
    return E

if __name__ == "__main__":
    # 原始矩阵定义 (保持用户提供的25x25矩阵)
    A = np.array([
        [1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,1,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,1,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,1,0,0,0,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,1,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,1,0,0,0,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,1],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,1],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1]
    ], dtype=int)

    # 使用标准高斯消元验证
    standard_E = gf2_gauss_jordan(A.copy())[1]
    print("标准高斯消元结果:")
    print(standard_E)

    # 使用分块算法计算
    block_E = block_gf2_invert(A.copy())
    print("\n分块算法结果:")
    print(block_E)

    # 验证结果一致性
    assert np.array_equal(standard_E, block_E), "结果不一致"
    print("\n验证通过，结果正确")