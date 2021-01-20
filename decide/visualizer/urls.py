from django.urls import path
from .views import StatisticsView
from .views import get_list_votings
from .views import VisualizerView, get_global_view

urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('global', get_global_view),
    path('<int:voting_id>/statistics', StatisticsView.as_view()),
    path('', get_list_votings),
]

