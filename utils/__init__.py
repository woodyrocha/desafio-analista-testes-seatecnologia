"""
Utilitários para testes automatizados.
"""

from .driver_factory import get_driver
from .data_factory import (
    gerar_cpf_fake,
    gerar_nome,
    gerar_data_nascimento,
    gerar_dados_funcionario
)
from .helpers import (
    tirar_screenshot,
    anexar_screenshot_allure,
    esperar_elemento_visivel,
    esperar_elemento_clicavel,
    esperar_elemento_presente,
    limpar_e_preencher,
    clicar_com_espera,
    elemento_existe,
    obter_texto_elemento,
    selecionar_dropdown_por_teclas,
)

__all__ = [
    'get_driver',
    'gerar_cpf_fake',
    'gerar_nome',
    'gerar_data_nascimento',
    'gerar_dados_funcionario',
    'tirar_screenshot',
    'anexar_screenshot_allure',
    'esperar_elemento_visivel',
    'esperar_elemento_clicavel',
    'esperar_elemento_presente',
    'limpar_e_preencher',
    'clicar_com_espera',
    'elemento_existe',
    'obter_texto_elemento',
    'selecionar_dropdown_por_teclas',
]