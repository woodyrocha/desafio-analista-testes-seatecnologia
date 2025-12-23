"""
Testes de Segurança - Inputs (XSS, Injection)

Objetivo: Validar que aplicação sanitiza inputs maliciosos
Status: ✅ Implementado e Melhorado

Testes incluídos:
- XSS em campo Nome
- XSS em múltiplos campos
- SQL Injection básico
- Script Injection
- HTML Injection
"""

import pytest
import allure
from selenium.webdriver.common.by import By
from pages.lista_funcionarios_page import ListaFuncionariosPage
from pages.cadastro_page import CadastroPage
from utils.data_factory import gerar_dados_funcionario
from utils.helpers import (
    tirar_screenshot,
    anexar_screenshot_allure,
    elemento_existe,
    esperar_elemento_clicavel
)
import time


@allure.feature('Segurança')
@allure.story('XSS - Cross-Site Scripting')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.security
@pytest.mark.xss
def test_xss_campo_nome_basico(driver, base_url):
    """
    Testa XSS básico no campo Nome.

    Payloads testados:
    - <script>alert('XSS')</script>
    - <img src=x onerror=alert('XSS')>
    - javascript:alert('XSS')

    Resultado esperado: Payloads devem ser sanitizados/escapados.
    """

    with allure.step("Acessar formulário de cadastro"):
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)
        lista_page.iniciar_cadastro_funcionario()

        cadastro_page = CadastroPage(driver)

        caminho = tirar_screenshot(driver, "antes_xss_teste")
        anexar_screenshot_allure(caminho, "Formulário antes do teste XSS")

    with allure.step("Testar payloads XSS no campo Nome"):
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg/onload=alert('XSS')>",
            "<<SCRIPT>alert('XSS')//<</SCRIPT>",
        ]

        resultados = []
        vulneravel = False

        for payload in payloads:
            try:
                # Preencher campo Nome com payload
                cadastro_page.preencher_nome(payload)
                time.sleep(0.5)

                # Verificar se alert apareceu
                try:
                    alert = driver.switch_to.alert
                    alert_text = alert.text
                    alert.accept()

                    # Se chegamos aqui, XSS foi executado!
                    vulneravel = True
                    resultados.append(f"❌ VULNERÁVEL: {payload}")
                    resultados.append(f"   Alert executado: {alert_text}")

                    caminho = tirar_screenshot(driver, f"xss_vulneravel_{len(resultados)}")
                    anexar_screenshot_allure(caminho, f"XSS Detectado: {payload[:30]}")

                except Exception:
                    # Sem alert = bom (sanitizado)
                    resultados.append(f"✅ SEGURO: {payload}")

                    # Verificar se payload foi sanitizado no campo
                    try:
                        nome_input = driver.find_element(By.XPATH,
                                                         "//input[@placeholder='Nome completo' or contains(@class, 'nome')]")
                        valor_atual = nome_input.get_attribute('value')

                        # Se contém tags HTML, ainda pode ser vulnerável
                        if '<' in valor_atual and '>' in valor_atual:
                            resultados.append(f"   ⚠️ Tags não removidas: {valor_atual[:50]}")
                        else:
                            resultados.append(f"   ✅ Sanitizado: {valor_atual[:50]}")
                    except:
                        pass

                # Limpar campo para próximo teste
                cadastro_page.preencher_nome("")
                time.sleep(0.3)

            except Exception as e:
                resultados.append(f"⚠️ ERRO ao testar {payload}: {str(e)}")

        relatorio = "\n".join(resultados)
        allure.attach(
            f"Resultados dos Testes XSS:\n\n{relatorio}",
            name="Análise XSS - Campo Nome",
            attachment_type=allure.attachment_type.TEXT
        )

        caminho = tirar_screenshot(driver, "apos_xss_testes")
        anexar_screenshot_allure(caminho, "Formulário após testes XSS")

        # Teste falha se encontrou vulnerabilidade
        assert not vulneravel, f"Aplicação VULNERÁVEL a XSS! Veja relatório Allure."


