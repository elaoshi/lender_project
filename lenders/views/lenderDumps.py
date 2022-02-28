from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.status import HTTP_201_CREATED

from lenders.services.lenderSerivce import LenderService


class LenderDumpView(generics.GenericAPIView):


    polygon_view_dump_desc = 'update a lender from csv file'
    @swagger_auto_schema(operation_description=polygon_view_dump_desc,)
    def post(self, request, *args, **kwargs):
        lender_service = LenderService()
        file_path = lender_service.dumps()
        return Response({"file_path":file_path}, status=HTTP_201_CREATED)
