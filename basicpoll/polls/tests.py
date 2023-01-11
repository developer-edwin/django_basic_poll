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

    # def test_no_future_question_are_displayed(self):
    #     """
    #     test_no_future_question_are_displayed This test create a question with the date 30 days in the future and should be not displayed
    #     """
    #     # response = self.client.get(reverse("polls:index"))
    #     time = timezone.now() + datetime.timedelta(days=30)
    #     future_question = Question.objects.create(question_text="Cual es el lenguaje mas usado?", pub_date=time)
    #     response = self.client.get(reverse("polls:index"))
    #     self.assertNotIn(future_question,response.context["latest_question_list"])

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
