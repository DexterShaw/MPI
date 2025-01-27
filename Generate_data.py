import random

def generate_minizinc_file(filename, v_range, m_range, ctr_range, rs_range, rt_out_range, hb_range, hs_range, hp_range, ca_range, ci_range):
    V_ = random.randint(*v_range)  # number of servers
    M_ = random.randint(*m_range)  # number of movies
    CTR = random.randint(*ctr_range)
    max_instances = 300
    
    RS = [random.randint(*rs_range) for _ in range(V_)]
    RT_OUT = [random.randint(*rt_out_range) for _ in range(V_)]
    
    HS = [random.randint(*hs_range) for _ in range(M_)]
    HB = [random.randint(*hb_range) for _ in range(M_)]
    HP = [[random.randint(*hp_range) for _ in range(M_)] for _ in range(V_)]
    
    ED = [[0 if i == j else random.randint(10, 100) for j in range(V_)] for i in range(V_)]
    
    CA = [[random.randint(*ca_range) for _ in range(M_)] for _ in range(V_)]
    
    CI = [random.randint(*ci_range) for _ in range(V_)]
    
    erlang_table = [101, 1525, 4554, 8693, 13607, 19090, 25009, 31275, 37825, 44611, 51598, 58759, 66072, 73516, 81081, 88750, 96516, 104370, 112300, 120306, 128379, 136513, 144704, 152950, 161247, 169587, 177972, 186401, 194869, 203372, 211910, 220481, 229087, 237719, 246379, 255071, 263786, 272523, 281290, 290073, 298882, 307711, 316560, 325429, 334316, 343225, 352146, 361083, 370044, 379016, 388000, 397001, 406019, 415048, 424095, 433147, 442216, 451297, 460390, 469493, 478614, 487741, 496879, 506023, 515184, 524351, 533529, 542718, 551914, 561120, 570333, 579557, 588787, 598028, 607275, 616527, 625797, 635066, 644342, 653629, 662921, 672214, 681524, 690834, 700155, 709476, 718814, 728153, 737491, 746841, 756202, 765563, 774925, 784297, 793676, 803054, 812450, 821840, 831241, 840637, 850049, 859462, 868881, 878299, 887729, 897159, 906600, 916036, 925483, 934925, 944377, 953842, 963300, 972770, 982234, 991710, 1001186, 1010662, 1020149, 1029636, 1039123, 1048622, 1058120, 1067619, 1077129, 1086639, 1096149, 1105659, 1115180, 1124702, 1134223, 1143756, 1153289, 1162822, 1172355, 1181900, 1191444, 1200988, 1210533, 1220088, 1229644, 1239200, 1248756, 1258323, 1267890, 1277458, 1287025, 1296604, 1306182, 1315750, 1325340, 1334918, 1344509, 1354087, 1363677, 1373279, 1382869, 1392471, 1402072, 1411674, 1421276, 1430877, 1440490, 1450103, 1459716, 1469329, 1478942, 1488567, 1498191, 1507804, 1517440, 1527065, 1536689, 1546325, 1555961, 1565597, 1575233, 1584869, 1594505, 1604152, 1613800, 1623447, 1633094, 1642742, 1652400, 1662048, 1671707, 1681365, 1691024, 1700683, 1710342, 1720012, 1729682, 1739341, 1749011, 1758682, 1768352, 1778022, 1787704, 1797386, 1807056, 1816738, 1826419, 1836101, 1845794, 1855476, 1865158, 1874851, 1884544, 1894226, 1903930, 1913612, 1923316, 1933021, 1942714, 1952407, 1962112, 1971817, 1981521, 1991226, 2000930, 2010635, 2020351, 2030067, 2039772, 2049488, 2059204, 2068908, 2078636, 2088352, 2098068, 2107795, 2117523, 2127239, 2136955, 2146682, 2156410, 2166137, 2175865, 2185592, 2195331, 2205070, 2214797, 2224525, 2234275, 2244003, 2253753, 2263481, 2273231, 2282958, 2292709, 2302459, 2312187, 2321937, 2331687, 2341438, 2351188, 2360939, 2370689, 2380439, 2390190, 2399940, 2409690, 2419452, 2429214, 2438964, 2448715, 2458488, 2468238, 2478012, 2487762, 2497535, 2507286, 2517059, 2526832, 2536582, 2546356, 2556129, 2565902, 2575675, 2585449, 2595211, 2604984, 2614768, 2624542, 2634315, 2644088, 2653861, 2663635, 2673419, 2683204, 2692977, 2702762, 2712547, 2722320, 2732116, 2741889, 2751686, 2761459, 2771255]
    
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
rs_range = (1, 20)
rt_out_range = (1, 10)
hb_range = (1, 5)
hs_range = (1, 5)
hp_range = (0, 40)
ca_range = (5, 10)
ci_range = (10, 20)

for i in range(2, 3):
    generate_minizinc_file(f"part2_cdn_data_1{i}.dzn", v_range, m_range, ctr_range, rs_range, rt_out_range, hb_range, hs_range, hp_range, ca_range, ci_range)
