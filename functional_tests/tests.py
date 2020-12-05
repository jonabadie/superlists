from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def typing_in_list_input(self, text):
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys(text)
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

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

    def test_can_start_list_and_retrieve_later(self):
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

        # And now the page lists "1: Buy a new laptop" as an item in a to-do list
        self.check_for_row_in_list_table(["1: Buy a new laptop"])

        # There is still a text box inviting him to add another item
        self.input_box_placeholder_present()

        # He enters "Configure the new laptop"
        self.typing_in_list_input('Configure the new laptop')

        # Page update again and shows both item in the list
        self.check_for_row_in_list_table(["1: Buy a new laptop", "2: Configure the new laptop"])

        self.fail('FINISH TEST')
        # User wonder if the website will remember the list
        # User sees that the site has generated a unique URL for her
        # There is some explanatory text to that effect

        # User visits that URL, his to-do list is still there
