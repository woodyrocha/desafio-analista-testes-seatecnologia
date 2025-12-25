# Relatório de Bugs - Desafio QA Analyst SEA Tecnologia

**Projeto:** Sistema de Cadastro de Funcionários  
**URL:** http://analista-teste.seatecnologia.com.br  
**Data do Teste:** 23/12/2024  
**Analista:** QA Team  
**Ambiente:** Produção (QA Challenge)

---

## 📊 Resumo Executivo

| Categoria | Crítico | Alto | Médio | Baixo | Total |
|-----------|---------|------|-------|-------|-------|
| Funcionalidade | 3 | 2 | 1 | 0 | 6 |
| UI/UX | 1 | 2 | 2 | 1 | 6 |
| Navegação | 1 | 0 | 0 | 0 | 1 |
| Segurança | 0 | 0 | 1 | 0 | 1 |
| Visual/Design | 0 | 2 | 2 | 1 | 5 |
| **TOTAL** | **5** | **6** | **6** | **2** | **19** |

**Bugs Detectados:**
- ✅ BUG-001: Documentação completa (10 páginas + 6 screenshots)
- ✅ BUG-003: Documentação completa (8 páginas + 8 screenshots)
- ✅ BUG-006: Documentação completa (6 páginas + 12 screenshots)
- ✅ BUG-013 a BUG-017: Bugs visuais documentados (MANUAL_REPORT.md)

**Status dos Testes:**
- **89 testes implementados** (82 Python + 7 BDD)
- 60 testes passando (67%)
- 14 testes falhando (16%)
- 15 testes bloqueados/skipped (17%)

---

## 🔴 BUGS CRÍTICOS (Bloqueadores)

### BUG-001: Menu "..." não abre opções de Editar/Excluir ⭐ ATUALIZADO
**Severidade:** 🔴 Crítica  
**Prioridade:** 🔴 Máxima  
**Status:** Aberto  
**Testes Afetados:** 9 testes (14% da suite)  
**Documentação:** `BUG-001-DOCUMENTACAO-COMPLETA.md`

**Descrição:**  
O menu de três pontos ("...") nos cards de funcionário é clicável, mas não exibe as opções de Editar/Excluir conforme especificado no Figma.

**Passos para Reproduzir:**
1. Acessar listagem de funcionários
2. Clicar no ícone "..." de qualquer funcionário
3. Observar comportamento

**Resultado Esperado:**  
Menu dropdown deve abrir com opções "Editar" e "Excluir"

**Resultado Atual:**  
Nada acontece (nenhum menu é exibido)

**Evidências:**
- XPATH: `/html/body/div/main/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[2]`
- Screenshots: 6 capturas (antes/depois de clicar)
  - `evidence/screenshots/funcionario_cadastrado_para_edicao.png`
  - `evidence/screenshots/antes_clicar_menu.png`
  - `evidence/screenshots/depois_clicar_menu.png`
  - `evidence/screenshots/funcionario_cadastrado_para_exclusao.png`
  - `evidence/screenshots/antes_clicar_menu_exclusao.png`
  - `evidence/screenshots/depois_clicar_menu_exclusao.png`

**Análise Técnica:**
- ✅ Elemento existe no DOM
- ✅ Elemento é clicável (sem erro)
- ❌ Clique não abre dropdown
- ❌ Event listener não configurado
- ❌ Ações de edição/exclusão inacessíveis

**Impacto:**  
🔴 **CRÍTICO** 
- Impossibilita edição de funcionários (100%)
- Impossibilita exclusão de funcionários (100%)
- CRUD apenas 50% funcional (falta Update e Delete)
- 9 testes automatizados bloqueados
- Aplicação não utilizável em produção

**Funcionalidades Bloqueadas:**
- Edição de funcionários (4 testes)
- Exclusão de funcionários (5 testes)

