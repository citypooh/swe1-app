from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Question, Choice


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


class QuestionDetailViewTests(TestCase):
    def setUp(self):
        """Clear all questions before each test."""
        Question.objects.all().delete()

    def test_past_question_detail(self):
        """Past questions should be accessible."""
        question = Question.objects.create(
            question_text="Past question.",
            pub_date=timezone.now() - timezone.timedelta(days=30),
        )
        response = self.client.get(reverse("polls:detail", args=(question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)

    def test_future_question_detail(self):
        """Future questions should be accessible (Django doesn't filter by default)."""
        question = Question.objects.create(
            question_text="Future question.",
            pub_date=timezone.now() + timezone.timedelta(days=30),
        )
        response = self.client.get(reverse("polls:detail", args=(question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)


class QuestionResultsViewTests(TestCase):
    def setUp(self):
        """Clear all questions before each test."""
        Question.objects.all().delete()

    def test_past_question_results(self):
        """Past questions should show results."""
        question = Question.objects.create(
            question_text="Past question.",
            pub_date=timezone.now() - timezone.timedelta(days=30),
        )
        response = self.client.get(reverse("polls:results", args=(question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)

    def test_future_question_results(self):
        """Future questions should be accessible (Django doesn't filter by default)."""
        question = Question.objects.create(
            question_text="Future question.",
            pub_date=timezone.now() + timezone.timedelta(days=30),
        )
        response = self.client.get(reverse("polls:results", args=(question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)


class VoteViewTests(TestCase):
    def setUp(self):
        """Clear all questions before each test."""
        Question.objects.all().delete()

    def test_vote_with_valid_choice(self):
        """Voting with a valid choice should work."""
        question = Question.objects.create(
            question_text="Test question.",
            pub_date=timezone.now() - timezone.timedelta(days=1),
        )
        choice = Choice.objects.create(
            question=question,
            choice_text="Test choice",
            votes=0,
        )

        response = self.client.post(
            reverse("polls:vote", args=(question.id,)), {"choice": choice.id}
        )

        # Should redirect to results page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("polls:results", args=(question.id,)))

        # Check that vote was recorded
        choice.refresh_from_db()
        self.assertEqual(choice.votes, 1)

    def test_vote_without_choice(self):
        """Voting without selecting a choice should show error."""
        question = Question.objects.create(
            question_text="Test question.",
            pub_date=timezone.now() - timezone.timedelta(days=1),
        )

        response = self.client.post(reverse("polls:vote", args=(question.id,)))

        # Should render detail page with error message
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You didn&#x27;t select a choice.")

    def test_vote_with_invalid_choice(self):
        """Voting with invalid choice should show error."""
        question = Question.objects.create(
            question_text="Test question.",
            pub_date=timezone.now() - timezone.timedelta(days=1),
        )

        response = self.client.post(
            reverse("polls:vote", args=(question.id,)),
            {"choice": 999},  # Non-existent choice
        )

        # Should render detail page with error message
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You didn&#x27;t select a choice.")
