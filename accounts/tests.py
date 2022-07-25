# Create your tests here.
from lib2to3.pgen2 import driver
from django.test import LiveServerTestCase
from django.urls import reverse_lazy
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

class TestLogin(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(executable_path="C:\chromedriver.exe")

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        # ログインページを開く
        self.selenium.get('http://localhost:8000' + str(reverse_lazy('account_login')))

        # ログイン
        #username_input = self.selenium.find_element_by_name("login")
        username_input = self.selenium.find_element(By.NAME, "login")
        username_input.send_keys('ngn2149610@stu.o-hara.ac.jp')
        #password_input = self.selenium.find_element_by_name("password")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('r2k3h07c')
        #self.selenium.find_element_by_class_name('btn').click()
        password_input = self.selenium.find_element(By.NAME, "submit").click()

        # ページタイトルの検証
        self.assertEquals('日記一覧 | Private Grayscale', self.selenium.title)
