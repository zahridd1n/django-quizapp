from django.db import models
from django.contrib.auth.models import User
from random import sample
import string, random
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class CodeGenerate(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)

    @staticmethod
    def generate_code():
        return ''.join(sample(string.ascii_letters + string.digits, 14))

    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                code = self.generate_code()
                if not self.__class__.objects.filter(code=code).count():
                    self.code = code
                    break
        super(CodeGenerate, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Quiz(CodeGenerate):
    name = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    @property
    def questions_count(self):
        return Question.objects.filter(quiz=self).count()


class Question(CodeGenerate):
    name = RichTextUploadingField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def options(self):
        option = Option.objects.filter(question=self)
        option_list = list(option)
        random.shuffle(option_list)
        return option_list

    @property
    def correct_option(self):
        return Option.objects.get(question=self, is_correct=True)


class Option(CodeGenerate):
    name = models.CharField(max_length=155)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     options = Option.objects.filter(question=self.question).count()
    #     first = options == 0
    #     second = self.is_correct
    #
    #     if (first and second) or (not first and not second):
    #         super(Option, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Answer(CodeGenerate):
    username = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class AnswerDetail(CodeGenerate):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.ForeignKey(Option, on_delete=models.CASCADE)

    @property
    def is_correct(self):
        return self.user_answer == self.question.correct_option

    def __str__(self):
        return f"{self.answer.username} - {self.question.name} - {self.user_answer.name}"
