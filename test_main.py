from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_all_teams():
    response = client.get("/teams")
    assert response.status_code == 200
    teams = response.json()
    assert len(teams) >= 4
    assert teams[0]["name"] == "Suns"


def test_get_existing_team():
    response = client.get("/teams/2")
    assert response.status_code == 200
    team = response.json()
    assert team["id"] == 2
    assert team["name"] == "Diamondbacks"
    assert team["city"] == "Phoenix"
    assert team["sport"] == "Baseball"


def test_get_nonexistent_team():
    response = client.get("/teams/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Team not found"


def test_get_team_with_invalid_id():
    response = client.get("/teams/abc")
    assert response.status_code == 422


def test_create_valid_team():
    new_team = {"name": "Sounders", "city": "Seattle", "sport": "Soccer"}
    response = client.post("/teams", json=new_team)
    assert response.status_code == 201
    team = response.json()
    assert team["name"] == "Sounders"
    assert team["city"] == "Seattle"
    assert team["sport"] == "Soccer"
    assert isinstance(team["id"], int)


def test_created_team_can_be_retrieved():
    new_team = {"name": "Rapids", "city": "Denver", "sport": "Soccer"}
    created = client.post("/teams", json=new_team).json()
    response = client.get(f"/teams/{created['id']}")
    assert response.status_code == 200
    assert response.json() == created


def test_create_team_with_missing_fields():
    response = client.post("/teams", json={"name": "Sharks"})
    assert response.status_code == 422
    missing_fields = [error["loc"][-1] for error in response.json()["detail"]]
    assert "city" in missing_fields
    assert "sport" in missing_fields


def test_create_team_with_empty_name():
    new_team = {"name": "", "city": "Denver", "sport": "Hockey"}
    response = client.post("/teams", json=new_team)
    assert response.status_code == 422


def test_create_team_with_wrong_data_type():
    new_team = {"name": 123, "city": "Denver", "sport": "Hockey"}
    response = client.post("/teams", json=new_team)
    assert response.status_code == 422


def test_invalid_team_is_not_added():
    before = len(client.get("/teams").json())
    client.post("/teams", json={"name": "Sharks"})
    after = len(client.get("/teams").json())
    assert before == after
