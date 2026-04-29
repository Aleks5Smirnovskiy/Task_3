import allure
import pytest
from page_objects.profile_page import ProfilePage
from page_objects.constructor_page import ConstructorPage


@pytest.mark.functional
@allure.feature("Личный кабинет")
class TestPersonalAccount:
    """Тесты для личного кабинета"""

    @allure.title("Переход в личный кабинет по клику")
    @allure.description("Проверка перехода в личный кабинет при клике на кнопку")
    def test_navigate_to_profile(self, browser, logged_in_user):
        """Проверить переход в личный кабинет"""
        constructor_page = ConstructorPage(browser)
        constructor_page.open_constructor_page()
        constructor_page.header.click_profile_button()

        profile_page = ProfilePage(browser)
        assert profile_page.is_on_profile_page(), \
            "Не выполнен переход в личный кабинет по кнопке 'Личный кабинет'"

    @allure.title("Переход в раздел 'История заказов'")
    @allure.description("Проверка перехода в раздел История заказов")
    def test_navigate_to_order_history(self, browser, logged_in_user):
        """Проверить переход в историю заказов"""
        profile_page = ProfilePage(browser)
        profile_page.open_profile_page()

        profile_page.click_order_history_link()
        assert profile_page.is_order_history_open(), \
            "Не произошел переход в раздел 'История заказов'"

    @allure.title("Выход из аккаунта")
    @allure.description("Проверка функциональности выхода из аккаунта")
    def test_logout_from_account(self, browser, logged_in_user):
        """Проверить выход из аккаунта"""
        profile_page = ProfilePage(browser)
        profile_page.open_profile_page()

        profile_page.logout()
        assert profile_page.is_logged_out(), \
            "После выхода пользователь не перенаправлен на страницу входа"
