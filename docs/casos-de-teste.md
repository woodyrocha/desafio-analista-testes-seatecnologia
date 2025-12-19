# Casos de Teste - Desafio QA Analyst SEA Tecnologia

**Projeto:** Sistema de Cadastro de Funcionários  
**URL:** http://analista-teste.seatecnologia.com.br  
**Framework:** Pytest + Selenium + Allure Reports  
**Padrão:** Page Object Model (POM)

---

## 📊 Resumo da Cobertura de Testes

| Categoria | Implementados | Passando | Falhando | Pendentes | Total Planejado |
|-----------|---------------|----------|----------|-----------|-----------------|
| E2E - Cadastro | 6 | 3 | 3 | 0 | 6 |
| E2E - Edição | 0 | 0 | 0 | 1 | 3 |
| E2E - Exclusão | 0 | 0 | 0 | 1 | 2 |
| Validações | 0 | 0 | 0 | 2 | 5 |
| Navegação | 0 | 0 | 0 | 1 | 3 |
| Segurança | 0 | 0 | 0 | 1 | 4 |
| **TOTAL** | **6** | **3** | **3** | **6** | **23** |

---

## 🎯 TESTES E2E - CADASTRO DE FUNCIONÁRIO

### CT-001: Cadastro de funcionário com dados válidos
**Arquivo:** `tests/e2e/test_cadastro_funcionario.py::test_cadastro_funcionario_dados_validos`  
**Severidade:** Crítica  
**Marcadores:** `@pytest.mark.e2e`, `@pytest.mark.smoke`  
**Status:** ❌ Falhando (BUG-003 - Lista sem scroll)

**Objetivo:**  
Validar cadastro completo de funcionário com todos os dados válidos.

**Pré-condições:**
- Aplicação acessível
- Browser Chrome disponível

**Dados de Teste:**
- Nome: Gerado aleatoriamente (padrão: "Teste XXXXXX")
- Sexo: Aleatório (M/F)
- CPF: 11 dígitos gerados
- Data Nascimento: 01/01/1995 (30 anos)
- RG: 9 dígitos gerados
- Cargo: "Cargo 1" (fixo)
- Não usa EPI: Sim

**Passos:**
1. Acessar aplicação
2. Clicar em "Adicionar Funcionário"
3. Preencher campo Nome
4. Selecionar Sexo
5. Preencher CPF
6. Preencher Data de Nascimento
7. Preencher RG
8. Selecionar Cargo no dropdown
9. Marcar checkbox "O trabalhador não usa EPI"
10. Clicar em "Salvar"
11. Aguardar redirecionamento
12. Validar funcionário na lista

**Resultado Esperado:**
- Funcionário cadastrado com sucesso
- Nome aparece na lista de funcionários
- Dados salvos corretamente

**Resultado Atual:**
❌ Funcionário não encontrado na lista (fica oculto devido à falta de scroll - BUG-003)

**Evidências:**
- Screenshot: `evidence/screenshots/test_cadastro_funcionario_dados_validos_*_FALHA.png`
- Allure Report: Passo-a-passo com screenshots de cada interação

**Observações:**
- Formulário preenche corretamente
- Salvamento aparentemente funciona (contador aumenta)
- Falha apenas na validação visual (busca no DOM)

---

### CT-002: Cadastro de funcionário sem EPI
**Arquivo:** `tests/e2e/test_cadastro_funcionario.py::test_cadastro_funcionario_sem_epi`  
**Severidade:** Crítica  
**Marcadores:** `@pytest.mark.e2e`  
**Status:** ❌ Falhando (BUG-003 - Lista sem scroll)

**Objetivo:**  
Validar cadastro marcando explicitamente "Não usa EPI".

**Dados de Teste:**
- Nome: Gerado aleatoriamente
- Sexo: Aleatório
- CPF: Gerado
- Data Nascimento: Gerada
- RG: Gerado
- Cargo: "Cargo 2"
- Não usa EPI: **Sim** (marcado)

**Passos:**
1. Acessar aplicação e iniciar cadastro
2. Preencher dados básicos
3. Selecionar cargo
4. **Marcar "O trabalhador não usa EPI"**
5. Salvar
6. Validar funcionário na lista

