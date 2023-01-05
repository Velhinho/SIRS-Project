from cryptography.fernet import Fernet
import socket

class SymmetricChannel:
  def __init__(self, socket: socket.socket, key) -> None:
      self.socket = socket
      self.key = key

  def send(self, data):
    fernet = Fernet(self.key)
    ct = fernet.encrypt(data)
    self.socket.sendall(ct)

  def recv(self):
    ct = self.socket.recv(1024 ** 2)
    if ct == b'':
      return ""
    else:
      fernet = Fernet(self.key)
      data = fernet.decrypt(ct)
      return data