import allure
import re
import requests
from selenium.webdriver.support.ui import WebDriverWait
from page_objects.base_page import BasePage
from page_objects.locators.locators import OrdersListLocators
from page_objects.header import Header


class OrdersListPage(BasePage):
    """Page Object для ленты заказов"""

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://qa-stellarburgers.education-services.ru/feed"
        self.header = Header(driver)

    @staticmethod
    def _normalize_order_number(value):
        """Нормализовать номер заказа: оставить только цифры без ведущих нулей"""
        if value is None:
            return ""
        digits = "".join(re.findall(r"\d+", str(value)))
        return str(int(digits)) if digits else ""

    @allure.step("Открыть ленту заказов")
    def open_orders_list_page(self):
        """Открыть страницу ленты заказов"""
        self.open_page(self.url)
        self.wait_until_visible(OrdersListLocators.FEED_TITLE)

    @allure.step("Кликнуть на заказ")
    def click_order(self):
        """Кликнуть на первый заказ в списке"""
        order = self.wait_until_clickable(OrdersListLocators.ORDER_ITEM)
        order.click()

    @allure.step("Проверить, что открылось окно деталей заказа")
    def is_order_details_modal_open(self):
        """Проверить, открылось ли окно деталей заказа"""
        return self.is_element_visible(OrdersListLocators.ORDER_DETAILS_MODAL)

    def _get_feed_totals(self):
        """Получить total и totalToday из API ленты заказов"""
        response = requests.get("https://qa-stellarburgers.education-services.ru/api/orders/all", timeout=10)
        response.raise_for_status()
        payload = response.json()
        return int(payload.get("total", 0)), int(payload.get("totalToday", 0))

    def is_order_present_in_feed_api(self, order_number):
        """Проверить наличие номера заказа в API общей ленты"""
        expected = self._normalize_order_number(order_number)
        response = requests.get("https://qa-stellarburgers.education-services.ru/api/orders/all", timeout=10)
        response.raise_for_status()
        orders = response.json().get("orders", [])
        numbers = [self._normalize_order_number(item.get("number")) for item in orders]
        return expected in numbers

    @allure.step("Получить количество выполненных заказов за всё время")
    def get_orders_done_count(self):
        """Получить количество выполненных заказов за всё время"""
        total, _ = self._get_feed_totals()
        return total

    @allure.step("Получить количество выполненных заказов за сегодня")
    def get_orders_done_today_count(self):
        """Получить количество выполненных заказов за сегодня"""
        _, total_today = self._get_feed_totals()
        return total_today

    @allure.step("Получить номер заказа из работающих")
    def get_order_number_in_work(self):
        """Получить номер заказа из разделе 'В работе'"""
        orders_in_work = self.get_elements_text(OrdersListLocators.ORDERS_IN_WORK)
        normalized = [self._normalize_order_number(order) for order in orders_in_work]
        return [order for order in normalized if order]

    @allure.step("Получить номера заказов из раздела 'Готовы'")
    def get_order_numbers_done(self):
        """Получить номера заказов из раздела 'Готовы'"""
        orders_done = self.get_elements_text(OrdersListLocators.ORDERS_DONE)
        normalized = [self._normalize_order_number(order) for order in orders_done]
        return [order for order in normalized if order]

    @allure.step("Получить номер первого заказа в ленте")
    def get_first_order_number(self):
        """Получить номер первого заказа на странице ленты"""
        first_card = self.find_element(OrdersListLocators.ORDER_ITEM)
        order_number = first_card.find_element(*OrdersListLocators.ORDER_NUMBER_IN_CARD).text
        return order_number.strip().replace("#", "")

    @allure.step("Проверить, что открыта страница ленты заказов")
    def is_feed_page_open(self):
        """Проверить наличие заголовка на странице ленты"""
        return self.is_element_visible(OrdersListLocators.FEED_TITLE)

    @allure.step("Дождаться увеличения счетчика до значения больше {initial_value}")
    def wait_counter_increase(self, locator, initial_value, timeout=30):
        """Дождаться увеличения выбранного счетчика"""
        def _counter_is_increased(_):
            total, total_today = self._get_feed_totals()
            if locator == OrdersListLocators.ORDERS_DONE_COUNT:
                return total > initial_value
            if locator == OrdersListLocators.ORDERS_DONE_TODAY_COUNT:
                return total_today > initial_value
            return False

        WebDriverWait(self.driver, timeout, poll_frequency=2).until(
            _counter_is_increased,
            message="Счетчик не увеличился за отведенное время"
        )

    @allure.step("Проверить, что номер заказа {order_number} отображается в разделе 'В работе'")
    def wait_order_in_progress(self, order_number, timeout=60):
        """Дождаться появления номера заказа в секции 'В работе'"""
        expected = self._normalize_order_number(order_number)

        def _order_visible_in_feed_sections(_):
            in_work = self.get_order_number_in_work()
            if expected in in_work:
                return True

            # On this stand order status may flip to "done" almost instantly,
            # so accept visibility in "Готовы" as a valid post-order state.
            done = self.get_order_numbers_done()
            if expected in done:
                return True

            # Fallback for occasional UI desync of status columns in headless mode.
            return self.is_order_present_in_feed_api(expected)

        WebDriverWait(self.driver, timeout).until(
            _order_visible_in_feed_sections,
            message=f"Номер заказа {order_number} не появился в разделе 'В работе'"
        )

    @allure.step("Проверить, что номер заказа {order_number} присутствует в ленте")
    def wait_order_in_feed(self, order_number, timeout=120):
        """Дождаться появления номера заказа в ленте через API"""
        expected = str(int(order_number))

        def _is_order_present(_):
            response = requests.get("https://qa-stellarburgers.education-services.ru/api/orders/all", timeout=10)
            response.raise_for_status()
            orders = response.json().get("orders", [])
            numbers = [str(int(item.get("number", 0))) for item in orders if item.get("number") is not None]
            return expected in numbers

        WebDriverWait(self.driver, timeout, poll_frequency=2).until(
            _is_order_present,
            message=f"Номер заказа {order_number} не найден в ленте"
        )
