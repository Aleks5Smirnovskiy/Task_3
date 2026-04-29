import allure
import re
from selenium.common.exceptions import TimeoutException
from page_objects.base_page import BasePage
from page_objects.locators.locators import ConstructorLocators
from page_objects.header import Header


class ConstructorPage(BasePage):
    """Page Object для конструктора"""

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://qa-stellarburgers.education-services.ru"
        self.header = Header(driver)

    @allure.step("Открыть конструктор")
    def open_constructor_page(self):
        """Открыть страницу конструктора"""
        self.open_page(self.url)
        self.wait_until_visible(ConstructorLocators.CONSTRUCTOR_TITLE)

    @allure.step("Кликнуть на ингредиент")
    def click_ingredient(self):
        """Кликнуть на ингредиент"""
        self.scroll_to_element(ConstructorLocators.INGREDIENT_ITEM)
        self.click_element(ConstructorLocators.INGREDIENT_ITEM)

    @allure.step("Проверить, что открылось всплывающее окно с деталями")
    def is_ingredient_details_modal_open(self):
        """Проверить, открылось ли окно деталей ингредиента"""
        return self.is_element_visible(ConstructorLocators.INGREDIENT_DETAILS_TITLE)

    @allure.step("Кликнуть на крестик для закрытия окна")
    def close_modal(self):
        """Закрыть всплывающее окно"""
        self.click_element(ConstructorLocators.MODAL_CLOSE_BUTTON)

    @allure.step("Проверить, что окно закрыто")
    def is_modal_closed(self):
        """Проверить, закрыто ли модальное окно"""
        return self.wait_until_invisible(ConstructorLocators.INGREDIENT_DETAILS_MODAL)

    @allure.step("Проверить, что каунтер ингредиента увеличился")
    def is_ingredient_counter_visible(self):
        """Проверить видимость счетчика ингредиента"""
        return self.is_element_visible(ConstructorLocators.INGREDIENT_COUNTER)

    @allure.step("Получить значение счетчика ингредиента")
    def get_bun_counter_value(self):
        """Получить текущее значение счетчика для первой булки"""
        try:
            counter_text = self.get_text(ConstructorLocators.BUN_INGREDIENT_COUNTER)
            return int(counter_text)
        except TimeoutException:
            return 0

    @allure.step("Перетащить булку в конструктор")
    def add_bun_to_constructor(self):
        """Добавить булку в конструктор перетаскиванием"""
        self.drag_and_drop(
            ConstructorLocators.BUN_INGREDIENT_ITEM,
            ConstructorLocators.CONSTRUCTOR_DROP_ZONE_TOP
        )

    @allure.step("Перетащить начинку в конструктор")
    def add_filling_to_constructor(self):
        """Добавить начинку в конструктор перетаскиванием"""
        self.drag_and_drop(
            ConstructorLocators.FILLING_INGREDIENT_ITEM,
            ConstructorLocators.CONSTRUCTOR_DROP_ZONE_FILLINGS
        )

    @allure.step("Кликнуть на кнопку 'Оформить заказ'")
    def click_order_button(self):
        """Кликнуть на кнопку оформления заказа"""
        self.scroll_to_element(ConstructorLocators.ORDER_BUTTON)
        self.click_element(ConstructorLocators.ORDER_BUTTON)

    @allure.step("Получить номер заказа из модального окна")
    def get_order_number(self):
        """Получить номер заказа из модального окна"""
        self.wait_until_visible(ConstructorLocators.ORDER_MODAL)

        def _get_real_number(_):
            text = self.driver.find_element(*ConstructorLocators.ORDER_NUMBER).text
            match = re.search(r"(\d+)", text)
            if not match:
                return False
            number = str(int(match.group(1)))
            if number == "9999":
                return False
            return number

        return self.wait.until(_get_real_number)

    @allure.step("Проверить, что открыта страница конструктора")
    def is_constructor_page_open(self):
        """Проверить наличие заголовка конструктора"""
        return self.is_element_visible(ConstructorLocators.CONSTRUCTOR_TITLE)
