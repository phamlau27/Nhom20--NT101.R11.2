
import base64
import secrets

def egcd(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

def modinv(e, phi):
    g, x, _ = egcd(e, phi)
    if g != 1:
        raise ValueError("e khong nguyen to cung nhau voi phi(n)")
    return x % phi

def is_prime(n, rounds=40):
    """Kiem tra nguyen to Miller-Rabin."""
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def gen_prime(bits):
    while True:
        c = secrets.randbits(bits) | (3 << (bits - 2)) | 1 
        if is_prime(c):
            return c


def make_keys(p, q, e):
    n = p * q
    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)
    return {"p": p, "q": q, "n": n, "phi": phi, "e": e, "d": d,
            "PU": (e, n), "PR": (d, n)}

def random_keys(bits=2048, e=65537):
    """Sinh cap khoa ngau nhien khi p, q, e khong duoc cung cap."""
    while True:
        p, q = gen_prime(bits // 2), gen_prime(bits // 2)
        if p == q:
            continue
        phi = (p - 1) * (q - 1)
        if egcd(e, phi)[0] == 1:
            return make_keys(p, q, e)


def encrypt_conf(m, k):   # C = M^e mod n  (bao mat)
    return pow(m, k["e"], k["n"])

def decrypt_conf(c, k):   # M = C^d mod n
    return pow(c, k["d"], k["n"])

def encrypt_auth(m, k):   # C = M^d mod n  (xac thuc / chu ky)
    return pow(m, k["d"], k["n"])

def decrypt_auth(c, k):   # M = C^e mod n
    return pow(c, k["e"], k["n"])


def sizes(n):
    return max(1, (n.bit_length() - 1) // 8), (n.bit_length() + 7) // 8

def encrypt_text(text, k, mode):
    f = encrypt_conf if mode == "conf" else encrypt_auth
    k_in, k_out = sizes(k["n"])
    data, out = text.encode("utf-8"), b""
    for i in range(0, len(data), k_in):
        m = int.from_bytes(data[i:i + k_in], "little")
        if m >= k["n"]:
            raise ValueError("khoi plaintext >= n, khoa qua nho cho thong diep nay")
        out += f(m, k).to_bytes(k_out, "little")
    return out

def decrypt_text(raw, k, mode):
    f = decrypt_conf if mode == "conf" else decrypt_auth
    k_in, k_out = sizes(k["n"])
    out = b""
    for i in range(0, len(raw), k_out):
        m = f(int.from_bytes(raw[i:i + k_out], "little"), k)
        out += m.to_bytes(k_in, "little")
    return out.rstrip(b"\x00").decode("utf-8", errors="replace")


KEYS = {
    1: make_keys(11, 17, 7),
    2: make_keys(20079993872842322116151219, 676717145751736242170789, 17),
    3: make_keys(0xF7E75FDC469067FFDC4E847C51F452DF,
                 0xE85CED54AF57E53E092113E62F436F4F, 0x0D88C3),
}
MESSAGE = "The University of Information Technology"
C1 = ("raUcesUlOkx/8ZhgodMoo0Uu18sC20yXlQFevSu7W/FDxIy0YRHMyXcHdD9PBvIT2aUft5fCQEGomiVVPv4I")
C2 = "C87F570FC4F699CEC24020C6F54221ABAB2CE0C3"
C3 = "Z2BUSkJcg0w4XEpgm0JcMExEQmBlVH6dYEpNTHpMHptMQ7NgTHlgQrNMQ2BKTQ=="
C4 = ("001010000001010011111111101101110010111011001010111011000110011"
      "110111111001111110110100011001111001100001001010001010100111101"
      "010100110011101110111011110101101100000100")

def hr(t):
    print("\n" + t)

def main():
    hr("CAU 1: Xac dinh PU, PR")
    for i, k in KEYS.items():
        print(f"[Bo khoa {i}] n bit = {k['n'].bit_length()}")
        print(f"  p = {k['p']}\n  q = {k['q']}\n  n = {k['n']}\n  phi(n) = {k['phi']}")
        print(f"  PU = (e, n) = ({k['e']}, {k['n']})")
        print(f"  PR = (d, n) = ({k['d']}, {k['n']})")

    hr("CAU 2: M = 5 voi bo khoa 1")
    k = KEYS[1]
    c = encrypt_conf(5, k)
    print(f"Bao mat   : C = 5^{k['e']} mod {k['n']} = {c} ; M = {c}^{k['d']} mod {k['n']} = {decrypt_conf(c, k)}")
    c = encrypt_auth(5, k)
    print(f"Xac thuc  : C = 5^{k['d']} mod {k['n']} = {c} ; M = {c}^{k['e']} mod {k['n']} = {decrypt_auth(c, k)}")

    hr("CAU 3: Ma hoa")
    print("Thong diep:", MESSAGE)
    for i, k in KEYS.items():
        k_in, k_out = sizes(k["n"])
        for mode, name in (("conf", "Bao mat (PU)"), ("auth", "Xac thuc (PR)")):
            raw = encrypt_text(MESSAGE, k, mode)
            back = decrypt_text(raw, k, mode)
            print(f"[K{i}] {name}, khoi vao {k_in}B / khoi ra {k_out}B:")
            print("  Base64:", base64.b64encode(raw).decode())
            print("  Giai ma kiem tra:", back, "->", "DUNG" if back == MESSAGE else "SAI")

    hr("CAU 4: Giai ma")
    cands = {
        "BM1 (Base64)": base64.b64decode(C1),
        "BM2 (HEX)": bytes.fromhex(C2),
        "BM3 (Base64)": base64.b64decode(C3),
        "BM4 (nhi phan)": int(C4, 2).to_bytes((len(C4) + 7) // 8, "big"),
    }
    for name, raw in cands.items():
        found = False
        for i, k in KEYS.items():
            _, k_out = sizes(k["n"])
            
            if i == 1:
                r = raw
            else:
                r = raw + b"\x00" * ((-len(raw)) % k_out)
            if len(r) % k_out:
                continue
            for mode in ("conf", "auth"):
                try:
                    t = decrypt_text(r, k, mode)
                except Exception:
                    continue
                if t and all(32 <= ord(ch) < 127 for ch in t):
                    print(f"{name}: khoa {i}, che do {'bao mat' if mode=='conf' else 'xac thuc'} -> {t!r}")
                    found = True
        if not found:
            print(f"{name}: khong giai ma duoc")

    hr("THEM: Sinh khoa ngau nhien lon (khi p, q, e khong duoc cung cap)")
    k = random_keys(2048)
    print("n bit =", k["n"].bit_length(), "| e =", k["e"])
    raw = encrypt_text(MESSAGE, k, "conf")
    print("Base64:", base64.b64encode(raw).decode()[:60] + "...")
    print("Giai ma:", decrypt_text(raw, k, "conf"))

if __name__ == "__main__":
    main()
