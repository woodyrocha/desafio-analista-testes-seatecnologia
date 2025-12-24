"""
Fixtures compartilhadas para testes BDD
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope='function')
def base_url():
    """URL base da aplicação"""
    return "http://analista-teste.seatecnologia.com.br"


@pytest.fixture(scope='function')
def driver(base_url):
    """
    Fixture do WebDriver para testes BDD
    Cria uma nova instância do Chrome para cada teste
    """
    # Configurar opções do Chrome
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    # Modo headless (comentar para ver execução)
    # chrome_options.add_argument('--headless')

    # Inicializar driver
    service = Service(ChromeDriverManager().install())
    driver_instance = webdriver.Chrome(service=service, options=chrome_options)
    driver_instance.implicitly_wait(10)

    yield driver_instance

    # Teardown - fechar browser
    driver_instance.quit()