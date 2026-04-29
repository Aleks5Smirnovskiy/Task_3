import allure
import re
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from page_objects.base_page import BasePage
from page_objects.locators.locators import ProfileLocators
from page_objects.header import Header


class ProfilePage(BasePage):
    """Page Object для личного кабинета"""

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://qa-stellarburgers.education-services.ru/account/profile"
        self.base_url = "https://qa-stellarburgers.education-services.ru"
        self.header = Header(driver)

    @allure.step("Открыть личный кабинет")
    def open_profile_page(self):
        """Открыть личный кабинет"""
        self.open_page("https://qa-stellarburgers.education-services.ru")
        self.header.click_profile_button()

    @allure.step("Проверить, что мы в личном кабинете")
    def is_on_profile_page(self):
        """Проверить, находимся ли мы на странице профиля"""
        return self.is_element_visible(ProfileLocators.PROFILE_NAME)

    @allure.step("Кликнуть на 'История заказов'")
    def click_order_history_link(self):
        """Кликнуть на ссылку истории заказов"""
        self.click_element(ProfileLocators.ORDER_HISTORY_LINK)

    @allure.step("Проверить, что открыта история заказов")
    def is_order_history_open(self):
        """Проверить, открыта ли история заказов"""
        return "/account/order-history" in self.get_current_url()

    @allure.step("Кликнуть на кнопку 'Выход'")
    def logout(self):
        """Выполнить выход из аккаунта"""
        self.click_element(ProfileLocators.LOGOUT_BUTTON)

    @allure.step("Проверить, что выход выполнен")
    def is_logged_out(self):
        """Проверить, что произошел выход (редирект на login)"""
        try:
            self.wait.until(EC.url_contains("/login"))
            return True
        except TimeoutException:
            return False

    @allure.step("Получить номер последнего заказа из истории")
    def get_last_history_order_number(self):
        """Получить номер первого заказа в истории заказов"""
        numbers = [element.text for element in self.driver.find_elements(*ProfileLocators.HISTORY_ORDER_NUMBERS)]
        for number_text in numbers:
            match = re.search(r"(\d+)", number_text)
            if match:
                return match.group(1)

        access_token = self.driver.execute_script("return window.localStorage.getItem('accessToken');")
        if access_token:
            response = requests.get(
                f"{self.base_url}/api/orders",
                headers={"Authorization": access_token},
                timeout=15
            )
            response.raise_for_status()
            orders = response.json().get("orders", [])
            if orders:
                latest_order = max(orders, key=lambda item: item.get("number", 0))
                return str(latest_order.get("number", ""))

        return ""
