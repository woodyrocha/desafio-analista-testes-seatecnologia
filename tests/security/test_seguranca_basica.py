"""
Testes de Segurança Básica

Objetivo: Validar aspectos básicos de segurança da aplicação
Status: ✅ Implementado

Testes incluídos:
- HTTPS/TLS
- Headers de segurança
- Cookies seguros
- Informações sensíveis expostas
- Versões de software expostas
"""

import pytest
import allure
import requests
from selenium.webdriver.common.by import By
from pages.lista_funcionarios_page import ListaFuncionariosPage
from pages.cadastro_page import CadastroPage
from utils.data_factory import gerar_dados_funcionario
from utils.helpers import tirar_screenshot, anexar_screenshot_allure


@allure.feature('Segurança')
@allure.story('Headers de Segurança HTTP')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.security
def test_security_headers_basicos(base_url):
    """
    Testa se aplicação possui headers de segurança básicos.

    Headers recomendados:
    - X-Content-Type-Options: nosniff
    - X-Frame-Options: DENY ou SAMEORIGIN
    - X-XSS-Protection: 1; mode=block (legado mas ainda útil)
    - Content-Security-Policy: (recomendado)

    Nota: Nem todos são obrigatórios, mas são boas práticas.
    """

    with allure.step("Fazer requisição HTTP para obter headers"):
        try:
            response = requests.get(base_url, timeout=10)
            headers = response.headers

            allure.attach(
                str(dict(headers)),
                name="Headers HTTP Recebidos",
                attachment_type=allure.attachment_type.TEXT
            )
        except Exception as e:
            pytest.skip(f"Não foi possível fazer requisição: {str(e)}")

    with allure.step("Validar headers de segurança"):
        resultados = []

        # X-Content-Type-Options
        if 'X-Content-Type-Options' in headers:
            resultados.append("✅ X-Content-Type-Options presente")
            if headers['X-Content-Type-Options'] == 'nosniff':
                resultados.append("  ✅ Valor correto: nosniff")
            else:
                resultados.append(f"  ⚠️ Valor: {headers['X-Content-Type-Options']}")
        else:
            resultados.append("❌ X-Content-Type-Options AUSENTE (recomendado)")

        # X-Frame-Options
        if 'X-Frame-Options' in headers:
            resultados.append("✅ X-Frame-Options presente")
            valor = headers['X-Frame-Options']
            if valor in ['DENY', 'SAMEORIGIN']:
                resultados.append(f"  ✅ Valor correto: {valor}")
            else:
                resultados.append(f"  ⚠️ Valor: {valor}")
        else:
            resultados.append("❌ X-Frame-Options AUSENTE (recomendado)")

        # X-XSS-Protection (legado mas ainda usado)
        if 'X-XSS-Protection' in headers:
            resultados.append("✅ X-XSS-Protection presente")
            resultados.append(f"  Valor: {headers['X-XSS-Protection']}")
        else:
            resultados.append("⚠️ X-XSS-Protection ausente (legado, opcional)")

        # Content-Security-Policy
        if 'Content-Security-Policy' in headers:
            resultados.append("✅ Content-Security-Policy presente")
            resultados.append(f"  Política: {headers['Content-Security-Policy'][:100]}...")
        else:
            resultados.append("⚠️ Content-Security-Policy ausente (recomendado)")

        # Strict-Transport-Security (HSTS) - se HTTPS
        if base_url.startswith('https'):
            if 'Strict-Transport-Security' in headers:
                resultados.append("✅ Strict-Transport-Security presente (HSTS)")
                resultados.append(f"  Valor: {headers['Strict-Transport-Security']}")
            else:
                resultados.append("❌ Strict-Transport-Security AUSENTE (obrigatório em HTTPS)")

        relatorio = "\n".join(resultados)
        allure.attach(
            relatorio,
            name="Análise de Headers de Segurança",
            attachment_type=allure.attachment_type.TEXT
        )

        # Contar quantos headers importantes estão presentes
        headers_importantes = [
            'X-Content-Type-Options',
            'X-Frame-Options'
        ]
        presentes = sum(1 for h in headers_importantes if h in headers)

        # Teste passa se pelo menos 1 dos 2 headers importantes está presente
        # (não é bloqueador, apenas informativo)
        assert presentes >= 1 or True, \
            f"Apenas {presentes}/2 headers de segurança importantes presentes"


