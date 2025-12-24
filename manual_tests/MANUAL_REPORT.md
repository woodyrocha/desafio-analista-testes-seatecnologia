# Relatório de Testes Manuais - Bugs Visuais/UI

**Projeto:** Sistema de Cadastro de Funcionários  
**Data dos Testes:** 24/12/2025  
**Testador:** Analista QA  
**Tipo de Teste:** Comparação Visual (Figma vs Aplicação)  
**Total de Bugs Encontrados:** 5

---

## 🎯 Escopo dos Testes Manuais

Este documento registra **bugs visuais/UI** identificados através da comparação entre o design aprovado no Figma e a implementação real da aplicação web.

**Metodologia:**
- Comparação lado a lado: Figma (design) vs Aplicação (implementação)
- Validação de cores, fontes, espaçamentos e componentes
- Foco em inconsistências de estilização

---

## 🐛 BUG-013: Stepper não enumera itens sequencialmente

### 📝 Descrição
A barra de progresso (stepper) no topo da página exibe "ITEM 1" repetidamente ao invés de enumerar sequencialmente (Item 1, Item 2, Item 3...).

### ✅ Comportamento Esperado (Figma)
- Stepper deve exibir: **Item 1, Item 2, Item 3, Item 4... Item 9**
- Cada step deve ter numeração única e sequencial
- Primeira etapa destacada, demais em cinza

### ❌ Comportamento Atual (Aplicação)
- Stepper exibe: **ITEM 1, ITEM 1, ITEM 1, ITEM 1... ITEM 1**
- Todos os steps mostram o mesmo texto
- Numeração sequencial não está implementada

### 📸 Evidências
**Screenshot 01 - FIGMA (correto):**  
![Screenshot_01_FIGMA](evidence/manual/Screenshot_01_FIGMA_from_2025-12-24_18-28-40.png)
- Numeração sequencial: Item 1, Item 2, Item 3, Item 4...

**Screenshot 01 - APP (incorreto):**  
![Screenshot_01_APP](evidence/manual/Screenshot_01_APP_from_2025-12-24_18-28-48.png)
- Todos os itens exibem "ITEM 1"

### 💥 Impacto
**🟡 Médio**
- Não impede funcionalidade mas causa confusão
- Usuário não consegue identificar em qual etapa está
- Prejudica UX e navegabilidade

### 🎯 Prioridade
**Alta** - Afeta usabilidade e orientação do usuário

### 🔧 Sugestão de Correção
Implementar loop de enumeração nos componentes do stepper:
```jsx
{steps.map((step, index) => (
  <StepItem key={index}>
    Item {index + 1}
  </StepItem>
))}
```

---

## 🐛 BUG-014: Botão "Limpar filtros" com cor incorreta

### 📝 Descrição
O botão "Limpar filtros" está implementado com estilização diferente do design aprovado no Figma.

### ✅ Comportamento Esperado (Figma)
- Botão **outline** (borda colorida, fundo transparente)
- Cor da borda: azul padrão do sistema
- Estilo: secondary/outline button

### ❌ Comportamento Atual (Aplicação)
- Botão com **preenchimento sólido** azul claro
- Não respeita estilo outline do Figma
- Cor de fundo não deveria existir

### 📸 Evidências
**Screenshot 02 - FIGMA (correto):**  
![Screenshot_02_FIGMA](evidence/manual/Screenshot_02_FIGMA_from_2025-12-24_18-29-07.png)
- Botão outline, sem preenchimento

**Screenshot 02 - APP (incorreto):**  
![Screenshot_02_APP](evidence/manual/Screenshot_02_APP_from_2025-12-24_18-29-19.png)
- Botão com preenchimento azul claro

### 💥 Impacto
**🟢 Baixo**
- Funcionalidade preservada
- Apenas inconsistência visual com design system

### 🎯 Prioridade
**Média** - Desalinhamento com design system

### 🔧 Sugestão de Correção
Aplicar classe/estilo correto ao botão:
```jsx
<Button variant="outline">Limpar filtros</Button>
```

---

## 🐛 BUG-015: Toggle "A etapa está concluída?" mal posicionado + ausência de marca d'água de fundo

### 📝 Descrição
Múltiplos problemas visuais na área do formulário:
1. Toggle "A etapa está concluída?" posicionado incorretamente
2. Botão "Próximo passo" dentro de DIV incorreta
3. Ausência de marca d'água/watermark de fundo conforme Figma

