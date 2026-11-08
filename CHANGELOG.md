# Changelog

## 1.3.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.2.0 - 2026-11-08

### Added
- Instinct evaluation engine (instinct-engine)
  - Backend: Instinct model with conditions, actions, priority, enabled state
  - API endpoints: POST/GET/PUT/DELETE /api/instincts, POST /api/instincts/evaluate
  - In-memory instinct storage with priority-based ordering
  - Condition operators: equals, not_equals, contains, greater_than, less_than, in, not_in
  - Action types: log, notify, execute, store_memory, skip
  - Frontend: InstinctList component with create/edit/delete forms and evaluation panel
  - 14 backend tests for all CRUD operations and evaluation scenarios

### Verified
- All 24 backend tests pass (2 health + 8 skills + 14 instincts)
- Frontend TypeScript compiles without errors
- Frontend production build succeeds

## 1.1.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## [0.2.0] - 2026-11-02

### Added
- Skill CRUD API and UI (skill-management)
  - Backend: Skill model with UUID, name, description, category, tags
  - API endpoints: POST/GET/PUT/DELETE /api/skills
  - In-memory skill storage
  - Frontend: SkillList component with modal form for create/edit
  - 8 backend tests for all CRUD operations

### Verified
- All 10 backend tests pass (2 health + 8 skills)
- Frontend TypeScript compiles without errors
- Frontend production build succeeds

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-10-26

### Added
- Core FastAPI/React skeleton with health check endpoint
- Backend: FastAPI application with health check at `/api/health`
- Frontend: React + Vite + TypeScript with health status display
- Docker Compose for orchestration
- Backend tests with pytest and httpx
- Basic project structure and documentation

### Verified
- Backend health check returns `{"status": "ok"}`
- Backend tests pass (2 tests)
- Frontend builds and runs (manual verification needed)
