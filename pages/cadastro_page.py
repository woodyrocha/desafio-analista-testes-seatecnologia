from selenium.webdriver.common.by import By
from .base_page import BasePage


class CadastroPage(BasePage):
    """Page object para a tela de cadastro de funcionário."""

    # Exemplo de seletores (ajustar conforme a aplicação)
    NOME = (By.NAME, "nome")
    CPF = (By.NAME, "cpf")
    DATA_NASC = (By.NAME, "data_nascimento")
    BOTAO_SALVAR = (By.CSS_SELECTOR, "button[type=submit]")

    def preencher_formulario(self, dados: dict):
        self.fill(*self.NOME, dados.get("nome", ""))
        self.fill(*self.CPF, dados.get("cpf", ""))
        self.fill(*self.DATA_NASC, dados.get("data_nascimento", ""))

    def submeter(self):
        self.click(*self.BOTAO_SALVAR)
