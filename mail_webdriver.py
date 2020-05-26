# create KEYS.py and put LOGIN:str and PASSWORD:str variables
from KEYS import LOGIN, PASSWORD

from typing import List, Union

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


def get_node_text(web_element) -> str:
    text: str = web_element.get_attribute("innerText")
    for child in web_element.find_elements_by_xpath(".//*"):
        text = text.replace(child.get_attribute("innerText"), '')
    return text.strip()


class MailRuBot:
    def __init__(self, username: str, password: str) -> None:
        super().__init__()
        self._inbox_url = "https://e.mail.ru/messages/inbox"
        self.driver = webdriver.Chrome()
        self.driver.get("https://mail.ru")
        self.username: str = username
        self.password: str = password
        self.isAuthorized: bool = False

    def _with_authorize(func):
        def check_auth_and_call(self, *args, **kwargs):
            if (self.isAuthorized):
                return func(self, *args, **kwargs)
            else:
                print(f"{func.__name__} can't invoke: You are not authorized")
        return check_auth_and_call

    def login(self) -> None:
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "mailbox:login")))

            login_input = self.driver.find_element_by_id("mailbox:login")
            login_input.send_keys(self.username)

            submit_button = self.driver.find_element_by_xpath(
                "//label[@id='mailbox:submit']/input[@type='submit']")
            submit_button.click()

            password_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "mailbox:password")))
            password_input.send_keys(self.password)

            submit_button.click()

            self.isAuthorized = WebDriverWait(self.driver, 10).until(
                EC.url_contains(self._inbox_url))
        except:
            error = self.driver.find_element_by_id("mailbox:error")
            print(error.get_attribute("value"))
            self.quit()

    @_with_authorize
    def get_unread_messages(self, count: int) -> Union[List[str], str]:
        try:
            if (not EC.url_contains(self._inbox_url)):
                self.driver.get(self._inbox_url)

            unread_emails = WebDriverWait(self.driver, 10).until(
                lambda driver: driver.find_elements_by_class_name(
                    "b-datalist__item_unread"))

            themes = [email.find_elements_by_class_name(
                "b-datalist__item__subj") for email in unread_emails]

            return [get_node_text(theme[0]) for theme in themes[:count]]
        except:
            self.quit()

    @_with_authorize
    def send_message(self, email: str, title: str) -> None:
        try:
            if (not EC.url_contains(self._inbox_url)):
                self.driver.get(self._inbox_url)

            write_message_button = WebDriverWait(self.driver, 10).until(
                lambda driver: driver.find_element_by_css_selector("a.b-toolbar__btn"))
            write_message_button.click()

            form = WebDriverWait(self.driver,10).until(
                lambda driver: driver.find_element_by_name("Compose"))

            email_area = form.find_element_by_css_selector("textarea.compose__labels__input")
            email_area.send_keys(email)

            theme = form.find_element_by_name("Subject")
            theme.send_keys(title)
        except:
            self.quit()

    def quit(self):
        self.driver.quit()


bot = MailRuBot(LOGIN, PASSWORD)

bot.login()

for theme in bot.get_unread_messages(10):
    print(theme)

bot.send_message("test@example.com", "Это тестовое письмо")
