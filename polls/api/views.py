from django.utils import timezone
from rest_framework import generics

from polls.models import Poll, Answer
from .serializers import (
    PollSerializer,
    AnswerCreateSerializer,
    AnswerDetailSerializer,
)


class PollActiveListAPIView(generics.ListAPIView):
    serializer_class = PollSerializer

    def get_queryset(self):
        now = timezone.now()
        return Poll.objects.filter(start_date__lte=now, end_date__gte=now)


class AnswerCreateAPIView(generics.CreateAPIView):
    serializer_class = AnswerCreateSerializer

    def perform_create(self, serializer):
        serializer.save(question_id=self.kwargs['q_id'])


class UserAnswerListAPIView(generics.ListAPIView):
    serializer_class = AnswerDetailSerializer

    def get_queryset(self):
        return Answer.objects.filter(user_id=self.kwargs['pk'])
