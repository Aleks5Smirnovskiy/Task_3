from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException


class BasePage:
    """Базовый класс для всех Page Object"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.actions = ActionChains(driver)

    def open_page(self, url):
        """Открыть страницу по URL"""
        self.driver.get(url)

    def find_element(self, locator):
        """Найти элемент и дождаться его видимости"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator):
        """Найти все элементы по локатору"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click_element(self, locator):
        """Кликнуть по элементу после его видимости"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def send_text(self, locator, text):
        """Отправить текст в элемент"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Получить текст элемента"""
        element = self.find_element(locator)
        return element.text

    def is_element_visible(self, locator):
        """Проверить видимость элемента"""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def get_element_attribute(self, locator, attribute):
        """Получить атрибут элемента"""
        element = self.find_element(locator)
        return element.get_attribute(attribute)

    def scroll_to_element(self, locator):
        """Скроллить до элемента"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def wait_until_visible(self, locator):
        """Дождаться видимости элемента"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_until_clickable(self, locator):
        """Дождаться кликабельности элемента"""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_until_invisible(self, locator):
        """Дождаться невидимости элемента"""
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def drag_and_drop(self, source_locator, target_locator):
        """Перетащить элемент на целевую область"""
        source = self.find_element(source_locator)
        target = self.find_element(target_locator)
        try:
            self.driver.execute_script(
                """
                const source = arguments[0];
                const target = arguments[1];
                const dataTransfer = new DataTransfer();

                source.dispatchEvent(new DragEvent('dragstart', {bubbles: true, cancelable: true, dataTransfer}));
                target.dispatchEvent(new DragEvent('dragenter', {bubbles: true, cancelable: true, dataTransfer}));
                target.dispatchEvent(new DragEvent('dragover', {bubbles: true, cancelable: true, dataTransfer}));
                target.dispatchEvent(new DragEvent('drop', {bubbles: true, cancelable: true, dataTransfer}));
                source.dispatchEvent(new DragEvent('dragend', {bubbles: true, cancelable: true, dataTransfer}));
                """,
                source,
                target,
            )
        except Exception:
            self.actions.click_and_hold(source).move_to_element(target).release().perform()

    def get_elements_text(self, locator):
        """Получить тексты набора элементов"""
        return [element.text for element in self.find_elements(locator)]

    def get_current_url(self):
        """Получить текущий URL"""
        return self.driver.current_url
