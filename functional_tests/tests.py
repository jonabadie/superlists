from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

from .waiter import JoWaiter


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
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

    def test_can_start_list_for_one_user(self):
        # User go on the website
        self.browser.get(self.live_server_url)

        # He checks he's on the right website by looking if to-do lists is in the title
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item
        self.input_box_placeholder_present()

        # He types "Buy a new laptop" into a text box
        # When he hits enter, the page updates
        self.typing_in_list_input('Buy a new laptop')

        time.sleep(1)
        # And now the page lists "1: Buy a new laptop" as an item in a to-do list
        self.waiter.until(lambda b: self.check_for_row_in_list_table(["1: Buy a new laptop"]))

        # There is still a text box inviting him to add another item
        self.input_box_placeholder_present()

        # He enters "Configure the new laptop"
        self.typing_in_list_input('Configure the new laptop')

        # Page update again and shows both item in the list
        self.waiter.until(
            lambda b:
            self.check_for_row_in_list_table(["1: Buy a new laptop", "2: Configure the new laptop"])
        )

        # User satisfied

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # User start a new list
        self.browser.get(self.live_server_url)
        self.typing_in_list_input('Buy a new laptop')
        self.waiter.until(lambda b: self.check_for_row_in_list_table(["1: Buy a new laptop"]))

        # User notices that his list has a unique URL
        user_list_url = self.browser.current_url
        self.assertRegex(user_list_url, '/lists/.+')

        # Now a new user, Jacob, comes along to the site

        # We use a new browser session to make sure that no information
        # of Edith's is coming through from cookies etc...
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Jacob visits the home page. There is no sign of first user's list
        self.browser.get(self.live_server_url)
        page = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("1: Buy a new laptop", page)
        self.assertNotIn("2: Configure the new laptop", page)

        # Jacob starts his own list
        self.typing_in_list_input('Rearrange living room')
        self.waiter.until(lambda b: self.check_for_row_in_list_table(["1: Rearrange living room"]))

        # Jacob has his own list url
        jacob_list_url = self.browser.current_url
        self.assertRegex(jacob_list_url, '/lists/.+')
        self.assertNotEqual(user_list_url, jacob_list_url)

        # Satisfied
