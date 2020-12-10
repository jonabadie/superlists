from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cant_add_empty_item(self):
        # Jacob goes on the website and try to submit an empty list item
        # He hits enter
        self.browser.get(self.live_server_url)
        self.typing_in_list_input('')

        # The page refresh and he receives an error message
        error_message = self.waiter.until(lambda d: d.find_element_by_css_selector('.has_error'))
        self.assertIn("empty item", error_message.text)

        # He tries again with something
        self.typing_in_list_input('Go take the kids at school')
        self.check_for_row_in_list_table(['1: Go take the kids at school'])

        # Then try again to add an empty item on the list page
        # And receive the same error as on the home page
        self.typing_in_list_input('')
        error_message = self.waiter.until(lambda d: d.find_element_by_css_selector('.has_error'))
        self.assertIn("empty item", error_message.text)

        # He corrects it again and enter something in the input box
        self.typing_in_list_input('Make them eat dinner')
        self.check_for_row_in_list_table(['1: Go take the kids at school', '2: Make them eat dinner'])
