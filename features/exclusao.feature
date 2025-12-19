Feature: Exclusão de Funcionário
  Como um usuário do sistema
  Eu quero remover registros

  @e2e
  Scenario: Excluir funcionário existente
    Given que existe um funcionário na lista
    When eu escolho remover esse funcionário
    And confirmo a exclusão
    Then o funcionário não deve mais aparecer na lista

