from django.forms import ModelForm
from .models import *
from django import forms


class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['name']


class QuestionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['quiz'].queryset = Quiz.objects.filter(author=user)

    class Meta:
        model = Question
        fields = ['quiz', 'name', 'code', ]
        exclude = ['code']
        # widgets = {
        #     'quiz': forms.Select(attrs={'class': 'form-control'}),
        # }
