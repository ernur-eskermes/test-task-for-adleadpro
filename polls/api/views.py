from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from polls.models import Poll, Question, Answer
from .serializers import (
    PollSerializer,
    QuestionSerializer,
    AnswerCreateSerializer,
    AnswerDetailSerializer,
)


class PollActiveListAPIView(generics.ListAPIView):
    serializer_class = PollSerializer

    def get_queryset(self):
        now = timezone.now()
        qs = Poll.objects.filter(
            start_date__lte=now,
            end_date__gte=now
        )
        return qs


class PollCreateAPIView(generics.CreateAPIView):
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticated]


class PollDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return super(PollDetailAPIView, self).get_permissions()


class QuestionListAPIView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionCreateAPIView(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]


class QuestionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return super(QuestionDetailAPIView, self).get_permissions()


class AnswerCreateAPIView(generics.CreateAPIView):
    serializer_class = AnswerCreateSerializer

    def perform_create(self, serializer):
        question = Question.objects.get(pk=self.kwargs['pk'])
        serializer.save(question=question)


class UserAnswerListAPIView(generics.ListAPIView):
    serializer_class = AnswerDetailSerializer

    def get_queryset(self):
        qs = Answer.objects.filter(
            user_id=self.kwargs['user_id']
        )
        return qs
