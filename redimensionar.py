import os
from PIL import Image, ImageFilter

# Caminhos de entrada e saída
pasta_entrada = "C:/Users/User/Desktop/CATEGORIA-V1/imagens_pineapple"
pasta_saida = "C:/Users/User/Desktop/CATEGORIA-V1/imagens_redimensionadas"

# Tamanho final da imagem (largura x altura)
tamanho_final = (2400, 800)
altura_final = tamanho_final[1]

# Extensões válidas
extensoes = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')

for subdir, _, arquivos in os.walk(pasta_entrada):
    for nome_arquivo in arquivos:
        if nome_arquivo.lower().endswith(extensoes):
            caminho_origem = os.path.join(subdir, nome_arquivo)
            caminho_relativo = os.path.relpath(caminho_origem, pasta_entrada)
            caminho_destino = os.path.join(pasta_saida, caminho_relativo)
            pasta_destino = os.path.dirname(caminho_destino)
            os.makedirs(pasta_destino, exist_ok=True)

            try:
                imagem = Image.open(caminho_origem)

                if imagem.mode in ("RGBA", "P"):
                    imagem = imagem.convert("RGB")

                # Redimensionar mantendo a altura exata de 800px
                proporcao = altura_final / imagem.height
                nova_largura = int(imagem.width * proporcao)
                imagem_redimensionada = imagem.resize(
                    (nova_largura, altura_final),
                    resample=Image.Resampling.LANCZOS
                )

                # Criar fundo branco de 2400x800
                fundo = Image.new("RGB", tamanho_final, "white")

                # Centralizar a camiseta horizontalmente
                offset_x = (tamanho_final[0] - imagem_redimensionada.width) // 2
                fundo.paste(imagem_redimensionada, (offset_x, 0))

                # Melhorar nitidez
                # fundo = fundo.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

                # Salvar imagem final
                extensao = os.path.splitext(nome_arquivo)[1].lower()
                if extensao in ['.jpg', '.jpeg']:
                    fundo.save(caminho_destino, quality=95)
                else:
                    fundo.save(caminho_destino)

                print(f"✅ OK: {caminho_destino}")
            except Exception as e:
                print(f"❌ Erro com {caminho_origem}: {e}")

print("🎉 Todas as camisetas agora ocupam 100% da altura de 800px!")
