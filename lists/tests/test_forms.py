from django.test import TestCase
from django.core.exceptions import NON_FIELD_ERRORS

from lists.forms import EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, ItemForm
from lists.models import List, Item


class ItemFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_item(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_with_no_list_create_a_new_list(self):
        form = ItemForm(data={'text': 'First item'})
        self.assertTrue(form.is_valid())
        item = form.save()
        self.assertEqual(List.objects.count(), 1)
        self.assertEqual(item.list, List.objects.first())

    def test_form_with_list_create_item_for_that_list(self):
        list1 = List.objects.create()
        form = ItemForm(for_list=list1, data={'text': 'item'})
        self.assertTrue(form.is_valid())
        item = form.save()
        self.assertEqual(item.list, list1)

    def test_form_validation_for_duplicate_items(self):
        list1 = List.objects.create()
        Item.objects.create(text='Twin', list=list1)
        form = ItemForm(for_list=list1, data={'text': 'Twin'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])