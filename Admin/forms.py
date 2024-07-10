# from django import forms
# from .models import Question, Quiz, AnswerOptions
# from Student.models import Student
# from django.forms import inlineformset_factory
#
#
# class QuizForm(forms.ModelForm):
#
#     assigned_to = forms.ModelMultipleChoiceField(
#         queryset=Student.objects.all(),
#         required=True,
#         widget=forms.CheckboxSelectMultiple,
#         label='Assign to Students:'
#     )
#
#     class Meta:
#         model = Quiz
#         fields = ['title', 'difficulty_level', 'assigned_to']
#         widgets = {
#             'title': forms.TextInput(
#                 attrs={
#                     'class': 'form-control',
#                     'label': "Quiz Title"
#                 }
#             )
#         }
#
#
# class OptionForm(forms.ModelForm):
#     class Meta:
#         model = AnswerOptions
#         fields = ['option_text']
#         widgets = {
#             'option_text': forms.TextInput(attrs={'class': 'form-control'}),
#         }
#
#
# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['question_statement', 'question_type', 'difficulty_level', 'correct_answer']
#         widgets = {
#             'question_statement': forms.TextInput(
#                 attrs={
#                     'class': 'form-control'
#                 }
#             ),
#             'correct_answer': forms.TextInput(
#                 attrs={
#                     'class': 'form-control'
#                 }
#             ),
#         }
#
#     OptionFormSet = inlineformset_factory(
#         Question,
#         AnswerOptions,
#         form=OptionForm,
#         extra=1,
#         can_delete=True
#     )
#
# QuestionFormSet = inlineformset_factory(
#     Quiz,
#     Question,
#     form=QuestionForm,
#     extra=1,
#     can_delete=False
# )
#
# # OptionFormSet = inlineformset_factory(
# #     Question,
# #     AnswerOptions,
# #     form=OptionForm,
# #     extra=1,
# #     can_delete=True
# # )


from django import forms
from Student.models import Student
from django.forms.models import inlineformset_factory
from .models import Quiz, Question, AnswerOptions


class QuizForm(forms.ModelForm):
    assigned_to = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple,
        label='Assign to Students:'
    )

    class Meta:
        model = Quiz
        fields = ['title', 'difficulty_level', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_statement', 'question_type', 'difficulty_level', 'correct_answer']
        widgets = {
            'question_statement': forms.TextInput(attrs={'class': 'form-control'}),
            'correct_answer': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AnswerOptionForm(forms.ModelForm):
    class Meta:
        model = AnswerOptions
        fields = ['option_text']
        widgets = {
            'option_text': forms.TextInput(attrs={'class': 'form-control'}),
        }


QuestionFormSet = inlineformset_factory(
    Quiz,
    Question,
    form=QuestionForm,
    extra=1,
    can_delete=True,
    widgets={
        'question_statement': forms.TextInput(attrs={'class': 'form-control'}),
        'question_type': forms.Select(attrs={'class': 'form-control'}),
        'difficulty_level': forms.Select(attrs={'class': 'form-control'}),
        'correct_answer': forms.TextInput(attrs={'class': 'form-control'}),
    }
)

AnswerOptionFormSet = inlineformset_factory(
    Question,
    AnswerOptions,
    form=AnswerOptionForm,
    fields=['option_text'],
    extra=1,
    can_delete=True
)

