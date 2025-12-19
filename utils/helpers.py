import os

try:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except Exception:
    # Fallback minimal definitions so static analysis or environments without selenium don't crash.
    class By:
        ID = "id"
        XPATH = "xpath"
        LINK_TEXT = "link text"
        PARTIAL_LINK_TEXT = "partial link text"
        NAME = "name"
        TAG_NAME = "tag name"
        CLASS_NAME = "class name"
        CSS_SELECTOR = "css selector"

    # Minimal stubs for WebDriverWait and EC that raise clear errors if used at runtime without selenium.
    class WebDriverWait:
        def __init__(self, driver, timeout):
            raise RuntimeError("selenium is not installed; WebDriverWait is unavailable")

    class EC:
        @staticmethod
        def presence_of_element_located(locator):
            raise RuntimeError("selenium is not installed; expected_conditions are unavailable")


def tirar_screenshot(driver, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    driver.save_screenshot(path)


def esperar_por_elemento(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
