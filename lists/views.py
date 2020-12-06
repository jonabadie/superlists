from django.shortcuts import render, redirect

from .models import Item, List


def home_page(request):
    return render(request, 'lists/home.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})


def new_list(request):
    text = request.POST.get('item_text')
    if text:
        Item.objects.create(text=text, list=List.objects.create())
    return redirect('/lists/the-only-list-in-the-world/')