from django.urls import path
from reservations import views

urlpatterns = [
    path("",views.ReservationCreateAPIView.as_view(),name='create'),
    path("info/",views.ReservationInfoAPIView.as_view(),name='info'),
    path("<int:pk>/",views.ReservationUpdateDestroyAPIView.as_view(),name='detail'),
    path("<int:pk>/entered/",views.EnterRestaurantAPIView.as_view(),name='entered'),
    path("<int:pk>/canceled/",views.CancelReservationAPIView.as_view(),name='canceled'),
    path("<int:pk>/noshow/",views.NoShowReservationAPIView.as_view(),name='noshow'),
]