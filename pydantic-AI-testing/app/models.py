"""Output schemas"""

from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.registry import APPROVED_ORG_IDS, EVIDENCE_IDS, RESEARCHER_IDS

# --- tier 0: profile -------------------------------------------------------


class WasteStream(BaseModel):
    name: str
    estimate: str = Field(
        description="Rough annual volume with units, flagged as estimated"
    )
    timing: str = Field(description="When in the year it arises")
    condition: str = Field(description="Physical state, moisture, contamination")
    disposal: str = Field(description="What most likely happens to it now")
    signal: str = Field(description="One sentence on why someone else might want it")


class StreamProfile(BaseModel):
    streams: list[WasteStream] = Field(min_length=4, max_length=6)


# --- tier 1: listing -------------------------------------------------------


class Spec(BaseModel):
    label: str
    value: str


class Listing(BaseModel):
    title: str = Field(description="Short and plain, no marketing language")
    summary: str = Field(description="Two or three sentences, honest about condition")
    specs: list[Spec] = Field(
        min_length=4,
        max_length=6,
        description="Volume, availability window, condition, contaminants, handling, location",
    )
    terms: str = Field(description="One line on what the farm is offering")
    flags: list[str] = Field(
        max_length=3, description="Genuine barriers a taker should know about"
    )


# --- tier 2: approved organisations ---------------------------------------


class OrgMatch(BaseModel):
    id: str
    fit: int = Field(ge=0, le=100)
    rationale: str
    gap: str = Field(description="What would have to be true for this to work")
    step: str = Field(description="A concrete next action for the farmer")

    @field_validator("id")
    @classmethod
    def must_be_in_register(cls, v: str) -> str:
        if v not in APPROVED_ORG_IDS:
            raise ValueError(
                f"{v} is not in the approved register. "
                f"Use only these ids: {sorted(APPROVED_ORG_IDS)}"
            )
        return v


class OrgMatches(BaseModel):
    matches: list[OrgMatch] = Field(min_length=1, max_length=3)


# --- tier 3: research ------------------------------------------------------


class Application(BaseModel):
    application: str
    maturity: Literal["commercial", "pilot", "lab only", "unevidenced"]
    evidence: str = Field(description="One sentence on what is actually known")
    caveat: str = Field(description="One sentence on the main unknown or constraint")
    source_id: str | None = Field(
        default=None,
        description=(
            "The id of the evidence entry supporting this application. Use null "
            "only when no entry in the evidence file covers it — in which case "
            "maturity must be 'unevidenced'."
        ),
    )

    @field_validator("source_id")
    @classmethod
    def must_be_known_evidence(cls, v: str | None) -> str | None:
        if v is not None and v not in EVIDENCE_IDS:
            raise ValueError(
                f"{v} is not in the evidence file. Cite one of "
                f"{sorted(EVIDENCE_IDS)}, or return null and set maturity to 'unevidenced'."
            )
        return v


class ResearcherMatch(BaseModel):
    id: str
    why: str
    question: str = Field(description="One specific question the farmer should ask")

    @field_validator("id")
    @classmethod
    def must_be_in_directory(cls, v: str) -> str:
        if v not in RESEARCHER_IDS:
            raise ValueError(
                f"{v} is not in the researcher directory. "
                f"Use only these ids: {sorted(RESEARCHER_IDS)}"
            )
        return v


class ResearchBrief(BaseModel):
    applications: list[Application] = Field(min_length=3, max_length=4)
    matches: list[ResearcherMatch] = Field(min_length=2, max_length=3)
    outreach: str = Field(
        description="A 90-word email the farmer can send, plain and specific"
    )
