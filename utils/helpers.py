"""
Funções auxiliares para testes automatizados.

Este módulo contém funções utilitárias para facilitar a escrita de testes,
incluindo waits, screenshots, validações e manipulação de elementos.
"""

import os
import time
import allure
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def tirar_screenshot(driver, nome: str, path: str = "evidence/screenshots"):
    """
    Captura um screenshot e salva no diretório especificado.

    Args:
        driver: Instância do WebDriver
        nome: Nome do arquivo (sem extensão)
        path: Diretório onde salvar (padrão: evidence/screenshots)

    Returns:
        str: Caminho completo do arquivo salvo
    """
    os.makedirs(path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{nome}_{timestamp}.png"
    filepath = os.path.join(path, filename)

    driver.save_screenshot(filepath)
    return filepath


def anexar_screenshot_allure(driver_ou_caminho, nome: str = "Screenshot"):
    """
    Captura screenshot e anexa ao relatório Allure.

    **CORREÇÃO:** Agora aceita DRIVER ou CAMINHO de arquivo.

    Args:
        driver_ou_caminho: Instância do WebDriver OU caminho do arquivo (str)
        nome: Nome do anexo no Allure

    Exemplo:
        # Opção 1: Passar driver
        anexar_screenshot_allure(driver, "Tela")

        # Opção 2: Passar caminho
        caminho = tirar_screenshot(driver, "teste")
        anexar_screenshot_allure(caminho, "Tela")
    """
    # Se é string, é caminho de arquivo
    if isinstance(driver_ou_caminho, str):
        with open(driver_ou_caminho, 'rb') as f:
            screenshot = f.read()
    else:
        # Se não, é o driver
        screenshot = driver_ou_caminho.get_screenshot_as_png()

    allure.attach(
        screenshot,
        name=nome,
        attachment_type=allure.attachment_type.PNG
    )


def esperar_elemento_visivel(driver, by, value, timeout=10):
    """
    Aguarda até que um elemento esteja visível na página.

    Args:
        driver: Instância do WebDriver
        by: Tipo de seletor (By.XPATH, By.ID, etc)
        value: Valor do seletor
        timeout: Tempo máximo de espera em segundos

    Returns:
        WebElement: Elemento encontrado

    Raises:
        TimeoutException: Se elemento não aparecer no tempo especificado
    """
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )


def esperar_elemento_clicavel(driver, by, value, timeout=10):
    """
    Aguarda até que um elemento esteja clicável.

    Args:
        driver: Instância do WebDriver
        by: Tipo de seletor
        value: Valor do seletor
        timeout: Tempo máximo de espera em segundos

    Returns:
        WebElement: Elemento clicável
    """
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )


def esperar_elemento_presente(driver, by, value, timeout=10):
    """
    Aguarda até que um elemento esteja presente no DOM.

    Args:
        driver: Instância do WebDriver
        by: Tipo de seletor
        value: Valor do seletor
        timeout: Tempo máximo de espera em segundos

    Returns:
        WebElement: Elemento encontrado
    """
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def esperar_texto_no_elemento(driver, by, value, texto, timeout=10):
    """
    Aguarda até que um elemento contenha um texto específico.

    Args:
        driver: Instância do WebDriver
        by: Tipo de seletor
        value: Valor do seletor
        texto: Texto esperado
        timeout: Tempo máximo de espera

    Returns:
        bool: True se texto for encontrado
    """
    return WebDriverWait(driver, timeout).until(
        EC.text_to_be_present_in_element((by, value), texto)
    )


