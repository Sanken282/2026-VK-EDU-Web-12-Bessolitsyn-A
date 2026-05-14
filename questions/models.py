from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class TagManager(models.Manager):
    def popular(self):
        return self.annotate(question_count=models.Count('questions')).order_by('-question_count')


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    objects = TagManager()

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def new(self):
        """Новые вопросы (по дате создания)"""
        return self.order_by('-created_at')

    def hot(self):
        """Лучшие вопросы (по рейтингу)"""
        return self.order_by('-rating')

    def by_tag(self, tag_name):
        """Вопросы по тегу"""
        return self.filter(tags__name=tag_name)


class Question(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст вопроса')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', verbose_name='Автор')
    tags = models.ManyToManyField(Tag, related_name='questions', verbose_name='Теги', blank=True)
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    objects = QuestionManager()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('questions:question_detail', kwargs={'question_id': self.pk})

    def get_answers_count(self):
        return self.answers.count()


class AnswerManager(models.Manager):
    def hot(self):
        """Лучшие ответы (по рейтингу)"""
        return self.order_by('-rating')


class Answer(models.Model):
    text = models.TextField(verbose_name='Текст ответа')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers', verbose_name='Автор')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    objects = AnswerManager()

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Ответ на "{self.question.title}" от {self.author.username}'


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_likes', verbose_name='Пользователь')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes', verbose_name='Вопрос')
    value = models.SmallIntegerField(choices=[(1, 'Лайк'), (-1, 'Дизлайк')], verbose_name='Оценка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Лайк вопроса'
        verbose_name_plural = 'Лайки вопросов'
        unique_together = ['user', 'question']

    def __str__(self):
        return f'Лайк вопроса "{self.question.title}" от {self.user.username}'


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_likes', verbose_name='Пользователь')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes', verbose_name='Ответ')
    value = models.SmallIntegerField(choices=[(1, 'Лайк'), (-1, 'Дизлайк')], verbose_name='Оценка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Лайк ответа'
        verbose_name_plural = 'Лайки ответов'
        unique_together = ['user', 'answer']

    def __str__(self):
        return f'Лайк ответа на "{self.answer.question.title}" от {self.user.username}'