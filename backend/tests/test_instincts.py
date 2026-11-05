import pytest
from httpx import AsyncClient
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app
from app.api.instincts import _instincts


@pytest.fixture(autouse=True)
def clear_instincts():
    """Clear the instincts storage before each test."""
    _instincts.clear()
    yield
    _instincts.clear()


@pytest.mark.asyncio
async def test_create_instinct():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/instincts",
            json={
                "name": "Error Handler",
                "description": "Handles error conditions",
                "conditions": [
                    {"field": "level", "operator": "equals", "value": "error"}
                ],
                "actions": [
                    {"type": "log", "parameters": {"message": "Error detected"}},
                    {"type": "notify", "parameters": {"title": "Error Alert", "body": "An error occurred"}}
                ],
                "priority": 10,
                "enabled": True
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Error Handler"
        assert data["description"] == "Handles error conditions"
        assert len(data["conditions"]) == 1
        assert data["conditions"][0]["field"] == "level"
        assert data["conditions"][0]["operator"] == "equals"
        assert data["conditions"][0]["value"] == "error"
        assert len(data["actions"]) == 2
        assert data["actions"][0]["type"] == "log"
        assert data["actions"][1]["type"] == "notify"
        assert data["priority"] == 10
        assert data["enabled"] is True
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data


@pytest.mark.asyncio
async def test_list_instincts():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create an instinct first
        await client.post("/api/instincts", json={
            "name": "Test Instinct",
            "description": "Test",
            "conditions": [],
            "actions": [],
            "priority": 5
        })
        
        response = await client.get("/api/instincts")
        assert response.status_code == 200
        data = response.json()
        assert "instincts" in data
        assert "total" in data
        assert data["total"] >= 1
        assert isinstance(data["instincts"], list)


@pytest.mark.asyncio
async def test_get_instinct():
    async with AsyncClient(app=app, base_url="http://test") as client:
        create_resp = await client.post("/api/instincts", json={
            "name": "Get Test",
            "description": "Test get",
            "conditions": [],
            "actions": [],
            "priority": 1
        })
        instinct_id = create_resp.json()["id"]
        
        response = await client.get(f"/api/instincts/{instinct_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == instinct_id
        assert data["name"] == "Get Test"


@pytest.mark.asyncio
async def test_get_instinct_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/instincts/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_instinct():
    async with AsyncClient(app=app, base_url="http://test") as client:
        create_resp = await client.post("/api/instincts", json={
            "name": "Original",
            "description": "Original desc",
            "conditions": [],
            "actions": [],
            "priority": 1
        })
        instinct_id = create_resp.json()["id"]
        
        response = await client.put(f"/api/instincts/{instinct_id}", json={
            "name": "Updated",
            "priority": 50
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated"
        assert data["priority"] == 50
        assert data["description"] == "Original desc"  # unchanged


@pytest.mark.asyncio
async def test_update_instinct_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put("/api/instincts/00000000-0000-0000-0000-000000000000", json={
            "name": "Updated"
        })
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_instinct():
    async with AsyncClient(app=app, base_url="http://test") as client:
        create_resp = await client.post("/api/instincts", json={
            "name": "To Delete",
            "description": "Will be deleted",
            "conditions": [],
            "actions": [],
            "priority": 1
        })
        instinct_id = create_resp.json()["id"]
        
        response = await client.delete(f"/api/instincts/{instinct_id}")
        assert response.status_code == 204
        
        get_resp = await client.get(f"/api/instincts/{instinct_id}")
        assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_instinct_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete("/api/instincts/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_evaluate_instincts_match():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create an instinct that matches "error" level
        await client.post("/api/instincts", json={
            "name": "Error Handler",
            "description": "Handles errors",
            "conditions": [
                {"field": "level", "operator": "equals", "value": "error"}
            ],
            "actions": [
                {"type": "log", "parameters": {"message": "Error detected"}}
            ],
            "priority": 10,
            "enabled": True
        })
        
        # Create another instinct that matches "warning" level
        await client.post("/api/instincts", json={
            "name": "Warning Handler",
            "description": "Handles warnings",
            "conditions": [
                {"field": "level", "operator": "equals", "value": "warning"}
            ],
            "actions": [
                {"type": "notify", "parameters": {"title": "Warning"}}
            ],
            "priority": 5,
            "enabled": True
        })
        
        # Evaluate with error context - should match Error Handler only
        response = await client.post("/api/instincts/evaluate", json={
            "data": {"level": "error", "message": "Something went wrong"}
        })
        assert response.status_code == 200
        data = response.json()
        assert data["total_evaluated"] == 2
        assert data["total_matched"] == 1
        assert len(data["results"]) == 2
        
        # Find the matched instinct
        matched = [r for r in data["results"] if r["matched"]]
        assert len(matched) == 1
        assert matched[0]["instinct_name"] == "Error Handler"
        assert len(matched[0]["executed_actions"]) == 1
        assert matched[0]["executed_actions"][0]["type"] == "log"


@pytest.mark.asyncio
async def test_evaluate_instincts_no_match():
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post("/api/instincts", json={
            "name": "Error Handler",
            "description": "Handles errors",
            "conditions": [
                {"field": "level", "operator": "equals", "value": "error"}
            ],
            "actions": [
                {"type": "log", "parameters": {"message": "Error detected"}}
            ],
            "priority": 10,
            "enabled": True
        })
        
        # Evaluate with info context - should not match
        response = await client.post("/api/instincts/evaluate", json={
            "data": {"level": "info", "message": "Just info"}
        })
        assert response.status_code == 200
        data = response.json()
        assert data["total_evaluated"] == 1
        assert data["total_matched"] == 0
        assert len(data["results"]) == 1
        assert data["results"][0]["matched"] is False
        assert len(data["results"][0]["executed_actions"]) == 0


@pytest.mark.asyncio
async def test_evaluate_instincts_disabled():
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post("/api/instincts", json={
            "name": "Disabled Handler",
            "description": "Disabled",
            "conditions": [
                {"field": "level", "operator": "equals", "value": "error"}
            ],
            "actions": [
                {"type": "log", "parameters": {"message": "Error detected"}}
            ],
            "priority": 10,
            "enabled": False
        })
        
        response = await client.post("/api/instincts/evaluate", json={
            "data": {"level": "error"}
        })
        data = response.json()
        # Disabled instincts are skipped entirely, so results will be empty
        assert data["total_evaluated"] == 1
        assert data["total_matched"] == 0
        assert len(data["results"]) == 0


@pytest.mark.asyncio
async def test_evaluate_instincts_priority_order():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Low priority instinct
        await client.post("/api/instincts", json={
            "name": "Low Priority",
            "description": "Low",
            "conditions": [{"field": "type", "operator": "equals", "value": "test"}],
            "actions": [{"type": "log", "parameters": {"message": "low"}}],
            "priority": 1,
            "enabled": True
        })
        
        # High priority instinct
        await client.post("/api/instincts", json={
            "name": "High Priority",
            "description": "High",
            "conditions": [{"field": "type", "operator": "equals", "value": "test"}],
            "actions": [{"type": "log", "parameters": {"message": "high"}}],
            "priority": 100,
            "enabled": True
        })
        
        response = await client.post("/api/instincts/evaluate", json={
            "data": {"type": "test"}
        })
        assert response.status_code == 200
        data = response.json()
        assert data["total_matched"] == 2
        # Results should be sorted by priority (high first)
        matched = [r for r in data["results"] if r["matched"]]
        assert matched[0]["instinct_name"] == "High Priority"
        assert matched[1]["instinct_name"] == "Low Priority"


@pytest.mark.asyncio
async def test_evaluate_instincts_contains_operator():
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post("/api/instincts", json={
            "name": "Contains Test",
            "description": "Tests contains",
            "conditions": [{"field": "tags", "operator": "contains", "value": "urgent"}],
            "actions": [{"type": "log", "parameters": {"message": "urgent found"}}],
            "priority": 10,
            "enabled": True
        })
        
        # Test with list containing "urgent"
        response = await client.post("/api/instincts/evaluate", json={
            "data": {"tags": ["urgent", "bug", "frontend"]}
        })
        assert response.status_code == 200
        data = response.json()
        assert data["total_matched"] == 1
        assert data["results"][0]["matched"] is True
        
        # Test with list not containing "urgent"
        response = await client.post("/api/instincts/evaluate", json={
            "data": {"tags": ["bug", "frontend"]}
        })
        assert response.status_code == 200
        data = response.json()
        assert data["total_matched"] == 0
        assert data["results"][0]["matched"] is False


@pytest.mark.asyncio
async def test_evaluate_instincts_numeric_operators():
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post("/api/instincts", json={
            "name": "High Value",
            "description": "Handles high values",
            "conditions": [
                {"field": "score", "operator": "greater_than", "value": 80},
                {"field": "score", "operator": "less_than", "value": 100}
            ],
            "actions": [{"type": "log", "parameters": {"message": "high score"}}],
            "priority": 10,
            "enabled": True
        })
        
        # Score 90 - should match
        response = await client.post("/api/instincts/evaluate", json={
            "data": {"score": 90}
        })
        assert response.status_code == 200
        data = response.json()
        assert data["total_matched"] == 1
        assert data["results"][0]["matched"] is True
        
        # Score 70 - should not match (not greater than 80)
        response = await client.post("/api/instincts/evaluate", json={
            "data": {"score": 70}
        })
        assert response.status_code == 200
        data = response.json()
        assert data["total_matched"] == 0
        assert data["results"][0]["matched"] is False
        
        # Score 100 - should not match (not less than 100)
        response = await client.post("/api/instincts/evaluate", json={
            "data": {"score": 100}
        })
        assert response.status_code == 200
        data = response.json()
        assert data["total_matched"] == 0
        assert data["results"][0]["matched"] is False
