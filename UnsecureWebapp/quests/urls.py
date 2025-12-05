from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:quest_id>/nextQuest/", views.nextQuest, name="nextQuest"),
    path("<int:quest_id>/", views.quest, name="Quest")
]