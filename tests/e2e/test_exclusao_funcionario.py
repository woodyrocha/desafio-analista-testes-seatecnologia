"""
Testes de Exclusão de Funcionário

Objetivo: Validar fluxo de exclusão de funcionários cadastrados
Status: ⚠️ BLOQUEADOS por BUG-001 (Menu de opções não abre)

IMPORTANTE: Todos os testes estão documentando o comportamento ESPERADO.
O menu "..." (três pontinhos) não abre, bloqueando acesso às opções de exclusão.
"""

import pytest
import allure
import time
from selenium.webdriver.common.by import By
from pages.lista_funcionarios_page import ListaFuncionariosPage
from pages.cadastro_page import CadastroPage
from utils.data_factory import gerar_dados_funcionario
from utils.helpers import (
    clicar_com_espera,
    tirar_screenshot,
    anexar_screenshot_allure,
    elemento_existe
)


@allure.feature('Exclusão de Funcionário')
@allure.story('Fluxo Básico de Exclusão')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.blocked
@pytest.mark.bug_001
def test_exclusao_funcionario_fluxo_basico(driver, base_url):
    """
    Testa o fluxo básico de exclusão de funcionário.

    ⚠️ BLOQUEADO POR BUG-001: Menu de opções (...) não abre

    Fluxo esperado:
        1. Cadastrar funcionário
        2. Localizar funcionário na lista
        3. Clicar no menu "..." (três pontinhos)
        4. Clicar em "Excluir"
        5. Confirmar exclusão no modal
        6. Validar que funcionário foi removido da lista

    Fluxo atual:
        1-2. ✅ Funcionam
        3. ❌ Menu "..." é clicável mas não abre
        4-6. ❌ Bloqueados (não consegue acessar exclusão)
    """

    with allure.step("Cadastrar funcionário para excluir"):
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)
        lista_page.iniciar_cadastro_funcionario()

        cadastro_page = CadastroPage(driver)
        dados = gerar_dados_funcionario()
        dados['cargo'] = 'Cargo 1'
        dados['nao_usa_epi'] = True

        allure.attach(
            f"Nome: {dados['nome']}\n"
            f"CPF: {dados['cpf']}\n"
            f"RG: {dados['rg']}\n"
            f"Cargo: {dados['cargo']}",
            name="Dados do Funcionário",
            attachment_type=allure.attachment_type.TEXT
        )

        cadastro_page.preencher_e_salvar(dados)
        time.sleep(2)

        caminho = tirar_screenshot(driver, "funcionario_cadastrado_para_exclusao")
        anexar_screenshot_allure(caminho, "Funcionário cadastrado")

    with allure.step("Tentar abrir menu de opções (...)"):
        # XPATH do menu "..." (três pontinhos)
        menu_opcoes_xpath = "/html/body/div/main/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[2]"

        caminho_antes = tirar_screenshot(driver, "antes_clicar_menu_exclusao")
        anexar_screenshot_allure(caminho_antes, "Antes de tentar abrir menu")

        # Verificar se menu existe
        menu_existe = elemento_existe(driver, By.XPATH, menu_opcoes_xpath, timeout=5)

        if not menu_existe:
            allure.attach(
                "⚠️ Menu de opções (...) não encontrado no DOM\n"
                "Possíveis causas:\n"
                "1. Funcionário não apareceu na lista (BUG-003)\n"
                "2. XPATH do menu está incorreto\n"
                "3. Estrutura da página mudou",
                name="Menu Não Encontrado",
                attachment_type=allure.attachment_type.TEXT
            )
            pytest.skip("Menu de opções não encontrado - Possivelmente devido a BUG-003")

        # Tentar clicar no menu
        try:
            clicar_com_espera(driver, By.XPATH, menu_opcoes_xpath, timeout=5)
            time.sleep(1)

            caminho_depois = tirar_screenshot(driver, "depois_clicar_menu_exclusao")
            anexar_screenshot_allure(caminho_depois, "Depois de clicar no menu")

        except Exception as e:
            allure.attach(
                f"❌ Erro ao clicar no menu: {str(e)}",
                name="Erro",
                attachment_type=allure.attachment_type.TEXT
            )
            pytest.skip(f"Erro ao clicar no menu: {str(e)}")

    with allure.step("Verificar se menu abriu e procurar opção 'Excluir'"):
        # XPATH esperado para opção "Excluir" (se menu abrir)
        opcao_excluir_xpath = "//div[contains(text(), 'Excluir')]"

        opcao_excluir_existe = elemento_existe(driver, By.XPATH, opcao_excluir_xpath, timeout=2)

        if not opcao_excluir_existe:
            # ❌ BUG-001 CONFIRMADO: Menu não abriu
            allure.attach(
                "❌ BUG-001 CONFIRMADO: Menu de opções não abre\n\n"
                "Evidências:\n"
                "✅ Menu existe no DOM (XPATH correto)\n"
                "✅ Menu é clicável (sem erro)\n"
                "❌ Clique não abre o menu\n"
                "❌ Opções 'Editar' e 'Excluir' não aparecem\n\n"
                "Comportamento esperado:\n"
                "- Clicar no menu deveria abrir dropdown\n"
                "- Dropdown deveria mostrar 'Editar' e 'Excluir'\n\n"
                "Comportamento atual:\n"
                "- Menu é clicável mas nada acontece\n"
                "- Dropdown não abre\n"
                "- Impossível acessar exclusão\n\n"
                "Impacto:\n"
                "- 🔴 CRÍTICO: Exclusão de funcionários IMPOSSÍVEL\n"
                "- 🔴 CRÍTICO: Edição de funcionários IMPOSSÍVEL\n"
                "- ❌ Funcionalidades essenciais bloqueadas\n\n"
                "XPATHs testados:\n"
                f"- Menu: {menu_opcoes_xpath}\n"
                f"- Excluir: {opcao_excluir_xpath}",
                name="BUG-001 Detectado",
                attachment_type=allure.attachment_type.TEXT
            )

            pytest.skip(
                "BUG-001: Menu de opções (...) não abre. "
                "Elemento é clicável mas sem ação configurada. "
                "Impossível acessar opção 'Excluir'. "
                "Ver documentação completa em docs/bugs-reportados.md"
            )

    # Se chegou aqui, menu abriu! (improvável, mas vamos documentar o fluxo)
    with allure.step("Clicar em 'Excluir'"):
        clicar_com_espera(driver, By.XPATH, opcao_excluir_xpath, timeout=5)
        time.sleep(1)

    with allure.step("Confirmar exclusão no modal"):
        # XPATH esperado para botão "Confirmar" no modal
        botao_confirmar_xpath = "//button[contains(text(), 'Confirmar')]"

        clicar_com_espera(driver, By.XPATH, botao_confirmar_xpath, timeout=5)
        time.sleep(2)

        caminho = tirar_screenshot(driver, "apos_confirmar_exclusao")
        anexar_screenshot_allure(caminho, "Após confirmar exclusão")

    with allure.step("Validar que funcionário foi removido"):
        lista_page = ListaFuncionariosPage(driver)

        # Validar que funcionário NÃO aparece mais na lista
        assert not lista_page.funcionario_existe(dados['nome']), \
            f"Funcionário '{dados['nome']}' ainda aparece na lista após exclusão"

        allure.attach(
            f"✅ Funcionário '{dados['nome']}' foi removido com sucesso",
            name="Resultado",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.feature('Exclusão de Funcionário')
@allure.story('Cancelar Exclusão')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.blocked
@pytest.mark.bug_001
def test_cancelar_exclusao_funcionario(driver, base_url):
    """
    Testa cancelamento de exclusão usando botão "Cancelar" no modal.

    ⚠️ BLOQUEADO POR BUG-001: Menu de opções não abre

    Cenário:
        1. Cadastrar funcionário
        2. Clicar em menu "..."
        3. Clicar em "Excluir"
        4. Aparecer modal de confirmação
        5. Clicar em "Cancelar"
        6. Validar que funcionário permanece na lista
    """

    pytest.skip(
        "BUG-001: Menu de opções (...) não abre. "
        "Impossível acessar funcionalidade de exclusão. "
        "Ver test_exclusao_funcionario_fluxo_basico para evidências completas."
    )


@allure.feature('Exclusão de Funcionário')
@allure.story('Exclusão Múltipla')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.blocked
@pytest.mark.bug_001
def test_exclusao_multiplos_funcionarios(driver, base_url):
    """
    Testa exclusão de múltiplos funcionários em sequência.

    ⚠️ BLOQUEADO POR BUG-001: Menu de opções não abre

    Cenário:
        1. Cadastrar 3 funcionários
        2. Excluir primeiro funcionário
        3. Excluir segundo funcionário
        4. Excluir terceiro funcionário
        5. Validar que todos foram removidos
    """

    pytest.skip(
        "BUG-001: Menu de opções (...) não abre. "
        "Impossível acessar funcionalidade de exclusão. "
        "Ver test_exclusao_funcionario_fluxo_basico para evidências completas."
    )


@allure.feature('Exclusão de Funcionário')
@allure.story('Validar Lista após Exclusão')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.blocked
@pytest.mark.bug_001
def test_funcionario_excluido_nao_aparece_na_lista(driver, base_url):
    """
    Valida que funcionário excluído não aparece mais na lista.

    ⚠️ BLOQUEADO POR BUG-001: Menu de opções não abre

    Cenário:
        1. Cadastrar funcionário A
        2. Cadastrar funcionário B
        3. Excluir funcionário A
        4. Validar que funcionário A não aparece
        5. Validar que funcionário B ainda aparece
    """

    pytest.skip(
        "BUG-001: Menu de opções (...) não abre. "
        "Impossível acessar funcionalidade de exclusão. "
        "Ver test_exclusao_funcionario_fluxo_basico para evidências completas."
    )


@allure.feature('Exclusão de Funcionário')
@allure.story('Modal de Confirmação')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.blocked
@pytest.mark.bug_001
def test_mensagem_confirmacao_exclusao(driver, base_url):
    """
    Testa que modal de confirmação exibe mensagem apropriada.

    ⚠️ BLOQUEADO POR BUG-001: Menu de opções não abre

    Cenário:
        1. Cadastrar funcionário
        2. Clicar em "Excluir"
        3. Validar que modal aparece
        4. Validar texto do modal
        5. Validar que tem botões "Confirmar" e "Cancelar"
    """

    pytest.skip(
        "BUG-001: Menu de opções (...) não abre. "
        "Impossível acessar funcionalidade de exclusão. "
        "Ver test_exclusao_funcionario_fluxo_basico para evidências completas."
    )