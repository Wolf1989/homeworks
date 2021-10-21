from django.shortcuts import render, reverse
from django.http import HttpResponse
from django.conf import settings

import os, datetime, pytz


def home_view(request):
    template_name = 'app/home.html'
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir'),
    }
    context = {
        'pages': pages,
    }
    return render(request, template_name, context)


def time_view(request):
    tz_Moscow = pytz.timezone('Europe/Moscow')
    current_time = datetime.datetime.now(tz_Moscow).strftime('%d %b %Y, %A (%H:%M:%S)')
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    files_list = os.listdir(settings.BASE_DIR)
    msg = f'Список файлов в {settings.BASE_DIR}:<br>'
    for file in files_list:
        msg += '&nbsp' * 4 + file + '<br>'
    return HttpResponse(msg)