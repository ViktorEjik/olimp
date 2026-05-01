import random
import os
import sys
import os
from pathlib import Path

def generate_and_save_tests(count=10, dir_name="tests"):
    os.makedirs(dir_name, exist_ok=True)
    
    coin_chars = "abcdefghi"
    values = {'a':1, 'b':5, 'c':10, 'd':50, 'e':100, 'f':200, 'g':500, 'h':1000, 'i':2500}

    for i in range(1, count + 1):
        n = random.randint(2, 1000)
        chests = []
        for _ in range(n):
            length = random.randint(0, 1000)
            if length == 0:
                chests.append("")
            else:
                chests.append("".join(random.choices(coin_chars, k=length)))

        sums = [sum(values.get(ch, 0) for ch in s) for s in chests]
        min_val, max_val = min(sums), max(sums)

        if min_val == max_val:
            ans_k, ans_l = n - 1, n
        else:
            idx_min = max(j for j, v in enumerate(sums) if v == min_val) + 1
            idx_max = max(j for j, v in enumerate(sums) if v == max_val) + 1
            ans_k, ans_l = min(idx_min, idx_max), max(idx_min, idx_max)

        inp_path = os.path.join(dir_name, f"{i:02d}.in")
        out_path = os.path.join(dir_name, f"{i:02d}.out")

        with open(inp_path, "w") as f:
            f.write(f"{n}\n")
            for c in chests:
                f.write(c + "\n")

        with open(out_path, "w") as f:
            f.write(f"{ans_k}\n{ans_l}\n")

if __name__ == "__main__":
    out_path = Path(sys.argv[2])
    num_tests = int(sys.argv[1])
    if not out_path.exists():
        os.mkdir(out_path)
    generate_and_save_tests(num_tests, out_path)