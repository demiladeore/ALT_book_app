from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_users():
  response = client.get("/users")
  assert response.status_code == 200
  assert isinstance(response.json(), list)

def test_add_user():
  payload = {
    "name": "Piya",
    "email": "piya@gmail.com",
    "password": "password123"
  }
  response = client.post("/users", json=payload)
  data = response.json()
  assert data["message"] == "User added successfully"
  assert data["user"]["name"] == "Piya"

def test_get_user_by_id():
  payload = {
    "name": "Piya",
    "email": "piya@gmail.com",
    "password": "password123"
  }
  response = client.post("/users", json=payload)
  add_user_data = response.json()
  user_id = add_user_data['user']['id']
  get_response = client.get(f"/users/{user_id}")
  get_user_data = get_response.json()
  assert get_response.status_code == 200
  assert get_user_data['id'] == user_id

def test_get_user_by_id_not_found():
  user_id = 0
  get_response = client.get(f"/users/{user_id}")
  get_user_data = get_response.json()
  assert get_response.status_code == 404
  assert get_user_data['detail'] == "User not found."

def test_update_user():
  payload = {
    "name": "Piya",
    "email": "piya@gmail.com",
    "password": "password123"
  }
  response = client.post("/users", json=payload)
  add_user_data = response.json()
  user_id = add_user_data['user']['id']
  update_payload = {
    "name": "Piya",
    "email": "piya@gmail.com"
  }
  update_response = client.put(f"/users/{user_id}", json=update_payload)
  update_user_data = update_response.json()
  assert update_response.status_code == 200
  assert update_user_data['message'] == "User updated successfully"
  assert update_user_data['user']['name'] == update_payload['name']
  assert update_user_data['user']['email'] == update_payload['email']

def test_update_user_not_found():
  user_id = 0
  update_payload = {
    "name": "Piya",
    "email": "piya@gmail.com"
  }
  update_response = client.put(f"/users/{user_id}", json=update_payload)
  update_user_data = update_response.json()
  assert update_response.status_code == 404
  assert update_user_data['detail'] == "User not found"

def test_delete_user():
  payload = {
    "name": "Piya",
    "email": "piya@gmail.com",
    "password": "password123"
  }
  response = client.post("/users", json=payload)
  add_user_data = response.json()
  user_id = add_user_data['user']['id']
  delete_response = client.delete(f"/users/{user_id}")
  delete_user_data = delete_response.json()
  assert delete_response.status_code == 200
  assert delete_user_data['message'] == "User deleted successfully"

def test_delete_user_not_found():
  user_id = 0
  delete_response = client.delete(f"/users/{user_id}")
  delete_user_data = delete_response.json()
  assert delete_response.status_code == 404
  assert delete_user_data['detail'] == f"User with id: {user_id} not found"