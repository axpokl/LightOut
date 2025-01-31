import numpy as np

def pad_matrix(mat, target_shape):
    """动态填充矩阵到目标尺寸"""
    padded = np.zeros(target_shape, dtype=mat.dtype)
    padded[:mat.shape[0], :mat.shape[1]] = mat
    return padded

def strassen_multiply(X, Y):
    """支持任意维度矩阵乘法的改进版Strassen算法"""
    # 获取实际矩阵维度
    m, k = X.shape
    n = Y.shape[1]
    
    # 基础情况处理
    if m <= 2 or k <= 2 or n <= 2:
        return np.mod(np.dot(X, Y), 2)
    
    # 统一中间维度并进行填充
    new_k = k + (k % 2)
    X_pad = pad_matrix(X, (m, new_k))
    Y_pad = pad_matrix(Y, (new_k, n))
    
    # 分块处理
    mid = new_k // 2
    A, B = X_pad[:, :mid], X_pad[:, mid:]
    C, D = Y_pad[:mid, :], Y_pad[mid:, :]
    
    # 递归计算子矩阵乘积
    P1 = strassen_multiply(A, C)
    P2 = strassen_multiply(B, D)
    
    # 组合结果矩阵
    result = (P1 + P2) % 2
    
    # 裁剪回原始维度
    return result[:m, :n]

def gaussian_invert(block):
    """优化后的高斯消元求逆"""
    n = block.shape[0]
    inv = np.eye(n, dtype=int)
    aug = np.hstack((block.copy(), inv))
    
    for col in range(n):
        pivot_row = np.argmax(aug[col:, col]) + col
        aug[[col, pivot_row]] = aug[[pivot_row, col]]
        
        for row in range(n):
            if row != col and aug[row, col]:
                aug[row] ^= aug[col]
    
    return aug[:, n:]

def block_gauss_invert(M, block_size=5):
    """维度安全的分块高斯消元"""
    n = M.shape[0]
    E = np.eye(n, dtype=int)
    M = M.copy()
    
    for col_block in range(0, n, block_size):
        # 处理当前块列
        current_block_size = min(block_size, n - col_block)
        pivot_block = M[col_block:col_block+block_size, col_block:col_block+block_size]
        
        try:
            inv_pivot = gaussian_invert(pivot_block)
        except np.linalg.LinAlgError:
            inv_pivot = np.zeros_like(pivot_block)
        
        # 更新当前块行
        M_block = M[col_block:col_block+block_size, :]
        E_block = E[col_block:col_block+block_size, :]
        
        M[col_block:col_block+block_size, :] = strassen_multiply(inv_pivot, M_block) % 2
        E[col_block:col_block+block_size, :] = strassen_multiply(inv_pivot, E_block) % 2
        
        # 消去其他块行
        for row_block in range(0, n, block_size):
            if row_block == col_block:
                continue
            
            row_slice = slice(row_block, row_block+block_size)
            factor = M[row_slice, col_block:col_block+block_size]
            
            # 更新M矩阵
            update = strassen_multiply(factor, M[col_block:col_block+block_size, :])
            M[row_slice, :] = (M[row_slice, :] ^ update) % 2
            
            # 更新E矩阵
            e_update = strassen_multiply(factor, E[col_block:col_block+block_size, :])
            E[row_slice, :] = (E[row_slice, :] ^ e_update) % 2
    
    return E

# 测试矩阵定义（保持原始矩阵不变）
if __name__ == "__main__":
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

    # 计算伪逆
    pseudo_inverse = block_gauss_invert(A)
    
    # 验证结果
    product = strassen_multiply(A, pseudo_inverse) % 2
    print("结果矩阵秩:", np.linalg.matrix_rank(product))
    print("前5x5块结构:")
    print(product[:25, :25])