from django.shortcuts import render, redirect

from .models import Item


def home_page(request):
    if request.method == 'POST':
        text = request.POST.get('item_text')
        Item.objects.create(text=text) if text else None
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'lists/home.html', {'items': items})
