from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum


class ConditionOperator(str, Enum):
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    CONTAINS = "contains"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    IN = "in"
    NOT_IN = "not_in"


class Condition(BaseModel):
    field: str = Field(..., min_length=1, max_length=100)
    operator: ConditionOperator
    value: Any


class ActionType(str, Enum):
    LOG = "log"
    NOTIFY = "notify"
    EXECUTE = "execute"
    STORE_MEMORY = "store_memory"
    SKIP = "skip"


class Action(BaseModel):
    type: ActionType
    parameters: Dict[str, Any] = Field(default_factory=dict)


class InstinctBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field("", max_length=500)
    conditions: List[Condition] = Field(default_factory=list)
    actions: List[Action] = Field(default_factory=list)
    priority: int = Field(0, ge=0, le=100)
    enabled: bool = True


class InstinctCreate(InstinctBase):
    pass


class InstinctUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    conditions: Optional[List[Condition]] = None
    actions: Optional[List[Action]] = None
    priority: Optional[int] = Field(None, ge=0, le=100)
    enabled: Optional[bool] = None


class Instinct(InstinctBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class InstinctList(BaseModel):
    instincts: List[Instinct]
    total: int


class EvaluationContext(BaseModel):
    data: Dict[str, Any] = Field(default_factory=dict)


class EvaluationResult(BaseModel):
    instinct_id: UUID
    instinct_name: str
    matched: bool
    executed_actions: List[Dict[str, Any]] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class EvaluationResponse(BaseModel):
    results: List[EvaluationResult]
    total_evaluated: int
    total_matched: int
