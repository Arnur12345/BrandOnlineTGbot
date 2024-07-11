from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Users, Subject, Tests, Questions, Options, UserAnswer, UserPerformance
from .forms import UserForm, SubjectForm, TestForm, QuestionForm, OptionForm, UserAnswerForm, UserPerformanceForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

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


@login_required
@staff_member_required
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

@login_required
@staff_member_required
class UserListView(ListView):
    model = Users
    template_name = 'user_list.html'
    context_object_name = 'users'

@login_required
@staff_member_required
class UserCreateView(CreateView):
    model = Users
    form_class = UserForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('user_list')

@login_required
@staff_member_required
class UserUpdateView(UpdateView):
    model = Users
    form_class = UserForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('user_list')

@login_required
@staff_member_required
class UserDeleteView(DeleteView):
    model = Users
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

@login_required
@staff_member_required
class SubjectListView(ListView):
    model = Subject
    template_name = 'subject_list.html'
    context_object_name = 'subjects'

@login_required
@staff_member_required
class SubjectCreateView(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subject_form.html'
    success_url = reverse_lazy('subject_list')

@login_required
@staff_member_required
class SubjectUpdateView(UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subject_form.html'
    success_url = reverse_lazy('subject_list')

@login_required
@staff_member_required
class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = 'subject_confirm_delete.html'
    success_url = reverse_lazy('subject_list')

@login_required
@staff_member_required
class TestListView(ListView):
    model = Tests
    template_name = 'test_list.html'
    context_object_name = 'tests'

@login_required
@staff_member_required
class TestCreateView(CreateView):
    model = Tests
    form_class = TestForm
    template_name = 'test_form.html'
    success_url = reverse_lazy('test_list')

@login_required
@staff_member_required
class TestUpdateView(UpdateView):
    model = Tests
    form_class = TestForm
    template_name = 'test_form.html'
    success_url = reverse_lazy('test_list')

@login_required
@staff_member_required
class TestDeleteView(DeleteView):
    model = Tests
    template_name = 'test_confirm_delete.html'
    success_url = reverse_lazy('test_list')

@login_required
@staff_member_required
class QuestionListView(ListView):
    model = Questions
    template_name = 'question_list.html'
    context_object_name = 'questions'

@login_required
@staff_member_required
class QuestionCreateView(CreateView):
    model = Questions
    form_class = QuestionForm
    template_name = 'question_form.html'
    success_url = reverse_lazy('question_list')

@login_required
@staff_member_required
class QuestionUpdateView(UpdateView):
    model = Questions
    form_class = QuestionForm
    template_name = 'question_form.html'
    success_url = reverse_lazy('question_list')

@login_required
@staff_member_required
class QuestionDeleteView(DeleteView):
    model = Questions
    template_name = 'question_confirm_delete.html'
    success_url = reverse_lazy('question_list')

@login_required
@staff_member_required
class OptionListView(ListView):
    model = Options
    template_name = 'option_list.html'
    context_object_name = 'options'

@login_required
@staff_member_required
class OptionCreateView(CreateView):
    model = Options
    form_class = OptionForm
    template_name = 'option_form.html'
    success_url = reverse_lazy('option_list')

@login_required
@staff_member_required
class OptionUpdateView(UpdateView):
    model = Options
    form_class = OptionForm
    template_name = 'option_form.html'
    success_url = reverse_lazy('option_list')

@login_required
@staff_member_required
class OptionDeleteView(DeleteView):
    model = Options
    template_name = 'option_confirm_delete.html'
    success_url = reverse_lazy('option_list')

@login_required
@staff_member_required
class UserAnswerListView(ListView):
    model = UserAnswer
    template_name = 'user_answer_list.html'
    context_object_name = 'user_answers'

@login_required
@staff_member_required
class UserAnswerCreateView(CreateView):
    model = UserAnswer
    form_class = UserAnswerForm
    template_name = 'user_answer_form.html'
    success_url = reverse_lazy('user_answer_list')

@login_required
@staff_member_required
class UserAnswerUpdateView(UpdateView):
    model = UserAnswer
    form_class = UserAnswerForm
    template_name = 'user_answer_form.html'
    success_url = reverse_lazy('user_answer_list')

@login_required
@staff_member_required
class UserAnswerDeleteView(DeleteView):
    model = UserAnswer
    template_name = 'user_answer_confirm_delete.html'
    success_url = reverse_lazy('user_answer_list')

@login_required
@staff_member_required
class UserPerformanceListView(ListView):
    model = UserPerformance
    template_name = 'user_performance_list.html'
    context_object_name = 'user_performances'

@login_required
@staff_member_required
class UserPerformanceCreateView(CreateView):
    model = UserPerformance
    form_class = UserPerformanceForm
    template_name = 'user_performance_form.html'
    success_url = reverse_lazy('user_performance_list')

@login_required
@staff_member_required
class UserPerformanceUpdateView(UpdateView):
    model = UserPerformance
    form_class = UserPerformanceForm
    template_name = 'user_performance_form.html'
    success_url = reverse_lazy('user_performance_list')

@login_required
@staff_member_required
class UserPerformanceDeleteView(DeleteView):
    model = UserPerformance
    template_name = 'user_performance_confirm_delete.html'
    success_url = reverse_lazy('user_performance_list')
