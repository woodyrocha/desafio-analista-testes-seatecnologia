# Casos de Teste - Desafio QA Analyst SEA Tecnologia

**Projeto:** Sistema de Cadastro de Funcionários  
**URL:** http://analista-teste.seatecnologia.com.br  
**Framework:** Pytest + Selenium + Allure Reports  
**Padrão:** Page Object Model (POM)

---

## 📊 Resumo da Cobertura de Testes

| Categoria | Implementados | Passando | Falhando | Bloqueados | Total Planejado |
|-----------|---------------|----------|----------|------------|-----------------|
| E2E - Cadastro | 6 | 3 | 3 | 0 | 6 |
| E2E - EPIs | 11 | 3 | 5 | 2 | 11 |
| E2E - Edição | 4 | 0 | 0 | 4 | 4 |
| E2E - Exclusão | 5 | 0 | 0 | 5 | 5 |
| Validações - CPF | 13 | 13 | 0 | 0 | 13 |
| Validações - Data | 17 | 17 | 0 | 0 | 17 |
| Navegação | 3 | 1 | 2 | 0 | 3 |
| Segurança | 2 | 0 | 0 | 1 | 4 |
| **TOTAL** | **61** | **37** | **10** | **12** | **63** |

**Taxa de Sucesso:** 61% (37/61 implementados passando)  
**Bloqueados por Bugs:** 20% (12/61 testes)  
**Cobertura:** 97% (61/63 planejados implementados)

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
3. Preencher todos os campos
4. Marcar "O trabalhador não usa EPI"
5. Clicar em "Salvar"
6. Aguardar redirecionamento
7. Validar funcionário na lista

**Resultado Esperado:**
- Funcionário cadastrado com sucesso
- Nome aparece na lista de funcionários

**Resultado Atual:**
❌ Funcionário não encontrado na lista (fica oculto devido à falta de scroll - BUG-003)

**Evidências:**
- Screenshot: `evidence/screenshots/test_cadastro_funcionario_dados_validos_*_FALHA.png`

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
- Cargo: "Cargo 2"
- Não usa EPI: **Sim** (marcado)

**Resultado Atual:**
❌ Mesma falha do CT-001 (BUG-003)

---

### CT-003: Validação de RG obrigatório ⭐ ATUALIZADO
**Arquivo:** `tests/e2e/test_cadastro_funcionario.py::test_validacao_rg_obrigatorio`  
**Severidade:** Critical  
**Marcadores:** `@pytest.mark.e2e`, `@pytest.mark.validations`  
**Status:** ✅ Passando

**Objetivo:**  
Validar que sistema exige preenchimento do campo RG.

**Passos:**
1. Preencher apenas Nome, Sexo, CPF, Data, Cargo
2. **Não preencher RG**
3. Marcar "Não usa EPI"
4. Tentar salvar

**Resultado Esperado:**
- Sistema deve rejeitar cadastro sem RG
- Deve exibir mensagem de erro

**Resultado Atual:**
✅ Sistema corretamente rejeita cadastro sem RG

**Observação:**
- Teste renomeado de `test_cadastro_funcionario_somente_obrigatorios`
- Agora valida comportamento correto (rejeição)
- Story: "Validação de RG obrigatório"
- Adicionado marker: `@pytest.mark.validations`

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

**Resultado Atual:**
✅ Teste passou - toggle funcional

---

### CT-006: Cadastro de múltiplos funcionários sequencialmente
**Arquivo:** `tests/e2e/test_cadastro_funcionario.py::test_cadastro_multiplos_funcionarios`  
**Severidade:** Normal  
**Marcadores:** `@pytest.mark.e2e`  
**Status:** ❌ Falhando (BUG-003 - Lista sem scroll)

**Objetivo:**  
Validar cadastro de 2 funcionários em sequência.

**Resultado Atual:**
❌ Segundo funcionário não é encontrado (BUG-003)

---

## 📦 TESTES E2E - EPIs

### CT-007: Cadastro com um EPI e uma Atividade
**Arquivo:** `tests/e2e/test_cadastro_com_epi.py::test_cadastro_com_um_epi`  
**Severidade:** Critical  
**Marcadores:** `@pytest.mark.e2e`, `@pytest.mark.epi`  
**Status:** ❌ Falhando (BUG-003)

**Objetivo:**  
Validar cadastro com 1 EPI e 1 atividade.

**Dados de Teste:**
- Atividade: "Ativid 01"
- EPI: "Capacete de segurança"
- Número CA: "12345"

**Resultado Atual:**
❌ Funcionário não encontrado na lista (BUG-003)

---

