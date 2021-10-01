from django.contrib import admin

from .models import (
    Poll,
    Question,
    ChoiceAnswer,
    Answer
)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_id',
        'question',
    )


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'start_date',
        'end_date',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'start_date',
        'end_date',
    )


class ChoiceAnswerInline(admin.StackedInline):
    model = ChoiceAnswer
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'type',
        'poll',
    )
    search_fields = (
        'text',
    )
    list_filter = (
        'type',
    )
    inlines = [ChoiceAnswerInline]
