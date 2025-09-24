import os
from PIL import Image

# Caminhos
pasta_entrada = "C:/Users/User/Desktop/CATEGORIA-v1/imagens_pineapple"
pasta_saida = "C:/Users/User/Desktop/CATEGORIA-v1/imagens_redimensionadas"

# Fundo final
fundo_tamanho = (1080, 1080)

# Área útil
limite_topo = 272
limite_base = 808
limite_esquerda = 204
limite_direita = 877
largura_util = limite_direita - limite_esquerda
altura_util = limite_base - limite_topo

# Função para detectar margens brancas e cortar automaticamente
def crop_por_cor_de_fundo(imagem, tolerancia=245):
    imagem = imagem.convert("RGB")
    pixels = imagem.load()
    largura, altura = imagem.size

    topo, base = 0, altura
    esquerda, direita = 0, largura

    # Função para verificar se um pixel é "quase branco"
    def eh_fundo(rgb):
        return all(v >= tolerancia for v in rgb)

    # Topo
    for y in range(altura):
        if any(not eh_fundo(pixels[x, y]) for x in range(largura)):
            topo = y
            break

    # Base
    for y in range(altura - 1, -1, -1):
        if any(not eh_fundo(pixels[x, y]) for x in range(largura)):
            base = y
            break

    # Esquerda
    for x in range(largura):
        if any(not eh_fundo(pixels[x, y]) for y in range(altura)):
            esquerda = x
            break

    # Direita
    for x in range(largura - 1, -1, -1):
        if any(not eh_fundo(pixels[x, y]) for y in range(altura)):
            direita = x
            break

    return imagem.crop((esquerda, topo, direita + 1, base + 1))

# Processar imagens
encontrou_imagem = False

for root, _, arquivos in os.walk(pasta_entrada):
    for nome_arquivo in arquivos:
        if nome_arquivo.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            encontrou_imagem = True
            print(f"🔍 Processando: {nome_arquivo}")

            try:
                caminho_imagem = os.path.join(root, nome_arquivo)

                # Abrir imagem
                imagem = Image.open(caminho_imagem)

                # Recorte automático pelas margens brancas
                imagem_crop = crop_por_cor_de_fundo(imagem, tolerancia=245)

                # Redimensionar proporcionalmente dentro da área útil
                proporcao = min(largura_util / imagem_crop.width, altura_util / imagem_crop.height)
                nova_largura = int(imagem_crop.width * proporcao)
                nova_altura = int(imagem_crop.height * proporcao)
                imagem_redimensionada = imagem_crop.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)

                # Criar fundo branco 1080x1080
                fundo = Image.new("RGB", fundo_tamanho, (255, 255, 255))
                offset_x = limite_esquerda + (largura_util - nova_largura) // 2
                offset_y = limite_topo + (altura_util - nova_altura) // 2
                fundo.paste(imagem_redimensionada, (offset_x, offset_y))

                # Caminho de saída
                caminho_relativo = os.path.relpath(caminho_imagem, pasta_entrada)
                caminho_destino = os.path.join(pasta_saida, caminho_relativo)
                os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)

                # Salvar em JPG com fundo branco
                fundo.save(caminho_destino.replace(".png", ".jpg"), format="JPEG", quality=95)
                print(f"✅ Finalizado: {caminho_destino}")

            except Exception as e:
                print(f"❌ Erro com {nome_arquivo}: {e}")

if not encontrou_imagem:
    print("⚠️ Nenhuma imagem válida foi encontrada na pasta.")
else:
    print("🎉 Todas as imagens foram processadas com sucesso!")
