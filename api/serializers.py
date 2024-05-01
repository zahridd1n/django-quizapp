from quiz import models
from rest_framework import serializers


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quiz
        fields = ['name', 'code']


class OptionSerailzier(serializers.ModelSerializer):
    class Meta:
        model = models.Option
        fields = ['code', 'name']


# class AnswerSerialzier(serializers.ModelSerializer):
#     class Meta:
#         model = models.Answer
#         fields =


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerailzier(read_only=True, many=True)

    class Meta:
        model = models.Question
        fields = ['code', 'name', 'options']
