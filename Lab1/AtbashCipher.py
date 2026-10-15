def atbash(van_ban):
    ket_qua = ""
    for c in van_ban:
        if c.isalpha():
            if c.isupper():
                
                ky_tu_moi = chr(ord('Z') - (ord(c) - ord('A')))
            else:
                
                ky_tu_moi = chr(ord('z') - (ord(c) - ord('a')))
            ket_qua += ky_tu_moi
        else:
            ket_qua += c 
    return ket_qua

if __name__ == "__main__":
    print("1. Ma hoa")
    print("2. Giai ma")
    chon = input("Chon (1/2): ").strip()
    van_ban = input("Nhap van ban: ")
    
  
    print("Ket qua:", atbash(van_ban))