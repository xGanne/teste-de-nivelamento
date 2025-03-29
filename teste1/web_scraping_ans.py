import os
import requests
from bs4 import BeautifulSoup
import zipfile
import re

def baixar_arquivo(url, nome_arquivo):
    """
    Função para baixar um arquivo a partir de uma URL
    """
    print(f"Baixando {nome_arquivo}...")
    resposta = requests.get(url, stream=True)
    
    # Verifica se a requisição foi bem-sucedida
    if resposta.status_code == 200:
        with open(nome_arquivo, 'wb') as arquivo:
            for chunk in resposta.iter_content(chunk_size=1024):
                if chunk:
                    arquivo.write(chunk)
        print(f"Download de {nome_arquivo} concluído com sucesso!")
        return True
    else:
        print(f"Falha ao baixar {nome_arquivo}. Código de status: {resposta.status_code}")
        return False

def main():
    # URL do site
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    
    # Criar pasta para armazenar os arquivos
    pasta_destino = "anexos"
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    
    # Acessar o site
    print(f"Acessando o site: {url}")
    resposta = requests.get(url)
    
    if resposta.status_code != 200:
        print(f"Falha ao acessar o site. Código de status: {resposta.status_code}")
        return
    
    # Parsear o HTML da página
    soup = BeautifulSoup(resposta.text, 'html.parser')
    
    # Encontrar links para os Anexos I e II (PDFs)
    links = soup.find_all('a', href=re.compile(r'.*\.(pdf|PDF)$'))
    
    # Filtrar apenas os anexos I e II
    anexos = []
    for link in links:
        texto = link.get_text().lower()
        url_anexo = link.get('href')
        
        # Verificar se é um link absoluto, caso contrário, torná-lo absoluto
        if not url_anexo.startswith('http'):
            if url_anexo.startswith('/'):
                url_anexo = f"https://www.gov.br{url_anexo}"
            else:
                url_anexo = f"https://www.gov.br/{url_anexo}"
        
        # Verificar se é um dos anexos que queremos
        if ('anexo i' in texto or 'anexo 1' in texto or 
            'anexo ii' in texto or 'anexo 2' in texto):
            nome_arquivo = os.path.join(pasta_destino, f"{texto.strip().replace(' ', '_')}.pdf")
            anexos.append((url_anexo, nome_arquivo))
            print(f"Encontrado: {texto.strip()} - {url_anexo}")
    
    if not anexos:
        print("Não foram encontrados os Anexos I e II no site.")
        return
    
    # Baixar os anexos
    arquivos_baixados = []
    for url_anexo, nome_arquivo in anexos:
        if baixar_arquivo(url_anexo, nome_arquivo):
            arquivos_baixados.append(nome_arquivo)
    
    # Compactar os arquivos baixados em um arquivo ZIP
    if arquivos_baixados:
        nome_zip = "anexos.zip"
        print(f"Compactando arquivos em {nome_zip}...")
        
        with zipfile.ZipFile(nome_zip, 'w') as zipf:
            for arquivo in arquivos_baixados:
                zipf.write(arquivo, os.path.basename(arquivo))
                print(f"Adicionado {arquivo} ao ZIP")
        
        print(f"Compactação concluída! Arquivo gerado: {nome_zip}")
    else:
        print("Nenhum arquivo foi baixado, não é possível criar o arquivo ZIP.")

if __name__ == "__main__":
    main()