from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_406_NOT_ACCEPTABLE
from rest_framework.views import APIView

from ..serializers import LenderSerializer
from ..services.lenderSerivce import LenderService


class LenderView(APIView):
    """
        Get resultes.
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
            )
        ]
    )
    def get(self, request):
        """
           Fetch lenders
        """
        lender_repository: LenderService = LenderService()

        response = lender_repository.fetch(request)
        return response

    polygon_view_get_desc = 'Create a lender'

    @swagger_auto_schema(operation_description=polygon_view_get_desc,
                         request_body=LenderSerializer)
    def post(self, request, *args, **kwargs):
        """
           Create lender
        """
        lender_repository: LenderService = LenderService()

        res = lender_repository.save(request.data)
        if res is False:
            return Response(status=HTTP_406_NOT_ACCEPTABLE)
        return Response(res, status=HTTP_201_CREATED)

    """
        create lender csv dumpfile
    """
    polygon_view_get_desc = 'Dump a lender CSV'

    @swagger_auto_schema(operation_description=polygon_view_get_desc)
    @action(methods=['post'], detail=False)
    def dumps(self, request, *args, **kwargs):
        """
           Export lender to csv
        """
        lender_repository: LenderService = LenderService()
        file_path = lender_repository.dumps()
        return Response({"file_path": file_path}, status=HTTP_201_CREATED)
