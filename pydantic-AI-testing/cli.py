"""Run the whole cascade in the terminal. No server, no browser.

    python cli.py                 # you type the operation
    python cli.py --example       # Wairarapa vineyard, straight through
    python cli.py --stream 2      # skip the picker, take stream 2

"""

import argparse
import asyncio
import json
import sys

from dotenv import load_dotenv

load_dotenv()

from app import agents  # noqa: E402
from app.registry import APPROVED_ORGS, EVIDENCE, RESEARCHERS  # noqa: E402

DIM, BOLD, GREEN, AMBER, BLUE, OFF = (
    "\033[2m",
    "\033[1m",
    "\033[32m",
    "\033[33m",
    "\033[34m",
    "\033[0m",
)

EXAMPLE = """We run 240 hectares in the Wairarapa - about 180 ha in Sauvignon Blanc and \
Pinot Noir, plus a small kiwifruit block on the flats. Harvest runs late February \
through April. Right now we pay a contractor to cart the grape marc away, and we burn \
most of the winter prunings on the headlands. The winery also generates spent \
diatomaceous earth from filtration, and we've got several years of end-of-life bird \
netting stacked behind the implement shed."""


def rule(label: str, colour: str = "") -> None:
    print(f"\n{colour}{BOLD}{label}{OFF}")
    print(f"{DIM}{'-' * 72}{OFF}")


def lookup(items: list[dict], id_: str) -> dict:
    return next((i for i in items if i["id"] == id_), {})


async def run(description: str, stream_choice: int | None) -> None:
    rule("Reading the operation")
    profile = await agents.profile_operation(description)

    for i, s in enumerate(profile.streams, 1):
        print(f"\n {BOLD}{i}. {s.name}{OFF}  {DIM}{s.estimate}{OFF}")
        print(f"    {s.signal}")
        print(f"    {DIM}{s.timing} | {s.condition} | now: {s.disposal}{OFF}")

    if stream_choice is None:
        raw = input(f"\n{BOLD}Which stream? [1]{OFF} ").strip()
        stream_choice = int(raw) if raw else 1
    stream = profile.streams[stream_choice - 1]
    print(f"\n{DIM}Taking: {stream.name}{OFF}")

    # ---- tier 1 ----------------------------------------------------------
    rule("Tier 1 - open marketplace", GREEN)
    listing = await agents.draft_listing(stream.model_dump(), description)
    print(f"\n {BOLD}{listing.title}{OFF}\n\n {listing.summary}\n")
    for sp in listing.specs:
        print(f"    {sp.label:<22} {DIM}{sp.value}{OFF}")
    print(f"    {'Terms':<22} {DIM}{listing.terms}{OFF}")
    if listing.flags:
        print(f"\n    {AMBER}flags:{OFF} " + " | ".join(listing.flags))

    print(f"\n {DIM}No taker above threshold. Escalating.{OFF}")

    # ---- tier 2 ----------------------------------------------------------
    rule("Tier 2 - approved organisations", AMBER)
    orgs = await agents.match_organisations(stream.model_dump(), listing.model_dump())
    for m in orgs.matches:
        org = lookup(APPROVED_ORGS, m.id)
        print(f"\n {BOLD}{org.get('name', m.id)}{OFF}  {DIM}fit {m.fit} | {m.id}{OFF}")
        print(f"    {m.rationale}")
        print(f"    {DIM}gap:  {m.gap}{OFF}")
        print(f"    next: {m.step}")
        print(f"    {DIM}{org.get('region', '')}{OFF}")

    # ---- tier 3 ----------------------------------------------------------
    rule("Tier 3 - research programmes", BLUE)
    brief = await agents.build_research_brief(stream.model_dump(), listing.model_dump())

    for a in brief.applications:
        src = lookup(EVIDENCE, a.source_id) if a.source_id else {}
        cite = src.get("source_url", "no NZ evidence on file")
        print(f"\n {BOLD}{a.application}{OFF}  {DIM}[{a.maturity}]{OFF}")
        print(f"    {a.evidence}")
        print(f"    {DIM}{a.caveat}{OFF}")
        print(f"    {DIM}source: {cite}{OFF}")

    for m in brief.matches:
        r = lookup(RESEARCHERS, m.id)
        print(f"\n {BOLD}{r.get('name', m.id)}{OFF}\n    {DIM}{r.get('unit', '')}{OFF}")
        print(f"    {m.why}")
        print(f"    {BLUE}ask:{OFF} {m.question}")

    print(f"\n{DIM}{'-' * 72}{OFF}\n{brief.outreach}\n")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--example", action="store_true", help="use the Wairarapa vineyard")
    p.add_argument("--stream", type=int, default=None, help="pick a stream, skip the prompt")
    p.add_argument("--json", action="store_true", help="dump raw model output and exit")
    args = p.parse_args()

    if args.example:
        description = EXAMPLE
        print(f"{DIM}{EXAMPLE}{OFF}")
    else:
        print("Describe the operation. Blank line to finish.\n")
        lines: list[str] = []
        while (line := sys.stdin.readline().rstrip("\n")) != "":
            lines.append(line)
        description = " ".join(lines)

    if args.json:
        profile = asyncio.run(agents.profile_operation(description))
        print(json.dumps(profile.model_dump(), indent=2))
        return

    asyncio.run(run(description, args.stream))


if __name__ == "__main__":
    main()
