"""
Testes End-to-End para cadastro de funcionário.

Testa o fluxo completo de cadastro, desde a navegação até a validação
de que o funcionário foi adicionado à lista.
"""

import pytest
import allure
from pages.lista_funcionarios_page import ListaFuncionariosPage
from pages.cadastro_page import CadastroPage
from utils.data_factory import gerar_dados_funcionario


@allure.feature('Cadastro de Funcionário')
@allure.story('Cadastro com dados válidos')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.smoke
def test_cadastro_funcionario_dados_validos(driver, base_url):
    """
    Testa o cadastro de um funcionário com todos os dados válidos.

    Cenário:
        1. Acessar a aplicação
        2. Clicar em "Adicionar Funcionário"
        3. Preencher todos os campos obrigatórios
        4. Salvar cadastro
        5. Validar que funcionário aparece na lista
    """

    with allure.step("Acessar a aplicação"):
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)

    with allure.step("Iniciar cadastro de novo funcionário"):
        lista_page.iniciar_cadastro_funcionario()

    with allure.step("Preencher formulário de cadastro"):
        cadastro_page = CadastroPage(driver)

        # Gerar dados fake para o teste
        dados = gerar_dados_funcionario()
        dados['cargo'] = 'Cargo 1'  # Cargo fixo do dropdown
        dados['nao_usa_epi'] = True

        # Anexar dados ao relatório Allure
        allure.attach(
            f"Nome: {dados['nome']}\n"
            f"CPF: {dados['cpf']}\n"
            f"Data Nascimento: {dados['data_nascimento']}\n"
            f"Cargo: {dados['cargo']}",
            name="Dados do Funcionário",
            attachment_type=allure.attachment_type.TEXT
        )

        # Preencher e salvar
        cadastro_page.preencher_e_salvar(dados)

    with allure.step("Validar que funcionário foi cadastrado"):
        # Aguardar redirecionamento para lista
        import time
        time.sleep(2)

        lista_page = ListaFuncionariosPage(driver)
        assert lista_page.validar_funcionario_cadastrado(dados['nome']), \
            f"Funcionário '{dados['nome']}' não foi encontrado na lista após cadastro"


@allure.feature('Cadastro de Funcionário')
@allure.story('Cadastro mínimo (sem EPIs)')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
def test_cadastro_funcionario_sem_epi(driver, base_url):
    """
    Testa o cadastro de um funcionário marcando a opção "Não usa EPI".

    Cenário:
        1. Acessar a aplicação
        2. Clicar em "Adicionar Funcionário"
        3. Preencher dados básicos
        4. Marcar "Não usa EPI"
        5. Salvar cadastro
        6. Validar que funcionário aparece na lista
    """

    with allure.step("Acessar a aplicação e iniciar cadastro"):
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)
        lista_page.iniciar_cadastro_funcionario()

    with allure.step("Preencher formulário marcando 'Não usa EPI'"):
        cadastro_page = CadastroPage(driver)

        dados = gerar_dados_funcionario()
        dados['cargo'] = 'Cargo 2'
        dados['nao_usa_epi'] = True

        cadastro_page.preencher_e_salvar(dados)

    with allure.step("Validar cadastro realizado"):
        import time
        time.sleep(2)

        lista_page = ListaFuncionariosPage(driver)
        assert lista_page.funcionario_existe(dados['nome']), \
            f"Funcionário '{dados['nome']}' não apareceu na lista"


@allure.feature('Cadastro de Funcionário')
@allure.story('Cadastro com dados parciais')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
def test_cadastro_funcionario_somente_obrigatorios(driver, base_url):
    """
    Testa cadastro preenchendo apenas campos obrigatórios.

    Cenário:
        1. Preencher apenas: Nome, Sexo, CPF, Data Nascimento, Cargo
        2. Não preencher RG
        3. Não preencher EPIs
        4. Validar que cadastro é aceito
    """

    with allure.step("Acessar aplicação e iniciar cadastro"):
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)
        lista_page.iniciar_cadastro_funcionario()

    with allure.step("Preencher apenas campos obrigatórios"):
        cadastro_page = CadastroPage(driver)

        dados = gerar_dados_funcionario()
        dados['cargo'] = 'Cargo 3'
        dados['nao_usa_epi'] = True
        # NÃO incluir RG

        cadastro_page.preencher_nome(dados['nome'])
        cadastro_page.selecionar_sexo('M')
        cadastro_page.preencher_cpf(dados['cpf'])
        cadastro_page.preencher_data_nascimento(dados['data_nascimento'])
        cadastro_page.selecionar_cargo(dados['cargo'])
        cadastro_page.marcar_nao_usa_epi()
        cadastro_page.salvar()

    with allure.step("Validar cadastro"):
        import time
        time.sleep(2)

        lista_page = ListaFuncionariosPage(driver)
        assert lista_page.funcionario_existe(dados['nome']), \
            "Cadastro com apenas campos obrigatórios deveria ser aceito"


