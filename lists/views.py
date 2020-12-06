from django.shortcuts import render, redirect

from .models import Item


def home_page(request):
    return render(request, 'lists/home.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})


def new_list(request):
    text = request.POST.get('item_text')
    Item.objects.create(text=text) if text else None
    return redirect('/lists/the-only-list-in-the-world/')