from fastapi import APIRouter, HTTPException, status
from uuid import UUID
from typing import List, Dict, Any
from datetime import datetime

from ..models.memory import (
    Memory,
    MemoryCreate,
    MemoryUpdate,
    MemoryList,
)

router = APIRouter(prefix="/memory", tags=["memory"])

_memories: Dict[UUID, Memory] = {}


@router.post("", response_model=Memory, status_code=status.HTTP_201_CREATED)
async def create_memory(memory_data: MemoryCreate) -> Memory:
    memory = Memory(**memory_data.model_dump())
    _memories[memory.id] = memory
    return memory


@router.get("", response_model=MemoryList)
async def list_memories() -> MemoryList:
    memories = list(_memories.values())
    return MemoryList(memories=memories, total=len(memories))


@router.get("/{memory_id}", response_model=Memory)
async def get_memory(memory_id: UUID) -> Memory:
    if memory_id not in _memories:
        raise HTTPException(status_code=404, detail="Memory not found")
    return _memories[memory_id]


@router.put("/{memory_id}", response_model=Memory)
async def update_memory(memory_id: UUID, memory_data: MemoryUpdate) -> Memory:
    if memory_id not in _memories:
        raise HTTPException(status_code=404, detail="Memory not found")
    memory = _memories[memory_id]
    update_data = memory_data.model_dump(exclude_unset=True)
    if update_data:
        updated = memory.model_copy(update=update_data)
        updated.updated_at = datetime.utcnow()
        _memories[memory_id] = updated
        return updated
    return memory


@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memory(memory_id: UUID) -> None:
    if memory_id not in _memories:
        raise HTTPException(status_code=404, detail="Memory not found")
    del _memories[memory_id]
