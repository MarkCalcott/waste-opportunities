import json
import os

from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel

from app.models import Listing, OrgMatches, ResearchBrief, StreamProfile
from app.registry import APPROVED_ORGS, EVIDENCE, RESEARCHERS

MODEL_NAME = os.environ.get("ANTHROPIC_MODEL")

model = AnthropicModel(MODEL_NAME)

# Incorrect call of missed pydantic validation
RETRIES = 2

profiler = Agent(
    model,
    output_type=StreamProfile,
    retries=RETRIES,
    system_prompt=(
        "You are a circular-economy analyst for agriculture. Given a description of a "
        "farming operation, identify the distinct waste or residue streams it generates, "
        "including ones the operator did not mention but which the operation type clearly "
        "implies. Volumes are estimates from operation type and scale — say so."
    ),
)

lister = Agent(
    model,
    output_type=Listing,
    retries=RETRIES,
    system_prompt=(
        "You write listings for a free agricultural by-product marketplace. Produce a "
        "listing a potential taker can act on. No marketing language. Be honest about "
        "condition and name the genuine barriers rather than hiding them."
    ),
)

matcher = Agent(
    model,
    output_type=OrgMatches,
    retries=RETRIES,
    system_prompt=(
        "You match an unwanted agricultural residue against a register of approved "
        "receiving organisations. Use only organisations from the register you are given "
        "— never invent one. Do not manufacture certainty: name what would have to change "
        "for each match to actually work."
    ),
)

briefer = Agent(
    model,
    output_type=ResearchBrief,
    retries=RETRIES,
    system_prompt=(
        "You brief a farmer on the research position for an agricultural residue, then "
        "connect them to research programmes. Use only entries from the directory you are "
        "given. Every application you claim must cite an id from the evidence file. If "
        "nothing in the evidence file covers it, say so — return a null source and mark "
        "it unevidenced. Never present an application as established when the file does "
        "not support it: no New Zealand work on this stream is a genuinely useful answer "
        "for the farmer."
    ),
)


async def profile_operation(description: str) -> StreamProfile:
    result = await profiler.run(f"Operation description:\n\n{description}")
    return result.output


async def draft_listing(stream: dict, farm: str) -> Listing:
    result = await lister.run(
        f"Stream:\n{json.dumps(stream, indent=2)}\n\nOperation context:\n{farm}"
    )
    return result.output


async def match_organisations(stream: dict, listing: dict) -> OrgMatches:
    result = await matcher.run(
        f"Stream:\n{json.dumps(stream, indent=2)}\n\n"
        f"Listing:\n{json.dumps(listing, indent=2)}\n\n"
        f"Approved register:\n{json.dumps(APPROVED_ORGS, indent=2)}"
    )
    return result.output


async def build_research_brief(stream: dict, listing: dict) -> ResearchBrief:
    result = await briefer.run(
        f"Stream:\n{json.dumps(stream, indent=2)}\n\n"
        f"Listing:\n{json.dumps(listing, indent=2)}\n\n"
        f"Research directory:\n{json.dumps(RESEARCHERS, indent=2)}\n\n"
        f"Evidence file:\n{json.dumps(EVIDENCE, indent=2)}"
    )
    return result.output
