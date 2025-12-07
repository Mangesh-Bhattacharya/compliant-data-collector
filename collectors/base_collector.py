from abc import ABC, abstractmethod
import time

class BaseCollector(ABC):
    """
    Base collector that handles:
    - Storing source configuration
    - Compliance checks (robots.txt via compliance checker)
    - Simple rate limiting
    - Basic logging hook
    """

    def __init__(self, source_config, compliance_checker, logger=print):
        self.source_config = source_config
        self.compliance_checker = compliance_checker
        self.logger = logger
        self.rate_limit_seconds = source_config.get("rate_limit_seconds", 1)
        self.user_agent = source_config.get("user_agent", "CompliantDataCollectorBot/1.0")

    def _sleep_politely(self):
        """Respect rate limits between requests."""
        time.sleep(self.rate_limit_seconds)

    def _can_fetch(self, url: str) -> bool:
        """Check robots.txt before any outbound request."""
        allowed = self.compliance_checker.can_fetch(url)
        if not allowed:
            self.logger(f"[SKIP] Disallowed by robots.txt: {url}")
        return allowed

    @abstractmethod
    def collect(self):
        """
        Implement in subclasses.
        Should return a list of dicts, each dict representing one record.
        """
        raise NotImplementedError
