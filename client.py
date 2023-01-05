import requests
from time import time, ctime

j = {"name": "Velhinho", "specialty": "Dentist", "doctor": "Dr. Sirs", "time": ctime(time())}
requests.post("https://localhost:5000/create", verify="server_cert.pem", json=j)