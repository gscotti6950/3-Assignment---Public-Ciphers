from Crypto.Util.number import getPrime


p = getPrime(2048)
q = getPrime(2048)
n = p * q
e = 65537
euler_totient = (p - 1)(q - 1)
d = pow(e, -1, euler_totient)

pu = {e, n}
pr = {d, n}

