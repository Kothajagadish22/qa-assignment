# Assignment 2 — FakeStoreAPI Cart Test Suite (Python)

API tests for https://fakestoreapi.com/ using **pytest + requests**, with **jsonschema** for
response/contract validation.

## What's covered

| Area | File |
|------|------|
| Cart CRUD — POST / GET / PUT / DELETE (positive) | `tests/test_cart_crud.py` |
| Negative cases (bad/non-existent ids, empty body) | `tests/test_cart_negative.py` |
| Authentication (`/auth/login`, Bearer token) | `tests/test_auth.py` |
| Response schema validation (jsonschema) | `tests/test_schema.py` |
| Data-driven — same scenario over 4 product IDs (`parametrize`) | `tests/test_datadriven.py` |
| **Contract / snapshot test (senior bonus)** | `tests/test_contract.py` |

## Run

```bash
pytest assignment2-api

# filter by marker
pytest assignment2-api -m schema
```

## Contract / snapshot test

`test_contract.py` derives the structural shape of a response (keys → types, recursively) and
snapshots it to `tests/__snapshots__/`. Future responses must match the committed snapshot, so any
added/removed field or type change breaks the build. Re-baseline intentionally:

```bash
# Windows PowerShell
$env:UPDATE_SNAPSHOTS=1; pytest assignment2-api/tests/test_contract.py; Remove-Item Env:UPDATE_SNAPSHOTS
# macOS/Linux
UPDATE_SNAPSHOTS=1 pytest assignment2-api/tests/test_contract.py
```

> Note: FakeStoreAPI is a public **mock** — writes are simulated (not persisted) and it's lenient on
> validation. Negative tests are therefore written to assert the *expected contract* while staying
> green against the mock (e.g. accept 4xx **or** an empty/null body), with comments noting what a
> production API should do.

## Framework choice + why

**pytest + requests + jsonschema.**
- `requests` is the de-facto Python HTTP client; a thin `ApiClient` fixture adds the base URL and
  JSON headers so tests stay readable.
- `jsonschema` validates exact field types and powers both the schema and contract checks with
  clear failures.
- `@pytest.mark.parametrize` gives a clean, idiomatic data-driven test.

## Extension plan (parallelisation / reporting)

- **Parallelisation:** API tests are independent — `pytest -n auto` (pytest-xdist) scales freely
  since there's no browser cost; shard across CI runners for very large suites.
- **Reporting:** `pytest-html` today; add Allure for trends and post a pass/fail summary to the PR.
- **Next:** drive the suite against multiple environments via an env-var base URL, generate schemas
  from an OpenAPI spec, add response-time/SLA assertions and a locust/k6 perf layer.
