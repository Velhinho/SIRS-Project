import socket, sys, json, base64, psycopg2
import asymmetric_channel as acm
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from asymmetric_channel import AsymmetricChannel
from secure_channel import SecureChannel

# Lab - A,  Hospital - B
# A sends encrypted(public_key_B, A)
# B sends encrypted(public_key_A, nounce)
# A sends encrypted(public_key_B, [nounce, session_key])
# A and B communicate using session key and TCP

HOST = "localhost"
PORT = 8080
key_file = sys.argv[1]
cert_file = sys.argv[2]

with open(key_file, "rb") as key_f, open(cert_file, "rb") as cert_f:
  cert = x509.load_pem_x509_certificate(cert_f.read())
  pub = cert.public_key()
  priv = serialization.load_pem_private_key(key_f.read(), password=None)

def verify(data, signature_str):
  signature_b64 = bytes(signature_str, "utf-8")
  signature = base64.b64decode(signature_b64)
  json_string = json.dumps(data)
  acm.verify(pub, signature, bytes(json_string, "utf-8"))

def send_to_db(data, signature_str):
	with psycopg2.connect("dbname=sirs user=velhinho") as conn, conn.cursor() as cur:
		cur.execute("INSERT INTO test_results VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", data + [signature_str])

def start_server():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("listening")
    s.listen()
    conn, addr = s.accept()
    with conn:
      print(f"Connected by {addr}")
      asy_channel = AsymmetricChannel(conn, pub, priv)
      secure_channel = SecureChannel(conn, asy_channel)
      secure_channel.recv_session_key()
      msg = secure_channel.recv()
      print(msg)
      verify(msg["data"], msg["signature"])
      send_to_db(msg["data"], msg["signature"])


start_server()