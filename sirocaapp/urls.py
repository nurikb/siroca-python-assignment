from django.urls import path
from .views import get_index, make_request


urlpatterns = [
    path('', get_index),
    path('pulls', make_request, name='git_url'),
]