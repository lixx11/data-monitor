from django.shortcuts import render, HttpResponse
from django.template import loader
from pyecharts import Line
import math
from django.conf import settings
import numpy as np


REMOTE_HOST = "https://pyecharts.github.io/assets/js"


# Create your views here.
def index(request):
    template = loader.get_template('monitor/index.html')
    data = np.loadtxt(settings.DATA_PATH)
    data_x = data[:, 0].tolist()
    data_y = data[:, 1].tolist()
    line = Line('', width=1000, height=600)
    line.add(
        '', data_x, data_y,
        is_xaxislabel_align=True,
        datazoom_range=[0, 100],
        is_datazoom_show=True,
        datazoom_type='both',
        is_more_utils=True
        )
    context = dict(
        myechart=line.render_embed(),
        host=REMOTE_HOST,
        script_list=line.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))
