import hashlib
import urllib.request
import urllib.error
from pathlib import Path

SAMPLES_DIR = Path(__file__).parent / "samples"

PDF1_URL = "https://raw.githubusercontent.com/cr-marcstevens/sha1collisiondetection/master/test/shattered-1.pdf"
PDF2_URL = "https://raw.githubusercontent.com/cr-marcstevens/sha1collisiondetection/master/test/shattered-2.pdf"

PDF1_PATH = SAMPLES_DIR / "shattered-1.pdf"
PDF2_PATH = SAMPLES_DIR / "shattered-2.pdf"

EXPECTED_SHA1 = "38762cf7f55934b34d179ae6a4c80cadccbb7f0a"
PDF_MAGIC = b"%PDF"


def download_file(url: str, dest: Path) -> None:
    print(f"  Đang tải: {url}")
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read()
        dest.write_bytes(data)
        print(f"  Đã lưu : {dest} ({len(data):,} bytes)")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Không thể tải {url}: {e}") from e


def validate_pdf(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"File không tồn tại: {path}")
    if path.stat().st_size == 0:
        raise ValueError(f"File rỗng: {path}")
    header = path.read_bytes()[:4]
    if header != PDF_MAGIC:
        raise ValueError(
            f"File không phải định dạng PDF hợp lệ. "
            f"Magic bytes nhận được: {header!r}, cần: {PDF_MAGIC!r}"
        )


def compute_hash(data: bytes, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    h.update(data)
    return h.hexdigest()


def print_separator(char: str = "─", width: int = 60):
    print(char * width)


def download_samples() -> None:
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    print("\n[BƯỚC 1] Tải file PDF về thư mục samples/")
    print_separator()
    download_file(PDF1_URL, PDF1_PATH)
    download_file(PDF2_URL, PDF2_PATH)


def analyze_pdfs() -> None:
    print("\n[BƯỚC 2] Kiểm tra định dạng PDF")
    print_separator()
    for path in (PDF1_PATH, PDF2_PATH):
        validate_pdf(path)
        print(f"  ✔ {path.name}: định dạng PDF hợp lệ ({path.stat().st_size:,} bytes)")

    print("\n[BƯỚC 3] Kích thước và so sánh nội dung nhị phân")
    print_separator()
    data1 = PDF1_PATH.read_bytes()
    data2 = PDF2_PATH.read_bytes()
    print(f"  shattered-1.pdf : {len(data1):,} bytes")
    print(f"  shattered-2.pdf : {len(data2):,} bytes")

    if data1 == data2:
        print("  Hai file có nội dung GIỐNG NHAU.")
    else:
        if len(data1) == len(data2):
            diff_count = sum(1 for a, b in zip(data1, data2) if a != b)
            print(f"  Hai file có nội dung KHÁC NHAU.")
            print(f"  Số byte khác nhau : {diff_count:,} / {len(data1):,}")
        else:
            print(f"  Hai file có nội dung KHÁC NHAU (kích thước khác nhau).")

    print("\n[BƯỚC 4] Tính SHA-1 và SHA-256")
    print_separator()
    sha1_pdf1 = compute_hash(data1, "sha1")
    sha1_pdf2 = compute_hash(data2, "sha1")
    sha256_pdf1 = compute_hash(data1, "sha256")
    sha256_pdf2 = compute_hash(data2, "sha256")

    print(f"  SHA-1  (shattered-1.pdf) : {sha1_pdf1}")
    print(f"  SHA-1  (shattered-2.pdf) : {sha1_pdf2}")
    print()
    print(f"  SHA-256 (shattered-1.pdf) : {sha256_pdf1}")
    print(f"  SHA-256 (shattered-2.pdf) : {sha256_pdf2}")

    print("\n[BƯỚC 5] Kiểm tra SHA-1 Collision")
    print_separator()
    sha1_match = sha1_pdf1 == sha1_pdf2
    sha1_expected_ok = sha1_pdf1 == EXPECTED_SHA1
    print(f"  SHA-1 chuẩn         : {EXPECTED_SHA1}")
    print(f"  SHA-1 hai file bằng nhau : {'✔ ĐÚNG' if sha1_match else '✘ SAI'}")
    print(f"  SHA-1 khớp giá trị chuẩn : {'✔ ĐÚNG' if sha1_expected_ok else '✘ SAI'}")

    print("\n[BƯỚC 6] So sánh SHA-256 để chứng minh hai file khác nhau")
    print_separator()
    sha256_match = sha256_pdf1 == sha256_pdf2
    content_diff = data1 != data2
    print(f"  SHA-256 hai file bằng nhau : {'✔ ĐÚNG' if sha256_match else '✘ SAI (hai file khác nhau)'}")
    print(f"  Nội dung nhị phân khác nhau : {'✔ ĐÚNG' if content_diff else '✘ SAI'}")

    print("\n[KẾT LUẬN]")
    print_separator()
    if sha1_match and content_diff and not sha256_match:
        print("  SHA-1 COLLISION xác nhận thành công trên hai file PDF.")
        print()
        print("  shattered-1.pdf và shattered-2.pdf:")
        print("    • Nội dung KHÁC NHAU (SHA-256 khác nhau)")
        print("    • Nhưng cho ra cùng giá trị SHA-1")
        print()
        print("  Đây là bằng chứng thực nghiệm từ nghiên cứu SHAttered (2017)")
        print("  của Google và CWI Amsterdam, chứng minh SHA-1 đã bị phá vỡ.")
        print("  SHA-256 vẫn phân biệt được hai file, chứng tỏ SHA-256 an toàn hơn.")
    else:
        print("  Kết quả không như mong đợi – kiểm tra lại quá trình tải file.")


def main():
    print_separator("═")
    print("  CÂU 3 – SHA-1 COLLISION TRÊN HAI FILE PDF")
    print_separator("═")
    download_samples()
    analyze_pdfs()
    print_separator("═")


if __name__ == "__main__":
    main()
