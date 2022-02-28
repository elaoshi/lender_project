from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_406_NOT_ACCEPTABLE

from lenders.services.lenderSerivce import LenderService


class LenderUploadView(generics.CreateAPIView):
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(operation_description='Upload csv file...',
                         manual_parameters=[openapi.Parameter(
                             name="file",
                             in_=openapi.IN_FORM,
                             type=openapi.TYPE_FILE,
                             required=True,
                             description="Document"
                         )],
                         )
    @action(detail=False, methods=['post'])
    def post(self, request):
        if 'file' in request.FILES:
            file = request.FILES['file'].file
        else:
            Response(status=HTTP_406_NOT_ACCEPTABLE)

        try:
            lender_service = LenderService()
            lender_service.bulk_upload(file)
        except Exception as e:
            print('Error While Importing Data: ', e)
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=HTTP_201_CREATED)
