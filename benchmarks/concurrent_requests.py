#!/usr/bin/env python3
import argparse
import concurrent.futures
import json
import statistics
import time
import urllib.error
import urllib.request


def percentile(values, pct):
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((pct / 100) * (len(ordered) - 1))))
    return ordered[index]


def request_once(url, timeout):
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            response.read()
            ok = 200 <= response.status < 400
            status = response.status
    except urllib.error.HTTPError as exc:
        ok = False
        status = exc.code
    except Exception as exc:
        ok = False
        status = type(exc).__name__
    elapsed_ms = (time.perf_counter() - started) * 1000
    return ok, status, elapsed_ms


def main():
    parser = argparse.ArgumentParser(description="Concurrent benchmark for Blender MCP HTTP endpoints")
    parser.add_argument("--url", default="http://localhost:8000")
    parser.add_argument("--endpoint", default="/mcp/list_tools")
    parser.add_argument("--requests", type=int, default=100)
    parser.add_argument("--concurrency", type=int, default=10)
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()

    target = args.url.rstrip("/") + "/" + args.endpoint.lstrip("/")
    started = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        results = list(pool.map(lambda _: request_once(target, args.timeout), range(args.requests)))
    wall_seconds = time.perf_counter() - started

    latencies = [item[2] for item in results]
    successes = sum(1 for ok, _, _ in results if ok)
    failures = args.requests - successes
    statuses = {}
    for _, status, _ in results:
        statuses[str(status)] = statuses.get(str(status), 0) + 1

    report = {
        "target": target,
        "requests": args.requests,
        "concurrency": args.concurrency,
        "successes": successes,
        "failures": failures,
        "wall_seconds": round(wall_seconds, 3),
        "throughput_requests_per_second": round(args.requests / wall_seconds, 2) if wall_seconds else 0,
        "latency_ms": {
            "mean": round(statistics.mean(latencies), 2) if latencies else 0,
            "p50": round(percentile(latencies, 50), 2),
            "p95": round(percentile(latencies, 95), 2),
            "p99": round(percentile(latencies, 99), 2),
            "max": round(max(latencies), 2) if latencies else 0,
        },
        "statuses": statuses,
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()