### CT-008: Validação de campos obrigatórios de EPI
**Arquivo:** `tests/e2e/test_cadastro_com_epi.py::test_validacao_campos_obrigatorios_epi`  
**Status:** ✅ Passando

**Objetivo:**  
Validar que campos Atividade, EPI e Número CA são obrigatórios.

**Resultado Atual:**
✅ Sistema valida corretamente campos obrigatórios

---

### CT-009: Toggle "Não usa EPI" oculta campos
**Arquivo:** `tests/e2e/test_cadastro_com_epi.py::test_toggle_nao_usa_epi_oculta_campos`  
**Status:** ✅ Passando

**Objetivo:**  
Validar que marcar "Não usa EPI" oculta campos de EPI.

**Resultado Atual:**
✅ Toggle funciona corretamente

---

### CT-010: Cadastro com múltiplos EPIs
**Arquivo:** `tests/e2e/test_cadastro_com_epi.py::test_cadastro_com_multiplos_epis`  
**Status:** ⏸️ SKIPPED (BUG-005 bloqueia)

**Objetivo:**  
Validar cadastro de múltiplos EPIs para um funcionário.

**Bloqueio:**
❌ BUG-005: Botão "Adicionar EPI" não funciona

---

### CT-011: Cadastro com múltiplas atividades
**Arquivo:** `tests/e2e/test_cadastro_com_epi.py::test_cadastro_com_multiplas_atividades`  
**Status:** ⏸️ SKIPPED (BUG-002 bloqueia)

**Objetivo:**  
Validar cadastro de múltiplas atividades para um funcionário.

**Bloqueio:**
❌ BUG-002: Botão "Adicionar outra Atividade" volta para tela inicial

---

### CT-012: Validação de número CA obrigatório
**Arquivo:** `tests/e2e/test_cadastro_com_epi.py::test_validacao_numero_ca_obrigatorio`  
**Status:** ✅ Passando

**Objetivo:**  
Validar que número CA é obrigatório quando EPI é selecionado.

**Resultado Atual:**
✅ Sistema valida corretamente

---

### CT-013 a CT-017: Cadastro com diferentes tipos de EPIs
**Arquivo:** `tests/e2e/test_cadastro_com_epi.py::test_cadastro_com_diferentes_epis`  
**Severidade:** Normal  
**Marcadores:** `@pytest.mark.e2e`, `@pytest.mark.epi`  
**Status:** ✅ 1 passando, ❌ 4 falhando

**Objetivo:**  
Validar que todos os 5 EPIs disponíveis podem ser selecionados.

**EPIs Testados:**
1. ✅ "Capacete de segurança" - PASSED
2. ❌ "Luvas descartáveis" - FAILED (BUG-003)
3. ❌ "Óculos de proteção" - FAILED (BUG-003)
4. ❌ "Calçado de segurança" - FAILED (Timeout + BUG-003)
5. ❌ "Protetor auditivo" - FAILED (BUG-003)

**Observação Especial - "Calçado de segurança":**
- TimeoutException ao selecionar dropdown
- Possível problema com caractere "ç" no XPATH

---

## 🔄 TESTES E2E - EDIÇÃO DE FUNCIONÁRIO ⭐ NOVO

### CT-018: Edição de funcionário - Fluxo básico
**Arquivo:** `tests/e2e/test_edicao_funcionario.py::test_edicao_funcionario_fluxo_basico`  
**Severidade:** Critical  
**Marcadores:** `@pytest.mark.e2e`, `@pytest.mark.blocked`, `@pytest.mark.bug_001`  
**Status:** ⏸️ SKIPPED (BUG-001 bloqueia 100%)

**Objetivo:**  
Validar edição de dados de funcionário existente.

**Passos (Planejados):**
1. Cadastrar funcionário
2. Localizar funcionário na lista
3. Clicar no menu "..." do card
4. Selecionar "Editar"
5. Modificar dados
6. Salvar
7. Validar alterações

**Bloqueio:**
❌ BUG-001 - Menu "..." não abre (crítico)

**Evidências Geradas:**
- Screenshot: `evidence/screenshots/funcionario_cadastrado_para_edicao.png`
- Screenshot: `evidence/screenshots/antes_clicar_menu.png`
- Screenshot: `evidence/screenshots/depois_clicar_menu.png`

**Documentação do Fluxo Esperado:**
- ✅ Cadastro funciona
- ✅ Localização funciona
- ❌ Menu não abre (BUG-001)
- ❌ Opção "Editar" inacessível
- ❌ Edição bloqueada

---

