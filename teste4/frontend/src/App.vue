<template>
  <div class="app-wrapper" :class="{ 'dark-mode': darkMode }">
    <div class="container">
      
      <div class="header-container">
        <h1>Busca de Operadoras de Planos de Saúde</h1>
        <button @click="toggleDarkMode" class="theme-toggle">
          {{ darkMode ? '☀️ Modo Claro' : '🌙 Modo Escuro' }}
        </button>
      </div>
      
      <div class="search-container">
        <input 
          v-model="searchTerm" 
          @keyup.enter="searchOperators"
          placeholder="Digite o termo de busca (mínimo 2 caracteres)" 
          class="search-input"
        />
        <button @click="searchOperators" class="search-button">Buscar</button>
      </div>
      
      <div v-if="loading" class="loading">
        Carregando resultados...
      </div>
      
      <div v-if="error" class="error">
        {{ error }}
      </div>
      
      <div v-if="results.length === 0 && !loading && searchPerformed" class="no-results">
        Nenhum resultado encontrado. Tente outro termo de busca.
      </div>
      
      <div class="debug-info" v-if="showDebug && debugInfo">
        <h3>Informações de Debug:</h3>
        <pre>{{ debugInfo }}</pre>
        <button @click="showDebug = false" class="close-debug-btn">Fechar</button>
      </div>
      
      <div v-if="results.length > 0" class="results-container">
        <div class="results-header">
          <h2>Resultados da Busca ({{ results.length }})</h2>
          <button v-if="!showDebug" @click="showDebug = true" class="debug-btn">Mostrar Debug</button>
        </div>
        
        <div v-for="(operator, index) in results" :key="index" class="operator-card">
          <h3>{{ formatValue(operator.Nome_Fantasia) || formatValue(operator.Razao_Social) }}</h3>
          <div class="operator-details">
            <p><strong>Registro ANS:</strong> {{ formatValue(operator.Registro_ANS) }}</p>
            <p><strong>CNPJ:</strong> {{ formatCNPJ(operator.CNPJ) }}</p>
            <p><strong>Razão Social:</strong> {{ formatValue(operator.Razao_Social) }}</p>
            <p><strong>Modalidade:</strong> {{ formatValue(operator.Modalidade) }}</p>
            <p><strong>Cidade:</strong> {{ formatValue(operator.Cidade) }}/{{ formatValue(operator.UF) }}</p>
            <p><strong>Email:</strong> {{ formatValue(operator.Endereco_eletronico) || 'Não informado' }}</p>
            <p><strong>Telefone:</strong> {{ formatTelefone(operator.DDD, operator.Telefone) }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchTerm: '',
      results: [],
      loading: false,
      error: null,
      searchPerformed: false,
      debugInfo: null,
      showDebug: false,
      darkMode: false
    };
  },
  methods: {
    // Alterna entre modo claro e escuro
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
      // Salva a preferência do usuário no localStorage
      localStorage.setItem('darkMode', this.darkMode);
    },
    
    // Formata CNPJ: XX.XXX.XXX/XXXX-XX
    formatCNPJ(cnpj) {
      if (!cnpj) return 'Não informado';
      
      // Remove caracteres não numéricos e garante que é uma string
      const cleanCNPJ = String(cnpj).replace(/\D/g, '');
      
      // Verifica se tem 14 dígitos
      if (cleanCNPJ.length !== 14) return cnpj;
      
      // Formata o CNPJ: XX.XXX.XXX/XXXX-XX
      return `${cleanCNPJ.substring(0, 2)}.${cleanCNPJ.substring(2, 5)}.${cleanCNPJ.substring(5, 8)}/${cleanCNPJ.substring(8, 12)}-${cleanCNPJ.substring(12)}`;
    },
    
    // Formata telefone com DDD: (XX) XXXX-XXXX
    formatTelefone(ddd, telefone) {
      if (!telefone) return 'Não informado';
      
      // Limpeza básica
      const cleanDDD = ddd ? String(ddd).replace(/\D/g, '') : '';
      const cleanTelefone = String(telefone).replace(/\D/g, '');
      
      // Se não tiver DDD, retorna apenas o telefone formatado
      if (!cleanDDD) {
        // Tenta formatar o telefone
        if (cleanTelefone.length === 8) {
          return `${cleanTelefone.substring(0, 4)}-${cleanTelefone.substring(4)}`;
        } else if (cleanTelefone.length === 9) {
          return `${cleanTelefone.substring(0, 5)}-${cleanTelefone.substring(5)}`;
        }
        return telefone;
      }
      
      // Com DDD, formata como (XX) XXXX-XXXX ou (XX) XXXXX-XXXX
      if (cleanTelefone.length === 8) {
        return `(${cleanDDD}) ${cleanTelefone.substring(0, 4)}-${cleanTelefone.substring(4)}`;
      } else if (cleanTelefone.length === 9) {
        return `(${cleanDDD}) ${cleanTelefone.substring(0, 5)}-${cleanTelefone.substring(5)}`;
      }
      
      // Se não se encaixar em nenhum padrão, retorna formatado mas sem separadores
      return `(${cleanDDD}) ${cleanTelefone}`;
    },
    
    // Formata valores genéricos para exibição
    formatValue(value) {
      if (value === null || value === undefined) return '';
      if (typeof value === 'number' && Number.isInteger(value)) return value.toString();
      if (typeof value === 'string' && value.trim() === '') return 'Não informado';
      return value;
    },
    // Busca operadoras na API
    async searchOperators() {
      if (this.searchTerm.length < 2) {
        this.error = 'Por favor, digite pelo menos 2 caracteres para buscar.';
        return;
      }
      
      this.loading = true;
      this.error = null;
      this.results = [];
      this.searchPerformed = true;
      this.debugInfo = null;
      
      try {
        console.log("Enviando requisição para a API...");
        const response = await axios.get('http://localhost:5000/api/search', {
          params: { q: this.searchTerm },
          responseType: 'json'
        });
        
        console.log("Resposta recebida:", response.data);
        
        // Informações de debug para diagnóstico
        this.debugInfo = {
          responseStatus: response.status,
          responseType: typeof response.data,
          hasResults: response.data && Array.isArray(response.data.results),
          resultsCount: response.data && response.data.results ? response.data.results.length : 0,
          firstResult: response.data && response.data.results && response.data.results.length > 0 
            ? { ...response.data.results[0] } 
            : null
        };
        
        if (response.data && Array.isArray(response.data.results)) {
          this.results = response.data.results;
        } else {
          console.error("Formato de resposta inesperado:", response.data);
          this.error = "Formato de resposta inesperado. Verifique o console para detalhes.";
        }
        
        this.loading = false;
      } catch (error) {
        console.error("Erro completo:", error);
        this.loading = false;
        this.error = error.response?.data?.error || 
                    `Erro ao buscar operadoras: ${error.message}. Verifique se a API está rodando em http://localhost:5000`;
      }
    },
    
    // Método para testar a conexão com a API
    async testApiConnection() {
      try {
        const response = await axios.get('http://localhost:5000/api/test');
        console.log("Teste de API:", response.data);
        
        // Verificar se o CSV foi carregado corretamente
        if (response.data.csv_status && !response.data.csv_status.includes("sucesso")) {
          this.error = `Problema com o arquivo CSV: ${response.data.csv_status}`;
        }
      } catch (error) {
        console.error("Erro ao conectar com a API:", error);
        this.error = "Não foi possível conectar ao servidor. Verifique se a API está rodando.";
      }
    }
  },
  mounted() {
    // Testa a conexão com a API quando o componente é montado
    this.testApiConnection();
    
    // Recupera a preferência de tema do usuário do localStorage
    const savedDarkMode = localStorage.getItem('darkMode');
    if (savedDarkMode !== null) {
      this.darkMode = savedDarkMode === 'true';
    } else {
      // Detecta se o usuário prefere tema escuro no navegador
      const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)').matches;
      this.darkMode = prefersDarkScheme;
    }
  }
};
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  transition: background-color 0.3s ease;
}

