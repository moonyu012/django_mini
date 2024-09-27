from django.urls import path
from users import views
from django.contrib.auth import views as auth_views # 자동으로 세션을 지워줌

# name 선언 이유 reverse 함수에서 쓰일 수 있음
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('verify/',views.VerifyEmailView.as_view(), name='verify'),
    path('login/',views.SessionLoginAPIView.as_view(),name='session_login'),
    path('logout/',views.SessionLogoutAPIView.as_view(),name='session_logout'),
]