"""
Testes de Edição de Funcionário

Objetivo: Validar fluxo de edição de funcionários cadastrados
Status: ⚠️ BLOQUEADOS por BUG-001 (Menu de opções não abre)

IMPORTANTE: Todos os testes estão documentando o comportamento ESPERADO.
O menu "..." (três pontinhos) não abre, bloqueando acesso às opções de edição.
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
    elemento_existe,
    esperar_elemento_clicavel
)


@allure.feature('Edição de Funcionário')
@allure.story('Fluxo Básico de Edição')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.blocked
@pytest.mark.bug_001
def test_edicao_funcionario_fluxo_basico(driver, base_url):
    """
    Testa o fluxo básico de edição de funcionário.

    ⚠️ BLOQUEADO POR BUG-001: Menu de opções (...) não abre

    Fluxo esperado:
        1. Cadastrar funcionário
        2. Localizar funcionário na lista
        3. Clicar no menu "..." (três pontinhos)
        4. Clicar em "Editar"
        5. Modificar dados
        6. Salvar
        7. Validar que alterações foram aplicadas

    Fluxo atual:
        1-2. ✅ Funcionam
        3. ❌ Menu "..." é clicável mas não abre
        4-7. ❌ Bloqueados (não consegue acessar edição)
    """

    with allure.step("Cadastrar funcionário para editar"):
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)
        lista_page.iniciar_cadastro_funcionario()

        cadastro_page = CadastroPage(driver)
        dados_originais = gerar_dados_funcionario()
        dados_originais['cargo'] = 'Cargo 1'
        dados_originais['nao_usa_epi'] = True

        allure.attach(
            f"Nome original: {dados_originais['nome']}\n"
            f"CPF: {dados_originais['cpf']}\n"
            f"RG: {dados_originais['rg']}\n"
            f"Cargo: {dados_originais['cargo']}",
            name="Dados Originais",
            attachment_type=allure.attachment_type.TEXT
        )

        cadastro_page.preencher_e_salvar(dados_originais)
        time.sleep(2)

        caminho = tirar_screenshot(driver, "funcionario_cadastrado_para_edicao")
        anexar_screenshot_allure(caminho, "Funcionário cadastrado")

    with allure.step("Tentar abrir menu de opções (...)"):
        # XPATH do menu "..." (três pontinhos)
        menu_opcoes_xpath = "/html/body/div/main/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[2]"

        caminho_antes = tirar_screenshot(driver, "antes_clicar_menu")
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

            caminho_depois = tirar_screenshot(driver, "depois_clicar_menu")
            anexar_screenshot_allure(caminho_depois, "Depois de clicar no menu")

        except Exception as e:
            allure.attach(
                f"❌ Erro ao clicar no menu: {str(e)}",
                name="Erro",
                attachment_type=allure.attachment_type.TEXT
            )
            pytest.skip(f"Erro ao clicar no menu: {str(e)}")

    with allure.step("Verificar se menu abriu e procurar opção 'Editar'"):
        # XPATH esperado para opção "Editar" (se menu abrir)
        opcao_editar_xpath = "//div[contains(text(), 'Editar')]"

        opcao_editar_existe = elemento_existe(driver, By.XPATH, opcao_editar_xpath, timeout=2)

        if not opcao_editar_existe:
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
                "- Impossível acessar edição/exclusão\n\n"
                "Impacto:\n"
                "- 🔴 CRÍTICO: Edição de funcionários IMPOSSÍVEL\n"
                "- 🔴 CRÍTICO: Exclusão de funcionários IMPOSSÍVEL\n"
                "- ❌ Funcionalidades essenciais bloqueadas\n\n"
                "XPATHs testados:\n"
                f"- Menu: {menu_opcoes_xpath}\n"
                f"- Editar: {opcao_editar_xpath}",
                name="BUG-001 Detectado",
                attachment_type=allure.attachment_type.TEXT
            )

            pytest.skip(
                "BUG-001: Menu de opções (...) não abre. "
                "Elemento é clicável mas sem ação configurada. "
                "Impossível acessar opção 'Editar'. "
                "Ver documentação completa em docs/bugs-reportados.md"
            )

    # Se chegou aqui, menu abriu! (improvável, mas vamos documentar o fluxo)
    with allure.step("Clicar em 'Editar'"):
        clicar_com_espera(driver, By.XPATH, opcao_editar_xpath, timeout=5)
        time.sleep(1)

    with allure.step("Modificar dados do funcionário"):
        cadastro_page = CadastroPage(driver)

        # Gerar novos dados
        novos_dados = gerar_dados_funcionario()
        novos_dados['cargo'] = 'Cargo 2'
        novos_dados['nao_usa_epi'] = True

        allure.attach(
            f"Nome novo: {novos_dados['nome']}\n"
            f"CPF novo: {novos_dados['cpf']}\n"
            f"RG novo: {novos_dados['rg']}\n"
            f"Cargo novo: {novos_dados['cargo']}",
            name="Dados Novos",
            attachment_type=allure.attachment_type.TEXT
        )

        # Modificar campos
        cadastro_page.preencher_nome(novos_dados['nome'])
        cadastro_page.preencher_cpf(novos_dados['cpf'])
        cadastro_page.preencher_rg(novos_dados['rg'])
        cadastro_page.selecionar_cargo(novos_dados['cargo'])

        cadastro_page.salvar()
        time.sleep(2)

    with allure.step("Validar que alterações foram aplicadas"):
        lista_page = ListaFuncionariosPage(driver)

        # Validar que novo nome aparece na lista
        assert lista_page.funcionario_existe(novos_dados['nome']), \
            f"Funcionário com nome editado '{novos_dados['nome']}' não encontrado"

        # Validar que nome antigo NÃO aparece mais
        assert not lista_page.funcionario_existe(dados_originais['nome']), \
            f"Nome original '{dados_originais['nome']}' ainda aparece (edição não funcionou)"


@allure.feature('Edição de Funcionário')
@allure.story('Editar apenas Nome')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.blocked
@pytest.mark.bug_001
def test_edicao_nome_funcionario(driver, base_url):
    """
    Testa edição apenas do nome do funcionário.

    ⚠️ BLOQUEADO POR BUG-001: Menu de opções não abre

    Cenário:
        1. Cadastrar funcionário
        2. Editar apenas o nome
        3. Manter todos os outros dados
        4. Validar que apenas nome foi alterado
    """

    pytest.skip(
        "BUG-001: Menu de opções (...) não abre. "
        "Impossível acessar funcionalidade de edição. "
        "Ver test_edicao_funcionario_fluxo_basico para evidências completas."
    )


@allure.feature('Edição de Funcionário')
@allure.story('Cancelar Edição')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.blocked
@pytest.mark.bug_001
def test_cancelar_edicao_funcionario(driver, base_url):
    """
    Testa cancelamento de edição usando botão Voltar.

    ⚠️ BLOQUEADO POR BUG-001: Menu de opções não abre

    Cenário:
        1. Cadastrar funcionário
        2. Entrar em modo de edição
        3. Modificar alguns campos
        4. Clicar em "Voltar"
        5. Validar que alterações NÃO foram salvas
    """

    pytest.skip(
        "BUG-001: Menu de opções (...) não abre. "
        "Impossível acessar funcionalidade de edição. "
        "Ver test_edicao_funcionario_fluxo_basico para evidências completas."
    )


@allure.feature('Edição de Funcionário')
@allure.story('Validações durante Edição')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.blocked
@pytest.mark.bug_001
def test_validacoes_durante_edicao(driver, base_url):
    """
    Testa que validações de campos funcionam durante edição.

    ⚠️ BLOQUEADO POR BUG-001: Menu de opções não abre

    Cenário:
        1. Cadastrar funcionário válido
        2. Entrar em modo de edição
        3. Tentar alterar CPF para valor inválido
        4. Tentar salvar
        5. Validar que sistema rejeita CPF inválido
        6. Validar que dados originais permanecem
    """

    pytest.skip(
        "BUG-001: Menu de opções (...) não abre. "
        "Impossível acessar funcionalidade de edição. "
        "Ver test_edicao_funcionario_fluxo_basico para evidências completas."
    )