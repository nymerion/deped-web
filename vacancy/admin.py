from django.contrib import admin
from vacancy.models import (
    SalaryGrade,
    Position,
    Station,
    Vacancy
)

admin.site.register(SalaryGrade)
admin.site.register(Position)
admin.site.register(Station)
admin.site.register(Vacancy)
