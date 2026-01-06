# 🎯 SCRIPT DE APRESENTAÇÃO - ENTREVISTA TÉCNICA

**Projeto:** Testes Automatizados - Sistema de Cadastro de Funcionários  
**Duração Total:** ~20 minutos + perguntas  (média 50 minutos)
**Candidato:** Woody

---

## 📊 ESTRUTURA REORGANIZADA

| Seção | Tempo | Acumulado |
|-------|-------|-----------|
| 1. Introdução + Apresentação Pessoal | 0:45 | 0:45 |
| 2. Visão Geral do Projeto | 1:00 | 1:45 |
| 3. Arquitetura Técnica | 2:00 | 3:45 |
| 4. Bugs e Resultados | 2:00 | 5:45 |
| 5. BDD e Documentação | 1:00 | 6:45 |
| 6. Conclusão + Início da Demonstração | 0:45 | 7:30 |
| 7. Perguntas (enquanto testes rodam) | ~5:00 | - |
| 8. Apresentação do Relatório Allure | 2:00 | - |

---

# ROTEIRO DETALHADO

---

## 1️⃣ INTRODUÇÃO + APRESENTAÇÃO PESSOAL (0:45)

### Objetivo
Criar conexão, contextualizar sua trajetória e posicionar o projeto.

### Fala

> "Bom dia/tarde a todos. Meu nome é **Woody**.
>
> Sou um profissional em **transição de carreira**. Venho da área de **Garantia da Qualidade automotiva**, onde atuei como Analista Administrativo responsável por processos de garantia de veículos em período de fábrica. Essa experiência me deu uma visão muito clara sobre o **impacto que a qualidade tem no produto final e na experiência do usuário**.
>
> Hoje estou migrando para **Desenvolvimento de Software**, com foco inicial em fullstack. Porém, a área de **Qualidade e Testes** me atrai especialmente porque, tanto como desenvolvedor quanto como usuário, eu conheço bem a dor de utilizar um software de baixa qualidade.
>
> **Trazer essa mentalidade de qualidade para o desenvolvimento é o que me motiva.**
>
> Vou apresentar o projeto de testes automatizados que desenvolvi para este desafio técnico, onde avaliei uma aplicação web de cadastro de funcionários, implementando uma suíte robusta de testes e documentando os problemas encontrados."

### Frase de Impacto
> *"Qualidade não é uma fase do projeto — é uma mentalidade que deve permear todo o ciclo de desenvolvimento."*

---

## 2️⃣ VISÃO GERAL DO PROJETO (1:00)

### Objetivo
Apresentar escopo, métricas e dar dimensão do trabalho realizado.

### Fala

> "A aplicação testada é um **Sistema de Cadastro de Funcionários** com funcionalidades de CRUD, gestão de EPIs e atividades de trabalho.
>
> **Em números, o projeto entregou:**
> - **89 testes** implementados — 82 automatizados em Python e 7 cenários BDD
> - **19 bugs** documentados, incluindo 5 críticos e 1 vulnerabilidade de segurança
> - **46 screenshots** de evidência
>
> **Resultados da execução:**
> - ✅ **67%** dos testes passando
> - ❌ **16%** falhando devido a bugs reais da aplicação
> - ⏸️ **17%** bloqueados aguardando correções
>
> Importante destacar: **testes falhando não são necessariamente ruins** — eles estão cumprindo seu papel de detectar defeitos."

### Frase de Impacto
> *"Um teste que falha e encontra um bug é mais valioso que cem testes que passam sem validar nada."*

---

## 3️⃣ ARQUITETURA TÉCNICA (2:00)

### Objetivo
Demonstrar domínio técnico e justificar decisões de design.

### Fala

> "Organizei o projeto seguindo o padrão **Page Object Model**, que é o padrão de mercado para automação de testes web."

**[MOSTRAR ESTRUTURA NO TERMINAL/IDE]**

