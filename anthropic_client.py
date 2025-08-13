# anthropic_client.py
import os
from dotenv import load_dotenv
from anthropic import Anthropic
import httpx
load_dotenv()
http_client = httpx.Client(verify=False)
_CLIENT = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"),http_client=http_client)

def ask_claude(prompt: str, model: str = "claude-sonnet-4-20250514", max_tokens: int = 800) -> str:
    """
    Return assistant text response as a plain string.
    """
    resp = _CLIENT.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )
    # adapt for the Anthropic SDK shape used earlier; fallback safely:
    try:
        return resp.content[0].text
    except Exception:
        # best-effort: if direct attribute missing, try str(resp)
        return str(resp)