**Testes Automatizados Bloqueados:**
```
tests/e2e/test_edicao_funcionario.py:
  - test_edicao_funcionario_fluxo_basico
  - test_edicao_nome_funcionario
  - test_cancelar_edicao_funcionario
  - test_validacoes_durante_edicao

tests/e2e/test_exclusao_funcionario.py:
  - test_exclusao_funcionario_fluxo_basico
  - test_cancelar_exclusao_funcionario
  - test_exclusao_multiplos_funcionarios
  - test_funcionario_excluido_nao_aparece_na_lista
  - test_mensagem_confirmacao_exclusao
```

**Sugestão de Correção:**
```javascript
// Adicionar event listener ao menu
document.querySelectorAll('.menu-opcoes button').forEach(btn => {
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    // Criar dropdown com opções Editar/Excluir
    showDropdown(btn, funcionarioId);
  });
});
```

**Referência Figma:**  
Tela "Lista de Funcionários" - Componente de card com menu de ações

---

### BUG-002: Botão "Adicionar outra Atividade" executa ação de "Voltar"
**Severidade:** Crítica  
**Prioridade:** Alta  
**Status:** Aberto  

**Descrição:**  
O botão "Adicionar outra Atividade" no formulário de cadastro está com ação incorreta configurada - ao invés de adicionar nova atividade, ele executa a ação do botão "Voltar", perdendo todos os dados preenchidos.

**Passos para Reproduzir:**
1. Clicar em "Adicionar Funcionário"
2. Preencher formulário parcialmente
3. Na seção "Quais EPIs o trabalhador usa na atividade?", clicar em "Adicionar outra atividade"
4. Observar comportamento

**Resultado Esperado:**  
Deve adicionar novo conjunto de campos para cadastrar outra atividade/EPI

**Resultado Atual:**  
Retorna para tela de listagem, perdendo todos os dados preenchidos

**Evidências:**
- XPATH: `/html/body/div/main/div[2]/div[2]/form/div[4]/div/button`
- Teste automatizado: `tests/e2e/test_cadastro_com_epi.py::test_cadastro_com_multiplas_atividades`

**Impacto:**  
🔴 **CRÍTICO** - Perda de dados do usuário e impossibilidade de cadastrar múltiplas atividades/EPIs para um funcionário.

**Teste Automatizado:**
- Status: SKIPPED
- Mensagem: "BUG-002: Botão 'Adicionar outra Atividade' volta para tela inicial"

---

### BUG-003: Lista de funcionários não possui scroll - registros ficam ocultos ⭐ ATUALIZADO
**Severidade:** 🔴 Crítica  
**Prioridade:** Alta  
**Status:** Aberto  
**Testes Afetados:** 8 testes (12% da suite)  
**Documentação:** `BUG-003-DOCUMENTACAO-COMPLETA.md`

**Descrição:**  
A lista de funcionários não possui barra de rolagem (scroll), fazendo com que funcionários cadastrados recentemente fiquem ocultos. Apenas os primeiros registros são visíveis.

**Passos para Reproduzir:**
1. Cadastrar mais de 5 funcionários
2. Observar a listagem
3. Tentar visualizar funcionários recém-cadastrados

**Resultado Esperado:**  
Container da lista deve ter scroll vertical ou paginação para acessar todos os registros

**Resultado Atual:**  
Funcionários ficam ocultos no HTML, não há forma de visualizá-los pela interface

**Evidências:**
- Screenshots: 8 capturas automáticas
  - `evidence/screenshots/test_cadastro_com_um_epi_*_FALHA.png`
  - `evidence/screenshots/test_cadastro_funcionario_dados_validos_*_FALHA.png`
  - `evidence/screenshots/test_cadastro_funcionario_sem_epi_*_FALHA.png`
  - `evidence/screenshots/test_cadastro_multiplos_funcionarios_*_FALHA.png`
  - `evidence/screenshots/test_cadastro_com_diferentes_epis_*_FALHA.png` (4 arquivos)
- Contador mostra 17+ funcionários, mas apenas 4-5 visíveis na tela

**Análise Técnica:**
- Container `.lista-funcionarios` sem propriedade `overflow-y: auto`
- Altura não limitada (`max-height` ausente)
- Funcionários existem no DOM mas ficam abaixo da área visível
- Comparação com Figma: Protótipo MOSTRA scroll vertical

