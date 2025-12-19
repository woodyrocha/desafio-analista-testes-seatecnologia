# Relatório de Bugs - Desafio QA Analyst SEA Tecnologia

**Projeto:** Sistema de Cadastro de Funcionários  
**URL:** http://analista-teste.seatecnologia.com.br  
**Data do Teste:** 19/12/2024  
**Analista:** [Seu Nome]  
**Ambiente:** Produção (QA Challenge)

---

## 📊 Resumo Executivo

| Categoria | Crítico | Alto | Médio | Baixo | Total |
|-----------|---------|------|-------|-------|-------|
| Funcionalidade | 3 | 2 | 1 | 0 | 6 |
| UI/UX | 0 | 1 | 2 | 1 | 4 |
| Navegação | 1 | 0 | 0 | 0 | 1 |
| **TOTAL** | **4** | **3** | **3** | **1** | **11** |

---

## 🔴 BUGS CRÍTICOS (Bloqueadores)

### BUG-001: Menu "..." não abre opções de Editar/Excluir
**Severidade:** Crítica  
**Prioridade:** Alta  
**Status:** Aberto  

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
- Screenshot: `evidence/screenshots/bug-001-menu-tres-pontos.png`
- XPATH: `/html/body/div/main/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[2]`

**Impacto:**  
🔴 **CRÍTICO** - Impossibilita edição e exclusão de funcionários, bloqueando fluxos essenciais do sistema.

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

**Impacto:**  
🔴 **CRÍTICO** - Perda de dados do usuário e impossibilidade de cadastrar múltiplas atividades/EPIs para um funcionário.

---

### BUG-003: Lista de funcionários não possui scroll - registros ficam ocultos
**Severidade:** Crítica  
**Prioridade:** Alta  
**Status:** Aberto  

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
- Screenshot: `evidence/screenshots/bug-003-lista-sem-scroll.png`
- Contador mostra 17+ funcionários, mas apenas 4-5 visíveis na tela

**Impacto:**  
🔴 **CRÍTICO** - Impossibilita visualização e gerenciamento de registros mais recentes.

**Sugestão de Correção:**  
Adicionar `overflow-y: auto` no container da lista com altura máxima definida.

---

### BUG-004: Ícones do menu lateral não têm ação configurada
**Severidade:** Crítica  
**Prioridade:** Média  
**Status:** Aberto  

**Descrição:**  
Os 6 ícones do menu lateral esquerdo são clicáveis mas não executam nenhuma ação. Segundo o Figma, deveriam redirecionar para uma página "Em breve".

**Passos para Reproduzir:**
1. Clicar em qualquer dos 6 ícones do menu lateral
2. Observar comportamento

**Resultado Esperado:**  
Deve redirecionar para componente/página "Em breve" (conforme Figma)

**Resultado Atual:**  
Nada acontece (nenhuma navegação)

**Evidências:**
- XPATHs: `/html/body/div/main/div[1]/div[2]/div[1]` até `div[6]`

**Impacto:**  
🔴 **CRÍTICO** - Navegação principal do sistema não funciona.

**Nota:**  
Componente "Em breve" não existe na aplicação (também é um bug - falta implementação).

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

**Impacto:**  
🟠 **ALTO** - Impossibilita cadastro de múltiplos EPIs para um funcionário.

**Problemas Adicionais:**  
- Elemento tem estilização incorreta (não segue padrão do Figma)

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

### BUG-007: Botão "Próximo passo" não funciona
**Severidade:** Alta  
**Prioridade:** Baixa  
**Status:** Aberto  

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

**Impacto:**  
🟠 **ALTO** - Bloqueia progressão no fluxo da aplicação (se houver etapas seguintes).

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

## 📋 BUGS PENDENTES DE INVESTIGAÇÃO

_Seção reservada para bugs encontrados durante testes automatizados ou exploratórios futuros_

### Template de Bug:
```markdown
### BUG-XXX: [Título descritivo]
**Severidade:** [Crítica|Alta|Média|Baixa]  
**Prioridade:** [Alta|Média|Baixa]  
**Status:** [Aberto|Em Análise|Corrigido|Fechado]  

**Descrição:**  
[Descrição detalhada do problema]

**Passos para Reproduzir:**
1. [Passo 1]
2. [Passo 2]

**Resultado Esperado:**  
[O que deveria acontecer]

**Resultado Atual:**  
[O que realmente acontece]

**Evidências:**
- [Screenshots, logs, etc]

**Impacto:**  
[Descrição do impacto no negócio/usuário]
```

---

## 🔐 ANÁLISE DE SEGURANÇA

_Seção reservada para testes de segurança (XSS, SQL Injection, etc)_

### Testes a Realizar:
- [ ] XSS em campos de texto
- [ ] SQL Injection em campos de busca/filtro
- [ ] Validação de CPF no backend
- [ ] Autenticação/Autorização (se aplicável)
- [ ] Upload de arquivos maliciosos

---

## 📈 MÉTRICAS

**Taxa de Defeitos por Funcionalidade:**
- Cadastro: 4 bugs
- Listagem: 3 bugs
- Edição: 1 bug (não testável devido BUG-001)
- Exclusão: 1 bug (não testável devido BUG-001)
- Navegação: 2 bugs

**Distribuição de Severidade:**
- Crítica: 36% (4/11)
- Alta: 27% (3/11)
- Média: 27% (3/11)
- Baixa: 9% (1/11)

---

## 📝 OBSERVAÇÕES GERAIS

1. **Conformidade com Figma**: Aplicação apresenta múltiplas divergências do design especificado
2. **Funcionalidades Incompletas**: Várias features do Figma não implementadas
3. **Problemas de UX**: Lista sem scroll é o problema mais crítico de usabilidade
4. **Qualidade do Código**: Elementos HTML incorretos (span ao invés de button)

---

**Documento gerado automaticamente durante execução dos testes**  
**Última atualização:** 19/12/2024 20:30