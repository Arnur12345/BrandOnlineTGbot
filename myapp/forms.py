from django import forms
from .models import Users, Subject, Tests, Questions, Options, UserAnswer, UserPerformance

class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['telegram_name', 'created_at']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']

class TestForm(forms.ModelForm):
    class Meta:
        model = Tests
        fields = ['name', 'subject']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['test', 'question_text', 'correct_answer']

class OptionForm(forms.ModelForm):
    class Meta:
        model = Options
        fields = ['question', 'option_text']

class UserAnswerForm(forms.ModelForm):
    class Meta:
        model = UserAnswer
        fields = ['user', 'question', 'selected_option', 'is_correct', 'answered_at']

class UserPerformanceForm(forms.ModelForm):
    class Meta:
        model = UserPerformance
        fields = ['user', 'test', 'score', 'completed_at']