**Impacto:**  
🔴 **CRÍTICO** 
- Impossibilita visualização de registros recentes
- Usuário não sabe que cadastro foi bem-sucedido
- 8 testes automatizados falhando
- Não-conformidade com design do Figma

**Testes Automatizados Afetados:**
```
tests/e2e/test_cadastro_com_epi.py:
  - test_cadastro_com_um_epi
  - test_cadastro_com_diferentes_epis (5 parametrizados)

tests/e2e/test_cadastro_funcionario.py:
  - test_cadastro_funcionario_dados_validos
  - test_cadastro_funcionario_sem_epi
  - test_cadastro_multiplos_funcionarios
```

**Sugestão de Correção:**  
```css
.lista-funcionarios {
  max-height: calc(100vh - 200px);
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 10px;
}

/* Estilização da scrollbar */
.lista-funcionarios::-webkit-scrollbar {
  width: 8px;
}

.lista-funcionarios::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}
```

**Workaround Temporário (para testes):**
```python
def rolar_lista_ate_final(driver):
    script = "document.querySelector('.lista-funcionarios').scrollTop = document.querySelector('.lista-funcionarios').scrollHeight;"
    driver.execute_script(script)
    time.sleep(0.5)
```

---

### BUG-004: Ícones do menu lateral não têm ação configurada (BUG-006) ⭐ ATUALIZADO
**Severidade:** 🔴 Crítica  
**Prioridade:** Média  
**Status:** Aberto  
**Testes Afetados:** 1 teste de navegação  
**Documentação:** `BUG-006-ICONES-MENU.md`

**Descrição:**  
Os 6 ícones do menu lateral esquerdo são clicáveis mas não executam nenhuma ação. Segundo o Figma e requisito do email RH, deveriam redirecionar para uma página "Em breve".

**Requisito do Email RH:**
> "Teste os links para assegurar que eles conduzam às etapas e itens de menu corretos. **Todos os links devem levar ao componente 'Em breve'**"

**Passos para Reproduzir:**
1. Clicar em qualquer dos 6 ícones do menu lateral
2. Observar comportamento

**Resultado Esperado:**  
Deve redirecionar para componente/página "Em breve" (conforme Figma e email RH)

**Resultado Atual:**  
Nada acontece (nenhuma navegação)

**Evidências:**
- XPATHs testados:
  - Ícone 1: `/html/body/div/main/div[1]/div[2]/div[1]`
  - Ícone 2: `/html/body/div/main/div[1]/div[2]/div[2]`
  - Ícone 3: `/html/body/div/main/div[1]/div[2]/div[3]`
  - Ícone 4: `/html/body/div/main/div[1]/div[2]/div[4]`
  - Ícone 5: `/html/body/div/main/div[1]/div[2]/div[5]`
  - Ícone 6: `/html/body/div/main/div[1]/div[2]/div[6]`
- Screenshots: 12 capturas (antes/depois de cada ícone)
  - `evidence/screenshots/Ícone_*_antes.png` (6 arquivos)
  - `evidence/screenshots/Ícone_*_depois.png` (6 arquivos)

**Análise Técnica:**
- ✅ Elementos existem no DOM
- ✅ Cursor muda para pointer (indica clicável)
- ❌ Event listeners não configurados
- ❌ URL não muda após clique
- ❌ Nenhuma navegação ocorre

**Impacto:**  
🔴 **CRÍTICO** 
- Navegação principal do sistema não funciona
- Não-conformidade com requisito obrigatório do email RH
- Componente "Em breve" não existe (também é um bug)
- 1 teste automatizado falhando

**Teste Automatizado:**
```
tests/navigation/test_navegacao_links.py:
  - test_navegacao_menu_lateral_icones
    Status: FAILED
    Mensagem: "6 ícones do menu NÃO levam para 'Em breve' conforme especificado no email RH"
```

