from flask import Flask, request
from sshtunnel import SSHTunnelForwarder
import psycopg2

app = Flask(__name__)
username = "postgres"
password = "postgres"
dbname = "sirs"

def db_connect():
# We were unable to run using SSH
	# ssh_tunnel = SSHTunnelForwarder(
	# 	"localhost",
	# 	ssh_username=username,
	# 	ssh_pkey="hospital_key.pem",
	# 	ssh_private_key_password= "~/.ssh/id_rsa.pub",
	# 	remote_bind_address=("localhost", 5432)
	# 	)
	# ssh_tunnel.start()
	# return psycopg2.connect(host="localhost", port=ssh_tunnel.local_bind_port, user=username, database=dbname)
	return psycopg2.connect(user=username, password=password, database=dbname, host="localhost")

@app.route("/create", methods=["POST"])
def create_appointment():
	with db_connect() as conn, conn.cursor() as cur:
		payload = request.get_json()
		name = payload["name"]
		specialty = payload["specialty"]
		doctor = payload["doctor"]
		starting_time = payload["time"]
		values = (name, specialty, doctor, starting_time)
		print(values)
		cur.execute("INSERT INTO appointments VALUES (%s, %s, %s, %s)", values)
		return "ok"

@app.route("/read", methods=["GET"])
def read_appointment():
	with db_connect() as conn, conn.cursor() as cur:
		payload = request.get_json()
		name = payload["name"]
		cur.execute("SELECT * FROM appointments WHERE name = (%s)", [name])
		values = cur.fetchall()
		print(values)
		return values

@app.route("/update", methods=["PUT"])
def update_appointment():
	pass

@app.route("/delete", methods=["DELETE"])
def delete_appointment():
	pass

@app.route("/test_results", methods=["GET"])
def read_test_results():
	with db_connect() as conn, conn.cursor() as cur:
		payload = request.get_json()
		name = payload["name"]
		cur.execute("SELECT * FROM test_results WHERE name = (%s)", [name])
		values = cur.fetchall()
		print(values)
		return values

if __name__ == "__main__":
	app.run()