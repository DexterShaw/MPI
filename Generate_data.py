import random

def generate_minizinc_file(filename, v_range, m_range, ctr_range, rs_range, rt_out_range, hb_range, hs_range, hp_range, ca_range, ci_range):
    V_ = random.randint(*v_range)  # number of servers
    M_ = random.randint(*m_range)  # number of movies
    CTR = random.randint(*ctr_range)
    max_instances = 30
    
    RS = [random.randint(*rs_range) for _ in range(V_)]
    RT_OUT = [random.randint(*rt_out_range) for _ in range(V_)]
    
    HS = [random.randint(*hs_range) for _ in range(M_)]
    HB = [random.randint(*hb_range) for _ in range(M_)]
    HP = [[random.randint(*hp_range) for _ in range(M_)] for _ in range(V_)]
    
    ED = [[0 if i == j else random.randint(10, 50) for j in range(V_)] for i in range(V_)]
    
    CA = [[random.randint(*ca_range) for _ in range(M_)] for _ in range(V_)]
    
    CI = [random.randint(*ci_range) for _ in range(V_)]
    
    erlang_table = [101, 1525, 4554, 8694, 13607, 19090, 25009, 31275, 37825, 44610, 51599, 58759, 66072, 73516, 81081, 88750, 96515, 104370, 112300, 120306, 128379, 136512, 144702, 152950, 161247, 169586, 177974, 186401, 194869, 203372]
    
    with open(filename, "w") as f:
        f.write(f"%number of servers\nV_ = {V_};\n\n")
        f.write(f"% number of Movies\nM_ = {M_};\n\n")
        f.write(f"% standard cost of sending 1 MB over 1km\nCTR = {CTR};\n\n")
        f.write("%lambda\n%target_pB\n\n")
        f.write(f"max_instances = {max_instances};\n\n")
        f.write(f"% storage capacity of server v\nRS = array1d (1..V_, {RS});\n\n")
        f.write(f"% outgoing transmission capacity of server v\nRT_OUT = array1d (1..V_, {RT_OUT});\n\n")
        f.write(f"% movie size\nHS = array1d (1..M_, {HS});\n\n")
        f.write(f"% movie bitrate\nHB = array1d (1..M_, {HB});\n\n")
        f.write("% movie popularity from each server\nHP = array2d (1..V_,1..M_, [\n")
        for row in HP:
            f.write(", ".join(map(str, row)) + ",\n")
        f.write("]);\n\n")
        f.write("% edge distances\nED = array2d (1..V_, 1..V_, [\n")
        for row in ED:
            f.write(", ".join(map(str, row)) + ",\n")
        f.write("]);\n\n")
        f.write("% allocation cost\nCA = array2d (1..V_, 1..M_, [\n")
        for row in CA:
            f.write(", ".join(map(str, row)) + ",\n")
        f.write("]);\n\n")
        f.write(f"% instance cost\nCI = array1d (1..V_, {CI});\n\n")
        f.write(f"erlang_table = array1d(1..max_instances, {erlang_table});\n")

# Example usage:
v_range = (3, 3)  # Example range for V_
m_range = (5, 5)  # Example range for M_
ctr_range = (1, 5)
rs_range = (10, 100)
rt_out_range = (50, 150)
hb_range = (1, 5)
hs_range = (5, 25)
hp_range = (1, 30)
ca_range = (150, 500)
ci_range = (1, 5)

for i in range(5, 11):
    generate_minizinc_file(f"data_{i}.dzn", v_range, m_range, ctr_range, rs_range, rt_out_range, hb_range, hs_range, hp_range, ca_range, ci_range)
