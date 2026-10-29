# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

core-skeleton

## Roadmap

### core-skeleton — Core FastAPI/React skeleton with health check

Status: done

Acceptance:
- FastAPI server starts on port 8000
- React dev server starts on port 3000
- GET /health returns {"status": "ok"}
- Frontend displays health status from backend

Implementation: `backend/app/main.py`, `backend/app/api/health.py`, `frontend/src/components/HealthStatus.tsx`

Tests: `backend/tests/test_health.py`

### skill-management — Skill CRUD API and UI

Status: planned

Acceptance:
- POST /skills creates a skill
- GET /skills lists skills
- GET /skills/{id} retrieves a skill
- PUT /skills/{id} updates a skill
- DELETE /skills/{id} deletes a skill
- Frontend skill list with create/edit/delete

### instinct-engine — Instinct evaluation engine

Status: planned

Acceptance:
- POST /instincts/evaluate runs instinct evaluation
- Instincts stored with conditions and actions
- Frontend instinct builder

### memory-store — Memory persistence layer

Status: planned

Acceptance:
- POST /memory stores a memory entry
- GET /memory retrieves memories with filters
- Memory TTL and cleanup

### security-audit — Security audit logging

Status: planned

Acceptance:
- All API calls logged with user/context
- Audit log query endpoint
- Sensitive data redaction

### research-assistant — Research-first development assistant

Status: planned

Acceptance:
- POST /research/query submits research task
- GET /research/{id} retrieves results
- Source citation tracking