### CT-019: Edição de funcionário - Alterar apenas nome
**Arquivo:** `tests/e2e/test_edicao_funcionario.py::test_edicao_nome_funcionario`  
**Status:** ⏸️ SKIPPED (BUG-001 bloqueia)

**Objetivo:**  
Validar edição parcial (apenas nome).

**Bloqueio:**
❌ BUG-001 - Menu "..." não abre

---

### CT-020: Cancelar edição de funcionário
**Arquivo:** `tests/e2e/test_edicao_funcionario.py::test_cancelar_edicao_funcionario`  
**Status:** ⏸️ SKIPPED (BUG-001 bloqueia)

**Objetivo:**  
Validar que botão "Voltar" cancela edição.

**Bloqueio:**
❌ BUG-001 - Menu "..." não abre

---

### CT-021: Validações durante edição
**Arquivo:** `tests/e2e/test_edicao_funcionario.py::test_validacoes_durante_edicao`  
**Status:** ⏸️ SKIPPED (BUG-001 bloqueia)

**Objetivo:**  
Validar que validações funcionam durante edição (ex: CPF inválido).

**Bloqueio:**
❌ BUG-001 - Menu "..." não abre

---

## 🗑️ TESTES E2E - EXCLUSÃO DE FUNCIONÁRIO ⭐ NOVO

### CT-022: Exclusão de funcionário - Fluxo básico
**Arquivo:** `tests/e2e/test_exclusao_funcionario.py::test_exclusao_funcionario_fluxo_basico`  
**Severidade:** Critical  
**Marcadores:** `@pytest.mark.e2e`, `@pytest.mark.blocked`, `@pytest.mark.bug_001`  
**Status:** ⏸️ SKIPPED (BUG-001 bloqueia 100%)

**Objetivo:**  
Validar exclusão de funcionário.

**Passos (Planejados):**
1. Cadastrar funcionário
2. Localizar funcionário na lista
3. Clicar no menu "..."
4. Selecionar "Excluir"
5. Confirmar exclusão no modal
6. Validar remoção da lista

**Bloqueio:**
❌ BUG-001 - Menu "..." não abre (crítico)

**Evidências Geradas:**
- Screenshot: `evidence/screenshots/funcionario_cadastrado_para_exclusao.png`
- Screenshot: `evidence/screenshots/antes_clicar_menu_exclusao.png`
- Screenshot: `evidence/screenshots/depois_clicar_menu_exclusao.png`

**Documentação do Fluxo Esperado:**
- ✅ Cadastro funciona
- ✅ Localização funciona
- ❌ Menu não abre (BUG-001)
- ❌ Opção "Excluir" inacessível
- ❌ Exclusão bloqueada

---

### CT-023: Cancelar exclusão de funcionário
**Arquivo:** `tests/e2e/test_exclusao_funcionario.py::test_cancelar_exclusao_funcionario`  
**Status:** ⏸️ SKIPPED (BUG-001 bloqueia)

**Objetivo:**  
Validar botão "Cancelar" no modal de confirmação.

**Bloqueio:**
❌ BUG-001 - Menu "..." não abre

---

### CT-024: Exclusão de múltiplos funcionários
**Arquivo:** `tests/e2e/test_exclusao_funcionario.py::test_exclusao_multiplos_funcionarios`  
**Status:** ⏸️ SKIPPED (BUG-001 bloqueia)

**Objetivo:**  
Validar exclusão de 3 funcionários em sequência.

**Bloqueio:**
❌ BUG-001 - Menu "..." não abre

---

### CT-025: Funcionário excluído não aparece na lista
**Arquivo:** `tests/e2e/test_exclusao_funcionario.py::test_funcionario_excluido_nao_aparece_na_lista`  
**Status:** ⏸️ SKIPPED (BUG-001 bloqueia)

**Objetivo:**  
Validar que funcionário excluído é removido da lista.

**Bloqueio:**
❌ BUG-001 - Menu "..." não abre

---

### CT-026: Modal de confirmação de exclusão
**Arquivo:** `tests/e2e/test_exclusao_funcionario.py::test_mensagem_confirmacao_exclusao`  
**Status:** ⏸️ SKIPPED (BUG-001 bloqueia)

**Objetivo:**  
Validar conteúdo e botões do modal de confirmação.

**Bloqueio:**
❌ BUG-001 - Menu "..." não abre

---

## ✅ TESTES DE VALIDAÇÃO - CPF

### CT-027 a CT-039: Validações de CPF
**Arquivo:** `tests/validations/test_validacao_cpf.py`  
**Total:** 13 testes  
**Status:** ✅ TODOS PASSANDO (100%)

