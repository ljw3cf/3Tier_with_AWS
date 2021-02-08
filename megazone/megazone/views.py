from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Question
from .forms import QuestionForm, AnswerForm, UserForm
from django.utils import timezone


def index(request):
    server_name = "WAS_SERVER1"
    context = {'server_name': server_name}
    return render(request, 'megazone/index.html', context)

def board(request):
    page = request.GET.get('page', '1')  # 페이지

    question_list = Question.objects.order_by('-create_date')

    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    return render(request, 'megazone/board_list.html', context)

def board_detail(request, question_id):
    question = Question.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'megazone/board_detail.html', context)

def reply_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('megazone:board_detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'megazone:question_detail.html', context)

def board_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('megazone:board')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'megazone/board_form.html', context)

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('megazone:index')
    else:
        form = UserForm()
    return render(request, 'megazone/signup.html', {'form': form})

# Create your views here.
