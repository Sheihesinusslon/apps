from django.shortcuts import render, redirect
from django.views import View
from .models import Resume
from django.http import HttpResponse
from django import forms


class CreateResume(forms.Form):
    description = forms.CharField(max_length=1024)


class ResumeListView(View):
    template_name = 'resume_list.html'

    def get(self, request, *args, **kwargs):
        resumes = Resume.objects.all()
        return render(request, self.template_name, {"resumes": resumes})


class CreateNewResume(View):
    template_name = 'create.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            empty_form = CreateResume()
            return render(request, self.template_name, {"form": empty_form})
        return HttpResponse(status=403)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            filled_form = CreateResume(request.POST)
            if filled_form.is_valid():
                description = filled_form.data.get('description')
                new_resume = Resume.objects.create(
                    description = description,
                    author = request.user
                )
                new_resume.save()
                return redirect('/home/')

        return HttpResponse(status=403)