**Resultado Esperado:**
- Cadastro aceito sem campos de EPI
- Funcionário aparece na lista

**Resultado Atual:**
❌ Mesma falha do CT-001 (BUG-003)

---

### CT-003: Cadastro com apenas campos obrigatórios
**Arquivo:** `tests/e2e/test_cadastro_funcionario.py::test_cadastro_funcionario_somente_obrigatorios`  
**Severidade:** Normal  
**Marcadores:** `@pytest.mark.e2e`  
**Status:** ❌ Falhando (BUG-003 - Lista sem scroll)

**Objetivo:**  
Validar que cadastro é aceito com apenas campos obrigatórios (sem RG).

**Dados de Teste:**
- Nome: Gerado
- Sexo: M (fixo para teste)
- CPF: Gerado
- Data Nascimento: Gerada
- RG: **NÃO PREENCHIDO**
- Cargo: "Cargo 3"
- Não usa EPI: Sim

**Passos:**
1. Preencher apenas Nome, Sexo, CPF, Data, Cargo
2. **Não preencher RG**
3. Marcar "Não usa EPI"
4. Salvar
5. Validar cadastro aceito

**Resultado Esperado:**
- Sistema aceita cadastro sem RG
- Funcionário cadastrado normalmente

**Resultado Atual:**
❌ Mesma falha do CT-001 (BUG-003)

**Observação:**
- Teste valida se RG é opcional (aparentemente é)

---

### CT-004: Botão Voltar cancela cadastro
**Arquivo:** `tests/e2e/test_cadastro_funcionario.py::test_botao_voltar_cancela_cadastro`  
**Severidade:** Normal  
**Marcadores:** `@pytest.mark.e2e`  
**Status:** ✅ Passando

**Objetivo:**  
Validar que botão "Voltar" cancela cadastro e retorna para lista.

**Passos:**
1. Clicar em "Adicionar Funcionário"
2. Preencher nome parcialmente
3. Clicar em botão "Voltar"
4. Validar retorno para listagem

**Resultado Esperado:**
- Retorna para tela de listagem
- Dados não são salvos

**Resultado Atual:**
✅ Teste passou - comportamento correto

---

### CT-005: Toggle de Status funcional
**Arquivo:** `tests/e2e/test_cadastro_funcionario.py::test_toggle_status_funcional`  
**Severidade:** Normal  
**Marcadores:** `@pytest.mark.e2e`  
**Status:** ✅ Passando

**Objetivo:**  
Validar que toggle "Ativo/Inativo" muda de estado visualmente.

**Passos:**
1. Acessar formulário de cadastro
2. Verificar estado inicial do toggle
3. Clicar no toggle
4. Validar mudança de estado
5. Clicar novamente
6. Validar retorno ao estado original

**Resultado Esperado:**
- Toggle alterna entre Ativo/Inativo

**Resultado Atual:**
✅ Teste passou - toggle funcional

---

### CT-006: Cadastro de múltiplos funcionários sequencialmente
**Arquivo:** `tests/e2e/test_cadastro_funcionario.py::test_cadastro_multiplos_funcionarios`  
**Severidade:** Normal  
**Marcadores:** `@pytest.mark.e2e`  
**Status:** ✅ Passando

**Objetivo:**  
Validar cadastro de 2 funcionários em sequência.

**Passos:**
1. Cadastrar primeiro funcionário
2. Retornar para lista
3. Cadastrar segundo funcionário
4. Validar que ambos aparecem

**Resultado Esperado:**
- Ambos funcionários cadastrados
- Sistema permite múltiplos cadastros

**Resultado Atual:**
✅ Teste passou - múltiplos cadastros funcionam

**Observação:**
- Este teste passou usando busca JavaScript no DOM

---

## 🔄 TESTES E2E - EDIÇÃO DE FUNCIONÁRIO

_Seção reservada para testes de edição_

### CT-007: Edição de funcionário - Fluxo básico
**Arquivo:** `tests/e2e/test_edicao_funcionario.py::test_edicao_funcionario_fluxo_basico`  
**Status:** ⏸️ Pendente (BUG-001 bloqueia implementação)

