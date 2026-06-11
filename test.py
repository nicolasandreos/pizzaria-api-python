import requests

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5IiwiZXhwIjoxNzgxMjEwMDAxfQ.AnKKfhc-a1isKzEa6HUIwzp_6O6ZgevA3eJ2ysGyGzA"
}
try:
    response = requests.get("http://127.0.0.1:8000/auth/refresh-access-token", headers=headers)
    print(response.json())
except Exception as e:
    print(e)
    print(e.response.text)