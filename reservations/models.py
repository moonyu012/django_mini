from django.db import models


class Reservation(models.Model):
    StatusChoices = [
        ('PD', 'Pending'),
        ('CF', 'Confirm'),
        ('CC', 'Canceled'),
        ('NS', 'No Show'),
        ('ET', 'Entered')
    ]

    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.RESTRICT, related_name='reservations')
    user = models.ForeignKey('users.User', on_delete=models.RESTRICT, related_name='customers')
    reserve_at = models.DateTimeField(auto_now_add=True)  # 줄서기를 누른 시점
    headcount = models.PositiveIntegerField()  # 예약 인원 수
    status = models.CharField(choices=StatusChoices, default='PD')  # 예약의 상태

    def __str__(self):
        return f'{self.user}의 {self.restaurant} 예약내역'

