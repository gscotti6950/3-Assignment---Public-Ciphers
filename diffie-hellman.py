from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
from random import randrange

#created a person class so that we could mimic private and
#access to the keys
class Person():
    def __init__(self, name, p, g):
        self.name = name
        self.p = p
        self.g = g
        self.__pr = randrange(self.p)
        self.pu = pow(g, self.__pr, p)
        self.__secret = None

    def makeConnection(self, bob):
        sha = SHA256.new()
        sha.update(str(pow(bob.pu, self.__pr, self.p)).encode())
        self.__secret = sha.digest()

    def sendPG(self):
        return (self.p, self.g)
    
    def sendSecretMessage(self, m):
        cipher = AES.new(self.__secret[:16], AES.MODE_CBC, self.__secret[16:])
        ciphertext = cipher.encrypt(pad(m.encode(), 16))
        return ciphertext

    def decryptSecretMessage(self, c):
        cipher = AES.new(self.__secret[:16], AES.MODE_CBC, self.__secret[16:])
        message = unpad(cipher.decrypt(c), 16)
        return message.decode()

alice = Person("Alice", 37, 13)
bob = Person("Bob", alice.sendPG()[0], alice.sendPG()[1])
alice.makeConnection(bob)
bob.makeConnection(alice)
print(bob.decryptSecretMessage(alice.sendSecretMessage("Hi Bob!")))
print(alice.decryptSecretMessage(bob.sendSecretMessage("Hi Alice!")))



        

# def Diffie_Hellman(p, g):
#     #make p and g
#     # p = 37
#     # g = 13

#     #generate public keys (A = g^a mod p, B = g^b mod p, A and B )
#     a = randrange(p)
#     b = randrange(p)
#     A = pow(g, a, p)
#     B = pow(g, b, p)

#     #generate shared secrets (s = B^a mod p and A^b mod p) 
#     bob_secret = pow(A, b, p)
#     alice_secret = pow(B, a, p)

#     assert bob_secret == alice_secret, "shared secret not the same"

#     #k = SHA256(s)
#     sha1 = SHA256.new()
#     sha2 = SHA256.new()
#     sha1.update(str(alice_secret).encode())
#     sha2.update(str(bob_secret).encode())
#     assert sha1.hexdigest() == sha2.hexdigest(), "key not the same"
#     assert sha1.digest() == sha2.digest()

#     #Encrypt Alice's message to Bob
#     m0 = "Hi Bob!"
#     cipherA = AES.new(sha1.digest()[:16], AES.MODE_CBC, sha1.digest()[16:])
#     c0 = cipherA.encrypt(pad(m0.encode(), 16))
#     print("Alice's encrypted message: ")
#     print(c0)

#     #Encrypt Bob's message to Alice
#     m1 = "Hi Alice!"
#     cipherB = AES.new(sha2.digest()[:16], AES.MODE_CBC, sha2.digest()[16:])
#     c1 = cipherB.encrypt(pad(m1.encode(), 16))
#     print("Bob's encrypted message: ")
#     print(c1)

#     #Alice Decrypts Bob's message
#     decryptA = AES.new(sha1.digest()[:16], AES.MODE_CBC, sha1.digest()[16:])
#     temp = unpad(decryptA.decrypt(c1), 16)
#     assert temp == m1.encode(), "message not the same"
#     print("Bob's decrypted message: ")
#     print(temp.decode())

#     # #Bob Decrypts Alice's message
#     decryptB = AES.new(sha2.digest()[:16], AES.MODE_CBC, sha2.digest()[16:])
#     temp = unpad(decryptB.decrypt(c0), 16)
#     assert temp == m0.encode(), "message not the same"
#     print("Alice's decrypted message: ")
#     print(temp.decode())

# Diffie_Hellman(37, 13)
# pl = "B10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371"
# gl ="A4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5"

# Diffie_Hellman(int(pl,16), int(gl, 16))
