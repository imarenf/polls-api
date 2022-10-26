from django.db import models
from django.contrib.auth.models import User
from datetime import date


def get_anonymous_user():
    return User.objects.get(pk=2)


class Poll(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    start_date = models.DateField(verbose_name='Дата старта', auto_now_add=True)
    end_date = models.DateField(verbose_name='Дата окончания', default=date.today())
    context = models.TextField(blank=True, verbose_name='Описание')
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=get_anonymous_user())

    class Meta:
        verbose_name_plural = 'Опросы'
        verbose_name = 'Опрос'
        ordering = ['-end_date']


class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200, verbose_name='Вопрос')

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name_plural = 'Вопросы'
        verbose_name = 'Вопрос'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=300, verbose_name='Ответ')
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=get_anonymous_user())

    def __str__(self):
        return self.answer_text

    class Meta:
        verbose_name_plural = 'Ответы'
        verbose_name = 'Ответ'
