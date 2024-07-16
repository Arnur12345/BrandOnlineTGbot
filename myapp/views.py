from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Users, Subject, Tests, Questions, Options, UserAnswer, UserPerformance
from .forms import UserForm, SubjectForm, TestForm, QuestionForm, OptionForm, UserAnswerForm, UserPerformanceForm, GoogleFormLinkForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
import requests
from bs4 import BeautifulSoup
import re


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


def dashboard(request):
    user_count = Users.objects.count()
    test_count = Tests.objects.count()
    subject_count = Subject.objects.count()
    users = Users.objects.all()
    context = {
        'user_count': user_count,
        'test_count': test_count,
        'subject_count': subject_count,
        'users': users,
    }
    return render(request, 'dashboard.html', context)


class UserListView(ListView):
    model = Users
    template_name = 'user_list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = Users
    form_class = UserForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('user_list')


class UserUpdateView(UpdateView):
    model = Users
    form_class = UserForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('user_list')


class UserDeleteView(DeleteView):
    model = Users
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('user_list')


class SubjectListView(ListView):
    model = Subject
    template_name = 'subject_list.html'
    context_object_name = 'subjects'


class SubjectCreateView(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subject_form.html'
    success_url = reverse_lazy('subject_list')


class SubjectUpdateView(UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subject_form.html'
    success_url = reverse_lazy('subject_list')


class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = 'subject_confirm_delete.html'
    success_url = reverse_lazy('subject_list')

class TestListView(ListView):
    model = Tests
    template_name = 'test_list.html'
    context_object_name = 'tests'

class TestCreateView(CreateView):
    model = Tests
    form_class = TestForm
    template_name = 'test_form.html'
    success_url = reverse_lazy('test_list')

class TestUpdateView(UpdateView):
    model = Tests
    form_class = TestForm
    template_name = 'test_form.html'
    success_url = reverse_lazy('test_list')

class TestDeleteView(DeleteView):
    model = Tests
    template_name = 'test_confirm_delete.html'
    success_url = reverse_lazy('test_list')

class TestDetailView(DetailView):
    model = Tests
    template_name = 'test_detail.html'
    context_object_name = 'test'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Questions.objects.filter(test=self.object)
        return context


class QuestionListView(ListView):
    model = Questions
    template_name = 'question_list.html'
    context_object_name = 'questions'

class QuestionCreateView(CreateView):
    model = Questions
    form_class = QuestionForm
    template_name = 'question_form.html'
    success_url = reverse_lazy('question_list')

class QuestionUpdateView(UpdateView):
    model = Questions
    form_class = QuestionForm
    template_name = 'question_form.html'
    success_url = reverse_lazy('question_list')

class QuestionDeleteView(DeleteView):
    model = Questions
    template_name = 'question_confirm_delete.html'
    success_url = reverse_lazy('question_list')

class OptionListView(ListView):
    model = Options
    template_name = 'option_list.html'
    context_object_name = 'options'

class OptionCreateView(CreateView):
    model = Options
    form_class = OptionForm
    template_name = 'option_form.html'
    success_url = reverse_lazy('option_list')

class OptionUpdateView(UpdateView):
    model = Options
    form_class = OptionForm
    template_name = 'option_form.html'
    success_url = reverse_lazy('option_list')

class OptionDeleteView(DeleteView):
    model = Options
    template_name = 'option_confirm_delete.html'
    success_url = reverse_lazy('option_list')

class UserAnswerListView(ListView):
    model = UserAnswer
    template_name = 'user_answer_list.html'
    context_object_name = 'user_answers'

class UserAnswerCreateView(CreateView):
    model = UserAnswer
    form_class = UserAnswerForm
    template_name = 'user_answer_form.html'
    success_url = reverse_lazy('user_answer_list')
class UserAnswerUpdateView(UpdateView):
    model = UserAnswer
    form_class = UserAnswerForm
    template_name = 'user_answer_form.html'
    success_url = reverse_lazy('user_answer_list')

class UserAnswerDeleteView(DeleteView):
    model = UserAnswer
    template_name = 'user_answer_confirm_delete.html'
    success_url = reverse_lazy('user_answer_list')

class UserPerformanceListView(ListView):
    model = UserPerformance
    template_name = 'user_performance_list.html'
    context_object_name = 'user_performances'

class UserPerformanceCreateView(CreateView):
    model = UserPerformance
    form_class = UserPerformanceForm
    template_name = 'user_performance_form.html'
    success_url = reverse_lazy('user_performance_list')

class UserPerformanceUpdateView(UpdateView):
    model = UserPerformance
    form_class = UserPerformanceForm
    template_name = 'user_performance_form.html'
    success_url = reverse_lazy('user_performance_list')

class UserPerformanceDeleteView(DeleteView):
    model = UserPerformance
    template_name = 'user_performance_confirm_delete.html'
    success_url = reverse_lazy('user_performance_list')

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import GoogleFormLinkForm
from .models import Questions, Options
import re

def import_google_form(request):
    if request.method == 'POST':
        form = GoogleFormLinkForm(request.POST)
        if form.is_valid():
            google_form_link = form.cleaned_data['google_form_link']
            selected_test = form.cleaned_data['test']
            
            # Fetch Google Form data
            response = requests.get(google_form_link)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract questions and options
            form_fields = soup.find_all('div', {'role': 'listitem'})

            for field in form_fields:
                # Extract question text
                question_title = field.find('div', {'role': 'heading'})
                if question_title:
                    question_text = question_title.text.strip()

                    # Extract the complete text including options
                    complete_text = field.get_text(separator="\n").strip()
                    
                    # Clean the complete text by removing question numbers and extra spaces
                    cleaned_text = re.sub(r'^\d+\.\s*', '', complete_text).strip()
                    
                    # Split the cleaned text into question and options
                    options = re.split(r'\s*[A-Я]\)\s*' or r'\s*[A-Я]\.\s*' or r'\s*[A-Z]\.\s*' or r'\s*[A-Z]\)s*',cleaned_text) #\s*[A-Я]\.\s* | \s*\d+\.\s*'
                    options = [opt.strip() for opt in options if opt.strip()]

                    
                    # Assume the first part is the question and the rest are options
                    question_text = options.pop(0)

                    # Ensure question text is cleaned properly
                    question_text = re.sub(r'^\d+\.\s*', '', question_text).strip()
                    
                    # Assuming there is no direct way to find correct answers, set a placeholder
                    correct_answer = "Not Available"
                    
                    # Create the Question and Options in the database
                    question = Questions.objects.create(test=selected_test, question_text=question_text, correct_answer=correct_answer)
                    
                    for option_text in options:
                        # Clean options: remove any lingering prefixes like A), B), etc.
                        cleaned_option = re.sub(r'^[A-Я]\)\s*', '', option_text).strip()
                        Options.objects.create(question=question, option_text=cleaned_option)
            
            return redirect(reverse_lazy('question_list'))
    else:
        form = GoogleFormLinkForm()

    return render(request, 'import_google_form.html', {'form': form})