### ✅ Comportamento Esperado (Figma)
- Toggle alinhado à direita do container
- Botão "Próximo passo" posicionado no canto inferior direito
- Marca d'água (watermark) no fundo da página

### ❌ Comportamento Atual (Aplicação)
- Toggle aparece em posição diferente
- Botão "Próximo passo" dentro de DIV errada (não visível na screenshot)
- Fundo totalmente branco, sem marca d'água

### 📸 Evidências
**Screenshot 03 - FIGMA (correto):**  
![Screenshot_03_FIGMA](evidence/manual/Screenshot_03_FIGMA_from_2025-12-24_18-29-50.png)
- Marca d'água visível no fundo
- Toggle bem posicionado

**Screenshot 03 - APP (incorreto):**  
![Screenshot_03_APP](evidence/manual/Screenshot_03_APP_from_2025-12-24_18-29-58.png)
- Fundo branco puro, sem marca d'água
- Toggle em posição diferente

### 💥 Impacto
**🟡 Médio**
- Impacto visual significativo
- Layout desalinhado com design

### 🎯 Prioridade
**Média** - Múltiplas inconsistências visuais

### 🔧 Sugestão de Correção
1. Ajustar posicionamento do toggle
2. Mover botão "Próximo passo" para container correto
3. Adicionar background-image ou watermark ao container principal

---

## 🐛 BUG-016: Formulário com cores e fontes diferentes do Figma

### 📝 Descrição
Todo o formulário de cadastro apresenta cores e tipografia diferentes do design aprovado:
- Cores dos campos de input
- Tonalidade do toggle "Ativo/Inativo"
- Fontes e tamanhos de texto
- Espaçamentos

### ✅ Comportamento Esperado (Figma)
- Paleta de cores específica definida no design system
- Toggle com cores e estados visuais específicos
- Tipografia: família, tamanho e peso conforme design

### ❌ Comportamento Atual (Aplicação)
- Cores aplicadas diferem do Figma
- Toggle "Ativo/Inativo" com estilização visual diferente
- Fontes não seguem especificação do design

### 📸 Evidências
**Screenshot 04 - FIGMA (correto):**  
![Screenshot_04_FIGMA](evidence/manual/Screenshot_04_FIGMA_from_2025-12-24_18-31-11.png)
- Design system correto aplicado

**Screenshot 04 - APP (incorreto):**  
![Screenshot_04_APP](evidence/manual/Screenshot_04_APP_from_2025-12-24_18-31-18.png)
- Cores e fontes divergentes

### 💥 Impacto
**🟡 Médio**
- Toda a identidade visual comprometida
- Inconsistência generalizada no design system

### 🎯 Prioridade
**Alta** - Impacto abrangente na UI

### 🔧 Sugestão de Correção
1. Revisar e aplicar variáveis CSS do design system
2. Importar fontes corretas do Figma
3. Validar tokens de cores (primary, secondary, etc.)
4. Ajustar componente Toggle para match com Figma

---

## 🐛 BUG-017: Botão "Adicionar EPI" sem estilização correta + ausência do botão "Próximo passo"

### 📝 Descrição
Dois problemas na seção de EPIs:
1. Botão "Adicionar EPI" não está estilizado conforme Figma (deveria ser link-style azul)
2. Botão "Próximo passo" não aparece na aplicação (existe no Figma)

### ✅ Comportamento Esperado (Figma)
- Botão "Adicionar EPI" em **azul claro, estilo link** (text button)
- Botão **"Próximo passo"** visível no canto inferior direito
- Layout completo com todos os elementos

### ❌ Comportamento Atual (Aplicação)
- Botão "Adicionar EPI" com estilização padrão/diferente
- Botão **"Próximo passo" ausente** (não renderizado)
- Layout incompleto

### 📸 Evidências
**Screenshot 05 - FIGMA (correto):**  
![Screenshot_05_FIGMA](evidence/manual/Screenshot_05_FIGMA_from_2025-12-24_18-31-43.png)
- Botão "Adicionar EPI" em azul (link-style)
- Botão "Próximo passo" presente

**Screenshot 05 - APP (incorreto):**  
![Screenshot_05_APP](evidence/manual/Screenshot_05_APP_from_2025-12-24_18-31-52.png)
- Botão "Adicionar EPI" estilização diferente
- Botão "Próximo passo" **NÃO EXISTE**

