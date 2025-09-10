from starlette.responses import JSONResponse
from src.health.schemas import ok
from src.health.schemas import formatError


class HealthController:
    @staticmethod
    async def health() -> JSONResponse:
        try:
            response = {
                "success": True,
            }

            return ok(response, "Server running successfully!")
        except Exception as e:
            return formatError("", f"{e}")
