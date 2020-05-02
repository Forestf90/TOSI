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

    e = random.randrange(phi/8, phi)

    while math.gcd(e, phi) != 1:
        e = random.randrange(phi/8, phi)

    d = pow(e, -1, phi)
    return [[e, n], [d, n]]


def string_to_bit(n):
    result = [int(digit) for digit in bin(n)[2:]]

    for i in range(8 - len(result)):
        result = [0] + result
    return result


def bit_to_string(bits):
    bit_string = ""

    for bit in bits:
        bit_string += str(bit)
    str_data = ''

    for i in range(0, len(bit_string), 8):
        temp_data = bit_string[i:i + 8]
        decimal_data = int(temp_data, 2)
        str_data = str_data + chr(decimal_data)

    return str_data


def encrypt(message, key):
    return pow(message, key[0], key[1])


def main():

    message = input("Text message to encrypt: ")
    print()
    massage_bits = []
    for ch in message:
        massage_bits.extend(string_to_bit(ord(ch)))

    keys = generate_key()
    public_key = keys[0]
    private_key = keys[1]
    encrypted_massage = encrypt(massage_bits, public_key)
    print("Encrypted message: ")
    print(bit_to_string(encrypted_massage))
    encrypted_massage = encrypt(encrypted_massage, private_key)
    print("Decrypted message: ")
    print(bit_to_string(encrypted_massage))


if __name__ == "__main__":
    main()
