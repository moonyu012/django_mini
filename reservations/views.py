from django.contrib.auth.models import AnonymousUser
from rest_framework import mixins, status, permissions
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from reservations.models import Reservation
from reservations import serializers
from restaurants.views import IsOwner


class ReservationCreateAPIView(CreateAPIView):
    serializer_class = serializers.ReservationSerializer
    queryset = Reservation.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReservationInfoAPIView(ListAPIView):
    serializer_class = serializers.ReservationSerializer
    queryset = Reservation.objects.all()


class ReservationUpdateDestroyAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    serializer_class = serializers.ReservationUpdateSerializer
    queryset = Reservation.objects.all()

    def get_object(self):
        reservation = self.queryset.filter(pk=self.kwargs.get("pk"), user=self.request.user).first()
        return reservation

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if not instance:
            return Response({"detail": "다른 유저의 잘못된 요청 입니다."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({"detail": "다른 유저의 잘못된 요청 입니다."}, status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class IsRestaurantOwner(IsOwner):
    def has_object_permission(self, request, view, obj):  # Put, Patch, Delete 요청 시 필요한 권한 점검
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.restaurant.owner == request.user


class ChangeReservationStatusBaseView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsRestaurantOwner]
    change_status = None

    def get_object(self):
        return Reservation.objects.get(pk=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = self.change_status
        instance.save()
        return Response(
            {"detail": f"{instance.user.nickname} was {instance.get_status_display()}."},
            status=status.HTTP_200_OK
        )


class EnterRestaurantAPIView(ChangeReservationStatusBaseView):
    change_status = "ET"


class CancelReservationAPIView(ChangeReservationStatusBaseView):
    change_status = "CC"


class NoShowReservationAPIView(ChangeReservationStatusBaseView):
    change_status = "NS"