from fastapi.testclient import TestClient
from TodoApp.main import app
client = TestClient(app)
for path in ['/home', '/login', '/register', '/todos', '/healthy']:
    response = client.get(path)
    print(path, response.status_code)
