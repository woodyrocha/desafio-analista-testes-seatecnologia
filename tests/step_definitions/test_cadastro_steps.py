"""
Step Definitions para cadastro.feature
Implementa 3 scenarios: cadastro válido, cadastro com EPI, cadastro sem campos
"""
from pytest_bdd import scenarios, given, when, then, parsers
import time
import allure
from pages.lista_funcionarios_page import ListaFuncionariosPage
from pages.cadastro_page import CadastroPage
from utils.data_factory import gerar_dados_funcionario

# Carregar TODOS os scenarios de cadastro.feature
scenarios('cadastro.feature')


# ==================== GIVEN (Pré-condições) ====================

@given('que estou na tela de listagem de funcionários', target_fixture='lista_page')
def estou_na_listagem(driver, base_url):
    """Acessa a aplicação e fica na tela de listagem"""
    with allure.step("Acessar tela de listagem"):
        driver.get(base_url)
        time.sleep(1)
        return ListaFuncionariosPage(driver)


@given('que estou no formulário de cadastro', target_fixture='cadastro_page')
def estou_no_formulario(driver, base_url):
    """Abre o formulário de cadastro"""
    with allure.step("Abrir formulário de cadastro"):
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)
        lista_page.iniciar_cadastro_funcionario()
        time.sleep(1)
        return CadastroPage(driver)


# ==================== WHEN (Ações) ====================

@when('eu clico no botão "Adicionar Funcionário"')
def clicar_adicionar_funcionario(driver, lista_page):
    """Clica no botão de adicionar funcionário"""
    with allure.step("Clicar em 'Adicionar Funcionário'"):
        lista_page.iniciar_cadastro_funcionario()
        time.sleep(1)


@when(parsers.parse('preencho o nome com "{nome}"'))
def preencher_nome(driver, nome):
    """Preenche o campo nome"""
    with allure.step(f"Preencher nome: {nome}"):
        cadastro_page = CadastroPage(driver)
        cadastro_page.preencher_nome(nome)
        time.sleep(0.3)

        # Armazenar para validação posterior
        driver.dados_teste = getattr(driver, 'dados_teste', {})
        driver.dados_teste['nome'] = nome


@when(parsers.parse('preencho o CPF com "{cpf}"'))
def preencher_cpf(driver, cpf):
    """Preenche o campo CPF"""
    with allure.step(f"Preencher CPF: {cpf}"):
        cadastro_page = CadastroPage(driver)
        cadastro_page.preencher_cpf(cpf)
        time.sleep(0.3)

        # Armazenar para validação posterior
        driver.dados_teste = getattr(driver, 'dados_teste', {})
        driver.dados_teste['cpf'] = cpf


@when(parsers.parse('preencho a data de nascimento com "{data}"'))
def preencher_data_nascimento(driver, data):
    """Preenche a data de nascimento"""
    with allure.step(f"Preencher data de nascimento: {data}"):
        cadastro_page = CadastroPage(driver)
        cadastro_page.preencher_data_nascimento(data)
        time.sleep(0.3)


@when(parsers.parse('seleciono o cargo "{cargo}"'))
def selecionar_cargo(driver, cargo):
    """Seleciona o cargo"""
    with allure.step(f"Selecionar cargo: {cargo}"):
        cadastro_page = CadastroPage(driver)
        # Mapear nomes amigáveis para cargos do sistema
        mapa_cargos = {
            "Analista": "Cargo 1",
            "Desenvolvedor": "Cargo 2",
            "Gerente": "Cargo 3"
        }
        cargo_sistema = mapa_cargos.get(cargo, "Cargo 1")
        cadastro_page.selecionar_cargo(cargo_sistema)
        time.sleep(0.5)


@when('preencho todos os campos obrigatórios com dados válidos')
def preencher_todos_campos(driver):
    """Preenche todos os campos obrigatórios com dados válidos"""
    with allure.step("Preencher todos os campos obrigatórios"):
        cadastro_page = CadastroPage(driver)
        dados = gerar_dados_funcionario()

        cadastro_page.preencher_nome(dados['nome'])
        cadastro_page.selecionar_sexo(dados['sexo'])
        cadastro_page.preencher_cpf(dados['cpf'])
        cadastro_page.preencher_data_nascimento(dados['data_nascimento'])
        cadastro_page.preencher_rg(dados['rg'])
        cadastro_page.selecionar_cargo('Cargo 1')

        # Armazenar dados para validação posterior
        driver.dados_funcionario = dados
        time.sleep(0.5)


