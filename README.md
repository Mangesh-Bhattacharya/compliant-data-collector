# Data Collector

Compliant data-collector is a Python toolkit for ethical, legally aware web and API data collection with CSV/Excel outputs, designed to respect robots.txt, Terms of Service, and privacy constraints while providing clean, analytics-ready datasets. [1][2]

## Overview

This repository demonstrates how to build a configurable, compliant data collection system that only accesses publicly permitted content from websites and APIs. It focuses on robots.txt enforcement, ToS-aware workflows, and a transparent cleaning and export pipeline for CSV and Excel outputs.[2][3]

## Key features

- Robots.txt-aware requests with automatic blocking of disallowed paths and customizable user agent. [2][4]
- Separate collectors for HTTP/HTML, Playwright-based dynamic pages, and official APIs, all using a shared compliance-aware base class. [5][3]
- Data cleaning and normalization pipeline that deduplicates records and exports to CSV and Excel using pandas. [6][7]

## Project structure

- `config/` – YAML configuration for sources, allowed paths, rate limits, and example schemas.  
- `collectors/` – Base collector plus HTTP, Playwright, and API collectors that implement source-specific logic.  
- `compliance/` – Robots.txt checker and ToS note templates to document manual legal reviews.  
- `pipeline/` – Cleaning, validation, and export utilities for CSV/Excel output.  
- `examples/` – End-to-end scripts showing how to configure a source and generate datasets.  
- `tests/` – Basic tests for compliance behaviour and export integrity using sample records.[5][8]

## Installation

1. Clone the repository:  
   `git clone https://github.com/<your-username>/compliant-data-collector.git`  
2. Enter the project directory:  
   `cd compliant-data-collector`  
3. Create and activate a virtual environment (optional but recommended).  
4. Install dependencies:  
   `pip install -r requirements.txt`[5][3]

## Configuration

- Edit `config/sources.yml` to define sources, including `base_url`, `robots_txt`, `allowed_paths`, `rate_limit_seconds`, and `user_agent`.  
- Extend schema files (for example, `schema_orders.yml`) to describe the expected output fields and types for your use case.  
- Add ToS review notes as Markdown files under `compliance/tos_notes/` to document where and how the source permits automated access.[2][9]

## Usage

- For a static demo site, run the example script:  
  `python examples/example_ecommerce_products.py`  
- The script will:  
  - Load configuration from `config/sources.yml`.  
  - Check robots.txt using `RobotsChecker` before requesting pages.  
  - Collect and parse records, then export `products.csv` and `products.xlsx` into the project root.[6][5]

## Ethical and legal considerations

- This project is designed to respect robots.txt rules and avoid crawling disallowed paths or ignoring crawl delays. [2][4]
- It is intended only for sites and APIs where automated access is legally permitted; users are responsible for complying with applicable laws, contracts, and Terms of Service.  
- Sensitive personal data, paywalled content, and login-protected resources are out of scope unless explicitly and lawfully authorized.[2][9]

## Extending the toolkit

- Add new collectors in `collectors/` for different site or API patterns, reusing the base collector for logging, rate limiting, and compliance checks.  
- Extend the cleaning logic in `pipeline/clean_transform.py` to handle domain-specific validation and normalization.  
- Integrate with schedulers or orchestration tools in your own environment to run collection jobs on a recurring basis.[3][8]

## Disclaimer

This repository is for educational and professional demonstration purposes. It must only be used on sources where automated data collection is explicitly allowed, and the maintainer does not accept liability for misuse or violation of third-party terms or laws.[2][9]

## Sources

[1] Python Web Scraping Tutorial: Step-By-Step (2025) - Oxylabs https://oxylabs.io/blog/python-web-scraping

[2] Robots.txt for Web Scraping Guide - Bright Data https://brightdata.com/blog/how-tos/robots-txt-for-web-scraping-guide

[3] Web Scraping with Python | Tutorial + Code - PacketStream https://packetstream.io/complete-guide-to-web-scraping-with-python-from-basics-to-advanced-techniques/

[4] urllib.robotparser — Parser for robots.txt https://docs.python.org/3/library/urllib.robotparser.html

[5] Python Web Scraping: Full Tutorial With Examples (2025) https://www.scrapingbee.com/blog/web-scraping-101-with-python/

[6] How to Save Scraped Data to CSV, Excel & Databases in ... https://decodo.com/blog/how-to-save-your-scraped-data

[7] Pandas Web Scraping https://pythonbasics.org/pandas-web-scraping/

[8] Web scraping with Python - Tutorial - IONOS CA https://www.ionos.ca/digitalguide/websites/web-development/web-scraping-with-python/

[9] How to Interpret `robots.txt` When Web Scraping https://www.scrapeless.com/en/blog/robots-txt