```
projeto/
├── pages/              → Page Objects (elementos e ações)
│   ├── base_page.py
│   ├── cadastro_page.py
│   └── lista_funcionarios_page.py
├── tests/
│   ├── e2e/            → Testes de fluxo completo
│   ├── validations/    → Testes de regras de negócio
│   ├── security/       → Testes de segurança
│   └── step_definitions/ → Steps do BDD
├── utils/              → Helpers e Data Factory
├── features/           → Cenários Gherkin
└── docs/               → Documentação completa
```

> "Essa arquitetura traz **três benefícios principais**:
>
> 1. **Manutenibilidade** — Se um seletor muda na aplicação, altero apenas o Page Object, não todos os testes
> 2. **Legibilidade** — Os testes leem como linguagem natural: `cadastro_page.preencher_nome()` é autoexplicativo
> 3. **Reutilização** — O mesmo Page Object serve para múltiplos testes em diferentes contextos
>
> **Sobre a stack escolhida:**
> - **Selenium + Python** pela maturidade do ecossistema e ampla adoção no mercado
> - **pytest** por ser mais flexível que unittest, com suporte nativo a fixtures e parametrização
> - **Allure Reports** para gerar relatórios visuais que facilitam a comunicação com stakeholders não-técnicos
> - **Faker** para geração de dados dinâmicos, evitando testes viciados em dados fixos"

**[MOSTRAR `cadastro_page.py` — 15 segundos]**

> "Aqui um exemplo prático: a classe `CadastroPage` centraliza todos os seletores XPath e métodos de interação com o formulário. Se amanhã o desenvolvedor mudar o seletor do campo CPF, eu altero **uma linha** e todos os testes continuam funcionando."

### Frase de Impacto
> *"Page Object Model não é sobre organização de código — é sobre criar uma camada de abstração que protege seus testes das mudanças inevitáveis da aplicação."*

---

## 4️⃣ BUGS E RESULTADOS (2:00)

### Objetivo
Mostrar capacidade analítica, priorização e comunicação de problemas.

### Fala

> "Durante a execução dos testes, identifiquei **19 bugs**, que categorizei por severidade seguindo critérios de impacto no usuário e no negócio:"

| Severidade | Qtd | Exemplos |
|------------|-----|----------|
| 🔴 Crítico | 5 | CRUD incompleto — edição e exclusão não funcionam |
| 🟠 Alto | 6 | Lista sem scroll — funcionários ficam ocultos |
| 🟡 Médio | 6 | Divergências entre Figma e aplicação |
| 🟢 Baixo | 2 | Problemas visuais menores |
| 🔵 Segurança | 1 | Vulnerabilidade de Open Redirect |

> "O **bug mais crítico** é a ausência das funcionalidades de edição e exclusão. O menu de três pontos no card do funcionário simplesmente não responde, impossibilitando o ciclo completo do CRUD. Isso significa que **50% das operações básicas não funcionam**.
>
> Também identifiquei uma **vulnerabilidade de segurança**: os ícones do menu lateral redirecionam para URLs externas sem validação, caracterizando um **Open Redirect** que poderia ser explorado em ataques de phishing.
>
> **Cada bug foi documentado com:**
> - Descrição clara do problema
> - Passos detalhados para reprodução
> - Resultado esperado versus resultado obtido
> - Severidade e prioridade sugerida
> - Screenshots como evidência"

**[MOSTRAR `docs/bugs-reportados.md` — 10 segundos]**

### Frase de Impacto
> *"Encontrar bugs é fácil. Documentá-los de forma que o desenvolvedor consiga reproduzir e corrigir — isso é o trabalho real do QA."*

---

## 5️⃣ BDD E DOCUMENTAÇÃO (1:00)

### Objetivo
Demonstrar visão além do código técnico.

### Fala

> "Além dos testes automatizados tradicionais, implementei **7 cenários BDD** usando Gherkin e pytest-bdd."

**[MOSTRAR `features/cadastro.feature`]**

```gherkin
Feature: Cadastro de Funcionário

  Scenario: Cadastro com dados válidos
    Given que estou na página de cadastro
    When preencho todos os campos obrigatórios
    And clico em salvar
    Then o funcionário aparece na lista
```

