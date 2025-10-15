from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.core.management import call_command
from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + timezone.timedelta(days=30)
        future_question = Question(question_text="Future question", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - timezone.timedelta(days=1, seconds=1)
        old_question = Question(question_text="Old question", pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - timezone.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(question_text="Recent question", pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    def setUp(self):
        """Clear all questions before each test."""
        Question.objects.all().delete()

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = Question.objects.create(
            question_text="Past question.",
            pub_date=timezone.now() - timezone.timedelta(days=30),
        )
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        _future_question = Question.objects.create(  # noqa: F841
            question_text="Future question.",
            pub_date=timezone.now() + timezone.timedelta(days=30),
        )
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])


class ManagementCommandTests(TestCase):
    def test_create_sample_data_command(self):
        """Test the create_sample_data management command."""
        # Run the management command
        call_command("create_sample_data")

        # Check that questions were created
        self.assertEqual(Question.objects.count(), 3)

        # Check that each question has choices
        for question in Question.objects.all():
            self.assertGreater(question.choice_set.count(), 0)
