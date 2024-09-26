from django.urls import path
from users import views

# name 선언 이유 reverse 함수에서 쓰일 수 있음
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
]