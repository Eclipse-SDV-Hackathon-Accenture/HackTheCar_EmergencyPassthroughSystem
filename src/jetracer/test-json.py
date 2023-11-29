import json
data = json.loads(b'{"move":"off"}')
print(data['move'])  # or `print data['two']` in Python 2
