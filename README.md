# Desafio – Analista de Testes

**Aplicação:** [http://analista-teste.seatecnologia.com.br](http://analista-teste.seatecnologia.com.br)
**Protótipo (Figma):** [https://tinyurl.com/yl58hs4m](https://tinyurl.com/yl58hs4m)
**Prazo original:** 7 dias
**Prazo real de execução:** 4 dias (execução acelerada)

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
* **Selenium WebDriver**
* **PyTest**
* **WebDriver Manager**
* **Git / GitHub**

A escolha por Selenium + Python se deu pela flexibilidade da ferramenta, ampla adoção no mercado e similaridade conceitual com ferramentas como Puppeteer, além de alinhamento com stacks comuns de automação.

---

### 6.2 Estrutura de Diretórios do Projeto

```text
analista-teste-automation/
│
├── README.md
├── requirements.txt
├── pytest.ini
│
├── docs/
│   ├── plano-de-testes.md
│   ├── casos-de-teste.md
│   ├── bugs-reportados.md
│   ├── analise-melhorias.md
│   └── relatorio-final.md
│
├── tests/
│   ├── e2e/
│   │   ├── test_cadastro_funcionario.py
│   │   ├── test_edicao_funcionario.py
│   │   ├── test_exclusao_funcionario.py
│   │
│   ├── validations/
│   │   ├── test_validacao_cpf.py
│   │   ├── test_validacao_data.py
│   │
│   ├── navigation/
│   │   ├── test_navegacao_links.py
│
├── pages/
│   ├── base_page.py
│   ├── cadastro_page.py
│   ├── lista_funcionarios_page.py
│
├── utils/
│   ├── driver_factory.py
│   ├── data_factory.py
│   ├── helpers.py
│
├── evidence/
│   ├── screenshots/
│   └── videos/
│
└── .gitignore
```

**Justificativa da Arquitetura:**

* Utilização do padrão **Page Object Model (POM)** para facilitar manutenção e reutilização de código
* Separação clara entre testes, páginas e utilidades
* Organização de evidências para facilitar avaliação
* Documentação estruturada incluindo análise de melhorias e relatório final
* Estrutura simples, porém escalável

---

### 6.3 Inicialização do Projeto

```bash
# criar ambiente virtual
python -m venv venv

# ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate     # Windows

# instalar dependências
pip install selenium pytest webdriver-manager

# gerar arquivo de dependências
pip freeze > requirements.txt
```

Execução dos testes:

```bash
pytest -v
```

---

## 7. Escopo da Automação

Serão automatizados prioritariamente:

* Fluxo completo de cadastro de funcionário
* Validações de formulário (CPF e data)
* Persistência e recuperação de dados
* Edição e exclusão de registros
* Navegação entre links e validação de componente "Em breve"

Testes puramente visuais e comparativos com o Figma serão majoritariamente manuais, devido à instabilidade da aplicação e ao custo-benefício da automação visual neste contexto.

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

---

## 9. Análise de Melhorias

Será fornecida uma análise abrangente contendo:

* Avaliação geral da qualidade da aplicação
* Sugestões de melhorias de funcionalidade
* Recomendações de performance
* Considerações de segurança
* Propostas de melhorias de UX/UI

---

## 10. Planejamento Cronológico de Execução (4 dias)

### Dia 1 – Análise e Planejamento (quinta/noite)

* Análise completa do Figma
* Testes exploratórios iniciais
* Mapeamento de telas e fluxos
* Criação do repositório GitHub
* Estruturação do README e documentação inicial

### Dia 2 – Testes Manuais e Estrutura da Automação (sexta)

* Execução de testes manuais críticos
* Testes de navegação e componente "Em breve"
* Registro de bugs com evidências
* Criação da estrutura da suíte de automação
* Implementação da base do Page Object Model

### Dia 3 – Automação dos Fluxos Críticos (sábado)

* Automação do cadastro de funcionário
* Automação das validações de formulário
* Automação de persistência e recuperação
* Automação de navegação
* Ajustes para lidar com falhas conhecidas da aplicação

### Dia 4 – Refinamento e Entrega (domingo/segunda)

* Automação de edição e exclusão
* Testes de navegação
* Testes básicos de segurança
* Análise de melhorias (performance, segurança, UX)
* Refatoração e organização do código
* Revisão final da documentação
* Elaboração do relatório final
* Preparação da entrega

---

## 11. Estrutura do Relatório Final

O relatório final incluirá:

1. **Resumo Executivo**
   * Visão geral do processo de teste
   * Principais descobertas

2. **Casos de Teste Executados**
   * Resumo dos testes manuais e automatizados
   * Métricas de cobertura

3. **Bugs Reportados**
   * Lista priorizada de defeitos encontrados
   * Severidade e impacto

4. **Análise de Conformidade**
   * Comparação detalhada com o protótipo Figma
   * Desvios de design identificados

5. **Testes Automatizados**
   * Descrição da suíte desenvolvida
   * Resultados de execução

6. **Análise de Melhorias**
   * Sugestões de funcionalidade
   * Recomendações de performance
   * Considerações de segurança
   * Propostas de UX/UI

7. **Conclusões e Próximos Passos**

---

## 12. Considerações Finais

Diante do prazo reduzido e da instabilidade da aplicação, o foco do trabalho foi priorizar fluxos críticos, manter clareza na documentação e demonstrar capacidade de análise, organização e automação com critério técnico.

O objetivo não foi atingir cobertura total, mas entregar uma solução sólida, compreensível e alinhada às boas práticas de testes de software, incluindo análise crítica de melhorias e recomendações fundamentadas.