def F(right, subkey):
    return (right ^ subkey) & 0x0F

def feistel_round(L_in, R_in, subkey):
    L_out = R_in                    
    R_out = L_in ^ F(R_in, subkey)  
    return L_out, R_out

def track_avalanche(msg, key):
    L, R = (msg >> 4) & 0x0F, msg & 0x0F
    subkeys = [key & 0x0F, (key >> 4) & 0x0F, (key + 1) & 0x0F, (key + 2) & 0x0F]
    print(f"Khởi tạo: L={format(L,'04b')}, R={format(R,'04b')}")
    for i in range(4):
        L, R = feistel_round(L, R, subkeys[i])
        print(f"Vòng {i+1}: L={format(L,'04b')}, R={format(R,'04b')}")
    return (L << 4) | R

print("Mã hóa M1"); track_avalanche(0xAB, 0x12)
print("Mã hóa M2"); track_avalanche(0xAC, 0x12)

def hamming(a, b):
    return bin(a ^ b).count("1")

def trace(msg, key):
    L, R = (msg >> 4) & 0x0F, msg & 0x0F
    subkeys = [key & 0x0F, (key >> 4) & 0x0F, (key + 1) & 0x0F, (key + 2) & 0x0F]
    states = [(L, R)]
    for k in subkeys:
        L, R = feistel_round(L, R, k)
        states.append((L, R))
    return states

s1, s2 = trace(0xAB, 0x12), trace(0xAC, 0x12)
for i, ((l1, r1), (l2, r2)) in enumerate(zip(s1, s2)):
    ten = "Khởi tạo" if i == 0 else f"Vòng {i}"
    print(f"{ten}: khác L={hamming(l1,l2)}, R={hamming(r1,r2)}, tổng={hamming(l1,l2)+hamming(r1,r2)}/8")