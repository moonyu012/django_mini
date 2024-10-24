from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from restaurants.models import Restaurant, Menu
from restaurants import serializers
from rest_framework import permissions

from django.contrib.auth.models import User, AnonymousUser


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):  # Put, Patch, Delete 요청 시 필요한 권한 점검
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

    def has_permission(self, request, view):  # Post 요청 시 필요한 권한 점검
        if not isinstance(request.user, AnonymousUser):  # 인증되지 않은 유저가 아니라면
            if request.method in permissions.SAFE_METHODS:  # 안전한 메소드 (GET 인지 확인)
                return True  # True를 반환하여 권한 인증 성공
            return request.user.is_owner  # 안전한 메소드가 아닌경우 is_owner가 True인지 확인
        return False  # AnonymousUser 이면 인증되지않은 유저이므로 무조건 False


class IsRestaurantOwner(IsOwner):

    def has_object_permission(self, request, view, obj):  # Put, Patch, Delete 요청 시 필요한 권한 점검
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.restaurant.owner == request.user


class RestaurantListCreateAPIView(ListCreateAPIView): # get 요청으로 식당 list 가져오고 create: post요청
    permission_classes = [permissions.IsAuthenticated, IsOwner] # 요청 보낸 사람이 로그인 되어 있는 유저인지먼저 확인
    serializer_class = serializers.RestaurantSerializer
    queryset = Restaurant.objects.all()




class RestaurantDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.RestaurantDetailSerializer
    queryset = Restaurant.objects.all()
    permission_classes = [IsOwner]
    # lookup_field = 'restaurant_id'
    #
    # def get_object(self):
    #     return self.queryset.get(id=self.kwargs['restaurant_id'])


class MenuCreateAPIView(CreateAPIView):
    serializer_class = serializers.MenuSerializer
    queryset = Menu.objects.all()
    permission_classes = [IsAuthenticated,IsRestaurantOwner]

class MenuDeleteAPIView(DestroyAPIView):
    queryset = Menu.objects.all()
    permission_classes = [IsAuthenticated,IsRestaurantOwner]


