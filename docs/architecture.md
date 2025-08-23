# Architecture

**AutonomiKit‑GPT** separates concerns into: **LLM client**, **tools**, **agent loop**,
**API**, and **CLI**. The agent uses a ReAct‑like policy: the model proposes a tool call in JSON,
the runtime executes it, then the model continues with new observations.
