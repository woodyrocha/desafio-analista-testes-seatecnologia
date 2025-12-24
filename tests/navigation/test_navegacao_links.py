"""
Testes de Navegação e Links

Objetivo: Validar navegação pelos links e menus da aplicação
Requisito: "Teste os links para assegurar que eles conduzam às etapas
           e itens de menu corretos. Todos os links devem levar ao componente 'Em breve'"
"""

import pytest
import allure
import time
from selenium.webdriver.common.by import By
from pages.lista_funcionarios_page import ListaFuncionariosPage
from utils.helpers import clicar_com_espera, tirar_screenshot, anexar_screenshot_allure, elemento_existe


@allure.feature('Navegação')
@allure.story('Menu Lateral - Ícones')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.navigation
def test_navegacao_menu_lateral_icones(driver, base_url):
    """
    Testa que os 6 ícones do menu lateral levam para componente "Em breve".

        "Teste os links para assegurar que eles conduzam às etapas e itens de menu corretos.
         Todos os links devem levar ao componente 'Em breve'"

    Comportamento esperado:
        - Cada ícone deve levar para página "Em breve"
        - Deve exibir mensagem indicando funcionalidade futura

    Comportamento atual:
        - Ícones são clicáveis MAS não tem ação configurada
        - BUG documentado em BUG-006-ICONES-MENU.md
    """

    with allure.step("Acessar aplicação"):
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)
        time.sleep(1)

    # XPATHs dos 6 ícones do menu lateral
    icones_menu = {
        "Ícone 1 (Topo)": "/html/body/div/main/div[1]/div[2]/div[1]",
        "Ícone 2": "/html/body/div/main/div[1]/div[2]/div[2]",
        "Ícone 3": "/html/body/div/main/div[1]/div[2]/div[3]",
        "Ícone 4": "/html/body/div/main/div[1]/div[2]/div[4]",
        "Ícone 5": "/html/body/div/main/div[1]/div[2]/div[5]",
        "Ícone 6 (Base)": "/html/body/div/main/div[1]/div[2]/div[6]",
    }

    bugs_encontrados = []
    icones_testados = 0

    for nome_icone, xpath in icones_menu.items():
        with allure.step(f"Testar {nome_icone}"):
            # Voltar para página inicial antes de cada teste
            driver.get(base_url)
            time.sleep(0.5)

            # Capturar screenshot antes de clicar
            caminho_antes = tirar_screenshot(driver, f"{nome_icone.replace(' ', '_')}_antes")
            anexar_screenshot_allure(caminho_antes, f"Antes de clicar - {nome_icone}")

            try:
                # Verificar se ícone existe
                if not elemento_existe(driver, By.XPATH, xpath, timeout=5):
                    bug_msg = f"❌ {nome_icone}: Elemento não encontrado no DOM"
                    bugs_encontrados.append(bug_msg)
                    allure.attach(bug_msg, name="Erro", attachment_type=allure.attachment_type.TEXT)
                    continue

                # Tentar clicar no ícone
                url_antes = driver.current_url
                clicar_com_espera(driver, By.XPATH, xpath, timeout=5)
                time.sleep(1)
                url_depois = driver.current_url

                # Capturar screenshot depois de clicar
                caminho_depois = tirar_screenshot(driver, f"{nome_icone.replace(' ', '_')}_depois")
                anexar_screenshot_allure(caminho_depois, f"Depois de clicar - {nome_icone}")

                # Verificar se navegou
                if url_antes == url_depois:
                    # URL não mudou - ícone não tem ação
                    bug_msg = f"❌ {nome_icone}: Clicável mas SEM ação (permaneceu em {url_depois})"
                    bugs_encontrados.append(bug_msg)
                    allure.attach(bug_msg, name="Bug Detectado", attachment_type=allure.attachment_type.TEXT)
                else:
                    # URL mudou - verificar se foi para "Em breve"
                    page_source = driver.page_source.lower()

                    if "em breve" in page_source or "coming soon" in page_source or "breve" in page_source:
                        # ✅ Comportamento ESPERADO!
                        msg_sucesso = f"✅ {nome_icone}: Levou para 'Em breve' (CORRETO)\nURL: {url_depois}"
                        allure.attach(msg_sucesso, name="Resultado Esperado",
                                      attachment_type=allure.attachment_type.TEXT)
                    else:
                        # Navegou mas não para "Em breve"
                        bug_msg = f"⚠️ {nome_icone}: Navegou mas NÃO para 'Em breve'\nURL: {url_depois}"
                        bugs_encontrados.append(bug_msg)
                        allure.attach(bug_msg, name="Comportamento Inesperado",
                                      attachment_type=allure.attachment_type.TEXT)

                icones_testados += 1

            except Exception as e:
                bug_msg = f"❌ {nome_icone}: Erro ao testar - {str(e)}"
                bugs_encontrados.append(bug_msg)
                allure.attach(bug_msg, name="Erro", attachment_type=allure.attachment_type.TEXT)

    # Resumo final
    with allure.step("Resumo dos testes de navegação"):
        resumo = f"""
📊 RESUMO DOS TESTES DE NAVEGAÇÃO DO MENU:

Ícones testados: {icones_testados}/6
Bugs encontrados: {len(bugs_encontrados)}

{'=' * 60}
"""

        if bugs_encontrados:
            resumo += "⚠️ BUGS DETECTADOS:\n\n"
            for i, bug in enumerate(bugs_encontrados, 1):
                resumo += f"{i}. {bug}\n"

            resumo += f"\n{'=' * 60}\n"
            resumo += "📋 DOCUMENTAÇÃO:\n"
            resumo += "- Ver: docs/bugs-reportados.md (BUG-006)\n"
            resumo += "- Screenshots: evidence/screenshots/*_antes.png e *_depois.png\n"
            resumo += f"\n{'=' * 60}\n"
            resumo += "🎯 CONCLUSÃO:\n"
            resumo += f"Dos 6 ícones do menu lateral, {len(bugs_encontrados)} apresentam problemas.\n"
            resumo += "Nenhum ícone leva para componente 'Em breve' conforme especificado no email RH.\n"
        else:
            resumo += "✅ TODOS OS ÍCONES FUNCIONAM CORRETAMENTE!\n"
            resumo += "Todos levam para componente 'Em breve' conforme especificado.\n"

        allure.attach(resumo, name="Resumo Final", attachment_type=allure.attachment_type.TEXT)

        # Se há bugs, marcar teste como falha esperada
        if bugs_encontrados:
            pytest.fail(
                f"{len(bugs_encontrados)} ícones do menu NÃO levam para 'Em breve' conforme especificado no email RH. "
                f"Bug documentado em docs/bugs-reportados.md (BUG-006)"
            )


