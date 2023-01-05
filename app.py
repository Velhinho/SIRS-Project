from flask import Flask, request
import psycopg2

app = Flask(__name__)

@app.route("/create", methods=["POST"])
def create_appointment():
	with psycopg2.connect("dbname=sirs user=velhinho") as conn, conn.cursor() as cur:
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
	pass

@app.route("/update", methods=["PUT"])
def update_appointment():
	pass

@app.route("/delete", methods=["DELETE"])
def delete_appointment():
	pass

if __name__ == "__main__":
	app.run()