from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
from random import randrange

#created a person class so that we could mimic private/public access to the keys
class Person():
    def __init__(self, p, g):
        self.p = p
        self.g = g
        self.__pr = randrange(self.p)
        self.pu = pow(g, self.__pr, p)
        self.__secret = None

    #makes the shared secret
    def makeConnection(self, pub_key):
        sha = SHA256.new()
        sha.update(str(pow(pub_key, self.__pr, self.p)).encode())
        self.__secret = sha.digest()
    
    #encrypts a message
    def sendSecretMessage(self, m):
        cipher = AES.new(self.__secret[:16], AES.MODE_CBC, self.__secret[16:])
        ciphertext = cipher.encrypt(pad(m.encode(), 16))
        return ciphertext

    #decrypts a message
    def decryptSecretMessage(self, c):
        cipher = AES.new(self.__secret[:16], AES.MODE_CBC, self.__secret[16:])
        message = unpad(cipher.decrypt(c), 16)
        return message.decode()

#---------------------------------------------------------------------------------
#Task 1
#---------------------------------------------------------------------------------

#simple p and g (p = 37, g = 13)
alice = Person(37, 13)
bob = Person(37, 13)
bob.makeConnection(alice.pu)
alice.makeConnection(bob.pu)
print(bob.decryptSecretMessage(alice.sendSecretMessage("Hi Bob!")))
print(alice.decryptSecretMessage(bob.sendSecretMessage("Hi Alice!")))

#big p and g
pl = "B10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371"
gl ="A4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5"
alice = Person(int(pl, 16), int(gl, 16))
bob = Person(int(pl, 16), int(gl, 16))
bob.makeConnection(alice.pu)
alice.makeConnection(bob.pu)
print(bob.decryptSecretMessage(alice.sendSecretMessage("Hi Bob!")))
print(alice.decryptSecretMessage(bob.sendSecretMessage("Hi Alice!")))

#---------------------------------------------------------------------------------
#Task 2
#---------------------------------------------------------------------------------

alice = Person(37, 13)
bob = Person(37, 31)

#oh no! mallory messed with the public keys
bob.makeConnection(37)
alice.makeConnection(37)

print(bob.decryptSecretMessage(alice.sendSecretMessage("Hi Bob!")))
print(alice.decryptSecretMessage(bob.sendSecretMessage("Hi Alice!")))