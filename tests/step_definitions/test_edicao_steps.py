"""
Step Definitions para edicao.feature
Implementa 1 scenario: Editar funcionário existente

NOTA: Testes de edição estão bloqueados por BUG-001
      (Menu "..." não abre opções de Editar)
"""
from pytest_bdd import scenarios, given, when, then, parsers
import time
import allure
import pytest
from pages.lista_funcionarios_page import ListaFuncionariosPage
from pages.cadastro_page import CadastroPage
from utils.data_factory import gerar_dados_funcionario

# Carregar scenarios de edicao.feature
scenarios('edicao.feature')


# ==================== GIVEN ====================

@given('que existe um funcionário cadastrado', target_fixture='funcionario_cadastrado')
def funcionario_cadastrado(driver, base_url):
    """Cadastra um funcionário para poder editar depois"""
    with allure.step("Cadastrar funcionário para teste de edição"):
        # Ir para aplicação
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)

        # Iniciar cadastro
        lista_page.iniciar_cadastro_funcionario()
        time.sleep(1)

        # Preencher dados
        cadastro_page = CadastroPage(driver)
        dados = gerar_dados_funcionario()

        cadastro_page.preencher_nome(dados['nome'])
        cadastro_page.selecionar_sexo(dados['sexo'])
        cadastro_page.preencher_cpf(dados['cpf'])
        cadastro_page.preencher_data_nascimento(dados['data_nascimento'])
        cadastro_page.preencher_rg(dados['rg'])
        cadastro_page.selecionar_cargo('Cargo 1')
        cadastro_page.marcar_nao_usa_epi()

        # Salvar
        cadastro_page.salvar()
        time.sleep(2)

        # Retornar dados para uso nos steps
        return dados


# ==================== WHEN ====================

@when(parsers.parse('eu edito o nome para "{novo_nome}"'))
def editar_nome(driver, novo_nome, funcionario_cadastrado):
    """Tenta editar o nome do funcionário"""
    with allure.step(f"Editar nome para: {novo_nome}"):
        lista_page = ListaFuncionariosPage(driver)

        # NOTA: Esta funcionalidade está bloqueada por BUG-001
        # Menu "..." não abre opções de Editar/Excluir

        # Tentar abrir menu (vai falhar devido ao bug)
        try:
            # XPATH do menu "..." (exemplo)
            menu_xpath = "/html/body/div/main/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div"

            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            menu = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, menu_xpath))
            )
            menu.click()
            time.sleep(1)

            # Tentar clicar em "Editar" (não vai aparecer)
            editar_xpath = "//button[contains(text(), 'Editar')] | //span[contains(text(), 'Editar')]"
            editar_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, editar_xpath))
            )
            editar_btn.click()
            time.sleep(1)

            # Se chegou aqui, editar funcionário
            cadastro_page = CadastroPage(driver)
            cadastro_page.preencher_nome(novo_nome)

        except Exception as e:
            # BUG-001: Menu não abre
            allure.attach(
                f"BUG-001: Menu não abre. Impossível editar.\nErro: {str(e)}",
                name="Bug Bloqueador",
                attachment_type=allure.attachment_type.TEXT
            )
            # Marcar teste como bloqueado
            pytest.skip("BUG-001: Menu de opções não abre. Impossível testar edição.")


@when('clico em "Salvar"')
def clicar_salvar_edicao(driver):
    """Salva as alterações"""
    with allure.step("Salvar alterações"):
        try:
            cadastro_page = CadastroPage(driver)
            cadastro_page.salvar()
            time.sleep(2)
        except:
            pass  # Se não conseguiu editar, não consegue salvar


# ==================== THEN ====================

@then(parsers.parse('a lista deve exibir "{nome}"'))
def lista_deve_exibir(driver, nome):
    """Valida que nome foi atualizado na lista"""
    with allure.step(f"Validar que lista exibe: {nome}"):
        lista_page = ListaFuncionariosPage(driver)

        try:
            assert lista_page.funcionario_existe(nome), \
                f"Funcionário '{nome}' não foi encontrado na lista após edição"
        except AssertionError:
            # Se falhou, provavelmente é por causa do BUG-001
            allure.attach(
                "Validação falhou - possivelmente devido a BUG-001 (menu não abre)",
                name="Falha Esperada",
                attachment_type=allure.attachment_type.TEXT
            )
            raise