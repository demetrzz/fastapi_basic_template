import pytest


@pytest.mark.asyncio
async def test_get_tasks(client, test_user, auth_backend):
    token = await auth_backend.get_strategy().write_token(test_user)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/tasks", headers=headers)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, content: {response.content}"
    tasks = response.json()
    assert len(tasks) == 5
    for i in range(5):
        assert tasks[i]["id"] == i
        assert tasks[i]["title"] == f"Task {i}"
        assert tasks[i]["completed"] == bool(i % 2)
        assert tasks[i]["author_id"] == str(test_user.id)
