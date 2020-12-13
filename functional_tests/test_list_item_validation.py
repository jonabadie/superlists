from .base import FunctionalTest
import time


class ItemValidationTest(FunctionalTest):
    def get_error_elem(self):
        return self.waiter.until(lambda d: self.browser.find_element_by_css_selector('.has-error'))

    def input_duplicate_item(self):
        # Jacob start a new list and enter the same tem a second time
        # An error should appear
        self.typing_in_list_input('Clean my room')
        self.wait_for_check_for_row(['1: Clean my room'])
        self.typing_in_list_input('Clean my room')

        return self.get_error_elem()

    def test_cant_add_empty_item(self):
        # Jacob goes on the website and try to submit an empty list item
        # He hits enter
        self.browser.get(self.live_server_url)
        self.typing_in_list_input('')

        # The page does not refresh and identify the entry as invalid
        self.waiter.until(lambda d: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # He tries again with something
        self.typing_in_list_input('Go take the kids at school')
        self.wait_for_check_for_row(['1: Go take the kids at school'])

        # Then try again to add an empty item on the list page
        # And receive the same error as on the home page
        self.typing_in_list_input('')
        self.waiter.until(lambda d: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # He corrects it again and enter something in the input box
        self.typing_in_list_input('Make them eat dinner')
        self.wait_for_check_for_row(['1: Go take the kids at school', '2: Make them eat dinner'])

        # Satisfied

    def test_cant_add_duplicate_item(self):
        # Jacob goes on the website
        self.browser.get(self.live_server_url)

        # Jacob start a new list and enter the same tem a second time
        # An error should appear
        error_elem = self.input_duplicate_item()
        self.assertEqual("You already have this item on your list", error_elem.text)

        # Satisfied

    def test_error_message_cleared_on_input(self):
        # Jacob starts a list and cause a validation error
        self.browser.get(self.live_server_url)

        # Jacob start a new list and enter the same tem a second time
        # An error should appear
        error_elem = self.input_duplicate_item()
        self.assertTrue(error_elem.is_displayed())

        # He start typing again in the input box to avoid the error
        self.typing_in_list_input('a')

        # The error message disappears
        error_elem = self.get_error_elem()
        self.assertFalse(error_elem.is_displayed())

        # Satisfied
