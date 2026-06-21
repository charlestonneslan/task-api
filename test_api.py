import api

def test_create_task(client):
    response = client.post("/tasks", json={"title": "Test title", "description": "Test description"})
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Test title",
        "description": "Test description",
        "done": False
    }

def test_list_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

    client.post("/tasks", json={"title": "Test title", "description": "Test description"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == [{
        "id": 1,
        "title": "Test title",
        "description": "Test description",
        "done": False
    }]

def test_mark_done(client):
    client.post("/tasks", json={"title": "Test title", "description": "Test description"})
    response = client.patch("/tasks/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "done": True}

    response = client.get("/tasks")
    assert response.json()[0]["done"] == True

def test_delete_task(client):
    client.post("/tasks", json={"title": "Test title", "description": "Test description"})
    response = client.delete("/tasks/1")
    assert response.status_code == 204

    response = client.get("/tasks")
    assert response.json() == []

def test_patch_missing_returns_404(client):
    response = client.patch("/tasks/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_delete_missing_returns_404(client):
    response = client.delete("/tasks/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}