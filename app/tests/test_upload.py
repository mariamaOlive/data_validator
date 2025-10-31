import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def csv_file():
    csv_content = "name,age\nJohn,30\nJane,25"
    return {"file": ("test.csv", csv_content, "text/csv")}

@pytest.mark.parametrize("path", ["/validate", "/typecheck"])
def test_upload_csv_file_success(csv_file, path):
    r = client.post(path, files=csv_file)
    assert r.status_code == 200
    assert r.json()["total_rows"] == 2


@pytest.mark.parametrize("path", ["/validate", "/typecheck"])
def test_upload_rejects_non_csv(path):
    txt_content = "This is a plain text file."
    files = {"file": ("test.txt", txt_content, "text/plain")}
    
    response = client.post(path, files=files)
    assert response.status_code == 422  
    
    
@pytest.mark.parametrize("path", ["/validate", "/typecheck"])    
def test_upload_empty_csv_file(path):
    csv_content = "name,age\n"
    files = {"file": ("empty.csv", csv_content, "text/csv")}
    
    response = client.post(path, files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["total_rows"] == 0