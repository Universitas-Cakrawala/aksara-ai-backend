from fastapi import APIRouter
from src.health.controller import HealthController

routerHealth = APIRouter()


@routerHealth.get("")
async def action():
    return await HealthController.health()
