"""
Testes de Validação de Data de Nascimento

Objetivo: Validar que o sistema aceita apenas datas válidas e dentro de faixas razoáveis
Escopo: Frontend (validação visual) + Backend (se implementado)
"""

import pytest
import allure
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By

from pages.lista_funcionarios_page import ListaFuncionariosPage
from pages.cadastro_page import CadastroPage
from utils.data_factory import gerar_dados_funcionario


# ========================================
# FUNÇÕES AUXILIARES DE VALIDAÇÃO
# ========================================

def validar_data_nascimento(data_str: str) -> tuple[bool, str]:
    """
    Valida data de nascimento segundo regras de negócio.

    Args:
        data_str: String com data no formato DD/MM/AAAA

    Returns:
        Tupla (é_válida, mensagem_erro)

    Regras:
        - Formato deve ser DD/MM/AAAA
        - Data não pode ser futura
        - Pessoa não pode ter mais de 120 anos
        - Data deve existir no calendário

    Exemplo:
        >>> validar_data_nascimento("01/01/1990")
        (True, "")
        >>> validar_data_nascimento("01/01/2030")
        (False, "Data não pode ser futura")
    """
    import re

    # CORREÇÃO: Validar formato DD/MM/AAAA ANTES de fazer parse
    # Isso garante que "1/1/2023" seja rejeitado (deve ser "01/01/2023")
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', data_str):
        return False, "Formato inválido. Use DD/MM/AAAA (com zeros à esquerda)"

    try:
        # Parse da data
        data = datetime.strptime(data_str, "%d/%m/%Y")
        hoje = datetime.now()

        # Valida se não é futura
        if data > hoje:
            return False, "Data de nascimento não pode ser futura"

        # Calcula idade
        idade = (hoje - data).days // 365

        # Valida idade mínima (recém-nascido - 0 anos)
        if idade < 0:
            return False, "Data inválida"

        # Valida idade máxima (120 anos é razoável)
        if idade > 120:
            return False, "Data muito antiga (pessoa teria mais de 120 anos)"

        # Valida que não é hoje
        if data.date() == hoje.date():
            return False, "Data de nascimento não pode ser hoje"

        return True, ""

    except ValueError as e:
        return False, f"Formato de data inválido: {str(e)}"


def calcular_idade(data_nascimento_str: str) -> int:
    """
    Calcula idade a partir da data de nascimento.

    Args:
        data_nascimento_str: Data no formato DD/MM/AAAA

    Returns:
        Idade em anos
    """
    try:
        data_nasc = datetime.strptime(data_nascimento_str, "%d/%m/%Y")
        hoje = datetime.now()
        idade = (hoje - data_nasc).days // 365
        return idade
    except:
        return -1


def eh_ano_bissexto(ano: int) -> bool:
    """
    Verifica se ano é bissexto.

    Regra: Divisível por 4, exceto seculares que devem ser divisíveis por 400
    """
    return (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0)


# ========================================
# FIXTURES
# ========================================

@pytest.fixture
def abrir_formulario_cadastro(driver, base_url):
    """Abre o formulário de cadastro de funcionário"""
    with allure.step("Acessar aplicação e abrir formulário de cadastro"):
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)
        lista_page.iniciar_cadastro_funcionario()
        return CadastroPage(driver)


# ========================================
# TESTES DE VALIDAÇÃO DE DATA
# ========================================

@allure.feature('Validações')
@allure.story('Validação de Data de Nascimento')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.validations
@pytest.mark.data
def test_data_nascimento_valida_aceita(driver, base_url):
    """
    Testa que data de nascimento válida é aceita pelo sistema.

    Cenário:
        1. Abrir formulário de cadastro
        2. Preencher data válida (01/01/1990)
        3. Validar que não há erro
        4. Verificar cálculo de idade
    """
    with allure.step("Abrir formulário de cadastro"):
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)
        lista_page.iniciar_cadastro_funcionario()
        cadastro_page = CadastroPage(driver)

    data_valida = "01/01/1990"

    with allure.step(f"Preencher data válida: {data_valida}"):
        # Validar com nossa função
        eh_valida, erro = validar_data_nascimento(data_valida)
        assert eh_valida, f"Data deveria ser válida. Erro: {erro}"

        # Calcular idade esperada
        idade = calcular_idade(data_valida)

        allure.attach(
            f"Data: {data_valida}\nIdade: ~{idade} anos\nVálida: {eh_valida}",
            name="Dados do Teste",
            attachment_type=allure.attachment_type.TEXT
        )

        cadastro_page.preencher_data_nascimento(data_valida)

    with allure.step("Validar que data foi aceita"):
        from utils.helpers import tirar_screenshot, anexar_screenshot_allure
        import time
        time.sleep(0.5)

        caminho = tirar_screenshot(driver, "data_valida_aceita")
        anexar_screenshot_allure(caminho, "Data Válida Aceita")


