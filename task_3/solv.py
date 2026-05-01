import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    
    it = iter(data)
    try:
        N = int(next(it))
    except StopIteration:
        return

    trib = [0, 0, 1]
    limit = 2**24
    while trib[-1] <= limit:
        trib.append(trib[-1] + trib[-2] + trib[-3])
    
    pos_trib = [t for t in trib if t > 0]
    
    tri_odious_count = 0
    
    for _ in range(N):
        A = int(next(it))
        
        if A == 0:
            continue
            
        ones = 0
        for t in reversed(pos_trib):
            if t <= A:
                A -= t
                ones += 1
                if A == 0:
                    break
                    
        if ones % 2 == 1:
            tri_odious_count += 1
            
    print(tri_odious_count)

if __name__ == "__main__":
    solve()