.app-wrapper {
  min-height: 100vh;
  width: 100%;
  background-color: #fff;
  transition: background-color 0.3s ease;
}

.app-wrapper.dark-mode {
  background-color: #1a1a1a;
  color: #f0f0f0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  color: inherit;
  transition: all 0.3s ease;
}

.dark-mode .operator-card {
  background-color: #2c2c2c;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.dark-mode .operator-card h3 {
  color: #63e2b7;
}

.dark-mode .search-input {
  background-color: #333;
  color: #f0f0f0;
  border-color: #555;
}

.dark-mode .search-button {
  background-color: #63e2b7;
}

.dark-mode .debug-info {
  background-color: #2c2c2c;
  border-color: #444;
}

.dark-mode .debug-btn,
.dark-mode .close-debug-btn {
  background-color: #555;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

h1 {
  color: inherit;
  text-align: center;
  margin-bottom: 0;
  flex: 0 1 auto;
  margin: 0 auto;
}

.theme-toggle {
  padding: 8px 12px;
  background-color: #f2f2f2;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
  min-width: 140px;
}

.dark-mode .theme-toggle {
  background-color: #333;
  border-color: #444;
  color: #f0f0f0;
}

.theme-toggle:hover {
  background-color: #e0e0e0;
}

.dark-mode .theme-toggle:hover {
  background-color: #444;
}

.search-container {
  display: flex;
  margin-bottom: 20px;
}

.search-input {
  flex-grow: 1;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
  transition: all 0.3s ease;
}

.search-button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
}

.search-button:hover {
  background-color: #3aa876;
}

.dark-mode .search-button:hover {
  background-color: #55d4a8;
}

.loading, .error, .no-results {
  text-align: center;
  padding: 20px;
  color: inherit;
}

.error {
  color: #e74c3c;
}

.dark-mode .error {
  color: #ff6b6b;
}

.debug-info {
  margin: 20px 0;
  padding: 15px;
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  position: relative;
  transition: all 0.3s ease;
}

.debug-info pre {
  white-space: pre-wrap;
  font-family: monospace;
  font-size: 14px;
}

.close-debug-btn, .debug-btn {
  padding: 5px 10px;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.close-debug-btn {
  position: absolute;
  top: 10px;
  right: 10px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.results-container {
  margin-top: 20px;
}

.operator-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.operator-card h3 {
  color: #42b983;
  margin-top: 0;
  margin-bottom: 10px;
  transition: color 0.3s ease;
}

.operator-details {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 10px;
}

.operator-details p {
  margin: 5px 0;
}
</style>