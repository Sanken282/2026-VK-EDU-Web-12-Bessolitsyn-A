import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from core.models import Profile
from questions.models import Tag, Question, Answer, QuestionLike, AnswerLike

fake = Faker()


class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio coefficient for data generation')

    def handle(self, *args, **options):
        ratio = options['ratio']

        self.stdout.write('Starting database population...')

        users = self.create_users(ratio)

        self.create_profiles(users)

        tags = self.create_tags(ratio)

        questions = self.create_questions(ratio * 10, users, tags)

        answers = self.create_answers(ratio * 100, questions, users)

        self.create_likes(ratio * 200, users, questions, answers)

        self.stdout.write(self.style.SUCCESS(f'Database populated successfully with ratio={ratio}'))

    def create_users(self, count):
        self.stdout.write(f'Creating {count} users...')
        users = []

        batch_size = 1000
        for i in range(0, count, batch_size):
            batch = []
            end = min(i + batch_size, count)
            for j in range(i, end):
                username = f'user_{fake.user_name()}_{j}'
                batch.append(User(
                    username=username,
                    email=fake.email(),
                    password='pbkdf2_sha256$...'
                ))
            User.objects.bulk_create(batch)
            users.extend(User.objects.filter(id__gt=0).order_by('-id')[:len(batch)])

        return User.objects.all()

    def create_profiles(self, users):
        self.stdout.write('Creating profiles...')
        profiles = []
        for user in users:
            profiles.append(Profile(user=user))

        Profile.objects.bulk_create(profiles, batch_size=1000)

    def create_tags(self, count):
        self.stdout.write(f'Creating {count} tags...')
        tags = []

        tag_names = set()
        while len(tag_names) < count:
            tag_names.add(fake.word())

        batch_size = 1000
        tag_names = list(tag_names)
        for i in range(0, count, batch_size):
            batch = [Tag(name=name) for name in tag_names[i:i + batch_size]]
            Tag.objects.bulk_create(batch)

        return Tag.objects.all()

    def create_questions(self, count, users, tags):
        self.stdout.write(f'Creating {count} questions...')
        questions = []
        tags_list = list(tags)
        users_list = list(users)

        batch_size = 1000
        for i in range(0, count, batch_size):
            batch = []
            end = min(i + batch_size, count)
            for _ in range(i, end):
                question = Question(
                    title=fake.sentence()[:200],
                    text=fake.text(),
                    author=random.choice(users_list),
                    rating=random.randint(-10, 100)
                )
                batch.append(question)

            Question.objects.bulk_create(batch)
            questions.extend(Question.objects.filter(id__gt=0).order_by('-id')[:len(batch)])

        self.stdout.write('Adding tags to questions...')
        through_model = Question.tags.through
        through_objects = []

        for question in questions:
            question_tags = random.sample(tags_list, random.randint(1, 5))
            for tag in question_tags:
                through_objects.append(
                    through_model(question_id=question.id, tag_id=tag.id)
                )

        through_model.objects.bulk_create(through_objects, batch_size=5000)

        return Question.objects.all()

    def create_answers(self, count, questions, users):
        self.stdout.write(f'Creating {count} answers...')
        answers = []
        questions_list = list(questions)
        users_list = list(users)

        batch_size = 1000
        for i in range(0, count, batch_size):
            batch = []
            end = min(i + batch_size, count)
            for _ in range(i, end):
                answer = Answer(
                    text=fake.text(),
                    question=random.choice(questions_list),
                    author=random.choice(users_list),
                    rating=random.randint(-5, 50)
                )
                batch.append(answer)

            Answer.objects.bulk_create(batch)

        return Answer.objects.all()

    def create_likes(self, count, users, questions, answers):
        self.stdout.write(f'Creating {count} likes...')
        questions_list = list(questions)
        answers_list = list(answers)
        users_list = list(users)

        question_likes = []
        question_like_pairs = set()

        for _ in range(count // 2):
            user = random.choice(users_list)
            question = random.choice(questions_list)
            pair = (user.id, question.id)

            if pair not in question_like_pairs:
                question_like_pairs.add(pair)
                question_likes.append(
                    QuestionLike(
                        user=user,
                        question=question,
                        value=random.choice([1, -1])
                    )
                )

        QuestionLike.objects.bulk_create(question_likes, batch_size=5000)

        answer_likes = []
        answer_like_pairs = set()

        for _ in range(count // 2):
            user = random.choice(users_list)
            answer = random.choice(answers_list)
            pair = (user.id, answer.id)

            if pair not in answer_like_pairs:
                answer_like_pairs.add(pair)
                answer_likes.append(
                    AnswerLike(
                        user=user,
                        answer=answer,
                        value=random.choice([1, -1])
                    )
                )

        AnswerLike.objects.bulk_create(answer_likes, batch_size=5000)