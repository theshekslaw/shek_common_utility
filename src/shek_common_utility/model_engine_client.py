from typing import Any, cast

from pydantic import BaseModel

from shek_common_utility.http import AsyncHTTPClient


class TaskInvocation(BaseModel):
    task: str
    input: dict[str, Any]


class ModelEngineClient:
    def __init__(
        self,
        *,
        base_url: str,
        auth_token: str | None = None,
        timeout: float = 300.0,
    ) -> None:
        self._http = AsyncHTTPClient(
            base_url=base_url, auth_token=auth_token, timeout=timeout
        )

    async def aclose(self) -> None:
        await self._http.aclose()

    async def list_tasks(self) -> list[dict[str, Any]]:
        response = await self._http.get("/tasks")
        return cast(list[dict[str, Any]], response.json())

    async def run_task(self, task: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = await self._http.post(f"/task/{task}", json=payload)
        return cast(dict[str, Any], response.json())

    async def health(self) -> dict[str, Any]:
        response = await self._http.get("/health")
        return cast(dict[str, Any], response.json())
