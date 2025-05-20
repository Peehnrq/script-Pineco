import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin
from unidecode import unidecode
import re

# Função para limpar nomes de pasta
def limpar_nome(nome):
    nome = unidecode(nome)
    nome = re.sub(r'[\\/*?:"<>|]', "", nome)
    nome = nome.strip()
    return nome

# Função para baixar imagem
def baixar_imagem(url, pasta, nome_arquivo):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            caminho = os.path.join(pasta, nome_arquivo)
            with open(caminho, 'wb') as f:
                f.write(response.content)
            print(f"✅ Imagem salva: {caminho}")
        else:
            print(f"❌ Falha ao baixar imagem: {url}")
    except Exception as e:
        print(f"⚠️ Erro ao baixar imagem {url}: {e}")

# Configuração do navegador headless
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--log-level=3")

navegador = webdriver.Chrome(options=options)

url_categoria = "https://www.shop-pineapple.co/vestuario"
navegador.get(url_categoria)

# Scroll para carregar mais produtos
for _ in range(10):
    navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

soup = BeautifulSoup(navegador.page_source, "html.parser")

# Busca a lista de produtos
ul = soup.select_one("div#listagemProdutos ul[data-produtos-linha]")
itens = ul.find_all("li", class_="span3") if ul else []

print(f"{len(itens)} produtos encontrados.")

produtos = []
for item in itens:
    a = item.find("a", href=True, title=True)
    if a:
        titulo = limpar_nome(a["title"])
        link = urljoin(url_categoria, a["href"])
        produtos.append((titulo, link))

# Cria a pasta raiz das imagens
os.makedirs("imagens_pineapple", exist_ok=True)

# Acessa cada produto e baixa as imagens
for i, (titulo, link_produto) in enumerate(produtos, 1):
    print(f"\n[{i}/{len(produtos)}] {titulo}")
    navegador.get(link_produto)
    time.sleep(1)

    soup_produto = BeautifulSoup(navegador.page_source, "html.parser")
    pasta_produto = os.path.join("imagens_pineapple", titulo)
    os.makedirs(pasta_produto, exist_ok=True)

    imagens = []

    # Imagem principal
    img_principal = soup_produto.select_one("img#imagemProduto")
    if img_principal and img_principal.get("src"):
        imagens.append(img_principal["src"])

    # Imagens extras das miniaturas
    miniaturas = soup_produto.select("ul.miniaturas li a[data-imagem-grande]")
    for a in miniaturas:
        url_img = a.get("data-imagem-grande")
        if url_img and url_img not in imagens:
            imagens.append(url_img)

    # Baixa as imagens
    for idx, url_img in enumerate(imagens, 1):
        nome_img = f"img_{idx}.jpg"
        baixar_imagem(url_img, pasta_produto, nome_img)

navegador.quit()
print("\n✅ Todas as imagens foram baixadas com sucesso!")
