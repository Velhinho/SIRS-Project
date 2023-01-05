import requests
from time import time, ctime

while True:
  print("type c to create appointment")
  print("type r to read appointment")
  print("type t to check test results")
  cmd = input()
  if cmd == "c":
    j = {"name": input("name: "), "specialty": input("specialty: "), "doctor": input("doctor: "), "time": ctime(time())}
    res = requests.post("https://localhost:5000/create", verify="server_cert.pem", json=j)
    print(res.text)
  elif cmd == "r":
    j = {"name": input("name: ")}
    res = requests.get("https://localhost:5000/read", verify="server_cert.pem", json=j)
    print(res.text)
  elif cmd == "t":
    j = {"name": input("name: ")}
    res = requests.get("https://localhost:5000/test_results", verify="server_cert.pem", json=j)
    print(res.text)
  else:
    print("invalid command")