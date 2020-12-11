from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List


class ListAndItemModelTest(TestCase):
    def test_cant_save_empty_item(self):
        list_ = List.objects.create()
        item = Item(text='', list=list_)
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        item1 = Item(text="First item", list=list_)
        item1.save()

        item2 = Item(text="Second item", list=list_)
        item2.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(saved_items[0].text, "First item")
        self.assertEqual(saved_items[1].text, "Second item")

        self.assertEqual(saved_items[0].list, list_)
        self.assertEqual(saved_items[1].list, list_)

