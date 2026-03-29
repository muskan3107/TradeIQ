"""
market_news.py — Fetch latest market headlines from public RSS feeds.

No API key required. Falls back to static headlines if the network or parse fails.
"""

from __future__ import annotations

import logging
import re
import xml.etree.ElementTree as ET
from html import unescape
from typing import Any
from urllib.parse import urlparse

import requests

logger = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (compatible; InvestorCoPilot/1.0; +https://example.local)"
)
TIMEOUT_SEC = 10
MAX_PER_FEED = 8

RSS_FEEDS = [
    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "https://www.moneycontrol.com/rss/business.xml",
]

FALLBACK_NEWS: list[dict[str, Any]] = [
    {
        "title": "Nifty holds range as investors weigh global cues and flows",
        "source": "Markets Desk",
        "link": "https://economictimes.indiatimes.com/markets",
    },
    {
        "title": "Banking pack in focus after policy commentary",
        "source": "Markets Desk",
        "link": "https://economictimes.indiatimes.com/markets",
    },
    {
        "title": "IT services outlook tracked on deal momentum",
        "source": "Markets Desk",
        "link": "https://economictimes.indiatimes.com/markets",
    },
]


def _strip_html(text: str) -> str:
    text = unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _host(url: str) -> str:
    try:
        return urlparse(url).netloc or "news"
    except Exception:
        return "news"


def _parse_rss(xml_bytes: bytes, feed_url: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        logger.debug("RSS parse error for %s: %s", feed_url, e)
        return out

    channel = root.find("channel")
    items_parent = channel if channel is not None else root
    for item in items_parent.findall(".//item")[:MAX_PER_FEED]:
        title_el = item.find("title")
        link_el = item.find("link")
        if title_el is None or title_el.text is None:
            continue
        title = _strip_html(title_el.text)
        link = (link_el.text or "#").strip() if link_el is not None else "#"
        if not title:
            continue
        out.append(
            {
                "title": title[:220],
                "source": _host(feed_url),
                "link": link,
            }
        )
    return out


def fetch_market_news(limit: int = 10) -> list[dict[str, Any]]:
    """
    Returns a list of dicts: title, source, link.
    """
    merged: list[dict[str, Any]] = []
    seen: set[str] = set()
    headers = {"User-Agent": USER_AGENT}

    for url in RSS_FEEDS:
        try:
            r = requests.get(url, headers=headers, timeout=TIMEOUT_SEC)
            r.raise_for_status()
            items = _parse_rss(r.content, url)
            for it in items:
                key = it["title"].lower()
                if key in seen:
                    continue
                seen.add(key)
                merged.append(it)
                if len(merged) >= limit:
                    return merged
        except Exception as exc:  # noqa: BLE001
            logger.debug("RSS fetch failed %s: %s", url, exc)

    if not merged:
        return list(FALLBACK_NEWS)[:limit]
    return merged[:limit]
