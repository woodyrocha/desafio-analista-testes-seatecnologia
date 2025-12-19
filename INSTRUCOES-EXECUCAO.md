# 🚀 GUIA DE INSTALAÇÃO E EXECUÇÃO - TESTES AUTOMATIZADOS

## 📋 Arquivos Criados

Os seguintes arquivos foram criados e devem ser colocados no projeto:

### **Raiz do Projeto:**
- `.env` → Configurações da aplicação
- `conftest.py` → Fixtures do pytest com Allure

### **Diretório `utils/`:**
- `helpers.py` → Funções auxiliares expandidas

### **Diretório `pages/`:**
- `cadastro_page.py` → Page Object do formulário (com XPaths reais)
- `lista_funcionarios_page.py` → Page Object da listagem (com XPaths reais)

### **Diretório `tests/e2e/`:**
- `test_cadastro_funcionario.py` → 7 testes E2E de cadastro

---

## 🔧 Instalação

### 1. Atualizar `requirements.txt`

O arquivo `requirements.txt` já foi atualizado com:
```
allure-pytest>=2.13.2
pytest-bdd>=7.0.0
```

Instale todas as dependências:

```bash
pip install -r requirements.txt
```

### 2. Instalar Allure (para relatórios)

**Mac:**
```bash
brew install allure
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

**Windows:**
```bash
scoop install allure
```

Ou baixe de: https://github.com/allure-framework/allure2/releases

### 3. Verificar instalação

```bash
allure --version
pytest --version
```

---

## ▶️ Execução dos Testes

### **Executar TODOS os testes:**

```bash
pytest -v --alluredir=evidence/allure-results
```

### **Executar apenas testes E2E:**

```bash
pytest tests/e2e/ -v --alluredir=evidence/allure-results
```

### **Executar teste específico:**

```bash
pytest tests/e2e/test_cadastro_funcionario.py::test_cadastro_funcionario_dados_validos -v --alluredir=evidence/allure-results
```

### **Executar por markers:**

```bash
# Apenas testes críticos (smoke)
pytest -m smoke -v --alluredir=evidence/allure-results

# Apenas testes E2E
pytest -m e2e -v --alluredir=evidence/allure-results
```

### **Executar sem headless (ver navegador):**

Edite o `.env`:
```
HEADLESS=False
```

---

## 📊 Visualizar Relatório Allure

### **Opção 1: Servidor Interativo (recomendado)**

```bash
allure serve evidence/allure-results
```

Isso abrirá automaticamente o relatório no navegador.

### **Opção 2: Gerar HTML Estático**

```bash
allure generate evidence/allure-results -o evidence/allure-report --clean
```

Depois abra `evidence/allure-report/index.html` no navegador.

---

## 🐛 Troubleshooting

### Problema: Módulos não encontrados

**Solução:**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

Ou certifique-se de que está executando de dentro do diretório raiz do projeto.

### Problema: ChromeDriver não encontrado

**Solução:**
O `webdriver-manager` baixa automaticamente. Se falhar:

```bash
pip install --upgrade webdriver-manager
```

### Problema: Elementos não encontrados

**Possíveis causas:**
1. Aplicação mudou estrutura HTML
2. Timeouts muito curtos (ajuste no `.env`: `TIMEOUT=20`)
3. Elemento ainda não carregou (aumentar `IMPLICIT_WAIT`)

---

## 📝 Próximos Passos

### **1. Implementar testes de validação:**
- `tests/validations/test_validacao_cpf.py`
- `tests/validations/test_validacao_data.py`

### **2. Implementar testes de navegação:**
- `tests/navigation/test_navegacao_links.py`

### **3. Implementar testes de segurança:**
- `tests/security/test_seguranca_basica.py`

### **4. Criar arquivos `.feature` (BDD):**
- `features/cadastro.feature`
- `features/validacoes.feature`

### **5. Documentar bugs encontrados:**
- Preencher `docs/bugs-reportados.md` com evidências

---

## ✅ Checklist de Validação

Antes de considerar pronto:

- [ ] Todos os testes executam sem erro
- [ ] Relatório Allure é gerado corretamente
- [ ] Screenshots aparecem no relatório em caso de falha
- [ ] Dados fake são gerados corretamente
- [ ] Page Objects funcionam com XPaths reais
- [ ] Documentação de bugs está completa
- [ ] README.md está atualizado

---

## 📧 Entrega Final

Inclua na entrega:

1. ✅ Repositório GitHub completo
2. ✅ Relatório Allure HTML (zipado)
3. ✅ Screenshots dos testes rodando
4. ✅ Documento `bugs-reportados.md` preenchido
5. ✅ Vídeo/GIF mostrando execução (opcional mas recomendado)

---

## 🎯 Comandos Rápidos

```bash
# Rodar testes + gerar relatório + abrir navegador
pytest -v --alluredir=evidence/allure-results && allure serve evidence/allure-results

# Rodar apenas smoke tests
pytest -m smoke -v --alluredir=evidence/allure-results

# Rodar com mais detalhes de debug
pytest -vv -s --alluredir=evidence/allure-results

# Limpar cache do pytest
pytest --cache-clear

# Ver markers disponíveis
pytest --markers
```

---

**Boa sorte no desafio! 🚀**