def elemento_existe(driver, by, value, timeout=2):
    """
    Verifica se um elemento existe na página.

    Args:
        driver: Instância do WebDriver
        by: Tipo de seletor
        value: Valor do seletor
        timeout: Tempo de espera (padrão: 2s)

    Returns:
        bool: True se elemento existe, False caso contrário
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return True
    except TimeoutException:
        return False


def limpar_e_preencher(driver, by, value, texto, timeout=10):
    """
    Limpa um campo e preenche com novo texto.

    Args:
        driver: Instância do WebDriver
        by: Tipo de seletor
        value: Valor do seletor
        texto: Texto para preencher
        timeout: Tempo máximo de espera
    """
    elemento = esperar_elemento_visivel(driver, by, value, timeout)
    elemento.clear()
    elemento.send_keys(texto)


def clicar_com_espera(driver, by, value, timeout=10):
    """
    Aguarda elemento estar clicável e clica.

    Args:
        driver: Instância do WebDriver
        by: Tipo de seletor
        value: Valor do seletor
        timeout: Tempo máximo de espera
    """
    elemento = esperar_elemento_clicavel(driver, by, value, timeout)
    elemento.click()


def rolar_ate_elemento(driver, elemento):
    """
    Rola a página até o elemento estar visível.

    Args:
        driver: Instância do WebDriver
        elemento: WebElement para rolar até
    """
    driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
    time.sleep(0.3)  # Pequena pausa para garantir que rolou


def obter_texto_elemento(driver, by, value, timeout=10):
    """
    Obtém o texto de um elemento.

    Args:
        driver: Instância do WebDriver
        by: Tipo de seletor
        value: Valor do seletor
        timeout: Tempo máximo de espera

    Returns:
        str: Texto do elemento
    """
    elemento = esperar_elemento_visivel(driver, by, value, timeout)
    return elemento.text


def selecionar_dropdown_por_texto(driver, dropdown_xpath, opcao_texto, timeout=10):
    """
    Seleciona uma opção em um dropdown pelo texto visível.

    Útil para dropdowns customizados que não são <select> padrão.

    Args:
        driver: Instância do WebDriver
        dropdown_xpath: XPATH do dropdown
        opcao_texto: Texto da opção a selecionar
        timeout: Tempo máximo de espera
    """
    # Clica no dropdown para abrir
    clicar_com_espera(driver, By.XPATH, dropdown_xpath, timeout)

    # Aguarda opções aparecerem e clica na desejada
    time.sleep(0.5)
    opcao_xpath = f"//div[contains(text(), '{opcao_texto}')]"
    clicar_com_espera(driver, By.XPATH, opcao_xpath, timeout)


def selecionar_dropdown_por_teclas(driver, dropdown_xpath, numero_opcao, timeout=10, tipo_dropdown="cargo"):
    """
    Seleciona opção em dropdown customizado Ant Design clicando diretamente na opção.

    Suporta dropdowns de: cargo, atividade, epi

    Args:
        driver: Instância do WebDriver
        dropdown_xpath: XPATH do dropdown para clicar
        numero_opcao: Número da opção (0=primeira, 1=segunda, etc)
        timeout: Tempo máximo de espera
        tipo_dropdown: Tipo do dropdown ("cargo", "atividade", "epi")
    """
    import time

    # 1. Clicar no dropdown para abrir
    clicar_com_espera(driver, By.XPATH, dropdown_xpath, timeout)
    time.sleep(0.8)  # Aguardar dropdown abrir e renderizar opções

    # 2. Construir XPATH baseado no tipo de dropdown
    if tipo_dropdown == "cargo":
        # Formato: Cargo 01, Cargo 02, etc
        opcao_xpath = f"//div[contains(@class, 'ant-select-item')][@title='Cargo 0{numero_opcao + 1}']"

    elif tipo_dropdown == "atividade":
        # Formato: Ativid 01, Ativid 02, etc
        opcao_xpath = f"//div[contains(@class, 'ant-select-item')][@title='Ativid 0{numero_opcao + 1}']"

    elif tipo_dropdown == "epi":
        # EPIs têm nomes completos
        mapa_epis = {
            0: "Capacete de segurança",
            1: "Luvas descartáveis",
            2: "Óculos de proteção",
            3: "Calçado de segurança",
            4: "Protetor auditivo"
        }
        nome_epi = mapa_epis.get(numero_opcao)
        if not nome_epi:
            raise ValueError(f"Índice de EPI inválido: {numero_opcao}")

        # Buscar por texto do EPI
        opcao_xpath = f"//div[contains(@class, 'ant-select-item') and contains(text(), '{nome_epi}')]"

    else:
        raise ValueError(f"Tipo de dropdown inválido: {tipo_dropdown}")

    # 3. Clicar na opção
    clicar_com_espera(driver, By.XPATH, opcao_xpath, timeout)
    time.sleep(0.3)


def validar_cpf_formato(cpf: str) -> bool:
    """
    Valida o formato básico de um CPF (XXX.XXX.XXX-XX).

    Args:
        cpf: String do CPF a validar

    Returns:
        bool: True se formato válido
    """
    import re
    # Remove caracteres não numéricos
    cpf_numeros = re.sub(r'[^0-9]', '', cpf)
    return len(cpf_numeros) == 11


def formatar_cpf(cpf: str) -> str:
    """
    Formata um CPF para o padrão XXX.XXX.XXX-XX.

    Args:
        cpf: CPF sem formatação (apenas números)

    Returns:
        str: CPF formatado
    """
    import re
    # Remove tudo que não for número
    cpf_numeros = re.sub(r'[^0-9]', '', cpf)

    # Formata
    if len(cpf_numeros) == 11:
        return f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"
    return cpf_numeros


def aguardar_carregamento(driver, timeout=10):
    """
    Aguarda até que a página esteja completamente carregada.

    Args:
        driver: Instância do WebDriver
        timeout: Tempo máximo de espera
    """
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def anexar_texto_allure(texto: str, nome: str = "Log"):
    """
    Anexa texto ao relatório Allure.

    Args:
        texto: Texto a anexar
        nome: Nome do anexo
    """
    allure.attach(
        texto,
        name=nome,
        attachment_type=allure.attachment_type.TEXT
    )


def step_allure(descricao: str):
    """
    Decorator para marcar steps no Allure Report.

    Usage:
        @step_allure("Preencher formulário")
        def meu_metodo():
            pass
    """
    return allure.step(descricao)


def contar_elementos(driver, by, value, timeout=2):
    """
    Conta quantos elementos correspondem ao seletor.

    Args:
        driver: Instância do WebDriver
        by: Tipo de seletor
        value: Valor do seletor
        timeout: Tempo de espera

    Returns:
        int: Número de elementos encontrados
    """
    try:
        driver.implicitly_wait(timeout)
        elementos = driver.find_elements(by, value)
        return len(elementos)
    except Exception:
        return 0
    finally:
        # Restaura implicit wait padrão
        driver.implicitly_wait(10)