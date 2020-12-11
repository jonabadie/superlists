from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Jacob goes on the website on a small computer screen
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Jacob notice that the input box is nicely centered
        input_box = self.get_input_box()
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )

        # He types a new list and sees the input is nicely centered there too
        self.typing_in_list_input('Buy a new laptop')
        self.waiter.until(lambda b: self.check_for_row_in_list_table(["1: Buy a new laptop"]))
        input_box = self.get_input_box()
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )
