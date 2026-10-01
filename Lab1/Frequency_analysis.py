"""
Task 2.2 - Mono-alphabetic Substitution Cipher + Frequency Analysis
NT101 - An Toan Mang May Tinh - Lab 01
"""

import string
from collections import Counter

ENGLISH_FREQ = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0,
    'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3,
    'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4, 'W': 2.4,
    'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5,
    'V': 1.0, 'K': 0.8, 'J': 0.15,'X': 0.15,'Q': 0.10,
    'Z': 0.07,
}


def analyze_frequency(ciphertext: str) -> list:
    text_upper = ciphertext.upper()
    letters_only = [ch for ch in text_upper if 'A' <= ch <= 'Z']
    total = len(letters_only)
    counts = Counter(letters_only)
    sorted_freq = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    result = []
    for letter, count in sorted_freq:
        pct = (count / total * 100) if total > 0 else 0
        result.append((letter, count, pct))
    return result


def apply_mapping(ciphertext: str, mapping: dict) -> str:
    result = []
    for ch in ciphertext:
        upper_ch = ch.upper()
        if 'A' <= upper_ch <= 'Z':        
            if upper_ch in mapping:
                result.append(mapping[upper_ch].lower())  
            else:
                result.append(upper_ch)                  
        else:
            result.append(ch)              
    return "".join(result)


def print_sep(char="-", width=72):
    print(char * width)


def print_freq_table(freq_list: list):
    """In bang tan suat theo dinh dang ro rang."""
    print_sep()
    print(f"  {'Rank':>4} | {'Cipher':>6} | {'Count':>6} | {'Pct %':>6} || {'English Ref':>11}")
    print_sep()
    eng_sorted = sorted(ENGLISH_FREQ.items(), key=lambda x: x[1], reverse=True)
    for i, (letter, count, pct) in enumerate(freq_list):
        eng_letter, eng_pct = eng_sorted[i] if i < len(eng_sorted) else ("-", 0)
        print(f"  {i+1:>4} | {letter:>6} | {count:>6} | {pct:>5.2f}% || {eng_letter}: {eng_pct:.2f}%")
    print_sep()


def print_mapping(mapping: dict):
    """Hien thi mapping hien tai."""
    print_sep()
    print("  Mapping hien tai (Cipher -> Plain):")
    if not mapping:
        print("  (chua co mapping nao)")
    else:
        items = sorted(mapping.items())
        row = ""
        for cipher_ch, plain_ch in items:
            row += f"  {cipher_ch}->{plain_ch.upper()}"
        print(row)
    # In cac chu chua map
    unmapped = [c for c in string.ascii_uppercase if c not in mapping]
    if unmapped:
        print(f"  Chua map: {' '.join(unmapped)}")
    print_sep()