**Objetivo:**  
Validar edição de dados de funcionário existente.

**Passos (Planejados):**
1. Cadastrar funcionário
2. Clicar no menu "..." do card
3. Selecionar "Editar"
4. Alterar dados
5. Salvar
6. Validar alterações

**Bloqueio:**
❌ BUG-001 - Menu "..." não abre

**Prioridade:** Alta (implementar após correção do BUG-001)

---

### CT-008: Edição de funcionário - Alterar status
**Status:** 📝 Planejado

**Objetivo:**  
Validar alteração de status Ativo/Inativo via edição.

---

### CT-009: Edição de funcionário - Adicionar/Remover EPIs
**Status:** 📝 Planejado

**Objetivo:**  
Validar gerenciamento de EPIs em funcionário existente.

---

## 🗑️ TESTES E2E - EXCLUSÃO DE FUNCIONÁRIO

_Seção reservada para testes de exclusão_

### CT-010: Exclusão de funcionário - Fluxo básico
**Arquivo:** `tests/e2e/test_exclusao_funcionario.py::test_exclusao_funcionario_fluxo_basico`  
**Status:** ⏸️ Pendente (BUG-001 bloqueia implementação)

**Objetivo:**  
Validar exclusão de funcionário.

**Passos (Planejados):**
1. Cadastrar funcionário
2. Clicar no menu "..."
3. Selecionar "Excluir"
4. Confirmar exclusão
5. Validar remoção da lista

**Bloqueio:**
❌ BUG-001 - Menu "..." não abre

---

### CT-011: Exclusão com confirmação
**Status:** 📝 Planejado

**Objetivo:**  
Validar modal de confirmação antes de excluir.

---

## ✅ TESTES DE VALIDAÇÃO

_Seção reservada para testes de validação de campos_

### CT-012: Validação de CPF - Formato válido
**Arquivo:** `tests/validations/test_validacao_cpf.py::test_validacao_cpf_exemplo`  
**Status:** 📝 Planejado

**Objetivo:**  
Validar que sistema aceita apenas CPFs no formato correto.

**Casos de Teste:**
- [ ] CPF válido (11 dígitos)
- [ ] CPF inválido (menos de 11 dígitos)
- [ ] CPF com caracteres especiais
- [ ] CPF com letras
- [ ] CPF em branco

---

### CT-013: Validação de CPF - Duplicação
**Status:** 📝 Planejado

**Objetivo:**  
Validar que sistema não aceita CPF duplicado.

---

### CT-014: Validação de Data de Nascimento
**Arquivo:** `tests/validations/test_validacao_data.py::test_validacao_data_exemplo`  
**Status:** 📝 Planejado

**Casos de Teste:**
- [ ] Data futura (não deve aceitar)
- [ ] Data com mais de 150 anos (não deve aceitar)
- [ ] Data válida
- [ ] Formato inválido

---

### CT-015: Validação de campos obrigatórios
**Status:** 📝 Planejado

**Objetivo:**  
Validar mensagens de erro para campos obrigatórios não preenchidos.

---

### CT-016: Validação de número CA
**Status:** 📝 Planejado

**Objetivo:**  
Validar formato do número do Certificado de Aprovação de EPI.

---

## 🧭 TESTES DE NAVEGAÇÃO

_Seção reservada para testes de navegação e links_

### CT-017: Navegação - Links do menu lateral
**Arquivo:** `tests/navigation/test_navegacao_links.py::test_navegacao_links_menu`  
**Status:** ⏸️ Pendente (BUG-004 - Links sem ação)

**Objetivo:**  
Validar que ícones do menu lateral navegam para páginas corretas.

**Bloqueio:**
❌ BUG-004 - Ícones não têm ação configurada

---

### CT-018: Navegação - Breadcrumb
**Status:** 📝 Planejado

**Objetivo:**  
Validar navegação via breadcrumb (se existir).

---

### CT-019: Navegação - Botão "Próximo passo"
**Status:** ⏸️ Pendente (BUG-007 - Botão sem ação)

