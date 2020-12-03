import random
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

BLOCK_SIZE = 16

def pad(s):
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

def unpad(s):
    return s[:-ord(s[len(s)-1:])]

def key_generator():
    k = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    key = hashlib.sha256(k.encode()).digest()
    with open("my_key", "wb") as file:
        file.write(key)

def get_key():
    with open("my_key", "rb") as file:
        key = file.read()
    return key

def encrypt(message, key):
    data = pad(message)
    iv = Random.new().read(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(data.encode("utf-8")))

def decrypt(encrypted, key):
    enc = base64.b64decode(encrypted)
    iv = enc[:BLOCK_SIZE]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[BLOCK_SIZE:])).decode("utf-8")
