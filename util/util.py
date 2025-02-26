from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# Utility function to get LLM
async def get_llm(llmProvider, model, apiKey):
    if llmProvider == "openai":
        return ChatOpenAI(model=model, api_key=apiKey, temperature=0.7, streaming=True)
    elif llmProvider == "google":
        return ChatGoogleGenerativeAI(model=model, api_key=apiKey, temperature=0.7, streaming=True)
    else:
        raise ValueError("Invalid llProvider")
