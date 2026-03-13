from __future__ import annotations

from urllib.parse import quote_plus
from xml.etree import ElementTree

import httpx


class PublicHotspotError(RuntimeError):
    """Raised when the public hotspot feed cannot be fetched or parsed."""


class PublicHotspotService:
    BASE_URL = "https://news.google.com/rss/search"

    async def search(self, topic: str, count: int = 5) -> list[dict[str, str]]:
        query = quote_plus(topic)
        url = f"{self.BASE_URL}?q={query}&hl=en-US&gl=US&ceid=US:en"
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.get(url, headers={"Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8"})
        if response.is_error:
            raise PublicHotspotError(f"Public hotspot request failed: {response.status_code}")
        try:
            root = ElementTree.fromstring(response.text)
        except ElementTree.ParseError as exc:
            raise PublicHotspotError("Failed to parse public hotspot feed.") from exc
        results: list[dict[str, str]] = []
        for item in root.findall("./channel/item")[:count]:
            title = (item.findtext("title") or "").strip()
            description = (item.findtext("description") or "").strip()
            link = (item.findtext("link") or "").strip()
            pub_date = (item.findtext("pubDate") or "").strip()
            source = ""
            title_bits = [bit.strip() for bit in title.split(" - ") if bit.strip()]
            if len(title_bits) >= 2:
                source = title_bits[-1]
            if title and link:
                results.append(
                    {
                        "title": title,
                        "description": description,
                        "url": link,
                        "age": pub_date,
                        "profile_name": source or "Public Hotspot Feed",
                    }
                )
        return results
