import allure
from page_objects.base_page import BasePage
from page_objects.locators.locators import ForgotPasswordLocators


class ForgotPasswordPage(BasePage):
    """Page Object для страницы восстановления пароля"""

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://qa-stellarburgers.education-services.ru/forgot-password"

    @allure.step("Открыть страницу восстановления пароля")
    def open_forgot_password_page(self):
        """Открыть страницу восстановления пароля"""
        self.open_page(self.url)

    @allure.step("Ввести email для восстановления: {email}")
    def enter_email(self, email):
        """Ввести email для восстановления"""
        self.send_text(ForgotPasswordLocators.EMAIL_INPUT, email)

    @allure.step("Кликнуть на кнопку 'Восстановить'")
    def click_restore_button(self):
        """Кликнуть на кнопку восстановления"""
        self.click_element(ForgotPasswordLocators.RESTORE_BUTTON)

    @allure.step("Кликнуть на кнопку показать/скрыть пароль")
    def click_password_toggle(self):
        """Кликнуть на кнопку показать/скрыть пароль"""
        self.click_element(ForgotPasswordLocators.PASSWORD_SHOW_TOGGLE)

    @allure.step("Проверить, что поле пароля активно")
    def is_password_field_active(self):
        """Проверить, активно ли поле пароля (подсвечено)"""
        wrapper_class = self.get_element_attribute(
            ForgotPasswordLocators.PASSWORD_INPUT_WRAPPER,
            "class"
        )
        return "input_status_active" in wrapper_class

    @allure.step("Проверить, что открыта страница сброса пароля")
    def is_reset_password_page_open(self):
        """Проверить, что открыт экран сброса пароля"""
        try:
            self.wait.until(lambda driver: "/reset-password" in driver.current_url)
            return True
        except Exception:
            return False

    @allure.step("Кликнуть на ссылку 'Войти'")
    def click_back_to_login_link(self):
        """Вернуться на страницу входа"""
        self.click_element(ForgotPasswordLocators.BACK_LINK)