def load_ciphertext() -> str:
    """Cho phep nguoi dung nhap ciphertext truc tiep hoac doc tu file."""
    print_sep("=")
    print("  Nhap ciphertext:")
    print("  1. Nhap truc tiep tu ban phim")
    print("  2. Doc tu file")
    print_sep("-")
    choice = input("Chon (1/2): ").strip()

    if choice == "2":
        path = input("Nhap duong dan file: ").strip()
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            print(f"[OK] Da doc {len(text)} ky tu tu file.")
            return text
        except FileNotFoundError:
            print(f"[!] Khong tim thay file: {path}")
            return ""
        except Exception as e:
            print(f"[!] Loi khi doc file: {e}")
            return ""
    else:
        print("Nhap ciphertext (dong trong de ket thuc):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        return "\n".join(lines).strip()


def menu_main():
    print_sep("=")
    print("  FREQUENCY ANALYSIS - NT101 Lab 01")
    print_sep("=")
    print("  1. Xem thong ke tan suat")
    print("  2. Nhap / thay doi mapping (Cipher->Plain)")
    print("  3. Xem plaintext tam thoi (theo mapping hien tai)")
    print("  4. Xem mapping hien tai")
    print("  5. Reset mapping")
    print("  6. Doi ciphertext moi")
    print("  0. Thoat")
    print_sep("-")


def main():
    ciphertext = ""
    mapping = {}   # { 'A': 'e', 'B': 't', ... }

    print_sep("=")
    print("  MONO-ALPHABETIC SUBSTITUTION - FREQUENCY ANALYSIS")
    print("  NT101 Lab 01")
    print_sep("=")

    # Buoc 1: Tai ciphertext
    ciphertext = load_ciphertext()
    if not ciphertext:
        print("[!] Khong co ciphertext. Ket thuc chuong trinh.")
        return

    while True:
        menu_main()
        choice = input("Chon (0-6): ").strip()

        if choice == "0":
            print("Thoat chuong trinh. Tam biet!")
            break

        elif choice == "1":
            # Thong ke tan suat
            freq = analyze_frequency(ciphertext)
            print("\n[Tan suat xuat hien cac chu cai trong ciphertext]")
            print_freq_table(freq)
            print("  Goi y: So sanh voi tan suat tieng Anh de doan mapping.")
            print("         E(12.7%) T(9.1%) A(8.2%) O(7.5%) I(7.0%) N(6.7%)")

        elif choice == "2":
            # Nhap / thay doi mapping
            print_sep("-")
            print("  Nhap mapping theo dinh dang: CIPHER=PLAIN")
            print("  Vi du: Z=e  hoac  Z=E  (co the nhap nhieu cap, cach nhau dau phay)")
            print("  Vi du: Z=e, X=t, Q=a")
            raw = input("  Nhap: ").strip()
            if not raw:
                print("[!] Khong co gi duoc nhap.")
            else:
                pairs = [p.strip() for p in raw.replace(",", " ").split() if "=" in p]
                updated = 0
                for pair in pairs:
                    parts = pair.split("=")
                    if len(parts) == 2:
                        c = parts[0].strip().upper()
                        p = parts[1].strip().upper()
                        if len(c) == 1 and 'A' <= c <= 'Z' and len(p) == 1 and 'A' <= p <= 'Z':
                            # Kiem tra one-to-one: plain letter nay da duoc dung chua?
                            conflict = [k for k, v in mapping.items() if v == p and k != c]
                            if conflict:
                                print(f"  [!] Canh bao: '{p}' da duoc map boi '{conflict[0]}'. "
                                      f"Ghi de mapping cu hay bo qua? (o=ghi de / b=bo qua): ", end="")
                                ans = input().strip().lower()
                                if ans != 'o':
                                    print(f"  [Huy] Bo qua mapping {c}={p}.")
                                    continue
                                # Xoa mapping cu truoc khi ghi de
                                for k in conflict:
                                    del mapping[k]
                            mapping[c] = p
                            updated += 1
                        else:
                            print(f"  [!] Bo qua cap khong hop le: {pair}")
                print(f"  [OK] Da cap nhat {updated} mapping.")
            # Tu dong hien thi plaintext tam thoi sau khi cap nhat
            if mapping:
                partial = apply_mapping(ciphertext, mapping)
                print_sep("-")
                print("[Plaintext tam thoi (chu thuong=da map, chu HOA=chua map)]:")
                print_sep("-")
                print(partial)
                print_sep("-")

        elif choice == "3":
            # Xem plaintext tam thoi
            if not mapping:
                print("  [!] Chua co mapping nao. Vui long nhap mapping truoc.")
            else:
                partial = apply_mapping(ciphertext, mapping)
                print_sep("-")
                print("[Plaintext tam thoi (chu thuong = da map, chu HOA = chua map)]:")
                print_sep("-")
                print(partial)
                print_sep("-")

        elif choice == "4":
            # Xem mapping hien tai
            print_mapping(mapping)

        elif choice == "5":
            # Reset mapping
            confirm = input("  Reset toan bo mapping? (y/n): ").strip().lower()
            if confirm == "y":
                mapping.clear()
                print("  [OK] Da xoa toan bo mapping.")
            else:
                print("  [Huy] Giu nguyen mapping cu.")

        elif choice == "6":
            # Doi ciphertext moi
            ciphertext = load_ciphertext()
            if ciphertext:
                mapping.clear()
                print("  [OK] Da tai ciphertext moi. Mapping duoc reset.")
            else:
                print("  [!] Khong co ciphertext moi, giu nguyen cu.")

        else:
            print("[!] Lua chon khong hop le. Vui long chon lai.")

        input("\nNhan Enter de tiep tuc...")


if __name__ == "__main__":
    main()
