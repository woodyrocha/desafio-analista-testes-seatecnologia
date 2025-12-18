import os
import pytest
from utils.driver_factory import get_driver
from pages.lista_funcionarios_page import ListaFuncionariosPage


BASE_URL = os.getenv("BASE_URL", "http://analista-teste.seatecnologia.com.br")


def test_exclusao_funcionario_fluxo_basico():
    driver = get_driver(headless=True)
    try:
        page = ListaFuncionariosPage(driver)
        page.open(BASE_URL)

        # TODO: localizar registro e executar exclusão, validar remoção
        pytest.skip("Implementar fluxo de exclusão conforme a aplicação")
    finally:
        driver.quit()
