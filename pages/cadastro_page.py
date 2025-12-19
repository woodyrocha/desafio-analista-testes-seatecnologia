"""
Page Object para a tela de cadastro de funcionário.

Contém todos os elementos e ações relacionadas ao formulário de cadastro.
"""

import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.helpers import (
    clicar_com_espera,
    limpar_e_preencher,
    esperar_elemento_visivel,
    anexar_screenshot_allure,
    selecionar_dropdown_por_texto
)


class CadastroPage(BasePage):
    """Page Object para cadastro de funcionário."""

    # ===== SELETORES XPATH REAIS =====

    # Navegação
    BOTAO_VOLTAR = (By.XPATH, "/html/body/div/main/div[2]/div[2]/form/div[1]/button")

    # Toggle Status
    TOGGLE_STATUS = (By.XPATH, "/html/body/div/main/div[2]/div[2]/form/div[2]/button")

    # Dados Básicos
    CAMPO_NOME = (By.XPATH, "/html/body/div/main/div[2]/div[2]/form/div[3]/div/div[1]/input")
    RADIO_MASCULINO = (By.XPATH, "/html/body/div/main/div[2]/div[2]/form/div[3]/div/div[2]/div/label[1]")
    RADIO_FEMININO = (By.XPATH, "/html/body/div/main/div[2]/div[2]/form/div[3]/div/div[2]/div/label[2]")
    CAMPO_CPF = (By.XPATH, "/html/body/div/main/div[2]/div[2]/form/div[3]/div/div[3]/input")
    CAMPO_DATA_NASCIMENTO = (By.XPATH, "/html/body/div/main/div[2]/div[2]/form/div[3]/div/div[4]/input")
    CAMPO_RG = (By.XPATH, "/html/body/div/main/div[2]/div[2]/form/div[3]/div/div[5]/input")
    DROPDOWN_CARGO = (By.XPATH, "/html/body/div/main/div[2]/div[2]/form/div[3]/div/div[6]/div/div")

    # EPIs e Atividades
    CHECKBOX_NAO_USA_EPI = (By.XPATH, "/html/body/div/main/div[2]/div[2]/form/div[4]/div/label/span[1]/input")
    DROPDOWN_ATIVIDADE = (By.XPATH, "/html/body/div/main/div[2]/div[2]/form/div[4]/div/div/div[1]/div/div")
    DROPDOWN_EPI = (By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/form/div[4]/div/div/div[2]/div/div[1]/div")
    CAMPO_NUMERO_CA = (By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/form/div[4]/div/div/div[2]/div/div[2]/input")
    BOTAO_ADICIONAR_EPI = (By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/form/div[4]/div/div/div[2]/span")
    BOTAO_ADICIONAR_ATIVIDADE = (By.XPATH, "/html/body/div/main/div[2]/div[2]/form/div[4]/div/button")

    # Upload
    INPUT_ARQUIVO = (By.ID, "file")
    BOTAO_SELECIONAR_ARQUIVO = (By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/form/div[5]/div/label")

    # Ações Finais
    BOTAO_SALVAR = (By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/form/button")

    # ===== MÉTODOS DE INTERAÇÃO =====

    @allure.step("Voltar para listagem")
    def clicar_voltar(self):
        """Clica no botão voltar."""
        clicar_com_espera(self.driver, *self.BOTAO_VOLTAR)

    @allure.step("Alternar status do funcionário")
    def alternar_status(self):
        """Alterna o toggle de status (Ativo/Inativo)."""
        clicar_com_espera(self.driver, *self.TOGGLE_STATUS)

    @allure.step("Preencher nome: {nome}")
    def preencher_nome(self, nome: str):
        """Preenche o campo nome."""
        limpar_e_preencher(self.driver, *self.CAMPO_NOME, nome)

    @allure.step("Selecionar sexo: {sexo}")
    def selecionar_sexo(self, sexo: str):
        """
        Seleciona o sexo do funcionário.

        Args:
            sexo: 'M' para Masculino, 'F' para Feminino
        """
        if sexo.upper() == 'M':
            clicar_com_espera(self.driver, *self.RADIO_MASCULINO)
        elif sexo.upper() == 'F':
            clicar_com_espera(self.driver, *self.RADIO_FEMININO)
        else:
            raise ValueError(f"Sexo inválido: {sexo}. Use 'M' ou 'F'.")

    @allure.step("Preencher CPF: {cpf}")
    def preencher_cpf(self, cpf: str):
        """Preenche o campo CPF."""
        limpar_e_preencher(self.driver, *self.CAMPO_CPF, cpf)

    @allure.step("Preencher data de nascimento: {data}")
    def preencher_data_nascimento(self, data: str):
        """
        Preenche a data de nascimento.

        Args:
            data: Data no formato DD/MM/AAAA
        """
        limpar_e_preencher(self.driver, *self.CAMPO_DATA_NASCIMENTO, data)

    @allure.step("Preencher RG: {rg}")
    def preencher_rg(self, rg: str):
        """Preenche o campo RG."""
        limpar_e_preencher(self.driver, *self.CAMPO_RG, rg)

    @allure.step("Selecionar cargo: {cargo}")
    def selecionar_cargo(self, cargo: str):
        """
        Seleciona um cargo no dropdown.

        Args:
            cargo: Texto do cargo (ex: "Cargo 1", "Cargo 2", etc)
        """
        from utils.helpers import selecionar_dropdown_por_teclas

        # Mapear texto para número da opção
        mapa_cargos = {
            "Cargo 1": 1,
            "Cargo 2": 2,
            "Cargo 3": 3,
            "Cargo 4": 4,
            "Cargo 5": 5,
        }

        numero_opcao = mapa_cargos.get(cargo)
        if not numero_opcao:
            raise ValueError(f"Cargo inválido: {cargo}. Use 'Cargo 1' até 'Cargo 5'.")

        selecionar_dropdown_por_teclas(
            self.driver,
            self.DROPDOWN_CARGO[1],  # XPATH do dropdown
            numero_opcao
        )

    @allure.step("Marcar 'Não usa EPI'")
    def marcar_nao_usa_epi(self):
        """Marca o checkbox 'O trabalhador não usa EPI'."""
        clicar_com_espera(self.driver, *self.CHECKBOX_NAO_USA_EPI)

    @allure.step("Selecionar atividade: {atividade}")
    def selecionar_atividade(self, atividade: str):
        """Seleciona uma atividade no dropdown."""
        selecionar_dropdown_por_texto(self.driver, self.DROPDOWN_ATIVIDADE[1], atividade)

    @allure.step("Selecionar EPI: {epi}")
    def selecionar_epi(self, epi: str):
        """Seleciona um EPI no dropdown."""
        selecionar_dropdown_por_texto(self.driver, self.DROPDOWN_EPI[1], epi)

    @allure.step("Preencher número do CA: {numero_ca}")
    def preencher_numero_ca(self, numero_ca: str):
        """Preenche o número do CA (Certificado de Aprovação)."""
        limpar_e_preencher(self.driver, *self.CAMPO_NUMERO_CA, numero_ca)

    @allure.step("Clicar em 'Adicionar EPI'")
    def clicar_adicionar_epi(self):
        """
        Clica no botão 'Adicionar EPI'.

        ATENÇÃO: Bug conhecido - elemento é span clicável mas sem ação configurada.
        """
        clicar_com_espera(self.driver, *self.BOTAO_ADICIONAR_EPI)

    @allure.step("Clicar em 'Adicionar outra atividade'")
    def clicar_adicionar_atividade(self):
        """
        Clica no botão 'Adicionar outra atividade'.

        ATENÇÃO: Bug conhecido - botão tem ação de 'Voltar' ao invés de adicionar atividade.
        """
        clicar_com_espera(self.driver, *self.BOTAO_ADICIONAR_ATIVIDADE)

    @allure.step("Fazer upload de arquivo: {caminho_arquivo}")
    def fazer_upload_arquivo(self, caminho_arquivo: str):
        """
        Faz upload de um arquivo (Atestado de Saúde).

        Args:
            caminho_arquivo: Caminho completo do arquivo a fazer upload
        """
        input_element = esperar_elemento_visivel(self.driver, *self.INPUT_ARQUIVO)
        input_element.send_keys(caminho_arquivo)

    @allure.step("Salvar cadastro")
    def salvar(self):
        """Clica no botão Salvar."""
        anexar_screenshot_allure(self.driver, "Antes de salvar")
        clicar_com_espera(self.driver, *self.BOTAO_SALVAR)

    # ===== MÉTODOS COMPOSTOS =====

    @allure.step("Preencher formulário completo")
    def preencher_formulario_completo(self, dados: dict):
        """
        Preenche todo o formulário de cadastro com os dados fornecidos.

        Args:
            dados: Dicionário com os dados do funcionário
                - nome (str): Nome completo
                - sexo (str): 'M' ou 'F'
                - cpf (str): CPF formatado ou não
                - data_nascimento (str): Data no formato DD/MM/AAAA
                - rg (str, opcional): RG
                - cargo (str): Cargo do funcionário
                - atividade (str, opcional): Atividade realizada
                - epi (str, opcional): EPI utilizado
                - numero_ca (str, opcional): Número do CA
                - arquivo (str, opcional): Caminho do arquivo para upload
        """
        # Dados básicos obrigatórios
        self.preencher_nome(dados.get("nome"))
        self.selecionar_sexo(dados.get("sexo"))
        self.preencher_cpf(dados.get("cpf"))
        self.preencher_data_nascimento(dados.get("data_nascimento"))

        # RG (opcional)
        if dados.get("rg"):
            self.preencher_rg(dados["rg"])

        # Cargo
        self.selecionar_cargo(dados.get("cargo"))

        # EPI e Atividades (opcional)
        if dados.get("atividade") and dados.get("epi"):
            self.selecionar_atividade(dados["atividade"])
            self.selecionar_epi(dados["epi"])

            if dados.get("numero_ca"):
                self.preencher_numero_ca(dados["numero_ca"])
        elif dados.get("nao_usa_epi"):
            self.marcar_nao_usa_epi()

        # Upload de arquivo (opcional)
        if dados.get("arquivo"):
            self.fazer_upload_arquivo(dados["arquivo"])

    @allure.step("Preencher e salvar formulário")
    def preencher_e_salvar(self, dados: dict):
        """
        Preenche o formulário completo e salva.

        Args:
            dados: Dicionário com os dados do funcionário
        """
        self.preencher_formulario_completo(dados)
        self.salvar()