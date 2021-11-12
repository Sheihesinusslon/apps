from django.urls import path
from .views import main_view, word_view

urlpatterns = [
    path('', main_view, name='main'),
    path('word', word_view, name='word'),
    path('error', word_view, name='word')
]