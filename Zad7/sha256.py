H = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
     0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
     0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
     0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
     0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
     0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
     0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
     0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
     0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
     0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
     0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
     0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
     0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
     0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

import struct


def rightRotate(n, d):
    return (n >> d) | (n << (32 - d)) & 0xFFFFFFFF


def sig0(n):
    return (rightRotate(n, 7) ^ rightRotate(n, 18) ^ (n >> 3))


def sig1(n):
    return (rightRotate(n, 17) ^ rightRotate(n, 19) ^ (n >> 10))


def eps0(x):
    return rightRotate(x, 2) ^ rightRotate(x, 13) ^ rightRotate(x, 22)


def eps1(x):
    return rightRotate(x, 6) ^ rightRotate(x, 11) ^ rightRotate(x, 25)


def maj_f(a, b, c):
    return (a & b) ^ (a & c) ^ (b & c)


def ch_f(e, f, g):
    return (e & f) ^ ((0xFFFFFFFF ^ e) & g)


def padding(massage):
    l = len(massage)
    temp = bytes(massage.encode()) + bytes.fromhex("80")

    padding = 64 - ((l + 1 + 8) % 64)

    temp += padding * bytes.fromhex("00")
    temp += (l * 8).to_bytes(8, byteorder="big")

    return temp


def hash(blocks):
    for i in blocks:
        a = H[0]
        b = H[1]
        c = H[2]
        d = H[3]
        e = H[4]
        f = H[5]
        g = H[6]
        h = H[7]
        W = []

        for j in range(16):
            W.append(bytes(i[j * 4:(j + 1) * 4]))
        for j in range(16, 64):
            value = (sig1(int.from_bytes(W[j - 2], "big")) +
                     int.from_bytes(W[j - 7], "big") +
                     sig0(int.from_bytes(W[j - 15], "big"))
                     + int.from_bytes(W[j - 16], "big")) & 0xFFFFFFFF
            W.append(value.to_bytes(4, "big"))

        for j in range(64):
            ch = ch_f(e, f, g)
            maj = maj_f(a, b, c)
            e0 = eps0(a)
            e1 = eps1(e)

            T1 = (h + e1 + ch + K[j] + int.from_bytes(W[j], "big")) & 0xFFFFFFFF
            T2 = (e0 + maj) & 0xFFFFFFFF
            h = g
            g = f
            f = e
            e = (d + T1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (T1 + T2) & 0xFFFFFFFF

        H[0] = (a + H[0]) & 0xFFFFFFFF
        H[1] = (b + H[1]) & 0xFFFFFFFF
        H[2] = (c + H[2]) & 0xFFFFFFFF
        H[3] = (d + H[3]) & 0xFFFFFFFF
        H[4] = (e + H[4]) & 0xFFFFFFFF
        H[5] = (f + H[5]) & 0xFFFFFFFF
        H[6] = (g + H[6]) & 0xFFFFFFFF
        H[7] = (h + H[7]) & 0xFFFFFFFF


    result = ""
    for xd in H:
        result += xd.to_bytes(4, byteorder="big").hex()

    return result


def main():
    massage = input("Text message to hash: ")
    print()
    byte_massage = padding(massage)
    blocks = []

    for i in range(0, len(byte_massage), 64):
        blocks.append(byte_massage[i:i + 64])

    result = hash(blocks)
    print(result)


if __name__ == "__main__":
    main()
