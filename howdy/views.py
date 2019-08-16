from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view
import mysql.connector
import json
from .checkinput import DateChecker
from .sqlrequest import *

@api_view(['GET'])
def detect_api(request):
    request_data = request.GET.dict()
    query=SqlRequest()
    query.__init__()
    try:
        status, result= query.request_all(request_data)
    except:
        query.__init__()
        status, result= query.request_all(request_data)
    if not status:
        return HttpResponseBadRequest("sai ngày tháng")
    else:
        return JsonResponse({"recevied": result})


@api_view(['GET'])
def one_detect_api(request):
    request_data = request.GET.dict()
    query=SqlRequest()
    try:
        status, result= query.request_one(request_data)      
    except:
        query.__init__()
        status, result= query.request_one(request_data)
    if not status:
        return HttpResponseBadRequest("sai ngày tháng")
    else:
        return JsonResponse({"recevied": result})
    
            
