import math
class Encryption():
    def __init__(self,d,n,e):
        self.d = d
        self.n = n
        self.e = e

    def decrypt(self, cipher_text):
        encoded_text = [pow(c,self.d,self.n) for c in cipher_text]
        print(encoded_text)
        message = "".join(chr(c) for c in encoded_text)
        return message
        
    def encrypt(self, message):
        encoded_text = [ord(c) for c in message]
        print(encoded_text)
        cipher_text = [pow(c,self.e,self.n) for c in encoded_text]
        return cipher_text