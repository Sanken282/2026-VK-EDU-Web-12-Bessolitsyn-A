from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

QUESTIONS = [
    {
        'id': i,
        'title': f'Question title {i}',
        'text': f'Text {i}',
        'rating': (i * 5)%7,
        'answers_count': (i * 3)%21,
        'tags': ['moon', 'bender'] if i % 2 == 0 else ['light', 'dark'],
        'time': i,
    }
    for i in range(1,31)
]

def index(request):
    # page_number = int(request.GET.get('page',1))
    # page = Paginator(QUESTIONS, 5)
    # page_obj = page.page(page_number)
    page = paginate(QUESTIONS, request)

    return render(request, 'questions/index.html', context={'questions': page.object_list, 'page_obj': page})

def hot(request):
    page = paginate(QUESTIONS[::-1], request)
    return render(request, 'questions/hot.html', context={'questions': page.object_list, 'page_obj': page})


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

def questions_by_tag(request, tag):
    filtered_questions = [q for q in QUESTIONS if tag in q['tags']]
    page = paginate(filtered_questions, request)
    return render(request, 'questions/tag.html', context={'questions': page.object_list, 'page_obj': page, 'tag': tag})


def question_detail(request, question_id):
    question = next((q for q in QUESTIONS if q['id'] == question_id), QUESTIONS[0])

    # Генерация ответов-заглушек
    ANSWERS = [
        {
            'id': i,
            'text': f'Answer text {i}',
            'rating': (i * 3)%10,
            'author': f'user{i}',
            'time': i,
        }
        for i in range(1, 21)
    ]

    page = paginate(ANSWERS, request)
    return render(request, 'questions/question.html', context={
        'question': question,
        'answers': page.object_list,
        'page_obj': page
    })


def ask_question(request):
    return render(request, 'questions/ask.html')


