import sys

def solve():
    data = sys.stdin.read().splitlines()
    if not data:
        return

    n = int(data[0].strip())
    chests = [line.strip() for line in data[1:n+1]]

    coin_values = {
        'a': 1, 'b': 5, 'c': 10, 'd': 50,
        'e': 100, 'f': 200, 'g': 500, 'h': 1000, 'i': 2500
    }

    sums = []
    for s in chests:
        cur = 0
        for ch in s:
            cur += coin_values.get(ch, 0)
        sums.append(cur)

    min_val = sums[0]
    max_val = sums[0]
    min_idx = 1
    max_idx = 1

    for i in range(1, n):
        val = sums[i]
        idx = i + 1
        if val <= min_val:
            min_val = val
            min_idx = idx


        if val >= max_val:
            max_val = val
            max_idx = idx

    if min_idx == max_idx:
        print(n - 1)
        print(n)
    else:
        k = min(min_idx, max_idx)
        l = max(min_idx, max_idx)
        print(k)
        print(l)

if __name__ == "__main__":
    solve()