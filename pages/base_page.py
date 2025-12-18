from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Classe base com utilitários comuns para as páginas (POM)."""

    def __init__(self, driver):
        self.driver = driver

    def open(self, url: str):
        self.driver.get(url)

    def find(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))

    def click(self, by, value, timeout=10):
        el = self.find(by, value, timeout)
        el.click()

    def fill(self, by, value, text, timeout=10):
        el = self.find(by, value, timeout)
        el.clear()
        el.send_keys(text)
