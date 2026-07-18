import json
import re
import time
from typing import List, Dict
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}


def _build_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--lang=pt-BR")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def _clean_url(url: str) -> str:
    parsed = urlparse(url)
    query_params = parse_qsl(parsed.query, keep_blank_values=True)
    blocked_params = {
        "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
        "ref", "tag", "sp", "source", "sr", "ascsubtag", "ls", "cmpid", "smid",
        "link_code", "campaign", "ad_id", "gclid", "fbclid", "pf_rd_r", "pf_rd_p",
        "sbo", "psc", "qid", "th"
    }
    filtered_params = [
        (key, value)
        for key, value in query_params
        if key.lower() not in blocked_params
    ]
    cleaned = parsed._replace(query=urlencode(filtered_params, doseq=True))
    return urlunparse(cleaned)


def _normalize_title(title: str) -> str:
    clean_title = re.sub(r"\s+", " ", title).strip()
    clean_title = re.sub(r"^(?:\d+%\s+off|\d+%\s+off\s+|[0-9.,]+%\s+off)\s*", "", clean_title, flags=re.IGNORECASE)
    clean_title = re.sub(r"\b(?:menor preço em \d+ dias|menor preço|com prime|com oferta especial|oferta|preço da oferta)\b", "", clean_title, flags=re.IGNORECASE)
    clean_title = re.sub(r"\b(?:preço|de|de:|r\$[\d\.,\s]+)+", "", clean_title, flags=re.IGNORECASE)
    clean_title = re.sub(r"\s*\|\s*.*", "", clean_title)
    clean_title = re.sub(r"\s+", " ", clean_title).strip(" -:|")
    clean_title = clean_title[:90].rstrip(" .")
    return clean_title


def _deduplicate_deals(deals: List[Dict[str, str]]) -> List[Dict[str, str]]:
    seen_links = set()
    unique_deals: List[Dict[str, str]] = []

    for deal in deals:
        clean_link = _clean_url(deal["link"])
        if clean_link.lower() in seen_links:
            continue
        seen_links.add(clean_link.lower())
        unique_deals.append({
            "title": deal["title"],
            "link": clean_link,
            "price": deal.get("price", "Preço a consultar"),
        })

    return unique_deals


def _extract_price(text: str) -> str:
    cleaned = text.replace("\xa0", " ")
    matches = re.findall(r"R\$\s*\d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d{2})?", cleaned)
    if not matches:
        return "Preço a consultar"
    return matches[0].replace(" ", "")


def get_deals(limit: int = 10) -> List[Dict[str, str]]:
    url = "https://www.amazon.com.br/deals?ref_=nav_cs_gb"

    print(f"Abrindo a página da Amazon: {url}")
    driver = _build_driver()
    try:
        driver.get(url)
        time.sleep(8)
        page_source = driver.page_source
        print("HTML capturado via Selenium.")
    except Exception as exc:
        print(f"Falha ao usar Selenium: {exc}")
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()
        page_source = response.text
        print("HTML capturado via requests como fallback.")
    finally:
        driver.quit()

    soup = BeautifulSoup(page_source, "html.parser")
    raw_deals: List[Dict[str, str]] = []

    for card in soup.select("a[href*='/dp/']"):
        img = card.find("img")
        title = (img.get("alt") if img and img.get("alt") else card.get_text(" ", strip=True)).strip()
        href = card.get("href")
        if not title or not href:
            continue

        normalized_title = _normalize_title(title)
        if not normalized_title or len(normalized_title) < 8:
            continue
        if any(keyword in normalized_title.lower() for keyword in ["ver detalhes", "ofertas", "amazon"]):
            continue

        price = _extract_price(card.get_text(" ", strip=True))
        if price == "Preço a consultar":
            continue

        raw_deals.append({
            "title": normalized_title,
            "link": _clean_url(href if href.startswith("http") else f"https://www.amazon.com.br{href}"),
            "price": price,
        })

    deals = _deduplicate_deals(raw_deals)
    return deals[:limit]


def build_products_from_deals(deals: List[Dict[str, str]]) -> List[Dict[str, str]]:
    products = []
    for deal in deals:
        products.append(
            {
                "name": deal["title"],
                "price": deal.get("price", "Preço a consultar"),
                "description": "Oferta capturada da Amazon",
                "link": deal["link"],
            }
        )
    return products


def main() -> None:
    try:
        deals = get_deals(limit=10)
        products = build_products_from_deals(deals)
        with open("products.json", "w", encoding="utf-8") as file:
            json.dump(products, file, ensure_ascii=False, indent=2)
        print(json.dumps(products, ensure_ascii=False, indent=2))
    except Exception as exc:
        print(f"Erro ao buscar ofertas: {exc}")


if __name__ == "__main__":
    main()
