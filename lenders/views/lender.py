from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services.lenderSerivce import LenderService


class LenderView(APIView):
    polygon_view_get_desc = 'list all lender'


    @swagger_auto_schema(operation_description=polygon_view_get_desc)
    def get(self,requeest,*args,**kwargs):
        lenderService = LenderService()
        response = lenderService.list(requeest)
        return response

    polygon_view_get_desc = 'upload a lender'
    @swagger_auto_schema(operation_description=polygon_view_get_desc)
    def post(self,request,*args,**kwargs):
        lenderService = LenderService()
        res = lenderService.save(request.data)
        return Response(res)
