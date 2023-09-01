# pylint: disable=redefined-outer-name

from http import HTTPStatus
from faker import Faker
import pytest

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from polls.models import Question

faker = Faker()


@pytest.fixture
def api_client():
    user = User.objects.create_user(
        username='testuser123', password='testpassword', is_staff=True, is_superuser=True)
    api_client = APIClient()
    # api_client.login(username='testuser', password='testpassword')
    api_client.force_authenticate(user=user)

    return api_client


@pytest.mark.django_db
class TestQuestionListAPI():

    def test_get_questions(self, api_client):
        response = api_client.get(reverse('api-question-list'))

        assert response.status_code == HTTPStatus.OK

    def test_create_question(self, api_client):
        Question.objects.all().delete()

        data = {'question_text': 'New Question', 'pub_date': '2023-08-28T12:00:00Z'}
        response = api_client.post(reverse('api-question-list'), data, format='json')

        assert response.status_code == HTTPStatus.CREATED
        assert Question.objects.count() == 1
        assert Question.objects.get().question_text == 'New Question'
        assert (
            Question.objects.get().pub_date.strftime("%Y-%m-%dT%H:%M:%SZ") == '2023-08-28T12:00:00Z'
        )


@pytest.mark.django_db
class TestQuestionDetailAPI():

    def test_get_question_detail(self, api_client):
        Question.objects.all().delete()
        question = Question.objects.create(
            question_text=faker.sentence(), pub_date='2023-08-28T12:00:00Z')

        response = api_client.get(reverse('api-question-detail', args=[question.pk]))

        assert response.status_code == HTTPStatus.OK

    def test_update_question(self, api_client):
        question = Question.objects.create(
            question_text='Question1', pub_date='2023-08-28T12:00:00Z')

        data = {'question_text': 'UpdatedText', 'pub_date': '2022-08-28T12:00:00Z'}
        response = api_client.put(
            reverse('api-question-detail', args=[question.pk]), data, format='json')

        assert response.status_code == HTTPStatus.OK
        updated_question = Question.objects.get(pk=question.pk)
        assert updated_question.question_text == 'UpdatedText'

    def test_delete_question(self, api_client):
        question = Question.objects.create(
            question_text='Question1', pub_date='2023-08-28T12:00:00Z')
        response = api_client.delete(
            reverse('api-question-detail', args=[question.pk]), format='json')

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert Question.objects.filter(pk=question.pk).exists() is False
