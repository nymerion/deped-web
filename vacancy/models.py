from __future__ import unicode_literals
from django.db import models
from mezzanine.pages.models import Page

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
    CESO = 'CESO'

    ELIGIBILITY_CHOICES = (
        (LET, 'LET/PBET'),
        (PD, 'PD 907'),
        (CSC1, 'CSC LVL 1'),
        (CSC2, 'CSC LVL 2'),
        (CESO, 'CESO'),
    )
    position = models.ForeignKey(Position, default=0, related_name='qualification_standards')
    qualification = models.ForeignKey(Qualification, **optional)
    education = models.CharField(max_length=256)
    work_experience = models.CharField(max_length=256)
    training = models.IntegerField(help_text="Hours of relevant training")
    eligibility = models.CharField(max_length=8,
                                   choices=ELIGIBILITY_CHOICES,
                                   default=LET)
    notes = models.CharField(max_length=256, **optional)


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
    pub_date = models.DateField(**optional)
    close_date = models.DateField(**optional)
    is_open = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"

    def __unicode__(self):
        return "%s - %s" % (self.pub_date, self.close_date)

    def save(self, *args, **kwargs):
        """
        Add title, slug and ordering to the Page object
        """
        self.title = self.pub_date.strftime("%B %d, %Y")
        self.slug = ''
        if self.id is None:
            try:
                page = Page.objects.get(slug='vacancy')
                self.parent = page

                idx = 0
                done = False
                for vacancy in Vacancy.objects.filter(parent=page).order_by('-pub_date'):
                    if self.pub_date > vacancy.pub_date and not done:
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
        self.slug += "%s" % self.pub_date.strftime('%Y-%m-%d')
        super(Vacancy, self).save(*args, **kwargs)


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
