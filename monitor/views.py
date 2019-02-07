from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.template import loader
from django.conf import settings
import numpy as np
from glob import glob
import os
from datetime import datetime
import json
import csv


TRANSFORM = {
    'identity': lambda x: x,
    'log': lambda x: np.log(x),
    'custom': lambda x: np.sin(x)*np.sqrt(x),
}


def index(request):
    template = loader.get_template('monitor/index.html')
    context = {
        'HOST': settings.HOST
    }
    return HttpResponse(template.render(context, request))


def data_summary(request):
    data_files = glob('%s/*.txt' % settings.DATA_DIR)
    data_items = []
    for data_file in data_files:
        basename = os.path.basename(data_file)
        latest_val = np.loadtxt(data_file)[-1][1]
        update_time = datetime.fromtimestamp(
            os.path.getmtime(data_file)
        ).strftime('%Y-%m-%d %H:%M:%S')
        data_items.append({
            'filename': basename,
            'latest_value': latest_val,
            'update_time': update_time,
        })
    return JsonResponse(data_items, safe=False)


def data(request, filename):
    transform = request.GET['transform']
    filepath = os.path.join(settings.DATA_DIR, filename)
    data = np.loadtxt(filepath)
    data[:, 1] = np.array(TRANSFORM[transform](data[:, 1]))
    return HttpResponse(json.dumps(data.tolist()), content_type='application/json')
