from django.shortcuts import render, redirect
from django.views import View
from .models import Vacancy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.http import HttpResponse
from django import forms


class CreateVacancy(forms.Form):
    description = forms.CharField(max_length=1024)


class MainPageView(View):
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class VacanciesListView(View):
    template_name = 'vacancies_list.html'

    def get(self, request, *args, **kwargs):
        vacancies = Vacancy.objects.all()
        return render(request, self.template_name, {"vacancies": vacancies})


class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'signup.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class CreateNewVacancy(View):
    template_name = 'create.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            empty_form = CreateVacancy()
            return render(request, self.template_name, {"form": empty_form})
        return HttpResponse(status=403)

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            filled_form = CreateVacancy(request.POST)
            if filled_form.is_valid():
                description = filled_form.data.get('description')
                new_vacancy = Vacancy.objects.create(
                    description = description,
                    author = request.user
                )
                new_vacancy.save()
                return redirect('/home/')
        return HttpResponse(status=403)