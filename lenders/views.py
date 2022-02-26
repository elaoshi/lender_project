# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from lenders.serializers import LenderSerializer


class LenderView(APIView):
    polygon_view_get_desc = 'list all lender'

    @swagger_auto_schema(operation_description=polygon_view_get_desc)
    def get(self,requeest,*args,**kwargs):
        data={
            "dd":'dd'
        }
        return Response(data)