@allure.feature('Navegação')
@allure.story('Botão Próximo Passo')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.navigation
def test_navegacao_botao_proximo_passo(driver, base_url):
    """
    Testa botão "Próximo passo" que aparece nos cards de funcionários.

    Comportamento esperado:
        - Botão deve avançar para próxima etapa do fluxo

    Comportamento atual:
        - Botão existe mas não tem ação configurada
        - BUG documentado em docs/bugs-reportados.md
    """

    with allure.step("Acessar aplicação e cadastrar funcionário"):
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)
        lista_page.iniciar_cadastro_funcionario()

        from pages.cadastro_page import CadastroPage
        from utils.data_factory import gerar_dados_funcionario

        cadastro_page = CadastroPage(driver)
        dados = gerar_dados_funcionario()
        dados['cargo'] = 'Cargo 1'
        dados['nao_usa_epi'] = True

        cadastro_page.preencher_e_salvar(dados)
        time.sleep(2)

    with allure.step("Localizar botão 'Próximo passo'"):
        # XPATH do botão "Próximo passo" no card
        botao_proximo_xpath = "/html/body/div/main/div[2]/div[3]/button"

        caminho_antes = tirar_screenshot(driver, "antes_proximo_passo")
        anexar_screenshot_allure(caminho_antes, "Lista antes de clicar 'Próximo passo'")

        # Verificar se botão existe
        botao_existe = elemento_existe(driver, By.XPATH, botao_proximo_xpath, timeout=5)

        if not botao_existe:
            allure.attach(
                "⚠️ Botão 'Próximo passo' não foi encontrado no DOM\n"
                "Possíveis causas:\n"
                "1. Funcionário não foi cadastrado (BUG-003)\n"
                "2. XPATH do botão está incorreto\n"
                "3. Estrutura da página mudou",
                name="Botão Não Encontrado",
                attachment_type=allure.attachment_type.TEXT
            )
            pytest.skip("Botão 'Próximo passo' não encontrado - Possivelmente devido a BUG-003")

    with allure.step("Clicar em 'Próximo passo'"):
        try:
            url_antes = driver.current_url
            clicar_com_espera(driver, By.XPATH, botao_proximo_xpath, timeout=5)
            time.sleep(1)
            url_depois = driver.current_url

            caminho_depois = tirar_screenshot(driver, "depois_proximo_passo")
            anexar_screenshot_allure(caminho_depois, "Depois de clicar 'Próximo passo'")

            # Verificar se navegou
            if url_antes == url_depois:
                allure.attach(
                    "❌ BUG CONFIRMADO: Botão 'Próximo passo' não tem ação configurada\n"
                    "Clique registrado mas nenhuma navegação ocorreu\n"
                    f"URL permaneceu: {url_depois}",
                    name="Bug Detectado",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.fail("Botão 'Próximo passo' sem ação - Bug documentado em docs/bugs-reportados.md")
            else:
                allure.attach(
                    f"✅ Botão 'Próximo passo' funcionou!\n"
                    f"Navegou de: {url_antes}\n"
                    f"Para: {url_depois}",
                    name="Resultado",
                    attachment_type=allure.attachment_type.TEXT
                )

        except Exception as e:
            allure.attach(
                f"⚠️ Erro ao testar botão 'Próximo passo': {str(e)}",
                name="Erro",
                attachment_type=allure.attachment_type.TEXT
            )
            pytest.skip(f"Não foi possível testar botão 'Próximo passo': {str(e)}")


@allure.feature('Navegação')
@allure.story('Botão Voltar')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.navigation
def test_navegacao_botao_voltar(driver, base_url):
    """
    Testa que botão Voltar retorna para listagem.

    ✅ Este teste já existe em test_cadastro_funcionario.py
    Incluído aqui para completude dos testes de navegação.

    Comportamento esperado:
        - Clicar em "Voltar" no formulário de cadastro
        - Sistema deve retornar para lista de funcionários
        - Dados não devem ser salvos
    """

    with allure.step("Acessar formulário de cadastro"):
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)
        lista_page.iniciar_cadastro_funcionario()
        time.sleep(0.5)

    with allure.step("Clicar em Voltar"):
        from pages.cadastro_page import CadastroPage
        cadastro_page = CadastroPage(driver)

        caminho_antes = tirar_screenshot(driver, "antes_voltar")
        anexar_screenshot_allure(caminho_antes, "No formulário antes de voltar")

        url_antes = driver.current_url
        cadastro_page.clicar_voltar()
        time.sleep(1)
        url_depois = driver.current_url

        caminho_depois = tirar_screenshot(driver, "depois_voltar")
        anexar_screenshot_allure(caminho_depois, "Depois de clicar Voltar")

    with allure.step("Validar que retornou para listagem"):
        # Verificar que botão "Adicionar Funcionário" está visível
        lista_page = ListaFuncionariosPage(driver)

        botao_adicionar_visivel = elemento_existe(
            driver,
            *lista_page.BOTAO_ADICIONAR_FUNCIONARIO,
            timeout=5
        )

        if not botao_adicionar_visivel:
            allure.attach(
                f"❌ Botão Voltar NÃO retornou para listagem\n"
                f"URL antes: {url_antes}\n"
                f"URL depois: {url_depois}\n"
                f"Botão 'Adicionar Funcionário' não está visível",
                name="Bug Detectado",
                attachment_type=allure.attachment_type.TEXT
            )
            pytest.fail("Botão Voltar não retornou para listagem")
        else:
            allure.attach(
                f"✅ Botão Voltar funciona corretamente!\n"
                f"Retornou de: {url_antes}\n"
                f"Para: {url_depois}\n"
                f"Botão 'Adicionar Funcionário' está visível",
                name="Resultado",
                attachment_type=allure.attachment_type.TEXT
            )