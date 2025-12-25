# Desafio – Analista de Testes

**Aplicação:** [http://analista-teste.seatecnologia.com.br](http://analista-teste.seatecnologia.com.br)
**Protótipo (Figma):** [https://tinyurl.com/yl58hs4m](https://tinyurl.com/yl58hs4m)


---

## 1. Objetivo do Desafio

Avaliar a qualidade de uma aplicação web em desenvolvimento, verificando sua conformidade com o protótipo fornecido, validando funcionalidades, identificando defeitos e propondo melhorias, por meio de testes manuais e automatizados.

O desafio busca avaliar não apenas a identificação de bugs, mas também a capacidade de análise, organização, priorização, documentação e automação de testes.

---

## 2. Escopo dos Testes

### 2.1 Tipos de Testes

* Testes Funcionais
* Testes de Validação de Dados
* Testes de Interface (UI)
* Testes de Navegação
* Testes de Persistência e Recuperação de Dados
* Testes de Compatibilidade entre Navegadores
* Testes de Segurança (análise básica)
* Testes Automatizados (Selenium + Python)

---

## 3. Análise de Requisitos

### 3.1 Requisitos Funcionais

* Cadastro de funcionário
* Validação de CPF
* Validação de data
* Inclusão de EPI
* Inclusão de atividades
* Persistência de dados do funcionário
* Recuperação de dados cadastrados
* Edição de registros (via menu "...")
* Exclusão de registros (via menu "...")
* Navegação entre páginas e links do menu
* Redirecionamento de links para componente "Em breve"

### 3.2 Requisitos Não Funcionais

* Conformidade visual com o protótipo (fonte, cores, layout)
* Navegação correta entre os links
* Compatibilidade com navegadores modernos
* Clareza e usabilidade da interface
* Segurança básica da aplicação

---

## 4. Estratégia de Testes

### 4.1 Abordagem Geral

* Análise comparativa entre protótipo (Figma) e aplicação
* Execução de testes exploratórios iniciais
* Criação de cenários de teste baseados em risco
* Automação prioritária dos fluxos críticos
* Documentação contínua dos achados
* Análise de segurança e sugestões de melhorias

### 4.2 Critérios de Priorização

1. Funcionalidades centrais (CRUD de funcionários)
2. Validações de dados (CPF, data)
3. Persistência e recuperação de dados
4. Navegação e comportamento esperado
5. Aspectos visuais mais evidentes
6. Segurança básica

---

## 5. Casos de Teste (Visão Geral)

* Cadastro com dados válidos
* Cadastro com CPF inválido
* Cadastro com data inválida
* Inclusão de múltiplos EPIs
* Inclusão de múltiplas atividades
* Edição de cadastro existente
* Exclusão de cadastro
* Recuperação de cadastro salvo
* Navegação por links do menu
* Validação de redirecionamento para "Em breve"
* Comparação visual com o protótipo
* Testes básicos de segurança (inputs maliciosos, XSS, SQL injection)

---

## 6. Arquitetura da Suíte de Testes Automatizados

### 6.1 Tecnologias Utilizadas

* **Python 3.x**
* **Selenium WebDriver** - Automação web
* **PyTest** - Framework de testes
* **WebDriver Manager** - Gerenciamento de drivers
* **Allure Report** - Relatórios visuais e interativos de execução de testes
* **pytest-bdd** - Suporte a Gherkin para especificação de cenários em BDD
* **Git / GitHub** - Controle de versão

A escolha por Selenium + Python se deu pela flexibilidade da ferramenta, ampla adoção no mercado e similaridade conceitual com ferramentas como Puppeteer, além de alinhamento com stacks comuns de automação.

**Allure Reports** foi adicionado para proporcionar relatórios visuais ricos, com screenshots automáticos, histórico de execuções, gráficos e categorização de falhas, facilitando a comunicação dos resultados para stakeholders técnicos e não-técnicos.

**Gherkin/BDD (Behavior-Driven Development)** foi incorporado para permitir a escrita de cenários de teste em linguagem natural (Given-When-Then), tornando os casos de teste mais legíveis e compreensíveis para todos os envolvidos no projeto, incluindo analistas de negócio e gestores.

---

### 6.2 Estrutura de Diretórios do Projeto

Abaixo está a estrutura atual do repositório, refletindo as alterações reais feitas durante a implementação (pacotes Python, `conftest.py`, diretório de evidências):

```text
/ (repo root)
├── README.md
├── requirements.txt
├── pytest.ini
├── conftest.py
├── .gitignore
├── .venv/                # ambiente virtual local (recomendado: não comitar)

├── docs/
│   ├── plano-de-testes.md
│   ├── casos-de-teste.md
│   ├── bugs-reportados.md
│   ├── analise-melhorias.md
│   └── relatorio-final.md

├── features/             # Arquivos .feature em Gherkin (BDD)
│   ├── cadastro.feature
│   ├── edicao.feature
│   ├── exclusao.feature
│   └── validacoes.feature

├── tests/
│   ├── e2e/
│   │   ├── test_cadastro_funcionario.py
│   │   ├── test_cadastro_com_epi.py
│   │   ├── test_edicao_funcionario.py
│   │   └── test_exclusao_funcionario.py
│   ├── validations/
│   │   ├── test_validacao_cpf.py
│   │   └── test_validacao_data.py
│   ├── navigation/
│   │   └── test_navegacao_links.py
│   ├── persistence/
│   │   └── test_persistencia_dados.py
│   ├── security/
│   │   ├── test_seguranca_basica.py
│   │   └── test_seguranca_inputs.py
│   └── step_definitions/    # Steps BDD (pytest-bdd)
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_cadastro_steps.py
│       ├── test_edicao_steps.py
│       ├── test_exclusao_steps.py
│       └── test_validacoes_steps.py

├── pages/                # Page Objects (POM) — agora pacotes Python
│   ├── __init__.py
│   ├── base_page.py
│   ├── cadastro_page.py
│   └── lista_funcionarios_page.py

├── utils/                # helpers e factories — agora pacotes Python
│   ├── __init__.py
│   ├── driver_factory.py
│   ├── data_factory.py
│   └── helpers.py

├── evidence/
│   ├── screenshots/
│   ├── videos/
│   └── allure-results/   # Resultados brutos do Allure
│       └── allure-report/ # Relatório HTML gerado pelo Allure

├── manual_tests/
│   ├── MANUAL_REPORT.md  # Relatório de testes manuais visuais
│   └── manual_screenshots/
│       ├── Screenshot_01_APP_from_2025-12-24_18-28-48.png
│       ├── Screenshot_01_FIGMA_from_2025-12-24_18-28-40.png
│       └── ...

└── .pytest_cache/
```

Notas rápidas:
- `pages/` e `utils/` foram transformados em pacotes Python (contêm `__init__.py`) para permitir imports diretos nos testes.
- `conftest.py` adiciona a raiz do projeto ao PYTHONPATH durante execução do pytest para evitar problemas de importação locais.
- O diretório do ambiente virtual (`.venv` ou `venv`) deve ser ignorado pelo Git — ver `.gitignore`.
- `features/` contém arquivos `.feature` escritos em Gherkin para documentação BDD dos cenários de teste.
- `evidence/allure-results/` armazena dados brutos da execução que o Allure utiliza para gerar relatórios.

**Justificativa da Arquitetura:**

* Utilização do padrão **Page Object Model (POM)** para facilitar manutenção e reutilização de código
* Separação clara entre testes, páginas e utilidades
* Organização de evidências para facilitar avaliação
* Documentação estruturada incluindo análise de melhorias e relatório final
* **BDD com Gherkin** para melhor comunicação com stakeholders não-técnicos
* **Allure Reports** para visualização profissional e interativa dos resultados
* Estrutura simples, porém escalável

---

### 6.3 Inicialização do Projeto

```bash
# criar ambiente virtual
python -m venv venv

# ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate     # Windows

# instalar dependências Python
pip install -r requirements.txt
```

#### Instalação do Allure CLI

O Allure CLI é necessário para visualizar os relatórios. **Deve ser instalado na máquina** (não é pacote Python).

**Linux (Debian/Ubuntu):**
```bash
# Opção 1: Download manual (recomendado)
cd /tmp
wget https://github.com/allure-framework/allure2/releases/download/2.30.0/allure-2.30.0.tgz
tar -zxvf allure-2.30.0.tgz
sudo mv allure-2.30.0 /opt/allure
sudo ln -s /opt/allure/bin/allure /usr/local/bin/allure

# Instalar Java (necessário para Allure)
sudo apt update
sudo apt install default-jre -y

# Verificar instalação
allure --version
java -version
```

**macOS:**
```bash
# Via Homebrew (recomendado)
brew install allure

# Verificar instalação
allure --version
```

**Windows:**
```powershell
# Via Scoop (recomendado)
scoop install allure

# OU via Chocolatey
choco install allure

# Verificar instalação
allure --version
```

**Nota:** O Allure requer Java instalado. Se não tiver, instale conforme comandos acima.

---

Execução dos testes:

```bash
# Limpar dados antigos do Allure (recomendado antes de nova execução)
rm -rf evidence/allure-results/*

# Executar todos os testes com relatório Allure
pytest -v --alluredir=evidence/allure-results

# Executar apenas testes BDD
pytest tests/step_definitions/ -v --alluredir=evidence/allure-results

# Executar apenas testes Python (excluir BDD)
pytest tests/ -v --ignore=tests/step_definitions/ --alluredir=evidence/allure-results

# Executar testes específicos
pytest tests/e2e/test_cadastro_funcionario.py -v --alluredir=evidence/allure-results

# Executar testes por marker
pytest -m e2e -v --alluredir=evidence/allure-results
pytest -m validations -v --alluredir=evidence/allure-results
pytest -m security -v --alluredir=evidence/allure-results

# Executar em paralelo (mais rápido)
pytest -v -n auto --alluredir=evidence/allure-results

# Gerar e abrir relatório Allure (abre navegador automaticamente)
allure serve evidence/allure-results

# Gerar relatório Allure estático (para compartilhar)
allure generate evidence/allure-results -o evidence/allure-report --clean
```

---

### 6.4 BDD com Gherkin

Os cenários de teste críticos foram documentados em Gherkin para facilitar o entendimento por parte de todos os stakeholders, incluindo analistas de negócio e gestores.

**Scenarios BDD Implementados (7 total):**

1. **cadastro.feature (3 scenarios):**
   - Cadastrar funcionário com dados válidos
   - Cadastrar funcionário com EPI
   - Tentar cadastrar sem campos obrigatórios

2. **validacoes.feature (2 scenarios):**
   - CPF inválido
   - Data inválida

3. **edicao.feature (1 scenario):**
   - Editar funcionário existente (SKIPPED - BUG-001)

4. **exclusao.feature (1 scenario):**
   - Excluir funcionário existente (SKIPPED - BUG-001)

**Exemplo de arquivo `.feature`:**

```gherkin
# features/cadastro.feature

Feature: Cadastro de Funcionário
  Como um usuário do sistema
  Eu quero cadastrar novos funcionários
  Para que eu possa gerenciar a equipe

  @e2e @smoke
  Scenario: Cadastrar funcionário com dados válidos
    Given que estou na tela de listagem de funcionários
    When eu clico no botão "Adicionar Funcionário"
    And preencho o nome com "João Silva"
    And preencho o CPF com "123.456.789-00"
    And preencho a data de nascimento com "01/01/1990"
    And seleciono o cargo "Analista"
    And clico no botão "Salvar"
    Then o funcionário deve aparecer na lista
    And deve exibir o nome "João Silva"
    And deve exibir o CPF "123.456.789-00"

  @validations
  Scenario: Tentar cadastrar sem campos obrigatórios
    Given que estou no formulário de cadastro
    When clico no botão "Salvar" sem preencher campos
    Then deve exibir mensagens de erro nos campos obrigatórios
    And o cadastro não deve ser salvo
```

**Estrutura dos arquivos `.feature`:**

* `features/cadastro.feature` - Cenários de cadastro de funcionário
* `features/edicao.feature` - Cenários de edição de funcionário
* `features/exclusao.feature` - Cenários de exclusão de funcionário
* `features/validacoes.feature` - Cenários de validação de campos

**Benefícios do BDD:**

* Linguagem natural compreensível por não-técnicos
* Documentação viva que acompanha o código
* Facilita discussões sobre requisitos e comportamentos esperados
* Serve como especificação executável
* No relatório Allure, scenarios aparecem organizados por Features

---

### 6.5 Allure Reports - Evidências Visuais

O Allure Framework foi integrado para gerar relatórios visuais e interativos dos testes automatizados, proporcionando:

**Recursos do Allure:**

* **Visão Geral (Overview):** Dashboard com métricas gerais (total de testes, passados, falhos, quebrados)
* **Suites:** Organização por suítes de teste
* **Gráficos:** Distribuição de resultados, tendências históricas, tempo de execução
* **Behaviors:** Agrupamento por features (BDD)
* **Categorias:** Classificação automática de falhas
* **Timeline:** Linha do tempo da execução
* **Anexos:** Screenshots automáticos em falhas, logs, vídeos

**Configuração do Allure:**

O pytest está configurado para capturar automaticamente:
* Screenshots em caso de falha
* Logs de execução
* Dados de ambiente (browser, SO, versão Python)
* Tempo de execução de cada teste
* Stack traces de erros

**Exemplo de anotações Allure no código:**

```python
import allure

@allure.feature('Cadastro de Funcionário')
@allure.story('Cadastro com dados válidos')
@allure.severity(allure.severity_level.CRITICAL)
def test_cadastro_funcionario():
    with allure.step('Acessar tela de cadastro'):
        # código
    with allure.step('Preencher formulário'):
        # código
    with allure.step('Validar cadastro realizado'):
        # código
```

**Visualização do Relatório:**

Após executar os testes, o relatório pode ser visualizado de duas formas:

1. **Servidor local interativo:** `allure serve evidence/allure-results`
2. **Relatório estático HTML:** `allure generate evidence/allure-results -o evidence/allure-report`

O relatório Allure será incluído na entrega final do desafio como evidência visual da execução dos testes automatizados.

---

## 7. Escopo da Automação

Serão automatizados prioritariamente:

* Fluxo completo de cadastro de funcionário
* Validações de formulário (CPF e data)
* Persistência e recuperação de dados
* Edição e exclusão de registros
* Navegação entre links e validação de componente "Em breve"

Testes puramente visuais e comparativos com o Figma serão majoritariamente manuais, devido à instabilidade da aplicação e ao custo-benefício da automação visual neste contexto.

Todos os testes automatizados terão:
* Cenários documentados em Gherkin (quando aplicável)
* Evidências capturadas automaticamente via Allure
* Categorização por severidade e tipo
* Screenshots em caso de falha

---

## 8. Reporte de Bugs

Cada bug reportado conterá:

* Título
* Descrição detalhada
* Passos para reprodução
* Resultado esperado
* Resultado atual
* Evidências (prints ou vídeos)
* Severidade
* Sugestão de melhoria (quando aplicável)

Os bugs identificados durante os testes automatizados serão automaticamente evidenciados no relatório Allure com screenshots e logs completos.

---

## 9. Análise de Melhorias

Será fornecida uma análise abrangente contendo:

* Avaliação geral da qualidade da aplicação
* Sugestões de melhorias de funcionalidade
* Recomendações de performance
* Considerações de segurança
* Propostas de melhorias de UX/UI


---

## 10. Estrutura do Relatório Final

O relatório final incluirá:

1. **Resumo Executivo**
   * Visão geral do processo de teste
   * Principais descobertas

2. **Casos de Teste Executados**
   * Resumo dos testes manuais e automatizados
   * Métricas de cobertura
   * Cenários BDD documentados

3. **Bugs Reportados**
   * Lista priorizada de defeitos encontrados
   * Severidade e impacto
   * Evidências do Allure Report

4. **Análise de Conformidade**
   * Comparação detalhada com o protótipo Figma
   * Desvios de design identificados

5. **Testes Automatizados**
   * Descrição da suíte desenvolvida
   * Resultados de execução (Allure Report)
   * Documentação BDD dos cenários

6. **Análise de Melhorias**
   * Sugestões de funcionalidade
   * Recomendações de performance
   * Considerações de segurança
   * Propostas de UX/UI

7. **Conclusões e Próximos Passos**

8. **Anexos**
   * Link para relatório Allure interativo
   * Screenshots e evidências
   * Arquivos `.feature` (Gherkin)

---

## 12. Considerações Finais

O foco do trabalho foi priorizar fluxos críticos, manter clareza na documentação e demonstrar capacidade de análise, organização e automação com critério técnico.

O objetivo não foi atingir cobertura total, mas entregar uma solução sólida, compreensível e alinhada às boas práticas de testes de software, incluindo análise crítica de melhorias e recomendações fundamentadas.

A utilização de **Allure Reports** proporciona uma visualização profissional e interativa dos resultados, enquanto **Gherkin/BDD** torna os cenários de teste acessíveis para todos os stakeholders, demonstrando maturidade técnica e capacidade de comunicação efetiva.