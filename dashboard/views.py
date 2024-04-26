from quiz import models
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def quiz_list(request):
    quizzes = models.Quiz.objects.filter(author_id=request.user.id)
    context = {
        'quizzes': quizzes
    }
    return render(request, 'quiz/quizlist.html', context)


@login_required(login_url='sign_in')
def quiz_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        author = request.user
        quiz = models.Quiz.objects.create(
            name=name,
            author=author
        )
        return redirect('quiz_list')


@login_required(login_url='sign_in')
def quiz_edit(request, code):
    quiz = models.Quiz.objects.get(code=code)
    if request.method == 'POST':
        quiz.name = request.POST.get('name')
        quiz.save()

    return redirect('quiz_list')


@login_required(login_url='sign_in')
def quiz_delete(request, code):
    quiz = models.Quiz.objects.get(code=code).delete()
    return redirect('quiz_list')


@login_required(login_url='sign_in')
def quiz_detail(request, code):  # + question list ham hisoblanadi bu funksiya
    quiz = models.Quiz.objects.get(code=code)
    questions = models.Question.objects.filter(quiz=quiz)
    context = {
        'quiz': quiz,
        'questions': questions
    }
    return render(request, 'quiz/quizdetail.html', context)


@login_required(login_url='sign_in')
def question_create(request):
    quizzes = models.Quiz.objects.filter(author=request.user)
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


@login_required(login_url='sign_in')
def question_edit(request, code):
    quizzes = models.Quiz.objects.filter(author=request.user)
    question = models.Question.objects.get(code=code)
    quiz = models.Quiz.objects.get(name=question.quiz.name)
    options = models.Option.objects.filter(question_id=question.id)
    if request.method == 'POST':
        question.quiz.id = request.POST.get('id')
        question.name = request.POST.get('name')
        question.save()

        c_option = models.Option.objects.get(question_id=question.id, is_correct=True)
        c_option.name = request.POST.get('correct_option')
        c_option.save()

        if request.POST.getlist('new_options'):
            for option in request.POST.getlist('new_options'):
                models.Option.objects.create(
                    name=option,
                    question=question,
                    is_correct=False
                )
        return redirect('quiz_detail', quiz.code)

    context = {
        "quizzes": quizzes,
        'question': question,
        'options': options,
    }

    return render(request, 'quiz/question_edit.html', context)


@login_required(login_url='sign_in')
def question_delete(request, code):
    question = models.Question.objects.get(code=code).delete()
    return redirect(request.META.get('HTTP_REFERER', 'quiz_list'))


@login_required(login_url='sign_in')
def question_detail(request, code):
    question = models.Question.objects.get(code=code)
    options = models.Option.objects.filter(question=question)
    context = {
        'question': question,
        'options': options
    }
    return render(request, 'quiz/question_detail.html', context)


# -------------Answer---------------------
@login_required(login_url='sign_in')
def answer_list(request, code):
    answers = models.Answer.objects.filter(quiz__code=code)
    context = {
        'answers': answers
    }
    return render(request, 'answer/list.html', context)


def answer_detail(request, code):
    answer = models.Answer.objects.get(code=code)
    queryset = models.AnswerDetail.objects.filter(answer=answer)
    correct = 0
    wrong = 0
    for item in queryset:
        if item.user_answer.is_correct:
            correct += 1
        else:
            wrong += 1
    correct_percentage = int(correct * 100 / queryset.count())
    wrong_percentage = 100 - correct_percentage
    context = {
        'answer': answer,
        'queryset': queryset,
        'correct': correct,
        'wrong': wrong,
        'correct_percentage': correct_percentage,
        'wrong_percentage': wrong_percentage,
        'total': queryset.count(),
    }

    return render(request, 'answer/detail.html', context)


# ------------AUTH------------------------
def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if password == password_confirm:
            user = User.objects.create_user(
                username=username,
                password=password, )
            login(request, user)
            return redirect('quiz_list')
        else:
            return redirect('sig_up')

    return render(request, 'auth/signup.html')


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('quiz_list')
        else:
            return redirect('sign_in')

    return render(request, 'auth/signin.html')


@login_required(login_url='sign_in')
def log_out(request):
    logout(request)
    return redirect('quiz_list')
