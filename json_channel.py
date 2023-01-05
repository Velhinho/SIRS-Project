import base64, json

class JsonChannel:
  def __init__(self, channel) -> None:
    self.channel = channel
    self.counter = 0

  def send(self, data):
    self.counter += 1
    json_string = json.dumps({"data": data, "counter": self.counter})
    encoded = base64_encode(json_string)
    self.channel.send(encoded)

  def recv(self):
    encoded = self.channel.recv()
    json_string = base64_decode(encoded)
    data = json.loads(json_string)
    if data["counter"] > self.counter:
      self.counter = data["counter"]
      return data["data"]
    else:
      raise ValueError("Repeated msg")

def base64_encode(data_str):
  return base64.b64encode(bytes(data_str, "utf-8"))

def base64_decode(encoded):
  return str(base64.b64decode(encoded), "utf-8")
