

def test_can_create_task(test_client):
    response =test_client.post(
        "/items/",
            json={
                "title":"Test Task",
                "description":"This is a test task",
                "todo": "2024-10-01T12:00:00",
                "done":False,
            },
    )
    assert response.status_code == 200
    assert response.json()["title"]=="Test Task"
    assert response.json()["description"]=="This is a test task"
    assert response.json()["todo"]=="2024-10-01T12:00:00"
    assert response.json()["done"]is False


def test_can_get_task(test_client):
    response =test_client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json()["items"],list)
    assert len(response.json()["items"])>0
    assert "title" in response.json()["items"][0]
    assert "description" in response.json()["items"][0]
    assert "todo" in response.json()["items"][0]
    assert "done" in response.json()["items"][0]

def test_can_get_task_by_id(test_client):
    create_renponse  = test_client.post(
        "/items/",
           json={
               "title":"Task to Get",
               "description": "This task will be retrived",
               "todo":"2024-10-01T12:00:00",
               "done":False,
           },
    )
    task_id = create_renponse.json()["id"]
    print(task_id)
    get_response = test_client.get(f"/items/{task_id}")
    assert get_response.status_code ==200
    assert get_response.json()["title"] =="Task to Get"
    assert get_response.json()["description"] =="This task will be retrived"
    assert get_response.json()["todo"] =="2024-10-01T12:00:00"
    assert get_response.json()["done"] is False


def test_can_update_task(test_client):
    create_response = test_client.post(
        "/items/",
        json={
            "title": "Task to Update",
            "description": "This task will be updated",
            "todo": "2024-10-01T12:00:00",
            "done": False,
        },
    )
    task_id = create_response.json()["id"]
    update_response = test_client.put(
        f"/items/{task_id}",
        json={
            "title": "Updated Task",
            "description": "This task has been Updated",
            "todo": "2024-10-01T12:00:00",
            "done": True,
        },
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Task"
    assert update_response.json()["description"] == "This task has been Updated"
    assert update_response.json()["todo"] == "2024-10-01T12:00:00"
    assert update_response.json()["done"] is True



def test_can_delete_task(test_client):   
    create_response = test_client.post(
        "/items/",
        json={
            "title": "Task to Delete",
            "description": "This task will be Delete",
            "todo": "2024-10-01T12:00:00",
            "done": False,
        },
    )
    task_id = create_response.json()["id"]
    delete_response = test_client.delete(f"/items/{task_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["title"] == "Task to Delete"
    assert delete_response.json()["description"] == "This task will be Delete"
    assert delete_response.json()["todo"] == "2024-10-01T12:00:00"
    assert delete_response.json()["done"] is False

    get_response = test_client.get(f"/items/{task_id}")
    assert get_response.statis_code ==404
    assert get_response.json()["detail"] =="Item not found"


def test_can_authenticate(test_client):
    response =test_client.post("/token",data = {"username":"admin487","password":"admin"},
    )
    assert response.status_code ==200
    assert "access_token" in response.json()
    assert response.json()["token_type"]=="bearer"
    token = response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    about_response = test_client.get("/about_users",headers=headers)
    assert about_response.status_code == 200
    assert about_response.json()["message"] == "This is a user:admin487"


def test_can_access_protected_route_without_token(test_client):
    response = test_client.get("/about_users")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
