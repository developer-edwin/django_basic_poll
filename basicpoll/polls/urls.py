from django.urls import path

from . import views

urlpatterns = [
    #ie: /polls/
    path("", views.index, name="index"),
    #ie: /polls/5/
    path("<int:question_id>/", views.detail, name="index"),
    #ie: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="index"),
    #ie: /polls/5/vote
    path("<int:question_id>/vote/", views.vote, name="index"),
]