from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, generics
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.status import HTTP_201_CREATED, HTTP_406_NOT_ACCEPTABLE
# from rest_framework.views import APIView

from ..dao.LenderRepository import LenderRepository
from ..serializers import LenderSerializer
from ..services.lenderSerivce import MyPageNumberPagination


class LenderView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    lender_repository = LenderRepository()
    queryset = lender_repository.list_all()
    serializer_class = LenderSerializer
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        queryset = self.queryset
        active = self.request.query_params.get('active')
        if active is not None:
            return queryset.filter(active=active)
        return queryset

    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['active', 'name', 'code']

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
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    polygon_view_post_desc = 'Create a lender'
    @swagger_auto_schema(operation_description=polygon_view_post_desc,
                         request_body=LenderSerializer)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

