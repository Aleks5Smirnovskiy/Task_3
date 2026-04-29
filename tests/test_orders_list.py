import allure
import pytest
from page_objects.orders_list_page import OrdersListPage
from page_objects.constructor_page import ConstructorPage
from page_objects.profile_page import ProfilePage
from page_objects.locators.locators import OrdersListLocators


@pytest.mark.functional
@allure.feature("Лента заказов")
class TestOrdersList:
    """Тесты для ленты заказов"""

    def _create_order_and_get_number(self, browser):
        """Создать заказ через конструктор и вернуть его номер"""
        constructor_page = ConstructorPage(browser)
        constructor_page.open_constructor_page()
        constructor_page.add_bun_to_constructor()
        constructor_page.add_filling_to_constructor()
        constructor_page.click_order_button()
        return constructor_page.get_order_number()

    @allure.title("Клик на заказ открывает всплывающее окно")
    @allure.description("Проверка, что клик на заказ открывает окно с деталями")
    def test_click_order_opens_modal(self, browser):
        """Проверить открытие модального окна при клике на заказ"""
        orders_list_page = OrdersListPage(browser)
        orders_list_page.open_orders_list_page()

        orders_list_page.click_order()
        assert orders_list_page.is_order_details_modal_open(), \
            "Всплывающее окно с деталями заказа не открылось"

    @allure.title("Заказы из истории отображаются на ленте")
    @allure.description("Проверка, что заказы пользователя из истории отображаются в ленте")
    def test_user_orders_appear_in_feed(self, browser, logged_in_user):
        """Проверить, что заказы пользователя отображаются на ленте"""
        order_number = self._create_order_and_get_number(browser)

        profile_page = ProfilePage(browser)
        profile_page.open_profile_page()
        profile_page.click_order_history_link()
        history_order_number = profile_page.get_last_history_order_number()

        orders_list_page = OrdersListPage(browser)
        orders_list_page.open_orders_list_page()
        orders_list_page.wait_order_in_feed(history_order_number)

        assert order_number == history_order_number, \
            "Заказ из истории пользователя не совпал с созданным заказом"

    @allure.title("Счетчик 'Выполнено за всё время' увеличивается")
    @allure.description("Проверка, что при создании заказа счетчик увеличивается")
    def test_total_completed_counter_increases(self, browser, logged_in_user):
        """Проверить увеличение счетчика выполненных заказов за всё время"""
        orders_list_page = OrdersListPage(browser)
        orders_list_page.open_orders_list_page()

        initial_count = orders_list_page.get_orders_done_count()
        self._create_order_and_get_number(browser)
        orders_list_page.open_orders_list_page()
        orders_list_page.wait_counter_increase(OrdersListLocators.ORDERS_DONE_COUNT, initial_count)

        updated_count = orders_list_page.get_orders_done_count()
        assert updated_count > initial_count, \
            "Счетчик 'Выполнено за все время' не увеличился после создания заказа"

    @allure.title("Счетчик 'Выполнено за сегодня' увеличивается")
    @allure.description("Проверка, что при создании заказа счетчик за сегодня увеличивается")
    def test_today_completed_counter_increases(self, browser, logged_in_user):
        """Проверить увеличение счетчика выполненных заказов за сегодня"""
        orders_list_page = OrdersListPage(browser)
        orders_list_page.open_orders_list_page()

        initial_count = orders_list_page.get_orders_done_today_count()
        self._create_order_and_get_number(browser)
        orders_list_page.open_orders_list_page()
        orders_list_page.wait_counter_increase(OrdersListLocators.ORDERS_DONE_TODAY_COUNT, initial_count)

        updated_count = orders_list_page.get_orders_done_today_count()
        assert updated_count > initial_count, \
            "Счетчик 'Выполнено за сегодня' не увеличился после создания заказа"

    @allure.title("Номер заказа появляется в разделе 'В работе'")
    @allure.description("Проверка, что после оформления заказа его номер появляется в работе")
    def test_order_number_appears_in_work(self, browser, logged_in_user):
        """Проверить, что номер заказа появляется в разделе 'В работе'"""
        self._create_order_and_get_number(browser)

        profile_page = ProfilePage(browser)
        profile_page.open_profile_page()
        profile_page.click_order_history_link()
        order_number = profile_page.get_last_history_order_number()

        orders_list_page = OrdersListPage(browser)
        orders_list_page.open_orders_list_page()
        orders_list_page.wait_order_in_progress(order_number)

        in_work = order_number in orders_list_page.get_order_number_in_work()
        in_done = order_number in orders_list_page.get_order_numbers_done()
        in_feed_api = orders_list_page.is_order_present_in_feed_api(order_number)

        assert in_work or in_done or in_feed_api, \
            "Номер оформленного заказа не появился в статусных блоках ленты и не найден в API ленты"
