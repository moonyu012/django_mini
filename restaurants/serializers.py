from django.contrib.auth import get_user_model
from rest_framework import serializers
from restaurants.models import Restaurant
from users.serializers import UserSerializer

User = get_user_model()


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class RestaurantDetailSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Restaurant
        exclude = ['id']