**Sugestão de Correção:**
```javascript
// 1. Criar página "Em breve"
// 2. Adicionar navegação aos ícones
document.querySelectorAll('.icone-menu').forEach(icone => {
  icone.addEventListener('click', () => {
    window.location.href = '/em-breve';
  });
});
```

**Nota:**  
Componente "Em breve" não existe na aplicação (BUG-010 - também precisa ser implementado).

---

## 🟠 BUGS DE ALTA SEVERIDADE

### BUG-005: Botão "Adicionar EPI" não funciona
**Severidade:** Alta  
**Prioridade:** Média  
**Status:** Aberto  

**Descrição:**  
O botão "Adicionar EPI" é um `<span>` clicável ao invés de `<button>`, e não possui ação configurada.

**Passos para Reproduzir:**
1. Iniciar cadastro de funcionário
2. Não marcar "O trabalhador não usa EPI"
3. Preencher Atividade, EPI e número CA
4. Clicar em "Adicionar EPI"
5. Observar comportamento

**Resultado Esperado:**  
Deve adicionar o EPI à lista e permitir cadastrar outro

**Resultado Atual:**  
Nada acontece

**Evidências:**
- XPATH: `/html/body/div[1]/main/div[2]/div[2]/form/div[4]/div/div/div[2]/span`
- Elemento HTML: `<span>` ao invés de `<button>`
- Teste automatizado: `tests/e2e/test_cadastro_com_epi.py::test_cadastro_com_multiplos_epis`

**Impacto:**  
🟠 **ALTO** - Impossibilita cadastro de múltiplos EPIs para um funcionário.

**Problemas Adicionais:**  
- Elemento tem estilização incorreta (não segue padrão do Figma)
- Uso incorreto de elemento HTML (span ao invés de button)

**Teste Automatizado:**
- Status: SKIPPED
- Mensagem: "BUG-005: Botão 'Adicionar EPI' não funciona"

---

### BUG-006: Campo "Status" exibe "Atividade" no card
**Severidade:** Alta  
**Prioridade:** Baixa  
**Status:** Aberto  

**Descrição:**  
O campo identificado como "Status" no Figma (Ativo/Inativo) está exibindo "Atividade" nos cards da listagem.

**Passos para Reproduzir:**
1. Cadastrar funcionário
2. Visualizar card na listagem
3. Observar segundo campo de informações

**Resultado Esperado:**  
Deve exibir "Ativo" ou "Inativo"

**Resultado Atual:**  
Exibe nome da atividade (ex: "Ativid 02")

**Evidências:**
- XPATH: `/html/body/div/main/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[2]`
- Screenshot: Campo mostra "Ativid 02" ao invés de status

**Impacto:**  
🟠 **ALTO** - Informação crítica (status do funcionário) não está visível.

---

### BUG-007: Botão "Próximo passo" não funciona ⭐ ATUALIZADO
**Severidade:** Alta  
**Prioridade:** Baixa  
**Status:** Aberto  
**Teste Afetado:** 1 teste de navegação

**Descrição:**  
Botão "Próximo passo" existe no footer da listagem mas não possui ação configurada.

**Passos para Reproduzir:**
1. Acessar listagem de funcionários
2. Clicar em "Próximo passo" no rodapé
3. Observar comportamento

**Resultado Esperado:**  
Deve avançar para próxima etapa do fluxo (conforme Figma)

**Resultado Atual:**  
Nada acontece

**Evidências:**
- XPATH: `/html/body/div/main/div[2]/div[3]/button`
- Screenshots:
  - `evidence/screenshots/antes_proximo_passo.png`
  - `evidence/screenshots/depois_proximo_passo.png`

**Análise Técnica:**
- ✅ Botão existe no DOM
- ✅ Botão é clicável
- ❌ Clique não causa navegação
- ❌ URL permanece a mesma

**Impacto:**  
🟠 **ALTO** - Bloqueia progressão no fluxo da aplicação (se houver etapas seguintes).

**Teste Automatizado:**
```
tests/navigation/test_navegacao_links.py:
  - test_navegacao_botao_proximo_passo
    Status: FAILED
    Mensagem: "Botão 'Próximo passo' sem ação"
```

