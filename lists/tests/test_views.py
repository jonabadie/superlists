from django.test import TestCase
from django.urls import reverse

from lists.models import Item, List


class HomePageTest(TestCase):
    def test_dont_save_item_when_get(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_root_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')


class NewListTest(TestCase):
    def test_can_save_POST_request(self):
        self.client.post(reverse('new-list'), data={'item_text': "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post(reverse('new-list'), data={'item_text': "A new list item"})
        list_ = List.objects.first()
        self.assertRedirects(response, reverse('view-list', args=[list_.id]))


class NewItemTest(TestCase):
    def test_can_save_POST_request(self):
        List.objects.create()
        list2 = List.objects.create()

        self.client.post(
            reverse('add-item', args=[list2.id]),
            data={'item_text': "A new list item"})

        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, "A new list item")
        self.assertEqual(Item.objects.first().list, list2)

    def test_redirects_after_POST(self):
        List.objects.create()
        list_ = List.objects.create()

        response = self.client.post(
            reverse('add-item', args=[list_.id]),
            data={'item_text': "A new list item"})

        self.assertRedirects(response, reverse('view-list', args=[list_.id]))


class ListViewTest(TestCase):
    def test_use_list_temple(self):
        list_ = List.objects.create()
        response = self.client.get(reverse('view-list', args=[list_.id]))
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_passes_correct_list_to_template(self):
        List.objects.create()
        list_ = List.objects.create()
        response = self.client.get(reverse('view-list', args=[list_.id]))
        self.assertEqual(response.context['list'], list_)

    def test_items_shows_in_page(self):
        texts = ["First item", "Second item", "Third item", "Fourth item"]
        list_ = List.objects.create()
        Item.objects.create(text=texts[0], list=list_)
        Item.objects.create(text=texts[1], list=list_)
        list2 = List.objects.create()
        Item.objects.create(text=texts[2], list=list2)
        Item.objects.create(text=texts[3], list=list2)

        response = self.client.get(reverse('view-list', args=[list_.id]))

        self.assertContains(response, texts[0])
        self.assertContains(response, texts[1])
        self.assertNotContains(response, texts[2])
        self.assertNotContains(response, texts[3])
