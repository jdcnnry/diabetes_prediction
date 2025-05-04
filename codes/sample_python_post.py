import http.client
import json

conn = http.client.HTTPConnection("localhost", 8080)
payload = json.dumps({
  "name": "Jade Connery Ramos",
  "email_address": "jade.ramos@student.ateneo.edu",
  "corporate": True,
  "company": "Ateneo de Manila University"
})
headers = {
  'Content-Type': 'application/json'
}
conn.request("POST", "/api/v1/users", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))