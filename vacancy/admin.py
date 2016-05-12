import locale
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from mezzanine.pages.admin import PageAdminForm
from ajax_select import make_ajax_form

from vacancy.models import (
    SalaryGrade,
    TrancheSalary,
    QualificationValue,
    Position,
    Item,
    Vacancy,
    Person,
    Registry,
    Appointment,
    SchoolYear,
)

#locale.setlocale(locale.LC_ALL, 'en_US')

class TrancheSalaryInline(admin.TabularInline):
    model = TrancheSalary
    fields = ('tranche_no', 'year', 'salary')
    extra = 4


class SalaryGradeAdmin(admin.ModelAdmin):
    model = SalaryGrade
    list_display = ('salary_grade', 'get_tranche_1', 'get_tranche_2', 'get_tranche_3', 'get_tranche_4')
    inlines = [TrancheSalaryInline,]

    def get_tranche_1(self, obj):
        return "%0.2f" % obj.tranche_salary.get(tranche_no=1).salary
    get_tranche_1.short_description = 'Tranche 1'
    get_tranche_1.admin_order_field = 'salary_grade'

    def get_tranche_2(self, obj):
        return "%0.2f" % obj.tranche_salary.get(tranche_no=2).salary
    get_tranche_2.short_description = 'Tranche 2'
    get_tranche_2.admin_order_field = 'salary_grade'

    def get_tranche_3(self, obj):
        return "%0.2f" % obj.tranche_salary.get(tranche_no=3).salary
    get_tranche_3.short_description = 'Tranche 3'
    get_tranche_3.admin_order_field = 'salary_grade'

    def get_tranche_4(self, obj):
        return "%0.2f" % obj.tranche_salary.get(tranche_no=4).salary
    get_tranche_4.short_description = 'Tranche 4'
    get_tranche_4.admin_order_field = 'salary_grade'


class QualificationValueInline(admin.TabularInline):
    model = QualificationValue
    fields = ('education','work_experience','training','eligibility','notes')
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


class VacancyAdminForm(PageAdminForm):
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), widget=FilteredSelectMultiple("Items", is_stacked=False))
    
    class Meta:
        model = Vacancy
        fields = ['items', 'publish_date', 'expiry_date', 'is_open']


class VacancyAdmin(admin.ModelAdmin):
    model = Vacancy
    list_display = ('publish_date', 'expiry_date', 'is_open')
    list_filter = ('is_open', 'publish_date', 'expiry_date')
    form = VacancyAdminForm


class PersonAdminForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['employee_id','first_name','last_name','name_ext','address','gender','marital_status','phone_number','email_address']

    def clean_email_address(self):
        return self.cleaned_data['email_address'] or None

    def clean_phone_number(self):
        return self.cleaned_data['phone_number'] or None


class PersonAdmin(admin.ModelAdmin):
    model = Person
    list_display = ('last_name', 'first_name', 'address')
    search_fields = ('last_name', 'first_name', 'address')
    form = PersonAdminForm


class RegistryAdmin(admin.ModelAdmin):
    model = Registry
    list_display = ('person', 'points', 'school', 'core_subject')
    list_filter = ('points', 'school', 'core_subject')
    search_fields = ('person__last_name', 'person__first_name')
    form = make_ajax_form(Registry, {
        'person': 'persons',
    })


class AppointmentAdmin(admin.ModelAdmin):
    model = Appointment
    list_display = ('appointee', 'item', 'get_position', 'nature', 'date_appointed', 'end_date')
    list_filter = (
        ('nature'),
        ('date_appointed'),
        ('end_date'),
    )
    search_fields = ('appointee__last_name', 'appointee__first_name', 'item__number', 'item__position__name')
    form = make_ajax_form(Appointment, {
        'appointee': 'persons',
    })

    def get_position(self, obj):
        return obj.item.position
    get_position.short_description = 'Position'
    get_position.admin_order_field = 'item__position__salary_grade'


class SchoolYearAdminForm(PageAdminForm):
    class Meta:
        model = SchoolYear
        fields = ['start_date', 'end_date']


class SchoolYearAdmin(admin.ModelAdmin):
    model = SchoolYear
    list_filter = ('start_date', 'end_date')
    form = SchoolYearAdminForm


admin.site.register(SalaryGrade, SalaryGradeAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Registry, RegistryAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(SchoolYear, SchoolYearAdmin)
