from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer): # ModelSerializer: request 데이터 넘겨받고 검증 후 세이브 업데이트 메서드를 통해서 디비에 쿼리를 날려줌
    password = serializers.CharField(write_only=True) # 보안을 위해 따로 설정 입력을 받고 읽을 수 는 없음
    class Meta:
        model = User
        exclude =['is_active', 'is_superuser', 'last_login', 'groups', 'user_permissions'] # 제외 시킬 필드 지정



    def create(self,validated_data): # 비밀번호 해시화
        user = super().create(validated_data)
        if validated_data.get('password'): # 유효성 검증을 통과한 데이터에 비번이 있으면 해시화 진행
            user.set_password(validated_data.get('password')) # 받은 비번을 해시화
            user.save()
        else:
            raise serializers.ValidationError(
                detail='Password is required.',code='password'
            )
        return user



class UserLoginSerializer(serializers.Serializer): # Serializer: 선언한 필드에 대해서 올바르게 데이터가 넘어왔는지만 검증만 해줌
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs): # attrs 선언한 필드
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), **attrs) # authenticate 유저가 올바른지 is_active True인지 검증
            if not user:
                raise serializers.ValidationError(
                    detail='Unable to log in with provided credentials.', code='authorization'
                )
        else:
            raise serializers.ValidationError(
                detail='Must be Required "email" and "password".', code='authorization'
            )

        attrs['user'] = user # 임의로 유저라는 key에 user 반환
        return attrs # 뷰에서 사용 가능

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','is_owner','phone','nickname']
    