### 💥 Impacto
**🔴 Alto**
- Botão "Próximo passo" ausente **quebra fluxo de navegação**
- Usuário não consegue avançar na jornada
- Estilização incorreta prejudica consistência

### 🎯 Prioridade
**Crítica** - Botão de navegação ausente

### 🔧 Sugestão de Correção
1. Implementar botão "Próximo passo" no layout
2. Ajustar estilo do "Adicionar EPI" para text button:
```jsx
<Button variant="link" color="primary">
  Adicionar EPI
</Button>
```
3. Posicionar "Próximo passo" no canto inferior direito

---

## 📊 Resumo Executivo

### Bugs por Prioridade
| Prioridade | Quantidade | IDs |
|------------|-----------|-----|
| 🔴 **Crítica** | 1 | BUG-017 |
| 🟠 **Alta** | 2 | BUG-013, BUG-016 |
| 🟡 **Média** | 2 | BUG-014, BUG-015 |
| 🟢 **Baixa** | 0 | - |

### Bugs por Categoria
| Categoria | Quantidade | Descrição |
|-----------|-----------|-----------|
| **Layout/Posicionamento** | 2 | BUG-015, BUG-017 |
| **Cores/Estilização** | 3 | BUG-014, BUG-016, BUG-017 |
| **Conteúdo Dinâmico** | 1 | BUG-013 |
| **Elementos Ausentes** | 1 | BUG-017 |

### Impacto nos Pilares de Qualidade
| Pilar | Impacto | Observação |
|-------|---------|------------|
| **Funcionalidade** | 🔴 Alto | BUG-017 impede navegação |
| **Usabilidade** | 🟡 Médio | BUG-013 confunde usuário |
| **Consistência Visual** | 🔴 Alto | Todos os bugs afetam |
| **Design System** | 🔴 Alto | Divergência generalizada |

---

## 🎯 Recomendações

### Ações Imediatas (Críticas)
1. **Implementar botão "Próximo passo"** (BUG-017)
   - Sem este botão, fluxo de navegação está quebrado

### Ações Prioritárias (Alta)
2. **Corrigir enumeração do stepper** (BUG-013)
3. **Aplicar design system corretamente** (BUG-016)
   - Revisar variáveis CSS
   - Validar tokens de cores e fontes

### Ações de Melhoria (Média)
4. **Ajustar estilização de botões** (BUG-014, BUG-017)
5. **Corrigir layout e marca d'água** (BUG-015)

---

## 📝 Notas do Testador

### Metodologia Aplicada
- ✅ Comparação visual Figma vs App (lado a lado)
- ✅ Screenshots capturados com nomenclatura padronizada
- ✅ Validação de cores, fontes, espaçamentos
- ✅ Testes realizados em Firefox ESR (Linux)

### Escopo dos Testes
- ✅ **Testado:** Estilização e layout visual
- ❌ **Não testado:** Funcionalidades (coberto por testes automatizados)
- ❌ **Não testado:** Responsividade mobile (layout 100% web)
- ❌ **Não testado:** Acessibilidade (fora do escopo)

### Ferramentas Utilizadas
- Figma (referência de design)
- Firefox ESR (navegador de teste)
- Screenshot nativo Linux (captura de tela)

---

## 📂 Evidências Completas

Todas as evidências visuais estão armazenadas em:
```
/manual_tests/manual_screenshots
├── Screenshot_01_APP_from_2025-12-24_18-28-48.png
├── Screenshot_01_FIGMA_from_2025-12-24_18-28-40.png
├── Screenshot_02_APP_from_2025-12-24_18-29-19.png
├── Screenshot_02_FIGMA_from_2025-12-24_18-29-07.png
├── Screenshot_03_APP_from_2025-12-24_18-29-58.png
├── Screenshot_03_FIGMA_from_2025-12-24_18-29-50.png
├── Screenshot_04_APP_from_2025-12-24_18-31-18.png
├── Screenshot_04_FIGMA_from_2025-12-24_18-31-11.png
├── Screenshot_05_APP_from_2025-12-24_18-31-52.png
└── Screenshot_05_FIGMA_from_2025-12-24_18-31-43.png
```

---

**Documento gerado em:** 24/12/2025  
**Versão:** 1.0  
**Status:** ✅ Concluído