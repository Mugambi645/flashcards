from django.urls import path
# from django.views.generic import TemplateView
from . import views
urlpatterns = [
    path(
        "",
        #TemplateView.as_view(template_name="cards/base.html"),
        views.CardListView.as_view(),
        name="home",
    ),
    path(
        "new",
        views.CardCreateView.as_view(),
        name="card-create"
    ),

]