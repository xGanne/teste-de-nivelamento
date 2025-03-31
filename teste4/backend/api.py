from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Caminho correto para o arquivo CSV (no mesmo diretório que api.py)
CSV_PATH = os.path.join(os.path.dirname(__file__), 'Relatorio_cadop.csv')

# Função para serializar dados de forma segura para JSON
def safe_json_serialize(obj):
    """Função para serializar dados do DataFrame de forma segura para JSON"""
    if isinstance(obj, dict):
        return {k: safe_json_serialize(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [safe_json_serialize(i) for i in obj]
    elif isinstance(obj, (pd.Series, pd.DataFrame)):
        return safe_json_serialize(obj.to_dict())
    elif pd.isna(obj):
        return None
    elif isinstance(obj, (np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.float64, np.float32)):
        return None if np.isnan(obj) else float(obj)
    else:
        return obj

# Formata campos especiais como telefone, DDD, etc
def format_special_fields(data):
    """Formata campos especiais como telefone, DDD, etc."""
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            # Formatação específica para campos numéricos
            if key == 'Telefone' and value is not None:
                # Remove o decimal do telefone
                try:
                    result[key] = str(int(float(value))) if '.' in str(value) else value
                except (ValueError, TypeError):
                    result[key] = value
            elif key == 'DDD' and value is not None:
                # Remove o decimal do DDD
                try:
                    result[key] = str(int(float(value))) if '.' in str(value) else value
                except (ValueError, TypeError):
                    result[key] = value
            elif key in ['CEP', 'Registro_ANS', 'CNPJ'] and value is not None:
                # Garante que estes campos sejam strings sem decimais
                try:
                    if isinstance(value, (int, float)) or (isinstance(value, str) and '.' in value):
                        result[key] = str(int(float(value)))
                    else:
                        result[key] = value
                except (ValueError, TypeError):
                    result[key] = value
            else:
                # Para outros campos, se for float com .0, converte para int
                if isinstance(value, (float)) and value == int(value):
                    result[key] = int(value)
                else:
                    result[key] = value
        return result
    elif isinstance(data, list):
        return [format_special_fields(item) for item in data]
    else:
        return data

# Carrega os dados do CSV
def load_data():
    try:
        # Tenta primeiro com UTF-8
        df = pd.read_csv(CSV_PATH, delimiter=';', encoding='utf-8')
        return df
    except UnicodeDecodeError:
        # Se falhar, tenta com Latin-1
        df = pd.read_csv(CSV_PATH, delimiter=';', encoding='latin1')
        return df
    except Exception as e:
        print(f"Erro ao carregar o CSV: {e}")
        # Verifica se o arquivo existe
        if not os.path.exists(CSV_PATH):
            print(f"Arquivo {CSV_PATH} não encontrado!")
        return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro

# Calcula a relevância de um registro com base no termo de busca
def calculate_relevance(row, search_term):
    relevance = 0
    search_term_lower = search_term.lower()
    
    # Colunas de maior relevância têm peso maior
    weighted_columns = {
        'Razao_Social': 3,
        'Nome_Fantasia': 3,
        'Registro_ANS': 4,
        'CNPJ': 4,
        'Cidade': 2,
        'UF': 1
    }
    
    # Verifica cada coluna do registro
    for column in row.index:
        weight = weighted_columns.get(column, 1)
        
        if pd.notnull(row[column]):
            # Converte o valor para string para garantir a comparação
            value = str(row[column]).lower()
            
            # Correspondência exata
            if search_term_lower == value:
                relevance += 10 * weight
            # Correspondência no início do valor
            elif value.startswith(search_term_lower):
                relevance += 7 * weight
            # Correspondência parcial
            elif search_term_lower in value:
                relevance += 5 * weight
            # Correspondência por palavras individuais
            else:
                for word in search_term_lower.split():
                    if word in value:
                        relevance += 2 * weight
    
    return relevance

@app.route('/api/search', methods=['GET'])
def search_operators():
    search_term = request.args.get('q', '')
    
    if not search_term:
        return jsonify({"error": "Termo de busca vazio"}), 400
    
    # Reduzir o requisito de caracteres para 2
    if len(search_term) < 2:
        return jsonify({"error": "Termo de busca muito curto. Mínimo 2 caracteres."}), 400
    
    try:
        df = load_data()
        
        # Verifica se o DataFrame está vazio
        if df.empty:
            print("DataFrame vazio, impossível realizar a busca")
            return jsonify({"error": "Dados não disponíveis. Verifique o arquivo CSV."}), 500
        
        print(f"Realizando busca por '{search_term}' em {len(df)} registros")
        
        # Calcula a relevância para cada registro
        results = []
        for index, row in df.iterrows():
            relevance = calculate_relevance(row, search_term)
            if relevance > 0:
                # Converta os valores NaN para None e valores numéricos para strings
                operator_data = {}
                for key, value in row.to_dict().items():
                    if pd.isna(value):
                        operator_data[key] = None
                    else:
                        operator_data[key] = value
                
                operator_data['relevance'] = relevance
                results.append(operator_data)
        
        # Ordena por relevância (decrescente)
        results.sort(key=lambda x: x['relevance'], reverse=True)
        
        print(f"Encontrados {len(results)} resultados para '{search_term}'")
        
        # Limita a 20 resultados mais relevantes e formata os campos especiais
        results_formatted = format_special_fields(safe_json_serialize(results[:20]))
        
        return jsonify({"results": results_formatted})
    
    except Exception as e:
        print(f"Erro na busca: {e}")
        return jsonify({"error": f"Erro na busca: {str(e)}"}), 500

# Rota de teste para verificar se a API está funcionando e se o CSV está carregando corretamente
@app.route('/api/test', methods=['GET'])
def test():
    try:
        df = load_data()
        return jsonify({
            "status": "API esta funcionando!",
            "csv_status": "CSV carregado com sucesso" if not df.empty else "CSV não foi carregado",
            "records_count": len(df) if not df.empty else 0
        })
    except Exception as e:
        return jsonify({
            "status": "API esta funcionando!",
            "csv_status": f"Erro ao carregar CSV: {str(e)}",
            "records_count": 0
        })

@app.after_request
def after_request(response):
    """Garante que o Content-Type seja application/json"""
    if request.path.startswith('/api/'):
        response.headers.add('Content-Type', 'application/json')
    return response

if __name__ == '__main__':
    print(f"Tentando carregar arquivo CSV de: {CSV_PATH}")
    try:
        test_df = load_data()
        if not test_df.empty:
            print(f"CSV carregado com sucesso! Encontradas {len(test_df)} linhas.")
        else:
            print("DataFrame vazio após carregar CSV!")
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")
    
    app.run(debug=True, port=5000)