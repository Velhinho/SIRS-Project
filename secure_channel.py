import base64, os
from cryptography.fernet import Fernet
from json_channel import JsonChannel
from symmetric_channel import SymmetricChannel

class SecureChannel:
  def __init__(self, socket, asymmetric_channel) -> None:
    self.socket = socket
    self.asymmetric_channel = asymmetric_channel
    self.symmetric_channel = None

  def send(self, data):
    if self.symmetric_channel == None:
      raise ValueError("session key not yet established")
    json_channel = JsonChannel(self.symmetric_channel)
    json_channel.send(data)

  def recv(self):
    if self.symmetric_channel == None:
      raise ValueError("session key not yet established")
    json_channel = JsonChannel(self.symmetric_channel)
    data = json_channel.recv()
    return data

  def send_session_key(self):    
    """ 
    Lab - A,  Hospital - B
    A sends encrypted(public_key_B, A)
    B sends encrypted(public_key_A, nounce)
    A sends encrypted(public_key_B, [nounce, session_key])
    A and B communicate using session key, symmetric encryption and TCP 
    """
    json_channel = JsonChannel(self.asymmetric_channel)
    print("Starting session")
    json_channel.send("Lab")
    nounce = json_channel.recv()
    print("Nounce: " + nounce)
    session_key = base64_encode_str(Fernet.generate_key())
    print("Sending session key")
    json_channel.send([nounce, session_key])
    self.symmetric_channel = SymmetricChannel(socket=self.socket, key=base64.b64decode(session_key))

  def recv_session_key(self):
    json_channel = JsonChannel(self.asymmetric_channel)
    lab_name = json_channel.recv()
    print("Starting session with: " + lab_name)
    nounce = base64_encode_str(os.urandom(16))
    print("Nounce: " + nounce)
    json_channel.send(nounce)
    recv_nounce, session_key = json_channel.recv()
    if recv_nounce != nounce:
      raise ValueError("Wrong nounce")
    print("Correct Nounce")
    print("Received session key:" + session_key)
    self.symmetric_channel = SymmetricChannel(socket=self.socket, key=base64.b64decode(session_key))
  
def base64_encode_str(data):
  return str(base64.b64encode(data), "utf-8")

def base64_decode_str(data_str):
  return base64.b64decode(bytes(data_str, "utf-8"))