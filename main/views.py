import re
from openpyxl import Workbook
from openpyxl.styles import NamedStyle, Font, Border, Side
from openpyxl.styles.numbers import BUILTIN_FORMATS
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from django.shortcuts import render
from .models import Vacancy
import requests
import json


def base(request):
    # return render(request, 'main/base_template.html', {'title':'Базовая страница'})
    return render(request, 'main/base_template.html')


def home(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'main/index.html', {"name": "Anna", "title": "Тестовая страница"})


def index(request):  # HttpRequest
    vacancies = Vacancy.objects.all()  # from database
    print("hello world")
    res = f'<div><h3>{vacancies[0].name}</h3></div>'
    return HttpResponse(res)
    # return HttpResponse("страница приложения main")


def vacancies(request, vacancy_id):
    return HttpResponse(f"<h1>Некая вакансия с неким номером {vacancy_id}<h1>")


def relevance(request):
    return render(request, 'main/relevance.html', {"title": "Востребованность"})


def last_vacancies(request):
    url = 'https://api.hh.ru/dictionaries'
    url = 'https://api.hh.ru/vacancies?text=gamedev&order_by=publication_time&only_with_salary=true'
    response = requests.get(url, headers={"User-Agent": "api-test-agent"})
    data = response.json()
    vs = data['items']
    print(vs)
    vacancies = [get_correct_vacancy(v) for v in vs]
    for v in vs:
        print(v['published_at'])
    # resume_search_order":[{"id":"publication_time","name":"по дате изменения"}
    response = requests.get("https://api.hh.ru/vacancies/75582359", headers={"User-Agent": "api-test-agent"})
    v = response.json()

    return render(request, "main/vacancies.html", {"vacancies": vacancies[:5], 'vacancy': v, 'title': 'Последнии вакансии'})


def get_correct_vacancy(vacancy):
    """Удаляет лишние символы из вакансии

    Args:
        vacancy (dict): Словарь, значения которого нужно очистить от лишних символов

    Returns:
        dict: Вакансия с корректными значениями
    """

    def get_correct_string(s):
        """Удаляет лишние пробелы и html теги из строки

        Args:
            s (str): Строка

        Returns:
            str: Очищенная строка
        """
        s = re.sub("[^a-zA-Z]",  # Search for all non-letters
                              " ",  # Replace all non-letters with spaces
                              str(s))
        s = re.sub(r'<[^>]*>', '', s)
        result = []
        for item in s.split('\n'):
            result.append(' '.join(item.split()))
        return '\n'.join(result)

    return {key: get_correct_string(vacancy[key]) for key in vacancy}
