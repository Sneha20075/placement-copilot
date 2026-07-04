# 🎯 Placement Copilot

A personal multi-agent AI concierge that helps final-year engineering
students prepare for campus placements — built for Kaggle's **AI Agents:
Intensive Vibe Coding Capstone Project**.

**Track:** Concierge Agents

## Problem

Final-year students juggle resume building, mock interviews, and study
planning simultaneously, usually with generic advice that doesn't adapt to
their actual skill gaps or deadline. Placement Copilot is a single personal
assistant that routes each request to the right specialist agent.

## Why Agents?

A single LLM prompt can't reliably do resume scoring, interview simulation,
*and* deadline-aware planning well at once — each needs different tools,
context, and behavior. A multi-agent architecture lets each specialist stay
focused and testable, while an orchestrator decides who handles what.

## Architecture

```
                 ┌────────────────────┐
   User  ─────►  │   root_agent        │  (orchestrator, reasoning-based
                 │  "placement_copilot"│   delegation via AgentTool)
                 └─────────┬───────────┘
             ┌─────────────┼─────────────┐
             ▼              ▼              ▼
     resume_agent   interview_agent   planner_agent
     (ATS score,     (mock Q&A,       (day-wise study
      skill gap)      evaluation)      plan, deadline-aware)
             │                             │
             └──────────────┬──────────────┘
                             ▼
                   shared tools (custom_tools.py)
                also exposed via MCP server (mcp_server/server.py)
```

## Key concepts demonstrated

| Concept | Where |
|---|---|
| Multi-agent system (ADK) | `placement_copilot/agent.py`, `sub_agents/` |
| MCP Server | `mcp_server/server.py` |
| Security features | `placement_copilot/security/guardrails.py` |
| Deployability | `Dockerfile`, `app.py` (Streamlit) |
| Agent skills / CLI | `adk run` / `adk web` (see below) |

## Setup

```bash
git clone <your-repo-url>
cd placement_copilot
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # then add your GOOGLE_API_KEY
cp .env.example placement_copilot/.env
```

Get a free Gemini API key: https://aistudio.google.com/apikey

## Run it

**Option A — ADK CLI (terminal chat):**
```bash
adk run placement_copilot
```

**Option B — ADK Dev Web UI:**
```bash
adk web
```
Open the printed URL and pick `placement_copilot` from the dropdown.

**Option C — Streamlit app (the deployable product):**
```bash
streamlit run app.py
```

**Option D — MCP server (exposes tools to any MCP client):**
```bash
python mcp_server/server.py
```

**Option E — Docker:**
```bash
docker build -t placement-copilot .
docker run -p 8501:8501 --env-file .env placement-copilot
```

## Security

- All user input passes through `sanitize_input()` before reaching the
  agent, stripping common prompt-injection phrases.
- `redact_pii()` masks phone numbers, emails, and ID-like numbers before
  anything is logged.
- No API keys are committed — `.env` is gitignored; only `.env.example`
  ships in the repo.

## Limitations / honest notes

- `estimate_resume_ats_score` and `check_skill_gap` use lightweight
  keyword heuristics, not a production ATS model.
- LeetCode/job-board integrations are stubbed for the demo; a real
  deployment would call live APIs.
