from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import socket, os, base64

class SymmetricChannel:
  def __init__(self, socket: socket.socket, key) -> None:
      self.socket = socket
      self.key = key

  def send(self, data):
    iv = os.urandom(16)
    ct = self.encrypt(data, iv)
    self.socket.sendall(iv)
    self.socket.sendall(ct)
    print("IV")
    print(base64.b64encode(iv))

  def recv(self):
    iv = self.socket.recv(16) # size of IV
    ct = self.socket.recv(1024 ** 2)
    print("ct")
    print(base64.b64encode(ct))
    print("IV")
    print(base64.b64encode(iv))
    if ct == b'': # when connection ends receives empty message b''
      return ""
    else:
      data = self.decrypt(ct, iv)
      return data

  def encrypt(self, data, iv):
    cipher = Cipher(algorithms.AES256(self.key), modes.OFB(iv))
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()
  
  def decrypt(self, ct, iv):
    cipher = Cipher(algorithms.AES256(self.key), modes.OFB(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(ct) + decryptor.finalize()