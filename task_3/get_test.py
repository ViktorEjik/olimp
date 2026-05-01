import random
import os
import os
import sys
from pathlib import Path

def generate_and_save_tests(count=10, dir_name="tests"):
    os.makedirs(dir_name, exist_ok=True)
    
    trib = [0, 0, 1]
    limit = 2**24
    while trib[-1] <= limit:
        trib.append(trib[-1] + trib[-2] + trib[-3])
    pos_trib = [t for t in trib if t > 0]
    
    def get_tri_odious_parity(num):
        if num == 0: return 0
        ones = 0
        for t in reversed(pos_trib):
            if t <= num:
                num -= t
                ones += 1
                if num == 0: break
        return ones % 2

    for i in range(1, count + 1):
        n = random.randint(2, 1000)
        queries = [random.randint(0, 2**24 - 1) for _ in range(n)]
        
        ans = sum(get_tri_odious_parity(x) for x in queries)
        
        inp_path = os.path.join(dir_name, f"{i:02d}.in")
        out_path = os.path.join(dir_name, f"{i:02d}.out")
        
        with open(inp_path, "w") as f:
            f.write(f"{n}\n")
            for q in queries:
                f.write(f"{q}\n")
                
        with open(out_path, "w") as f:
            f.write(f"{ans}\n")

if __name__ == "__main__":
    out_path = Path(sys.argv[2])
    num_tests = int(sys.argv[1])
    if not out_path.exists():
        os.mkdir(out_path)
    generate_and_save_tests(num_tests, out_path)