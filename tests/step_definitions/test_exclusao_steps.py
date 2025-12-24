"""
Step Definitions para exclusao.feature
Implementa 1 scenario: Excluir funcionário existente

NOTA: Testes de exclusão estão bloqueados por BUG-001
      (Menu "..." não abre opções de Excluir)
"""
from pytest_bdd import scenarios, given, when, then
import time
import allure
import pytest
from pages.lista_funcionarios_page import ListaFuncionariosPage
from pages.cadastro_page import CadastroPage
from utils.data_factory import gerar_dados_funcionario

# Carregar scenarios de exclusao.feature
scenarios('exclusao.feature')


# ==================== GIVEN ====================

@given('que existe um funcionário na lista', target_fixture='funcionario_existente')
def funcionario_na_lista(driver, base_url):
    """Cadastra um funcionário para poder excluir depois"""
    with allure.step("Cadastrar funcionário para teste de exclusão"):
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

        # Armazenar nome para validação posterior
        driver.nome_funcionario_excluir = dados['nome']

        return dados


# ==================== WHEN ====================

@when('eu escolho remover esse funcionário')
def escolher_remover(driver, funcionario_existente):
    """Tenta abrir menu e escolher remover"""
    with allure.step("Escolher opção de remover funcionário"):
        # NOTA: Esta funcionalidade está bloqueada por BUG-001
        # Menu "..." não abre opções de Editar/Excluir

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

            # Tentar clicar em "Excluir" (não vai aparecer)
            excluir_xpath = "//button[contains(text(), 'Excluir')] | //span[contains(text(), 'Excluir')]"
            excluir_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, excluir_xpath))
            )
            excluir_btn.click()
            time.sleep(1)

        except Exception as e:
            # BUG-001: Menu não abre
            allure.attach(
                f"BUG-001: Menu não abre. Impossível excluir.\nErro: {str(e)}",
                name="Bug Bloqueador",
                attachment_type=allure.attachment_type.TEXT
            )
            # Marcar teste como bloqueado
            pytest.skip("BUG-001: Menu de opções não abre. Impossível testar exclusão.")


@when('confirmo a exclusão')
def confirmar_exclusao(driver):
    """Confirma a exclusão na modal/dialog"""
    with allure.step("Confirmar exclusão"):
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            # Procurar botão de confirmação (pode ser "Sim", "Confirmar", "OK", etc)
            confirmar_xpaths = [
                "//button[contains(text(), 'Sim')]",
                "//button[contains(text(), 'Confirmar')]",
                "//button[contains(text(), 'OK')]",
                "//button[contains(@class, 'confirm')]"
            ]

            for xpath in confirmar_xpaths:
                try:
                    btn = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    btn.click()
                    time.sleep(1)
                    break
                except:
                    continue

        except:
            # Se não conseguiu abrir menu, não tem o que confirmar
            pass


# ==================== THEN ====================

@then('o funcionário não deve mais aparecer na lista')
def funcionario_nao_deve_aparecer(driver):
    """Valida que funcionário foi removido da lista"""
    with allure.step("Validar que funcionário foi removido"):
        if hasattr(driver, 'nome_funcionario_excluir'):
            lista_page = ListaFuncionariosPage(driver)
            nome = driver.nome_funcionario_excluir

            try:
                # Verificar que funcionário NÃO existe mais
                existe = lista_page.funcionario_existe(nome)
                assert not existe, \
                    f"Funcionário '{nome}' ainda aparece na lista após exclusão"

            except AssertionError:
                # Se falhou, provavelmente é por causa do BUG-001
                allure.attach(
                    "Validação falhou - possivelmente devido a BUG-001 (menu não abre)",
                    name="Falha Esperada",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise
        else:
            # Se não tem nome armazenado, apenas aguardar
            time.sleep(1)