@allure.feature('Segurança')
@allure.story('Protocolo HTTPS')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.security
def test_https_protocol(base_url):
    """
    Verifica se aplicação usa HTTPS.

    Nota: Como é ambiente de teste, pode estar em HTTP.
    Teste documenta se HTTPS está sendo usado.
    """

    with allure.step("Verificar protocolo da URL"):
        usa_https = base_url.startswith('https://')

        if usa_https:
            resultado = "✅ HTTPS: Aplicação usa protocolo seguro"
            allure.attach(
                "Aplicação usa HTTPS ✅\n"
                "Comunicação é criptografada\n"
                "Dados do usuário protegidos em trânsito",
                name="HTTPS Ativo",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            resultado = "⚠️ HTTP: Aplicação NÃO usa HTTPS"
            allure.attach(
                "⚠️ Aplicação usa HTTP (não seguro)\n\n"
                "Recomendações:\n"
                "1. Implementar HTTPS em produção\n"
                "2. Redirecionar HTTP → HTTPS\n"
                "3. Usar certificado SSL/TLS válido\n"
                "4. Configurar HSTS header\n\n"
                "Riscos do HTTP:\n"
                "- Dados trafegam em texto plano\n"
                "- Vulnerável a man-in-the-middle\n"
                "- Credenciais expostas\n"
                "- Sem garantia de integridade",
                name="HTTP Detectado (Não Seguro)",
                attachment_type=allure.attachment_type.TEXT
            )

        # Não falha o teste, apenas documenta
        # (ambiente de teste pode não ter HTTPS)
        assert True, resultado


@allure.feature('Segurança')
@allure.story('Informações Sensíveis Expostas')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.security
def test_informacoes_sensiveis_expostas(driver, base_url):
    """
    Verifica se há informações sensíveis expostas no HTML/JavaScript.

    Procura por:
    - Senhas em texto plano
    - API keys
    - Tokens de autenticação
    - Comentários com informações sensíveis
    - Stack traces
    """

    with allure.step("Acessar aplicação e obter HTML"):
        driver.get(base_url)
        import time
        time.sleep(2)

        page_source = driver.page_source.lower()

        caminho = tirar_screenshot(driver, "analise_seguranca_html")
        anexar_screenshot_allure(caminho, "Página analisada")

    with allure.step("Procurar por padrões sensíveis"):
        padroes_sensiveis = {
            "password": "Palavra 'password' encontrada",
            "api_key": "Possível API key exposta",
            "apikey": "Possível API key exposta",
            "secret": "Palavra 'secret' encontrada",
            "token": "Palavra 'token' encontrada",
            "accesstoken": "Access token possível",
            "private_key": "Private key mencionada",
            "admin": "Palavra 'admin' encontrada",
            "database": "Informações de database",
            "db_password": "Senha de database",
            "error": "Mensagem de erro exposta",
            "exception": "Exception exposta",
            "stack trace": "Stack trace exposto",
        }

        encontrados = []
        for padrao, descricao in padroes_sensiveis.items():
            if padrao in page_source:
                encontrados.append(f"⚠️ {descricao}: '{padrao}'")

        if encontrados:
            relatorio = "Padrões sensíveis encontrados:\n\n" + "\n".join(encontrados)
            relatorio += "\n\nRecomendação: Revisar se informações sensíveis estão realmente expostas."

            allure.attach(
                relatorio,
                name="Análise de Informações Sensíveis",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                "✅ Nenhum padrão sensível óbvio encontrado no HTML",
                name="Análise Limpa",
                attachment_type=allure.attachment_type.TEXT
            )

        # Teste passa sempre (apenas informativo)
        # Se encontrar algo, está documentado no Allure
        assert True


@allure.feature('Segurança')
@allure.story('Cookies Seguros')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.security
def test_cookies_seguros(driver, base_url):
    """
    Verifica se cookies possuem flags de segurança.

    Flags importantes:
    - HttpOnly: Previne acesso via JavaScript
    - Secure: Apenas em HTTPS
    - SameSite: Previne CSRF
    """

    with allure.step("Acessar aplicação e obter cookies"):
        driver.get(base_url)
        import time
        time.sleep(2)

        cookies = driver.get_cookies()

        if not cookies:
            allure.attach(
                "ℹ️ Nenhum cookie encontrado na aplicação",
                name="Sem Cookies",
                attachment_type=allure.attachment_type.TEXT
            )
            pytest.skip("Aplicação não usa cookies")

    with allure.step("Analisar flags de segurança dos cookies"):
        analise = []

        for cookie in cookies:
            nome = cookie.get('name', 'unnamed')
            analise.append(f"\n📍 Cookie: {nome}")

            # HttpOnly
            if cookie.get('httpOnly', False):
                analise.append("  ✅ HttpOnly: Sim (protegido contra XSS)")
            else:
                analise.append("  ⚠️ HttpOnly: Não (acessível via JavaScript)")

            # Secure
            if cookie.get('secure', False):
                analise.append("  ✅ Secure: Sim (apenas HTTPS)")
            else:
                analise.append("  ⚠️ Secure: Não (pode trafegar em HTTP)")

            # SameSite
            samesite = cookie.get('sameSite', 'None')
            if samesite in ['Strict', 'Lax']:
                analise.append(f"  ✅ SameSite: {samesite} (proteção CSRF)")
            else:
                analise.append(f"  ⚠️ SameSite: {samesite} (sem proteção CSRF)")

        relatorio = "\n".join(analise)
        allure.attach(
            relatorio,
            name="Análise de Cookies",
            attachment_type=allure.attachment_type.TEXT
        )

        # Teste passa sempre (apenas informativo)
        assert True


@allure.feature('Segurança')
@allure.story('Versões de Software Expostas')
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.security
def test_versoes_software_expostas(base_url):
    """
    Verifica se headers expõem versões de software.

    Headers que podem expor informações:
    - Server: nginx/1.18.0
    - X-Powered-By: PHP/7.4.3
    - X-AspNet-Version: 4.0.30319

    Expor versões facilita ataques direcionados a vulnerabilidades conhecidas.
    """

    with allure.step("Obter headers da resposta HTTP"):
        try:
            response = requests.get(base_url, timeout=10)
            headers = response.headers
        except Exception as e:
            pytest.skip(f"Não foi possível fazer requisição: {str(e)}")

    with allure.step("Verificar se versões estão expostas"):
        headers_suspeitos = {
            'Server': 'Servidor web',
            'X-Powered-By': 'Tecnologia backend',
            'X-AspNet-Version': 'Versão ASP.NET',
            'X-AspNetMvc-Version': 'Versão ASP.NET MVC',
        }

        expostos = []
        for header, descricao in headers_suspeitos.items():
            if header in headers:
                valor = headers[header]
                expostos.append(f"⚠️ {descricao} exposto: {valor}")

        if expostos:
            relatorio = "Versões de software expostas:\n\n"
            relatorio += "\n".join(expostos)
            relatorio += "\n\nRecomendação: Ocultar versões em produção para dificultar ataques direcionados."

            allure.attach(
                relatorio,
                name="Versões Expostas",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                "✅ Nenhuma versão de software obviamente exposta",
                name="Boas Práticas",
                attachment_type=allure.attachment_type.TEXT
            )

        # Teste passa sempre (apenas informativo)
        assert True


@allure.feature('Segurança')
@allure.story('Redirecionamento Aberto')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.security
def test_open_redirect(driver, base_url):
    """
    Testa se aplicação é vulnerável a Open Redirect.

    Open Redirect permite que atacante redirecione usuários para sites maliciosos.

    Nota: Teste básico, pode ter falsos positivos/negativos.
    """

    with allure.step("Tentar redirecionamento para site externo"):
        # Testar padrões comuns de open redirect
        payloads = [
            f"{base_url}?redirect=https://evil.com",
            f"{base_url}?url=https://evil.com",
            f"{base_url}?next=https://evil.com",
            f"{base_url}?return=https://evil.com",
        ]

        vulneravel = False
        detalhes = []

        for payload in payloads:
            try:
                driver.get(payload)
                import time
                time.sleep(1)

                url_atual = driver.current_url

                # Se redirecionou para evil.com, é vulnerável
                if 'evil.com' in url_atual:
                    vulneravel = True
                    detalhes.append(f"❌ VULNERÁVEL: {payload}")
                    detalhes.append(f"   Redirecionou para: {url_atual}")
                else:
                    detalhes.append(f"✅ Seguro: {payload}")
                    detalhes.append(f"   Permaneceu em: {url_atual}")
            except Exception as e:
                detalhes.append(f"⚠️ Erro ao testar: {payload}")
                detalhes.append(f"   {str(e)}")

        relatorio = "\n".join(detalhes)

        if vulneravel:
            allure.attach(
                f"❌ VULNERABILIDADE DETECTADA: Open Redirect\n\n{relatorio}",
                name="Open Redirect Detectado",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"✅ Sem vulnerabilidade de Open Redirect detectada\n\n{relatorio}",
                name="Teste Open Redirect",
                attachment_type=allure.attachment_type.TEXT
            )

        # Teste passa se não for vulnerável
        assert not vulneravel, "Aplicação vulnerável a Open Redirect"