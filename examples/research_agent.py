from autonomi_kit.orchestrator import run_task

if __name__ == "__main__":
    task = "Find 3 recent papers on retrieval-augmented generation (RAG) with citations."
    print(run_task(task))
