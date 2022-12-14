import socket, sys, json, base64, psycopg2, tabulate
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
PORT = 8081
key_file = sys.argv[1]
cert_file = sys.argv[2]
dbname = "sirs"
user = "postgres"
password = "postgres"

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
	with psycopg2.connect(dbname=dbname, user=user, password=password, host=HOST) as conn, conn.cursor() as cur:
	  cur.execute("INSERT INTO test_results VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", data + [signature_str])

def show_table():
  with psycopg2.connect(dbname=dbname, user=user, password=password, host=HOST) as conn:
    with conn.cursor() as cur:
      cur.execute("SELECT * FROM test_results")
      values = cur.fetchall()
      values = [list(value) for value in values]
      for value in values:
        value[len(value) - 1] = value[len(value) - 1][0:10] + "..."
      print(tabulate.tabulate(values, headers=["Name", "Age", "Hemogoblin", "Red Blood Cells", "White Blood Cells", "Platelets", "Neutrophils", "Signature"]))

def test_authenticity():
  with psycopg2.connect(dbname=dbname, user=user, password=password, host=HOST) as conn:
    with conn.cursor() as cur:
      cur.execute("SELECT * FROM test_results")
      values = cur.fetchall()
      for i, value in enumerate(values):
        signature_str = value[len(value) - 1]
        fields = [str(field) for field in value[: len(value) - 1]]
        print("fields " + str(fields))
        print("Authenticating row " + str(i))
        verify(fields, signature_str)
        print("Authenticity confirmed for row " + str(i))

def start_server():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("listening")
    s.listen()
    while True:
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
        show_table()
      if input("continue to receive requests? [y/n]") == "n":
        test_authenticity()
        break

start_server()