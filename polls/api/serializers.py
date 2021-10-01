from rest_framework import serializers

from polls.models import (
    Poll,
    Question,
    ChoiceAnswer,
    Answer,
)


class ChoiceAnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ChoiceAnswer
        fields = (
            'id',
            'text',
            'correct',
        )


class QuestionSerializer(serializers.ModelSerializer):
    choiceanswer_set = ChoiceAnswerSerializer(many=True)

    def create(self, validated_data):
        question = Question.objects.create(
            text=validated_data['text'],
            type=validated_data['type'],
            answer=validated_data['answer'],
            poll_id=self.context['request'].parser_context['kwargs']['poll_id'],
        )
        for choice_answer in validated_data['choiceanswer_set']:
            ChoiceAnswer.objects.create(
                text=choice_answer['text'],
                correct=choice_answer['correct'],
                question=question
            )
        return question

    def update(self, instance, validated_data):
        for field in ['text', 'type']:
            if validated_data.get(field):
                setattr(instance, field, validated_data[field])
        instance.save()
        for choice_answer in validated_data.get('choiceanswer_set', []):
            choice_answer_obj = ChoiceAnswer.objects.filter(
                id=choice_answer['id']
            ).first()
            for field in ['text', 'correct']:
                if choice_answer.get(field) is not None:
                    setattr(choice_answer_obj, field, choice_answer[field])
            choice_answer_obj.save()
        return instance

    class Meta:
        model = Question
        fields = (
            'id',
            'text',
            'type',
            'poll',
            'choiceanswer_set',
        )
        extra_kwargs = {
            'poll': {'read_only': True}
        }


class PollSerializer(serializers.ModelSerializer):
    question_set = QuestionSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        if instance.start_date != validated_data.get('start_date'):
            raise serializers.ValidationError({
                'error': 'Вы не можете изменить дату начала опроса'
            })
        return super(PollSerializer, self).update(
            instance,
            validated_data
        )

    class Meta:
        model = Poll
        fields = (
            'id',
            'name',
            'start_date',
            'end_date',
            'description',
            'question_set',
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

    def validate(self, attrs):
        question = Question.objects.get(
            pk=self.context['request'].parser_context['kwargs']['pk']
        )
        answer = Answer.objects.filter(
            user_id=attrs['user_id'],
            question=question
        ).exists()
        if answer:
            raise serializers.ValidationError({
                'error': 'Вы уже ответили на этот вопрос'
            })
        type = question.type
        count_answers = len(attrs['selected_answers'])
        if type == 'text' and attrs['selected_answers'] or \
                type in ['single', 'multiple'] and attrs['answer']:
            raise serializers.ValidationError({
                'error': 'Данные не соответствует типам вопроса'
            })
        elif type == 'single' and count_answers != 1:
            raise serializers.ValidationError({
                'error': 'Выберите один из вариантов ответа'
            })
        elif type == 'multiple' and count_answers <= 1:
            raise serializers.ValidationError({
                'error': 'Выберите несколько вариантов ответа'
            })
        for selected_answer in attrs['selected_answers']:
            if not question.choiceanswer_set.filter(
                    pk=selected_answer.pk
            ).exists():
                raise serializers.ValidationError({
                    'error': 'Ваш вариант ответа не является '
                             'вариантом ответа на вопрос'
                })
        return attrs


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
