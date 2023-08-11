"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from polls.views import QuestionList, QuestionDetail, ChoiceList, ChoiceDetail, QuestionList2

# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'', QuestionList2)

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),

    path('api/questions/', QuestionList.as_view(), name='api-question-list'),
    path('api/questions/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),

    path('api/questions2/', QuestionList2.as_view(), name='api-question-list-2'),


    path('api/choices/', ChoiceList.as_view(), name='choice-list'),
    path('api/choices/<int:pk>/', ChoiceDetail.as_view(), name='question-detail'),
    # path('api/questions2/', include(router.urls)),


]
