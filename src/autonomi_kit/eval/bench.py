from __future__ import annotations
import time, argparse, os, csv
from pathlib import Path
import matplotlib.pyplot as plt
from ..orchestrator import run_task

TASKS = {
    "small": [
        "Use python to compute the first 15 Fibonacci numbers and return them as a list.",
        "Search the web for 'PEP 8' and summarize its purpose in 2 bullet points with a link.",
        "Store 'AutonomiKit is awesome' in vector memory then query for 'awesome' and summarize the result.",
    ]
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", default="small")
    parser.add_argument("--plot", default="out/bench.png")
    args = parser.parse_args()

    tasks = TASKS.get(args.tasks, TASKS["small"])
    out_dir = Path(args.plot).parent
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "bench.csv"

    rows = []
    for i, task in enumerate(tasks, 1):
        t0 = time.time()
        try:
            result = run_task(task, max_steps=6)
            ok = int(bool(result and len(result) > 0))
        except Exception as e:
            result = str(e)
            ok = 0
        dt = time.time() - t0
        rows.append({"id": i, "task": task[:60], "ok": ok, "seconds": round(dt, 2)})
        print(f"[{i}] {ok=} {dt:.2f}s")

    # Save CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "task", "ok", "seconds"])
        writer.writeheader()
        writer.writerows(rows)

    # Plot
    xs = [r["id"] for r in rows]
    ys = [r["seconds"] for r in rows]
    plt.figure()
    plt.title("AutonomiKit Bench (seconds)")
    plt.xlabel("Task #")
    plt.ylabel("Seconds")
    plt.plot(xs, ys, marker="o")
    plt.savefig(args.plot, bbox_inches="tight")
    print(f"Wrote: {csv_path} and {args.plot}")

if __name__ == "__main__":
    main()
