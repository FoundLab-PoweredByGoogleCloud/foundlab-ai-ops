from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class Risk(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Complexity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    frontier = "frontier"


class DecisionStatus(str, Enum):
    allow = "ALLOW"
    review = "REVIEW"
    deny = "DENY"
    blocked = "BLOCKED"


class TaskExecution(BaseModel):
    type: str = "general"
    remote_writes: bool = False
    destructive_operations: bool = False


class TaskRequirements(BaseModel):
    repositories: bool = False
    web: bool = False
    github: bool = False
    gcp: bool = False
    linear: bool = False
    drive: bool = False


class TaskExpected(BaseModel):
    complexity: Complexity = Complexity.medium
    ambiguity: Literal["low", "medium", "high"] = "medium"
    repetitive: bool = False
    adversarial_review: bool = False
    unresolved_after_escalation: bool = False


class TaskVerification(BaseModel):
    required: bool = True
    commands: list[str] = Field(default_factory=list)


class Task(BaseModel):
    id: str
    objective: str
    risk: Risk = Risk.medium
    execution: TaskExecution = Field(default_factory=TaskExecution)
    requirements: TaskRequirements = Field(default_factory=TaskRequirements)
    expected: TaskExpected = Field(default_factory=TaskExpected)
    verification: TaskVerification = Field(default_factory=TaskVerification)


class Decision(BaseModel):
    decision: DecisionStatus
    profile: str
    model_class: str
    reasoning: str
    fast_mode: bool
    max_agents: int
    sandbox: str
    external_writes: bool
    required_sources: list[str]
    required_checks: list[str]
    rationale: list[str] = Field(default_factory=list)
