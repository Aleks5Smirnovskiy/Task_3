from selenium.webdriver.common.by import By


class AuthLocators:
    """Локаторы для страницы входа"""
    EMAIL_INPUT = (By.XPATH, "//label[.='Email']/following-sibling::input")
    PASSWORD_INPUT = (By.XPATH, "//label[.='Пароль']/following-sibling::input")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти')]")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[contains(text(), 'Восстановить пароль')]")


class ForgotPasswordLocators:
    """Локаторы для страницы восстановления пароля"""
    EMAIL_INPUT = (By.XPATH, "//label[.='Email']/following-sibling::input")
    RESTORE_BUTTON = (By.XPATH, "//button[contains(text(), 'Восстановить')]")
    NEW_PASSWORD_INPUT = (By.XPATH, "//label[.='Пароль']/following-sibling::input")
    PASSWORD_SHOW_TOGGLE = (By.XPATH, "//label[.='Пароль']/following-sibling::div")
    PASSWORD_INPUT_WRAPPER = (By.XPATH, "//label[.='Пароль']/parent::*")
    BACK_LINK = (By.XPATH, "//a[contains(text(), 'Войти')]")


class HeaderLocators:
    """Локаторы для хедера"""
    PROFILE_BUTTON = (By.XPATH, "//nav//p[contains(text(), 'Личный Кабинет')]/ancestor::a[1]")
    CONSTRUCTOR_BUTTON = (By.XPATH, "//nav//p[contains(text(), 'Конструктор')]/ancestor::a[1]")
    ORDERS_LIST_BUTTON = (By.XPATH, "//nav//p[contains(text(), 'Лента Заказов')]/ancestor::a[1]")
    LOGO = (By.CSS_SELECTOR, "svg[class*='logo']")


class ProfileLocators:
    """Локаторы для личного кабинета"""
    PROFILE_NAME = (By.XPATH, "//main//nav//a[normalize-space(text())='Профиль']")
    ORDER_HISTORY_LINK = (By.XPATH, "//main//nav//a[normalize-space(text())='История заказов']")
    LOGOUT_BUTTON = (By.XPATH, "//main//nav//button[normalize-space(text())='Выход']")
    HISTORY_ORDER_NUMBERS = (By.XPATH, "//main//a[contains(@href, '/account/order-history')]//p[contains(@class, 'text_type_digits-default')]")


class ConstructorLocators:
    """Локаторы для конструктора"""
    CONSTRUCTOR_TITLE = (By.XPATH, "//h1[contains(text(), 'Соберите бургер')]")
    INGREDIENT_ITEM = (By.XPATH, "//h2[text()='Булки']/following-sibling::ul[1]/a[1]")
    BUN_INGREDIENT_ITEM = (By.XPATH, "//h2[text()='Булки']/following-sibling::ul[1]/a[1]")
    FILLING_INGREDIENT_ITEM = (By.XPATH, "//h2[text()='Начинки']/following-sibling::ul[1]/a[1]")
    BUN_INGREDIENT_COUNTER = (By.XPATH, "(//h2[text()='Булки']/following-sibling::ul[1]/a[1]//p)[1]")
    CONSTRUCTOR_DROP_ZONE_TOP = (By.XPATH, "//*[contains(text(), 'Перетяните булочку сюда (верх)')]/ancestor::li[1]")
    CONSTRUCTOR_DROP_ZONE_FILLINGS = (By.XPATH, "//ul[contains(@class, 'BurgerConstructor_basket__list')]")
    INGREDIENT_DETAILS_TITLE = (By.XPATH, "//h2[contains(text(), 'Детали ингредиента')]")
    INGREDIENT_DETAILS_MODAL = (By.XPATH, "//section[contains(@class, 'Modal_modal_opened')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'modal__close')]")
    INGREDIENT_COUNTER = (By.XPATH, "//p[contains(@class, 'counter_counter__num')]")
    ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    ORDER_MODAL = (By.XPATH, "//section[contains(@class, 'Modal_modal_opened')]")
    ORDER_NUMBER = (By.XPATH, "//section[contains(@class, 'Modal_modal_opened')]//h2")


class OrdersListLocators:
    """Локаторы для ленты заказов"""
    FEED_TITLE = (By.XPATH, "//h1[contains(text(), 'Лента заказов')]")
    ORDER_ITEM = (By.XPATH, "//a[contains(@href, '/feed/')]")
    ORDER_NUMBER_IN_CARD = (By.XPATH, ".//p[contains(@class, 'text_type_digits-default')]")
    ORDER_DETAILS_MODAL = (By.XPATH, "//section[contains(@class, 'Modal_modal_opened')]")
    ORDERS_DONE_COUNT = (By.XPATH, "//p[contains(text(), 'Выполнено за все время')]/following-sibling::p")
    ORDERS_DONE_TODAY_COUNT = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня')]/following-sibling::p")
    ORDERS_DONE = (By.XPATH, "//p[contains(text(), 'Готовы')]/following-sibling::ul[1]//li")
    ORDERS_IN_WORK = (By.XPATH, "//p[contains(text(), 'В работе')]/following-sibling::ul[1]//li")
