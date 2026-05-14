from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Question, Tag
from django.contrib.auth.models import User
from django.db.models import Count, Sum



def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page


def get_common_context():
    popular_tags = Tag.objects.annotate(
        question_count=Count('questions')
    ).order_by('-question_count')[:10]

    # Получаем пользователей с реальной активностью
    best_members = User.objects.filter(
        questions__isnull=False  # Есть хотя бы один вопрос
    ).annotate(
        rating=Sum('questions__rating')  # Суммируем рейтинг вопросов
    ).order_by('-rating', 'id')[:5]

    return {
        'popular_tags': popular_tags,
        'best_members': best_members,
    }


def index(request):
    questions = Question.objects.new().select_related('author').prefetch_related('tags')

    questions = questions.annotate(answers_count=Count('answers'))

    page = paginate(questions, request)
    context = get_common_context()
    context.update({
        'questions': page.object_list,
        'page_obj': page
    })
    return render(request, 'questions/index.html', context)


def hot(request):
    questions = Question.objects.hot().select_related('author').prefetch_related('tags')
    questions = questions.annotate(answers_count=Count('answers'))

    page = paginate(questions, request)
    context = get_common_context()
    context.update({
        'questions': page.object_list,
        'page_obj': page
    })
    return render(request, 'questions/hot.html', context)


def questions_by_tag(request, tag):
    questions = Question.objects.by_tag(tag).select_related('author').prefetch_related('tags')
    questions = questions.annotate(answers_count=Count('answers'))

    context = get_common_context()

    if not questions.exists():
        context.update({
            'questions': None,
            'page_obj': None,
            'tag': tag
        })
        return render(request, 'questions/tag.html', context)

    page = paginate(questions, request)
    context.update({
        'questions': page.object_list,
        'page_obj': page,
        'tag': tag
    })
    return render(request, 'questions/tag.html', context)


def question_detail(request, question_id):
    question = get_object_or_404(
        Question.objects.select_related('author').prefetch_related('tags'),
        pk=question_id
    )
    answers = question.answers.select_related('author').order_by('-created_at')
    page = paginate(answers, request)

    context = get_common_context()
    context.update({
        'question': question,
        'answers': page.object_list,
        'page_obj': page
    })
    return render(request, 'questions/question.html', context)


def ask_question(request):
    context = get_common_context()
    return render(request, 'questions/ask.html', context)