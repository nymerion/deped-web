import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from vacancy.models import Vacancy
from vacancy.utils import generate_vacancy_context


def listing(request, year, month, day, template):
    context = {'vacancies': []}
    date = datetime.datetime(int(year), int(month), int(day))
    vacancies = Vacancy.objects.filter(is_open=True, pub_date=date).order_by('-pub_date')

    for vacancy in vacancies:
        generate_vacancy_context(vacancy, context)

    return render(request, template, context)


def latest(request, template):
    vacancy = Vacancy.objects.filter(is_open=True).order_by('-pub_date')[0]
    url = '/vacancy/%d-%.2d-%.2d/' % (vacancy.pub_date.year, vacancy.pub_date.month, vacancy.pub_date.day)
    return HttpResponseRedirect(url)