> "O BDD agrega dois valores importantes:
>
> 1. **Documentação viva** — Os cenários são especificações executáveis. Se o teste passa, a feature funciona.
> 2. **Comunicação** — Product Owners e stakeholders conseguem ler e validar os cenários sem conhecimento técnico.
>
> **A documentação completa do projeto inclui:**
> - Plano de testes com estratégia e escopo
> - 63 casos de teste detalhados
> - Relatório de bugs com evidências
> - Análise comparativa Figma vs Aplicação
> - Sugestões de melhorias para o time de desenvolvimento"

### Frase de Impacto
> *"BDD não é sobre sintaxe Gherkin — é sobre criar uma linguagem comum entre negócio e tecnologia."*

---

## 6️⃣ CONCLUSÃO + INÍCIO DA DEMONSTRAÇÃO (0:45)

### Objetivo
Fechar com impacto e fazer transição elegante para a demo.

### Fala

> "**Em resumo**, entreguei uma suíte completa que:
> - ✅ Cobre os fluxos críticos da aplicação
> - ✅ Documenta 19 bugs com evidências reproduzíveis
> - ✅ Segue padrões de mercado como Page Object Model e BDD
> - ✅ Gera relatórios visuais com Allure para comunicação com stakeholders
>
> **Minha recomendação técnica** seria priorizar a correção dos 5 bugs críticos antes de qualquer consideração de deploy — especialmente a funcionalidade de CRUD completo e a vulnerabilidade de segurança.
>
> Agora vou **iniciar a execução completa da suíte de testes**. Enquanto os testes rodam, fico à disposição para responder perguntas. Ao final, apresento o relatório visual gerado pelo Allure."

**[EXECUTAR NO TERMINAL]**

```bash
pytest tests/ -v --alluredir=evidence/allure-results
```

### Frase de Impacto
> *"Automação de testes não substitui o pensamento crítico — ela libera tempo para que o QA foque no que realmente importa: encontrar os problemas que ninguém pensou em procurar."*

---

## 7️⃣ PERGUNTAS (Enquanto testes rodam)

### Objetivo
Demonstrar conhecimento técnico respondendo perguntas enquanto a suíte executa em background.

### Postura
- Manter o terminal visível em parte da tela
- Responder com calma e técnica
- Referenciar o projeto sempre que possível

### Fala de Transição (se houver silêncio)

> "Enquanto aguardamos a execução, posso detalhar qualquer aspecto do projeto — arquitetura, decisões técnicas, processo de identificação de bugs, ou minha metodologia de trabalho."

---

## 8️⃣ APRESENTAÇÃO DO RELATÓRIO ALLURE (2:00)

### Objetivo
Mostrar o resultado visual e consolidar a apresentação.

**[EXECUTAR NO TERMINAL]**

```bash
allure serve evidence/allure-results
```

### Fala

> "O Allure gerou automaticamente este relatório interativo. Vou destacar os pontos principais:"

**[NAVEGAR PELO RELATÓRIO]**

> "**Overview** — Visão geral com taxa de sucesso, duração e distribuição por severidade.
>
> **Suites** — Organização por categoria de teste: E2E, validações, segurança, BDD.
>
> **Graphs** — Gráficos de tendência que seriam úteis em um pipeline de CI/CD para acompanhar a saúde do projeto ao longo do tempo.
>
> **Detalhe de um teste falhando** — Aqui podemos ver os steps executados, onde falhou, screenshot do momento da falha, e logs para debug."

**[MOSTRAR UM TESTE COM FALHA E EVIDÊNCIAS]**

> "Este tipo de relatório facilita muito a comunicação com o time de desenvolvimento e com gestores que precisam de visibilidade sobre a qualidade do produto."

### Fala de Encerramento

> "Com isso, concluo minha apresentação. Agradeço a oportunidade e fico à disposição para qualquer pergunta adicional."

---

---

# 📋 ÍNDICE RESUMIDO (COLA PARA APRESENTAÇÃO)

## ESTRUTURA RÁPIDA