---

## 🟡 BUGS DE MÉDIA SEVERIDADE

### BUG-008: Estilização dos botões difere do Figma
**Severidade:** Média  
**Prioridade:** Baixa  
**Status:** Aberto  

**Descrição:**  
Botões da aplicação possuem estilização diferente da especificada no Figma.

**Componentes Afetados:**
- Botão "Adicionar Funcionário"
- Botão "Salvar"
- Botão "Adicionar EPI" (especialmente problemático)
- Botões de filtro

**Evidências:**
- Comparativo visual: Figma vs Aplicação

**Impacto:**  
🟡 **MÉDIO** - Inconsistência visual, não afeta funcionalidade core.

---

### BUG-009: Campo RG não tem limite de caracteres
**Severidade:** Média  
**Prioridade:** Baixa  
**Status:** Aberto  

**Descrição:**  
Campo RG aceita quantidade ilimitada de caracteres.

**Nota:**  
Não é necessariamente um bug crítico, pois RG pode ter tamanhos variados por estado.

**Sugestão:**  
Validar formato conforme estado ou definir limite razoável (ex: 15 caracteres).

**Impacto:**  
🟡 **MÉDIO** - Risco de dados inconsistentes, mas não bloqueia funcionalidade.

---

### BUG-010: Componente "Em breve" não implementado
**Severidade:** Média  
**Prioridade:** Média  
**Status:** Aberto  

**Descrição:**  
Componente "Em breve" está especificado no Figma mas não existe na aplicação.

**Resultado Esperado:**  
Página/componente de placeholder para funcionalidades futuras

**Resultado Atual:**  
Componente não existe

**Impacto:**  
🟡 **MÉDIO** - Falta de implementação de requisito do Figma.

**Relação:** Bloqueia correção do BUG-004/BUG-006 (ícones do menu)

---

## ⚪ BUGS DE BAIXA SEVERIDADE

### BUG-011: Toggle "Etapa concluída" sem feedback visual claro
**Severidade:** Baixa  
**Prioridade:** Baixa  
**Status:** Aberto  

**Descrição:**  
Toggle "Etapa concluída" no footer da listagem não possui feedback visual claro de mudança de estado.

**Impacto:**  
⚪ **BAIXO** - UX poderia ser melhor, mas não impacta funcionalidade.

---

### BUG-012: Vulnerabilidade Open Redirect 
**Severidade:** 🟡 Média  
**Categoria:** Segurança  
**Prioridade:** Alta  
**Status:** Aberto  
**Teste Afetado:** `tests/security/test_seguranca_basica.py::test_open_redirect`

**Descrição:**  
Aplicação é vulnerável a Open Redirect, permitindo redirecionamento para URLs externas sem validação quando parâmetros de redirecionamento são usados na URL.

**Passos para Reproduzir:**
1. Acessar: `http://analista-teste.seatecnologia.com.br?redirect=https://evil.com`
2. Observar que aplicação redireciona para `evil.com`

**Resultado Esperado:**  
Aplicação deve validar URL de redirecionamento e bloquear domínios externos

**Resultado Atual:**  
Aplicação redireciona sem validação para qualquer URL fornecida

**Payloads Testados:**
```
✅ Detectados como vulneráveis:
- ?redirect=https://evil.com
- ?url=https://evil.com  
- ?next=https://evil.com
- ?return=https://evil.com
```

**Evidências:**
- Screenshot: `evidence/screenshots/test_open_redirect_*_FALHA.png`
- Teste automatizado: FAILED (vulnerabilidade confirmada)

**Impacto:**  
🟡 **MÉDIO** - Pode ser explorada para phishing:
- Atacante pode criar URLs maliciosas aparentando ser legítimas
- Usuários redirecionados para sites de phishing
- Credenciais podem ser roubadas
- Reputação da empresa comprometida

