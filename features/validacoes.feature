Feature: Validações de Campos
  Cenários de validação para CPF e data

  @validations
  Scenario: CPF inválido
    Given que estou no formulário de cadastro
    When preencho o CPF com "111.111.111-11"
    And clico em "Salvar"
    Then deve exibir mensagem de erro "CPF inválido"

  @validations
  Scenario: Data inválida
    Given que estou no formulário de cadastro
    When preencho a data de nascimento com "31/02/1990"
    And clico em "Salvar"
    Then deve exibir mensagem de erro "Data inválida"

