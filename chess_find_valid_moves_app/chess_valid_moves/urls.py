from django.urls import path
from .views import GetValidMovesView
urlpatterns = [
    path('<str:piece_type>', GetValidMovesView.as_view(), name='get_valid_moves'),
]
