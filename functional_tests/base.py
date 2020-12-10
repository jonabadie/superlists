from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import os

from .waiter import JoWaiter


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = "http://" + staging_server
        self.waiter = JoWaiter(
            self.browser,
            timeout=3,
            ignored_exceptions=[
                AssertionError,
                WebDriverException
            ]
        )

    def tearDown(self):
        self.browser.quit()

    def typing_in_list_input(self, text):
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys(text)
        input_box.send_keys(Keys.ENTER)

    def input_box_placeholder_present(self):
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

    def check_for_row_in_list_table(self, texts):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        rows_text = [row.text for row in rows]
        for text in texts:
            self.assertIn(text, rows_text)
        return True
