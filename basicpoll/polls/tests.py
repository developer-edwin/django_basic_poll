# Python
import datetime

# Django
from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from .models import Question

# Create your tests here.


def create_question(question_text, days):
    """
    create_question Create aquestion with the given "question_text", and published the given numbers of days offset to now
    
    * Negative number for questions published in the past
    * Positive numbers for questions that yet to be published

    Args:
        days (int): Days to offset the date.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

    # time = timezone.now() + datetime.timedelta(days=days)
    # return Question(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):

    def setUp(self):
        self.question = Question(question_text="Que lenguaje de programacion prefieres?")

    def test_was_published_recently_with_future_questions(self):
        """
        test_was_published_recently_with_future_questions This test probes the published date if was recently, with future questions
        """
        time = timezone.now() + datetime.timedelta(days=30)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_published_recently_with_present_questions(self):
        """
        test_was_published_recently_with_present_questions This test probes the published date if was recently, with question with less than 24 hours
        """
        time = timezone.now() - datetime.timedelta(hours=23)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), True)

    def test_was_published_recently_with_past_questions(self):
        """
        test_was_published_recently_with_past_questions This test probes the published date if was recently, with past questions
        """
        time = timezone.now() - datetime.timedelta(days=1, minutes=1)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        test_no_questions If no question exist, an appropiate messge is displayed
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls found.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question(self):
        """
        test_future_question Questions with a pub_date in the future are not displayed on index page.
        """
        create_question("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls found.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_questions(self):
        """
        test_past_questions Questions with a pub_date in the past are not displayed on index page.
        """
        question = create_question("Past question", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_future_question_and_past_question(self):
        """
        test_future_question_and_past_question Even if both past and questions exists, only past questions are displayed.
        """
        past_question = create_question(question_text="Past question", days=-30)
        future_question = create_question(question_text="Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )

    def test_two_past_questions(self):
        """
        test_two_past_questions The questions index page may display multiple questions.
        """
        past_question1 = create_question(question_text="Past question 1", days=-30)
        past_question2 = create_question(question_text="Past question 2", days=-40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1, past_question2]
        )

    def test_two_future_questions(self):
        """
        test_two_future_questions The questions index page may not display any future question.
        """
        create_question(question_text="Future question 1", days=30)
        create_question(question_text="Future question 2", days=40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        test_future_question The detail view of a question with a pub_date in the future returns a 404 error not found
        """
        future_question = create_question(question_text="Future question", days=30)
        url = reverse("polls:detail", args=(future_question.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        """
        test_past_question The detail view with a question with a pub_date in the past display the question's text
        """
        past_question = create_question(question_text="Past question", days=-10)
        url = reverse("polls:detail", args=(past_question.pk,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)