from __future__ import unicode_literals

from django.db import models


class SalaryGrade(models.Model):
    salary_grade = models.IntegerField(unique=True)
    monthly_salary = models.DecimalField(max_digits=7, decimal_places=2)

    def __unicode__(self):
        return "SG %d" % self.salary_grade


class Position(models.Model):
    name = models.CharField(max_length=32, unique=True)
    salary_grade = models.ForeignKey(SalaryGrade)

    class Meta:
        unique_together = ('name', 'salary_grade')

    def __unicode__(self):
        return "%s" % self.name


class Station(models.Model):
    ES = 'ES'
    HS = 'HS'
    DO = 'DO'
    STATION_CHOICES = (
        (ES, 'Elementary School'),
        (HS, 'High School'),
        (DO, 'Division Office')
    )
    name = models.CharField(max_length=64, unique=True)
    station_type = models.CharField(max_length=2,
                                    choices=STATION_CHOICES,
                                    default=DO)

    def __unicode__(self):
        return "%s" % self.name


class Vacancy(models.Model):
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
    item_number = models.CharField(max_length=32, unique=True)
    position = models.ForeignKey(Position)
    station = models.ForeignKey(Station)
    qs_education = models.CharField(max_length=64)
    qs_work_experience = models.IntegerField(help_text="Years of relevant experience")
    qs_training = models.IntegerField(help_text="Hours of relevant training")
    eligibility = models.CharField(max_length=8,
                                    choices=ELIGIBILITY_CHOICES,
                                    default=LET)
    is_open = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"

    def __unicode__(self):
        return "%s - %s" % (self.position, self.station)
