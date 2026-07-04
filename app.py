"""
Streamlit UI for Placement Copilot.
Run with: streamlit run app.py
"""

import asyncio
import os

import streamlit as st
from dotenv import load_dotenv

from google.adk.runners import InMemoryRunner
from google.genai import types

from placement_copilot.agent import root_agent
from placement_copilot.security.guardrails import sanitize_input

load_dotenv()

st.set_page_config(page_title="Placement Copilot", page_icon="🎯")
st.title("🎯 Placement Copilot")
st.caption("Your personal AI concierge for campus placement prep")

if "GOOGLE_API_KEY" not in os.environ:
    st.error("GOOGLE_API_KEY not set. Add it to your .env file.")
    st.stop()

if "runner" not in st.session_state:
    st.session_state.runner = InMemoryRunner(agent=root_agent, app_name="placement_copilot")
    st.session_state.session_id = None
    st.session_state.messages = []


async def _ensure_session():
    if st.session_state.session_id is None:
        session = await st.session_state.runner.session_service.create_session(
            app_name="placement_copilot", user_id="student_1"
        )
        st.session_state.session_id = session.id


async def _run_agent(user_text: str) -> str:
    await _ensure_session()
    content = types.Content(role="user", parts=[types.Part(text=user_text)])
    reply = ""
    async for event in st.session_state.runner.run_async(
        user_id="student_1",
        session_id=st.session_state.session_id,
        new_message=content,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    reply += part.text
    return reply


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about your resume, request a mock interview, or a study plan...")

if user_input:
    clean_input = sanitize_input(user_input)
    st.session_state.messages.append({"role": "user", "content": clean_input})
    with st.chat_message("user"):
        st.markdown(clean_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = asyncio.run(_run_agent(clean_input))
            st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
