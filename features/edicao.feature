Feature: Edição de Funcionário
  Como um usuário do sistema
  Eu quero editar registros existentes

  @e2e
  Scenario: Editar funcionário existente
    Given que existe um funcionário cadastrado
    When eu edito o nome para "Maria Souza"
    And clico em "Salvar"
    Then a lista deve exibir "Maria Souza"

