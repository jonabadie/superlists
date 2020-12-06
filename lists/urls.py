from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.new_list, name='new-list'),
    path('<int:list_id>/', views.view_list, name='view-list'),
    path('<int:list_id>/add_item', views.new_item, name='add-item'),
]
