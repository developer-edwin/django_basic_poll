# Python
import datetime

# Django
from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from .models import Question

# Create your tests here.
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