**Testes Implementados:**
1. ✅ `test_cpf_valido_aceito` - CPF válido é aceito
2. ✅ `test_cpf_invalido_rejeitado` (6 parametrizados):
   - 111.111.111-11 (dígitos iguais)
   - 000.000.000-00 (todos zeros)
   - 123.456.789-00 (dígito verificador incorreto)
   - 999.999.999-99 (todos 9s)
   - 123.456.789-10 (segundo dígito incorreto)
3. ✅ `test_cpf_formatacao_automatica` - Sistema formata CPF
4. ✅ `test_cpf_duplicado_nao_permitido` - CPF duplicado rejeitado
5. ✅ `test_cpf_caracteres_invalidos` (4 parametrizados):
   - abc.def.ghi-jk (letras)
   - 123-456-789.00 (formato errado)
   - 12.345.678 (incompleto)
   - 123 456 789 00 (espaços)
6. ✅ `test_algoritmo_validacao_cpf_correto` - Algoritmo funciona

**Resultado:**
✅ 13/13 testes passando - Validações de CPF 100% funcionais

---

## 📅 TESTES DE VALIDAÇÃO - DATA

### CT-040 a CT-056: Validações de Data de Nascimento
**Arquivo:** `tests/validations/test_validacao_data.py`  
**Total:** 17 testes  
**Status:** ✅ TODOS PASSANDO (100%)

**Testes Implementados:**
1. ✅ `test_data_nascimento_valida_aceita` - Data válida aceita
2. ✅ `test_data_nascimento_invalida_rejeitada` (10 parametrizados):
   - 01/01/2030 (futura)
   - 32/01/1990 (dia inválido)
   - 01/13/1990 (mês inválido)
   - 00/01/1990 (dia zero)
   - 01/00/1990 (mês zero)
   - 31/02/1990 (fevereiro com 31 dias)
   - 29/02/2023 (ano não bissexto)
   - 01/01/1850 (mais de 120 anos)
   - 01/01/1900 (mais de 120 anos)
3. ✅ `test_data_nascimento_futura_rejeitada` - Data futura rejeitada
4. ✅ `test_data_nascimento_menor_idade` - Menor de idade aceito
5. ✅ `test_ano_bissexto_validacao` - Ano bissexto funciona
6. ✅ `test_data_nascimento_hoje_rejeitada` - Hoje rejeitado
7. ✅ `test_data_formato_invalido` (7 parametrizados):
   - 2023-01-01 (formato ISO)
   - 01-01-2023 (traços)
   - 1/1/2023 (sem zeros)
   - 01/1/2023 (mês sem zero)
   - 1/01/2023 (dia sem zero)
   - abc/def/ghij (letras)
   - 01/01/23 (ano com 2 dígitos)
8. ✅ `test_calculo_idade_correto` - Cálculo de idade correto (corrigido em 2025)
9. ✅ `test_datas_limite_fronteira` - Datas limites funcionam

**Resultado:**
✅ 17/17 testes passando - Validações de Data 100% funcionais

---

## 🧭 TESTES DE NAVEGAÇÃO ⭐ NOVO

### CT-057: Navegação - Ícones do menu lateral
**Arquivo:** `tests/navigation/test_navegacao_links.py::test_navegacao_menu_lateral_icones`  
**Severidade:** Critical  
**Marcadores:** `@pytest.mark.e2e`, `@pytest.mark.navigation`  
**Status:** ❌ FAILED (BUG-006)

**Objetivo:**  
Validar que 6 ícones do menu lateral levam para componente "Em breve" (requisito do email RH).

**Requisito do Email RH:**
> "Teste os links para assegurar que eles conduzam às etapas e itens de menu corretos. **Todos os links devem levar ao componente 'Em breve'**"

**Ícones Testados:**
1. ❌ Ícone 1 (Topo) - Sem ação
2. ❌ Ícone 2 - Sem ação
3. ❌ Ícone 3 - Sem ação
4. ❌ Ícone 4 - Sem ação
5. ❌ Ícone 5 - Sem ação
6. ❌ Ícone 6 (Base) - Sem ação

**Resultado Atual:**
❌ 0/6 ícones funcionando - BUG-006 detectado

**Evidências:**
- 12 screenshots (antes/depois de cada ícone)

---

### CT-058: Navegação - Botão "Próximo passo"
**Arquivo:** `tests/navigation/test_navegacao_links.py::test_navegacao_botao_proximo_passo`  
**Severidade:** Normal  
**Marcadores:** `@pytest.mark.e2e`, `@pytest.mark.navigation`  
**Status:** ❌ FAILED (BUG-007)

**Objetivo:**  
Validar botão "Próximo passo" no footer.

**Resultado Atual:**
❌ Botão sem ação configurada (BUG-007)

