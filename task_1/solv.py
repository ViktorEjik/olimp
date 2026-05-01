import sys
from itertools import permutations
from fractions import Fraction

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    
    nums = [int(x) for x in data]
    
    max_val = None
    best_p = 0
    best_q = 1
    
    # Тупой переборный вариант. Можно лучше и для произвольного числа начальных 
    # чисел, но мне влом.
    for k, l, m, n in permutations(nums):
        if l == 0 or n == 0:
            continue
            
        current_val = Fraction(k, l) + Fraction(m, n)
        
        if max_val is None or current_val > max_val:
            max_val = current_val
            best_p = max_val.numerator
            best_q = max_val.denominator
            
    print(best_p, best_q)

if __name__ == "__main__":
    solve()