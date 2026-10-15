"""
Lab 02 - Nhiem vu 2.4: SEED Lab - Error Propagation AES-128
Mon: An toan mang may tinh | Nhom 20
"""
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

BLOCK        = 16
DATA_LEN     = 1000
CORRUPT_BYTE = 25   # byte thu 26 (index 25)


def flip_bit(data, idx):
    b = bytearray(data)
    b[idx] ^= 1
    return bytes(b)


def diff_blocks(orig, recv):
    n = min(len(orig), len(recv)) // BLOCK
    return sum(orig[i*BLOCK:(i+1)*BLOCK] != recv[i*BLOCK:(i+1)*BLOCK] for i in range(n))


def run(mode_name, data, key, iv):
    if   mode_name == "ECB": enc = AES.new(key, AES.MODE_ECB)
    elif mode_name == "CBC": enc = AES.new(key, AES.MODE_CBC, iv)
    elif mode_name == "CFB": enc = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
    elif mode_name == "OFB": enc = AES.new(key, AES.MODE_OFB, iv)

    ct = enc.encrypt(pad(data, BLOCK) if mode_name in ("ECB","CBC") else data)
    ct_bad = flip_bit(ct, CORRUPT_BYTE)

    if   mode_name == "ECB": pt = AES.new(key, AES.MODE_ECB).decrypt(ct_bad)[:DATA_LEN]
    elif mode_name == "CBC": pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct_bad)[:DATA_LEN]
    elif mode_name == "CFB": pt = AES.new(key, AES.MODE_CFB, iv, segment_size=128).decrypt(ct_bad)
    elif mode_name == "OFB": pt = AES.new(key, AES.MODE_OFB, iv).decrypt(ct_bad)

    bad_bytes = sum(a != b for a, b in zip(data, pt))
    bad_blocks = diff_blocks(data, pt)
    total_blocks = (DATA_LEN + BLOCK - 1) // BLOCK
    print(f"  {mode_name}: {bad_blocks}/{total_blocks} khoi hong  |  {bad_bytes} byte hong")


def main():
    print("Nhiem vu 2.4: Error Propagation AES-128")
    print(f"  Du lieu: {DATA_LEN} byte  |  Lam hong: byte {CORRUPT_BYTE+1}  |  Khoi loi: {CORRUPT_BYTE//BLOCK+1}")

    data = bytes(i % 256 for i in range(DATA_LEN))
    key  = os.urandom(16)
    iv   = os.urandom(16)

    for mode in ["ECB", "CBC", "CFB", "OFB"]:
        run(mode, data, key, iv)


if __name__ == "__main__":
    main()
