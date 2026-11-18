import pytest
from httpx import AsyncClient
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app


@pytest.mark.asyncio
async def test_create_memory():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/memory",
            json={
                "key": "user1",
                "value": {"name": "Alice", "age": 30},
                "tags": ["user", "profile"],
                "metadata": {"source": "signup"}
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["key"] == "user1"
        assert data["value"] == {"name": "Alice", "age": 30}
        assert data["tags"] == ["user", "profile"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
        assert data["metadata"] == {"source": "signup"}


@pytest.mark.asyncio
async def test_list_memories():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create a memory first
        await client.post("/api/memory", json={
            "key": "mem1",
            "value": "test"
        })

        response = await client.get("/api/memory")
        assert response.status_code == 200
        data = response.json()
        assert "memories" in data
        assert "total" in data
        assert data["total"] >= 1
        assert isinstance(data["memories"], list)


@pytest.mark.asyncio
async def test_get_memory():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create a memory
        create_resp = await client.post("/api/memory", json={
            "key": "mem2",
            "value": "value2"
        })
        memory_id = create_resp.json()["id"]

        # Get the memory
        response = await client.get(f"/api/memory/{memory_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["key"] == "mem2"
        assert data["id"] == memory_id


@pytest.mark.asyncio
async def test_get_memory_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/memory/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_memory():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create a memory
        create_resp = await client.post("/api/memory", json={
            "key": "mem3",
            "value": "old_value"
        })
        memory_id = create_resp.json()["id"]

        # Update the memory
        response = await client.put(f"/api/memory/{memory_id}", json={
            "key": "mem3_updated",
            "value": "new_value",
            "tags": ["updated"]
        })
        assert response.status_code == 200
        data = response.json()
        assert data["key"] == "mem3_updated"
        assert data["value"] == "new_value"
        assert data["tags"] == ["updated"]
        assert data["updated_at"] != data["created_at"]  # updated time changed


@pytest.mark.asyncio
async def test_update_memory_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put(
            "/api/memory/00000000-0000-0000-0000-000000000000",
            json={"key": "newkey"}
        )
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_memory():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create a memory
        create_resp = await client.post("/api/memory", json={
            "key": "mem_to_delete",
            "value": "will delete"
        })
        memory_id = create_resp.json()["id"]

        # Delete the memory
        response = await client.delete(f"/api/memory/{memory_id}")
        assert response.status_code == 204

        # Verify it's gone
        get_resp = await client.get(f"/api/memory/{memory_id}")
        assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_memory_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete("/api/memory/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404
