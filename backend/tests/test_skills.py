import pytest
from httpx import AsyncClient
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app


@pytest.mark.asyncio
async def test_create_skill():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/skills",
            json={
                "name": "Python Programming",
                "description": "Expert in Python development",
                "category": "Programming",
                "tags": ["python", "backend", "api"]
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Python Programming"
        assert data["description"] == "Expert in Python development"
        assert data["category"] == "Programming"
        assert data["tags"] == ["python", "backend", "api"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data


@pytest.mark.asyncio
async def test_list_skills():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create a skill first
        await client.post("/api/skills", json={
            "name": "JavaScript",
            "description": "Frontend development",
            "category": "Programming",
            "tags": ["js", "frontend"]
        })
        
        response = await client.get("/api/skills")
        assert response.status_code == 200
        data = response.json()
        assert "skills" in data
        assert "total" in data
        assert data["total"] >= 1
        assert isinstance(data["skills"], list)


@pytest.mark.asyncio
async def test_get_skill():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create a skill
        create_resp = await client.post("/api/skills", json={
            "name": "Rust",
            "description": "Systems programming",
            "category": "Programming",
            "tags": ["rust", "systems"]
        })
        skill_id = create_resp.json()["id"]
        
        # Get the skill
        response = await client.get(f"/api/skills/{skill_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Rust"
        assert data["id"] == skill_id


@pytest.mark.asyncio
async def test_get_skill_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/skills/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_skill():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create a skill
        create_resp = await client.post("/api/skills", json={
            "name": "Go",
            "description": "Concurrent programming",
            "category": "Programming",
            "tags": ["go", "concurrency"]
        })
        skill_id = create_resp.json()["id"]
        
        # Update the skill
        response = await client.put(f"/api/skills/{skill_id}", json={
            "name": "Golang",
            "tags": ["go", "concurrency", "backend"]
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Golang"
        assert data["tags"] == ["go", "concurrency", "backend"]
        assert data["description"] == "Concurrent programming"  # unchanged


@pytest.mark.asyncio
async def test_update_skill_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put(
            "/api/skills/00000000-0000-0000-0000-000000000000",
            json={"name": "Test"}
        )
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_skill():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create a skill
        create_resp = await client.post("/api/skills", json={
            "name": "Delete Me",
            "description": "Will be deleted",
            "category": "Test",
            "tags": []
        })
        skill_id = create_resp.json()["id"]
        
        # Delete the skill
        response = await client.delete(f"/api/skills/{skill_id}")
        assert response.status_code == 204
        
        # Verify it's gone
        get_resp = await client.get(f"/api/skills/{skill_id}")
        assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_skill_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete("/api/skills/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404
