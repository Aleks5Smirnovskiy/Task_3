import allure
import pytest
from page_objects.constructor_page import ConstructorPage
from page_objects.orders_list_page import OrdersListPage


@pytest.mark.functional
@allure.feature("Основной функционал")
class TestMainFunctionality:
    """Тесты для основного функционала конструктора"""

    @allure.title("Переход на страницу конструктора")
    @allure.description("Проверка перехода на страницу конструктора по кнопке")
    def test_navigate_to_constructor(self, browser):
        """Проверить переход в конструктор"""
        orders_list_page = OrdersListPage(browser)
        orders_list_page.open_orders_list_page()
        orders_list_page.header.click_constructor_button()

        constructor_page = ConstructorPage(browser)
        assert constructor_page.is_constructor_page_open(), \
            "Не произошел переход в конструктор"

    @allure.title("Переход на страницу ленты заказов")
    @allure.description("Проверка перехода на страницу ленты заказов")
    def test_navigate_to_orders_list(self, browser):
        """Проверить переход на ленту заказов"""
        constructor_page = ConstructorPage(browser)
        constructor_page.open_constructor_page()

        constructor_page.header.click_orders_list_button()

        orders_list_page = OrdersListPage(browser)
        assert orders_list_page.is_feed_page_open(), \
            "Не произошел переход на ленту заказов"

    @allure.title("Клик на ингредиент открывает всплывающее окно")
    @allure.description("Проверка, что клик на ингредиент открывает окно с деталями")
    def test_click_ingredient_opens_modal(self, browser):
        """Проверить открытие модального окна при клике на ингредиент"""
        constructor_page = ConstructorPage(browser)
        constructor_page.open_constructor_page()
        constructor_page.click_ingredient()

        assert constructor_page.is_ingredient_details_modal_open(), \
            "Всплывающее окно с деталями ингредиента не открылось"

    @allure.title("Закрытие модального окна по крестику")
    @allure.description("Проверка, что окно с деталями закрывается по крестику")
    def test_close_ingredient_modal_with_x_button(self, browser):
        """Проверить закрытие модального окна по крестику"""
        constructor_page = ConstructorPage(browser)
        constructor_page.open_constructor_page()
        constructor_page.click_ingredient()
        assert constructor_page.is_ingredient_details_modal_open()

        constructor_page.close_modal()
        assert constructor_page.is_modal_closed(), \
            "Модальное окно не закрылось после клика на крестик"

    @allure.title("Каунтер ингредиента увеличивается при добавлении")
    @allure.description("Проверка, что при добавлении ингредиента увеличивается счетчик")
    def test_ingredient_counter_increases(self, browser):
        """Проверить увеличение счетчика при добавлении ингредиента"""
        constructor_page = ConstructorPage(browser)
        constructor_page.open_constructor_page()

        initial_counter = constructor_page.get_bun_counter_value()
        constructor_page.add_bun_to_constructor()
        updated_counter = constructor_page.get_bun_counter_value()

        assert updated_counter > initial_counter, \
            "Счетчик ингредиента не увеличился после добавления в заказ"

    @allure.title("Залогиненный пользователь может оформить заказ")
    @allure.description("Проверка возможности оформить заказ для залогиненного пользователя")
    def test_logged_in_user_can_order(self, browser, logged_in_user):
        """Проверить, что залогиненный пользователь может оформить заказ"""
        constructor_page = ConstructorPage(browser)
        constructor_page.open_constructor_page()

        constructor_page.add_bun_to_constructor()
        constructor_page.add_filling_to_constructor()
        constructor_page.click_order_button()

        order_number = constructor_page.get_order_number()
        assert order_number.isdigit(), "После оформления заказа не получен валидный номер заказа"
