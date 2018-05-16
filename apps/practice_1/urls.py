from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.index),
    url(r"^register$", views.register),
    url(r"^login$", views.login),
    url(r"^logout$", views.logout),
    url(r"^books$", views.books),
    url(r"^books/add$", views.add),
    url(r"^delete$", views.delete_review),
    url(r"^books/add_book$", views.add_book),
    url(r"^books/add_review$", views.add_review),
    url(r"^books/(?P<number>\d+)$", views.show_book),
    url(r"^users/(?P<number>\d+)$", views.show_user)
]