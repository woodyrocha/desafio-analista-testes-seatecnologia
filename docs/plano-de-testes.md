# Plano de Testes — Projeto Desafio Analista de Testes

## 1. Objetivo

Definir a abordagem, o escopo, os critérios de aceitação e a estratégia para a execução dos testes (manuais e automatizados) do projeto.

## 2. Escopo

- Funcionalidades críticas: cadastro, edição, exclusão e recuperação de funcionários.
- Validações de formulário: CPF, data de nascimento e campos obrigatórios.
- Navegação: links do menu e redirecionamentos (componente "Em breve").
- Persistência: salvar registros e consultar lista de funcionários.
- Segurança básica: testes de injeção simples (XSS) e inputs maliciosos.
- Evidências: prints e vídeos dos bugs críticos.

Itens fora do escopo inicial:
- Testes cross-browser avançados (padrão será Chrome headless; executar manualmente se necessário).
- Testes visuais automatizados complexos (comparação pixel-a-pixel).

## 3. Critérios de Aceitação

- Cenários críticos (cadastro, edição, exclusão) devem passar sem erros de exceção.
- Validações de CPF e data devem impedir submissão com valores inválidos.
- Dados criados devem aparecer na lista e persistir entre sessões (quando aplicável).
- Não devem ocorrer falhas de segurança simples como reflexo de XSS em campos que exibem texto sem escape.

## 4. Ambiente de Teste

- Requisitos:
  - Python 3.9+ (preferível 3.10+)
  - Chrome (ou Chromium) instalado para execução local
  - `webdriver-manager` para gerenciar o chromedriver automaticamente
  - Ambiente virtual isolado (recomendado: `.venv`)

- Variáveis de ambiente (opcionais):
  - BASE_URL — URL da aplicação alvo (por padrão: http://analista-teste.seatecnologia.com.br)

## 5. Estratégia e Abordagem

- Abordagem mista:
  - Testes manuais para validação visual e exploração inicial.
  - Testes automatizados com pytest + selenium para fluxos repetíveis e regressão.

- Organização:
  - `pages/` — Page Objects
  - `tests/` — testes organizados por tipo (e2e, validations, navigation, security)
  - `utils/` — factories e helpers

- Prioridades:
  1. Fluxo de cadastro completo (end-to-end)
  2. Validações críticas (CPF, data)
  3. Persistência e recuperação
  4. Edição e exclusão
  5. Navegação
  6. Segurança básica

## 6. Casos de Teste Principais (exemplos)

1. Cadastro com dados válidos
   - Pré-condição: aplicação acessível
   - Passos: preencher formulário com dados válidos e submeter
   - Resultado esperado: registro salvo e listado

2. Cadastro com CPF inválido
   - Resultado esperado: mensagem de erro e bloqueio de submissão

3. Cadastro com data inválida / futura
   - Resultado esperado: mensagem de erro e bloqueio de submissão

4. Edição de registro existente
   - Passos: abrir ação de editar no primeiro registro, alterar dados e salvar
   - Resultado esperado: dados atualizados na listagem

5. Exclusão de registro
   - Resultado esperado: registro removido da lista

6. Teste de XSS reflexivo simples
   - Passos: inserir payload `<script>alert(1)</script>` em campo de texto, submeter e verificar se alerta é executado ou se payload é exibido sem execução
   - Resultado esperado: payload não é executado (apenas exibido com escape) ou filtrado

## 7. Critérios de Risco e Prioridade

- Fluxos que manipulam persistência têm prioridade alta.
- Validações de dados que afetam integridade têm prioridade alta.
- Testes de segurança básicos são prioridade média (identificação rápida de problemas óbvios).

## 8. Métricas e Relatórios

- Métricas a coletar:
  - Número de casos executados / passados / falhados
  - Número de bugs abertos / fechados
  - Tempo médio de execução dos testes automatizados

- Relatórios:
  - Logs do pytest e artefatos (HTML) gerados por `pytest-html`
  - Evidências (screenshots) salvas em `evidence/screenshots`

## 9. Cronograma de Execução (curto prazo)

- Sprint curto (4 dias):
  - Dia 1: Análise e testes exploratórios
  - Dia 2: Estrutura da automação e primeiros testes e2e
  - Dia 3: Implementação de validações automatizadas e persistência
  - Dia 4: Reforma e reporte final

## 10. Considerações Finais

- Atualizar seletores nos Page Objects conforme o HTML real da aplicação.
- Configurar CI (GitHub Actions) posteriormente para rodar a suíte automaticamente.
- Manter documentação de bugs em `docs/bugs-reportados.md` e atualizá-la com evidências.

---
