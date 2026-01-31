from django.urls import path
from .views import house
urlpatterns = [
    path('', house, name = 'chat')
]