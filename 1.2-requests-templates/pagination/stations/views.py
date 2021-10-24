from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings

import csv


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    db_stations = []

    with open(settings.BUS_STATION_CSV, mode='r', encoding='utf-8') as data_file:
        stations_list = csv.DictReader(data_file)
        for station in stations_list:
            station = dict(
                Name=station['Name'],
                Street=station['Street'],
                District=station['District']
            )
            db_stations.append(station)

    paginator = Paginator(db_stations, 10)
    current_page = request.GET.get('page')
    page = paginator.get_page(current_page)
    bus_stations = page.object_list

    context = {
        'bus_stations': bus_stations,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
