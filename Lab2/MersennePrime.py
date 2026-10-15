import random
import secrets
 
SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
 

def mod_pow(a, x, p):
    """Tinh a^x mod p, dung tinh chat (a*b) mod n = ((a mod n)*(b mod n)) mod n"""
    result = 1
    a %= p
    while x > 0:
        if x & 1:                    
            result = (result * a) % p
        a = (a * a) % p             
        x >>= 1
    return result
 

def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)
 
 
def is_prime(n, rounds=40):
    if n < 2:
        return False
    for p in SMALL_PRIMES:
        if n == p:
            return True
        if n % p == 0:
            return False
    d, s = n - 1, 0
    while d % 2 == 0:              
        d //= 2
        s += 1
 
    bases = SMALL_PRIMES[:12] + [random.randrange(2, n - 1) for _ in range(rounds)]
    for a in bases:
        a %= n
        if a < 2:
            continue
        x = mod_pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False             
    return True                      
 
 
def random_prime(bits):
    while True:
        n = secrets.randbits(bits) | (1 << (bits - 1)) | 1   
        if is_prime(n):
            return n
 
 
if __name__ == "__main__":
    print("=== 1a. So nguyen to ngau nhien ===")
    for b in (8, 16, 64):
        p = random_prime(b)
        print(f"{b:>2} bit: {p}  (bit_length = {p.bit_length()})")
 
    print("\n=== 1b. 10 so nguyen to lon nhat < M10 = 2^89 - 1 ===")
    M10 = 2**89 - 1
    print("M10 la so nguyen to?", "Dung" if is_prime(M10) else "Sai", "| M10 =", M10)
    found, n = [], M10 - 1
    while len(found) < 10:
        if is_prime(n):
            found.append(n)
        n -= 1
    for i, p in enumerate(found, 1):
        print(f"{i:>2}. {p}   (M10 - {M10 - p})")
 
    print("\n=== 1c. Kiem tra nguyen to ===")
    tests = [97, 561, 1_000_000_007, 2**61 - 1, 2**64 + 1, 2**88 + 1, found[0], found[0] + 2, 2**89 - 1]
    for t in tests:
        print(f"{t} -> {'NGUYEN TO' if is_prime(t) else 'HOP SO'}")
    try:
        s = input("\nNhap mot so nguyen < 2^89 - 1 (Enter de bo qua): ").strip()
        if s:
            v = int(s)
            if v >= M10:
                print("So nhap phai nho hon 2^89 - 1")
            else:
                print("-> NGUYEN TO" if is_prime(v) else "-> HOP SO")
    except EOFError:
        pass
 
    print("\n=== 2. GCD ===")
    g = secrets.randbits(512) | 1
    a = g * secrets.randbits(2048)
    b = g * secrets.randbits(2048)
    print(f"a: {a.bit_length()} bit, b: {b.bit_length()} bit")
    r = gcd(a, b)
    print("gcd(a, b) bit_length =", r.bit_length(), "| chia het cho g:", "Dung" if r % g == 0 else "Sai")
    print("gcd(48, 18) =", gcd(48, 18), "| gcd(2^127-1, 2^89-1) =", gcd(2**127 - 1, 2**89 - 1))
 
    print("\n=== 3. a^x mod p ===")
    print("7^40 mod 19 =", mod_pow(7, 40, 19), "| kiem tra pow():", pow(7, 40, 19))
    big_a, big_x, big_p = secrets.randbits(256), secrets.randbits(1024), random_prime(256)
    print("So lon khop voi pow():", "Dung" if mod_pow(big_a, big_x, big_p) == pow(big_a, big_x, big_p) else "Sai")