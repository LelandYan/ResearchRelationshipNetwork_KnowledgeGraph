from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,JsonResponse
import os
# Create your views here.
from xml.dom.minidom import parse
from toolkit.paper2kg.toolkit.pdf_parser import Parser
from toolkit.paper2kg.readXML import PaperXML
import os
import time
import nltk
import re
import json
from django.views.decorators.csrf import csrf_exempt


def index(request):
    template = loader.get_template('index.html')
    # if request.method == "POST":
    #     # print(request.POST)
    #     file = request.POST.get('action')
    #     # print(file)
    s = "Event List"
    context = {
        's': s,
    }
    return render(request, 'index.html', context)


def upload(request):
    linksData = None
    if request.method == "POST":
        f = request.FILES.get('file', None)
        with open(r'toolkit/paper2kg/ELG.pdf', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        start = time.time()
        parser = Parser('cermine')
        basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r"/toolkit/paper2kg"
        parser.parse('text', basedir + r'/ELG.pdf', basedir + r'/output', 0)
        # basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r"/toolkit/paper2kg"
        paper = PaperXML(basedir + '/output/ELG.cermine.xml', basedir)
        paper.paper2kg_d3js(confidence=0.3, max_entity_len=10, fine_grain=True)
        paper.paper2kg_d3js_basicInfo()
        print(time.time() - start)
        linksData = open(basedir + r"/paper_d3js_data.txt",encoding="utf8").read()
        # linksData = open(basedir + r"/section_d3js_data.txt").read()
        print(linksData)
    # return render(request, 'index.html', {"linksData": linksData})
    return JsonResponse(linksData, safe=False)


def notfound(request):
    return render(request, 'notfound.html')
