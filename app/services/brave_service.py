from __future__ import annotations

import httpx


class BraveSearchError(RuntimeError):
    """Raised when Brave Search returns a recoverable API error."""


class BraveService:
    BASE_URL = "https://api.search.brave.com/res/v1/web/search"

    def __init__(self, api_key: str | None) -> None:
        self.api_key = api_key

    async def search(self, topic: str, count: int = 5) -> list[dict[str, str]]:
        if not self.api_key:
            raise BraveSearchError("BRAVE_API_KEY is not configured.")
        params = {"q": topic, "count": count, "search_lang": "en"}
        headers = {"Accept": "application/json", "X-Subscription-Token": self.api_key}
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(self.BASE_URL, params=params, headers=headers)
        if response.is_error:
            try:
                payload = response.json()
                detail = payload.get("error", {}).get("detail")
                code = payload.get("error", {}).get("code")
            except ValueError:
                detail = response.text
                code = None
            message = detail or "Brave search request failed."
            if code:
                message = f"{message} ({code})"
            raise BraveSearchError(message)
        payload = response.json()
        results = payload.get("web", {}).get("results", [])
        normalized: list[dict[str, str]] = []
        for item in results[:count]:
            normalized.append(
                {
                    "title": item.get("title", ""),
                    "description": item.get("description", ""),
                    "url": item.get("url", ""),
                    "age": item.get("age", ""),
                    "profile_name": item.get("profile", {}).get("name", ""),
                }
            )
        return normalized
