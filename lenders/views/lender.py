from django.shortcuts import render

# Create your views here.
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from ..serializers import LenderSerializer
from ..services.lenderSerivce import LenderService


class LenderView(APIView):
    """
        Get resultes.
        :param page:
        :rtype: BaseModel | None
        :return:

        """
    polygon_view_get_desc = 'List lender with filter'


    @swagger_auto_schema(
        operation_description=polygon_view_get_desc,
        manual_parameters=[
            openapi.Parameter(
                name='page',
                in_=openapi.IN_QUERY,
                description='Page',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='size',
                in_=openapi.IN_QUERY,
                description='Size of page',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='active',
                in_=openapi.IN_QUERY,
                description='Filter lender, 1 for actived , 0 for inactived',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description='lender id',
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self,request):

        lenderService = LenderService()

        response = lenderService.fetch(request)
        return response

    polygon_view_get_desc = 'Get lender with id'
    @swagger_auto_schema(
        operation_description=polygon_view_get_desc,
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description='lender id',
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    @action(detail=True)
    def retrieve(self, request, id=None):
        lenderService = LenderService()
        if id != None:
            response = lenderService.show(id)
        return response

    polygon_view_get_desc = 'Create a lender'
    @swagger_auto_schema(operation_description=polygon_view_get_desc,
                         request_body=LenderSerializer)
    def post(self,request,*args,**kwargs):
        lenderService = LenderService()
        res = lenderService.save(request.data)
        return Response(res,status=HTTP_201_CREATED)


    @swagger_auto_schema(
        operation_description=polygon_view_get_desc,
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description='lender id',
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def show(self,request,id=None):

        lenderService = LenderService()
        response = lenderService.fetch(id)
        return response