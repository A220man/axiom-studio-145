from fastapi import APIRouter, HTTPException, status
from uuid import UUID
from typing import List
from datetime import datetime

from ..models.skill import Skill, SkillCreate, SkillUpdate, SkillList

router = APIRouter(prefix="/skills", tags=["skills"])

_skills: dict[UUID, Skill] = {}


@router.post("", response_model=Skill, status_code=status.HTTP_201_CREATED)
async def create_skill(skill_data: SkillCreate) -> Skill:
    skill = Skill(**skill_data.model_dump())
    _skills[skill.id] = skill
    return skill


@router.get("", response_model=SkillList)
async def list_skills() -> SkillList:
    skills = list(_skills.values())
    return SkillList(skills=skills, total=len(skills))


@router.get("/{skill_id}", response_model=Skill)
async def get_skill(skill_id: UUID) -> Skill:
    if skill_id not in _skills:
        raise HTTPException(status_code=404, detail="Skill not found")
    return _skills[skill_id]


@router.put("/{skill_id}", response_model=Skill)
async def update_skill(skill_id: UUID, skill_data: SkillUpdate) -> Skill:
    if skill_id not in _skills:
        raise HTTPException(status_code=404, detail="Skill not found")
    skill = _skills[skill_id]
    update_data = skill_data.model_dump(exclude_unset=True)
    if update_data:
        updated = skill.model_copy(update=update_data)
        updated.updated_at = datetime.utcnow()
        _skills[skill_id] = updated
        return updated
    return skill


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(skill_id: UUID) -> None:
    if skill_id not in _skills:
        raise HTTPException(status_code=404, detail="Skill not found")
    del _skills[skill_id]
