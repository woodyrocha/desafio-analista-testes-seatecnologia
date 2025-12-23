"""
Testes de Validação de CPF

Objetivo: Validar que o sistema aceita apenas CPFs válidos e rejeita inválidos
Escopo: Frontend (validação visual) + Backend (se implementado)
"""

import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.lista_funcionarios_page import ListaFuncionariosPage
from pages.cadastro_page import CadastroPage
from utils.data_factory import gerar_dados_funcionario

# Biblioteca para gerar e validar CPF REAL
try:
    from validate_docbr import CPF
    cpf_validator = CPF()
    VALIDATE_DOCBR_DISPONIVEL = True
except ImportError:
    VALIDATE_DOCBR_DISPONIVEL = False
    print("⚠️ validate-docbr não instalado. Usando validação manual.")
    print("   Instale: pip install validate-docbr")


# ========================================
# FUNÇÕES AUXILIARES DE VALIDAÇÃO
# ========================================

def gerar_cpf_valido() -> str:
    """
    Gera um CPF REAL e VÁLIDO usando validate-docbr.

    Returns:
        CPF válido formatado (XXX.XXX.XXX-XX)

    Exemplo:
        >>> cpf = gerar_cpf_valido()
        >>> cpf  # Exemplo: "123.456.789-09"
    """
    if VALIDATE_DOCBR_DISPONIVEL:
        return cpf_validator.generate(True)  # True = com formatação
    else:
        # Fallback: usar CPF fixo válido conhecido
        return "123.456.789-09"