**Objetivo:**  
Validar fluxo do botão "Próximo passo".

**Bloqueio:**
❌ BUG-007 - Botão não funciona

---

## 🔐 TESTES DE SEGURANÇA

_Seção reservada para testes de segurança_

### CT-020: XSS - Injeção em campos de texto
**Arquivo:** `tests/security/test_seguranca_inputs.py::test_xss_basic_injection_input`  
**Status:** ⏸️ Parcialmente implementado

**Objetivo:**  
Validar que sistema sanitiza inputs contra XSS.

**Payloads de Teste:**
- `<script>alert('XSS')</script>`
- `<img src=x onerror=alert('XSS')>`
- `javascript:alert('XSS')`

**Status Atual:**
⏸️ Teste implementado mas não localiza campos (precisa ajuste de seletores)

---

### CT-021: SQL Injection - Campos de busca
**Status:** 📝 Planejado

**Objetivo:**  
Validar proteção contra SQL Injection.

---

### CT-022: Upload de arquivo malicioso
**Status:** 📝 Planejado

**Objetivo:**  
Validar sanitização de upload de arquivos.

---

### CT-023: Manipulação de sessão
**Status:** 📝 Planejado

**Objetivo:**  
Validar controle de sessão e autenticação (se aplicável).

---

## 📊 MATRIZ DE RASTREABILIDADE

| Requisito Figma | Caso de Teste | Status | Bugs Relacionados |
|-----------------|---------------|--------|-------------------|
| Cadastro de funcionário | CT-001 a CT-006 | ✅ Implementado | BUG-003 |
| Edição de funcionário | CT-007 a CT-009 | ⏸️ Bloqueado | BUG-001 |
| Exclusão de funcionário | CT-010, CT-011 | ⏸️ Bloqueado | BUG-001 |
| Validação de campos | CT-012 a CT-016 | 📝 Planejado | - |
| Navegação | CT-017 a CT-019 | ⏸️ Bloqueado | BUG-004, BUG-007 |
| Segurança | CT-020 a CT-023 | 📝 Em progresso | - |

---

## 🎯 ESTRATÉGIA DE TESTE

### Prioridades:
1. **P0 - Crítico:** Fluxo de cadastro (CT-001 a CT-006)
2. **P1 - Alto:** Edição e Exclusão (CT-007 a CT-011)
3. **P2 - Médio:** Validações (CT-012 a CT-016)
4. **P3 - Baixo:** Navegação e Segurança (CT-017 a CT-023)

### Critérios de Aceite:
- ✅ Testes P0 devem passar 100%
- ✅ Testes P1 devem passar 80%+
- ✅ Cobertura de código: não aplicável (app externa)

### Ambientes:
- **Desenvolvimento:** Não disponível
- **QA:** http://analista-teste.seatecnologia.com.br
- **Produção:** N/A (ambiente de desafio)

---

## 📝 TEMPLATE PARA NOVOS CASOS DE TESTE

```markdown
### CT-XXX: [Título do Caso de Teste]
**Arquivo:** `tests/[categoria]/test_[nome].py::[função]`  
**Severidade:** [Crítica|Alta|Normal|Baixa]  
**Marcadores:** `@pytest.mark.[categoria]`  
**Status:** [✅ Passando | ❌ Falhando | ⏸️ Bloqueado | 📝 Planejado]

**Objetivo:**  
[Descrição clara do que está sendo testado]

**Pré-condições:**
- [Condição 1]
- [Condição 2]

**Dados de Teste:**
- [Dado 1: valor]
- [Dado 2: valor]

**Passos:**
1. [Passo 1]
2. [Passo 2]
3. [Passo N]

**Resultado Esperado:**
[O que deveria acontecer]

**Resultado Atual:**
[O que realmente acontece]

**Evidências:**
- Screenshot: [caminho]
- Log: [caminho]

**Bloqueios/Dependências:**
[Se houver]

**Observações:**
[Notas adicionais]
```

---

**Documento vivo - atualizado conforme evolução dos testes**  
**Última atualização:** 19/12/2024 21:00