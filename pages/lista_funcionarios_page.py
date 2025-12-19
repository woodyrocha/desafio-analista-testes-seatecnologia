"""
Page Object para a tela de listagem de funcionários.

Contém todos os elementos e ações relacionadas à visualização,
filtro e gerenciamento de funcionários cadastrados.
"""

import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.helpers import (
    clicar_com_espera,
    esperar_elemento_visivel,
    elemento_existe,
    obter_texto_elemento,
    anexar_screenshot_allure,
    contar_elementos
)


class ListaFuncionariosPage(BasePage):
    """Page Object para listagem de funcionários."""

    # ===== SELETORES XPATH REAIS =====

    # Menu Lateral
    ICONE_MENU_1 = (By.XPATH, "/html/body/div/main/div[1]/div[2]/div[1]")
    ICONE_MENU_2 = (By.XPATH, "/html/body/div/main/div[1]/div[2]/div[2]")
    ICONE_MENU_3 = (By.XPATH, "/html/body/div/main/div[1]/div[2]/div[3]")
    ICONE_MENU_4 = (By.XPATH, "/html/body/div/main/div[1]/div[2]/div[4]")
    ICONE_MENU_5 = (By.XPATH, "/html/body/div/main/div[1]/div[2]/div[5]")
    ICONE_MENU_6 = (By.XPATH, "/html/body/div/main/div[1]/div[2]/div[6]")

    # Barra Superior e Ações
    BOTAO_ADICIONAR_FUNCIONARIO = (By.XPATH, "/html/body/div/main/div[2]/div[2]/div[2]/button")

    # Filtros
    BOTAO_VER_APENAS_ATIVOS = (By.XPATH, "/html/body/div/main/div[2]/div[2]/div[2]/div[1]/button[1]")
    BOTAO_LIMPAR_FILTROS = (By.XPATH, "/html/body/div/main/div[2]/div[2]/div[2]/div[1]/button[2]")

    # Card de Funcionário (PRIMEIRO DA LISTA)
    CARD_CONTAINER = (By.XPATH, "/html/body/div/main/div[2]/div[2]/div[2]")
    CARD_NOME = (By.XPATH, "/html/body/div/main/div[2]/div[2]/div[2]/div[2]/div/div[1]/span")
    CARD_CPF = (By.XPATH, "/html/body/div/main/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[1]")
    CARD_STATUS = (By.XPATH, "/html/body/div/main/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[2]")
    CARD_CARGO = (By.XPATH, "/html/body/div/main/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[3]")
    CARD_MENU_TRES_PONTOS = (By.XPATH, "/html/body/div/main/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[2]")

    # Footer
    BOTAO_ETAPA_CONCLUIDA = (By.XPATH, "/html/body/div/main/div[2]/div[2]/div[2]/div[3]/button")
    BOTAO_PROXIMO_PASSO = (By.XPATH, "/html/body/div/main/div[2]/div[3]/button")

    # Seletores genéricos para múltiplos cards (usando contains)
    TODOS_CARDS_XPATH = "//div[contains(@class, 'card')]"  # Ajustar conforme estrutura real

    # ===== MÉTODOS DE NAVEGAÇÃO =====

    @allure.step("Clicar no botão 'Adicionar Funcionário'")
    def clicar_adicionar_funcionario(self):
        """Clica no botão para adicionar novo funcionário."""
        anexar_screenshot_allure(self.driver, "Tela de listagem")
        clicar_com_espera(self.driver, *self.BOTAO_ADICIONAR_FUNCIONARIO)

    @allure.step("Clicar no ícone {numero} do menu lateral")
    def clicar_icone_menu(self, numero: int):
        """
        Clica em um dos ícones do menu lateral.

        Args:
            numero: Número do ícone (1-6)

        ATENÇÃO: Bug conhecido - ícones são clicáveis mas não têm ação configurada.
        """
        icones = {
            1: self.ICONE_MENU_1,
            2: self.ICONE_MENU_2,
            3: self.ICONE_MENU_3,
            4: self.ICONE_MENU_4,
            5: self.ICONE_MENU_5,
            6: self.ICONE_MENU_6
        }

        if numero not in icones:
            raise ValueError(f"Número de ícone inválido: {numero}. Use 1-6.")

        clicar_com_espera(self.driver, *icones[numero])

    # ===== MÉTODOS DE FILTRO =====

    @allure.step("Clicar em 'Ver apenas ativos'")
    def filtrar_apenas_ativos(self):
        """Clica no botão para filtrar apenas funcionários ativos."""
        clicar_com_espera(self.driver, *self.BOTAO_VER_APENAS_ATIVOS)

    @allure.step("Clicar em 'Limpar filtros'")
    def limpar_filtros(self):
        """Clica no botão para limpar todos os filtros aplicados."""
        clicar_com_espera(self.driver, *self.BOTAO_LIMPAR_FILTROS)

    # ===== MÉTODOS DE LEITURA DE DADOS =====

    @allure.step("Obter nome do primeiro funcionário")
    def obter_nome_primeiro_funcionario(self) -> str:
        """
        Obtém o nome do primeiro funcionário da lista.

        Returns:
            str: Nome do funcionário
        """
        return obter_texto_elemento(self.driver, *self.CARD_NOME)

    @allure.step("Obter CPF do primeiro funcionário")
    def obter_cpf_primeiro_funcionario(self) -> str:
        """
        Obtém o CPF do primeiro funcionário da lista.

        Returns:
            str: CPF do funcionário
        """
        return obter_texto_elemento(self.driver, *self.CARD_CPF)

    @allure.step("Obter status do primeiro funcionário")
    def obter_status_primeiro_funcionario(self) -> str:
        """
        Obtém o status do primeiro funcionário.

        Returns:
            str: Status (Ativo/Inativo)

        ATENÇÃO: Bug conhecido - este elemento mostra Atividade no lugar do Status.
        """
        return obter_texto_elemento(self.driver, *self.CARD_STATUS)

    @allure.step("Obter cargo do primeiro funcionário")
    def obter_cargo_primeiro_funcionario(self) -> str:
        """
        Obtém o cargo do primeiro funcionário.

        Returns:
            str: Cargo do funcionário
        """
        return obter_texto_elemento(self.driver, *self.CARD_CARGO)

    @allure.step("Verificar se funcionário existe na lista")
    def funcionario_existe(self, nome: str) -> bool:
        """
        Verifica se um funcionário com o nome especificado existe na lista.

        Args:
            nome: Nome do funcionário a buscar

        Returns:
            bool: True se funcionário existe, False caso contrário
        """
        xpath = f"//span[contains(text(), '{nome}')]"
        return elemento_existe(self.driver, By.XPATH, xpath, timeout=5)

    @allure.step("Contar funcionários na lista")
    def contar_funcionarios(self) -> int:
        """
        Conta o número de funcionários visíveis na lista.

        Returns:
            int: Número de funcionários

        NOTA: Pode não contar todos se houver scroll necessário.
        """
        # Este seletor precisa ser ajustado conforme a estrutura real
        return contar_elementos(self.driver, By.XPATH, self.TODOS_CARDS_XPATH)

    # ===== MÉTODOS DE AÇÃO NO CARD =====

    @allure.step("Clicar no menu '...' do primeiro funcionário")
    def clicar_menu_tres_pontos(self):
        """
        Clica no menu "..." (três pontos) do primeiro funcionário.

        ATENÇÃO: Bug conhecido - elemento é clicável mas não abre menu.
        """
        clicar_com_espera(self.driver, *self.CARD_MENU_TRES_PONTOS)

    # ===== MÉTODOS DE FOOTER =====

    @allure.step("Marcar etapa como concluída")
    def marcar_etapa_concluida(self):
        """Clica no botão para marcar a etapa como concluída."""
        clicar_com_espera(self.driver, *self.BOTAO_ETAPA_CONCLUIDA)

    @allure.step("Clicar em 'Próximo passo'")
    def clicar_proximo_passo(self):
        """
        Clica no botão 'Próximo passo'.

        ATENÇÃO: Bug conhecido - botão existe mas não tem ação configurada.
        """
        clicar_com_espera(self.driver, *self.BOTAO_PROXIMO_PASSO)

    # ===== MÉTODOS DE VALIDAÇÃO =====

    @allure.step("Validar que funcionário foi cadastrado")
    def validar_funcionario_cadastrado(self, nome: str, cpf: str = None) -> bool:
        """
        Valida que um funcionário foi cadastrado com sucesso.

        Args:
            nome: Nome do funcionário
            cpf: CPF do funcionário (opcional)

        Returns:
            bool: True se funcionário foi encontrado
        """
        funcionario_existe = self.funcionario_existe(nome)

        if funcionario_existe:
            allure.attach(
                f"Funcionário '{nome}' encontrado na lista",
                name="Validação de Cadastro",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"Funcionário '{nome}' NÃO encontrado na lista",
                name="Validação de Cadastro - FALHOU",
                attachment_type=allure.attachment_type.TEXT
            )

        anexar_screenshot_allure(self.driver, "Lista após cadastro")
        return funcionario_existe

    @allure.step("Verificar componente 'Em breve' está visível")
    def verificar_componente_em_breve_visivel(self) -> bool:
        """
        Verifica se o componente "Em breve" está visível na tela.

        Returns:
            bool: True se componente está visível

        NOTA: Seletor precisa ser ajustado quando componente for implementado.
        """
        # Este seletor precisa ser definido quando o componente existir
        xpath_em_breve = "//div[contains(text(), 'Em breve')]"
        return elemento_existe(self.driver, By.XPATH, xpath_em_breve, timeout=3)

    # ===== MÉTODOS COMPOSTOS =====

    @allure.step("Fluxo: Adicionar novo funcionário")
    def iniciar_cadastro_funcionario(self):
        """
        Fluxo completo para iniciar o cadastro de um novo funcionário.

        - Acessa a tela de listagem
        - Clica em 'Adicionar Funcionário'
        - Aguarda carregamento do formulário
        """
        self.clicar_adicionar_funcionario()
        # Aguardar transição para tela de cadastro
        import time
        time.sleep(1)