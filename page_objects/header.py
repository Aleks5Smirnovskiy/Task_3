import allure
from page_objects.base_page import BasePage
from page_objects.locators.locators import HeaderLocators


class Header(BasePage):
    """Page Object для хедера приложения"""

    @allure.step("Кликнуть на 'Личный Кабинет'")
    def click_profile_button(self):
        """Кликнуть на кнопку личного кабинета"""
        self.click_element(HeaderLocators.PROFILE_BUTTON)

    @allure.step("Кликнуть на 'Конструктор'")
    def click_constructor_button(self):
        """Кликнуть на кнопку конструктора"""
        self.click_element(HeaderLocators.CONSTRUCTOR_BUTTON)

    @allure.step("Кликнуть на 'Лента заказов'")
    def click_orders_list_button(self):
        """Кликнуть на кнопку ленты заказов"""
        self.click_element(HeaderLocators.ORDERS_LIST_BUTTON)

    @allure.step("Кликнуть на логотип")
    def click_logo(self):
        """Кликнуть на логотип"""
        self.click_element(HeaderLocators.LOGO)

