import allure
import pytest
from page_objects.forgot_password_page import ForgotPasswordPage
from page_objects.auth_page import AuthPage


@pytest.mark.functional
@allure.feature("Восстановление пароля")
class TestPasswordRecovery:
    """Тесты для восстановления пароля"""

    @allure.title("Переход на страницу восстановления пароля по кнопке")
    @allure.description("Проверка перехода на страницу восстановления пароля при клике на ссылку")
    def test_navigate_to_forgot_password_page(self, browser):
        """Проверить переход на страницу восстановления пароля"""
        auth_page = AuthPage(browser)
        auth_page.open_auth_page()
        auth_page.click_forgot_password_link()

        assert "/forgot-password" in auth_page.get_current_url(), \
            "Не произошел переход на страницу восстановления пароля"

    @allure.title("Ввод почты и клик по кнопке 'Восстановить'")
    @allure.description("Проверка, что можно ввести email и нажать кнопку восстановления")
    def test_restore_password_with_email(self, browser, test_user):
        """Проверить восстановление пароля с помощью email"""
        forgot_password_page = ForgotPasswordPage(browser)
        forgot_password_page.open_forgot_password_page()

        test_email = test_user["email"]
        forgot_password_page.enter_email(test_email)
        forgot_password_page.click_restore_button()

        assert forgot_password_page.is_reset_password_page_open(), \
            "После клика на 'Восстановить' не открылась страница сброса пароля"

    @allure.title("Кнопка показать/скрыть пароль активирует поле")
    @allure.description("Проверка, что клик на кнопку показать/скрыть пароль делает поле активным")
    def test_password_visibility_toggle(self, browser, test_user):
        """Проверить, что кнопка показать/скрыть пароль делает поле активным"""
        forgot_password_page = ForgotPasswordPage(browser)
        forgot_password_page.open_forgot_password_page()
        forgot_password_page.enter_email(test_user["email"])
        forgot_password_page.click_restore_button()

        forgot_password_page.click_password_toggle()

        is_active = forgot_password_page.is_password_field_active()
        assert is_active, "Поле пароля не активно после клика на кнопку показать/скрыть"
