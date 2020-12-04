from django.test import TestCase

from lists.models import Item


class HomePageTest(TestCase):

    def test_root_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_root_can_save_POST_request(self):
        response = self.client.post('/', data={'item_text': "A new list item"})
        self.assertIn("A new list item", response.content.decode())
        self.assertTemplateUsed(response, 'lists/home.html')


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        item1 = Item(text="First item")
        item1.save()

        item2 = Item(text="Second item")
        item2.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(saved_items[0].text, "First item")
        self.assertEqual(saved_items[1].text, "Second item")