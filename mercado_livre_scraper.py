import json
import os
import time
from typing import List, Dict

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Cache-Control": "max-age=0",
}


def _build_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--lang=pt-BR")
    options.add_argument("--start-maximized")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def search_products(query: str, limit: int = 4) -> List[Dict[str, str]]:
    safe_query = query.strip().replace(" ", "-")
    url = f"https://lista.mercadolivre.com.br/{safe_query}"

    print(f"Abrindo a URL com Selenium: {url}")
    driver = _build_driver()
    try:
        driver.get(url)
        print("Aguarde a validação manual do Cloudflare no navegador...")
        input("Pressione Enter quando concluir a validação manual e quiser continuar...")
        time.sleep(3)
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

    with open("mercado_livre_page.html", "w", encoding="utf-8") as file:
        file.write(page_source)

    print(url)

    soup = BeautifulSoup(page_source, "html.parser")
    products: List[Dict[str, str]] = []

    for card in soup.select("a.ui-search-item__group__element"):
        title = card.select_one("h2")
        price = card.select_one("span.price-tag-fraction")
        href = card.get("href")

        if title and href:
            products.append(
                {
                    "name": title.get_text(" ", strip=True),
                    "price": price.get_text(" ", strip=True) if price else "Preço não informado",
                    "link": href if href.startswith("http") else f"https://www.mercadolivre.com.br{href}",
                }
            )
            if len(products) >= limit:
                break

    if not products:
        raise RuntimeError("Nenhum produto foi encontrado na página de resultados.")

    return products


def main() -> None:
    query = "fone-de-ouvido"
    print(f"Buscando produtos para: {query}")
    try:
        products = search_products(query, limit=4)
        print(json.dumps(products, ensure_ascii=False, indent=2))
    except Exception as exc:
        print(f"Erro ao buscar produtos: {exc}")


if __name__ == "__main__":
    main()
