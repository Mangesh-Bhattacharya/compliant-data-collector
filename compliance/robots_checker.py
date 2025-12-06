from urllib.robotparser import RobotFileParser
import requests

class RobotsChecker:
    def __init__(self, robots_url, user_agent="CompliantDataCollectorBot/1.0"):
        self.robots_url = robots_url
        self.user_agent = user_agent
        self.rp = RobotFileParser()
        self._load()

    def _load(self):
        try:
            resp = requests.get(self.robots_url, timeout=10)
            if resp.status_code == 200:
                self.rp.parse(resp.text.splitlines())
            else:
                # If robots.txt missing or not reachable, treat as no rules
                self.rp.parse([])
        except Exception:
            self.rp.parse([])

    def can_fetch(self, url):
        return self.rp.can_fetch(self.user_agent, url)
