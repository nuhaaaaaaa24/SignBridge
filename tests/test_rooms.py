def test_invalid_room_returns_404(client):
    response = client.get('/call?room=FAKE-0000')
    assert response.status_code == 404

def test_valid_room_returns_200(client, test_room):
    response = client.get('/call?room=TEST-1234')
    assert response.status_code == 200

def test_create_room_requires_login(client):
    response = client.post('/create-room', follow_redirects=True)
    assert response.status_code == 200