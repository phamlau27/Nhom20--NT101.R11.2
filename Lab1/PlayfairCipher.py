def tao_ma_tran(khoa):
    khoa = khoa.upper().replace("J", "I")
    chuoi = ""
    for c in khoa:
        if c.isalpha() and c not in chuoi:
            chuoi += c
    for c in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if c not in chuoi:
            chuoi += c
    return [list(chuoi[i * 5 : (i + 1) * 5]) for i in range(5)]


def in_ma_tran(m):
    print("Ma tran Playfair 5x5:")
    for hang in m:
        print(" ".join(hang))


def tim_vi_tri(m, c):
    for r in range(5):
        for col in range(5):
            if m[r][col] == c:
                return r, col


def tach_cap(text):
    text = [c for c in text.upper().replace("J", "I") if c.isalpha()]
    caps = []
    i = 0
    while i < len(text):
        c1 = text[i]
        if i + 1 < len(text):
            c2 = text[i + 1]
            if c1 == c2:
                caps.append((c1, "X"))
                i += 1
            else:
                caps.append((c1, c2))
                i += 2
        else:
            caps.append((c1, "X"))
            i += 1
    return caps


def ma_hoa(text, m):
    caps = tach_cap(text)
    kq = ""
    for c1, c2 in caps:
        r1, c1_col = tim_vi_tri(m, c1)
        r2, c2_col = tim_vi_tri(m, c2)
        if r1 == r2:
            kq += m[r1][(c1_col + 1) % 5] + m[r2][(c2_col + 1) % 5]
        elif c1_col == c2_col:
            kq += m[(r1 + 1) % 5][c1_col] + m[(r2 + 1) % 5][c2_col]
        else:
            kq += m[r1][c2_col] + m[r2][c1_col]
    return kq


def giai_ma(text, m):
    text = [c for c in text.upper().replace("J", "I") if c.isalpha()]
    kq = ""
    for i in range(0, len(text), 2):
        c1 = text[i]
        c2 = text[i + 1] if i + 1 < len(text) else "X"
        r1, c1_col = tim_vi_tri(m, c1)
        r2, c2_col = tim_vi_tri(m, c2)
        if r1 == r2:
            kq += m[r1][(c1_col - 1) % 5] + m[r2][(c2_col - 1) % 5]
        elif c1_col == c2_col:
            kq += m[(r1 - 1) % 5][c1_col] + m[(r2 - 1) % 5][c2_col]
        else:
            kq += m[r1][c2_col] + m[r2][c1_col]
    return kq


chon = input("1. Ma hoa\n2. Giai ma\nChon (1/2): ").strip()
khoa = input("Nhap khoa: ").strip()
van_ban = input("Nhap van ban: ").strip()

ma_tran = tao_ma_tran(khoa)
in_ma_tran(ma_tran)

if chon == "1":
    print("Ket qua:", ma_hoa(van_ban, ma_tran))
else:
    print("Ket qua:", giai_ma(van_ban, ma_tran))