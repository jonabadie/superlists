from django.shortcuts import render, redirect, get_object_or_404

from .models import Item, List


def home_page(request):
    return render(request, 'lists/home.html')


def view_list(request, list_id):
    list_ = get_object_or_404(List, pk=list_id)
    return render(request, 'lists/list.html', {'list': list_})


def new_list(request):
    text = request.POST.get('item_text')
    if text:
        list_ = List.objects.create()
        Item.objects.create(text=text, list=list_)
        return redirect(f'/lists/{list_.id}/')


def new_item(request, list_id):
    text = request.POST.get('item_text')
    list_ = get_object_or_404(List, pk=list_id)
    if text:
        Item.objects.create(text=text, list=list_)
        return redirect(f'/lists/{list_.id}/')