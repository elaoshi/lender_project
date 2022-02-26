# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from lenders.models import Lender
from lenders.serializers import LenderSerializer


class LenderView(generics.ListAPIView):
    queryset = Lender.objects.all()
    serializer_class = LenderSerializer
    filter_fields = ('category', 'in_stock')


