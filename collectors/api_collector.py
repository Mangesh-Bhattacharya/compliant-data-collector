import requests

from collectors.base_collector import BaseCollector


class ApiCollector(BaseCollector):
    """
    Collector for official APIs.
    Respects rate limits and keeps a clear separation between:
    - building the request
    - calling the API
    - normalizing responses into list[dict]
    """

    def _build_headers(self) -> dict:
        headers = {"User-Agent": self.user_agent}
        extra_headers = self.source_config.get("headers", {})
        headers.update(extra_headers)
        return headers

    def _build_params(self) -> dict:
        """Override or extend to support pagination/query params."""
        return self.source_config.get("params", {})

    def _parse_response(self, resp_json) -> list[dict]:
        """
        Override this to map the API's JSON structure to list[dict].
        Default assumes a top-level list.
        """
        if isinstance(resp_json, list):
            return resp_json
        self.logger("[WARN] ApiCollector._parse_response() using default handler.")
        return []

    def collect(self) -> list[dict]:
        endpoint = self.source_config["endpoint"]
        # robots.txt might not apply to APIs, but we call it for consistency
        if not self._can_fetch(endpoint):
            return []

        headers = self._build_headers()
        params = self._build_params()

        self.logger(f"[INFO] Calling API: {endpoint}")
        resp = requests.get(endpoint, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        self._sleep_politely()

        data = resp.json()
        records = self._parse_response(data)
        return records
