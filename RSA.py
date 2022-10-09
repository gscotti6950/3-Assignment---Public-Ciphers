from Crypto.Util.number import getPrime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256

#---------------------------------------------------------------------
#Task 3-1
#---------------------------------------------------------------------
p = getPrime(2048)
q = getPrime(2048)
n = p * q
e = 65537
euler_totient = (p - 1)*(q - 1)
d = pow(e, -1, euler_totient)

#let's say these are Alice's keys
pu = {e, n}
pr = {d, n}

#---------------------------------------------------------------------
#Task 3-2
#---------------------------------------------------------------------
message = "please work"
m0 = int(message.encode().hex(), 16)

#Bob encrypts the message with Alice's public key
ciphertext = pow(m0, e, n)

#Alice decrypts the message with her private key
m1 = pow(ciphertext, d, n)
print(bytes.fromhex(hex(m1)[2:]).decode())

#Uh oh! Mallory messed with Bob's message
c_prime = pow(ciphertext, e, n)

#Alice decrypts the modified ciphertext from Mallory
s = pow(c_prime, d, n)
assert s == ciphertext
#Now Mallory knows the key (the ciphertext sent by Bob)

temp = str(s).encode()
sha = SHA256.new()
sha.update(temp)
k = sha.digest()

cipher1 = AES.new(k[:16], AES.MODE_CBC, k[16:])
cipher2 = AES.new(k[:16], AES.MODE_CBC, k[16:])

#Alice encrypts a message
temp = cipher1.encrypt(pad(b"secret message", 16))

#Mallory knows the key and is able to decrypt it
print(unpad(cipher2.decrypt(temp), 16))


