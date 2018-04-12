from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response  import Response
from rest_framework.request  import Request
from rest_framework.renderers import JSONRenderer
from io import BytesIO
from django.http import HttpResponse,HttpRequest
import base64
from .utils import get_translate_string
import os
import pickle
from .drawgraps import draw_dig_metric, draw_dig_path


class DigMetricView(APIView):
    '''
        Class for create dig metric graph.
    '''
    def get(self, request, format=None):
        '''
            return a dig metric graph created with dig metric data.
        '''
        locale = 'en'
        shift_start_timestamp = 0
        #parameter values
        if len(request.query_params) >0:
            locale = request.query_params.get('locale','en')
            shift_start_timestamp = request.query_params.get('shift_start_timestamp',None)
            
        pil_image = draw_dig_metric(shift_start_timestamp, locale)
        response = HttpResponse(content_type="image/png")
        pil_image.save(response,"PNG")
        return response

class DigPathView(APIView):
    '''
        Class for create dig path graph.
    '''
    def get(self, request, format=None):
        '''
            return a dig path graph created with dig path data.
        '''
        locale = 'en'
        equipment = ''
        #parameter values
        if len(request.query_params) >0:
            locale = request.query_params.get('locale','en')
            equipment = request.query_params.get('equipment',None)
            
        pil_image = draw_dig_path(equipment, locale)
        response = HttpResponse(content_type="image/png")
        pil_image.save(response,"PNG")
        return response