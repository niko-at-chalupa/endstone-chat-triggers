from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field


class ConditionCheck(BaseModel):
    """
    A single condition: run `command`, and require that the command's success/failure matches `expected`.

    conditions:
      - testfor Chalupa7235: true # -> command="testfor Chalupa7235", expected=True
    """
    command: str
    expected: bool
    # Whereever this condition came from, for logs
    source_line: int | None = None


class Workflow(BaseModel):
    name: str
    event_name: str
    conditions: List[ConditionCheck] = Field(default_factory=list)
    steps: List[str] = Field(default_factory=list)
    # Path of the file this workflow was loaded from, for logs/errors.
    source_file: str | None = None
    source_line: int | None = None