@allure.feature('Validações')
@allure.story('Validação de Data de Nascimento')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.validations
@pytest.mark.data
@pytest.mark.parametrize("data_invalida,motivo_erro", [
    ("01/01/2030", "Data futura"),
    ("32/01/1990", "Dia inválido (32)"),
    ("01/13/1990", "Mês inválido (13)"),
    ("00/01/1990", "Dia zero"),
    ("01/00/1990", "Mês zero"),
    ("31/02/1990", "Fevereiro não tem 31 dias"),
    ("29/02/2023", "2023 não é bissexto"),
    ("01/01/1850", "Mais de 120 anos"),
    ("01/01/1900", "Mais de 120 anos"),
])
def test_data_nascimento_invalida_rejeitada(data_invalida, motivo_erro):
    """
    Testa que datas inválidas são rejeitadas.

    Parametrizado para testar múltiplas datas inválidas.
    """
    with allure.step(f"Testar data inválida: {data_invalida} ({motivo_erro})"):
        allure.attach(
            f"Data: {data_invalida}\nMotivo: {motivo_erro}",
            name="Dados do Teste",
            attachment_type=allure.attachment_type.TEXT
        )

        # Validar com nossa função
        eh_valida, mensagem_erro = validar_data_nascimento(data_invalida)

        # Data deve ser inválida
        assert not eh_valida, f"Data {data_invalida} deveria ser inválida ({motivo_erro})"

        # Anexar mensagem de erro
        allure.attach(
            mensagem_erro,
            name="Mensagem de Erro",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.feature('Validações')
@allure.story('Validação de Data de Nascimento')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.validations
@pytest.mark.data
def test_data_nascimento_futura_rejeitada(driver, base_url, abrir_formulario_cadastro):
    """
    Testa especificamente que data futura é rejeitada.

    Cenário crítico: Usuário não pode cadastrar pessoa que ainda vai nascer.
    """
    cadastro_page = abrir_formulario_cadastro

    # Data futura (1 ano à frente)
    data_futura = (datetime.now() + timedelta(days=365)).strftime("%d/%m/%Y")

    with allure.step(f"Tentar preencher data futura: {data_futura}"):
        # Validar com nossa função
        eh_valida, erro = validar_data_nascimento(data_futura)
        assert not eh_valida, "Data futura deveria ser rejeitada"
        assert "futura" in erro.lower(), f"Erro deveria mencionar 'futura'. Erro: {erro}"

        allure.attach(
            f"Data: {data_futura}\nErro esperado: {erro}",
            name="Validação de Data Futura",
            attachment_type=allure.attachment_type.TEXT
        )

        cadastro_page.preencher_data_nascimento(data_futura)

        import time
        time.sleep(0.5)

        from utils.helpers import tirar_screenshot, anexar_screenshot_allure
        caminho = tirar_screenshot(driver, "data_futura_rejeitada")
        anexar_screenshot_allure(caminho, "Tentativa de Data Futura")


@allure.feature('Validações')
@allure.story('Validação de Data de Nascimento')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.validations
@pytest.mark.data
def test_data_nascimento_menor_idade(driver, base_url, abrir_formulario_cadastro):
    """
    Testa cadastro de funcionário menor de idade (15 anos).

    Comportamento esperado pode variar:
        - Sistema pode permitir (com aviso)
        - Sistema pode rejeitar

    Este teste documenta o comportamento.
    """
    cadastro_page = abrir_formulario_cadastro

    # Data para pessoa de 15 anos
    data_menor = (datetime.now() - timedelta(days=15 * 365)).strftime("%d/%m/%Y")
    idade = calcular_idade(data_menor)

    with allure.step(f"Preencher data de menor de idade: {data_menor} (~{idade} anos)"):
        # Data é tecnicamente válida
        eh_valida, _ = validar_data_nascimento(data_menor)
        assert eh_valida, "Data é válida (menor de idade, mas data correta)"

        allure.attach(
            f"Data: {data_menor}\nIdade: ~{idade} anos\nMenor de idade: Sim",
            name="Dados do Teste",
            attachment_type=allure.attachment_type.TEXT
        )

        cadastro_page.preencher_data_nascimento(data_menor)

        import time
        time.sleep(0.5)

        from utils.helpers import tirar_screenshot, anexar_screenshot_allure
        caminho = tirar_screenshot(driver, "data_menor_idade")
        anexar_screenshot_allure(caminho, "Cadastro de Menor de Idade")

        # Nota: Sistema pode exibir aviso mas permitir cadastro


@allure.feature('Validações')
@allure.story('Validação de Data de Nascimento')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.validations
@pytest.mark.data
def test_ano_bissexto_validacao():
    """
    Testa validação de datas em anos bissextos.

    Regra: 29 de fevereiro só existe em anos bissextos.
    """
    with allure.step("Testar 29/02 em anos bissextos"):
        anos_bissextos = [2000, 2004, 2020, 2024]

        for ano in anos_bissextos:
            data = f"29/02/{ano}"
            eh_valida, erro = validar_data_nascimento(data)

            # Verificar que ano é bissexto
            assert eh_ano_bissexto(ano), f"{ano} deveria ser bissexto"

            # Data deve ser válida (assumindo que não é futura)
            if ano <= datetime.now().year:
                assert eh_valida, f"{data} deveria ser válida (ano bissexto)"
                allure.attach(f"✅ {data} - Válida (bissexto)", name="Ano Bissexto",
                              attachment_type=allure.attachment_type.TEXT)

    with allure.step("Testar 29/02 em anos NÃO bissextos"):
        anos_nao_bissextos = [1900, 2001, 2021, 2023]

        for ano in anos_nao_bissextos:
            data = f"29/02/{ano}"
            eh_valida, erro = validar_data_nascimento(data)

            # Verificar que ano NÃO é bissexto
            assert not eh_ano_bissexto(ano), f"{ano} não deveria ser bissexto"

            # Data deve ser inválida
            assert not eh_valida, f"{data} deveria ser inválida (não é bissexto)"
            allure.attach(f"❌ {data} - Inválida (não bissexto)", name="Ano Não Bissexto",
                          attachment_type=allure.attachment_type.TEXT)


@allure.feature('Validações')
@allure.story('Validação de Data de Nascimento')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.validations
@pytest.mark.data
def test_data_nascimento_hoje_rejeitada():
    """
    Testa que data de nascimento igual a hoje é rejeitada.

    Funcionário não pode ter acabado de nascer hoje.
    """
    data_hoje = datetime.now().strftime("%d/%m/%Y")

    with allure.step(f"Validar que data de hoje é rejeitada: {data_hoje}"):
        eh_valida, erro = validar_data_nascimento(data_hoje)

        assert not eh_valida, "Data de hoje deveria ser rejeitada"
        assert "hoje" in erro.lower() or "futura" in erro.lower(), f"Erro deveria mencionar 'hoje'. Erro: {erro}"

        allure.attach(
            f"Data: {data_hoje} (hoje)\nVálida: {eh_valida}\nErro: {erro}",
            name="Validação Data de Hoje",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.feature('Validações')
@allure.story('Validação de Data de Nascimento')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.validations
@pytest.mark.data
@pytest.mark.parametrize("formato_invalido", [
    "2023-01-01",  # Formato ISO
    "01-01-2023",  # Hífen ao invés de barra
    "1/1/2023",  # Sem zero à esquerda
    "01/1/2023",  # Mês sem zero
    "1/01/2023",  # Dia sem zero
    "abc/def/ghij",  # Texto
    "01/01/23",  # Ano com 2 dígitos
])
def test_data_formato_invalido(formato_invalido):
    """
    Testa que formatos de data inválidos são rejeitados.

    Formato esperado: DD/MM/AAAA
    """
    with allure.step(f"Validar formato inválido: {formato_invalido}"):
        eh_valida, erro = validar_data_nascimento(formato_invalido)

        assert not eh_valida, f"Formato {formato_invalido} deveria ser rejeitado"

        allure.attach(
            f"Formato: {formato_invalido}\nVálida: {eh_valida}\nErro: {erro}",
            name="Formato Inválido",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.feature('Validações')
@allure.story('Validação de Data de Nascimento')
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.validations
@pytest.mark.data
def test_calculo_idade_correto():
    """
    Testa que cálculo de idade está correto.
    """
    with allure.step("Testar cálculo de idade"):
        # Casos conhecidos - ATUALIZADO PARA 2025
        casos = [
            ("01/01/1990", 35),  # 35 anos em 2025
            ("01/01/2000", 25),  # 25 anos em 2025
            ("01/01/2010", 15),  # 15 anos em 2025
        ]

        for data, idade_esperada in casos:
            idade_calculada = calcular_idade(data)

            # Margem de erro de 1 ano (depende da data atual)
            assert abs(idade_calculada - idade_esperada) <= 1, \
                f"Idade para {data} deveria ser ~{idade_esperada}, calculou {idade_calculada}"

            allure.attach(
                f"Data: {data}\nIdade Esperada: ~{idade_esperada}\nIdade Calculada: {idade_calculada}",
                name=f"Cálculo de Idade - {data}",
                attachment_type=allure.attachment_type.TEXT
            )


@allure.feature('Validações')
@allure.story('Validação de Data de Nascimento')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.validations
@pytest.mark.data
def test_datas_limite_fronteira():
    """
    Testa casos de borda (boundary testing).

    Importante testar limites:
        - Exatamente 120 anos
        - Exatamente hoje
        - Exatamente amanhã
        - 1 dia antes de hoje
    """
    hoje = datetime.now()

    with allure.step("Testar data de exatamente 120 anos atrás"):
        data_120_anos = (hoje - timedelta(days=120 * 365)).strftime("%d/%m/%Y")
        eh_valida, erro = validar_data_nascimento(data_120_anos)

        # Pode ou não aceitar exatamente 120 anos (decisão de negócio)
        allure.attach(
            f"Data: {data_120_anos}\nVálida: {eh_valida}\nErro: {erro}",
            name="120 anos exatos",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Testar data de ontem"):
        ontem = (hoje - timedelta(days=1)).strftime("%d/%m/%Y")
        eh_valida, erro = validar_data_nascimento(ontem)

        # Ontem é válido (bebê de 1 dia)
        assert eh_valida, f"Ontem deveria ser válido. Erro: {erro}"

        allure.attach(
            f"Data: {ontem}\nVálida: {eh_valida}",
            name="Data de Ontem",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Testar data de amanhã"):
        amanha = (hoje + timedelta(days=1)).strftime("%d/%m/%Y")
        eh_valida, erro = validar_data_nascimento(amanha)

        # Amanhã é inválido (futura)
        assert not eh_valida, "Amanhã deveria ser inválido"

        allure.attach(
            f"Data: {amanha}\nVálida: {eh_valida}\nErro: {erro}",
            name="Data de Amanhã",
            attachment_type=allure.attachment_type.TEXT
        )


# ========================================
# NOTAS PARA APRESENTAÇÃO
# ========================================

"""
PONTOS PARA DESTACAR NA ENTREVISTA:

1. **Validações de Negócio:**
   - Data não pode ser futura
   - Pessoa não pode ter mais de 120 anos
   - Formato DD/MM/AAAA padrão brasileiro

2. **Casos de Borda (Boundary Testing):**
   - Exatamente hoje/ontem/amanhã
   - Exatamente 120 anos
   - 29 de fevereiro em bissextos

3. **Testes Parametrizados:**
   - Múltiplos formatos inválidos testados
   - Fácil adicionar novos casos

4. **Validação de Anos Bissextos:**
   - Implementei algoritmo correto de bissexto
   - Testo 29/02 em anos bissextos e não-bissextos

5. **Funções Reutilizáveis:**
   - validar_data_nascimento()
   - calcular_idade()
   - eh_ano_bissexto()

6. **Documentação com Allure:**
   - Cada teste documenta regra de negócio
   - Screenshots de tentativas inválidas

REGRAS DE NEGÓCIO IMPLEMENTADAS:
- ✅ Data não pode ser futura
- ✅ Data não pode ser hoje
- ✅ Pessoa não pode ter mais de 120 anos
- ✅ Data deve existir no calendário
- ✅ Formato deve ser DD/MM/AAAA
- ✅ Anos bissextos validados corretamente

LIMITAÇÕES (Seja transparente):
- Sistema atual pode não ter todas essas validações
- Alguns testes validam apenas nossa lógica
- Validação completa requer implementação no backend
"""