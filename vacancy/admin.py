from django.contrib import admin
from django import forms
from django.forms import inlineformset_factory

from vacancy.models import (
    SalaryGrade,
    Qualification,
    QualificationValue,
    Position,
    Item,
    Vacancy,
    Person,
    Registry,
)

class SalaryGradeAdmin(admin.ModelAdmin):
    model = SalaryGrade
    list_display = ('salary_grade', 'monthly_salary',)


class QualificationValueInline(admin.TabularInline):
    model = QualificationValue
    fields = ('education','work_experience','training','eligibility')
    extra = 2


class PositionAdmin(admin.ModelAdmin):
    model = Position
    list_display = ('name', 'salary_grade',)
    inlines = [QualificationValueInline,]


class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ('number', 'position', 'station_type', 'filled')


class VacancyAdmin(admin.ModelAdmin):
    model = Vacancy
    list_display = ('pub_date', 'close_date', 'is_open')


class PersonAdmin(admin.ModelAdmin):
    model = Person
    list_display = ('last_name', 'first_name', 'address')


class RegistryAdmin(admin.ModelAdmin):
    model = Registry
    list_display = ('person', 'score')


admin.site.register(SalaryGrade, SalaryGradeAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Registry, RegistryAdmin)
