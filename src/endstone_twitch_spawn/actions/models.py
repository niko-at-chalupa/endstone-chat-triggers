from __future__ import annotations
from enum import Enum
from pathlib import Path

from typing import List
from pydantic import BaseModel, Field


class Condition(BaseModel):
    command: str
    expected: bool

    source_line: int | None = None
    source_file: Path | None = None

    def resolve(self, actual: bool) -> ResolvedCondition:
        return ResolvedCondition(**self.model_dump(), actual=actual)


class ResolvedCondition(Condition):
    actual: bool


class Workflow(BaseModel):
    name: str
    event_names: List[str] = Field(default_factory=list)
    conditions: List[Condition] = Field(default_factory=list)
    steps: List[str] = Field(default_factory=list)
    fail_steps: List[str] = Field(default_factory=list)

    source_file: Path | None = None
    source_line: int | None = None


class ExecutionResult(BaseModel):
    workflow_name: str
    triggered: bool
    ran_steps: List[str] = Field(default_factory=list)
    condition_results: List[ResolvedCondition] = Field(default_factory=list)


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"


class Issue(BaseModel):
    name: str | None = None
    file: Path
    source_line: int
    severity: Severity
    help: str | None = None
    code: str


class FailedWorkflow(BaseModel):
    name: str | None = None
    file: Path
    issues: list[Issue] = Field(default_factory=list)
