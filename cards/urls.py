from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.CardListView.as_view(),
        name="home",
    ),
    path(
        "new",
        views.CardCreateView.as_view(),
        name="card-create"
    ),
    path(
        "edit/<int:pk>",
        views.CardUpdateView.as_view(),
        name="card-update"
    ),
]