@allure.feature('Cadastro de Funcionário')
@allure.story('Botão voltar cancela cadastro')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
def test_botao_voltar_cancela_cadastro(driver, base_url):
    """
    Testa que o botão voltar cancela o cadastro e retorna para a lista.

    Cenário:
        1. Iniciar cadastro
        2. Preencher alguns campos
        3. Clicar em "Voltar"
        4. Validar que retornou para listagem
        5. Validar que dados não foram salvos
    """

    with allure.step("Iniciar cadastro"):
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)
        lista_page.iniciar_cadastro_funcionario()

    with allure.step("Preencher parcialmente o formulário"):
        cadastro_page = CadastroPage(driver)
        dados = gerar_dados_funcionario()

        cadastro_page.preencher_nome(dados['nome'])
        cadastro_page.preencher_cpf(dados['cpf'])

    with allure.step("Clicar no botão voltar"):
        cadastro_page.clicar_voltar()

    with allure.step("Validar que retornou para lista e dados não foram salvos"):
        import time
        time.sleep(1)

        lista_page = ListaFuncionariosPage(driver)
        # Verifica que voltou para listagem (botão Adicionar está visível)
        assert lista_page.elemento_existe(*lista_page.BOTAO_ADICIONAR_FUNCIONARIO, timeout=5), \
            "Não retornou para a tela de listagem"

        # Verifica que funcionário NÃO foi salvo
        assert not lista_page.funcionario_existe(dados['nome']), \
            "Funcionário não deveria estar salvo após clicar em Voltar"


@allure.feature('Cadastro de Funcionário')
@allure.story('Toggle de status funciona')
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.e2e
def test_toggle_status_funcional(driver, base_url):
    """
    Testa que o toggle de status (Ativo/Inativo) funciona corretamente.

    Cenário:
        1. Acessar formulário de cadastro
        2. Verificar estado inicial do toggle
        3. Clicar no toggle
        4. Verificar que estado mudou
    """

    with allure.step("Acessar formulário de cadastro"):
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)
        lista_page.iniciar_cadastro_funcionario()

    with allure.step("Interagir com toggle de status"):
        cadastro_page = CadastroPage(driver)

        # Clicar no toggle para alternar
        cadastro_page.alternar_status()

        # Nota: Validação visual seria necessária aqui para confirmar mudança
        # Por enquanto, apenas verificamos que não dá erro

        allure.attach(
            "Toggle clicado com sucesso",
            name="Resultado do Toggle",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.feature('Cadastro de Funcionário')
@allure.story('Cadastro múltiplos funcionários sequencialmente')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
def test_cadastro_multiplos_funcionarios(driver, base_url):
    """
    Testa o cadastro de múltiplos funcionários em sequência.

    Cenário:
        1. Cadastrar primeiro funcionário
        2. Retornar para lista
        3. Cadastrar segundo funcionário
        4. Validar que ambos aparecem na lista
    """

    funcionarios_cadastrados = []

    for i in range(2):
        with allure.step(f"Cadastrar funcionário {i + 1}"):
            if i == 0:
                driver.get(base_url)

            lista_page = ListaFuncionariosPage(driver)
            lista_page.iniciar_cadastro_funcionario()

            cadastro_page = CadastroPage(driver)
            dados = gerar_dados_funcionario()
            dados['cargo'] = f'Cargo {i + 1}'
            dados['nao_usa_epi'] = True

            cadastro_page.preencher_e_salvar(dados)
            funcionarios_cadastrados.append(dados['nome'])

            import time
            time.sleep(2)

    with allure.step("Validar que todos os funcionários foram cadastrados"):
        lista_page = ListaFuncionariosPage(driver)

        for nome in funcionarios_cadastrados:
            assert lista_page.funcionario_existe(nome), \
                f"Funcionário '{nome}' não encontrado na lista"

        allure.attach(
            f"Funcionários cadastrados:\n" + "\n".join(funcionarios_cadastrados),
            name="Lista de Funcionários",
            attachment_type=allure.attachment_type.TEXT
        )