**Evidências:**
- `evidence/screenshots/antes_proximo_passo.png`
- `evidence/screenshots/depois_proximo_passo.png`

---

### CT-059: Navegação - Botão "Voltar"
**Arquivo:** `tests/navigation/test_navegacao_links.py::test_navegacao_botao_voltar`  
**Severidade:** Critical  
**Marcadores:** `@pytest.mark.e2e`, `@pytest.mark.navigation`  
**Status:** ✅ PASSED

**Objetivo:**  
Validar que botão "Voltar" retorna para lista.

**Resultado Atual:**
✅ Botão funciona corretamente

---

## 🔒 TESTES DE SEGURANÇA

### CT-060: XSS - Injeção em campos de texto
**Arquivo:** `tests/security/test_seguranca_inputs.py::test_xss_basic_injection_input`  
**Status:** ⏸️ SKIPPED (Não localiza campos)

**Objetivo:**  
Validar que sistema sanitiza inputs contra XSS.

**Payloads de Teste:**
- `<script>alert('XSS')</script>`
- `<img src=x onerror=alert('XSS')>`
- `javascript:alert('XSS')`

**Status Atual:**
⏸️ Teste implementado mas precisa ajuste de seletores

---

## 📊 MATRIZ DE RASTREABILIDADE

| Requisito Figma | Casos de Teste | Implementados | Passando | Status |
|-----------------|----------------|---------------|----------|--------|
| Cadastro de funcionário | CT-001 a CT-006 | 6/6 | 3/6 | ❌ BUG-003 |
| EPIs | CT-007 a CT-017 | 11/11 | 3/11 | ❌ BUG-003 |
| Edição de funcionário | CT-018 a CT-021 | 4/4 | 0/4 | ⏸️ BUG-001 |
| Exclusão de funcionário | CT-022 a CT-026 | 5/5 | 0/5 | ⏸️ BUG-001 |
| Validação de CPF | CT-027 a CT-039 | 13/13 | 13/13 | ✅ 100% |
| Validação de Data | CT-040 a CT-056 | 17/17 | 17/17 | ✅ 100% |
| Navegação | CT-057 a CT-059 | 3/3 | 1/3 | ❌ BUG-006/007 |
| Segurança | CT-060 | 1/4 | 0/1 | ⏸️ Ajustar |

---

## 🎯 ESTRATÉGIA DE TESTE

### Prioridades:
1. **P0 - Crítico:** Fluxo de cadastro (CT-001 a CT-017) - ✅ Implementado
2. **P1 - Alto:** Edição e Exclusão (CT-018 a CT-026) - ✅ Implementado (bloqueados)
3. **P2 - Médio:** Validações (CT-027 a CT-056) - ✅ Implementado (100%)
4. **P3 - Baixo:** Navegação (CT-057 a CT-059) - ✅ Implementado

### Critérios de Aceite:
- ✅ Testes P0 devem passar 80%+ (atual: 55% devido a BUG-003)
- ✅ Testes P2 devem passar 100% (atual: 100% ✅)
- ⏸️ Testes P1 bloqueados por BUG-001 (0% executável)

### Ambientes:
- **QA:** http://analista-teste.seatecnologia.com.br

---

## 📈 ESTATÍSTICAS FINAIS

**Total de Testes:** 61 implementados / 63 planejados (97%)

**Por Status:**
- ✅ Passando: 37 (61%)
- ❌ Falhando: 10 (16%)
- ⏸️ Bloqueados: 12 (20%)
- 📋 Pendentes: 2 (3%)

**Por Categoria:**
- E2E: 33 testes (45% passando, 24% falhando, 30% bloqueados)
- Validações: 30 testes (100% passando) ⭐
- Navegação: 3 testes (33% passando, 67% falhando)
- Segurança: 1 teste (100% bloqueados)

**Bugs Detectados:**
- 3 bugs críticos documentados completamente
- 26 screenshots de evidência
- 9 testes bloqueados por BUG-001
- 8 testes falhando por BUG-003
- 1 teste falhando por BUG-006
- 1 teste falhando por BUG-007

**Conclusão:**
- ✅ Validações: 100% funcionais (30/30)
- ⚠️ Cadastro: 55% funcional (BUG-003 afeta visualização)
- ❌ Edição/Exclusão: 0% funcional (BUG-001 bloqueia 100%)
- ⚠️ Navegação: 33% funcional (BUG-006/007)

---

**Documento vivo - atualizado conforme evolução dos testes**  
**Última atualização:** 23/12/2024 18:30  
**Versão:** 2.0 (Completo com Blocos 1-4 implementados)