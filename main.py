from flask import Flask, request, jsonify
import unittest
import os

app = Flask(__name__)

# Sample Data Storage (simulating a database)
users = {}
houses = {}
rooms = {}
devices = {}

# Error Handling Class
class APIError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code

@app.errorhandler(APIError)
def handle_api_error(error):
    response = jsonify({'error': error.message})
    response.status_code = error.status_code
    return response

# User API Endpoints
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if 'id' not in data or 'name' not in data:
        raise APIError("Missing required fields", 400)
    users[data['id']] = data['name']
    return jsonify({'message': 'User created', 'user': data}), 201

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    if user_id not in users:
        raise APIError("User not found", 404)
    return jsonify({'id': user_id, 'name': users[user_id]})

# House API Endpoints
@app.route('/houses', methods=['POST'])
def create_house():
    data = request.json
    if 'id' not in data or 'name' not in data:
        raise APIError("Missing required fields", 400)
    houses[data['id']] = {'name': data['name'], 'rooms': []}
    return jsonify({'message': 'House created', 'house': data}), 201

@app.route('/houses/<house_id>', methods=['GET'])
def get_house(house_id):
    if house_id not in houses:
        raise APIError("House not found", 404)
    return jsonify(houses[house_id])

# Room API Endpoints
@app.route('/rooms', methods=['POST'])
def create_room():
    data = request.json
    if 'id' not in data or 'name' not in data or 'house_id' not in data:
        raise APIError("Missing required fields", 400)
    if data['house_id'] not in houses:
        raise APIError("House does not exist", 404)
    rooms[data['id']] = {'name': data['name'], 'devices': []}
    houses[data['house_id']]['rooms'].append(data['id'])
    return jsonify({'message': 'Room created', 'room': data}), 201

# Device API Endpoints
@app.route('/devices', methods=['POST'])
def create_device():
    data = request.json
    if 'id' not in data or 'type' not in data or 'room_id' not in data:
        raise APIError("Missing required fields", 400)
    if data['room_id'] not in rooms:
        raise APIError("Room does not exist", 404)
    devices[data['id']] = {'type': data['type']}
    rooms[data['room_id']]['devices'].append(data['id'])
    return jsonify({'message': 'Device created', 'device': data}), 201

# Unit Tests
class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_user(self):
        response = self.app.post('/users', json={'id': '1', 'name': 'Alice'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created', response.json['message'])

    def test_get_nonexistent_user(self):
        response = self.app.get('/users/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found', response.json['error'])

if __name__ == '__main__':
    if os.getenv("RUNNING_TESTS"):
        unittest.main()
    else:
        app.run(debug=True)
