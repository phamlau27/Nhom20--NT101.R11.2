"""
Lab 02 - Nhiem vu 2.3: Avalanche Effect - DES
Mon: An toan mang may tinh | Nhom 20
"""
from Crypto.Cipher import DES

P1 = b"STAYHOME"
P2 = b"STAYHOMA"


def to_bits(data):
    """Chuyen bytes -> chuoi nhi phan 64 bit."""
    return bin(int.from_bytes(data, "big"))[2:].zfill(64)


def hamming(b1, b2):
    """Dem so bit khac nhau."""
    return sum(x != y for x, y in zip(b1, b2))


def des_encrypt(key_bytes, pt):
    return DES.new(key_bytes, DES.MODE_ECB).encrypt(pt)


def test_key(key_bytes, label):
    """Ma hoa p1, p2 voi key; in ket qua; tra ve (diff, pct)."""
    c1 = des_encrypt(key_bytes, P1)
    c2 = des_encrypt(key_bytes, P2)
    b1, b2 = to_bits(c1), to_bits(c2)
    diff = hamming(b1, b2)
    pct  = diff / 64 * 100

    print(f"\n  Key    : {key_bytes.decode(errors='replace')}  [{label}]")
    print(f"  C1 Hex : {c1.hex()}")
    print(f"  C2 Hex : {c2.hex()}")
    print(f"  C1 Bin : {b1}")
    print(f"  C2 Bin : {b2}")
    print(f"  Hamming: {diff}/64  ({pct:.2f}%)")
    return diff, pct


def main():
    print("Nhiem vu 2.3: Avalanche Effect - DES ECB")
    print(f"  P1 = {P1.decode()}  |  P2 = {P2.decode()}  (khac 1 ky tu cuoi)")
    print("-" * 60)

    # Thu nghiem voi key mac dinh
    test_key(b"87654321", "default")

    # Thu nghiem voi MSSV cac thanh vien
    results = []
    i = 1
    print()
    while True:
        raw = input(f"  Nhap MSSV thanh vien {i} (8 chu so, Enter de ket thuc): ").strip()
        if not raw:
            break
        if len(raw) != 8 or not raw.isdigit():
            print("  [LOI] MSSV phai co dung 8 chu so (0-9).")
            continue
        diff, pct = test_key(raw.encode("ascii"), f"MSSV {raw}")
        results.append((raw, diff, pct))
        i += 1

    # Bang tong hop
    if results:
        print()
        print("-" * 60)
        print(f"  {'MSSV':<12} {'Hamming':>10} {'Ty le (%)':>10}")
        print(f"  {'-'*12} {'-'*10} {'-'*10}")
        for mssv, diff, pct in results:
            print(f"  {mssv:<12} {str(diff)+'/64':>10} {pct:>9.2f}%")
        avg = sum(p for _, _, p in results) / len(results)
        print(f"\n  Trung binh MSSV: {avg:.2f}%  (ly tuong ~50%)")


if __name__ == "__main__":
    main()
