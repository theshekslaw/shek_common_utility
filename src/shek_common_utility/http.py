from types import TracebackType
from typing import Any, Self

import httpx


class AsyncHTTPClient:
    def __init__(
        self,
        *,
        base_url: str,
        auth_token: str | None = None,
        timeout: float = 30.0,
        default_headers: dict[str, str] | None = None,
    ) -> None:
        headers: dict[str, str] = {"Accept": "application/json"}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        if default_headers:
            headers.update(default_headers)

        transport = httpx.AsyncHTTPTransport(retries=2)
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers=headers,
            timeout=timeout,
            transport=transport,
        )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self._client.aclose()

    async def get(self, path: str, **kwargs: Any) -> httpx.Response:
        response = await self._client.get(path, **kwargs)
        response.raise_for_status()
        return response

    async def post(self, path: str, *, json: Any = None, **kwargs: Any) -> httpx.Response:
        response = await self._client.post(path, json=json, **kwargs)
        response.raise_for_status()
        return response

    async def stream(
        self, method: str, path: str, **kwargs: Any
    ) -> httpx.Response:
        request = self._client.build_request(method, path, **kwargs)
        return await self._client.send(request, stream=True)
