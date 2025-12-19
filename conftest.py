"""
Configurações globais do Pytest e Fixtures compartilhadas.

Este arquivo é automaticamente carregado pelo pytest e disponibiliza
fixtures para todos os testes do projeto.
"""

import sys
import os
import pytest
import allure
from datetime import datetime
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Carregar variáveis de ambiente
load_dotenv()

# Garantir que a raiz do repositório esteja no PYTHONPATH
ROOT = os.path.abspath(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Importar factory após configurar PYTHONPATH
from utils.driver_factory import get_driver


@pytest.fixture(scope="function")
def driver():
    """
    Fixture que cria e gerencia uma instância do Chrome WebDriver.

    Scope: function - Nova instância para cada teste
    Yield: WebDriver configurado e pronto para uso
    Finalização: Fecha o navegador após o teste
    """
    # Obter configurações do .env
    headless = os.getenv("HEADLESS", "False").lower() == "true"
    implicit_wait = int(os.getenv("IMPLICIT_WAIT", "10"))

    # Criar driver
    driver = get_driver(headless=headless)
    driver.implicitly_wait(implicit_wait)

    # Anexar configuração ao Allure
    allure.attach(
        f"Browser: Chrome\nHeadless: {headless}\nImplicit Wait: {implicit_wait}s",
        name="Test Configuration",
        attachment_type=allure.attachment_type.TEXT
    )

    yield driver

    # Cleanup: fecha o navegador após o teste
    driver.quit()


@pytest.fixture(scope="function")
def base_url():
    """
    Fixture que retorna a URL base da aplicação.
    """
    return os.getenv("BASE_URL", "http://analista-teste.seatecnologia.com.br")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook do pytest que captura o resultado do teste.

    Necessário para capturar falhas e anexar screenshots no Allure.
    """
    outcome = yield
    rep = outcome.get_result()

    # Armazena o resultado no item para uso em outras fixtures
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="function", autouse=True)
def capture_screenshot_on_failure(request, driver):
    """
    Fixture que captura screenshot automaticamente quando um teste falha.

    Autouse: True - Executa automaticamente para todos os testes
    """
    yield

    # Verifica se o teste falhou
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        # Gera nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name.replace(" ", "_").replace("[", "_").replace("]", "_")
        screenshot_name = f"{test_name}_{timestamp}_FALHA.png"

        # Path para salvar
        screenshot_dir = os.getenv("EVIDENCE_PATH", "evidence/screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, screenshot_name)

        # Captura screenshot
        try:
            driver.save_screenshot(screenshot_path)

            # Anexa ao Allure Report
            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name=f"Screenshot - {test_name}",
                    attachment_type=allure.attachment_type.PNG
                )

            print(f"\n📸 Screenshot de falha salvo: {screenshot_path}")
        except Exception as e:
            print(f"\n⚠️ Erro ao capturar screenshot: {e}")


@pytest.fixture(scope="function")
def wait(driver):
    """
    Fixture que retorna um WebDriverWait configurado.

    Útil para esperas explícitas em testes.
    """
    timeout = int(os.getenv("TIMEOUT", "10"))
    return WebDriverWait(driver, timeout)


# Configuração de metadados do Allure para o ambiente de teste
def pytest_configure(config):
    """
    Configura metadados do ambiente para o Allure Report.
    """
    # Cria diretório de resultados se não existir
    allure_dir = "evidence/allure-results"
    os.makedirs(allure_dir, exist_ok=True)

    # Define metadados do ambiente
    env_properties = {
        "Browser": "Chrome",
        "Base URL": os.getenv("BASE_URL", "http://analista-teste.seatecnologia.com.br"),
        "Python Version": sys.version.split()[0],
        "Test Environment": "QA",
    }

    # Escreve arquivo de environment para o Allure
    env_file = os.path.join(allure_dir, "environment.properties")
    with open(env_file, "w") as f:
        for key, value in env_properties.items():
            f.write(f"{key}={value}\n")