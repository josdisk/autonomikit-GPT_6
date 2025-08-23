"use client";
import { useState } from "react";
import ResultCard from "../components/ResultCard";

export default function Page() {
  const [task, setTask] = useState("Find 3 recent papers on RAG (with links) and summarize.");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState("");

  const run = async () => {
    setLoading(true);
    setResult("");
    try {
      const r = await fetch("/api/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task }),
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const data = await r.json();
      setResult(data.result || "");
    } catch (e: any) {
      setResult(`Error: ${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main>
      <div className="card">
        <label className="label">Task</label>
        <textarea
          className="input mt-2 h-36"
          value={task}
          onChange={(e) => setTask(e.target.value)}
        />
        <div className="mt-3 flex items-center gap-3">
          <button className="button" onClick={run} disabled={loading}>
            {loading ? "Running..." : "Run Task"}
          </button>
          <span className="text-slate-400 text-sm">
            API base: <code>process.env.API_BASE_URL</code>
          </span>
        </div>
      </div>
      <ResultCard result={result} />
    </main>
  );
}
