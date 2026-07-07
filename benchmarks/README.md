# Benchmarking Blender MCP

This directory contains a reproducible HTTP concurrency harness. It intentionally ships without fabricated performance numbers.

## Run

Start Blender and enable the MCP server, then run:

```bash
python benchmarks/concurrent_requests.py \
  --url http://localhost:8000 \
  --endpoint /mcp/list_tools \
  --requests 100 \
  --concurrency 10
```

For a write-path benchmark, point the harness at a stable invocation endpoint or extend it with a JSON payload for one representative tool.

## Record the environment

When publishing results, include:

- CPU and RAM;
- operating system;
- Blender version;
- Python version;
- server commit SHA;
- endpoint/tool under test;
- request count and concurrency;
- whether Blender was headless or interactive.

## Metrics

The harness reports:

- successes and failures;
- response status distribution;
- total wall time;
- requests per second;
- mean latency;
- p50, p95 and p99 latency;
- maximum latency.

## Interpretation

Blender scene mutations are serialized by design to protect `bpy` state. A concurrency benchmark therefore measures request handling, queueing pressure and response behavior; it should not be misrepresented as simultaneous scene mutation.

A useful benchmark matrix is:

| Scenario | Requests | Concurrency | Purpose |
|---|---:|---:|---|
| Tool discovery | 100 | 10 | HTTP/API baseline |
| Tool discovery | 500 | 50 | request burst behavior |
| Lightweight read tool | 100 | 10 | queue overhead |
| Representative mutation | 50 | 5 | serialized Blender workload |

Commit results only after they have been measured.