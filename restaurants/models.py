from django.db import models


class Restaurant(models.Model):
    TYPE = [
        ('KOREAN', '한식'),
        ('CHINESE', '중식'),
        ('WESTERN', '양식'),
        ('JAPANESE', '일식'),
        ('OTHER', '기타')
    ]
    DAYS_OF_WEEK = [
        ('MON', '월요일'),
        ('TUE', '화요일'),
        ('WED', '수요일'),
        ('THU', '목요일'),
        ('FRI', '금요일'),
        ('SAT', '토요일'),
        ('SUN', '일요일')
    ]
    owner = models.ForeignKey('users.User', on_delete=models.RESTRICT, related_name='restaurants')
    name = models.CharField(max_length=30)
    # 식당 종류(한식, 중식, 양식, 일식 등)
    type = models.CharField(choices=TYPE, max_length=10)
    description = models.TextField(null=True, blank=True)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    # 정기휴무일
    regular_holiday = models.CharField(choices=DAYS_OF_WEEK, max_length=3, null=True, blank=True)
    # 라스트 오더 시간
    last_order = models.TimeField(null=True, blank=True)
    # 음식점 주소
    address = models.CharField(max_length=200)
    # 음식점 연락처
    contact = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/restaurants')


class Menu(models.Model):
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete = models.CASCADE, related_name ='menu')
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/menu')

    def __str__(self):
        return self.name
