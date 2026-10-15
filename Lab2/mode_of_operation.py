from Crypto.Cipher import AES

key = b'1234567890123456'
iv  = b'0000000000000000'  # IV cố định theo đề bài
plaintext = b"UIT_LAB_UIT_LAB_UIT_LAB_UIT_LAB_"  # 32 byte = 2 khối

def show(name, ct):
    b = [ct[i:i+16].hex() for i in range(0, len(ct), 16)]
    print(f"{name}: {ct.hex()}")
    for i, x in enumerate(b): print(f"   Khối {i+1}: {x}")
    print("   Hai khối giống nhau?", b[0] == b[1])

show("ECB", AES.new(key, AES.MODE_ECB).encrypt(plaintext))
show("CBC", AES.new(key, AES.MODE_CBC, iv).encrypt(plaintext))
show("CFB", AES.new(key, AES.MODE_CFB, iv, segment_size=128).encrypt(plaintext))
show("OFB", AES.new(key, AES.MODE_OFB, iv).encrypt(plaintext))
show("CTR", AES.new(key, AES.MODE_CTR, nonce=b'12345678').encrypt(plaintext))