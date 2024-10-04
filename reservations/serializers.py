from rest_framework import serializers
from reservations.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    reserver_info = serializers.SerializerMethodField()
    reservation_turn = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ['restaurant','headcount','reserver_info','reservation_turn']

    def get_reserver_info(self,obj):
        info = {
            "phone": obj.user.phone,
            "nickname": obj.user.nickname,
        }
        return info

    def get_reservation_turn(self, obj):
        reservation_count = obj.restaurant.reservations.filter(status='PD').count() # 대기중인 상태만 가져와서 카운트
        if reservation_count != 0:
            return reservation_count + 1
        return 1

    def create(self,validated_data):
        pass
        # if 이미 해당 식당에 예약된 내역이 존재하면?
        # 예약을 받지 않고 기존에 있는 예약을 반환한다.

