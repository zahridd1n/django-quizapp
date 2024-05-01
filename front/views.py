from django.shortcuts import render, redirect
from quiz import models
import random


def index(request):
    return redirect('quiz_list')


def quiz_detail(request, code):
    quiz = models.Quiz.objects.get(code=code)
    questions = models.Question.objects.filter(quiz=quiz)

    questions_list = list(questions)
    random.shuffle(questions_list)
    context = {
        'quiz': quiz,
        'questions': questions_list,
    }
    if request.method == 'POST':
        answer = models.Answer.objects.create(
            quiz=quiz,
            username=request.POST.get('username'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
        )

        for key, value in request.POST.items():
            if key.isdigit():
                models.AnswerDetail.objects.create(
                    answer=answer,
                    question_id=int(key),
                    user_answer_id=int(value),
                )
        queryset = models.AnswerDetail.objects.filter(answer=answer)
        correct = 0
        wrong = 0
        for item in queryset:
            if item.user_answer.is_correct:
                correct += 1
            else:
                wrong += 1
        correct_percentage = int(correct * 100 / queryset.count())
        context.update({'correct_percentage': correct_percentage})
        context.update({'correct': correct})
        context.update({'wrong': wrong})
        return redirect('answer_detail', answer.code)

    return render(request, 'front/questions.html', context)
