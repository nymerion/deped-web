import datetime
from django.http import HttpResponseRedirect
from vacancy.models import Vacancy
from django.shortcuts import render
from vacancy.utils import generate_vacancy_context
from django.utils import timezone


def listing(request, year, month, day, template):
    context = {'vacancies': []}
    #tz = timezone.get_current_timezone()
    date = datetime.datetime(int(year), int(month), int(day))
    #date_tz = tz.localize(date)
    vacancies = Vacancy.objects.filter(is_open=True, publish_date__range=(
        datetime.datetime.combine(date, datetime.time.min),
        datetime.datetime.combine(date, datetime.time.max)
        )).order_by('-publish_date')

    #raise Exception
    for vacancy in vacancies:
        generate_vacancy_context(vacancy, context)

    return render(request, template, context)


def latest(request, template):
    vacancy = Vacancy.objects.filter(is_open=True).order_by('-publish_date')[0]
    #tz = timezone.get_current_timezone()
    #date_tz = tz.localize(vacancy.publish_date)
    date = vacancy.publish_date
    url = "/vacancy/%s/" % date.strftime('%Y-%m-%d')
    return HttpResponseRedirect(url)
