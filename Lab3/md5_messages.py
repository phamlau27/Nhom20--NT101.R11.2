import hashlib

MSG1_HEX = (
    "d131dd02c5e6eec4693d9a0698aff95c"
    "2fcab58712467eab4004583eb8fb7f89"
    "55ad340609f4b30283e488832571415a"
    "085125e8f7cdc99fd91dbdf280373c5b"
    "d8823e3156348f5bae6dacd436c919c6"
    "dd53e2b487da03fd02396306d248cda0"
    "e99f33420f577ee8ce54b67080a80d1e"
    "c69821bcb6a8839396f9652b6ff72a70"
)

MSG2_HEX = (
    "d131dd02c5e6eec4693d9a0698aff95c"
    "2fcab50712467eab4004583eb8fb7f89"
    "55ad340609f4b30283e4888325f1415a"
    "085125e8f7cdc99fd91dbd7280373c5b"
    "d8823e3156348f5bae6dacd436c919c6"
    "dd53e23487da03fd02396306d248cda0"
    "e99f33420f577ee8ce54b67080280d1e"
    "c69821bcb6a8839396f965ab6ff72a70"
)

EXPECTED_MD5 = "79054025255fb1a26e4bc422aef54eb4"
EXPECTED_DIFF_POSITIONS = [19, 45, 59, 83, 109, 123]


def hex_to_bytes(hex_str: str) -> bytes:
    cleaned = hex_str.replace(" ", "").replace("\n", "")
    if len(cleaned) % 2 != 0:
        raise ValueError(f"Chuỗi HEX có độ dài lẻ: {len(cleaned)}")
    return bytes.fromhex(cleaned)


def find_diff_positions(b1: bytes, b2: bytes) -> list[int]:
    if len(b1) != len(b2):
        raise ValueError("Hai thông điệp có độ dài khác nhau, không thể so sánh từng vị trí.")
    return [i for i in range(len(b1)) if b1[i] != b2[i]]


def compute_md5(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def print_separator(char: str = "─", width: int = 60):
    print(char * width)


def main():
    print_separator("═")
    print("  CÂU 1 – MD5 COLLISION TRÊN HAI THÔNG ĐIỆP HEX")
    print_separator("═")

    msg1 = hex_to_bytes(MSG1_HEX)
    msg2 = hex_to_bytes(MSG2_HEX)

    print(f"\n[1] Độ dài thông điệp")
    print(f"    Message 1 : {len(msg1)} bytes")
    print(f"    Message 2 : {len(msg2)} bytes")

    diff_positions = find_diff_positions(msg1, msg2)
    print(f"\n[2] So sánh nội dung")
    print(f"    Số byte khác nhau : {len(diff_positions)}")
    print(f"    Vị trí khác nhau  : {diff_positions}")

    print(f"\n[3] Chi tiết các byte khác nhau")
    print(f"    {'Vị trí':>8}  {'MSG1 (hex)':>10}  {'MSG2 (hex)':>10}  {'MSG1 (dec)':>10}  {'MSG2 (dec)':>10}")
    print_separator()
    for pos in diff_positions:
        print(f"    {pos:>8}  {msg1[pos]:>10x}  {msg2[pos]:>10x}  {msg1[pos]:>10}  {msg2[pos]:>10}")

    md5_msg1 = compute_md5(msg1)
    md5_msg2 = compute_md5(msg2)

    print(f"\n[4] Giá trị MD5")
    print(f"    MD5(Message 1) : {md5_msg1}")
    print(f"    MD5(Message 2) : {md5_msg2}")

    print(f"\n[5] Kiểm tra collision")
    collision_ok = md5_msg1 == md5_msg2
    match_expected = md5_msg1 == EXPECTED_MD5
    diff_ok = msg1 != msg2

    print(f"    Hai thông điệp khác nhau : {'✔ ĐÚNG' if diff_ok else '✘ SAI'}")
    print(f"    MD5 của hai thông điệp bằng nhau : {'✔ ĐÚNG' if collision_ok else '✘ SAI'}")
    print(f"    MD5 khớp giá trị chuẩn ({EXPECTED_MD5}) : {'✔ ĐÚNG' if match_expected else '✘ SAI'}")
    print(f"    Vị trí khác khớp chuẩn {EXPECTED_DIFF_POSITIONS} : {'✔ ĐÚNG' if diff_positions == EXPECTED_DIFF_POSITIONS else '✘ SAI'}")

    print(f"\n[KẾT LUẬN]")
    if collision_ok and diff_ok:
        print("    MD5 COLLISION xác nhận thành công.")
        print("    Hai thông điệp hoàn toàn khác nhau nhưng tạo ra cùng một giá trị MD5.")
        print("    Điều này chứng minh MD5 không còn an toàn cho mục đích xác thực toàn vẹn.")
    else:
        print("    Không phát hiện collision – kiểm tra lại dữ liệu đầu vào.")

    print_separator("═")


if __name__ == "__main__":
    main()
