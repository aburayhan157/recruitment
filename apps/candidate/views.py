import requests
import json
import uuid

from django.shortcuts import render, redirect
from .services import service
from . import forms


def login(request):
    context = {}
    if request.method == 'POST':
        user = {
            "username": request.POST['username'],
            "password": request.POST['password']
        }

        try:
            res = service.login(json.dumps(user))
            res.raise_for_status()
            data = res.json()

            # set session
            request.session['user_name'] = data['auth_info']['name']
            request.session['auth_token'] = data['token']

            return redirect('apply')

        except requests.exceptions.RequestException as err:
            context['message'] = json.loads(err.response.text)['message']
    else:
        if request.session.get('auth_token'):
            return redirect('apply')

    return render(request, 'login.html', context)


def apply(request):
    if not request.session.get('auth_token'):
        return redirect('login')

    context = {}
    if request.method == 'POST':
        form = forms.ApplicationForm(request.POST, request.FILES)
        context['form'] = form
        if form.is_valid():
            applicant_info = {
                "tsync_id": str(uuid.uuid1()),
                "name": form.cleaned_data['name'],
                "email": form.cleaned_data['email'],
                "phone": form.cleaned_data['phone'],
                "full_address": form.cleaned_data['full_address'],
                "name_of_university": form.cleaned_data['name_of_university'],
                "graduation_year": form.cleaned_data['graduation_year'],
                "cgpa": form.cleaned_data['cgpa'],
                "experience_in_months": form.cleaned_data['experience_in_months'],
                "current_work_place_name": form.cleaned_data['current_work_place_name'],
                "applying_in": form.cleaned_data['applying_in'],
                "expected_salary": form.cleaned_data['expected_salary'],
                "field_buzz_reference": form.cleaned_data['field_buzz_reference'],
                "github_project_url": form.cleaned_data['github_project_url'],
                "cv_file": {
                    "tsync_id": str(uuid.uuid1())
                }
            }

            try:
                auth_token = request.session.get('auth_token')
                res = service.apply(auth_token, json.dumps(applicant_info))
                res.raise_for_status()

                data = res.json()
                file_token_id = data['cv_file']['id']
                file = request.FILES['cv_file']
                files = {
                    'file': file.read()
                }

                res2 = service.upload(auth_token, file_token_id, files)
                res2.raise_for_status()

                data2 = res.json()
                context['form'] = forms.ApplicationForm()
                context['message'] = data2['message']

            except requests.exceptions.RequestException as err:
                # Unauthorized
                if json.loads(err.response.text)['status_code'] == 401:
                    return redirect('logout')

                context['message'] = json.loads(err.response.text)['message']

    else:
        form = forms.ApplicationForm()
        context['form'] = form

    return render(request, 'apply.html', context)


def logout(request):
    request.session.flush()
    return redirect('login')
