import os
import pytest
from utils.driver_factory import get_driver


BASE_URL = os.getenv("BASE_URL", "http://analista-teste.seatecnologia.com.br")


def test_navegacao_links_menu():
    driver = get_driver(headless=True)
    try:
        driver.get(BASE_URL)
        # TODO: percorrer links do menu e validar redirecionamentos / componente 'Em breve'
        pytest.skip("Implementar verificação de navegação de links")
    finally:
        driver.quit()
