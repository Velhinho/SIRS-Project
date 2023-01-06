import requests, sys
from time import time, ctime

url = "https://localhost:5000"
cert = sys.argv[1]

while True:
  print("type c to create appointment")
  print("type r to read appointment")
  print("type t to check test results")
  cmd = input()
  if cmd == "c":
    j = {"name": input("name: "), "specialty": input("specialty: "), "doctor": input("doctor: "), "time": ctime(time())}
    res = requests.post(url + "/create", verify=cert, json=j)
    print(res.text)
  elif cmd == "r":
    j = {"name": input("name: ")}
    res = requests.get(url + "/read", verify=cert, json=j)
    print(res.text)
  elif cmd == "t":
    j = {"name": input("name: ")}
    res = requests.get(url + "/test_results", verify=cert, json=j)
    print(res.text)
  else:
    print("invalid command")