from .base import FunctionalTest
import time


class ItemValidationTest(FunctionalTest):
    def test_cant_add_empty_item(self):
        # Jacob goes on the website and try to submit an empty list item
        # He hits enter
        self.browser.get(self.live_server_url)
        self.typing_in_list_input('')

        # The page does not refresh and identify the entry as invalid
        self.waiter.until(lambda d: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # He tries again with something
        self.typing_in_list_input('Go take the kids at school')
        self.waiter.until(lambda b: self.check_for_row_in_list_table(['1: Go take the kids at school']))

        # Then try again to add an empty item on the list page
        # And receive the same error as on the home page
        self.typing_in_list_input('')
        self.waiter.until(lambda d: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # He corrects it again and enter something in the input box
        self.typing_in_list_input('Make them eat dinner')
        self.waiter.until(lambda b: self.check_for_row_in_list_table(
            ['1: Go take the kids at school', '2: Make them eat dinner']
        ))

        # Satisfied

    def test_cant_add_duplicate_item(self):
        # Jacob goes on the website
        self.browser.get(self.live_server_url)

        # Jacob start a new list
        # It goes on the list page
        # He can see his item on the page
        self.typing_in_list_input('Clean my room')
        self.waiter.until(lambda b: self.check_for_row_in_list_table(['1: Clean my room']))

        # Jacob enter the exact same item
        self.typing_in_list_input('Clean my room')

        # Invalid because it already exist
        self.waiter.until(lambda d: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # Jacob enter a different item and everything is fine
        self.typing_in_list_input('Clean my other room')
        self.waiter.until(lambda b: self.check_for_row_in_list_table(
            ['1: Clean my room', '2: Clean my other room']
        ))

        # Satisfied
