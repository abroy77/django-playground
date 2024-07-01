from django.test import TestCase
import datetime
from django.utils import timezone

from .models import Question
from django.urls import reverse

# Create your tests here.


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for 
        questions whose pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)

        future_question = Question(pub_date=time)
        self.assertFalse(future_question.was_published_recently())


    def test_was_published_recently_with_old_date(self):
        time = timezone.now() - timezone.timedelta(days=2)

        future_question = Question(pub_date = time)

        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_recent_date(self):
        time = timezone.now() - timezone.timedelta(hours=23, minutes=59,seconds=59)

        future_question = Question(pub_date = time)

        self.assertTrue(future_question.was_published_recently())    

def create_question(question_text: str, days: int) -> Question:
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date = time)


class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        # Arrange
        question = create_question("Past question", -30)

        # Act

        response = self.client.get(reverse("polls:index"))
        # Assert

        self.assertEqual(response.status_code,200)
        self.assertQuerySetEqual(response.context["latest_question_list"], [question]) 

    def test_future_question(self):
        # Arrange
        _ = create_question("Future question", 30)

        # Act

        response = self.client.get(reverse("polls:index"))
        # Assert

        self.assertEqual(response.status_code,200)
        self.assertQuerySetEqual(response.context["latest_question_list"], []) 


    def test_future_and_past_question(self):
        # Arrange
        past_question = create_question("Past question", -30)
        _future_question = create_question("Future question.", 30)

        # Act

        response = self.client.get(reverse("polls:index"))
        # Assert

        self.assertEqual(response.status_code,200)
        self.assertQuerySetEqual(response.context["latest_question_list"], [past_question]) 

    def test_2_past_question(self):
        # Arrange
        q1 = create_question("Past question 1", -15)
        q2 = create_question("Past question 2", -30)
 
        # Act

        response = self.client.get(reverse("polls:index"))
        # Assert

        self.assertEqual(response.status_code,200)
        self.assertQuerySetEqual(response.context["latest_question_list"], [q1,q2]) 

    
class QuestionViewTest(TestCase):
    def test_future_question(self):
        # Arrange
        future_question = create_question("Future question", 30)
        url = reverse("polls:question", args=(future_question.id,))

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        # Arrange
        past_question = create_question("Past question", -30)
        url = reverse("polls:question", args=(past_question.id,))

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text) 
