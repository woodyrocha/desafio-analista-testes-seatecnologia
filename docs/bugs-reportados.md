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
| UI/UX | 0 | 1 | 2 | 1 | 4 |
| Navegação | 1 | 0 | 0 | 0 | 1 |
| **TOTAL** | **4** | **3** | **3** | **1** | **11** |

**Novos Bugs Detectados (23/12/2024):**
- ✅ BUG-001: Documentação completa (10 páginas + 6 screenshots)
- ✅ BUG-003: Documentação completa (8 páginas + 8 screenshots)
- ✅ BUG-006: Documentação completa (6 páginas + 12 screenshots)

**Status dos Testes Automatizados:**
- 66 testes implementados
- 44 testes passando (67%)
- 10 testes falhando (15%)
- 12 testes bloqueados/skipped (18%)

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

## 📊 MÉTRICAS DE BUGS

**Distribuição por Severidade:**
- Crítica: 36% (4/11) ⬆️ +1 (BUG-006 reclassificado)
- Alta: 27% (3/11)
- Média: 27% (3/11)
- Baixa: 9% (1/11)

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

**Impacto nos Testes Automatizados:**
- Total de testes: 66
- Testes passando: 44 (67%)
- Testes falhando: 10 (15%) - Todos devido a bugs conhecidos
- Testes bloqueados: 12 (18%) - 9 por BUG-001, 2 por BUG-002/005, 1 por campos

**Análise de Criticidade:**
```
BUG-001 (CRÍTICO): 9 testes bloqueados (14%)
BUG-003 (CRÍTICO): 8 testes falhando (12%)
BUG-006 (CRÍTICO): 1 teste falhando (2%)
BUG-007 (ALTO): 1 teste falhando (2%)
Total impactado: 19 testes (29% da suite)
```

---

## 🔍 ANÁLISE DE SEGURANÇA

### Testes de Segurança Planejados:
- [ ] XSS em campos de texto
- [ ] SQL Injection em campos de busca/filtro
- [ ] Validação de CPF no backend
- [ ] Autenticação/Autorização (se aplicável)
- [ ] Upload de arquivos maliciosos

**Status Atual:**
- 1 teste de segurança implementado: `tests/security/test_seguranca_inputs.py::test_xss_basic_injection_input`
- Status: SKIPPED (não localiza campos - precisa ajuste)

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

## 📋 ARQUIVOS DE DOCUMENTAÇÃO

**Bugs Principais:**
- `BUG-001-DOCUMENTACAO-COMPLETA.md` (10 páginas)
- `BUG-003-DOCUMENTACAO-COMPLETA.md` (8 páginas)
- `BUG-003-RESUMO-EXECUTIVO.md` (executivo)
- `BUG-006-ICONES-MENU.md` (6 páginas)

**Blocos de Implementação:**
- `EXPLICACAO-BLOCO-1.md` (Correções)
- `EXPLICACAO-BLOCO-2.md` (Navegação)
- `EXPLICACAO-BLOCOS-3-4.md` (Edição e Exclusão)

**Status Geral:**
- `STATUS-GERAL-4-BLOCOS.md` (Panorama completo)

---

**Documento atualizado durante execução dos testes automatizados**  
**Última atualização:** 23/12/2024 18:00  
**Versão:** 2.0 (Atualizado com testes automatizados completos)