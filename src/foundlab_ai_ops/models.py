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


class Provider(str, Enum):
    deterministic = "deterministic"
    openai = "openai"
    google = "google"


class ExecutionMode(str, Enum):
    interactive = "interactive"
    standard = "standard"
    background = "background"
    flex = "flex"
    batch = "batch"


class ComputeClass(str, Enum):
    economy = "economy"
    balanced = "balanced"
    professional = "professional"
    frontier = "frontier"


class TaskExecution(BaseModel):
    type: str = "general"
    remote_writes: bool = False
    destructive_operations: bool = False
    provider_preference: Provider | None = None
    surface_preference: str | None = None
    execution_mode_preference: ExecutionMode | None = None


class TaskRequirements(BaseModel):
    repositories: bool = False
    web: bool = False
    github: bool = False
    gcp: bool = False
    google_docs: bool = False
    linear: bool = False
    drive: bool = False
    managed_mcp: list[str] = Field(default_factory=list)


class TaskExpected(BaseModel):
    complexity: Complexity = Complexity.medium
    ambiguity: Literal["low", "medium", "high"] = "medium"
    latency: Literal["interactive", "normal", "deferred"] = "normal"
    repetitive: bool = False
    adversarial_review: bool = False
    unresolved_after_escalation: bool = False


class TaskVerification(BaseModel):
    required: bool = True
    commands: list[str] = Field(default_factory=list)


class RequestedAction(BaseModel):
    system: str
    action: str


class PermissionCheck(BaseModel):
    system: str
    action: str
    result: Literal["allow", "review", "deny", "explicit"]


class Task(BaseModel):
    id: str
    objective: str
    risk: Risk = Risk.medium
    execution: TaskExecution = Field(default_factory=TaskExecution)
    requirements: TaskRequirements = Field(default_factory=TaskRequirements)
    expected: TaskExpected = Field(default_factory=TaskExpected)
    verification: TaskVerification = Field(default_factory=TaskVerification)
    requested_actions: list[RequestedAction] = Field(default_factory=list)


class Decision(BaseModel):
    decision: DecisionStatus
    profile: str
    provider: Provider
    surface: str
    execution_mode: ExecutionMode
    compute_class: ComputeClass
    reasoning: str
    fast_mode: bool
    max_agents: int
    sandbox: str
    external_writes: bool
    required_sources: list[str]
    required_checks: list[str]
    managed_mcp: list[str] = Field(default_factory=list)
    telemetry_required: bool = True
    permission_checks: list[PermissionCheck] = Field(default_factory=list)
    rationale: list[str] = Field(default_factory=list)
