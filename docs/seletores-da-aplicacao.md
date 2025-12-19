# SELETORES DA APLICAÇÃO

## TELA 1 - LISTA DE FUNCIONÁRIOS

### Menu Lateral
- Ícone 1: /html/body/div/main/div[1]/div[2]/div[1] 
- Ícone 2: /html/body/div/main/div[1]/div[2]/div[2]
- Ícone 3: /html/body/div/main/div[1]/div[2]/div[3]
- Ícone 4: /html/body/div/main/div[1]/div[2]/div[4]
- Ícone 5: /html/body/div/main/div[1]/div[2]/div[5]
- Ícone 6: /html/body/div/main/div[1]/div[2]/div[6]
- (ERRO DETECTADO: No figma esses botões deveriam navegar para a página EM BREVE, no aplicativo nenhum tem efeito ou ação configuradas apesar de serem clicáveis)

### Componente "Em breve"
- Banner: [ID/CLASS/XPATH] (ERRO DETECTADO: No Figma o elemento existe, porém no aplicativo a página não navega até as outras para capturar XPATH)

### Barra Superior
- Botão "+ Adicionar Funcionário": /html/body/div/main/div[2]/div[2]/div[2]/button

### Filtros
- Botão "Ver apenas ativos": /html/body/div/main/div[2]/div[2]/div[2]/div[1]/button[1]
- Botão "Limpar filtros": /html/body/div/main/div[2]/div[2]/div[2]/div[1]/button[2]

### Card de Funcionário (PRIMEIRO DA LISTA)
- Card container: /html/body/div/main/div[2]/div[2]/div[2]
- Nome: /html/body/div/main/div[2]/div[2]/div[2]/div[2]/div/div[1]/span
- CPF: /html/body/div/main/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[1]
- Status: /html/body/div/main/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[2] (ERRO DETECTADO: Este elemento no figma representa o Status, e no aplicativo representa a Atividade)
- Cargo: /html/body/div/main/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[3]
- Menu "...": /html/body/div/main/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[2] (ERRO DETECTADO: Elemento é clicável, no figma abre menu com Excluir/Editar, mas não abre no aplicativo)
- Opção "Editar": [ID/CLASS/XPATH] (ERRO DETECTADO: Elemento MENU é clicável, no figma abre menu com Excluir/Editar, mas não abre no aplicativo)
- Opção "Excluir": [ID/CLASS/XPATH] (ERRO DETECTADO: Elemento MENU é clicável, no figma abre menu com Excluir/Editar, mas não abre no aplicativo)
- Botão Etapa Concluída: /html/body/div/main/div[2]/div[2]/div[2]/div[3]/button
- Botão "Próximo passo": /html/body/div/main/div[2]/div[3]/button (ERRO DETECTADO: Botão existe mas não está configurado para ter alguma ação)

## TELA 2 - FORMULÁRIO

### Dados Básicos
- Botão de voltar: /html/body/div/main/div[2]/div[2]/form/div[1]/button
- Status (Botão Ativo/Inativo): /html/body/div/main/div[2]/div[2]/form/div[2]/button
- Campo Nome: /html/body/div/main/div[2]/div[2]/form/div[3]/div/div[1]/input
- Radio Feminino: /html/body/div/main/div[2]/div[2]/form/div[3]/div/div[2]/div/label[2]/span[1]/input
- Radio Masculino: /html/body/div/main/div[2]/div[2]/form/div[3]/div/div[2]/div/label[1]/span[1]/input
- Campo CPF: /html/body/div/main/div[2]/div[2]/form/div[3]/div/div[3]/input
- Campo Data Nascimento: /html/body/div/main/div[2]/div[2]/form/div[3]/div/div[4]/input (OBSERVAÇÃO: Esse elemento tem um calendário embarcado, porém ele aceita digitação, acredito que digitar é melhor para os testes automáticos)
- Campo RG: /html/body/div/main/div[2]/div[2]/form/div[3]/div/div[5]/input (OBSERVAÇÃO: Campo não limita o número de caractéres, o que não chega a ser problema pois o númro de digitos do RG pode variar)
- Dropdown Cargo: /html/body/div/main/div[2]/div[2]/form/div[3]/div/div[6]/div/div
- Span Dropdown Cargo (1 a 5): //*[@id="rc_select_12"] (OBSERVAÇÃO: Consegui perceber através do devtools que esse ID É DINÂMICO, e dentro do Span de seleção do cargo ele adquire um "_list_0" até "_list_4" para representar os 5 cargos)

### EPIs
- Checkbox "Não usa EPI": /html/body/div/main/div[2]/div[2]/form/div[4]/div/label/span[1]/input
- Dropdown Atividade: /html/body/div/main/div[2]/div[2]/form/div[4]/div/div/div[1]/div/div
- Span Dropdown Atividade (1 a 5): /html/body/div[1]/main/div[2]/div[2]/form/div[4]/div/div/div[1]/div/div/span[2] (OBSERVAÇÃO: Consegui perceber através do devtools que esse ID É DINÂMICO) 
- Dropdown EPI: /html/body/div[1]/main/div[2]/div[2]/form/div[4]/div/div/div[2]/div/div[1]/div
- Span Dropdown EPI (1 a 5): /html/body/div[1]/main/div[2]/div[2]/form/div[4]/div/div/div[2]/div/div[1]/div/div/span[2] (OBSERVAÇÃO: Também tem ID DINÂMICO, e 5 opções de EPI Capacete de segurança, Luvas descartáveis, Óculos de proteção, Calçado de segurança, Protetor auditivo)
- Campo número CA: /html/body/div[1]/main/div[2]/div[2]/form/div[4]/div/div/div[2]/div/div[2]/input
- Botão "Adicionar EPI": /html/body/div[1]/main/div[2]/div[2]/form/div[4]/div/div/div[2]/span (ERRO DETECTADO: DOIS ERROS, primeiro que visualmente o elemento não atende aos requisitos do figma, vai precisar de evidência visual, segundo que deveria ser um button e é só um span que é clicável mas não tem ação configurada, até porque não é button)
- Botão "Adicionar outra Atividade": /html/body/div/main/div[2]/div[2]/form/div[4]/div/button (ERRO DETECTADO: Botão existe, possui ação configurada, mas ou por erro ou má configuração ele tem a mesma ação do botão de "Voltar", perdendo o preenchimento feito anteriormente e voltando para a tela inicial de "Adicionar funcionário")

### Botões
- Input Selecione arquivo: //*[@id="file"]
- Botão Selecione arquivo: /html/body/div[1]/main/div[2]/div[2]/form/div[5]/div/label
- Botão "Salvar": /html/body/div[1]/main/div[2]/div[2]/form/button
- Botão "Próximo passo": [ID/CLASS/XPATH] (ERRO DETECTADO: Botão "Próximo passo" só aparece na tela do Card do Funcionário, e mesmo lá não funciona para avançar)

### Observações gerais

- No geral, os botões estão com estilização diferente da proposta no figma, e o mais grotesco é o Botão "Adicionar EPI".
- No geral, os botões que deveriam levar para a página do componente EM BREVE nenhum está funcional, então a navegação fica presa entre a página com os dados dos funcionário e botão de adicionar funcionário, e a página do formulário de cadastro de funcionário.
- A listagem dos funcionário possívelmente necessiria de uma div container própria e com scroll bar vertical, pois ficam ocultos dentro do HTML os funcionários que vão sendo adicionados, aparecem apenas os do topo da lista.