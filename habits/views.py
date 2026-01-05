from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginators import HabitListPagination
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitViewSet(ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitListPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "destroy", "retrieve"]:
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class PublicHabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitListPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
