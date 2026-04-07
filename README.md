# Salary Management API

A FastAPI-based REST API for managing employee records, calculating salaries with country-based deductions, and providing salary metrics.

## Features

- **Employee CRUD** — Create, read, update, and delete employee records (stored in SQLite)
- **Salary Calculation** — Compute net salary with country-specific tax deductions (India 10% TDS, US 12% TDS)
- **Salary Metrics** — Min/max/average salary by country, average salary by job title

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy + SQLite
- pytest + httpx (testing)
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

## TDD Approach

This project follows strict Test-Driven Development:

1. **Red** — Write failing tests first
2. **Green** — Implement minimal code to pass
3. **Refactor** — Clean up while keeping tests green

Commit history reflects each TDD cycle.

## Implementation Details

- AI tool used: **Claude Code** (Anthropic CLI)
- Used for scaffolding project structure, generating test cases, and drafting implementation code
- All code reviewed and validated through the TDD loop
