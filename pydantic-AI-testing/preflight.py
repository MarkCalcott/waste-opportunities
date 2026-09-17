"""Preflight. Run this before anything else.

    python preflight.py

Three checks in the order things break. Each failure prints the fix rather
than a stack trace, because at this stage the problem is almost always a
missing key or an unfunded account, not the code.
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

OK, BAD, DIM, OFF = "\033[32m✓\033[0m", "\033[31m✗\033[0m", "\033[2m", "\033[0m"


def fail(msg: str, fix: str) -> None:
    print(f"{BAD} {msg}\n{DIM}   {fix}{OFF}\n")
    sys.exit(1)


def main() -> None:
    model_name = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")

    # 1 — key present --------------------------------------------------------
    if not os.environ.get("ANTHROPIC_API_KEY"):
        fail(
            "ANTHROPIC_API_KEY is not set",
            "cp .env.example .env, then paste a key from "
            "https://console.anthropic.com/settings/keys",
        )
    print(f"{OK} Key found\n{OK} Model  {model_name}\n")

    # 2 — SDK installed and a real call --------------------------------------
    try:
        from anthropic import Anthropic, APIStatusError, AuthenticationError
    except ImportError:
        fail("anthropic SDK not installed", "pip install -r requirements-cli.txt")

    client = Anthropic()
    try:
        r = client.messages.create(
            model=model_name,
            max_tokens=10,
            messages=[{"role": "user", "content": "Reply with the word: ready"}],
        )
        print(f"{OK} API call  {r.content[0].text.strip()}\n")
    except AuthenticationError:
        fail("Key rejected", "The key is wrong, revoked, or from a different org. Generate a fresh one.")
    except APIStatusError as e:
        if e.status_code == 429:
            fail(
                "Rate limited or out of credit",
                "New accounts start with low limits and need credit on the billing page. "
                "Add a little credit at console.anthropic.com/settings/billing.",
            )
        if e.status_code == 404:
            fail(f"Model '{model_name}' not found", "Check ANTHROPIC_MODEL in .env for a typo.")
        fail(f"API error {e.status_code}: {e.message}", "The message above is from the API directly.")

    # 3 — structured output through Pydantic AI ------------------------------
    try:
        from pydantic import BaseModel
        from pydantic_ai import Agent
        from pydantic_ai.models.anthropic import AnthropicModel
    except ImportError:
        fail("pydantic-ai not installed", "pip install -r requirements-cli.txt")

    class Check(BaseModel):
        crop: str
        residue: str

    agent = Agent(AnthropicModel(model_name), output_type=Check)
    out = agent.run_sync("A Marlborough vineyard. Name the crop and its main residue.")
    print(f"{OK} Structured output  {out.output.model_dump()}\n")

    print("All three passed. Run: python cli.py --example --stream 1")


if __name__ == "__main__":
    main()
