from django.test import TestCase

from lists.models import Item


class HomePageTest(TestCase):
    def test_dont_save_item_when_get(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_root_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_can_save_POST_request(self):
        self.client.post('/', data={'item_text': "A new list item"})

        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': "A new list item"})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_items_shows_in_home_page(self):
        texts = ["First item", "Second item"]
        Item.objects.create(text=texts[0])
        Item.objects.create(text=texts[1])

        response = self.client.get('/')

        self.assertIn(texts[0], response.content.decode())
        self.assertIn(texts[1], response.content.decode())
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
