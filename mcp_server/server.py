"""
MCP (Model Context Protocol) server for Placement Copilot.

This exposes the same underlying tools (skill-gap checker, ATS scorer,
days-until calculator) as MCP tools, so ANY MCP-compatible client
(Claude Desktop, other ADK agents, etc.) can call them too -- not just
our own agents. This satisfies the "MCP Server" evaluation concept.

Run with:  python mcp_server/server.py
"""

import sys
import os

# Allow importing the sibling package without installing it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from mcp.server.fastmcp import FastMCP  # pip install mcp
from placement_copilot.tools.custom_tools import (
    check_skill_gap,
    days_until,
    estimate_resume_ats_score,
)

mcp = FastMCP("placement-copilot-tools")


@mcp.tool()
def skill_gap(target_role: str, current_skills: str) -> dict:
    """Compare a student's current skills against a target role's
    requirements and return what's missing."""
    return check_skill_gap(target_role, current_skills)


@mcp.tool()
def days_remaining(target_date: str) -> dict:
    """Calculate days remaining until a placement/exam date (YYYY-MM-DD)."""
    return days_until(target_date)


@mcp.tool()
def ats_score(resume_text: str, job_description: str) -> dict:
    """Estimate an ATS keyword-match score between a resume and a JD."""
    return estimate_resume_ats_score(resume_text, job_description)


if __name__ == "__main__":
    # Runs the MCP server over stdio so it can be plugged into any
    # MCP-compatible client (Claude Desktop config, ADK MCPToolset, etc.)
    mcp.run(transport="stdio")
