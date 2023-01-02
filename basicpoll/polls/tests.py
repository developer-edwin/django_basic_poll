# Python
import datetime

# Django
from django.test import TestCase
from django.utils import timezone

from .models import Question

# Create your tests here.
class QuestionModelTests(TestCase):
    
    def test_was_published_recently(self):
        """
        test_was_published_recently This test probe the published date if was recently, including future dates that should be False
        """
        time = timezone.now() + datetime.timedelta(days=30)
        the_question_test = Question(question_text="Que lenguaje de programacion prefires?", pub_date=time)
        self.assertIs(the_question_test.was_published_recently(), False)