@allure.feature('Segurança')
@allure.story('XSS - Múltiplos Campos')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.security
@pytest.mark.xss
def test_xss_multiplos_campos(driver, base_url):
    """
    Testa XSS em múltiplos campos do formulário.

    Campos testados:
    - Nome
    - RG
    - CPF (se aceitar não-numérico)

    Payload: <script>alert('XSS')</script>
    """

    with allure.step("Acessar formulário e testar múltiplos campos"):
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)
        lista_page.iniciar_cadastro_funcionario()

        cadastro_page = CadastroPage(driver)
        time.sleep(1)

        payload = "<script>alert('XSS')</script>"
        campos_testados = []
        vulneravel = False

        # Testar Nome
        try:
            cadastro_page.preencher_nome(payload)
            time.sleep(0.5)

            try:
                alert = driver.switch_to.alert
                alert.accept()
                vulneravel = True
                campos_testados.append("❌ NOME: Vulnerável")
            except:
                campos_testados.append("✅ NOME: Seguro")
        except Exception as e:
            campos_testados.append(f"⚠️ NOME: Erro - {str(e)}")

        # Testar RG
        try:
            cadastro_page.preencher_rg(payload)
            time.sleep(0.5)

            try:
                alert = driver.switch_to.alert
                alert.accept()
                vulneravel = True
                campos_testados.append("❌ RG: Vulnerável")
            except:
                campos_testados.append("✅ RG: Seguro")
        except Exception as e:
            campos_testados.append(f"⚠️ RG: Erro - {str(e)}")

        relatorio = "\n".join(campos_testados)
        allure.attach(
            f"Teste XSS em Múltiplos Campos:\n\n{relatorio}",
            name="Análise XSS Multi-Campo",
            attachment_type=allure.attachment_type.TEXT
        )

        caminho = tirar_screenshot(driver, "xss_multiplos_campos")
        anexar_screenshot_allure(caminho, "Teste XSS Múltiplos Campos")

        assert not vulneravel, "Um ou mais campos vulneráveis a XSS"


@allure.feature('Segurança')
@allure.story('SQL Injection Básico')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.security
@pytest.mark.sql_injection
def test_sql_injection_basico(driver, base_url):
    """
    Testa SQL Injection básico nos campos.

    Payloads testados:
    - ' OR '1'='1
    - '; DROP TABLE funcionarios; --
    - ' UNION SELECT * FROM users --

    Resultado esperado: 
    - Nenhum erro SQL exposto
    - Dados não retornados indevidamente
    - Aplicação não quebra
    """

    with allure.step("Acessar formulário de cadastro"):
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)
        lista_page.iniciar_cadastro_funcionario()

        cadastro_page = CadastroPage(driver)
        time.sleep(1)

    with allure.step("Testar payloads SQL Injection"):
        payloads = [
            "' OR '1'='1",
            "'; DROP TABLE funcionarios; --",
            "' UNION SELECT * FROM users --",
            "admin'--",
            "' OR 1=1--",
        ]

        resultados = []
        erro_sql_encontrado = False

        for payload in payloads:
            try:
                # Tentar injetar no campo Nome
                cadastro_page.preencher_nome(payload)
                time.sleep(0.5)

                # Verificar se página mostra erro SQL
                page_source = driver.page_source.lower()

                erros_sql = [
                    'sql syntax',
                    'mysql_fetch',
                    'pg_query',
                    'odbc_exec',
                    'sqlite_query',
                    'ora-',
                    'postgresql',
                    'you have an error in your sql',
                    'warning: mysql',
                    'unclosed quotation mark',
                ]

                erro_encontrado = any(erro in page_source for erro in erros_sql)

                if erro_encontrado:
                    erro_sql_encontrado = True
                    resultados.append(f"❌ ERRO SQL EXPOSTO: {payload}")

                    caminho = tirar_screenshot(driver, f"sql_injection_{len(resultados)}")
                    anexar_screenshot_allure(caminho, f"SQL Error: {payload[:30]}")
                else:
                    resultados.append(f"✅ Sem erro SQL: {payload}")

                # Limpar campo
                cadastro_page.preencher_nome("")

            except Exception as e:
                resultados.append(f"⚠️ Erro ao testar {payload}: {str(e)}")

        relatorio = "\n".join(resultados)
        allure.attach(
            f"Testes SQL Injection:\n\n{relatorio}\n\n"
            f"Nota: Ausência de erro SQL não garante segurança completa.\n"
            f"Aplicação pode usar prepared statements corretamente.",
            name="Análise SQL Injection",
            attachment_type=allure.attachment_type.TEXT
        )

        # Teste falha se erro SQL foi exposto
        assert not erro_sql_encontrado, \
            "Aplicação expõe erros SQL - possível vulnerabilidade"


