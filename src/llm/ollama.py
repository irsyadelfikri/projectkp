from langchain_ollama import ChatOllama

from src.config.settings import LLM_MODEL


def create_llm() -> ChatOllama:

    return ChatOllama(
        model=LLM_MODEL,
        temperature=0,
    )