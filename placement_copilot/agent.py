"""
Root agent for Placement Copilot.

Architecture:
    root_agent (orchestrator)
        -> resume_agent    (resume review + ATS score)
        -> interview_agent (mock interview)
        -> planner_agent   (day-wise study plan)

The orchestrator doesn't do the specialist work itself — it reasons about
which sub-agent(s) the student's request needs, and delegates via AgentTool.
This mirrors ADK's "reasoning-based delegation" pattern.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents import resume_agent, interview_agent, planner_agent
from .security.guardrails import sanitize_input  # noqa: F401  (used by app.py)

root_agent = Agent(
    name="placement_copilot",
    model="gemini-2.5-flash",
    description=(
        "A personal placement-prep concierge for final-year students. "
        "Routes requests to a resume reviewer, a mock interviewer, or a "
        "study planner depending on what the student needs."
    ),
    instruction="""You are Placement Copilot, a personal AI concierge for a
final-year engineering student preparing for campus placements.

You have three specialists available as tools:
- resume_agent: for resume review, ATS scoring, skill-gap checks
- interview_agent: for mock technical/HR interview practice
- planner_agent: for building a day-wise study plan before a deadline

Decide which specialist(s) the student's message needs and delegate to them.
If the request spans more than one (e.g. "review my resume AND make me a
plan"), call multiple specialists and combine their outputs clearly under
separate headings.

Never fabricate the student's skills, scores, or projects — only work with
what they actually tell you. If information is missing (e.g. no target
role or no deadline given), ask ONE short clarifying question before
delegating.""",
    tools=[
        AgentTool(agent=resume_agent),
        AgentTool(agent=interview_agent),
        AgentTool(agent=planner_agent),
    ],
)
