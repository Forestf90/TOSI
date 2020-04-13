from Crypto.Util import number


def generate_key(m_size):
    n_length = 512
    key = []
    p = number.getPrime(n_length)
    while p % 4 != 3:
        p = number.getPrime(n_length)
    q = number.getPrime(n_length)
    while p == q or q % 4 != 3:
        q = number.getPrime(n_length)

    n = p * q
    seed = number.getRandomRange(n//8, n)

    x0 = (seed*seed) % n
    x = [x0]
    for i in range(1, m_size+1):
        xi = (x[i-1] * x[i-1]) % n
        key.append(xi % 2)
        x.append(xi)

    return key


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
    encrypted_massage = []

    for i, k in zip(message, key):
        encrypted_massage.append(i ^ k)

    return encrypted_massage


def main():

    message = input("Text message to encrypt: ")
    print()
    massage_bits = []
    for ch in message:
        massage_bits.extend(string_to_bit(ord(ch)))

    key = generate_key(len(massage_bits))
    encrypted_massage = encrypt(massage_bits, key)
    print("Encrypted message: ")
    print(bit_to_string(encrypted_massage))
    encrypted_massage = encrypt(encrypted_massage, key)
    print("Decrypted message: ")
    print(bit_to_string(encrypted_massage))


if __name__ == "__main__":
    main()


