from __future__ import annotations
from typing import Literal, List
from pathlib import Path
import yaml
from pydantic import BaseModel, Field, model_validator


class GeometryScan(BaseModel):
    """Bond‑length or angle scan definition."""

    param: Literal["r", "angle"] = "r"
    range: str = Field(description="format 'start:stop:step', e.g. '1.4:3.4:0.2'")


class Experiment(BaseModel):
    system: str
    basis_set: str = "sto-3g"
    qubit_budget: int
    ansatz: List[str]
    optimiser: List[str]
    backends: List[str]
    noise_mitigation: List[str] = ["none"]
    geometry_scan: GeometryScan

    # ---------- helpers ----------
    @classmethod
    def load(cls, path: str | Path) -> "Experiment":
        with open(path, "r", encoding="utf-8") as fh:
            return cls(**yaml.safe_load(fh))

    @model_validator(mode="after")
    def _validate_budget(self):
        if self.qubit_budget <= 0:
            raise ValueError("qubit_budget must be > 0")
        return self
