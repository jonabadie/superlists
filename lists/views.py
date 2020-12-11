from django.shortcuts import render, redirect, get_object_or_404

from .models import Item, List


def home_page(request):
    return render(request, 'lists/home.html')


def view_list(request, list_id):
    list_ = get_object_or_404(List, pk=list_id)
    if request.method == 'POST':
        text = request.POST.get('item_text')
        if text:
            Item.objects.create(text=text, list=list_)
            return redirect('view-list', list_id=list_.id)
    return render(request, 'lists/list.html', {'list': list_})


def new_list(request):
    text = request.POST.get('item_text')
    if not text:
        error = "You can't have an empty list item"
        return render(request, 'lists/home.html', {'error': error})
    list_ = List.objects.create()
    Item.objects.create(text=text, list=list_)
    return redirect('view-list', list_id=list_.id)