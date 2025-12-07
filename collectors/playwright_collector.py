from playwright.sync_api import sync_playwright

from collectors.base_collector import BaseCollector


class PlaywrightCollector(BaseCollector):
    """
    Collector for JS-heavy pages using Playwright (sync API).
    Use when content requires rendering (SPAs, dynamic tables, etc.).
    """

    def _collect_page(self, page, url: str) -> list[dict]:
        """
        Override this method in subclasses or wrappers to implement
        page-specific extraction logic using Playwright's `page` object.
        """
        self.logger("[WARN] PlaywrightCollector._collect_page() not overridden.")
        return []

    def collect(self) -> list[dict]:
        base_url = self.source_config["base_url"]
        paths = self.source_config.get("paths", ["/"])

        all_records: list[dict] = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=self.user_agent)

            for path in paths:
                url = base_url.rstrip("/") + path
                if not self._can_fetch(url):
                    continue

                self.logger(f"[INFO] Playwright fetching: {url}")
                page = context.new_page()
                page.goto(url, wait_until="networkidle")
                self._sleep_politely()

                page_records = self._collect_page(page, url)
                all_records.extend(page_records)

                page.close()

            browser.close()

        return all_records
