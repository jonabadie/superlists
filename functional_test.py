from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_list_and_retrieve_later(self):
        # User go on the website
        self.browser.get('http://localhost:8000')

        # He checks he's on the right website by looking if to-do lists is in the title
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "Buy a new laptop" into a text box
        inputbox.send_keys('Buy a new laptop')

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy a new laptop" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == "Buy a new laptop" for row in rows)
        )

        self.fail('FINISH TEST')
        # There is still a text box inviting him to add another item

        # He enters "Configure the new laptop"

        # Page update again and shows both item in the list

        # User wonder if the website will remember the list
        # User sees that the site has generated a unique URL for her
        # There is somee explanatory text to that effect

        # User visits that URL, his to-do list is still there


if __name__ == '__main__':
    unittest.main()
