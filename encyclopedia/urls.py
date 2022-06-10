from wsgiref.simple_server import WSGIRequestHandler
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_page, name="entry_page"),
    path("random_page", views.random_page, name="random_page"),
    path("edit_page/<str:title>", views.edit_page, name="edit_entry"),
    path("save_entry", views.save_new_entry, name="save_new_entry"),
    path("create_new", views.new_page, name = "create_new"),
    path("save_edit_entry/<str:title>", views.save_edit_entry, name = "save_edit_entry"),
    path("search_query", views.search_entry, name="search_query")
]
