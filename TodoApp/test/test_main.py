from fastapi.testclient import TestClient
import main
from fastapi import status



# test client
client = TestClient(main.app)
def test_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "Healthy"}