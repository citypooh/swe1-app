from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from polls.models import Question, Choice


class Command(BaseCommand):
    help = "Create sample poll data and admin user"

    def handle(self, *args, **options):
        # Create admin user if it doesn't exist
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin", email="admin@example.com", password="admin123"
            )
            self.stdout.write(self.style.SUCCESS("✅ Admin user created!"))
        else:
            self.stdout.write(self.style.WARNING("⚠️ Admin user already exists"))

        # Clear existing questions
        Question.objects.all().delete()
        self.stdout.write("🗑️ Cleared existing questions")

        # Create sample questions
        questions_data = [
            {
                "question_text": (
                    "What is the most challenging part of "
                    "Software Engineering assignments?"
                ),
                "pub_date": timezone.now() - timedelta(days=2),
                "choices": [
                    ("Django Web Development", 5),
                    ("CI/CD Pipeline Setup", 8),
                    ("AWS Deployment", 3),
                    ("Writing Tests", 4),
                ],
            },
            {
                "question_text": "What is your favorite programming language?",
                "pub_date": timezone.now() - timedelta(days=1),
                "choices": [
                    ("Python", 12),
                    ("JavaScript", 8),
                    ("Java", 6),
                    ("C++", 4),
                    ("Go", 2),
                ],
            },
            {
                "question_text": "What is the most useful development tool?",
                "pub_date": timezone.now() - timedelta(hours=6),
                "choices": [
                    ("Git", 15),
                    ("Docker", 10),
                    ("VS Code", 12),
                    ("Travis CI", 7),
                ],
            },
        ]

        for q_data in questions_data:
            question = Question.objects.create(
                question_text=q_data["question_text"], pub_date=q_data["pub_date"]
            )

            for choice_text, votes in q_data["choices"]:
                Choice.objects.create(
                    question=question, choice_text=choice_text, votes=votes
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Created {len(questions_data)} questions with choices!"
            )
        )
        self.stdout.write("🌐 Admin URL: /admin/")
        self.stdout.write("👤 Username: admin")
        self.stdout.write("🔑 Password: admin123")
