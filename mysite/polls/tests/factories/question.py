import factory
import datetime
from django.utils import timezone
from polls.models import Question


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question
        exclude = ('days')

    question_text = 'question_text'
    pub_date = factory.LazyAttribute(lambda o: timezone.now() + datetime.timedelta(days=o.days))
