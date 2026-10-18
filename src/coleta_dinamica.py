from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv

BASE_DIR = Path(__file__).resolve().parent.parent

def realizar_scraping_dinamico():
    print("Iniciando scraping dinâmico com Selenium...")

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        url = "https://agenciabrasil.ebc.com.br/direitos-humanos"
        driver.get(url)
        driver.implicitly_wait(10)

        # Salva snapshot bruto em data/raw/
        raw_dir = BASE_DIR / "data" / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        (raw_dir / "pagina_dinamica.html").write_text(driver.page_source, encoding="utf-8")

        # Processa com BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        noticias = []

        for link in soup.find_all("a", href=True):
            texto = link.get_text(" ", strip=True)
            if any(kw in texto.lower() for kw in ["pcd", "deficiência", "inclusão", "cotas", "trabalho"]):
                noticias.append({"manchete": texto, "link": link["href"]})

        proc_dir = BASE_DIR / "data" / "processed"
        proc_dir.mkdir(parents=True, exist_ok=True)

        with open(proc_dir / "noticias_pcd.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["manchete", "link"])
            writer.writeheader()
            writer.writerows(noticias)

        print(f"Sucesso! {len(noticias)} notícias capturadas.")

    finally:
        driver.quit()

if __name__ == "__main__":
    realizar_scraping_dinamico()