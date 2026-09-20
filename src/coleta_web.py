# Importação de bibliotecas
import requests  
import re        
import csv       
from pathlib import Path  
from bs4 import BeautifulSoup  

# Define o diretório raiz do projeto navegando 2 níveis acima a partir deste arquivo
BASE_DIR = Path(__file__).resolve().parent.parent

# Endereço URL da página do portal que será raspada para obter as notícias
URL_NOTICIAS = "https://agenciabrasil.ebc.com.br/direitos-humanos"

# Cabeçalho da requisição para identificar quem está acessando o site (boa prática de ética em Web Scraping)
HEADERS = {"User-Agent": "INFNET-PainelODS-IncluaTech (material didatico; contato: carolina.passos@al.infnet.edu.br)"}


def raspar_noticias_pcd():
    """
    Função responsável por fazer o scraping das notícias, filtrar os conteúdos
    relevantes para a temática PCD/Inclusão e salvar os resultados em CSV e TXT.
    """
    print("Iniciando a coleta automatizada de notícias...")

    # Realiza a requisição GET para baixar o conteúdo HTML da página
    resp = requests.get(URL_NOTICIAS, headers=HEADERS, timeout=30)
    
    # Verifica o status da resposta HTTP e dispara uma exceção/erro se o código for 4xx (não encontrado) ou 5xx (erro no servidor)
    resp.raise_for_status()

    # Transforma o texto HTML bruto da resposta em um objeto "analisável" pelo BeautifulSoup
    soup = BeautifulSoup(resp.text, "html.parser")

    # Lista vazia que armazenará os dicionários com as notícias encontradas
    noticias = []

    # Busca todas as tags de link (<a>) da página que possuam o atributo 'href' (links válidos)
    for link in soup.find_all("a", href=True):
        # Extrai o texto visível dentro da tag do link, removendo espaços extras nas pontas
        texto = link.get_text(" ", strip=True)
        
        # Converte o texto para minúsculo e verifica se contém alguma das palavras-chave do projeto
        if any(kw in texto.lower() for kw in ["pcd", "deficiência", "inclusão", "cotas", "trabalho"]):
            # Adiciona um dicionário com a manchete e a URL do link à lista de notícias
            noticias.append({"manchete": texto, "link": link["href"]})

    # Caso nenhum elemento atenda aos critérios de busca, encerra a função sem sobrescrever os arquivos locais
    if not noticias:
        print("Aviso: Nenhuma notícia encontrada com as palavras-chave. Os arquivos anteriores foram mantidos.")
        return

    # Define o diretório de destino (data/processed/) e cria as pastas caso elas ainda não existam
    path_dir = BASE_DIR / "data" / "processed"
    path_dir.mkdir(parents=True, exist_ok=True)

    # --- GRAVAÇÃO EM ARQUIVO CSV ---
    path_csv = path_dir / "noticias_pcd.csv"
    
    # Abre o arquivo CSV para escrita ('w') com codificação UTF-8 (suporta acentos em português)
    with open(path_csv, "w", newline="", encoding="utf-8") as f_csv:
        # Cria o gravador baseado em dicionário, definindo os nomes do cabeçalho
        writer = csv.DictWriter(f_csv, fieldnames=["manchete", "link"])
        # Escreve a linha do cabeçalho ("manchete", "link")
        writer.writeheader()
        # Escreve todas as linhas de notícias capturadas
        writer.writerows(noticias)

    # --- GRAVAÇÃO EM ARQUIVO TXT ---
    path_txt = path_dir / "noticias_pcd.txt"
    
    # Abre o arquivo TXT para escrita ('w')
    with open(path_txt, "w", encoding="utf-8") as f_txt:
        # Percorre as notícias gravando cada uma em uma nova linha formatada
        for item in noticias:
            f_txt.write(f"{item['manchete']} - {item['link']}\n")

    print(f"Coleta concluída com sucesso! {len(noticias)} notícias salvas em CSV e TXT.")


# Ponto de entrada padrão do script Python (só executa a função se o arquivo for rodado diretamente)
if __name__ == "__main__":
    raspar_noticias_pcd()