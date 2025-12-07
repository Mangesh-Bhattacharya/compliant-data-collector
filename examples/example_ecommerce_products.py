import os
import yaml
import requests
from bs4 import BeautifulSoup

from compliance.robots_checker import RobotsChecker
from pipeline.export_csv_excel import export_to_files
from collectors.base_collector import BaseCollector


class DemoEcommerceCollector(BaseCollector):
    def collect(self):
        base = self.source_config["base_url"]
        path = "/products"
        url = base + path

        if not self._can_fetch(url):
            return []

        resp = requests.get(
            url,
            headers={"User-Agent": self.user_agent},
            timeout=10,
        )
        resp.raise_for_status()

        self._sleep_politely()

        soup = BeautifulSoup(resp.text, "html.parser")
        items = []
        for card in soup.select(".product"):
            name = card.select_one(".product-name")
            price = card.select_one(".product-price")
            items.append(
                {
                    "name": name.get_text(strip=True) if name else None,
                    "price": price.get_text(strip=True) if price else None,
                }
            )
        return items


if __name__ == "__main__":
    # Resolve config path from project root
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sources_path = os.path.join(ROOT_DIR, "config", "sources.yml")

    with open(sources_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    src = cfg["sources"]["demo_ecommerce"]
    checker = RobotsChecker(src["robots_txt"], user_agent=src["user_agent"])
    collector = DemoEcommerceCollector(src, checker)

    data = collector.collect()
    export_to_files(data, csv_path="products.csv", xlsx_path="products.xlsx")
