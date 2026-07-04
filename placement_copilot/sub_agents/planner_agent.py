from google.adk.agents import Agent
from ..tools.custom_tools import days_until, check_skill_gap

planner_agent = Agent(
    name="planner_agent",
    model="gemini-2.5-flash",
    description=(
        "Builds a day-wise placement study plan based on the student's "
        "target date, target role, and current skill gaps."
    ),
    instruction="""You create realistic, day-wise placement prep timetables.

Rules:
1. Use `days_until` to know exactly how much time is left.
2. Use `check_skill_gap` to know what to prioritize.
3. Split each day into concrete blocks (e.g. DSA 2hrs, Core CS 1hr,
   Projects/GenAI 1hr, Aptitude 30min) — never vague ("study ML").
4. If less than 14 days remain, prioritize revision + mock
   interviews + aptitude over learning brand-new topics.
5. Output as a clean day-by-day table.""",
    tools=[days_until, check_skill_gap],
)
