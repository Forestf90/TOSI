from Crypto.Util import number
import random
import math

def generate_key():
    p_length = random.randrange(512, 2048-512, 8)
    q_length = 2048 - p_length
    p = number.getPrime(p_length)
    q = number.getPrime(q_length)
    while p == q:
        q = number.getPrime(q_length)

    n = p * q
    phi = (p-1)*(q-1)

    e = random.randrange(phi//8, phi)

    while math.gcd(e, phi) != 1:
        e = random.randrange(phi//8, phi)

    d = number.inverse(e, phi)
    return [[e, n], [d, n]]


def encrypt(message, key):
    cipher = []
    for char in message:
        cipher.append(pow(ord(char), key[0], key[1]))

    return cipher

def decrypt(message, key):
    encrypted = []
    for char in message:
        encrypted.append(chr(pow(char, key[0], key[1])))

    return ''.join(encrypted)


def main():

    massage = input("Text message to encrypt: ")
    print()

    keys = generate_key()
    public_key = keys[0]
    private_key = keys[1]
    encrypted_massage = encrypt(massage, public_key)
    print("Encrypted message: ")
    print(''.join(map(lambda x: str(x), encrypted_massage)))


    encrypted_massage = decrypt(encrypted_massage, private_key)
    print("Decrypted message: ")
    print(encrypted_massage)


if __name__ == "__main__":
    main()
