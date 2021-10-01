from django.db import models


class Poll(models.Model):
    name = models.CharField(
        'Название',
        max_length=255
    )
    start_date = models.DateTimeField(
        'Дата старта',
    )
    end_date = models.DateTimeField(
        'Дата окончания',
    )
    description = models.TextField(
        'Описание',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Question(models.Model):
    text = models.CharField(
        'Текст вопроса',
        max_length=500
    )
    TYPE_CHOICES = (
        ('text', 'Текст'),
        ('single', 'Выбор одного варианта'),
        ('multiple', 'Выбор нескольких вариантов'),
    )
    type = models.CharField(
        'Тип вопроса',
        choices=TYPE_CHOICES,
        max_length=50
    )
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        verbose_name='Опрос',
    )

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class ChoiceAnswer(models.Model):
    text = models.TextField(
        'Текст',
    )
    correct = models.BooleanField(
        'Верный ответ',
        default=False
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='Вопрос',
    )

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Ответ для выбора'
        verbose_name_plural = 'Ответы для выбора'


class Answer(models.Model):
    user_id = models.IntegerField(
        'ID пользователя',
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='Вопрос',
    )
    answer = models.TextField(
        'Ответ',
        help_text='Ответ пользователя в виде текста',
        blank=True
    )
    selected_answers = models.ManyToManyField(
        ChoiceAnswer,
        verbose_name='Выбранные пользователем ответы',
        blank=True
    )

    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
