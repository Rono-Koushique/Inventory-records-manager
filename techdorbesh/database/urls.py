from django.urls import path
from . import views

urlpatterns = [
    path('', views.db_home, name='db_home'),
    path('AddRecord', views.db_addrecord, name='db_addrecord'),
    path('Inventory', views.db_inventory, name='db_inventory'),
    path('Records', views.db_records, name='db_records'),
    path('Logout', views.db_logout, name='db_logout')
]