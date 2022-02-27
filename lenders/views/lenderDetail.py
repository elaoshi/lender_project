from django.shortcuts import render

# Create your views here.
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from ..serializers import LenderSerializer
from ..services.lenderSerivce import LenderService

class LenderDetailView(APIView):
    """
        Get resultes.
        :param page:
        :rtype: BaseModel | None
        :return:

        """

    polygon_view_get_desc = 'Get lender with id'
    @swagger_auto_schema(
        operation_description=polygon_view_get_desc,
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description='lender id',
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self,request,id):
        lenderService = LenderService()
        print('id is ',id)
        response = lenderService.show(id)
        if response == False:
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(response,status=HTTP_200_OK)


    polygon_view_put_desc = 'update a lender'
    @swagger_auto_schema(operation_description=polygon_view_put_desc,
                         request_body=LenderSerializer)
    @action(methods=['put'],detail=True)
    def put(self, request, id):
        lenderService = LenderService()
        res = lenderService.update(id,request.data)
        if res == False:
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(res, status=HTTP_200_OK)


    polygon_view_del_desc = 'delete a lender'
    @swagger_auto_schema(operation_description=polygon_view_del_desc)
    @action(methods=['delete'], detail=True)
    def delete(self, request, id):
        lenderService = LenderService()
        if lenderService.delete(id):
            return Response(status=HTTP_200_OK)
        else:
            return Response(status=HTTP_204_NO_CONTENT)
