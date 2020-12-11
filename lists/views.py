from django.shortcuts import render, redirect, get_object_or_404

from .models import Item, List
from .forms import ItemForm


def home_page(request):
    return render(request, 'lists/home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = get_object_or_404(List, pk=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST.get('text'), list=list_)
            return redirect(list_)
    return render(request, 'lists/list.html', {'list': list_, 'form': form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        Item.objects.create(text=request.POST.get('text'), list=list_)
        return redirect(list_)
    else:
        return render(request, 'lists/home.html', {'form': form})
