from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from requests import Response
import numpy as np
import json, time, random
from datetime import datetime

# Create your views here.

def monitor(request):

    context = {}
    context.update({'tab_tittle':'Furuta Monitor',
                    'painel_tittle':'Simulação'})

    return render(request, 'monitor.html', context)

def chart_data(request):
    def generate_random_data():
        step = 0
        while True:
            json_data = json.dumps(
                {'time': step,
                 'Value':random.random()})
            yield f"data:{json_data}\n\n"
            time.sleep(2)
            step+=1
    response = StreamingHttpResponse(generate_random_data())
    response['Content-Type'] = 'text/event-stream'

    return response
