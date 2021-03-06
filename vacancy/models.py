from __future__ import unicode_literals
from datetime import datetime

from django.core.validators import RegexValidator
from django.db import models

from mezzanine.core.fields import RichTextField
from mezzanine.pages.models import Page

optional = {'blank':True, 'null':True}


class SalaryGrade(models.Model):
    salary_grade = models.IntegerField(unique=True)

    def __unicode__(self):
        return "SG %d" % self.salary_grade

    def get_default_salary(self):
        now = datetime.now()
        return self.tranche_salary.get(year=now.year).salary

    def get_salary_for_year(self, year):
        return self.tranche_salary.get(year=year).salary


class Tranche(models.Model):
    name = models.IntegerField()


class TrancheSalary(models.Model):
    salary_grade = models.ForeignKey(SalaryGrade, related_name='tranche_salary')
    tranche = models.ForeignKey(Tranche, **optional)
    tranche_no = models.IntegerField()
    year = models.IntegerField()
    salary = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        unique_together = ('salary_grade', 'year',)

    def __unicode__(self):
        return "SG %d Tranche %d" % (self.salary_grade.salary_grade, self.tranche_no)


class Qualification(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return "%s" % self.name


class Position(models.Model):
    TS = 'TS'
    NTS = 'NTS'
    TR = 'TR'

    CATEGORY_CHOICES = (
        (TS, 'Teaching Staff'),
        (NTS, 'Non-Teaching Staff'),
        (TR, 'Teaching-Related'),
    )

    name = models.CharField(max_length=32, unique=True)
    salary_grade = models.ForeignKey(SalaryGrade)
    qualification = models.ManyToManyField(Qualification, through='QualificationValue')
    category = models.CharField(max_length=8,
                                choices=CATEGORY_CHOICES,
                                default=TS)

    def __unicode__(self):
        return "%s" % self.name

    def get_default_salary(self):
        return self.salary_grade.get_default_salary();

    def get_salary_for_year(self, year):
        return self.salary_grade.get_salary_for_year(year);


class QualificationValue(models.Model):
    LET = 'LET/PBET'
    RA1080 = 'RA1080'
    PD = 'PD907'
    CSC1 = 'CSC1'
    CSC2 = 'CSC2'
    CESO = 'CESO'

    ELIGIBILITY_CHOICES = (
        (LET, 'LET/PBET'),
        (RA1080, 'RA 1080'),
        (PD, 'PD 907'),
        (CSC1, 'CSC LVL 1'),
        (CSC2, 'CSC LVL 2'),
        (CESO, 'CESO'),
    )
    position = models.ForeignKey(Position, default=0, related_name='qualification_standards')
    qualification = models.ForeignKey(Qualification, **optional)
    education = RichTextField(max_length=512)
    work_experience = RichTextField(max_length=512)
    training = RichTextField(max_length=512, help_text="Relevant training")
    eligibility = models.CharField(max_length=8,
                                   choices=ELIGIBILITY_CHOICES,
                                   default=LET, **optional)
    notes = RichTextField(max_length=256, **optional)


class Item(models.Model):
    ES = 'ES'
    HS = 'HS'
    SDS = 'SDS'
    CID = 'CID'
    SGOD = 'SGOD'

    STATION_CHOICES = (
        (ES, 'Elementary'),
        (HS, 'High School'),
        (SDS, 'Office of the Schools Division Superintendent'),
        (CID, 'Curriculum Implementation Division'),
        (SGOD, 'School Governance and Operations Division'),
    )

    number = models.CharField(max_length=32, unique=True)
    position = models.ForeignKey(Position)
    station_name = models.CharField(max_length=64, **optional)
    station_type = models.CharField(max_length=2,
                                    choices=STATION_CHOICES,
                                    default=ES)
    filled = models.BooleanField(default=False)
    is_new = models.BooleanField("Newly created item", default=True)

    def __unicode__(self):
        return "%s" % self.number


class Vacancy(Page):
    items = models.ManyToManyField(Item)
    is_open = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"

    def __unicode__(self):
        return "%s - %s" % (self.publish_date, self.expiry_date)

    def save(self, *args, **kwargs):
        """
        Add title, slug and ordering to the Page object
        """
        self.title = self.publish_date.strftime("%B %d, %Y")
        self.slug = ''
        if self.id is None:
            try:
                page = Page.objects.get(slug='vacancy')
                self.parent = page

                idx = 0
                done = False
                for vacancy in Vacancy.objects.filter(parent=page).order_by('-publish_date'):
                    if self.publish_date > vacancy.publish_date and not done:
                        self._order = idx
                        done = True
                        idx += 1
                    if idx != vacancy._order:
                        vacancy._order = idx
                        vacancy.save()
                    idx += 1
            except:
                pass
        parent = self.parent
        while parent:
            self.slug += parent.slug
            if parent.slug[-1] != '/':
                self.slug += '/'
            parent = parent.parent
        self.slug += "%s" % self.publish_date.strftime('%Y-%m-%d')
        super(Vacancy, self).save(*args, **kwargs)


class Person(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    MARRIED = 'M'
    SINGLE = 'S'

    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    MARITAL_CHOICES = (
        (SINGLE, 'Single'),
        (MARRIED, 'Married'),
    )

    phone_regex = RegexValidator(regex=r'^\+?1?\d{11,12}$', message="Phone number must be entered in the format: '+639191234567'. Up to 12 digits allowed.")

    employee_id = models.CharField(max_length=64, **optional)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    name_ext = models.CharField(max_length=32, **optional)
    address = models.CharField(max_length=256, **optional)
    gender = models.CharField(max_length=1,
                              choices=GENDER_CHOICES,
                              default=MALE)
    marital_status = models.CharField(max_length=1,
                              choices=MARITAL_CHOICES,
                              default=SINGLE)
    phone_number = models.CharField(max_length=16, unique=True, validators=[phone_regex], **optional)
    email_address = models.EmailField(unique=True, **optional)

    def fullname(self):
        if (self.name_ext):
            return "%s %s, %s" % (self.first_name, self.last_name, self.name_ext)
        return "%s %s" % (self.first_name, self.last_name)

    def __unicode__(self):
        return self.fullname()

    class Meta:
        unique_together = ('first_name', 'last_name', 'name_ext')


class Registry(models.Model):
    ES = 'ES'
    HS = 'HS'

    SCHOOL_CHOICES = (
        (ES, 'Elementary'),
        (HS, 'High School'),
    )

    ENG = 'ENG'
    MTH = 'MTH'
    SCI = 'SCI'
    FIL = 'FIL'

    SUBJECTS = (
        (ENG, 'English'),
        (SCI, 'Science'),
        (MTH, 'Mathematics'),
        (FIL, 'Filipino'),
    )
    
    person = models.ForeignKey(Person, related_name='+')
    points = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    school_year = models.ForeignKey('SchoolYear')
    school = models.CharField(max_length=2,
                              choices=SCHOOL_CHOICES,
                              default=ES)
    core_subject = models.CharField(max_length=3,
                                    choices=SUBJECTS,
                                    default=ENG)

    class Meta:
        verbose_name = "RQA Entry"
        verbose_name_plural = "RQA Entries"
        unique_together = ('person', 'school_year')

    def __unicode__(self):
        return "%s" % self.person


class Appointment(models.Model):
    ORG = 'ORG'
    PRM = 'PRM'
    TRN = 'TRN'
    REM = 'REM'
    REA = 'REA'
    REC = 'REC'
    DEM = 'DEM'
    NATURE_CHOICES = (
        (ORG, 'Original'),
        (PRM, 'Promotion'),
        (TRN, 'Transfer'),
        (REM, 'Re-employment'),
        (REA, 'Reappointment'),
        (REC, 'Reclassification'),
        (DEM, 'Demotion'),
    )

    PMT = 'PMT'
    SUB = 'SUB'
    STATUS_CHOICES = (
        (PMT, 'Permanent'),
        (SUB, 'Substitute'),
    )

    item = models.ForeignKey(Item)
    appointee = models.ForeignKey(Person, related_name='+')
    date_appointed = models.DateField()
    nature = models.CharField(max_length=3,
                              choices=NATURE_CHOICES,
                              default=ORG)
    status = models.CharField(max_length=3,
                              choices=STATUS_CHOICES,
                              default=PMT)
    end_date = models.DateField(**optional)

    def __unicode__(self):
        return "%s - %s" % (self.appointee, self.item.position)


class SchoolYear(Page):
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return "%s - %s" % (self.start_date.year, self.end_date.year)

    def save(self, *args, **kwargs):
        """
        Add title, slug and ordering to the Page object
        """
        self.title = "%d-%d" % (self.start_date.year, self.end_date.year)
        self.slug = ''
        self.publish_date = self.start_date
        if self.id is None:
            try:
                page = Page.objects.get(slug='noa')
                self.parent = page

                idx = 0
                done = False
                for school_year in SchoolYear.objects.filter(parent=page).order_by('-start_date'):
                    if self.publish_date > school_year.start_date and not done:
                        self._order = idx
                        done = True
                        idx += 1
                    if idx != school_year._order:
                        school_year._order = idx
                        school_year.save()
                    idx += 1
            except:
                pass
        parent = self.parent
        while parent:
            self.slug += parent.slug
            if parent.slug[-1] != '/':
                self.slug += '/'
            parent = parent.parent
        self.slug += "%s" % self.title
        super(SchoolYear, self).save(*args, **kwargs)
