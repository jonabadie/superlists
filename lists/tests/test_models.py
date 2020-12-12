from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List


class ListAndItemModelTest(TestCase):
    def test_string_representation(self):
        item = Item(text='First item')
        self.assertEqual(str(item), 'First item')

    def test_list_ordering(self):
        list_ = List.objects.create()
        item1 = Item.objects.create(text='First', list=list_)
        item2 = Item.objects.create(text='First2', list=list_)
        item3 = Item.objects.create(text='First3', list=list_)
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])

    def test_cant_save_duplicate_item(self):
        list_ = List.objects.create()
        Item.objects.create(text='Item', list=list_)
        with self.assertRaises(ValidationError):
            item = Item(text='Item', list=list_)
            item.full_clean()

    def test_can_save_items_with_same_text_in_different_lists(self):
        list_ = List.objects.create()
        Item.objects.create(text='Item', list=list_)

        list2 = List.objects.create()
        item = Item(text='Item', list=list2)

        item.full_clean()  # Shouldn't raise

    def test_cant_save_empty_item(self):
        list_ = List.objects.create()
        item = Item(text='', list=list_)
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list1 = List.objects.create()
        item = Item.objects.create(text='first', list=list1)
        item.save()
        self.assertEqual(item, list1.item_set.first())

