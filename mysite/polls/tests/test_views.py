import pytest

from django.urls import reverse
from django.test import Client
from faker import Faker
from polls.tests.factories.question import QuestionFactory

faker = Faker()


@pytest.mark.django_db
class TestQuestionIndexView():
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = Client().get(reverse('polls:index'))

        assert response.status_code == 200
        assert "No polls are available." in response.content.decode()
        assert len(response.context['latest_question_list']) == 0

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = QuestionFactory(question_text="Past question.",
                                   days=faker.random_int(min=-1000, max=-1))

        client = Client()
        response = client.get(reverse('polls:index'))
        assert (
            question in response.context['latest_question_list']
        ), "Past question exist on the index page"

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        QuestionFactory(question_text="Future question.",
                        days=faker.random_int(min=1, max=1000))
        response = Client().get(reverse('polls:index'))
        assert "No polls are available." in response.content.decode()
        assert len(response.context['latest_question_list']) == 0

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = QuestionFactory(question_text="Past question.",
                                   days=faker.random_int(min=-1000, max=-1))
        QuestionFactory(question_text="Future question.", days=faker.random_int(min=1, max=1000))
        response = Client().get(reverse('polls:index'))
        assert question in response.context['latest_question_list']

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = QuestionFactory(question_text="Past question 1.",
                                    days=faker.random_int(min=-1000, max=-500))
        question2 = QuestionFactory(question_text="Past question 2.",
                                    days=faker.random_int(min=-499, max=-1))

        response = Client().get(reverse('polls:index'))

        assert [question2, question1] == list(response.context['latest_question_list'])

    @pytest.mark.parametrize("question_text, days, result",
                             [("Future question.", 30, False), ("Past question.", -10, True),])
    def test_question(self, question_text, days, result):
        # question = create_question(question_text=question_text, days=days)
        question = QuestionFactory(question_text=question_text, days=days)
        response = Client().get(reverse('polls:index'))
        assert (question in response.context['latest_question_list']) == result
