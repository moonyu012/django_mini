from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # 보안을 위해 따로 설정 입력을 받고 읽을 수 는 없음
    class Meta:
        model = User
        exclude =['is_active', 'is_superuser', 'last_login', 'groups', 'user_permissions'] # 제외 시킬 필드 지정