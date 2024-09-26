from django.core import signing
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users import serializers


# generics : mixins -> CreateModelMixin : 검증해주는 기본 폼이 있는 메서드
class SignUpView(CreateAPIView):
    permission_classes = [AllowAny] # 회원 가입은 모든 유저가 접근이 가능해야함
    serializer_class = serializers.SignUpSerializer


    def perform_create(self, serializer): # 이메일 인증 기능
        user = serializer.save() # save 기능: 저장된 값을 리턴해줌 user 변수에 저장
        signer = signing.TimestampSigner() # 서명기능을 제공하고 특정 시간 동안만 secret_key 를 가지고 특정한 값을 암호화
        signed_user_email = signer.sign(user.email)
        signer_dump = signing.dumps(signed_user_email)

        # http://127.0.0.1:8000/users/verify/?code={signer_dump}/
        self.verify_link = self.request.build_absolute_uri(f'/users/verify/?code={signer_dump}/') # 사용자가 보낸 url뒤에 붙여줌
        subject = '[Tabling] 회원가입 인증 메일입니다.'
        message = f'안녕하세요. {user.email}님, 회원가입을 완료하기 위해 아래 링크를 클릭해주세요.\n{self.verify_link}'


        send_mail(subject, message, settings.EMAIL_HOST_USER,[user.email])