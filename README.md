# Axiom Studio 145 — Ryan Vo

> Work in progress. This checkpoint may be incomplete or fail tests. See PLAN.md and STATUS.md before use.


The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond.

## Quick Start

### Using Docker Compose (Recommended)

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Health Check: http://localhost:8000/api/health

### Manual Development Setup

#### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
axiom-studio-145/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI application
│   │   ├── config.py        # Configuration
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── skill.py     # Skill model
│   │   │   └── instinct.py  # Instinct model
│   │   └── api/
│   │       ├── __init__.py
│   │       ├── health.py    # Health check endpoint
│   │       ├── skills.py    # Skills CRUD API
│   │       └── instincts.py # Instincts CRUD + evaluation API
│   ├── tests/
│   │   ├── test_health.py
│   │   ├── test_skills.py
│   │   └── test_instincts.py
│   ├── requirements.txt
│   ├── pytest.ini
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── main.tsx         # Entry point
│   │   ├── App.tsx          # Main app component
│   │   ├── App.css
│   │   ├── index.css
│   │   └── components/
│   │       ├── HealthStatus.tsx
│   │       ├── SkillList.tsx
│   │       └── InstinctList.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── index.html
│   └── Dockerfile
├── docker-compose.yml
├── feature-plan.json
├── PLAN.md
├── CHANGELOG.md
└── STATUS.md
```

## API Endpoints

- `GET /` - Root endpoint with app info
- `GET /api/health` - Health check returns `{"status": "ok"}`
- `GET /api/skills` - List all skills
- `POST /api/skills` - Create a skill
- `GET /api/skills/{id}` - Get a skill by ID
- `PUT /api/skills/{id}` - Update a skill
- `DELETE /api/skills/{id}` - Delete a skill
- `GET /api/instincts` - List all instincts
- `POST /api/instincts` - Create an instinct
- `GET /api/instincts/{id}` - Get an instinct by ID
- `PUT /api/instincts/{id}` - Update an instinct
- `DELETE /api/instincts/{id}` - Delete an instinct
- `POST /api/instincts/evaluate` - Evaluate instincts against context data
## Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate
pytest -v
```

## Features

- [x] Core FastAPI/React skeleton
- [x] Skill CRUD API and UI
- [x] Instinct evaluation engine
- [ ] Memory persistence layer
- [ ] Security audit logging
- [ ] Research-first development assistant

See [PLAN.md](PLAN.md) for detailed roadmap.

Maintainer: Ryan Vo <ryandtvo@gmail.com>
