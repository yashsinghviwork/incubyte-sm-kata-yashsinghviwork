# Salary Management API

A FastAPI-based REST API for managing employee records, calculating salaries with country-based deductions, and providing salary metrics.

## Features

- **Employee CRUD** — Create, read, update (full & partial), and delete employee records stored in SQLite
- **Salary Calculation** — Compute net salary with country-specific tax deductions (India 10% TDS, US 12% TDS), accepts optional gross salary override
- **Salary Metrics** — Min/max/average salary filtered by country, job title, or both
- **Input Validation** — Rejects empty fields and negative salaries at the schema level

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy + SQLite
- Pydantic v2 (validation)
- pytest + Starlette TestClient (testing)
- uv (package manager)

## Setup

```bash
uv sync
```

## Running the Server

```bash
uv run uvicorn app.main:app --reload
```

## Running Tests

```bash
uv run pytest tests/ -v
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/employees` | Create employee |
| GET | `/employees` | List all employees |
| GET | `/employees/{id}` | Get employee by ID |
| PUT | `/employees/{id}` | Full update |
| PATCH | `/employees/{id}` | Partial update |
| DELETE | `/employees/{id}` | Delete employee |
| GET | `/employees/{id}/salary?gross_salary=` | Calculate net salary (optional gross override) |
| GET | `/metrics/salary?country=&job_title=` | Salary min/max/avg |

## TDD Approach

This project follows strict Test-Driven Development:

1. **Red** — Write failing tests first
2. **Green** — Implement minimal code to pass
3. **Refactor** — Clean up while keeping tests green

Commit history reflects each TDD cycle with incremental commits.

## Implementation Details

- **AI tool used:** Claude Code (Anthropic CLI), powered by Claude Opus
- **How AI was used:**
  - **Project scaffolding** — Initial project structure, pyproject.toml, and dependency setup were generated via prompt ("set up a Python FastAPI project with uv")
  - **Test generation** — Failing test cases were drafted by describing the kata requirements and asking for RED-phase tests covering CRUD, salary calculation, and metrics
  - **Implementation** — Endpoint code, SQLAlchemy models, and Pydantic schemas were generated from the test expectations, then reviewed for correctness
  - **Refactoring** — Prompted to split monolithic main.py into routers, extract helpers, and modernize to mapped_column; verified tests stayed green after each change
  - **Edge cases** — Asked for validation edge cases (empty strings, negative salary, zero salary, combined filters); generated failing tests first, then minimal validation code
- **Trade-offs made with AI:**
  - Accepted AI-suggested project layout (app/routers/, schemas, models, database separation) as it follows standard FastAPI conventions
  - Manually reviewed all generated code before committing to ensure it matched kata requirements exactly (e.g., deduction rules, metric calculations)
  - Chose sync endpoints over async since SQLite with synchronous SQLAlchemy doesn't benefit from async and keeps the code simpler
  - Used Starlette TestClient (sync) instead of httpx AsyncClient to keep tests straightforward
