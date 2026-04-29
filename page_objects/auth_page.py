import allure
from page_objects.base_page import BasePage
from page_objects.locators.locators import AuthLocators


class AuthPage(BasePage):
    """Page Object для страницы входа"""

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://qa-stellarburgers.education-services.ru/login"

    @allure.step("Открыть страницу входа")
    def open_auth_page(self):
        """Открыть страницу входа"""
        self.open_page(self.url)

    @allure.step("Ввести email: {email}")
    def enter_email(self, email):
        """Ввести email в поле входа"""
        self.send_text(AuthLocators.EMAIL_INPUT, email)

    @allure.step("Ввести пароль: {password}")
    def enter_password(self, password):
        """Ввести пароль"""
        self.send_text(AuthLocators.PASSWORD_INPUT, password)

    @allure.step("Кликнуть на кнопку 'Войти'")
    def click_login_button(self):
        """Кликнуть на кнопку входа"""
        self.click_element(AuthLocators.LOGIN_BUTTON)

    @allure.step("Кликнуть на ссылку 'Восстановить пароль'")
    def click_forgot_password_link(self):
        """Кликнуть на ссылку восстановления пароля"""
        self.click_element(AuthLocators.FORGOT_PASSWORD_LINK)

    @allure.step("Выполнить вход с email: {email}")
    def login(self, email, password):
        """Выполнить вход с email и паролем"""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()

    @allure.step("Проверить, что открыта страница входа")
    def is_login_page_open(self):
        """Проверить, что пользователь находится на странице входа"""
        return "/login" in self.get_current_url()
