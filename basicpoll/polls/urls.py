from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [
    #ie: /polls/
    path("", views.IndexView.as_view(), name="index"),
    #ie: /polls/5/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    #ie: /polls/5/results/
    path("<int:pk>/results/", views.ResultView.as_view(), name="results"),
    #ie: /polls/5/vote
    path("<int:question_id>/vote/", views.vote, name="vote"),
]