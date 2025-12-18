import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def tirar_screenshot(driver, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    driver.save_screenshot(path)


def esperar_por_elemento(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
