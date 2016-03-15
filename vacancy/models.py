from __future__ import unicode_literals

from django.db import models

optional = {'blank':True, 'null':True}

class SalaryGrade(models.Model):
    salary_grade = models.IntegerField(unique=True)
    monthly_salary = models.DecimalField(max_digits=8, decimal_places=2)

    def __unicode__(self):
        return "SG %d" % self.salary_grade


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


class QualificationValue(models.Model):
    LET = 'LET/PBET'
    PD = 'PD907'
    CSC1 = 'CSC1'
    CSC2 = 'CSC2'

    ELIGIBILITY_CHOICES = (
        (LET, 'LET/PBET'),
        (PD, 'PD 907'),
        (CSC1, 'CSC LVL 1'),
        (CSC2, 'CSC LVL 2'),
    )
    position = models.ForeignKey(Position, default=0, related_name='qualification_standards')
    qualification = models.ForeignKey(Qualification, default=0)
    education = models.CharField(max_length=256)
    work_experience = models.CharField(max_length=256)
    training = models.IntegerField(help_text="Hours of relevant training")
    eligibility = models.CharField(max_length=8,
                                   choices=ELIGIBILITY_CHOICES,
                                   default=LET)


class Item(models.Model):
    ES = 'ES'
    HS = 'HS'
    DO = 'DO'
    STATION_CHOICES = (
        (ES, 'Elementary'),
        (HS, 'High School'),
        (DO, 'Division Office')
    )

    number = models.CharField(max_length=32, unique=True)
    position = models.ForeignKey(Position)
    station_name = models.CharField(max_length=64, **optional)
    station_type = models.CharField(max_length=2,
                                    choices=STATION_CHOICES,
                                    default=ES)
    filled = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" % self.number


class Vacancy(models.Model):
    items = models.ManyToManyField(Item)
    pub_date = models.DateField(**optional)
    close_date = models.DateField(**optional)
    is_open = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"

    def __unicode__(self):
        return "%s - %s" % (self.pub_date, self.close_date)


class Person(models.Model):
    employee_id = models.CharField(max_length=64, **optional)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    address = models.CharField(max_length=256)

    def __unicode__(self):
        return "%s, %s" % (self.last_name, self.first_name)


class Registry(models.Model):
    person = models.OneToOneField(Person)
    score = models.IntegerField(default=0)

    class Meta:
        verbose_name = "RQA Entry"
        verbose_name_plural = "RQA Entries"

    def __unicode__(self):
        return "%s" % self.person


class ItemHistory(models.Model):
    item = models.ForeignKey(Item)
    appointee = models.ForeignKey(Person, related_name='+')
    incumbent = models.ForeignKey(Person, related_name='+')
    start_date = models.DateField(**optional)
    end_date = models.DateField(**optional)
