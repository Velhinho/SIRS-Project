import socket, sys, json, base64
import asymmetric_channel as acm
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from asymmetric_channel import AsymmetricChannel
from secure_channel import SecureChannel

HOST = "localhost"
PORT = 8080
key_file = sys.argv[1]
cert_file = sys.argv[2]

with open(key_file, "rb") as key_f, open(cert_file, "rb") as cert_f:
  cert = x509.load_pem_x509_certificate(cert_f.read())
  pub = cert.public_key()
  priv = serialization.load_pem_private_key(key_f.read(), password=None)

def sign(data):
  json_string = json.dumps(data)
  signature = acm.sign(priv, bytes(json_string, "utf-8"))
  signature_b64 = base64.b64encode(signature)
  signature_str = str(signature_b64, "utf-8")
  return signature_str

def start_client():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    asy_channel = AsymmetricChannel(s, pub, priv)
    secure_channel = SecureChannel(s, asy_channel)
    secure_channel.send_session_key()
    results = ["Velhinho", 1, 1, 1, 1, 1, 1]
    print({"data": results, "signature": sign(results)})
    secure_channel.send({"data": results, "signature": sign(results)})

start_client()