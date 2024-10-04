from django.urls import path
from restaurants import views



urlpatterns = [
    path('',views.RestaurantListCreateAPIView.as_view(),name='list_create'),
    path('<int:pk>/',views.RestaurantDetailAPIView.as_view(),name='restaurant_detail'),
]