import pdfplumber
import pandas as pd
import zipfile
import os


def extrair_tabela_pdf(caminho_pdf, num_colunas=13):
    """
    Extrai todas as tabelas de um arquivo PDF usando pdfplumber e garante que todas as linhas tenham o mesmo número de colunas.
    """
    print(f"Extraindo tabelas do arquivo: {caminho_pdf}")
    data = []

    with pdfplumber.open(caminho_pdf) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if any(cell is not None for cell in row):  # Ignorar linhas completamente vazias
                        data.append(row)

    if not data:
        raise ValueError("Nenhuma tabela encontrada no PDF.")

    # Ajustar o número de colunas para exatamente `num_colunas`
    data = [row[:num_colunas] + [None] * (num_colunas - len(row)) for row in data]

    # Remover cabeçalhos repetidos
    header = data[0]
    data = [row for row in data if row != header]

    return pd.DataFrame(data, columns=header)


def limpar_e_corrigir_dados(df):
    """
    Limpa e corrige os dados extraídos, incluindo substituição de abreviações e remoção de inconsistências.
    """
    print("Limpando e corrigindo os dados...")

    # Remover linhas completamente vazias
    df = df.dropna(how='all')

    # Substituir abreviações conforme solicitado
    df = df.rename(columns={
        'OD': 'Seg. Odontológica',
        'AMB': 'Seg. Ambulatorial'
    })

    # Remover quebras de linha e aspas desnecessárias
    df = df.replace(r'\n', ' ', regex=True)
    df = df.replace(r'"', '', regex=True)

    # Garantir que o DataFrame tenha exatamente 13 colunas
    num_colunas = 13
    if len(df.columns) > num_colunas:
        df = df.iloc[:, :num_colunas]  # Truncar colunas extras
    elif len(df.columns) < num_colunas:
        for i in range(len(df.columns), num_colunas):
            df[f"Coluna_{i+1}"] = None  # Adicionar colunas vazias

    return df


def salvar_csv_e_compactar(df, nome_csv, nome_zip):
    """
    Salva o DataFrame em um arquivo CSV e compacta em um arquivo ZIP.
    """
    print(f"Salvando dados em: {nome_csv}")
    df.to_csv(nome_csv, index=False, encoding='utf-8-sig')

    print(f"Compactando em: {nome_zip}")
    with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(nome_csv, os.path.basename(nome_csv))

    print("Processo concluído com sucesso!")


def main():
    """
    Função principal que coordena a extração, limpeza, salvamento e compactação dos dados.
    """
    # Configurações
    caminho_pdf = "anexo_i.pdf"  # Ajuste o caminho conforme necessário
    nome_csv_final = "rol_procedimentos.csv"
    nome_zip = "Teste_FelipeAugustoClaudinoRamos.zip"

    try:
        # Extração dos dados do PDF
        df = extrair_tabela_pdf(caminho_pdf)

        # Limpeza e correção dos dados
        df_corrigido = limpar_e_corrigir_dados(df)

        # Salvamento e compactação
        salvar_csv_e_compactar(df_corrigido, nome_csv_final, nome_zip)

    except Exception as e:
        print(f"Erro durante o processo: {str(e)}")


if __name__ == "__main__":
    main()