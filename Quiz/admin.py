from django.contrib import admin
from .models import *


class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to_list', 'Total_score', 'difficulty_level', 'Time_allowed')
    list_filter = ['difficulty_level']

    def assigned_to_list(self, obj):
        students = Student.objects.filter(quiz=obj)
        std_names = []
        for std in students:
            std_names.append(std.username)
        return ", ".join(std_names)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_statement', 'question_type', 'difficulty_level', 'correct_answer', 'answeroption')
    list_filter = ('question_type', 'difficulty_level')

    def answeroption(self, obj):
        answwer_options = AnswerOptions.objects.filter(question=obj)
        option_texts = []
        for option in answwer_options:
            option_texts.append(option.option_text)
        return ", ".join(option_texts)


class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'option_text')


class StudentAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'attempt_date', 'attempt_score')


class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'answer', 'score')


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(AnswerOptions, AnswerOptionAdmin)
admin.site.register(StudentQuizAttempt, StudentAttemptAdmin)
admin.site.register(StudentAnswer, StudentAnswerAdmin)



