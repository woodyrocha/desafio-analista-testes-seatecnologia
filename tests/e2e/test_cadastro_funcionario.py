import os
import pytest
from utils.driver_factory import get_driver
from pages.cadastro_page import CadastroPage
from utils.data_factory import gerar_dados_funcionario


BASE_URL = os.getenv("BASE_URL", "http://analista-teste.seatecnologia.com.br")


def test_cadastro_funcionario_fluxo_basico():
    driver = get_driver(headless=True)
    try:
        page = CadastroPage(driver)
        page.open(BASE_URL)

        dados = gerar_dados_funcionario()
        page.preencher_formulario(dados)
        page.submeter()

        # TODO: adicionar verificações específicas da aplicação
        assert True
    finally:
        driver.quit()
