from django.urls import path
from questions import views

app_name = 'questions'

urlpatterns = [
    path('', views.index, name='index'),
    path('hot', views.hot, name='hot'),
    path('tag/<str:tag>/', views.questions_by_tag, name='tag'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('ask/', views.ask_question, name='ask'),
]