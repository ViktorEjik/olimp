import random
import sys
import os
from pathlib import Path
from itertools import permutations
from fractions import Fraction

def generate_tests(count=10, out_path = Path("./tests")):
    for i in range(1, count + 1):
        nums = [random.randint(-2_147_483_648, 2_147_483_647) for _ in range(4)]
        
        max_val = None
        best_p, best_q = 0, 1
        
        for k, l, m, n in permutations(nums):
            if l == 0 or n == 0: continue
            val = Fraction(k, l) + Fraction(m, n)
            if max_val is None or val > max_val:
                max_val = val
                best_p, best_q = val.numerator, val.denominator
                
        inp = " ".join(map(str, nums))
        out = f"{best_p} {best_q}"
        with open(out_path / f"{i}.in", 'w+') as f:
            f.write(inp)
        with open(out_path / f'{i}.out', 'w+') as f:
            f.write(out)

if __name__ == "__main__":
    out_path = Path(sys.argv[2])
    num_tests = int(sys.argv[1])
    if not out_path.exists():
        os.mkdir(out_path)
    
    generate_tests(num_tests, out_path)