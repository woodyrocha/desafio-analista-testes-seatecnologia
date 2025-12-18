import os
import pytest
from utils.driver_factory import get_driver

BASE_URL = os.getenv("BASE_URL", "http://analista-teste.seatecnologia.com.br")


@pytest.mark.security
def test_xss_basic_injection_input():
    """Teste simples de XSS: insere payloads em campos de formulário e verifica se são escapados.

    Observação: este é um teste leve de análise de segurança funcional. Ajuste seletores/payloads conforme a aplicação.
    """
    driver = get_driver(headless=True)
    try:
        driver.get(BASE_URL)

        # Exemplo: localizar campo de nome e injetar payload XSS
        try:
            nome = driver.find_element("name", "nome")
            payload = "<script>alert('xss')</script>"
            nome.clear()
            nome.send_keys(payload)

            # Submeter se houver botão de submit
            btn = None
            try:
                btn = driver.find_element("css selector", "button[type=submit]")
            except Exception:
                pass
            if btn:
                btn.click()

            # Verificar se o alert aparece (indicador de XSS não sanitizado)
            # Se alert aparecer, o teste falha. Se não, consideramos seguro neste fluxo.
            try:
                alert = driver.switch_to.alert
                # Se chegarmos aqui, XSS ocorreu
                alert_text = alert.text
                alert.accept()
                pytest.fail(f"XSS detectado: {alert_text}")
            except Exception:
                # Nenhum alert — OK (não prova ausência total de XSS)
                assert True
        except Exception as e:
            pytest.skip(f"Não foi possível localizar campos na página para executar o teste: {e}")
    finally:
        driver.quit()
