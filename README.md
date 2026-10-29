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
│   │   └── api/
│   │       └── health.py    # Health check endpoint
│   ├── tests/
│   │   └── test_health.py
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
│   │       └── HealthStatus.tsx
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

## Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate
pytest -v
```

## Features

- [x] Core FastAPI/React skeleton
- [ ] Skill CRUD API and UI
- [ ] Instinct evaluation engine
- [ ] Memory persistence layer
- [ ] Security audit logging
- [ ] Research-first development assistant

See [PLAN.md](PLAN.md) for detailed roadmap.

Maintainer: Ryan Vo <ryandtvo@gmail.com>