**Correção Sugerida:**
```javascript
function validarRedirect(url) {
  // Whitelist de domínios permitidos
  const dominiosPermitidos = [
    'seatecnologia.com.br',
    'analista-teste.seatecnologia.com.br'
  ];
  
  try {
    const urlObj = new URL(url);
    const dominio = urlObj.hostname;
    
    // Verificar se domínio está na whitelist
    const permitido = dominiosPermitidos.some(d => 
      dominio === d || dominio.endsWith('.' + d)
    );
    
    if (!permitido) {
      console.warn('Redirect bloqueado:', url);
      return '/'; // Redirecionar para home
    }
    
    return url;
  } catch {
    return '/'; // URL inválida, redirecionar para home
  }
}
```

**Esforço Estimado:** 2-3 horas

**Referências:**
- OWASP: Unvalidated Redirects and Forwards
- CWE-601: URL Redirection to Untrusted Site ('Open Redirect')

---

## 📊 MÉTRICAS DE BUGS

**Distribuição por Severidade:**
- Crítica: 33% (4/12)
- Alta: 25% (3/12)
- Média: 33% (4/12) ⬆️ +1 (BUG-012 adicionado)
- Baixa: 8% (1/12)

**Bugs com Documentação Completa:**
- BUG-001: ✅ 10 páginas + 6 screenshots
- BUG-003: ✅ 8 páginas + 8 screenshots
- BUG-006: ✅ 6 páginas + 12 screenshots
- **Total:** 24 páginas + 26 screenshots

**Taxa de Defeitos por Funcionalidade:**
- Cadastro: 4 bugs (2 críticos, 1 alto, 1 médio)
- Listagem: 3 bugs (2 críticos, 1 alto)
- Edição: 1 bug crítico (bloqueador 100%)
- Exclusão: 1 bug crítico (bloqueador 100%)
- Navegação: 2 bugs (1 crítico, 1 alto)
- Segurança: 1 bug médio (Open Redirect)

**Impacto nos Testes Automatizados:**
- Total de testes: 82 ⬆️ +16 (11 segurança + 6 persistência)
- Testes passando: 58 (71%)
- Testes falhando: 10 (12%) - Bugs conhecidos + 1 vulnerabilidade
- Testes bloqueados: 14 (17%)

**Análise de Criticidade:**
```
BUG-001 (CRÍTICO): 9 testes bloqueados (11%)
BUG-003 (CRÍTICO): 6 testes falhando (7%)
BUG-006 (CRÍTICO): 1 teste falhando (1%)
BUG-007 (ALTO): 1 teste falhando (1%)
BUG-012 (MÉDIO): 1 teste falhando (1%) 
Total impactado: 19 testes (23% da suite)
```

---

## 🔍 ANÁLISE DE SEGURANÇA ⭐ ATUALIZADO

### Testes de Segurança Implementados (11 testes):

**tests/security/test_seguranca_basica.py** (6 testes):
- ✅ Security Headers HTTP (X-Content-Type, X-Frame-Options, CSP)
- ✅ Protocolo HTTPS/TLS  
- ✅ Informações Sensíveis Expostas
- ⏸️ Cookies Seguros (SKIPPED - aplicação não usa cookies)
- ✅ Versões de Software Expostas
- ❌ Open Redirect - **VULNERÁVEL** (BUG-012)

**tests/security/test_seguranca_inputs.py** (5 testes):
- ✅ XSS no campo Nome (5 payloads testados)
- ✅ XSS em múltiplos campos
- ✅ SQL Injection básico (5 payloads testados)
- ✅ HTML Injection
- ✅ Path Traversal básico

**Resultados da Execução:**
- **10/11 testes passando** (91%)
- **1 vulnerabilidade REAL detectada**: Open Redirect (BUG-012)

**Análise de Vulnerabilidades:**

✅ **SEGURO contra:**
- XSS (Cross-Site Scripting) - Todos os payloads sanitizados
- SQL Injection - Nenhum erro SQL exposto
- HTML Injection - Tags sanitizadas
- Path Traversal - Bloqueado

❌ **VULNERÁVEL a:**
- **Open Redirect** - Permite redirecionamento para URLs externas sem validação
  - Parâmetros vulneráveis: ?redirect=, ?url=, ?next=, ?return=
  - Impacto: Phishing, roubo de credenciais
  - Severidade: Média (mas pode ser explorada para ataques)

