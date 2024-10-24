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
        return reservation_count



    def create(self, validated_data):
        # if 이미 해당 식당에 예약된 내역이 존재하면?
        # 예약을 받지 않고 에러를 반환한다.
        user = self.context.get('request').user
        print(self.context.get('request'))
        if Reservation.objects.filter(user=user, restaurant=validated_data['restaurant']).exists():
            raise serializers.ValidationError('이미 예약하신 내역이 존재합니다.')
        instance = self.Meta.model.objects.create(**validated_data)
        return instance

class ReservationInfoSerializer(serializers.ModelSerializer):
    reserver_info = serializers.SerializerMethodField()
    my_turn = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ['restaurant', 'headcount', 'reserver_info', 'my_turn']

    def get_reserver_info(self,obj):
        info = {
            "phone": obj.user.phone,
            "nickname": obj.user.nickname,
        }
        return info

    def get_my_turn(self, obj):
        my_turn = Reservation.objects.filter(
            restaurant=obj.restaurant,
            reserved_at__lte=obj.reserved_at,  # 현재 예약 시간보다 앞선 사람들
            status='PD'  # 예약 대기 중인 상태
        ).count()
        return my_turn

class ReservationUpdateSerializer(ReservationInfoSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(read_only=True)



