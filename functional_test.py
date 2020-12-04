from selenium import webdriver
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
        self.fail('FINISH TEST')

        # He is invited to enter a to-do item

        # He types "Buy a new laptop" into a text box

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy a new laptop" as an item in a to-do list

        # There is still a text box inviting him to add another item

        # He enters "Configure the new laptop"

        # Page update again and shows both item in the list

        # User wonder if the website will remember the list
        # User sees that the site has generated a unique URL for her
        # There is somee explanatory text to that effect

        # User visits that URL, his to-do list is still there


if __name__ == '__main__':
    unittest.main()
