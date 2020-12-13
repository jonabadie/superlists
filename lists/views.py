from django.shortcuts import render, redirect, get_object_or_404

from .models import Item, List
from .forms import ItemForm


def home_page(request):
    return render(request, 'lists/home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = get_object_or_404(List, pk=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'lists/list.html', {'list': list_, 'form': form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        item = form.save()
        return redirect(item.list)
    else:
        return render(request, 'lists/home.html', {'form': form})
