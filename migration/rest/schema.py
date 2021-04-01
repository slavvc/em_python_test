from pydantic import BaseModel
from typing import List, Optional, Literal

from ..business.representation_models import Workload, Migration


class IDList(BaseModel):
    ids: List[int]


class ID(BaseModel):
    id: int


class WorkloadResponse(BaseModel):
    workload: Optional[Workload]


class MigrationResponse(BaseModel):
    migration: Optional[Migration]


class Result(BaseModel):
    success: bool


class MigrationState(BaseModel):
    state: Literal['not_started', 'running', 'error', 'success']
    error_reason: Optional[str]
