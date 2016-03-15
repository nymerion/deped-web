import locale
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

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

locale.setlocale(locale.LC_ALL, 'en_US')


class SalaryGradeAdmin(admin.ModelAdmin):
    model = SalaryGrade
    list_display = ('salary_grade', 'get_salary',)

    def get_salary(self, obj):
        return locale.format("%0.2f", obj.monthly_salary, grouping=True)
    get_salary.short_description = 'Monthly Salary'
    get_salary.admin_order_field = 'monthly_salary'


class QualificationValueInline(admin.TabularInline):
    model = QualificationValue
    fields = ('education','work_experience','training','eligibility')
    extra = 2


class PositionAdmin(admin.ModelAdmin):
    model = Position
    list_display = ('name', 'salary_grade',)
    inlines = [QualificationValueInline,]
    list_filter = (
        ('salary_grade', admin.RelatedOnlyFieldListFilter),
    )
    search_fields = ('name',)


class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ('number', 'position', 'station_type', 'station_name', 'filled')
    list_filter = (
        ('position', admin.RelatedOnlyFieldListFilter),
        ('station_type'),
        ('station_name'),
        ('filled'),
    )
    search_fields = ('number',)


class VacancyAdminForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), widget=FilteredSelectMultiple("Items", is_stacked=False))
    
    class Meta:
        model = Vacancy
        fields = ['items', 'pub_date', 'close_date', 'is_open']


class VacancyAdmin(admin.ModelAdmin):
    model = Vacancy
    list_display = ('pub_date', 'close_date', 'is_open')
    list_filter = ('is_open', 'pub_date', 'close_date')
    form = VacancyAdminForm


class PersonAdmin(admin.ModelAdmin):
    model = Person
    list_display = ('last_name', 'first_name', 'address')
    search_fields = ('last_name', 'first_name', 'address')


class RegistryAdmin(admin.ModelAdmin):
    model = Registry
    list_display = ('person', 'score')


admin.site.register(SalaryGrade, SalaryGradeAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Registry, RegistryAdmin)
