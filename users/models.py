from  django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserManager(BaseUserManager): # User 모델에 대한 CRUD 작업을 가능하게 해주는 클래스

    def create_user(self, email, password,**extra_fields): # 새로운 유저 생성
        if email is None:
            raise ValueError('Users must have an email address')
        if password is None:
            raise ValueError('Users must have a password')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db) # _db 디폴드 값으로 지정한 데이터베이스에 저장하겠다

        return user

    def create_superuser(self, email, password, **extra_fields): # 관리자 계정 생성
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(email, password, **extra_fields)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    GenderChoice = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    email = models.EmailField(max_length=30, unique=True) # 이메일
    is_active = models.BooleanField(default=False) # 이메일 인증 여부에 따라 필드 수정하고 싶기 떄문에 초기 선언을 다시 해줌
    phone = models.CharField(max_length=13, unique=True) # 전화번호
    nickname = models.CharField(max_length=12) # 이름(닉네임)
    birthday = models.DateField(null=True, blank=True) # 생일
    gender = models.CharField(choices=GenderChoice) # 성별
    is_owner = models.BooleanField(default=False) # 사용자인지 오너인지 여부

    objects = UserManager()

    USERNAME_FIELD = 'email'

