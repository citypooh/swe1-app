# Generated manually for sample data

from django.db import migrations
from django.utils import timezone
from datetime import timedelta


def create_sample_data(apps, schema_editor):
    """Create sample poll questions and choices."""
    Question = apps.get_model("polls", "Question")
    Choice = apps.get_model("polls", "Choice")

    # Clear existing data
    Question.objects.all().delete()

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


def reverse_sample_data(apps, schema_editor):
    """Remove sample data."""
    Question = apps.get_model("polls", "Question")
    Question.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_sample_data, reverse_sample_data),
    ]
