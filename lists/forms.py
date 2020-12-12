from django import forms
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

from .models import Item, List

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You already have this item on your list"


class ItemForm(forms.ModelForm):
    def __init__(self, for_list=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def save(self, commit=True):
        if self.instance.list_id is None:
            self.instance.list = List.objects.create()
        return super().save(commit)

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg'
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR},
            NON_FIELD_ERRORS: {
                'unique_together': DUPLICATE_ITEM_ERROR
            }
        }