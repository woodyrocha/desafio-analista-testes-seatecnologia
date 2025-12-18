from selenium.webdriver.common.by import By
from .base_page import BasePage


class ListaFuncionariosPage(BasePage):
    """Page object para a listagem de funcionários."""

    # Seletores de exemplo
    BUSCAR = (By.CSS_SELECTOR, "input[type=search]")
    ROWS = (By.CSS_SELECTOR, "table tbody tr")

    def buscar_por_texto(self, texto: str):
        self.fill(*self.BUSCAR, texto)

    def obter_linhas(self):
        return self.driver.find_elements(*self.ROWS)

    def primeiro_registro(self):
        linhas = self.obter_linhas()
        return linhas[0] if linhas else None

    def editar_primeiro(self):
        row = self.primeiro_registro()
        if row:
            btn = row.find_element(By.CSS_SELECTOR, "button[aria-label=editar]")
            btn.click()

    def excluir_primeiro(self):
        row = self.primeiro_registro()
        if row:
            btn = row.find_element(By.CSS_SELECTOR, "button[aria-label=excluir]")
            btn.click()
