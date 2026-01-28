from django.urls import path
from .views import house
urlpatterns = [
    path('chat/', house, name = 'chat')
]