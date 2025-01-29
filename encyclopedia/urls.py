from django.urls import path

from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("Create_New_Page", views.newpage, name="newpage"),
    path('Edit/<str:edit_page>', views.edit, name="edit"),
    path("<str:page>", views.article, name="article"),
    path("<str:randomfile>", views.random_page, name="random_page")
]

