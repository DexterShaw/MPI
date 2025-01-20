def PB(A: float, n: int) -> float:
    if n == 0:
        return 1.0
    else:
        prev = PB(A, n - 1)
        return (A * prev) / (A * prev + n)

def find_max_offered_load(n: int, target_pB: float, low: float, high: float) -> float:
    mid = (low + high) / 2.0
    pB = PB(mid, n)

    if abs(pB - target_pB) < 1e-6:
        return mid
    elif pB > target_pB:
        return find_max_offered_load(n, target_pB, low, mid)
    else:
        return find_max_offered_load(n, target_pB, mid, high)


max_instances = 30  
target_pB = 0.01  

erlang_table = {}

for n in range(1, max_instances + 1):
    erlang_table[n] = find_max_offered_load(n, target_pB, 0.0, 25.0)


for n, value in erlang_table.items():
    print(f"Instance {n}: Max Offered Load = {value}")
    
e_t = ""
for n, value in erlang_table.items():
    a = int(value*10000)
    e_t += str(a) + ', '
print(e_t)

