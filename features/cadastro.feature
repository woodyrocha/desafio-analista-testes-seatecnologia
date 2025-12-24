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

  @e2e @epi
  Scenario: Cadastrar funcionário com EPI
    Given que estou na tela de listagem de funcionários
    When eu clico no botão "Adicionar Funcionário"
    And preencho todos os campos obrigatórios com dados válidos
    And seleciono o EPI "Capacete"
    And seleciono a atividade "Soldagem"
    And clico no botão "Salvar"
    Then o funcionário deve aparecer na lista
    And deve exibir o EPI selecionado

  @e2e @validations
  Scenario: Tentar cadastrar sem campos obrigatórios
    Given que estou no formulário de cadastro
    When clico no botão "Salvar" sem preencher campos
    Then deve exibir mensagens de erro nos campos obrigatórios
    And o cadastro não deve ser salvo
