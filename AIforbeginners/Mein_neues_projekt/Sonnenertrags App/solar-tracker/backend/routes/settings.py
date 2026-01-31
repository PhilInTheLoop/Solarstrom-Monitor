from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from ..database import get_all_settings, update_setting

router = APIRouter(prefix="/api/settings", tags=["settings"])

class SettingUpdate(BaseModel):
    key: str
    value: str

@router.get("")
async def list_settings():
    return get_all_settings()

@router.put("")
async def update_settings(setting: SettingUpdate):
    update_setting(setting.key, setting.value)
    return {"message": "Setting updated", "key": setting.key}

@router.put("/bulk")
async def update_settings_bulk(settings: dict):
    for key, value in settings.items():
        update_setting(key, str(value))
    return {"message": "Settings updated", "count": len(settings)}
