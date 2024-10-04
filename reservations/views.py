from rest_framework.generics import CreateAPIView
from reservations.models import Reservation
from reservations import serializers


class ReservationCreateView(CreateAPIView):
    serializer_class = serializers.ReservationSerializer
    queryset = Reservation.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


