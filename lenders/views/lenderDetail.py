from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from ..dao.LenderRepository import LenderRepository
from ..serializers import LenderSerializer
from ..services.lenderSerivce import LenderService


class LenderDetailView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    lender_repository = LenderRepository()
    queryset = lender_repository.list_all()
    serializer_class = LenderSerializer

    """
        Get resultes.
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
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    polygon_view_put_desc = 'update a lender'

    @swagger_auto_schema(operation_description=polygon_view_put_desc,
                         request_body=LenderSerializer)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    polygon_view_del_desc = 'delete a lender'

    @swagger_auto_schema(operation_description=polygon_view_del_desc)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
