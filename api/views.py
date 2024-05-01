from . import serializers
from quiz import models
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import *
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import generics


class QuizCreate(generics.CreateAPIView):
    serializer_class = serializers.QuizSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class QuizList(generics.ListAPIView):
    serializer_class = serializers.QuizSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]

    def get_queryset(self):
        a = models.Quiz.objects.filter(author_id=self.request.user.id)
        return a


@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def quiz_detail(request, code):
    quiz = models.Quiz.objects.get(code=code)
    quiz_serializer = serializers.QuizSerializer(quiz)
    questions = models.Question.objects.filter(quiz=quiz)
    question_serializers = serializers.QuestionSerializer(questions, many=True)
    return Response({
        'quiz': quiz_serializer.data,
        'questions': question_serializers.data
    })


@api_view(['POST'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def answer_create(request, code):
    quiz = models.Quiz.objects.get(code=code)
    user_name = request.data.get('user_name')
    email = request.data.get('email')
    phone = request.data.get('phone')
    answer = models.Answer.objects.create(
        quiz=quiz,
        username=user_name,
        email=email,
        phone=phone
    )
    answers = request.data.get('answers')
    correct = 0
    wrong = 0
    for key, value in answers.items():
        question = models.Question.objects.get(code=key)
        option = models.Option.objects.get(code=value)
        answer_detail = models.AnswerDetail.objects.create(
            answer=answer,
            question=question,
            user_answer=option,
        )

        if answer_detail.is_correct:
            correct += 1

    total = models.Question.objects.filter(quiz=quiz).count()
    ishlanganlar = len(answers)
    wrong = total - correct
    correct_percentage = int(correct * 100 / total)
    wrong_percentage = 100 - correct_percentage

    return Response({
        'status': True,
        'total': total,
        'correct': correct,
        "wrong": wrong,
        'correct_percentage': correct_percentage,
        'wrong_percentage': wrong_percentage,
        'ishlanganlar': ishlanganlar

    })


@api_view(["POST"])
def log_in(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response


@api_view(["POST"])
def log_out(request):
    token = Token.objects.get(user=request.user).delete()
    return Response
