from django.shortcuts import get_object_or_404
from rest_framework import serializers

from polls.models import (
    Poll,
    Question,
    ChoiceAnswer,
    Answer,
)


class ChoiceAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceAnswer
        fields = (
            'id',
            'text',
            'correct',
        )


class QuestionSerializer(serializers.ModelSerializer):
    choiceanswer_set = ChoiceAnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'text',
            'type',
            'poll',
            'choiceanswer_set',
        )


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = (
            'id',
            'name',
            'start_date',
            'end_date',
            'description',
        )


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            'id',
            'user_id',
            'answer',
            'selected_answers'
        )

    def get_question(self):
        q_id = self.context['request'].parser_context['kwargs']['q_id']
        return get_object_or_404(Question, pk=q_id)

    def validate(self, attrs):
        q_id = self.context['request'].parser_context['kwargs']['q_id']
        if Answer.objects.filter(
            user_id=attrs['user_id'],
            question_id=q_id
        ).exists():
            raise serializers.ValidationError({
                "detail": "Вы уже ответили на этот вопрос"
            })
        return attrs

    def validate_answer(self, value):
        q_type = self.get_question().type
        if q_type in ['single', 'multiple'] and value:
            raise serializers.ValidationError({
                'detail': 'Данные не соответствует типам вопроса'
            })
        return value

    def validate_selected_answers(self, selected_answers):
        question = self.get_question()
        q_type = question.type
        count_answers = len(selected_answers)

        if q_type == 'text' and selected_answers:
            raise serializers.ValidationError({
                'detail': 'Данные не соответствует типам вопроса'
            })
        elif q_type == 'single' and count_answers != 1:
            raise serializers.ValidationError({
                'detail': 'Выберите один из вариантов ответа'
            })
        elif q_type == 'multiple' and count_answers <= 1:
            raise serializers.ValidationError({
                'detail': 'Выберите несколько вариантов ответа'
            })
        return selected_answers


class AnswerDetailSerializer(AnswerCreateSerializer):
    selected_answers = ChoiceAnswerSerializer(many=True)
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = (
            'id',
            'user_id',
            'answer',
            'selected_answers',
            'question',
        )
