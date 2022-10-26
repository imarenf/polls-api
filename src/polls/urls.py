from django.urls import path

from polls.api import PollAPIView, PollDetailAPIView

urlpatterns = [
    path('polls/', PollAPIView.as_view()),
    path('polls/<int:pk>/', PollDetailAPIView.as_view()),
]
