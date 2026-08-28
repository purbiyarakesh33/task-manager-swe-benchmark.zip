# Task Manager API — SWE Agent Benchmark

A small but realistic Python repository designed to benchmark an AI software-engineering agent.

## Goal

The agent should be able to inspect the repository, reproduce a failure, trace the code path, make the smallest correct change, and run the tests.

The repository is intentionally clean when first created. The benchmark bugs are described separately in `benchmark/bug_catalog.md` and are NOT injected into the main repository.

## Setup

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -e ".[dev]"
pytest -q
```

Expected result:

```text
19 passed
```

## Run the API

```bash
uvicorn task_manager.api:app --reload
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn SWE agents","description":"Benchmark the agent"}'
```

## Benchmark workflow

1. Copy the repository to a fresh working directory.
2. Inject exactly one bug from `benchmark/bug_catalog.md`.
3. Give the agent only the repository and a generic task such as:
   `There is a bug in this repository. Find it, fix it, and run the tests.`
4. Record whether the agent:
   - identified the root cause,
   - changed the correct code,
   - preserved unrelated behavior,
   - passed all tests.
5. Reset the repository before testing the next bug.

## Design

The code intentionally has multiple layers:

API -> Service -> Repository -> Model

There are unit tests and API tests. Some benchmark bugs require following data across more than one layer.