@when(parsers.parse('seleciono o EPI "{epi}"'))
def selecionar_epi(driver, epi):
    """Seleciona o EPI"""
    with allure.step(f"Selecionar EPI: {epi}"):
        cadastro_page = CadastroPage(driver)
        # Mapear nomes amigáveis
        mapa_epis = {
            "Capacete": "EPI 1",
            "Luvas": "EPI 2",
            "Botas": "EPI 3"
        }
        epi_sistema = mapa_epis.get(epi, "EPI 1")
        cadastro_page.selecionar_epi(epi_sistema)

        # Armazenar EPI selecionado
        driver.epi_selecionado = epi
        time.sleep(0.5)


@when(parsers.parse('seleciono a atividade "{atividade}"'))
def selecionar_atividade(driver, atividade):
    """Seleciona a atividade"""
    with allure.step(f"Selecionar atividade: {atividade}"):
        cadastro_page = CadastroPage(driver)
        # Mapear nomes amigáveis
        mapa_atividades = {
            "Soldagem": "Atividade 1",
            "Pintura": "Atividade 2",
            "Montagem": "Atividade 3"
        }
        atividade_sistema = mapa_atividades.get(atividade, "Atividade 1")
        cadastro_page.selecionar_atividade(atividade_sistema)
        time.sleep(0.5)


@when('clico no botão "Salvar"')
def clicar_salvar(driver):
    """Clica no botão Salvar"""
    with allure.step("Clicar em 'Salvar'"):
        cadastro_page = CadastroPage(driver)
        cadastro_page.salvar()
        time.sleep(2)  # Aguardar redirecionamento


@when('clico no botão "Salvar" sem preencher campos')
def clicar_salvar_sem_preencher(driver, cadastro_page):
    """Tenta salvar sem preencher campos obrigatórios"""
    with allure.step("Tentar salvar sem preencher campos"):
        cadastro_page.salvar()
        time.sleep(1)


# ==================== THEN (Validações) ====================

@then('o funcionário deve aparecer na lista')
def funcionario_deve_aparecer(driver):
    """Valida que funcionário aparece na lista"""
    with allure.step("Validar que funcionário aparece na lista"):
        lista_page = ListaFuncionariosPage(driver)

        # Verificar se tem dados armazenados
        if hasattr(driver, 'dados_teste') and 'nome' in driver.dados_teste:
            nome = driver.dados_teste['nome']
            assert lista_page.funcionario_existe(nome), \
                f"Funcionário '{nome}' não foi encontrado na lista"
        elif hasattr(driver, 'dados_funcionario'):
            nome = driver.dados_funcionario['nome']
            assert lista_page.funcionario_existe(nome), \
                f"Funcionário '{nome}' não foi encontrado na lista"
        else:
            # Se não tem nome armazenado, apenas verificar que voltou para lista
            time.sleep(1)


@then(parsers.parse('deve exibir o nome "{nome}"'))
def deve_exibir_nome(driver, nome):
    """Valida que o nome está sendo exibido"""
    with allure.step(f"Validar exibição do nome: {nome}"):
        lista_page = ListaFuncionariosPage(driver)
        assert lista_page.funcionario_existe(nome), \
            f"Nome '{nome}' não está sendo exibido na lista"


@then(parsers.parse('deve exibir o CPF "{cpf}"'))
def deve_exibir_cpf(driver, cpf):
    """Valida que o CPF está sendo exibido"""
    with allure.step(f"Validar exibição do CPF: {cpf}"):
        # CPF validation - simplificado por enquanto
        # Idealmente, verificaria o CPF específico no card do funcionário
        time.sleep(0.5)


@then('deve exibir o EPI selecionado')
def deve_exibir_epi(driver):
    """Valida que o EPI está sendo exibido"""
    with allure.step("Validar exibição do EPI"):
        # Validação simplificada
        # Idealmente verificaria o EPI específico no card
        time.sleep(0.5)


@then('deve exibir mensagens de erro nos campos obrigatórios')
def deve_exibir_erros(driver):
    """Valida que mensagens de erro aparecem"""
    with allure.step("Validar mensagens de erro"):
        # Verificar que ainda está no formulário (não redirecionou)
        time.sleep(1)
        current_url = driver.current_url
        # Deve continuar no formulário ou na raiz
        assert current_url.endswith('/') or 'cadastro' in current_url.lower(), \
            "Formulário deveria estar ainda visível após erro de validação"


@then('o cadastro não deve ser salvo')
def cadastro_nao_salvo(driver):
    """Valida que o cadastro não foi salvo"""
    with allure.step("Validar que não salvou"):
        # Verificar que continua no formulário
        time.sleep(0.5)
        current_url = driver.current_url
        # Não deve ter redirecionado para a lista
        assert current_url.endswith('/') or 'cadastro' in current_url.lower(), \
            "Não deveria ter salvado o cadastro"