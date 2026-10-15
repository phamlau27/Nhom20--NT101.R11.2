"""
Task 2.1 - Caesar Cipher
NT101 - An Toan Mang May Tinh - Lab 01
"""

import string

COMMON_WORDS = {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "it",
    "for", "not", "on", "with", "he", "as", "you", "do", "at", "this",
    "but", "his", "by", "from", "they", "we", "say", "her", "she", "or",
    "an", "will", "my", "one", "all", "would", "there", "their", "what",
    "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
    "is", "are", "was", "were", "has", "had", "been", "its", "can",
    "university", "information", "technology", "research", "education",
    "students", "program", "field", "wide", "range",
}


def caesar_encrypt(text: str, key: int) -> str:
    """Ma hoa Caesar: dich chuyen moi chu cai theo key."""
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + key) % 26 + base))
        else:
            result.append(ch)  # giu nguyen khoang trang, dau cau
    return "".join(result)


def caesar_decrypt(text: str, key: int) -> str:
    """Giai ma Caesar: dich nguoc theo key."""
    return caesar_encrypt(text, -key)


def score_text(text: str) -> int:
    """Cham diem van ban: dem so tu tieng Anh pho bien xuat hien."""
    words = text.lower().split()
    return sum(1 for w in words if w.strip(string.punctuation) in COMMON_WORDS)


def brute_force(ciphertext: str):
    """Thu tat ca 25 key, chon key cho van ban co nghia nhat."""
    best_key = 1
    best_score = -1
    results = []

    for key in range(1, 26):
        candidate = caesar_decrypt(ciphertext, key)
        s = score_text(candidate)
        results.append((key, s, candidate))
        if s > best_score:
            best_score = s
            best_key = key

    return best_key, results


def print_sep(char="=", width=72):
    print(char * width)


def menu():
    print_sep("=")
    print("          CAESAR CIPHER -- NT101 Lab 01")
    print_sep("=")
    print("  1. Encrypt  (ma hoa)")
    print("  2. Decrypt  (giai ma)")
    print("  3. Brute-force (thu tat ca 25 key)")
    print("  0. Thoat")
    print_sep("-")


def run_encrypt():
    print_sep("-")
    text = input("Nhap plaintext  : ").strip()
    if not text:
        print("[!] Van ban khong duoc de trong.")
        return
    try:
        key = int(input("Nhap key (1-25) : ").strip())
        if not 1 <= key <= 25:
            raise ValueError
    except ValueError:
        print("[!] Key phai la so nguyen tu 1 den 25.")
        return

    cipher = caesar_encrypt(text, key)
    print_sep("-")
    print(f"  Plaintext  : {text}")
    print(f"  Key        : {key}")
    print(f"  Ciphertext : {cipher}")
    print_sep("-")


def run_decrypt():
    print_sep("-")
    text = input("Nhap ciphertext : ").strip()
    if not text:
        print("[!] Van ban khong duoc de trong.")
        return
    try:
        key = int(input("Nhap key (1-25) : ").strip())
        if not 1 <= key <= 25:
            raise ValueError
    except ValueError:
        print("[!] Key phai la so nguyen tu 1 den 25.")
        return

    plain = caesar_decrypt(text, key)
    print_sep("-")
    print(f"  Ciphertext : {text}")
    print(f"  Key        : {key}")
    print(f"  Plaintext  : {plain}")
    print_sep("-")


def run_brute_force():
    print_sep("-")
    print("Nhap ciphertext:")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    ciphertext = " ".join(lines).strip()

    if not ciphertext:
        print("[!] Ciphertext khong duoc de trong.")
        return

    best_key, results = brute_force(ciphertext)

    print_sep("-")
    print(f"{'Key':>4} | {'Score':>5} | Plaintext (60 ky tu dau)")
    print_sep("-")
    for key, score, plain in results:
        marker = " <<< BEST" if key == best_key else ""
        preview = plain[:60].replace("\n", " ")
        print(f"  {key:>2} | {score:>5} | {preview}{marker}")

    print_sep()
    print(f"\n[OK] Key tot nhat: {best_key}")
    print(f"\n[Plaintext day du - Key {best_key}]:")
    print_sep("-")
    print(caesar_decrypt(ciphertext, best_key))
    print_sep("-")



def main():
    while True:
        menu()
        choice = input("Chon (0-3): ").strip()

        if choice == "1":
            run_encrypt()
        elif choice == "2":
            run_decrypt()
        elif choice == "3":
            run_brute_force()
        elif choice == "0":
            print("Thoat chuong trinh. Tam biet!")
            break
        else:
            print("[!] Lua chon khong hop le. Vui long chon lai.")

        input("\nNhan Enter de tiep tuc...")


if __name__ == "__main__":
    main()
