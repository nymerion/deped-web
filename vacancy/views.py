from django.shortcuts import render
from vacancy.models import Vacancy


def listing(request):
    vacancies = Vacancy.objects.filter(is_open=True)

    return render(request, 'listing.html', {'vacancies':vacancies})
