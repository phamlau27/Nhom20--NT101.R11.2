import os
from collections import Counter

ENGLISH_FREQ = {
    'A': 8.2,  'B': 1.5,  'C': 2.8,  'D': 4.3,  'E': 12.7, 'F': 2.2,  'G': 2.0,
    'H': 6.1,  'I': 7.0,  'J': 0.15, 'K': 0.77, 'L': 4.0,  'M': 2.4,  'N': 6.7,
    'O': 7.5,  'P': 1.9,  'Q': 0.095,'R': 6.0,  'S': 6.3,  'T': 9.1,  'U': 2.8,
    'V': 0.98, 'W': 2.4,  'X': 0.15, 'Y': 2.0,  'Z': 0.074
}

def clean_text(text):
    return ''.join([c.upper() for c in text if c.isalpha()])

def calculate_ic(text):
    n = len(text)
    if n <= 1:
        return 0.0
    counts = Counter(text)
    return sum(count * (count - 1) for count in counts.values()) / (n * (n - 1))

def find_key_length(ciphertext, max_len=20):
    clean_ct = clean_text(ciphertext)
    best_length = 1
    best_avg_ic = 0.0
    ic_scores = {}

    for klen in range(1, max_len + 1):
        total_ic = 0.0
        for i in range(klen):
            slice_text = clean_ct[i::klen]
            total_ic += calculate_ic(slice_text)
        avg_ic = total_ic / klen
        ic_scores[klen] = avg_ic

        if avg_ic > best_avg_ic:
            best_avg_ic = avg_ic
            best_length = klen

    return best_length, ic_scores

def solve_caesar(slice_text):
    n = len(slice_text)
    counts = Counter(slice_text)
    best_shift = 0
    lowest_chi2 = float('inf')

    for shift in range(26):
        chi2 = 0.0
        for i in range(26):
            char = chr(ord('A') + i)
            enc_char = chr(ord('A') + (i + shift) % 26)
            observed = counts.get(enc_char, 0)
            expected = n * (ENGLISH_FREQ[char] / 100.0)
            chi2 += ((observed - expected) ** 2) / (expected + 1e-9)

        if chi2 < lowest_chi2:
            lowest_chi2 = chi2
            best_shift = shift

    return chr(ord('A') + best_shift)

def crack_vigenere(ciphertext, max_key_len=20):
    clean_ct = clean_text(ciphertext)
    if len(clean_ct) < 10:
        return None, "Ciphertext quá ngắn để phân tích thống kê!", 0, {}

    key_length, ic_scores = find_key_length(clean_ct, max_key_len)

    recovered_key = []
    for i in range(key_length):
        slice_text = clean_ct[i::key_length]
        char = solve_caesar(slice_text)
        recovered_key.append(char)
    key = ''.join(recovered_key)

    plaintext = []
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            is_upper = char.isupper()
            c_val = ord(char.upper()) - ord('A')
            k_val = ord(key[key_index % key_length]) - ord('A')
            p_val = (c_val - k_val + 26) % 26
            p_char = chr(ord('A') + p_val) if is_upper else chr(ord('a') + p_val)
            plaintext.append(p_char)
            key_index += 1
        else:
            plaintext.append(char)

    return key, ''.join(plaintext), key_length, ic_scores

def get_input_ciphertext():
    while True:
        print("=" * 55)
        print(" CHƯƠNG TRÌNH PHÁ MÃ VIGENÈRE")
        print("=" * 55)
        print("1. Nhập ciphertext trực tiếp từ bàn phím")
        print("2. Đọc ciphertext từ file (cùng thư mục)")
        print("0. Thoát chương trình")
        print("-" * 55)
        
        choice = input("Vui lòng chọn (1/2/0): ").strip()

        if choice == '1':
            ciphertext = input("\nNhập bản mã: ").strip()
            if ciphertext:
                return ciphertext
            else:
                print(">> [Lỗi]: Bạn chưa nhập văn bản mã hóa. Vui lòng thử lại!\n")

        elif choice == '2':
            filename = input("\nNhập tên file (VD: cipher.txt): ").strip()
            current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
            file_path = os.path.join(current_dir, filename)

            if not os.path.isfile(file_path):
                file_path = filename

            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        ciphertext = f.read().strip()
                    if ciphertext:
                        print(f">> Đọc thành công file: {filename} ({len(ciphertext)} ký tự)")
                        return ciphertext
                    else:
                        print(">> [Lỗi]: File rỗng, vui lòng kiểm tra lại nội dung!\n")
                except Exception as e:
                    print(f">> [Lỗi khi đọc file]: {e}\n")
            else:
                print(f">> [Lỗi]: Không tìm thấy file '{filename}' trong thư mục hiện tại!\n")

        elif choice == '0':
            print("Đã thoát chương trình.")
            return None
        else:
            print(">> Lựa chọn không hợp lệ, vui lòng chọn lại (1, 2 hoặc 0)!\n")

def main():
    ciphertext = get_input_ciphertext()
    if not ciphertext:
        return

    print("\n" + "=" * 55)
    print(" ĐANG TIẾN HÀNH PHÂN TÍCH THỐNG KÊ...")
    print("=" * 55)

    key, plaintext, key_length, ic_scores = crack_vigenere(ciphertext)

    if not key:
        print(plaintext)
        return

    print("\n* BẢNG THỐNG KÊ INDEX OF COINCIDENCE (IoC) THEO ĐỘ DÀI KHÓA:")
    for k in range(1, min(16, len(ic_scores) + 1)):
        bar = "#" * int(ic_scores[k] * 200)
        marker = " <-- TỐI ƯU NHẤT" if k == key_length else ""
        print(f"  - Độ dài {k:2d}: IoC = {ic_scores[k]:.4f} | {bar}{marker}")

    print("\n* KẾT QUẢ PHÂN TÍCH:")
    print(f"  - Độ dài khóa dự đoán : {key_length}")
    print(f"  - Khóa tìm được        : {key}")

    print("\n* BẢN RÕ (PLAINTEXT) TƯƠNG ỨNG:\n")
    print("-" * 55)
    print(plaintext)
    print("-" * 55)

if __name__ == "__main__":
    main()