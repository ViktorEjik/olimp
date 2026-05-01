import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    
    it = iter(data)
    try:
        N = int(next(it))
    except StopIteration:
        return

    temps = [int(next(it)) for _ in range(N)]
    K = int(next(it))

    M = 1
    while M < N:
        M <<= 1 

    INF_NEG = -10**18
    tree = [INF_NEG] * (2 * M)
    
    for i in range(N):
        tree[M + i] = temps[i]
        
    for i in range(M - 1, 0, -1):
        left = tree[2 * i]
        right = tree[2 * i + 1]
        tree[i] = left if left > right else right
        

    out = []
    num_queries = N - K + 1
    
    for _ in range(num_queries):
        l_exp = int(next(it))
        r_exp = int(next(it))
        
        i = len(out)
        L = i - l_exp
        R = i + K - 1 + r_exp
        
        if L < 0: L = 0
        if R >= N: R = N - 1
        
        l, r = L + M, R + M
        mx = INF_NEG
        while l <= r:
            if l & 1:
                val = tree[l]
                if val > mx: mx = val
                l += 1
            if not (r & 1):
                val = tree[r]
                if val > mx: mx = val
                r -= 1
            l >>= 1
            r >>= 1
            
        out.append(str(mx))
        
    sys.stdout.write(' '.join(out) + '\n')

if __name__ == "__main__":
    solve()