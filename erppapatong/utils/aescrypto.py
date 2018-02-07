import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

#PYTHON2
# BS = 16
# pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
# unpad = lambda s : s[0:-ord(s[-1])]
# PYTHON3
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-s[-1]]

class AESCrypto(object):
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode('utf-8')).digest()

    def on_encrypt(self, value):
        value = pad(value)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode( iv + cipher.encrypt( value ) ).decode("utf-8")

    def on_decrypt(self, value):
        value = base64.b64decode(value)
        iv = value[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt(value[16:])).decode("utf-8")

