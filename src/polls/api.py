from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from .models import Poll, Question, get_anonymous_user
from .serializers import PollSerializer, QuestionSerializer, AnswerSerializer
from .permissions import IsOwnerOrReadOnly
from core.funcs import get_poll_data, get_questions_data, get_answers_data

# curl query example
# curl -d "question=1&answer_text=test_answer_text_3" -X POST http://localhost:8000/api/v1/polls/1


class PollAPIView(APIView):

    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get(self, request):
        serialized_polls_data = PollSerializer(Poll.objects.all(), many=True)
        return Response({'polls': serialized_polls_data.data},
                        status=status.HTTP_200_OK)

    def post(self, request):
        poll_data = get_poll_data(request)
        poll_data.update({'author': request.user})
        serialized_poll_data = PollSerializer(data=poll_data)
        serialized_poll_data.is_valid(raise_exception=True)
        new_poll = serialized_poll_data.save()

        serialized_questions_data = QuestionSerializer(data=get_questions_data(request.data, new_poll), many=True)
        serialized_questions_data.is_valid(raise_exception=True)
        serialized_questions_data.save()

        return Response({'poll': serialized_poll_data.data,
                         'questions': serialized_questions_data.data},
                        status=status.HTTP_201_CREATED)


class PollDetailAPIView(APIView):

    permission_classes = [
        IsOwnerOrReadOnly,
        IsAdminUser,
    ]

    def _get_poll_by_pk(self, pk):
        if not pk:
            return Response({'error': 'Method PUT requires "pk" argument'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            poll = Poll.objects.get(pk=pk)
        except ...:
            return Response({'error': 'The poll with given "pk" argument does not exist'},
                            status=status.HTTP_404_NOT_FOUND)
        return poll

    def get_question_by_pk(self, pk):
        try:
            question = Question.objects.get(pk=pk)
        except ...:
            question = None
        return question

    def get(self, request, pk):
        poll = self._get_poll_by_pk(pk)
        serialized_poll_data = PollSerializer(poll)
        serialized_questions_data = QuestionSerializer(Question.objects.filter(poll=poll), many=True)
        return Response({'polls': serialized_poll_data.data,
                         'questions': serialized_questions_data.data},
                        status=status.HTTP_200_OK)

    def put(self, request, pk):
        poll = self._get_poll_by_pk(pk)
        questions = Question.objects.filter(poll=poll)

        serialized_poll_data = PollSerializer(data=get_poll_data(request), instance=poll)
        serialized_poll_data.is_valid(raise_exception=True)
        serialized_questions_data = QuestionSerializer(data=get_questions_data(request.data, poll),
                                                       instance=questions, many=True)
        serialized_questions_data.is_valid(raise_exception=True)
        serialized_poll_data.save()
        serialized_questions_data.save()

        return Response({'poll': serialized_poll_data.data,
                         'questions': serialized_questions_data.data},
                        status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        poll = self._get_poll_by_pk(pk)
        poll.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, poll_pk):
        current_user = request.user if request.user else get_anonymous_user()
        answer_data = get_answers_data(self, request.data, current_user)

        answers = AnswerSerializer(data=answer_data, many=True)
        answers.is_valid(raise_exception=True)
        answers.save()
        return Response(answers.data, status=status.HTTP_202_ACCEPTED)
