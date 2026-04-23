import json

def test_get_token(client, test_user):
    response = client.post('/api/tokens',
        headers={'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='}
    )
    # 200 means token was issued
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data

def test_get_users_without_token(client):
    response = client.get('/api/users')
    assert response.status_code == 401

def test_get_users_with_token(client, test_user):
    # Get token first
    token_response = client.post('/api/tokens',
        headers={'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='}
    )
    token = json.loads(token_response.data)['token']

    response = client.get('/api/users',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200

def test_get_rooms_with_token(client, test_user, test_room):
    token_response = client.post('/api/tokens',
        headers={'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='}
    )
    token = json.loads(token_response.data)['token']

    response = client.get('/api/rooms',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200