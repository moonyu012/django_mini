from django.urls import path
from reservations import views

urlpatterns = [
    path("",views.ReservationCreateView.as_view(),name='create'),
]