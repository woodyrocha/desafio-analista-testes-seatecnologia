Feature: Cadastro de Funcionário
  Como um usuário do sistema
  Eu quero cadastrar novos funcionários
  Para que eu possa gerenciar a equipe

  @e2e @smoke
  Scenario: Cadastrar funcionário com dados válidos
    Given que estou na tela de listagem de funcionários
    When eu clico no botão "Adicionar Funcionário"
    And preencho o nome com "João Silva"
    And preencho o CPF com "123.456.789-00"
    And preencho a data de nascimento com "01/01/1990"
    And seleciono o cargo "Analista"
    And clico no botão "Salvar"
    Then o funcionário deve aparecer na lista
    And deve exibir o nome "João Silva"
    And deve exibir o CPF "123.456.789-00"

