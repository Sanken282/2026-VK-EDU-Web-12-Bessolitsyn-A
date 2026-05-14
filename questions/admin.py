from django.contrib import admin
from .models import Tag, Question, Answer, QuestionLike, AnswerLike


class AnswerInline(admin.TabularInline):
    """Инлайн для отображения ответов на странице вопроса"""
    model = Answer
    extra = 0
    raw_id_fields = ['author']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'rating', 'created_at', 'get_answers_count']
    list_filter = ['tags', 'created_at']
    search_fields = ['title', 'text']
    raw_id_fields = ['author']
    filter_horizontal = ['tags']
    inlines = [AnswerInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author').prefetch_related('tags')

    def get_answers_count(self, obj):
        return obj.answers.count()

    get_answers_count.short_description = 'Количество ответов'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'author', 'rating', 'is_correct', 'created_at']
    list_filter = ['is_correct', 'created_at']
    search_fields = ['text']
    raw_id_fields = ['question', 'author']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('question', 'author')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'value', 'created_at']
    list_filter = ['value']
    raw_id_fields = ['user', 'question']


@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'answer', 'value', 'created_at']
    list_filter = ['value']
    raw_id_fields = ['user', 'answer']