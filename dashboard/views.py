from quiz import models
from django.shortcuts import redirect, render


def quiz_list(request):
    quizzes = models.Quiz.objects.filter(author_id=request.user.id)
    context = {
        'quizzes': quizzes
    }
    return render(request, 'quiz/quizlist.html', context)


def quiz_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        author = request.user
        quiz = models.Quiz.objects.create(
            name=name,
            author=author
        )
        return redirect('quiz_list')


def quiz_detail(request, code):  # + question list ham hisoblanadi bu funksiya
    quiz = models.Quiz.objects.get(code=code)
    questions = models.Question.objects.filter(quiz=quiz)
    context = {
        'quiz': quiz,
        'questions': questions
    }
    return render(request, 'quiz/quizdetail.html', context)


def question_create(request):
    quizzes = models.Quiz.objects.all()
    context = {
        'quizzes': quizzes,
    }
    if request.method == 'POST':
        quiz = models.Quiz.objects.get(code=request.POST.get('code'))
        question = models.Question.objects.create(
            name=request.POST['name'],
            quiz=quiz
        )
        models.Option.objects.create(
            name=request.POST.get('correct_option'),
            question=question,
            is_correct=True
        )
        for option in request.POST.getlist('options'):
            models.Option.objects.create(
                name=option,
                question=question,
                is_correct=False
            )
        return redirect('quiz_detail', quiz.code)
    return render(request, 'quiz/question_create.html', context)


def question_detail(request, code):
    question = models.Question.objects.get(code=code)
    options = models.Option.objects.filter(question=question)
    context = {
        'question': question,
        'options': options
    }
    return render(request, 'quiz/question_detail.html', context)