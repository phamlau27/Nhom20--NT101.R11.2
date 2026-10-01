def tao_khoa(van_ban, khoa):
    khoa = khoa.upper()
    chuoi_khoa = ""
    vi_tri = 0
    for ky_tu in van_ban:
        if ky_tu.isalpha():
            chuoi_khoa += khoa[vi_tri % len(khoa)]
            vi_tri += 1
        else:
            chuoi_khoa += ky_tu
    return chuoi_khoa


def ma_hoa(ban_ro, khoa):
    chuoi_khoa = tao_khoa(ban_ro, khoa)
    ban_ma = ""
    for i in range(len(ban_ro)):
        c = ban_ro[i]
        k = chuoi_khoa[i]
        if c.isalpha():
            p_so = ord(c.upper()) - ord("A")
            k_so = ord(k) - ord("A")
            c_so = (p_so + k_so) % 26
            ky_tu_moi = chr(c_so + ord("A"))
            ban_ma += ky_tu_moi.lower() if c.islower() else ky_tu_moi
        else:
            ban_ma += c
    return ban_ma


def giai_ma(ban_ma, khoa):
    chuoi_khoa = tao_khoa(ban_ma, khoa)
    ban_ro = ""
    for i in range(len(ban_ma)):
        c = ban_ma[i]
        k = chuoi_khoa[i]
        if c.isalpha():
            c_so = ord(c.upper()) - ord("A")
            k_so = ord(k) - ord("A")
            p_so = (c_so - k_so + 26) % 26
            ky_tu_moi = chr(p_so + ord("A"))
            ban_ro += ky_tu_moi.lower() if c.islower() else ky_tu_moi
        else:
            ban_ro += c
    return ban_ro


if __name__ == "__main__":
    print("1. Ma hoa")
    print("2. Giai ma")
    lua_chon = input("Chon (1 hoac 2): ").strip()

    if lua_chon == "1":
        ban_ro = input("Nhap ban ro: ")
        khoa = input("Nhap khoa: ").strip()
        print("\nKet qua ma hoa:", ma_hoa(ban_ro, khoa))
    elif lua_chon == "2":
        ban_ma = input("Nhap ciphertext: ")
        khoa = input("Nhap khoa: ").strip()
        print("\nKet qua giai ma:", giai_ma(ban_ma, khoa))
    else:
        print("Lua chon khong hop le!")