"""Pydantic data models — the shared contract across LLM, Compute, and API layers.

Mirrors §3 of decision_debugger_design.md.
"""
from __future__ import annotations

import uuid
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


class State(str, Enum):
    SETUP = "SETUP"
    ANALYZE = "ANALYZE"
    QUESTIONING = "QUESTIONING"
    RESULT = "RESULT"


class Option(BaseModel):
    id: str
    name: str
    description: str = ""


class Factor(BaseModel):
    id: str
    name: str
    description: str = ""
    type: Literal["concrete", "abstract"] = "concrete"
    direction: Literal["higher_better", "lower_better"] = "higher_better"
    importance: float = 1.0  # LLM-decided initial importance -> WeightState.prior
    relevance: str = ""


class Score(BaseModel):
    value: float  # normalized-ish [0,1] as decided by the LLM (re-normalized in compute)
    rationale: str = ""


class WeightState(BaseModel):
    prior: dict[str, float] = Field(default_factory=dict)    # factor_id -> w (LLM)
    current: dict[str, float] = Field(default_factory=dict)  # factor_id -> w (refined)


class Question(BaseModel):
    id: str
    kind: Literal["weight_pairwise", "sub_question"]
    payload: dict[str, Any] = Field(default_factory=dict)
    status: Literal["pending", "answered"] = "pending"


class Answer(BaseModel):
    question_id: str
    value: Any
    timestamp: float


class Result(BaseModel):
    utilities: dict[str, float] = Field(default_factory=dict)
    ranking: list[str] = Field(default_factory=list)  # option_ids best -> worst
    sensitivity: dict[str, Any] = Field(default_factory=dict)
    robustness: str = "stable"  # "stable" | "close"
    report: str = ""
    next_info: list[str] = Field(default_factory=list)
    conflict: list[dict[str, Any]] = Field(default_factory=list)


class DecisionSession(BaseModel):
    id: str
    status: State = State.SETUP
    context: str = ""
    context_summary: str = ""
    options: list[Option] = Field(default_factory=list)
    factors: list[Factor] = Field(default_factory=list)
    weights: WeightState = Field(default_factory=WeightState)
    # option_id -> factor_id -> Score
    score_matrix: dict[str, dict[str, Score]] = Field(default_factory=dict)
    # option_id -> factor_id -> normalized value in [0,1]
    norm_scores: dict[str, dict[str, float]] = Field(default_factory=dict)
    # "factorA_id||factorB_id" -> {question, example_a, example_b}
    pairwise_verbalizations: dict[str, dict[str, str]] = Field(default_factory=dict)
    questions: list[Question] = Field(default_factory=list)
    answers: list[Answer] = Field(default_factory=list)
    result: Optional[Result] = None
    # while resolving a "잘 모르겠어요" via recursive sub-questions (§6.3):
    # {"root_id", "factor_a_id", "factor_b_id", "depth"} — None when not decomposing
    active_decomposition: Optional[dict[str, Any]] = None

    # --- convenience lookups ---
    def factor(self, factor_id: str) -> Optional[Factor]:
        return next((f for f in self.factors if f.id == factor_id), None)

    def option(self, option_id: str) -> Optional[Option]:
        return next((o for o in self.options if o.id == option_id), None)

    def question(self, question_id: str) -> Optional[Question]:
        return next((q for q in self.questions if q.id == question_id), None)


# ---------- API request/response DTOs ----------

class CreateSessionRequest(BaseModel):
    context: str


class AnswerRequest(BaseModel):
    question_id: str
    value: Any
