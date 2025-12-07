import requests
from bs4 import BeautifulSoup

from collectors.base_collector import BaseCollector


class HttpCollector(BaseCollector):
    """
    Simple HTML collector using requests + BeautifulSoup.
    Expects the subclass or caller to implement/override `parse`.
    """

    def fetch(self, url: str) -> str | None:
        """Fetch a single URL if allowed by robots.txt."""
        if not self._can_fetch(url):
            return None

        headers = {"User-Agent": self.user_agent}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        self._sleep_politely()
        return resp.text

    def parse(self, html: str) -> list[dict]:
        """
        Default parse implementation – override this in subclasses
        or wrap this class for specific sites.
        """
        soup = BeautifulSoup(html, "html.parser")
        # Example placeholder: return empty until customized
        self.logger("[WARN] HttpCollector.parse() called but not overridden.")
        return []

    def collect(self) -> list[dict]:
        """
        Basic implementation:
        - Reads `paths` from source_config (list of URL paths)
        - Fetches each path
        - Parses HTML to list[dict]
        """
        base_url = self.source_config["base_url"]
        paths = self.source_config.get("paths", ["/"])

        all_records: list[dict] = []
        for path in paths:
            url = base_url.rstrip("/") + path
            self.logger(f"[INFO] Fetching: {url}")
            html = self.fetch(url)
            if not html:
                continue
            records = self.parse(html)
            all_records.extend(records)

        return all_records