```
1. INTRODUÇÃO (0:45)
   └─ Apresentação pessoal + transição de carreira + contexto do projeto

2. VISÃO GERAL (1:00)
   └─ Métricas: 89 testes | 19 bugs | 67% passando

3. ARQUITETURA (2:00)
   └─ Page Object Model
   └─ Estrutura de diretórios
   └─ Stack: Selenium + pytest + Allure + Faker
   └─ [MOSTRAR: cadastro_page.py]

4. BUGS (2:00)
   └─ 5 críticos | 6 altos | 6 médios | 2 baixos | 1 segurança
   └─ Destaque: CRUD incompleto + Open Redirect
   └─ [MOSTRAR: bugs-reportados.md]

5. BDD (1:00)
   └─ 7 cenários Gherkin
   └─ Documentação: plano + casos + relatório + análise
   └─ [MOSTRAR: cadastro.feature]

6. CONCLUSÃO (0:45)
   └─ Resumo entregas
   └─ Recomendação: corrigir 5 bugs críticos
   └─ [EXECUTAR: pytest tests/ -v --alluredir=evidence/allure-results]

7. PERGUNTAS
   └─ Responder enquanto testes rodam

8. ALLURE (2:00)
   └─ [EXECUTAR: allure serve evidence/allure-results]
   └─ Overview → Suites → Graphs → Detalhe de falha
```

---

## FRASES DE IMPACTO (MEMORIZAR)

| Momento | Frase |
|---------|-------|
| Introdução | "Qualidade não é uma fase — é uma mentalidade." |
| Visão Geral | "Um teste que falha e encontra um bug é mais valioso que cem testes que passam sem validar nada." |
| Arquitetura | "POM protege seus testes das mudanças inevitáveis da aplicação." |
| Bugs | "Documentar bugs para que o dev consiga reproduzir — isso é o trabalho real do QA." |
| BDD | "BDD é sobre criar linguagem comum entre negócio e tecnologia." |
| Conclusão | "Automação libera tempo para focar no que importa: encontrar problemas que ninguém pensou em procurar." |

---

## ✅ CHECKLIST PRÉ-APRESENTAÇÃO

### Ambiente (fazer ANTES de entrar na sala)

```
□ Clonar repositório no computador da empresa
  git clone [URL_DO_REPO]
  cd [PASTA_DO_PROJETO]

□ Criar ambiente virtual e instalar dependências
  python -m venv .venv
  source .venv/bin/activate  (ou .venv\Scripts\activate no Windows)
  pip install -r requirements.txt

□ Verificar se Allure está instalado
  allure --version
  (Se não estiver: scoop install allure / brew install allure / choco install allure)

□ Executar testes 1x para validar ambiente
  pytest tests/validations/test_validacao_cpf.py -v

□ Limpar resultados anteriores
  rm -rf evidence/allure-results/*
```

### Arquivos para deixar abertos no IDE

```
□ pages/cadastro_page.py
□ tests/e2e/test_cadastro_funcionario.py
□ features/cadastro.feature
□ docs/bugs-reportados.md
□ README.md
```

### Navegador

```
□ GitHub do projeto aberto em uma aba
□ Aplicação testada aberta em outra aba
  http://analista-teste.seatecnologia.com.br
```

### Terminal

```
□ Terminal aberto na raiz do projeto
□ Ambiente virtual ativado
□ Comando pronto para copiar/colar:
  pytest tests/ -v --alluredir=evidence/allure-results
```

### Verificação Final

```
□ Testar compartilhamento de tela (se for remoto)
□ Fechar notificações / apps desnecessários
□ Silenciar celular
□ Copo d'água por perto
```

---

## 🚨 PLANO B (Se algo der errado)

| Problema | Solução |
|----------|---------|
| Testes não rodam | Mostrar código no IDE + relatório Allure pré-gerado |
| Allure não instalado | Mostrar screenshots da pasta `evidence/` |
| Internet instável | Ter prints do GitHub salvos localmente |
| Aplicação fora do ar | Explicar que testes dependem do ambiente + mostrar evidências |

---