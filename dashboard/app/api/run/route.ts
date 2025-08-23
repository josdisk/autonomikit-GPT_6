import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const task = String(body?.task || "");
    const API_BASE_URL = process.env.API_BASE_URL || "http://localhost:8000";
    const r = await fetch(`${API_BASE_URL}/v1/agent/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task }),
      cache: "no-store",
    });
    const data = await r.json();
    return NextResponse.json(data, { status: 200 });
  } catch (e: any) {
    return NextResponse.json({ error: e?.message || "Unknown error" }, { status: 500 });
  }
}
