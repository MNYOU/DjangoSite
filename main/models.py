from django.db import models

# Create your models here.

"""
name,key_skills,salary_from,salary_to,salary_currency,published_at
"""


class Vacancy(models.Model):
    name = models.TextField(default="программист")
    # key_skills = []
    # salary = models.ForeignKey()
    # published_at = models.DateTimeField(default="2003-10-07T00:00:00+0400")

    def __str__(self):
        # return self.name
        return "Вакансия"


class Salary(models.Model):
    salary_from = models.FloatField
    salary_to = models.FloatField
    salary_currency = models.CharField(max_length=10)

    def __str__(self):
        return "Статья"


# class Graph(models.Model):
#     image = models.ImageField(upload_to="photos/")