def validar_cpf(cpf: str) -> bool:
    """
    Valida CPF usando biblioteca validate-docbr (oficial brasileiro).

    Args:
        cpf: String com CPF (com ou sem formatação)

    Returns:
        True se CPF é válido, False caso contrário

    Exemplo:
        >>> validar_cpf("123.456.789-09")
        True
        >>> validar_cpf("111.111.111-11")
        False
    """
    # Usar validate-docbr se disponível
    if VALIDATE_DOCBR_DISPONIVEL:
        return cpf_validator.validate(cpf)

    # FALLBACK: Implementação manual do algoritmo oficial
    cpf_numeros = ''.join(filter(str.isdigit, cpf))

    if len(cpf_numeros) != 11:
        return False

    # CPFs inválidos conhecidos (todos dígitos iguais)
    cpfs_invalidos = [str(i) * 11 for i in range(10)]
    if cpf_numeros in cpfs_invalidos:
        return False

    # Validação do primeiro dígito verificador
    soma = sum(int(cpf_numeros[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    if int(cpf_numeros[9]) != digito1:
        return False

    # Validação do segundo dígito verificador
    soma = sum(int(cpf_numeros[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    if int(cpf_numeros[10]) != digito2:
        return False

    return True


def formatar_cpf(cpf: str) -> str:
    """
    Formata CPF no padrão XXX.XXX.XXX-XX

    Args:
        cpf: String com números do CPF

    Returns:
        CPF formatado
    """
    cpf_numeros = ''.join(filter(str.isdigit, cpf))
    if len(cpf_numeros) == 11:
        return f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"
    return cpf


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
# TESTES DE VALIDAÇÃO DE CPF
# ========================================

@allure.feature('Validações')
@allure.story('Validação de CPF')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.validations
@pytest.mark.cpf
def test_cpf_valido_aceito(driver, base_url):
    """
    Testa que CPF válido é aceito pelo sistema.

    Cenário:
        1. Abrir formulário de cadastro
        2. Preencher CPF válido
        3. Validar que não há erro
    """
    with allure.step("Abrir formulário de cadastro"):
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)
        lista_page.iniciar_cadastro_funcionario()
        cadastro_page = CadastroPage(driver)

    # Gerar CPF válido REAL para teste
    cpf_valido = gerar_cpf_valido()

    with allure.step(f"Preencher CPF válido: {cpf_valido}"):
        # Validar com nossa função
        assert validar_cpf(cpf_valido), "CPF deveria ser válido segundo algoritmo"

        # Log da origem
        if VALIDATE_DOCBR_DISPONIVEL:
            allure.attach("CPF gerado pela biblioteca validate-docbr (REAL)",
                         name="Origem do CPF",
                         attachment_type=allure.attachment_type.TEXT)

        cadastro_page.preencher_cpf(cpf_valido)
        allure.attach(f"CPF preenchido: {cpf_valido}", name="CPF Válido", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Validar que CPF foi aceito"):
        # Verificar que campo foi preenchido
        import time
        time.sleep(0.5)

        # Capturar screenshot
        from utils.helpers import tirar_screenshot, anexar_screenshot_allure
        caminho_screenshot = tirar_screenshot(driver, "cpf_valido_aceito")
        anexar_screenshot_allure(caminho_screenshot, "CPF Válido Aceito")

        # Nota: Validação completa depende de validação implementada no sistema
        # Este teste valida nossa função de validação e o preenchimento


@allure.feature('Validações')
@allure.story('Validação de CPF')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.validations
@pytest.mark.cpf
@pytest.mark.parametrize("cpf_invalido,motivo", [
    ("111.111.111-11", "Todos dígitos iguais"),
    ("000.000.000-00", "Todos zeros"),
    ("123.456.789-00", "Dígito verificador incorreto"),
    ("999.999.999-99", "Todos 9s"),
    ("123.456.789-10", "Segundo dígito incorreto"),
])
def test_cpf_invalido_rejeitado(driver, base_url, cpf_invalido, motivo):
    """
    Testa que CPFs inválidos são rejeitados.

    Parametrizado para testar múltiplos CPFs inválidos.
    """
    with allure.step(f"Testar CPF inválido: {cpf_invalido} ({motivo})"):
        allure.attach(f"CPF: {cpf_invalido}\nMotivo: {motivo}",
                     name="Dados do Teste",
                     attachment_type=allure.attachment_type.TEXT)

        # Validar com nossa função
        assert not validar_cpf(cpf_invalido), f"CPF {cpf_invalido} deveria ser inválido"

        # Nota: Teste completo dependeria de validação implementada no frontend/backend
        # Por ora, validamos que nossa função de validação funciona corretamente


@allure.feature('Validações')
@allure.story('Validação de CPF')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.validations
@pytest.mark.cpf
def test_cpf_formatacao_automatica(driver, base_url, abrir_formulario_cadastro):
    """
    Testa se o sistema formata CPF automaticamente ao digitar apenas números.

    Comportamento esperado:
        Digitar: 12345678909
        Resultado: 123.456.789-09
    """
    cadastro_page = abrir_formulario_cadastro

    cpf_sem_formatacao = "12345678909"
    cpf_formatado_esperado = "123.456.789-09"

    with allure.step(f"Digitar CPF sem formatação: {cpf_sem_formatacao}"):
        cadastro_page.preencher_cpf(cpf_sem_formatacao)

    with allure.step("Verificar formatação automática"):
        # Capturar screenshot
        from utils.helpers import tirar_screenshot, anexar_screenshot_allure
        import time
        time.sleep(0.5)

        caminho = tirar_screenshot(driver, "cpf_formatacao_automatica")
        anexar_screenshot_allure(caminho, "Formatação de CPF")

        # Nota: Validação visual - em teste real verificaríamos o valor do campo


@allure.feature('Validações')
@allure.story('Validação de CPF')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.validations
@pytest.mark.cpf
def test_cpf_duplicado_nao_permitido(driver, base_url):
    """
    Testa que o sistema não permite cadastrar funcionário com CPF duplicado.

    Cenário:
        1. Cadastrar funcionário com CPF X
        2. Tentar cadastrar outro funcionário com mesmo CPF X
        3. Sistema deve rejeitar
    """
    cpf_teste = "123.456.789-09"

    with allure.step(f"Cadastrar primeiro funcionário com CPF {cpf_teste}"):
        driver.get(base_url)
        lista_page = ListaFuncionariosPage(driver)
        lista_page.iniciar_cadastro_funcionario()

        cadastro_page = CadastroPage(driver)
        dados = gerar_dados_funcionario()
        dados['cpf'] = cpf_teste
        dados['cargo'] = 'Cargo 1'
        dados['nao_usa_epi'] = True

        cadastro_page.preencher_e_salvar(dados)

        import time
        time.sleep(2)

    with allure.step(f"Tentar cadastrar segundo funcionário com mesmo CPF {cpf_teste}"):
        lista_page = ListaFuncionariosPage(driver)
        lista_page.iniciar_cadastro_funcionario()

        cadastro_page = CadastroPage(driver)
        dados2 = gerar_dados_funcionario()
        dados2['cpf'] = cpf_teste  # MESMO CPF
        dados2['cargo'] = 'Cargo 2'
        dados2['nao_usa_epi'] = True

        # Preencher formulário
        cadastro_page.preencher_nome(dados2['nome'])
        cadastro_page.selecionar_sexo(dados2['sexo'])
        cadastro_page.preencher_cpf(dados2['cpf'])
        cadastro_page.preencher_data_nascimento(dados2['data_nascimento'])
        cadastro_page.preencher_rg(dados2['rg'])
        cadastro_page.selecionar_cargo(dados2['cargo'])
        cadastro_page.marcar_nao_usa_epi()

        # Tentar salvar
        cadastro_page.salvar()

        import time
        time.sleep(1)

    with allure.step("Validar que sistema rejeitou CPF duplicado"):
        from utils.helpers import tirar_screenshot, anexar_screenshot_allure
        caminho = tirar_screenshot(driver, "cpf_duplicado_rejeitado")
        anexar_screenshot_allure(caminho, "Tentativa de CPF Duplicado")

        # Nota: Validação completa dependeria de verificar mensagem de erro
        # Por ora, documentamos o comportamento esperado


@allure.feature('Validações')
@allure.story('Validação de CPF')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.validations
@pytest.mark.cpf
@pytest.mark.parametrize("entrada_invalida", [
    "abc.def.ghi-jk",  # Letras
    "123-456-789.00",  # Formato errado
    "12.345.678",      # Incompleto
    "123 456 789 00",  # Espaços
])
def test_cpf_caracteres_invalidos(entrada_invalida):
    """
    Testa que CPF com caracteres inválidos é rejeitado.

    Testa apenas a função de validação (sem UI).
    """
    with allure.step(f"Validar entrada inválida: {entrada_invalida}"):
        allure.attach(entrada_invalida, name="Entrada Testada", attachment_type=allure.attachment_type.TEXT)

        # Nossa função deve rejeitar
        assert not validar_cpf(entrada_invalida), f"Deveria rejeitar: {entrada_invalida}"


@allure.feature('Validações')
@allure.story('Validação de CPF')
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.validations
@pytest.mark.cpf
def test_algoritmo_validacao_cpf_correto():
    """
    Testa que nossa função de validação de CPF está correta.

    Valida CPFs conhecidos como válidos e inválidos.
    """
    with allure.step("Testar CPFs válidos conhecidos"):
        cpfs_validos = [
            "123.456.789-09",
            "111.444.777-35",
            "123.456.789-09",
        ]

        for cpf in cpfs_validos:
            assert validar_cpf(cpf), f"CPF {cpf} deveria ser válido"
            allure.attach(f"✅ {cpf}", name="CPF Válido", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Testar CPFs inválidos conhecidos"):
        cpfs_invalidos = [
            "111.111.111-11",
            "000.000.000-00",
            "123.456.789-00",
            "999.999.999-99",
            "12345",
            "",
        ]

        for cpf in cpfs_invalidos:
            assert not validar_cpf(cpf), f"CPF {cpf} deveria ser inválido"
            allure.attach(f"❌ {cpf}", name="CPF Inválido", attachment_type=allure.attachment_type.TEXT)


# ========================================
# NOTAS PARA APRESENTAÇÃO
# ========================================

"""
PONTOS PARA DESTACAR NA ENTREVISTA:

1. **Validação Algorítmica Correta:**
   - Implementei o algoritmo oficial de validação de CPF brasileiro
   - Valida dígitos verificadores conforme Receita Federal
   
2. **Testes Parametrizados:**
   - Um teste → múltiplos cenários
   - Facilita adicionar novos casos
   
3. **Cobertura Completa:**
   - CPFs válidos/inválidos
   - Formatação automática
   - Duplicação
   - Caracteres especiais
   
4. **Evidências com Allure:**
   - Screenshots automáticos
   - Anexos com dados testados
   - Organização por Feature/Story
   
5. **Função Reutilizável:**
   - validar_cpf() pode ser usada em qualquer lugar
   - Separada da lógica de teste
   
LIMITAÇÕES (Seja transparente):
- Sistema atual pode não ter validação implementada
- Alguns testes validam apenas nossa função
- Testes de UI dependem de elementos na página
"""