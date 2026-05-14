Как запустить проект AskPupkin

Локальный запуск (через venv):

1. Убедитесь, что установлен Python 3.12 и PostgreSQL
2. Создайте базу данных PostgreSQL:
   CREATE DATABASE askpupkin;
   CREATE USER askpupkin_user WITH PASSWORD 'qwer1234';
   GRANT ALL PRIVILEGES ON DATABASE askpupkin TO askpupkin_user;
3. Скопируйте .env.example в .env.local и при необходимости отредактируйте
4. Создайте виртуальное окружение:
   python -m venv venv
5. Активируйте виртуальное окружение:
   Windows: venv\Scripts\activate
   Linux/Mac: source venv/bin/activate
6. Установите зависимости:
   pip install -r requirements.txt
7. Выполните миграции:
   python manage.py migrate
8. Создайте суперпользователя (опционально):
   python manage.py createsuperuser
9. Запустите сервер:
   python manage.py runserver
10. Откройте в браузере http://127.0.0.1:8000


Запуск через Docker Compose:

1. Убедитесь, что установлены Docker и Docker Compose
2. Скопируйте .env.example в .env.docker (можно оставить как есть)
3. Соберите и запустите контейнеры:
   docker compose up --build
4. В другом терминале выполните миграции:
   docker compose exec web python manage.py migrate
5. Создайте суперпользователя (опционально):
   docker compose exec web python manage.py createsuperuser
6. Откройте в браузере http://localhost:8000

Остановка Docker: нажмите Ctrl+C или выполните docker compose down


Основные страницы:

Главная (новые вопросы) - /
Лучшие вопросы - /hot
Вопросы по тегу - /tag/название/
Страница вопроса - /question/номер/
Задать вопрос - /ask/
Вход - /login/
Регистрация - /signup/
Профиль - /profile/
Админка - /admin/

Наполнение базы тестовыми данными:

python manage.py fill_db 10
(где 10 - коэффициент: пользователи = ratio, вопросы = ratio*10, ответы = ratio*100)

Страницы (роуты) проекта:

/ - Главная (список новых вопросов)
/hot - Лучшие вопросы
/tag/<название>/ - Вопросы по тегу
/question/<id>/ - Страница вопроса с ответами
/ask/ - Задать новый вопрос
/login/ - Вход
/signup/ - Регистрация
/profile/ - Профиль пользователя
/settings/ - Настройки профиля
/admin/ - Админ-панель