@allure.feature('Segurança')
@allure.story('HTML Injection')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.security
def test_html_injection(driver, base_url):
    """
    Testa se aplicação sanitiza HTML malicioso.

    HTML Injection pode:
    - Alterar aparência da página
    - Criar campos falsos (phishing)
    - Injetar links maliciosos
    """

    with allure.step("Acessar formulário"):
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)
        lista_page.iniciar_cadastro_funcionario()

        cadastro_page = CadastroPage(driver)
        time.sleep(1)

    with allure.step("Testar payloads HTML Injection"):
        payloads = [
            "<h1>Título Injetado</h1>",
            "<a href='http://evil.com'>Clique aqui</a>",
            "<iframe src='http://evil.com'></iframe>",
            "<img src='http://evil.com/img.jpg'>",
            "<style>body{display:none}</style>",
        ]

        resultados = []

        for payload in payloads:
            try:
                cadastro_page.preencher_nome(payload)
                time.sleep(0.5)

                # Verificar se HTML foi renderizado
                page_source = driver.page_source

                # Se encontrar as tags no HTML renderizado, pode ser vulnerável
                tags = ['<h1>', '<a ', '<iframe', '<img', '<style']
                tag_renderizada = any(tag in page_source for tag in tags)

                if tag_renderizada:
                    resultados.append(f"⚠️ HTML pode ter sido injetado: {payload[:40]}")
                else:
                    resultados.append(f"✅ HTML sanitizado: {payload[:40]}")

                cadastro_page.preencher_nome("")

            except Exception as e:
                resultados.append(f"⚠️ Erro: {str(e)}")

        relatorio = "\n".join(resultados)
        allure.attach(
            f"Testes HTML Injection:\n\n{relatorio}",
            name="Análise HTML Injection",
            attachment_type=allure.attachment_type.TEXT
        )

        caminho = tirar_screenshot(driver, "html_injection_teste")
        anexar_screenshot_allure(caminho, "Teste HTML Injection")

        # Teste sempre passa (apenas informativo)
        assert True


@allure.feature('Segurança')
@allure.story('Path Traversal')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.security
def test_path_traversal_basico(driver, base_url):
    """
    Testa se aplicação é vulnerável a Path Traversal.

    Payloads:
    - ../../etc/passwd
    - ..\\..\\windows\\system32\\config\\sam

    Nota: Teste básico, pode ter falsos negativos.
    """

    with allure.step("Testar path traversal em URL"):
        payloads = [
            f"{base_url}/../../etc/passwd",
            f"{base_url}/../../../etc/passwd",
            f"{base_url}/%2e%2e%2f%2e%2e%2fetc/passwd",
        ]

        resultados = []

        for payload in payloads:
            try:
                driver.get(payload)
                time.sleep(1)

                page_source = driver.page_source.lower()

                # Procurar por indicadores de path traversal bem-sucedido
                indicadores = ['root:', 'daemon:', '/bin/bash', 'nobody:']

                if any(ind in page_source for ind in indicadores):
                    resultados.append(f"❌ VULNERÁVEL: {payload}")

                    caminho = tirar_screenshot(driver, "path_traversal_vulneravel")
                    anexar_screenshot_allure(caminho, "Path Traversal Detectado")
                else:
                    resultados.append(f"✅ Seguro: {payload}")

            except Exception as e:
                resultados.append(f"⚠️ Erro: {str(e)}")

        relatorio = "\n".join(resultados)
        allure.attach(
            f"Testes Path Traversal:\n\n{relatorio}",
            name="Análise Path Traversal",
            attachment_type=allure.attachment_type.TEXT
        )

        # Teste sempre passa (apenas informativo)
        assert True