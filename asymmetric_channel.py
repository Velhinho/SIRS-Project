from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class AsymmetricChannel:
  def __init__(self, socket, pub_encrypt_key, priv_decrypt_key) -> None:
    self.socket = socket
    self.pub_encrypt_key = pub_encrypt_key
    self.priv_decrypt_key = priv_decrypt_key

  def send(self, data):
    ct = encrypt(self.pub_encrypt_key, data)
    self.socket.sendall(ct)

  def recv(self):
    ct = self.socket.recv(1024)
    if ct == b'':
      return ""
    else:
      pt = decrypt(self.priv_decrypt_key, ct)
      return pt

def encrypt(public_key, data):
  return public_key.encrypt(
    data,
    padding.OAEP(
      mgf=padding.MGF1(algorithm=hashes.SHA256()),
      algorithm=hashes.SHA256(),
      label=None
    )
  )

def decrypt(private_key, data):
  return private_key.decrypt(
    data,
    padding.OAEP(
      mgf=padding.MGF1(algorithm=hashes.SHA256()),
      algorithm=hashes.SHA256(),
      label=None
    )
  )

def sign(private_key, data):
  return private_key.sign(
    data,
    padding.PSS(
      mgf=padding.MGF1(hashes.SHA256()),
      salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
  )

def verify(public_key, signature, data):
  public_key.verify(
    signature,
    data,
    padding.PSS(
      mgf=padding.MGF1(hashes.SHA256()),
      salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
  )