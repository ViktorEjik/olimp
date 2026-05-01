import random
import os
import sys
from pathlib import Path

def generate_and_save_tests(count=10, dir_name="tests"):
    os.makedirs(dir_name, exist_ok=True)
    
    for i in range(1, count + 1):
        N = random.randint(2, min(1000, 10**7))
        temps = [random.randint(-1000, 1000) for _ in range(N)]
        K = random.randint(1, min(N, 100))
        queries = [(random.randint(0, K), random.randint(0, K)) for _ in range(N - K + 1)]
        
        ans = []
        for idx, (l_exp, r_exp) in enumerate(queries):
            L = max(0, idx - l_exp)
            R = min(N - 1, idx + K - 1 + r_exp)
            ans.append(str(max(temps[L:R+1])))
            
        inp_path = os.path.join(dir_name, f"input_{i:02d}.txt")
        out_path = os.path.join(dir_name, f"output_{i:02d}.txt")
        
        with open(inp_path, "w") as f:
            f.write(f"{N} {' '.join(map(str, temps))}\n")
            f.write(f"{K}\n")
            for l, r in queries:
                f.write(f"{l} {r}\n")
                
        with open(out_path, "w") as f:
            f.write(' '.join(ans) + '\n')

if __name__ == "__main__":
    out_path = Path(sys.argv[2])
    num_tests = int(sys.argv[1])
    if not out_path.exists():
        os.mkdir(out_path)
        generate_and_save_tests(num_tests, out_path)