import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from vacancy.models import Vacancy
from vacancy.utils import generate_vacancy_context


def listing(request, year, month, day, template):
    context = {'vacancies': []}
    date = datetime.datetime(int(year), int(month), int(day))
    vacancies = Vacancy.objects.filter(is_open=True, publish_date__range=(
        datetime.datetime.combine(date, datetime.time.min),
        datetime.datetime.combine(date, datetime.time.max)
        )).order_by('-publish_date')

    for vacancy in vacancies:
        generate_vacancy_context(vacancy, context)

    return render(request, template, context)


def latest(request, template):
    vacancy = Vacancy.objects.filter(is_open=True).order_by('-publish_date')[0]
    url = '/vacancy/%d-%.2d-%.2d/' % (vacancy.publish_date.year, vacancy.publish_date.month, vacancy.publish_date.day)
    return HttpResponseRedirect(url)
