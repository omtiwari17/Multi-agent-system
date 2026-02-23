from crewai import Agent, LLM
import os

DEFAULT_MODEL = "gemini/gemini-2.5-flash"

def _make_llm(api_key: str, model: str = DEFAULT_MODEL):
    # Force LiteLLM path (avoid CrewAI native provider import)
    return LLM(
        model=model,
        api_key=api_key,
        # IMPORTANT: make sure provider is NOT causing native gemini import
        # Usually leaving provider unset works best with LiteLLM-style model strings.
        # If your CrewAI supports it, you can also explicitly disable native:
        use_native=False,  # <- key line (if your version supports it)
    )

def build_researcher(api_key: str, model: str = DEFAULT_MODEL):
    llm = _make_llm(api_key, model)
    return Agent(
        role="Supplier Researcher",
        goal="Find potential suppliers matching the sourcing query and return JSON only.",
        backstory="You are good at structured web research and evidence capture.",
        llm=llm,
        verbose=False,
    )

def build_writer(api_key: str, model: str = DEFAULT_MODEL):
    llm = _make_llm(api_key, model)
    return Agent(
        role="Supplier Report Writer",
        goal="Convert research dataset into ranked suppliers + markdown report.",
        backstory="You write structured, clear supplier comparisons.",
        llm=llm,
        verbose=False,
    )
