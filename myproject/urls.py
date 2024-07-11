"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from myapp import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'), #done
    path('login/', views.user_login, name='login'),#done
    path('logout/', views.user_logout, name='logout'),#done
    path('users/', views.UserListView.as_view(), name='user_list'),#done
    path('users/add/', views.UserCreateView.as_view(), name='user_create'),#done
    path('users/edit/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),#done
    path('users/delete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),#done
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),#done
    path('subjects/add/', views.SubjectCreateView.as_view(), name='subject_create'),#done
    path('subjects/edit/<int:pk>/', views.SubjectUpdateView.as_view(), name='subject_update'),#done
    path('subjects/delete/<int:pk>/', views.SubjectDeleteView.as_view(), name='subject_delete'),#done
    path('tests/', views.TestListView.as_view(), name='test_list'),#done
    path('tests/add/', views.TestCreateView.as_view(), name='test_create'),#done
    path('tests/edit/<int:pk>/', views.TestUpdateView.as_view(), name='test_update'),#done
    path('tests/delete/<int:pk>/', views.TestDeleteView.as_view(), name='test_delete'),#done
    path('questions/', views.QuestionListView.as_view(), name='question_list'),
    path('questions/add/', views.QuestionCreateView.as_view(), name='question_create'),
    path('questions/edit/<int:pk>/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('questions/delete/<int:pk>/', views.QuestionDeleteView.as_view(), name='question_delete'),
    path('options/', views.OptionListView.as_view(), name='option_list'),
    path('options/add/', views.OptionCreateView.as_view(), name='option_create'),
    path('options/edit/<int:pk>/', views.OptionUpdateView.as_view(), name='option_update'),
    path('options/delete/<int:pk>/', views.OptionDeleteView.as_view(), name='option_delete'),
    path('user_answers/', views.UserAnswerListView.as_view(), name='user_answer_list'),
    path('user_answers/add/', views.UserAnswerCreateView.as_view(), name='user_answer_create'),
    path('user_answers/edit/<int:pk>/', views.UserAnswerUpdateView.as_view(), name='user_answer_update'),
    path('user_answers/delete/<int:pk>/', views.UserAnswerDeleteView.as_view(), name='user_answer_delete'),
    path('user_performances/', views.UserPerformanceListView.as_view(), name='user_performance_list'),
    path('user_performances/add/', views.UserPerformanceCreateView.as_view(), name='user_performance_create'),
    path('user_performances/edit/<int:pk>/', views.UserPerformanceUpdateView.as_view(), name='user_performance_update'),
    path('user_performances/delete/<int:pk>/', views.UserPerformanceDeleteView.as_view(), name='user_performance_delete'),
]