**Conclusão:**
Aplicação possui boa sanitização de inputs (XSS e SQL Injection protegidos), mas apresenta vulnerabilidade de Open Redirect que deve ser corrigida antes de produção.

### Testes de Persistência Implementados (6 testes):

**tests/persistence/test_persistencia_dados.py**:
- ✅ Persistência após refresh (F5)
- ⏸️ Persistência após remover do DOM (SKIPPED - BUG-003)
- ✅ Verificar tipo de storage usado
- ✅ Persistência em nova sessão/aba
- ✅ Limite de storage
- ⏸️ Persistência longo prazo (teste manual)

**Descobertas:**
- Dados persistem dentro da mesma sessão (F5 funciona)
- Dados NÃO persistem entre dias (observação do analista)
- Provável uso de sessionStorage ou localStorage sem backend
- Sem API para persistência real

---

## 🎨 BUGS VISUAIS/DESIGN (Comparação Figma vs Aplicação)

### BUG-013: Stepper não enumera itens sequencialmente
**Severidade:** 🟠 Alta  
**Prioridade:** 🟠 Alta  
**Status:** Aberto  
**Categoria:** Visual/UX

**Descrição:**  
A barra de progresso (stepper) no topo da página exibe "ITEM 1" repetidamente ao invés de enumerar sequencialmente (Item 1, Item 2, Item 3...).

**Comportamento Esperado (Figma):**
- Stepper deve exibir: Item 1, Item 2, Item 3, Item 4... Item 9
- Cada step deve ter numeração única e sequencial

**Comportamento Atual:**
- Stepper exibe: ITEM 1, ITEM 1, ITEM 1, ITEM 1... ITEM 1
- Todos os steps mostram o mesmo texto

**Impacto:**
- Usuário não consegue identificar em qual etapa está
- Prejudica UX e navegabilidade

**Evidências:**
- `manual_tests/manual_screenshots/Screenshot_01_FIGMA_from_2025-12-24_18-28-40.png`
- `manual_tests/manual_screenshots/Screenshot_01_APP_from_2025-12-24_18-28-48.png`

**Documentação Completa:** `MANUAL_REPORT.md`

---

### BUG-014: Botão "Limpar filtros" com cor incorreta
**Severidade:** 🟡 Média  
**Prioridade:** 🟡 Média  
**Status:** Aberto  
**Categoria:** Visual/Design System

**Descrição:**  
O botão "Limpar filtros" está implementado com estilização diferente do design aprovado no Figma.

**Comportamento Esperado (Figma):**
- Botão outline (borda colorida, fundo transparente)
- Cor da borda: azul padrão do sistema

**Comportamento Atual:**
- Botão com preenchimento sólido azul claro
- Não respeita estilo outline do Figma

**Impacto:**
- Funcionalidade preservada
- Inconsistência visual com design system

**Evidências:**
- `manual_tests/manual_screenshots/Screenshot_02_FIGMA_from_2025-12-24_18-29-07.png`
- `manual_tests/manual_screenshots/Screenshot_02_APP_from_2025-12-24_18-29-19.png`

**Documentação Completa:** `MANUAL_REPORT.md`

---

### BUG-015: Toggle mal posicionado + ausência de marca d'água de fundo
**Severidade:** 🟡 Média  
**Prioridade:** 🟡 Média  
**Status:** Aberto  
**Categoria:** Visual/Layout

**Descrição:**  
Múltiplos problemas visuais na área do formulário:
1. Toggle "A etapa está concluída?" posicionado incorretamente
2. Botão "Próximo passo" dentro de DIV incorreta
3. Ausência de marca d'água/watermark de fundo conforme Figma

**Comportamento Esperado (Figma):**
- Toggle alinhado à direita do container
- Marca d'água (watermark) no fundo da página

**Comportamento Atual:**
- Toggle em posição diferente
- Fundo totalmente branco, sem marca d'água

