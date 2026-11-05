from fastapi import APIRouter, HTTPException, status
from uuid import UUID
from typing import List, Dict, Any
from datetime import datetime

from ..models.instinct import (
    Instinct,
    InstinctCreate,
    InstinctUpdate,
    InstinctList,
    Condition,
    ConditionOperator,
    Action,
    ActionType,
    EvaluationContext,
    EvaluationResult,
    EvaluationResponse,
)

router = APIRouter(prefix="/instincts", tags=["instincts"])

_instincts: Dict[UUID, Instinct] = {}


def evaluate_condition(condition: Condition, data: Dict[str, Any]) -> bool:
    field_value = data.get(condition.field)
    if field_value is None:
        return False

    op = condition.operator
    value = condition.value

    if op == ConditionOperator.EQUALS:
        return field_value == value
    elif op == ConditionOperator.NOT_EQUALS:
        return field_value != value
    elif op == ConditionOperator.CONTAINS:
        if isinstance(field_value, str) and isinstance(value, str):
            return value in field_value
        elif isinstance(field_value, list):
            return value in field_value
        return False
    elif op == ConditionOperator.GREATER_THAN:
        try:
            return float(field_value) > float(value)
        except (ValueError, TypeError):
            return False
    elif op == ConditionOperator.LESS_THAN:
        try:
            return float(field_value) < float(value)
        except (ValueError, TypeError):
            return False
    elif op == ConditionOperator.IN:
        if isinstance(value, list):
            return field_value in value
        return False
    elif op == ConditionOperator.NOT_IN:
        if isinstance(value, list):
            return field_value not in value
        return False
    return False


def execute_action(action: Action, data: Dict[str, Any]) -> Dict[str, Any]:
    action_map = {
        ActionType.LOG: lambda p: {"type": "log", "message": p.get("message", "Action executed")},
        ActionType.NOTIFY: lambda p: {"type": "notify", "title": p.get("title", "Notification"), "body": p.get("body", "")},
        ActionType.EXECUTE: lambda p: {"type": "execute", "command": p.get("command", ""), "args": p.get("args", [])},
        ActionType.STORE_MEMORY: lambda p: {"type": "store_memory", "key": p.get("key", ""), "value": p.get("value", "")},
        ActionType.SKIP: lambda p: {"type": "skip", "reason": p.get("reason", "")},
    }
    handler = action_map.get(action.type, lambda p: {"type": "unknown"})
    return handler(action.parameters)


@router.post("", response_model=Instinct, status_code=status.HTTP_201_CREATED)
async def create_instinct(instinct_data: InstinctCreate) -> Instinct:
    instinct = Instinct(**instinct_data.model_dump())
    _instincts[instinct.id] = instinct
    return instinct


@router.get("", response_model=InstinctList)
async def list_instincts() -> InstinctList:
    instincts = list(_instincts.values())
    instincts.sort(key=lambda x: (-x.priority, x.created_at))
    return InstinctList(instincts=instincts, total=len(instincts))


@router.get("/{instinct_id}", response_model=Instinct)
async def get_instinct(instinct_id: UUID) -> Instinct:
    if instinct_id not in _instincts:
        raise HTTPException(status_code=404, detail="Instinct not found")
    return _instincts[instinct_id]


@router.put("/{instinct_id}", response_model=Instinct)
async def update_instinct(instinct_id: UUID, instinct_data: InstinctUpdate) -> Instinct:
    if instinct_id not in _instincts:
        raise HTTPException(status_code=404, detail="Instinct not found")
    instinct = _instincts[instinct_id]
    update_data = instinct_data.model_dump(exclude_unset=True)
    if update_data:
        updated = instinct.model_copy(update=update_data)
        updated.updated_at = datetime.utcnow()
        _instincts[instinct_id] = updated
        return updated
    return instinct


@router.delete("/{instinct_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instinct(instinct_id: UUID) -> None:
    if instinct_id not in _instincts:
        raise HTTPException(status_code=404, detail="Instinct not found")
    del _instincts[instinct_id]


@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_instincts(context: EvaluationContext) -> EvaluationResponse:
    results: List[EvaluationResult] = []
    total_matched = 0

    sorted_instincts = sorted(_instincts.values(), key=lambda x: (-x.priority, x.created_at))

    for instinct in sorted_instincts:
        if not instinct.enabled:
            continue

        matched = True
        for condition in instinct.conditions:
            if not evaluate_condition(condition, context.data):
                matched = False
                break

        executed_actions = []
        if matched:
            total_matched += 1
            for action in instinct.actions:
                executed_actions.append(execute_action(action, context.data))

        results.append(EvaluationResult(
            instinct_id=instinct.id,
            instinct_name=instinct.name,
            matched=matched,
            executed_actions=executed_actions,
        ))

    return EvaluationResponse(
        results=results,
        total_evaluated=len(_instincts),
        total_matched=total_matched,
    )
