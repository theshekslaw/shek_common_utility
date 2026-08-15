from typing import Any, cast

from shek_common_utility.http import AsyncHTTPClient


class BrainClient:
    def __init__(
        self,
        *,
        base_url: str,
        auth_token: str | None = None,
        timeout: float = 60.0,
    ) -> None:
        self._http = AsyncHTTPClient(
            base_url=base_url, auth_token=auth_token, timeout=timeout
        )

    async def aclose(self) -> None:
        await self._http.aclose()

    async def ingest_paper(self, paper: dict[str, Any]) -> dict[str, Any]:
        response = await self._http.post("/ingest/paper", json=paper)
        return cast(dict[str, Any], response.json())

    async def semantic_search(self, query: str, k: int = 10) -> dict[str, Any]:
        response = await self._http.get(
            "/search/semantic", params={"q": query, "k": k}
        )
        return cast(dict[str, Any], response.json())

    async def graph_view(self, focus: str, depth: int = 2) -> dict[str, Any]:
        response = await self._http.get(
            "/graph/view", params={"focus": focus, "depth": depth}
        )
        return cast(dict[str, Any], response.json())

    async def get_paper(self, paper_id: str) -> dict[str, Any]:
        response = await self._http.get(f"/papers/{paper_id}")
        return cast(dict[str, Any], response.json())

    async def health(self) -> dict[str, Any]:
        response = await self._http.get("/health")
        return cast(dict[str, Any], response.json())