**Impacto:**
- Impacto visual significativo
- Layout desalinhado com design

**Evidências:**
- `manual_tests/manual_screenshots/Screenshot_03_FIGMA_from_2025-12-24_18-29-50.png`
- `manual_tests/manual_screenshots/Screenshot_03_APP_from_2025-12-24_18-29-58.png`

**Documentação Completa:** `MANUAL_REPORT.md`

---

### BUG-016: Formulário com cores e fontes diferentes do Figma
**Severidade:** 🟠 Alta  
**Prioridade:** 🟠 Alta  
**Status:** Aberto  
**Categoria:** Visual/Design System

**Descrição:**  
Todo o formulário de cadastro apresenta cores e tipografia diferentes do design aprovado:
- Cores dos campos de input
- Tonalidade do toggle "Ativo/Inativo"
- Fontes e tamanhos de texto
- Espaçamentos

**Comportamento Esperado (Figma):**
- Paleta de cores específica definida no design system
- Tipografia: família, tamanho e peso conforme design

**Comportamento Atual:**
- Cores aplicadas diferem do Figma
- Fontes não seguem especificação do design

**Impacto:**
- Toda a identidade visual comprometida
- Inconsistência generalizada no design system

**Evidências:**
- `manual_tests/manual_screenshots/Screenshot_04_FIGMA_from_2025-12-24_18-31-11.png`
- `manual_tests/manual_screenshots/Screenshot_04_APP_from_2025-12-24_18-31-18.png`

**Documentação Completa:** `MANUAL_REPORT.md`

---

### BUG-017: Botão "Adicionar EPI" sem estilização + ausência botão "Próximo passo"
**Severidade:** 🔴 Crítica  
**Prioridade:** 🔴 Máxima  
**Status:** Aberto  
**Categoria:** Visual/Funcionalidade

**Descrição:**  
Dois problemas na seção de EPIs:
1. Botão "Adicionar EPI" não está estilizado conforme Figma (deveria ser link-style azul)
2. Botão "Próximo passo" não aparece na aplicação (existe no Figma)

**Comportamento Esperado (Figma):**
- Botão "Adicionar EPI" em azul claro, estilo link (text button)
- Botão "Próximo passo" visível no canto inferior direito

**Comportamento Atual:**
- Botão "Adicionar EPI" com estilização padrão/diferente
- Botão "Próximo passo" AUSENTE (não renderizado)

**Impacto:**
- **CRÍTICO:** Botão "Próximo passo" ausente quebra fluxo de navegação
- Usuário não consegue avançar na jornada
- Estilização incorreta prejudica consistência

**Evidências:**
- `manual_tests/manual_screenshots/Screenshot_05_FIGMA_from_2025-12-24_18-31-43.png`
- `manual_tests/manual_screenshots/Screenshot_05_APP_from_2025-12-24_18-31-52.png`

**Documentação Completa:** `MANUAL_REPORT.md`

---

## 📝 OBSERVAÇÕES GERAIS

1. **Conformidade com Figma**: Aplicação apresenta múltiplas divergências do design especificado
2. **Funcionalidades Incompletas**: Várias features do Figma não implementadas
3. **Problemas de UX**: Lista sem scroll é o problema mais crítico de usabilidade
4. **Qualidade do Código**: Elementos HTML incorretos (span ao invés de button)
5. **CRUD Incompleto**: Sistema apenas 50% funcional (falta Update e Delete)

**Pontos Positivos:**
- ✅ Validações de CPF funcionam corretamente (13 testes)
- ✅ Validações de Data funcionam corretamente (17 testes)
- ✅ Cadastro funciona (com ressalvas de visualização)
- ✅ Botão "Voltar" funciona corretamente

**Pontos Críticos:**
- ❌ CRUD incompleto (sem edição/exclusão)
- ❌ Lista sem scroll oculta funcionários
- ❌ Navegação principal não funciona
- ❌ Múltiplos EPIs/atividades impossível

---


**Documento atualizado durante execução dos testes automatizados e manuais**  
**Última atualização:** 24/12/2025